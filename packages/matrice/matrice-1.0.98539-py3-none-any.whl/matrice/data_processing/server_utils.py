import os
import requests
import shutil
import logging
import zipfile
import tarfile
from collections import defaultdict
from urllib.parse import urlparse
import uuid
import base64
import traceback
import math
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
from matrice.data_processing.client_utils import is_file_compressed

def get_corresponding_split_type(path: str, include_year: bool = False) -> str:
    """
    Get the split type (train/val/test) from a file path.
    """
    split_types = ["train", "val", "test"]
    
    text_parts = path.split(os.sep)
    split_type = next(
        (key for part in text_parts for key in split_types if key in part.lower()),
        "unassigned"
    )

    if split_type != "unassigned" and include_year:
        year = ''.join(filter(str.isdigit, path))
        return f"{split_type}{year}" if year else split_type
    return split_type


def construct_relative_path(dataset_id, folder_name, file_name):
    return f"{dataset_id}/images/{folder_name}/{file_name}"


def download_file(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Create parent directory if it doesn't exist
        parent_dir = os.path.dirname(file_path)
        if parent_dir:
            try:
                os.makedirs(parent_dir, exist_ok=True)
            except Exception as e:
                logging.error(f"Error creating directory: {str(e)}")
                raise

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        logging.debug(f"Successfully downloaded file {url} to {file_path}")
        return file_path

    except Exception as e:
        logging.error(f"Error downloading file: {str(e)}")
        raise


def get_batch_pre_signed_download_urls(file_location, rpc, bucket_alias="", account_number=""):
    resp = rpc.post(
        "/v2/dataset/get_batch_pre_signed_download_urls",
        payload={
            "fileNames": [file_location],
            "type": "samples",
            "isPrivateBucket": True if bucket_alias else False,
            "bucketAlias": bucket_alias,
            "accountNumber": account_number,
        },
    )
    return resp["data"][file_location]


def get_filename_from_url(url):
    parsed_url = urlparse(url)
    file_name = parsed_url.path.split('/')[-1]
    return file_name


def rpc_get_call(rpc, path, params={}):
    resp= rpc.get(path=path, params=params)
    if resp['success']:
        return resp["data"]
    else:
        logging.error(f"Failed to get response for path: {path} , response: {resp}")
        return None

def update_partition_status(rpc, action_record_id, dataset_id, version, partition, status, partition_items, annotation_type):
    logging.debug(f"Updating partition status for partition items {partition_items}")
    try:
        class_stats = get_classwise_splits(partition_items, annotation_type)
        status_update_payload = {
            "classStat": class_stats,
            "actionRecordId": action_record_id,
            "targetVersion": version,
            "partitionNumber": partition,
            "status": status,
        }
        logging.debug(f"Updating partition status for partition {partition} to {status_update_payload}")
        resp = rpc.put(
            path=f"/v2/dataset/update-partition-status/{dataset_id}",
            payload=status_update_payload,
        )
        if resp['success']:
            logging.info(f"Successfully updated partition status for partition {partition} to {status}, response: {resp}")
            return resp["data"]
        else:
            error_msg = f"Failed to update partition status: {resp}"
            logging.error(error_msg)
    except Exception as e:
        logging.error(f"Error updating partition status: {str(e)}")
        raise

def get_unprocessed_partitions(rpc, dataset_id, version):
    unprocessed_partitions_response = rpc_get_call(
        rpc,
        f"/v2/dataset/get_unprocessed_partitions/{dataset_id}/version/{str(version)}",
        params={},
    )
    if unprocessed_partitions_response is None:
        return []
    unprocessed_partitions = list(
        set(x["partitionNum"] for x in unprocessed_partitions_response)
    )
    logging.info(f"Found {len(unprocessed_partitions)} unprocessed partitions: {unprocessed_partitions}")
    return unprocessed_partitions

def generate_short_uuid():
    return base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b'=').decode('utf-8')

def delete_tmp_folder(tmp_folder_path):
    """Delete the temporary folder."""
    logging.info(f"Attempting to delete temporary folder: {tmp_folder_path}")
    if os.path.exists(tmp_folder_path):
        shutil.rmtree(tmp_folder_path)
        logging.info(f"Temporary folder {tmp_folder_path} has been deleted.")
        print(f"Temporary folder {tmp_folder_path} has been deleted.")

def extract_dataset(dataset_path, get_inner_dir=False):
    logging.info(f"Extracting dataset from {dataset_path}")
    extract_dir = os.path.splitext(dataset_path)[0]
    os.makedirs(extract_dir, exist_ok=True)

    try:
        if dataset_path.endswith('.zip'):
            logging.debug("Extracting ZIP archive")
            with zipfile.ZipFile(dataset_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
                
        elif dataset_path.endswith(('.tar', '.tar.gz', '.tar.bz2', '.tar.xz')):
            logging.debug("Extracting TAR archive")
            mode = 'r:*'  # Auto-detect compression
            with tarfile.open(dataset_path, mode) as tar_ref:
                tar_ref.extractall(extract_dir)
        
        else:
            raise ValueError(f"Unsupported archive format for file: {dataset_path}")
        
        if get_inner_dir:
            extracted_path = os.path.join(extract_dir, [path for path in os.listdir(extract_dir) if not (path.startswith("_") or path.startswith("."))][0])
        else:
            extracted_path = extract_dir
        logging.info(f"Successfully extracted dataset to: {extracted_path}")
        return extracted_path
        
    except Exception as e:
        logging.error(f"Error extracting dataset: {str(e)}")
        raise

def get_classwise_splits(partition_items, annotation_type="classification"):
    logging.debug(f"Getting classwise splits for {len(partition_items)} items with annotation type: {annotation_type}")
    classwise_splits = defaultdict(
        lambda: {"train": 0, "test": 0, "val": 0, "unassigned": 0, "total": 0}
    )
    for item in partition_items:
        split_type = item.get("splitType")
        annotations = item.get("annotations")
        try:
            if not annotations:
                continue
            if annotation_type == "detection":
                for annotation in annotations:
                    category = annotation.get("category")
                    if category and split_type:
                        classwise_splits[category][split_type] += 1
            elif annotation_type == "classification":
                category = annotations[0].get("category")
                if category and split_type:
                    classwise_splits[category][split_type] += 1
        except Exception as e:
            logging.error(f"Error processing item {item}: {str(e)}")
    # Only return if there are actual classes found
    if not classwise_splits:
        logging.warning("No classes found in partition items")
        return {}
    # Calculate total for each category
    for category, counts in classwise_splits.items():
        counts["total"] = sum(counts.values())
    logging.debug(f"Final classwise splits: {dict(classwise_splits)}")
    return classwise_splits

def update_action_status(
    action_record_id,
    action_type,
    step_code,
    status,
    status_description,
    rpc
):
    """Updates action status."""
    url = "/v1/project/action"
    payload = {
        "_id": action_record_id,
        "stepCode": step_code,
        "status": status,
        "statusDescription": status_description,
        "serviceName": "be-dataset",
        "action": action_type,
        "subAction": action_type,
    }
    rpc.put(url, payload)

def log_error(action_record_id, exception, filename, function_name, rpc):
    """Log error to be-system."""
    traceback_str = traceback.format_exc().rstrip()
    log_err = {
        "actionRecordID": action_record_id,
        "serviceName": "Data-Processing",
        "stackTrace": traceback_str,
        "errorType": "Internal",
        "description": str(exception),
        "fileName": filename,
        "functionName": function_name,
        "moreInfo": {},
    }
    error_logging_route = "/v1/system/log_error"
    rpc.post(url=error_logging_route, data=log_err)
    print("An exception occurred. Logging the exception information:")

def chunk_items(
    items: List[Dict[str, Any]], chunk_size: int
) -> List[List[Dict[str, Any]]]:
    """Chunk items into smaller batches.

    Args:
        items: List of items to chunk
        chunk_size: Size of each chunk

    Returns:
        List of chunked item batches
    """
    if not items:
        logging.warning("No valid items to chunk")
        return []

    len_items = len(items)
    return [
        items[i : min(i + chunk_size, len_items)]
        for i in range(0, len_items, chunk_size)
    ]

def fetch_items(
    rpc: Any,
    path: str,
    request_batch_size: int,
    page_number: int = None,
    download_images_required: bool = False,
) -> List[Dict[str, Any]]:
    """Fetch items from the dataset API.

    Args:
        rpc: RPC client for making API calls
        path: API path to fetch items
        request_batch_size: Number of items to fetch per page
        page_number: Page number to fetch (optional)
        download_images_required: Whether to get presigned URLs for images

    Returns:
        List of dataset items
    """
    if page_number is not None:
        path += f"?isPresignedURLRequired={'true' if download_images_required else 'false'}&pageNumber={page_number}&pageSize={request_batch_size}"

    response = rpc_get_call(rpc=rpc, path=path)

    if not response:
        logging.error(f"Failed to get response for path: {path}")
        return []

    return response.get("items", [])


def get_batch_partition_items(
    rpc: Any,
    dataset_id: str,
    partition: int,
    page_number: int,
    download_images_required: bool = False,
    request_batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """Get a batch of items from a specific partition page."""
    path = f"/v2/dataset/list-partition-items/{dataset_id}/{partition}"
    batch_items = fetch_items(rpc, path, request_batch_size, page_number, download_images_required)

    return [{**item, "partition": partition} for item in batch_items if item]


def get_number_of_partition_pages(
    rpc: Any, dataset_id: str, partition: int, request_batch_size: int
) -> int:
    """Calculate total number of pages for a partition."""
    path = f"/v2/dataset/list-partition-items/{dataset_id}/{partition}"
    response = rpc_get_call(rpc=rpc, path=path)

    if not response:
        logging.error(f"Failed to get total items for partition {partition}")
        return 0

    total_items = response.get("total", 0)
    return math.ceil(total_items / request_batch_size)


def get_partition_items(
    rpc: Any,
    dataset_id: str,
    partition: int,
    download_images_required: bool = False,
    request_batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """Get items for a partition."""
    number_of_partition_pages = get_number_of_partition_pages(rpc, dataset_id, partition, request_batch_size)

    if number_of_partition_pages == 0:
        logging.warning(f"No items found for partition {partition}")
        return []

    all_dataset_items = []
    with ThreadPoolExecutor(max_workers=number_of_partition_pages) as executor:
        futures = [
            executor.submit(
                get_batch_partition_items,
                rpc,
                dataset_id,
                partition,
                page_number,
                download_images_required,
                request_batch_size,
            )
            for page_number in range(number_of_partition_pages)
        ]

        for future in futures:
            try:
                all_dataset_items.extend(future.result())
            except Exception as e:
                logging.error(f"Error getting batch for partition {partition}: {e}")

    return all_dataset_items


def get_batch_dataset_items(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    page_number: int,
    request_batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """Get a batch of items from a specific dataset version page."""
    path = f"/v2/dataset/item/{dataset_id}/version/{dataset_version}"
    return fetch_items(rpc, path, request_batch_size, page_number)


def get_number_of_dataset_pages(
    rpc: Any, dataset_id: str, dataset_version: str, request_batch_size: int
) -> int:
    """Calculate total number of pages for a dataset."""
    path = f"/v2/dataset/item/{dataset_id}/version/{dataset_version}"
    response = rpc_get_call(rpc=rpc, path=path)

    if not response:
        logging.error(f"Failed to get total items for dataset {dataset_id} version {dataset_version}")
        return 0

    total_items = response.get("total", 0)
    return math.ceil(total_items / request_batch_size)


def get_dataset_items(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    request_batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """Get items for a dataset."""
    number_of_dataset_pages = get_number_of_dataset_pages(rpc, dataset_id, dataset_version, request_batch_size)

    if number_of_dataset_pages == 0:
        logging.warning(f"No items found for dataset {dataset_id} version {dataset_version}")
        return []

    all_dataset_items = []
    with ThreadPoolExecutor(max_workers=number_of_dataset_pages) as executor:
        futures = [
            executor.submit(
                get_batch_dataset_items,
                rpc,
                dataset_id,
                dataset_version,
                page_number,
                request_batch_size,
            )
            for page_number in range(number_of_dataset_pages)
        ]

        for future in futures:
            try:
                all_dataset_items.extend(future.result())
            except Exception as e:
                logging.error(f"Error getting batch for dataset {dataset_id} version {dataset_version}: {e}")

    return all_dataset_items


def handle_source_url_dataset_download(source_URL) -> str:
    logging.info("Processing dataset from URL: %s", source_URL)
    dataset_path = download_file(
        source_URL, source_URL.split("?")[0].split("/")[-1]
    )
    if is_file_compressed(dataset_path):
        dataset_path = extract_dataset(dataset_path, get_inner_dir=True)
    logging.info("Dataset path: %s", dataset_path)
    return dataset_path


# def is_classwise_balanced(classwise_splits):
#     """
#     Checks if the distribution of class counts is balanced within an
#     acceptable percentage range.
#     """
#     logging.info("Checking class-wise balance")
#     class_counts = [info["total"] for info in classwise_splits.values()]
#     total_count = sum(class_counts)
#     # Define the acceptable percentage range (50% to 200%) as fractions
#     min_percentage = 0.5  # 50% as fraction
#     max_percentage = 2.0  # 200% as fraction
#     try:
#         avg_count = total_count / len(class_counts)
#         logging.debug(f"Average count per class: {avg_count}")
#     except Exception as e:
#         logging.warning("Unable to calculate average count, defaulting to balanced", exc_info=True)
#         return True
#     # Calculate the minimum and maximum acceptable average number of images per class
#     min_avg_count = avg_count * min_percentage
#     max_avg_count = avg_count * max_percentage
#     # Check if the count for each class falls within the acceptable range
#     for count in class_counts:
#         if count < min_avg_count or count > max_avg_count:
#             logging.info(f"Class count {count} outside acceptable range [{min_avg_count}, {max_avg_count}]")
#             return False
#     logging.info("Class-wise balance check passed")
#     return True

# def is_splitwise_balanced(classwise_splits):
#     """
#     Checks whether the dataset splits (train, test, val, unassigned) are balanced with respect to the categories.
#     """
#     logging.info("Checking split-wise balance")
#     # Initialize a set for each split to track categories
#     train_categories = set()
#     test_categories = set()
#     val_categories = set()
#     unassigned_categories = set()

#     # Iterate through the categories and populate the split sets
#     for category, splits in classwise_splits.items():
#         if splits["train"] > 0:
#             train_categories.add(category)
#         if splits["test"] > 0:
#             test_categories.add(category)
#         if splits["val"] > 0:
#             val_categories.add(category)
#         if splits["unassigned"] > 0:
#             unassigned_categories.add(category)

#     # Get the union of all categories across splits
#     all_categories = train_categories | test_categories | val_categories | unassigned_categories
#     logging.debug(f"Total unique categories found: {len(all_categories)}")

#     # Check if each split contains all the categories in the union
#     if (train_categories == all_categories and
#         test_categories == all_categories and
#         val_categories == all_categories):
#         logging.info("Split-wise balance check passed")
#         return True
#     else:
#         logging.info("Split-wise balance check failed - not all splits contain all categories")
#         logging.debug(f"Missing categories in train: {all_categories - train_categories}")
#         logging.debug(f"Missing categories in test: {all_categories - test_categories}")
#         logging.debug(f"Missing categories in val: {all_categories - val_categories}")
#         return False

# def update_dataset_class_splits(rpc, dataset_id, version, classwise_splits, splitwise_balanced, classwise_balanced):
#     logging.info(f"Updating dataset class splits for dataset {dataset_id} version {version}")
#     update_split_payload={
#                 "datasetID": dataset_id,
#                 "version":version,
#                 "classWiseSplits":classwise_splits,
#                 "isSplitWiseBalanced":splitwise_balanced,
#                 "isClassWiseBalanced":classwise_balanced
#             }
#     try:
#         resp = rpc.put(path="/v2/dataset/update-dataset-class-splits", payload=update_split_payload)
#         if resp['success']:
#             logging.info(f"Successfully updated dataset class splits with {update_split_payload}")
#             return resp["data"]
#         else:
#             error_msg = f"Failed to update dataset class splits: {resp['message']}"
#             logging.error(error_msg)
#     except Exception as e:
#         logging.error(f"Error updating dataset class splits: {str(e)}", exc_info=True)

# def add_dataset_class_splits_info(rpc, dataset_id, dataset_version, classwise_splits):
#     classwise_balanced = is_classwise_balanced(classwise_splits)
#     splitwise_balanced = is_splitwise_balanced(classwise_splits)
#     logging.info(
#         f"Class balance: {classwise_balanced}, Split balance: {splitwise_balanced}"
#     )
#     update_dataset_class_splits(
#         rpc,
#         dataset_id,
#         dataset_version,
#         classwise_splits,
#         splitwise_balanced,
#         classwise_balanced,
#     )
