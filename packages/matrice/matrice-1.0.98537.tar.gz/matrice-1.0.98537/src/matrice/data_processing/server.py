import os
import traceback
import logging
from queue import Queue
from PIL import Image
from typing import List, Dict, Any, Optional
import cv2

from matrice.data_processing.data_formats.mscoco_detection import (
    get_msococo_images_details,
    add_mscoco_dataset_items_details,
)
from matrice.data_processing.data_formats.imagenet_classification import (
    add_imagenet_dataset_items_details,
)
from matrice.data_processing.data_formats.pascalvoc_detection import (
    get_pascalvoc_image_details,
    add_pascalvoc_dataset_items_details,
)
from matrice.data_processing.data_formats.labelbox_detection import (
    get_labelbox_image_details,
    add_labelbox_dataset_items_details,
    add_labelbox_dataset_item_local_file_path,
    download_labelbox_dataset
)
from matrice.data_processing.data_formats.labelbox_classification import (
    get_labelbox_classification_image_details,
    add_labelbox_classification_dataset_items_details,
    add_labelbox_classification_dataset_item_local_file_path,
    download_labelbox_classification_dataset
)
from matrice.data_processing.data_formats.yolo_detection import (
    get_yolo_image_details,
    add_yolo_dataset_items_details,
    convert_payload_to_coco_format,
)
from matrice.data_processing.data_formats.unlabelled import (
    add_unlabelled_dataset_items_details
)
from matrice.data_processing.data_formats.video_mscoco_detection import (
    get_msococo_videos_details,
    add_mscoco_video_dataset_items_details
)
from matrice.data_processing.server_utils import (
    download_file,
    rpc_get_call,
    get_batch_pre_signed_download_urls,
    get_filename_from_url,
    update_partition_status,
    get_unprocessed_partitions,
    extract_dataset,
    get_partition_items,
    chunk_items,
    handle_source_url_dataset_download
)
from matrice.data_processing.client_utils import scan_folder
from matrice.data_processing.pipeline import Pipeline

# Create tmp folder in a more robust way
TMP_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")
os.makedirs(TMP_FOLDER, exist_ok=True)
logging.info(f"Created temporary folder at {TMP_FOLDER}")

def download_dataset(source_URL="", input_type="", dataset_id="", rpc="", dataset_version="") -> str:
    if (input_type == "labelbox" or input_type=="labelbox_classification") and not source_URL:
        logging.info("Downloading annotation file for labelbox dataset")
        dataset_path = get_annotation_files(
            rpc, dataset_id, dataset_version, False
        )[0]
    else:
        dataset_path = handle_source_url_dataset_download(source_URL)
    if (input_type == "labelbox" or input_type=="labelbox_classification"):
        logging.info("Downloading dataset from labelbox")
        dataset_path = download_labelbox_dataset(dataset_id, dataset_path)
    return dataset_path

def partition_items_producer(
    rpc: Any,
    dataset_id: str,
    partition: int,
    pipeline_queue: Queue,
    download_images_required: bool = False,
    request_batch_size: int = 1000,
    processing_batch_size: int = 10,
) -> None:
    """Get items for a partition and add them to the pipeline queue.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        partition: Partition number
        pipeline_queue: Queue to add items to
        download_images_required: Whether to get presigned URLs for images
        request_batch_size: Number of items to fetch per API request
        processing_batch_size: Size of batches to add to pipeline queue
    """
    try:
        # Get items for the partition
        all_dataset_items = get_partition_items(
            rpc,
            dataset_id,
            partition,
            download_images_required,
            request_batch_size,
        )

        # Chunk items into processing batches
        processing_batches = chunk_items(all_dataset_items, processing_batch_size)

        # Add batches to the pipeline queue
        for batch in processing_batches:
            pipeline_queue.put(batch)

        logging.info(
            f"Successfully fetched {len(all_dataset_items)} items for partition {partition}"
        )

    except Exception as e:
        logging.error(f"Error processing partition {partition}: {e}")
        traceback.print_exc()


def download_samples(image_details: Dict[str, Any], rpc: Any, bucket_alias: str="", account_number: str="") -> Dict[str, Any]:
    """Download sample and update sample details.

    Args:
        image_details: Dictionary containing image metadata
        rpc: RPC client for making API calls
        bucket_alias: Bucket alias
        account_number: Account number

    Returns:
        Updated sample details dictionary
    """
    if image_details.get("is_complete"):
        return image_details

    dataset_item = image_details.get("sample_details")

    try:
        if not dataset_item.get("cloudPath"):
            dataset_item["cloudPath"] = get_batch_pre_signed_download_urls(
                dataset_item.get("fileLocation"), rpc, bucket_alias, account_number
            )
        if not dataset_item.get("local_file_path"):
            dataset_item["local_file_path"] = os.path.join(
                TMP_FOLDER, dataset_item["filename"]
            )

        # Create subdirectories if needed
        os.makedirs(os.path.dirname(dataset_item["local_file_path"]), exist_ok=True)

        download_file(dataset_item["cloudPath"], dataset_item["local_file_path"])
        return {"sample_details": dataset_item, "is_complete": False}

    except Exception as e:
        logging.error(f"Error downloading image {dataset_item.get('filename')}: {e}")
        return {"sample_details": dataset_item, "is_complete": False}


def batch_download_samples(
    batch_image_details: List[Dict[str, Any]], rpc: Any, bucket_alias: str="", account_number: str=""
) -> List[Dict[str, Any]]:
    """Download a batch of samples.

    Args:
        batch_image_details: List of image details dictionaries
        rpc: RPC client for making API calls

    Returns:
        List of updated sample details
    """
    logging.debug(f"Processing batch of {len(batch_image_details)} samples for download")
    return [
        download_samples(image_details, rpc, bucket_alias, account_number) for image_details in batch_image_details
    ]

def calculate_video_properties(video_details: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate properties of a video.

    Args:
        video_details: Dictionary containing video metadata

    Returns:
        Updated video details with calculated properties
    """
    if video_details.get("is_complete"):
        return video_details

    dataset_item = video_details.get("sample_details")
    
    try:
        cap = cv2.VideoCapture(dataset_item["local_file_path"])
        
        if not cap.isOpened():
            raise ValueError(f"Failed to open video file: {dataset_item['local_file_path']}")
            
        try:
            # Get video properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = float(cap.get(cv2.CAP_PROP_FPS))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Verify frame count by iterating if necessary
            if total_frames <= 0:
                total_frames = 0
                while cap.isOpened():
                    ret, _ = cap.read()
                    if not ret:
                        break
                    total_frames += 1
            
            # Additional verification of properties
            if width <= 0 or height <= 0 or fps <= 0:
                # Try to read first frame to get dimensions
                ret, frame = cap.read()
                if ret:
                    height, width = frame.shape[:2]
                    # If fps is invalid, use a default value and log warning
                    if fps <= 0:
                        fps = 30.0
                        logging.warning(f"Invalid FPS for {dataset_item.get('filename')}, using default value: 30.0")
            
            dataset_item.update(
                {
                    "video_height": height,
                    "video_width": width,
                    "fps": round(fps, 2),
                    "total_frames": total_frames,
                    "duration_seconds": round(total_frames / fps, 2) if fps > 0 else 0,
                }
            )
            
            is_complete = all(
                dataset_item.get(k, 0) > 0 
                for k in ["video_height", "video_width", "fps", "total_frames"]
            )
            
            if not is_complete:
                logging.warning(
                    f"Some video properties are invalid for {dataset_item.get('filename')}: "
                    f"height={height}, width={width}, fps={fps}, frames={total_frames}"
                )
            
        finally:
            # Always release the video capture
            cap.release()

        # Clean up local file after processing
        os.remove(dataset_item["local_file_path"])
        return {"sample_details": dataset_item, "is_complete": is_complete}

    except Exception as e:
        logging.error(f"Error processing video {dataset_item.get('filename')}: {e}")
        # Ensure video capture is released in case of error
        if 'cap' in locals() and cap is not None:
            cap.release()
        return {"sample_details": dataset_item, "is_complete": False}
    

def calculate_image_properties(image_details: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate properties of an image.

    Args:
        image_details: Dictionary containing image metadata

    Returns:
        Updated image details with calculated properties
    """
    if image_details.get("is_complete"):
        return image_details

    dataset_item = image_details.get("sample_details")

    try:
        with Image.open(dataset_item["local_file_path"]) as image:
            width, height = image.size
            dataset_item.update(
                {
                    "image_height": height,
                    "image_width": width,
                    "image_area": height * width,
                }
            )

            # Clean up local file after processing
            os.remove(dataset_item["local_file_path"])
            return {"sample_details": dataset_item, "is_complete": True}

    except Exception as e:
        logging.error(f"Error processing image {dataset_item.get('filename')}: {e}")
        return {"sample_details": dataset_item, "is_complete": False}


def batch_calculate_sample_properties(
    batch_sample_details: List[Dict[str, Any]], properties_calculation_fn: callable
) -> List[Dict[str, Any]]:
    """Calculate properties for a batch of samples.

    Args:
        batch_image_details: List of image details dictionaries

    Returns:
        List of processed image details
    """
    logging.debug(
        f"Processing batch of {len(batch_sample_details)} samples for property calculation"
    )
    processed_batch = []
    for dataset_item in batch_sample_details:
        dataset_item = properties_calculation_fn(dataset_item)
        if dataset_item.get("is_complete"):
            processed_batch.append(dataset_item["sample_details"])
    return processed_batch


def batch_update_dataset_items(
    batch_image_details: List[Dict[str, Any]],
    rpc: Any,
    dataset_id: str,
    version: str,
    attempts: int = 3,
    isYolo: bool = False,
) -> List[Dict[str, Any]]:
    """Update dataset items in batch.

    Args:
        batch_image_details: List of image details to update
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        version: Version of the dataset
        attempts: Number of retry attempts
        isYolo: Whether the dataset is in YOLO format

    Returns:
        List of updated dataset items
    """
    retry_count = 0
    while retry_count < attempts:
        try:
            logging.debug(
                f"Attempting to update batch of {len(batch_image_details)} items (attempt {retry_count + 1}/{attempts})"
            )

            payload = {
                "datasetId": str(dataset_id),
                "items": [
                    {
                        "datasetItemId": str(dataset_item.get("_id")),
                        "version": str(version),
                        "splitType": str(dataset_item.get("splitType")),
                        "annotations": dataset_item.get("annotations"),
                        "height": int(dataset_item.get("image_height")),
                        "width": int(dataset_item.get("image_width")),
                        "area": int(dataset_item.get("image_area")),
                    }
                    for dataset_item in batch_image_details
                ],
            }

            if isYolo:
                payload = convert_payload_to_coco_format(payload)

            
            resp = rpc.put(
                path="/v2/dataset/update-dataset-items/",
                payload=payload,
            )
            logging.debug(f"Update dataset items payload: {payload}")

            if resp.get("success"):
                logging.debug(
                    f"Successfully updated batch of {len(batch_image_details)} items"
                )
                for item in batch_image_details:
                    item["status"] = "processed"
                return batch_image_details

            logging.error(f"Failed to update batch: {resp.get('data')}")
            retry_count += 1

        except Exception as e:
            logging.error(f"Error updating batch: {e}")
            retry_count += 1

    for item in batch_image_details:
        item["status"] = "errored"
    return batch_image_details

def batch_update_video_dataset_items(
    batch_video_details: List[Dict[str, Any]],
    rpc: Any,
    dataset_id: str,
    version: str,
    attempts: int = 3,
    isYolo: bool = False,
) -> List[Dict[str, Any]]:
    """Update video dataset items in batch.

    Args:
        batch_video_details: List of video details to update
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        version: Version of the dataset
        attempts: Number of retry attempts
        isYolo: Whether the dataset is in YOLO format

    Returns:
        List of updated dataset items
    """
    retry_count = 0
    while retry_count < attempts:
        try:
            logging.debug(
                f"Attempting to update batch of {len(batch_video_details)} video items (attempt {retry_count + 1}/{attempts})"
            )

            payload = {
                "datasetId": str(dataset_id),
                "items": [
                    {
                        "datasetItemId": str(dataset_item.get("_id")),
                        "version": str(version),
                        "splitType": str(dataset_item.get("splitType")),
                        "annotations": dataset_item.get("annotations"),
                        "height": int(dataset_item.get("video_height")),
                        "width": int(dataset_item.get("video_width")),
                        "fps": float(dataset_item.get("fps")),
                        "total_frames": int(dataset_item.get("total_frames")),
                        "duration_seconds": float(dataset_item.get("duration_seconds", 0.0)),
                        "frame_annotations": _group_annotations_by_frame(dataset_item.get("annotations", [])),
                    }
                    for dataset_item in batch_video_details
                ]
            }

            if isYolo:
                payload = convert_payload_to_coco_format(payload)

            resp = rpc.put(
                path="/v2/dataset/update-video-dataset-items/",
                payload=payload,
            )
            logging.debug(f"Update video dataset items payload: {payload}")

            if resp.get("success"):
                logging.debug(
                    f"Successfully updated batch of {len(batch_video_details)} video items"
                )
                for item in batch_video_details:
                    item["status"] = "processed"
                return batch_video_details

            logging.error(f"Failed to update batch: {resp.get('data')}")
            retry_count += 1

        except Exception as e:
            logging.error(f"Error updating batch: {e}")
            retry_count += 1

    for item in batch_video_details:
        item["status"] = "errored"
    return batch_video_details

def _group_annotations_by_frame(annotations: List[Dict[str, Any]]) -> Dict[int, List[Dict[str, Any]]]:
    """Group annotations by frame ID for efficient processing.
    
    Args:
        annotations: List of annotation dictionaries
        
    Returns:
        Dictionary mapping frame IDs to lists of annotations
    """
    frame_annotations = {}
    for annotation in annotations:
        frame_id = annotation.get("frame_id")
        if frame_id is not None:
            if frame_id not in frame_annotations:
                frame_annotations[frame_id] = []
            frame_annotations[frame_id].append(annotation)
    return frame_annotations


def submit_partition_status(
    dataset_items_batches: List[List[Dict[str, Any]]],
    rpc: Any,
    action_record_id: str,
    dataset_id: str,
    version: str,
    annotation_type: str,
) -> None:
    """Submit status updates for processed partitions.

    Args:
        dataset_items_batches: List of processed dataset item batches
        rpc: RPC client for making API calls
        action_record_id: ID of the action record
        dataset_id: ID of the dataset
        version: Version of the dataset
        annotation_type: Type of annotations
    """
    logging.info(
        f"Submitting partition status for dataset {dataset_id} version {version}"
    )
    try:
        partitions_status = {}
        partition_items = {}

        for batch in dataset_items_batches:
            for item in batch:
                partition_num = item.get("partition")
                status = item.get("status")

                if partition_num not in partition_items:
                    partition_items[partition_num] = []
                partition_items[partition_num].append(item)

                if status == "errored":
                    partitions_status[partition_num] = "errored"
                    logging.error(f"Partition {partition_num} errored")
                elif status == "processed" and partition_num not in partitions_status:
                    partitions_status[partition_num] = "processed"
                    logging.info(f"Partition {partition_num} processed successfully")

        logging.info(f"Updating status for {len(partitions_status)} partitions")
        for partition_num, status in partitions_status.items():
            logging.debug(
                f"Updating partition {partition_num} with status {status} and {len(partition_items[partition_num])} items"
            )
            update_partition_status(
                rpc,
                action_record_id,
                dataset_id,
                version,
                partition_num,
                status,
                partition_items[partition_num],
                annotation_type,
            )
            logging.info(f"Successfully marked partition {partition_num} as {status}")
    except Exception as e:
        logging.error(f"Failed to submit partition status: {e}")
        logging.debug(f"Full error traceback: {traceback.format_exc()}")


def get_annotation_files(
    rpc: Any, dataset_id: str, dataset_version: str, is_annotations_compressed: bool = False
) -> List[str]:
    """Download and return paths to annotation files.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        is_annotations_compressed: Whether annotations are in compressed format

    Returns:
        List of local paths to downloaded annotation files
    """
    logging.info(f"Getting annotation files for dataset {dataset_id}")
    response = rpc_get_call(rpc, f"/v2/dataset/list-annotation-files/{dataset_id}/{dataset_version}", {})

    annotation_files = []
    annotation_dir = os.path.join(TMP_FOLDER, "annotations")
    os.makedirs(annotation_dir, exist_ok=True)

    for s3_url in response:
        try:
            file_name = get_filename_from_url(s3_url)
            file_path = os.path.join(annotation_dir, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            download_file(s3_url, file_path)
            if is_annotations_compressed:
                annotation_files.extend(scan_folder(extract_dataset(file_path)))
            else:
                annotation_files.append(file_path)

        except Exception as e:
            logging.error(f"Error downloading annotation file {s3_url}: {e}")
            
    logging.info(f"Found {len(annotation_files)} annotation files: {annotation_files}")
    return annotation_files


def get_mscoco_server_processing_pipeline(
    rpc: Any, dataset_id: str, dataset_version: str, action_record_id: str, bucket_alias: str="", account_number: str=""
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            f"Setting up processing pipeline for dataset {dataset_id} version {dataset_version}"
        )
        annotation_files = get_annotation_files(rpc, dataset_id, dataset_version)
        logging.info("Processing MSCOCO image details")
        images_details, missing_annotations, classwise_splits = (
            get_msococo_images_details(annotation_files)
        )

        unprocessed_partitions = get_unprocessed_partitions(
            rpc, dataset_id, dataset_version
        )
        logging.info(f"Found {len(unprocessed_partitions)} unprocessed partitions")

        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()

        pipeline = Pipeline()

        # Add producer for each partition
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                },
                partition_num=partition,
            )

        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_mscoco_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"images_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={"rpc": rpc, "bucket_alias": bucket_alias, "account_number": account_number},
            num_threads=5,
        )

        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=5,
        )

        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )

        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "detection",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline

    except Exception as e:
        logging.error(f"Error setting up pipeline: {e}")
        traceback.print_exc()
        raise


def get_imagenet_server_processing_pipeline(
    rpc: Any, dataset_id: str, dataset_version: str, action_record_id: str, bucket_alias: str="", account_number: str=""
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            f"Setting up processing pipeline for dataset {dataset_id} version {dataset_version}"
        )

        unprocessed_partitions = get_unprocessed_partitions(
            rpc, dataset_id, dataset_version
        )
        logging.info(f"Found {len(unprocessed_partitions)} unprocessed partitions")

        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()

        pipeline = Pipeline()

        # Add producer for each partition
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": True,
                },
                partition_num=partition,
            )

        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_imagenet_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={"rpc": rpc, "bucket_alias": bucket_alias, "account_number": account_number},
            num_threads=10,
        )

        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )


        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )

        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "classification",
            },
        )

        logging.info("Pipeline configuration complete")
        return pipeline

    except Exception as e:
        logging.error(f"Error setting up pipeline: {e}")
        traceback.print_exc()
        raise


def get_pascalvoc_server_processing_pipeline(
    rpc: Any, dataset_id: str, dataset_version: str, action_record_id: str, bucket_alias: str="", account_number: str=""
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            f"Setting up processing pipeline for dataset {dataset_id} version {dataset_version}"
        )
        annotation_files = get_annotation_files(
            rpc, dataset_id, dataset_version, is_annotations_compressed=True
        )
        logging.info("Processing Pascal image details")
        images_details, missing_annotations, classwise_splits = (
            get_pascalvoc_image_details(annotation_files)
        )

        unprocessed_partitions = get_unprocessed_partitions(
            rpc, dataset_id, dataset_version
        )
        logging.info(f"Found {len(unprocessed_partitions)} unprocessed partitions")

        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()

        pipeline = Pipeline()

        # Add producer for each partition
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                },
                partition_num=partition,
            )

        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_pascalvoc_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"images_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={"rpc": rpc, "bucket_alias": bucket_alias, "account_number": account_number},
            num_threads=10,
        )

        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )


        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )

        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "detection",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline

    except Exception as e:
        logging.error(f"Error setting up Pascal VOC pipeline: {e}")
        traceback.print_exc()
        raise


def get_labelbox_server_processing_pipeline(
    rpc: Any, dataset_id: str, dataset_version: str, action_record_id: str, bucket_alias: str="", account_number: str=""
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            f"Setting up processing pipeline for dataset {dataset_id} version {dataset_version}"
        )
        annotation_files = get_annotation_files(rpc, dataset_id, dataset_version)
        logging.info("Processing Labelbox image details")
        images_details, missing_annotations, classwise_splits = (
            get_labelbox_image_details(annotation_files)
        )

        unprocessed_partitions = get_unprocessed_partitions(
            rpc, dataset_id, dataset_version
        )
        logging.info(f"Found {len(unprocessed_partitions)} unprocessed partitions")

        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()

        pipeline = Pipeline()

        # Add producer for each partition
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                },
                partition_num=partition,
            )

        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_labelbox_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"images_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Add Dataset Item Local File Path",
            process_fn=add_labelbox_dataset_item_local_file_path,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={"base_dataset_path": dataset_id},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )


        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "detection",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error(f"Error setting up pipeline: {e}")
        traceback.print_exc()
        raise

def get_labelbox_classification_server_processing_pipeline(
    rpc: Any, dataset_id: str, dataset_version: str, action_record_id: str, bucket_alias: str="", account_number: str=""
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            f"Setting up processing pipeline for dataset {dataset_id} version {dataset_version}"
        )
        annotation_files = get_annotation_files(rpc, dataset_id, dataset_version)
        logging.info("Processing Labelbox image details")
        images_details, missing_annotations, classwise_splits = (
            get_labelbox_classification_image_details(annotation_files)
        )

        unprocessed_partitions = get_unprocessed_partitions(
            rpc, dataset_id, dataset_version
        )
        logging.info(f"Found {len(unprocessed_partitions)} unprocessed partitions")

        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()

        pipeline = Pipeline()

        # Add producer for each partition
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                },
                partition_num=partition,
            )

        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_labelbox_classification_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"images_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Add Dataset Item Local File Path",
            process_fn=add_labelbox_classification_dataset_item_local_file_path,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={"base_dataset_path": dataset_id},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )


        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "classification",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error(f"Error setting up pipeline: {e}")
        traceback.print_exc()
        raise


def get_yolo_server_processing_pipeline(
    rpc: Any, dataset_id: str, dataset_version: str, action_record_id: str, bucket_alias: str="", account_number: str=""
):
    """Create and configure the processing pipeline.
    Args:

        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            f"Setting up processing pipeline for dataset {dataset_id} version {dataset_version}"
        )
        annotation_files = get_annotation_files(
            rpc, dataset_id, dataset_version, is_annotations_compressed=True
        )
        logging.info("Processing Pascal image details")
        images_details, missing_annotations, classwise_splits = get_yolo_image_details(
            annotation_files
        )

        unprocessed_partitions = get_unprocessed_partitions(
            rpc, dataset_id, dataset_version
        )
        logging.info(f"Found {len(unprocessed_partitions)} unprocessed partitions")

        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()

        pipeline = Pipeline()

        # Add producer for each partition
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                },
                partition_num=partition,
            )

        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_yolo_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"images_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={"rpc": rpc, "bucket_alias": bucket_alias, "account_number": account_number},
            num_threads=10,
        )

        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )

        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "isYolo": True,
            },
            num_threads=10,
            is_last_stage=True,
        )

        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "detection",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline

    except Exception as e:
        logging.error(f"Error setting up Pascal VOC pipeline: {e}")
        traceback.print_exc()
        raise

def get_unlabelled_server_processing_pipeline(
    rpc: Any, dataset_id: str, dataset_version: str, action_record_id: str, bucket_alias: str="", account_number: str=""
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            f"Setting up processing pipeline for dataset {dataset_id} version {dataset_version}"
        )

        unprocessed_partitions = get_unprocessed_partitions(
            rpc, dataset_id, dataset_version
        )
        logging.info(f"Found {len(unprocessed_partitions)} unprocessed partitions")

        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()

        pipeline = Pipeline()

        # Add producer for each partition
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": True,
                },
                partition_num=partition,
            )

        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_unlabelled_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={"rpc": rpc, "bucket_alias": bucket_alias, "account_number": account_number},
            num_threads=10,
        )

        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )

        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )

        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "classification",
            },
        )

        logging.info("Pipeline configuration complete")
        return pipeline

    except Exception as e:
        logging.error(f"Error setting up pipeline: {e}")
        traceback.print_exc()
        raise

def get_mscoco_video_server_processing_pipeline(
    rpc: Any, dataset_id: str, dataset_version: str, action_record_id: str, bucket_alias: str="", account_number: str=""
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            f"Setting up processing pipeline for dataset {dataset_id} version {dataset_version}"
        )
        annotation_files = get_annotation_files(rpc, dataset_id, dataset_version)
        logging.info("Processing MSCOCO image details")
        videos_details, missing_annotations, classwise_splits = (
            get_msococo_videos_details(annotation_files)
        )

        unprocessed_partitions = get_unprocessed_partitions(
            rpc, dataset_id, dataset_version
        )
        logging.info(f"Found {len(unprocessed_partitions)} unprocessed partitions")

        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()

        pipeline = Pipeline()

        # Add producer for each partition
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                },
                partition_num=partition,
            )

        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_mscoco_video_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"images_details": videos_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Videos",
            process_fn=batch_download_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={"rpc": rpc, "bucket_alias": bucket_alias, "account_number": account_number},
            num_threads=5,
        )

        pipeline.add_stage(
            stage_name="Calculate Video Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_video_properties},
            num_threads=5,
        )

        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_video_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )

        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "detection",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline

    except Exception as e:
        logging.error(f"Error setting up pipeline: {e}")
        traceback.print_exc()
        raise