import os
import logging
import requests
import zipfile

MAX_PARTITION_SIZE_BYTES = 2 * 1024 * 1024 * 1024  # 2GB
ANNOTATION_EXTENSIONS = [".json", ".txt", ".xml", ".ndjson", ".yaml"]
SAMPLES_EXTENSIONS = [
    # Image formats
    ".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp",
    # Video formats 
    ".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv", ".webm"
]
COMPRESSED_EXTENSIONS = [
    ".zip",
    ".tar",
    ".tar.gz",
    ".tar.bz2",
    ".tar.xz",
    ".gz",
    ".bz2",
    ".xz",
    ".7z",
    ".rar",
]
ANNOTATION_PARTITION_TYPE = "annotation"
SAMPLES_PARTITION_TYPE = "samples"

def get_size_mb(path):
    """Calculate total size in MB for a file, folder, or list of paths."""
    total_size = 0

    def get_file_size(file_path):
        if os.path.isfile(file_path) and not os.path.islink(file_path):
            return os.path.getsize(file_path)
        return 0

    def get_folder_size(folder_path):
        size = 0
        for dirpath, _, filenames in os.walk(folder_path):
            for filename in filenames:
                size += get_file_size(os.path.join(dirpath, filename))
        return size

    if isinstance(path, (list, tuple)):
        for p in path:
            total_size += get_file_size(p) if os.path.isfile(p) else get_folder_size(p)
    else:
        total_size += (
            get_file_size(path) if os.path.isfile(path) else get_folder_size(path)
        )

    return -(-total_size // (1024 * 1024))

def scan_folder(folder_path):
    file_paths = []
    for root, _, files in os.walk(folder_path):
        # Skip directories that contain 'SegmentationClass' or 'SegmentationObject' in their respective path
        if "SegmentationClass" in root or "SegmentationObject" in root:
            continue
        
        for filename in files:
            file_paths.append(os.path.join(root, filename))
    
    return file_paths

def scan_dataset(base_path):
    logging.debug(f"Scanning dataset at {base_path}")
    annotation_files = []
    image_files = []
    
    file_paths = scan_folder(base_path)
    
    for file_path in file_paths:
        _, ext = os.path.splitext(file_path.lower())
        if ext in ANNOTATION_EXTENSIONS:
            annotation_files.append(file_path)
        elif ext in SAMPLES_EXTENSIONS:
            image_files.append(file_path)

    logging.debug(f"Found {len(annotation_files)} annotation files and {len(image_files)} image files")
    return annotation_files, image_files

def get_images_partitions(image_files):
    """Split image files into partitions and return partition stats."""
    logging.debug("Creating image partitions")
    partitions = []
    current_partition = []
    current_size = 0
    partition_num = 1

    def create_partition(files, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(files),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": files,
        }

    for image_file in image_files:
        file_size = os.path.getsize(image_file)

        if current_size + file_size > MAX_PARTITION_SIZE_BYTES:
            partitions.append(
                create_partition(current_partition, current_size, partition_num)
            )
            partition_num += 1
            current_partition = [image_file]
            current_size = file_size
        else:
            current_partition.append(image_file)
            current_size += file_size

    if current_partition:
        partitions.append(
            create_partition(current_partition, current_size, partition_num)
        )

    logging.debug(f"Created {len(partitions)} image partitions")
    return partitions

def get_annotations_partition(annotation_files):
    logging.debug("Creating annotations partition")
    return {
        "partitionNum": 0,
        "sampleCount": len(annotation_files),
        "diskSizeMB": get_size_mb(annotation_files),
        "type": ANNOTATION_PARTITION_TYPE,
        "files": annotation_files,
    }


def get_cloud_file_path(dataset_id, dataset_version, base_dataset_path, file_path, include_version_in_cloud_path=False):
    if include_version_in_cloud_path:
        return os.path.join(dataset_id, dataset_version, os.path.relpath(file_path, base_dataset_path)).replace(os.sep, "/")
    else:
        return os.path.join(dataset_id, os.path.relpath(file_path, base_dataset_path)).replace(os.sep, "/")


def get_batch_pre_signed_upload_urls(cloud_file_paths, rpc, type, bucket_alias="", account_number=""):
    logging.debug(f"Getting presigned URLs for {len(cloud_file_paths)} files")
    resp = rpc.post(
        "/v2/dataset/get_batch_pre_signed_upload_urls",
        payload={
            "fileNames": cloud_file_paths,
            "type": type,
            "isPrivateBucket": True if bucket_alias else False,
            "bucketAlias": bucket_alias,
            "accountNumber": account_number,
        },
    )
    if resp["success"]:
        return resp["data"]
    else:
        logging.error(f"Failed to get presigned URLs: {resp['message']}")
        return resp["message"]

def upload_file(local_path, presigned_url, max_attempts=5):
    if not presigned_url:
        logging.error(f"Missing presigned URL for {local_path}")
        return False
    for attempt in range(max_attempts):
        try:
            with open(local_path, "rb") as f:
                response = requests.put(presigned_url, data=f)
                if response.status_code == 200:
                    logging.debug(f"Successfully uploaded {local_path} to {presigned_url}")
                    return True
                else:
                    logging.warning(
                        f"Failed to upload {local_path} (status: {response.status_code}), "
                        f"attempt {attempt + 1}/{max_attempts}"
                    )
                    response.raise_for_status()
        except Exception as e:
            if attempt == max_attempts - 1:
                logging.error(
                    f"Failed to upload {local_path} after {max_attempts} attempts. Error: {e}"
                )
                return False
            else:
                logging.warning(
                    f"Attempt {attempt + 1}/{max_attempts} failed for {local_path}. "
                    f"Retrying... Error: {e}"
                )

def update_annotation_bucket_url(rpc, dataset_id, partition_number, annotation_bucket_url):
    payload = {
        "partitionNumber": partition_number,
        "path": annotation_bucket_url,
    }
    logging.debug(f"Updating annotation bucket URL for partition {partition_number} with URL: {annotation_bucket_url}")
    url = f"/v2/dataset/update_annotation_path/{dataset_id}"
    response = rpc.post(url, payload=payload)
    return response


def upload_compressed_dataset(rpc, dataset_path, bucket_alias="", account_number=""):
    file_name = os.path.basename(dataset_path)
    presigned_urls = get_batch_pre_signed_upload_urls([file_name], rpc, "compressed", bucket_alias, account_number)
    upload_url = presigned_urls[file_name]
    upload_file(dataset_path, upload_url)
    return upload_url.split("?")[0]

def compress_annotation_files(file_paths, base_dataset_path):
    zip_file_path = os.path.join(base_dataset_path,"annotations.zip")
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            zipf.write(file_path, arcname=os.path.relpath(file_path, base_dataset_path).replace(os.sep, "/"))
    logging.info(f"Files zipped successfully into {zip_file_path}")
    return zip_file_path

def is_file_compressed(file_path):
    _, ext = os.path.splitext(file_path.lower())
    return ext in COMPRESSED_EXTENSIONS


def update_partitions_numbers(rpc, dataset_id, items, partition_key="partitionNum"):
    try:
        logging.info(f"Updating partition numbers for dataset {dataset_id}")
        dataset_info = rpc.get(f"/v2/dataset/{dataset_id}").get("data")
        if dataset_info:
            dataset_partition_stats = dataset_info.get("partitionStats")
            if dataset_partition_stats:
                max_partition_num = max(
                    [p["partitionNum"] for p in dataset_partition_stats]
                )
                for item in items:
                    item[partition_key] = max_partition_num + item[partition_key]
    except Exception as e:
        logging.error(f"Error updating partition numbers: {e}")
    return items

def complete_dataset_items_upload(
    rpc, dataset_id, partition_stats, target_version="v1.0", source_version="", action_type="data_import",
):
    logging.info(f"Completing dataset items upload for dataset {dataset_id}")
    url = "/v2/dataset/complete_dataset_items_upload"
    payload = {
	"action":action_type,
	"_id":dataset_id,
	"sourceVersion":source_version,
    "targetVersion":target_version,
	"totalSample":sum([p["sampleCount"] for p in partition_stats if p["type"] == SAMPLES_PARTITION_TYPE]),
	"partitionInfo":[{
        "partitionNum": p["partitionNum"],
        "sampleCount": p["sampleCount"],
        "diskSizeMB": p["diskSizeMB"],
        "type": p["type"]
    } for p in partition_stats if p["type"] == SAMPLES_PARTITION_TYPE]
}
    logging.info(f"Payload: {payload}")
    response = rpc.post(url, payload=payload)
    logging.info(f"Response: {response}")
    return response

def create_partition_stats(rpc, partition_stats, dataset_id, target_version, source_version=""):
    logging.info(f"Creating partition stats for dataset {dataset_id}")

    # Filter out None values from partition_stats
    new_partition_stats = [stat for stat in partition_stats if stat is not None]

    payload = {
        "datasetId": dataset_id,
        "sourceVersion": source_version,
        "targetVersion": target_version,
        "partitionStats": new_partition_stats
    }
    
    url = "/v2/dataset/create-partition"
    logging.debug(f"Making request to {url} with payload: {payload}")
    response = rpc.post(url, payload=payload)
    logging.debug(f"response after calling create-partition API: {response}")
    
    return response
