import os
from queue import Queue
import logging

from matrice.data_processing.pipeline import Pipeline
from matrice.data_processing.client_utils import (
    ANNOTATION_PARTITION_TYPE,
    SAMPLES_PARTITION_TYPE,
    scan_dataset,
    get_annotations_partition,
    get_images_partitions,
    get_cloud_file_path,
    update_annotation_bucket_url,
    get_batch_pre_signed_upload_urls,
    upload_file,
    compress_annotation_files,
    update_partitions_numbers,
    create_partition_stats,
)

def get_partition_status(
    base_path, skip_annotation_partition=False
):
    logging.info("Getting partition status")
    annotation_partition, images_partitions = None, []
    annotation_files, image_files = scan_dataset(base_path)
    if not skip_annotation_partition:
        annotation_partition = get_annotations_partition(annotation_files)
    images_partitions = get_images_partitions(image_files)
    return annotation_partition, images_partitions


def get_partition_batches(partition, batch_size, dataset_id, dataset_version, base_dataset_path, include_version_in_cloud_path=False):
    files = partition["files"]

    def create_file_info(file_path):
        file_name = os.path.basename(file_path)
        return {
            "partition_num": partition["partitionNum"],
            "partition_type": partition["type"],
            "local_file_path": file_path,
            "file_name": file_name,
            "cloud_file_path": get_cloud_file_path(
                dataset_id, dataset_version, base_dataset_path, file_path, include_version_in_cloud_path
            ),

        }

    # Process all files in a single batch if total files <= batch_size
    if len(files) <= batch_size:
        return [[create_file_info(f) for f in files]]

    # Split into multiple batches
    batches = []
    num_batches = (len(files) + batch_size - 1) // batch_size
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min(start_idx + batch_size, len(files))
        batch_files = files[start_idx:end_idx]
        batches.append([create_file_info(f) for f in batch_files])

    logging.info(
        f"Created {len(batches)} batches for partition {partition['partitionNum']}"
    )
    return batches


def add_batch_presigned_upload_urls(
    batch, rpc, partition_type, bucket_alias="", account_number=""
):
    logging.debug(f"batch to add presigned urls: {batch}")
    cloud_paths_presigned_url_dict = get_batch_pre_signed_upload_urls(
        [file_info["cloud_file_path"] for file_info in batch],
        rpc,
        partition_type,
        bucket_alias,
        account_number,
    )
    for file_info in batch:
        file_info["presigned_url"] = cloud_paths_presigned_url_dict.get(
            file_info["cloud_file_path"], None
        )
    return batch


def upload_batch_files(batch, max_attempts=5):
    for file_info in batch:
        success = upload_file(
            file_info["local_file_path"], file_info["presigned_url"], max_attempts
        )
        file_info["upload_success"] = success
    return batch


def batch_create_dataset_items(batch, dataset_id, dataset_version, rpc):
    logging.debug(f"batch to create dataset items: {batch}")
    payload = {
        "datasetId": dataset_id,
        "partitionNumber": batch[0]["partition_num"],
        "version": dataset_version,
        "files": [
            {
                "fileName": item["file_name"],
                "fileLocation": item["cloud_file_path"],
            }
            for item in batch
        ],
    }
    resp = rpc.post("/v2/dataset/add_dataset_items", payload=payload)
    logging.info(f"Response from create dataset items: {resp}")
    return batch


def get_client_annotations_processing_pipeline(
    annotations_partition,
    dataset_id,
    dataset_version,
    base_dataset_path,
    rpc,
    compress_annotations=False,
    max_attempts=5,
    batch_size=16,
    bucket_alias="",

    account_number="",
):
    logging.info("Setting up annotations pipeline")

    stage_1_queue = Queue()
    stage_2_queue = Queue()

    annotations_client_pipeline = Pipeline()

    if compress_annotations:
        annotations_partition["files"] = [
            compress_annotation_files(annotations_partition["files"], base_dataset_path)
        ]

    batches = get_partition_batches(
        annotations_partition, batch_size, dataset_id, dataset_version, base_dataset_path, include_version_in_cloud_path=True
    )
    for batch in batches:
        stage_1_queue.put(batch)

    update_annotation_bucket_url(
        rpc,
        dataset_id,
        batches[0][0]["partition_num"],
        "/".join(batches[0][0]["cloud_file_path"].split("/")[:-1]),
    )

    annotations_client_pipeline.add_stage(
        stage_name="fetching_presigned_urls",
        process_fn=add_batch_presigned_upload_urls,
        pull_queue=stage_1_queue,
        push_queue=stage_2_queue,
        process_params={
            "rpc": rpc,
            "partition_type": ANNOTATION_PARTITION_TYPE,
            "bucket_alias": bucket_alias,
            "account_number": account_number,
        },
        num_threads=10,
    )

    annotations_client_pipeline.add_stage(
        stage_name="uploading_files",
        pull_queue=stage_2_queue,
        process_fn=upload_batch_files,
        process_params={"max_attempts": max_attempts},
        num_threads=10,
    )

    return annotations_client_pipeline


def get_client_images_processing_pipeline(
    images_partitions,
    dataset_id,
    dataset_version,
    base_dataset_path,
    rpc,
    max_attempts=5,
    batch_size=16,
    bucket_alias="",
    account_number="",
):
    logging.info("Setting up images pipeline")
    logging.debug(
        f"images_partitions: {images_partitions}, dataset_id: {dataset_id}, dataset_version: {dataset_version}, base_dataset_path: {base_dataset_path}"
    )

    stage_1_queue = Queue()
    stage_2_queue = Queue()
    stage_3_queue = Queue()

    for partition in images_partitions:
        for batch in get_partition_batches(
            partition, batch_size, dataset_id, dataset_version, base_dataset_path
        ):
            stage_1_queue.put(batch)

    images_client_pipeline = Pipeline()
    images_client_pipeline.add_stage(
        stage_name="fetching_presigned_urls",
        pull_queue=stage_1_queue,
        push_queue=stage_2_queue,
        process_fn=add_batch_presigned_upload_urls,
        process_params={
            "rpc": rpc,
            "partition_type": SAMPLES_PARTITION_TYPE,
            "bucket_alias": bucket_alias,
            "account_number": account_number,
        },
        num_threads=10,
    )
    images_client_pipeline.add_stage(
        stage_name="uploading_files",
        pull_queue=stage_2_queue,
        push_queue=stage_3_queue,
        process_fn=upload_batch_files,
        process_params={"max_attempts": max_attempts},
        num_threads=10,
    )
    images_client_pipeline.add_stage(
        stage_name="inserting_dataset_items",
        pull_queue=stage_3_queue,
        process_fn=batch_create_dataset_items,
        process_params={
            "dataset_id": dataset_id,
            "dataset_version": dataset_version,
            "rpc": rpc,
        },
        num_threads=10,
    )
    return images_client_pipeline

def get_client_processing_pipelines(
        rpc,
        dataset_id,
        dataset_version,
        images_partition_status: list,
        annotation_partition_status: list,
        dataset_path: str,
        is_annotations_compressed: bool,
        destination_bucket_alias: str,
        account_number: str,

    ):
    annotation_pipeline, images_pipeline = None, None
    if annotation_partition_status:
        annotation_pipeline = get_client_annotations_processing_pipeline(
            annotations_partition=annotation_partition_status,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            base_dataset_path=dataset_path,
            rpc=rpc,
            compress_annotations=is_annotations_compressed,
            bucket_alias=destination_bucket_alias,
            account_number=account_number,
        )

    if images_partition_status:
        images_pipeline = get_client_images_processing_pipeline(
            images_partitions=images_partition_status,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            base_dataset_path=dataset_path,
            rpc=rpc,
            bucket_alias=destination_bucket_alias,
            account_number=account_number,
        )
    return annotation_pipeline, images_pipeline

def handle_partition_stats(rpc, dataset_id, source_dataset_version, target_dataset_version, dataset_path, skip_annotation_pipeline):
    partition_stats = []
    annotation_partition_status, images_partition_status = get_partition_status(
        base_path=dataset_path,
        skip_annotation_partition=skip_annotation_pipeline,
    )
    if annotation_partition_status:
        partition_stats.append(annotation_partition_status)
    if images_partition_status:
        partition_stats.extend(images_partition_status)
    partition_stats = update_partitions_numbers(rpc, dataset_id, partition_stats)
    create_partition_stats(
        rpc,
        partition_stats,
        dataset_id,
        target_dataset_version,
        source_dataset_version,
    )
    return annotation_partition_status, images_partition_status

def start_client_processing_pipelines(
    rpc,
    dataset_id,
    dataset_version,
    images_partition_status,
    annotation_partition_status,
    dataset_path,
    is_annotations_compressed,
    destination_bucket_alias,
    account_number,
):
    annotation_pipeline, images_pipeline = get_client_processing_pipelines(
        rpc=rpc,
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        images_partition_status=images_partition_status,
        annotation_partition_status=annotation_partition_status,
        dataset_path=dataset_path,
        is_annotations_compressed=is_annotations_compressed,
        destination_bucket_alias=destination_bucket_alias,
        account_number=account_number,
    )
    if annotation_pipeline:
        logging.info("Starting annotation pipeline")
        annotation_pipeline.start()
        logging.info("Waiting for annotation pipeline to complete")
        annotation_pipeline.wait_to_finish_processing_and_stop()
    if images_pipeline:
        logging.info("Starting images pipeline")
        images_pipeline.start()
        logging.info("Waiting for images pipeline to complete")
        images_pipeline.wait_to_finish_processing_and_stop()


def handle_client_processing_pipelines(
    rpc,
    dataset_id,
    source_dataset_version,
    target_dataset_version,
    input_type,
    source_URL="",
    dataset_path="",
    destination_bucket_alias="",
    account_number="",
):

    is_annotations_compressed = input_type in ["pascalvoc", "pascal_voc", "yolo"]

    skip_annotation_pipeline = (
        input_type in ["imagenet", "unlabeled"]
        or (input_type == "labelbox" and not source_URL)
        or (input_type == "labelbox_classification" and not source_URL)
    )

    annotation_partition_status, images_partition_status = handle_partition_stats(
        rpc=rpc,
        dataset_id=dataset_id,
        source_dataset_version=source_dataset_version,
        target_dataset_version=target_dataset_version,
        dataset_path=dataset_path,
        skip_annotation_pipeline=skip_annotation_pipeline
    )
    start_client_processing_pipelines(
        rpc=rpc,
        dataset_id=dataset_id,
        dataset_version=target_dataset_version,
        images_partition_status=images_partition_status,
        annotation_partition_status=annotation_partition_status,
        dataset_path=dataset_path,
        is_annotations_compressed=is_annotations_compressed,
        destination_bucket_alias=destination_bucket_alias,
        account_number=account_number,
    )
