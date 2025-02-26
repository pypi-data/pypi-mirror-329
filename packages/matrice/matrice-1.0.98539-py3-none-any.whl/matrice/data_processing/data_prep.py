import logging
from queue import Queue
import os
import yaml
import json
import datetime
from typing import Any

from matrice.data_processing.server_utils import (
    download_file,
    get_dataset_items,
    chunk_items,
)
from matrice.data_processing.pipeline import Pipeline


def dataset_items_producer(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    pipeline_queue: Queue,
    request_batch_size: int = 100,
    processing_batch_size: int = 10,
) -> None:
    """Get items for a partition and add them to the pipeline queue.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Dataset version
        pipeline_queue: Queue to add items to
        request_batch_size: Number of items to fetch per API request
        processing_batch_size: Size of batches to add to pipeline queue
    """
    try:
        # Get items for the partition
        all_dataset_items = get_dataset_items(
            rpc,
            dataset_id,
            dataset_version,
            request_batch_size,
        )

        # Chunk items into processing batches
        processing_batches = chunk_items(all_dataset_items, processing_batch_size)

        # Add batches to the pipeline queue
        for batch in processing_batches:
            pipeline_queue.put(batch)

        logging.info(
            f"Successfully processed {len(all_dataset_items)} items for dataset version {dataset_version}"
        )

    except Exception as e:
        logging.error(f"Error processing dataset version {dataset_version}: {e}")
        raise


def process_final_annotations(
    dataset_items, base_dataset_path: str, input_format: str, dataset_version: str
) -> None:
    """Process final annotations after pipeline completion.

    Args:
        dataset_items: List of dataset items to process
        base_dataset_path: Base path to save dataset files
        input_format: Format of annotations (YOLO/COCO)
        dataset_version: Dataset version
    """
    if not dataset_items:
        logging.warning("No items to process for annotations")
        return

    dataset_items = [item for batch in dataset_items for item in batch]
    logging.info("Processing final annotations for %d items", len(dataset_items))
    logging.debug(f"Base dataset path: {base_dataset_path}")
    logging.debug(f"Input format: {input_format}")

    input_format = input_format.lower()
    if input_format == "yolo":
        logging.info("Writing YOLO format labels")
        write_yolo_labels(base_dataset_path, dataset_items, dataset_version)
    elif input_format in ["mscoco", "coco"]:
        logging.info("Writing MSCOCO format annotations")
        write_mscoco_annotation_files(base_dataset_path, dataset_items, dataset_version)
    logging.info("DATA PREP SUCCESS")


def get_item_set_type(dataset_item: dict, dataset_version: str = "v1.0") -> str:
    """Get the set type (train/test/val) for a dataset item."""
    for info in dataset_item["versionInfo"]:
        if info["version"] == dataset_version:
            return info.get("itemSetType", "")
    return ""


def get_image_annotations(dataset_item: dict, dataset_version: str = "v1.0") -> list:
    """Get annotations for a dataset item."""
    for info in dataset_item["versionInfo"]:
        if info["version"] == dataset_version:
            return info.get("annotation", [])
    return []


def get_category_name(dataset_item: dict, dataset_version: str = "v1.0") -> str:
    """Get category name from dataset item annotations."""
    annotations = get_image_annotations(dataset_item, dataset_version)
    if annotations:
        return annotations[0]["category"]
    return None


def get_image_path(
    base_dataset_path: str, dataset_item: dict, input_format: str, dataset_version: str
) -> str:
    """Get save path for an image.

    Args:
        base_dataset_path: Base path to save dataset
        dataset_item: Dataset item containing image info
        input_format: Format of dataset
        dataset_version: Dataset version

    Returns:
        Full path where image should be saved
    """
    item_set_type = get_item_set_type(dataset_item, dataset_version)
    image_name = dataset_item["filename"].split("/")[-1]

    if item_set_type not in ["train", "test", "val"]:
        return None

    if "imagenet" in input_format.lower():
        category = get_category_name(dataset_item, dataset_version)
        if not category:
            return None
        save_path = os.path.dirname(
            f"{base_dataset_path}/images/{item_set_type}/{category}/{image_name}"
        )
    else:
        save_path = os.path.dirname(
            f"{base_dataset_path}/images/{item_set_type}/{image_name}"
        )

    os.makedirs(save_path, exist_ok=True)
    return os.path.join(save_path, image_name)


def download_images(
    dataset_items: list, input_format: str, base_dataset_path: str, dataset_version: str
) -> list:
    """Download images for dataset items.

    Args:
        dataset_items: List of dataset items
        input_format: Format of dataset
        base_dataset_path: Base path to save images
        dataset_version: Dataset version

    Returns:
        List of successfully downloaded items
    """
    downloaded_images = []
    for dataset_item in dataset_items:
        try:
            save_path = get_image_path(
                base_dataset_path, dataset_item, input_format, dataset_version
            )
            if save_path and dataset_item.get("fileLocation"):
                download_file(dataset_item["fileLocation"], save_path)
                downloaded_images.append(dataset_item)
            else:
                logging.warning(
                    f"Skipping download for {dataset_item['filename']} - Invalid path or missing URL"
                )
        except Exception as e:
            logging.error(
                "Error downloading image %s: %s", dataset_item["filename"], str(e)
            )
    return downloaded_images


def convert_bbox_coco2yolo(img_width: int, img_height: int, bbox: list) -> list:
    """Convert COCO format bounding box to YOLO format.

    Args:
        img_width: Width of image
        img_height: Height of image
        bbox: Bounding box in COCO format [x,y,w,h]

    Returns:
        Bounding box in YOLO format [x_center,y_center,w,h]
    """
    if not all(isinstance(x, (int, float)) for x in bbox):
        raise ValueError("Invalid bbox format - all values must be numeric")

    x_tl, y_tl, w, h = bbox

    if img_width <= 0 or img_height <= 0:
        raise ValueError("Invalid image dimensions")

    dw = 1.0 / img_width
    dh = 1.0 / img_height

    x_center = x_tl + w / 2.0
    y_center = y_tl + h / 2.0

    x = x_center * dw
    y = y_center * dh
    w = w * dw
    h = h * dh

    return [x, y, w, h]


def write_data_yaml(categories_id_map: dict, yaml_file_path: str) -> None:
    """Write category data to YAML file.

    Args:
        categories_id_map: Dictionary mapping categories to IDs
        yaml_file_path: Path to save YAML file
    """
    if not categories_id_map:
        raise ValueError("Categories dictionary is empty")

    data = {
        "train": "images/train",
        "test": "images/test",
        "val": "images/val",
        "nc": len(categories_id_map),
        "names": {v: k for k, v in categories_id_map.items()},
    }

    os.makedirs(os.path.dirname(yaml_file_path), exist_ok=True)
    with open(yaml_file_path, "w", encoding="utf-8") as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)


def write_yolo_labels(
    local_path: str, dataset_items: list, dataset_version: str
) -> None:
    """Write YOLO format labels for images.

    Args:
        local_path: Base path to save labels
        dataset_items: List of dataset items
        dataset_version: Dataset version
    """
    os.makedirs(f"{local_path}/labels", exist_ok=True)

    categories_id_map = get_categories_id_map(dataset_items, start_id=0)

    for image in dataset_items:
        img_name = image["filename"].split("/")[-1]
        item_set_type = get_item_set_type(image, dataset_version)
        
        if not item_set_type:
            logging.warning(f"Skipping {img_name} - no valid set type")
            continue

        os.makedirs(
            f"{local_path}/labels/{item_set_type}",
            exist_ok=True,
        )
        anno_txt = f'{local_path}/labels/{item_set_type}/{img_name.split(".")[0] + ".txt"}'

        with open(anno_txt, "w", encoding="utf-8") as f:
            for anno in get_image_annotations(image, dataset_version):
                try:
                    x, y, w, h = convert_bbox_coco2yolo(
                        image["width"], image["height"], anno["bbox"]
                    )

                    category = anno["category"]
                    category_id = categories_id_map.get(category)
                    if category_id is None:
                        logging.warning(f"Unknown category {category} in {img_name}")
                        continue

                    f.write(f"{category_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")

                    if "segmentation" in anno and anno.get("segmentation"):
                        segmentation_points_list = []
                        for segmentation in anno.get("segmentation", []):
                            if any(isinstance(point, str) for point in segmentation):
                                continue
                            segmentation_points = [
                                str(float(point) / image["width"]) for point in segmentation
                            ]
                            segmentation_points_list.append(" ".join(segmentation_points))
                        segmentation_points_string = " ".join(segmentation_points_list)
                        f.write(f"{category_id} {segmentation_points_string}\n")
                except Exception as e:
                    logging.error(f"Error processing annotation in {img_name}: {str(e)}")

    write_data_yaml(categories_id_map, f"{local_path}/data.yaml")


def get_categories_id_map(dataset_items: list, start_id: int = 0) -> dict:
    """Get mapping of categories to IDs.

    Args:
        dataset_items: List of dataset items
        start_id: Starting ID for categories

    Returns:
        Dictionary mapping category names to IDs
    """
    categories_id_map = {}
    category_num = start_id
    for image in dataset_items:
        for anno in get_image_annotations(image):
            category = anno.get("category")
            if not category:
                continue
            if category not in categories_id_map:
                categories_id_map[category] = category_num
                category_num += 1
    logging.info(f"Categories ID map: {categories_id_map}")
    return categories_id_map


def get_mscoco_categories(categories_id_map: dict) -> list:
    """Extract MSCOCO categories from dataset items.

    Args:
        dataset_items: List of dataset items

    Returns:
        List of category dictionaries in MSCOCO format
    """
    categories = []
    for category_name, category_id in categories_id_map.items():
        categories.append(
            {
                "id": category_id,
                "name": category_name,
                "supercategory": "",
            }
        )
    return categories


def get_mscoco_images(dataset_items: list) -> list:
    """Extract MSCOCO images from dataset items.

    Args:
        dataset_items: List of dataset items

    Returns:
        List of image dictionaries in MSCOCO format
    """
    images = []
    image_id_counter = 1
    logging.info("Getting Image file")

    for image in dataset_items:
        if not all(key in image for key in ["width", "height", "filename"]):
            logging.warning(f"Skipping image with missing required fields: {image}")
            continue
            
        image_info = {
            "id": image_id_counter,
            "width": image["width"],
            "height": image["height"],
            "file_name": image["filename"].split("/")[-1],
            "date_captured": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        image_id_counter += 1
        images.append(image_info)

    logging.info("Returning Image file")
    return images


def get_mscoco_annotations(dataset_items: list, categories_id_map: dict) -> list:
    """Extract MSCOCO annotations from dataset items.

    Args:
        dataset_items: List of dataset items
        categories_id_map: Dictionary mapping categories to IDs

    Returns:
        List of annotation dictionaries in MSCOCO format
    """
    annotations = []
    annotation_id_counter = 1
    image_id_counter = 1

    logging.info("Getting Annotation file")

    for image in dataset_items:
        for bbox_info in get_image_annotations(image):
            try:
                category = bbox_info.get("category")
                if not category:
                    continue
                    
                category_id = categories_id_map.get(category)
                if category_id is None:
                    continue

                bbox = bbox_info.get("bbox")
                if not bbox or len(bbox) != 4:
                    continue

                annotation_info = {
                    "id": annotation_id_counter,
                    "image_id": image_id_counter,
                    "category_id": category_id,
                    "segmentation": bbox_info.get("segmentation", []),
                    "area": bbox[2] * bbox[3],
                    "bbox": bbox,
                    "iscrowd": 0,
                }
                annotation_id_counter += 1
                annotations.append(annotation_info)
            except Exception as e:
                logging.error(f"Error processing annotation: {str(e)}")
                
        image_id_counter += 1

    logging.info("Returning Annotation file")
    return annotations


def write_mscoco_annotation_file(
    dataset_items: list, categories_id_map: dict, ann_json_path: str
) -> None:
    """Write MSCOCO annotation file in COCO format.

    Args:
        dataset_items: List of dataset items
        categories_id_map: Dictionary mapping categories to IDs
        ann_json_path: Path to save annotation file
    """
    logging.info("Writing Annotation file")
    coco_format_data = {
        "info": {},
        "licenses": [],
        "images": get_mscoco_images(dataset_items),
        "annotations": get_mscoco_annotations(dataset_items, categories_id_map),
        "categories": get_mscoco_categories(categories_id_map),
    }
    logging.info("Writing Annotation file complete")
    os.makedirs(os.path.dirname(ann_json_path), exist_ok=True)
    with open(ann_json_path, "w", encoding="utf-8") as f:
        json.dump(coco_format_data, f, indent=2)


def write_mscoco_annotation_files(
    local_path: str, dataset_items: list, dataset_version: str
) -> None:
    """Write MSCOCO annotation files for different itemSetTypes.

    Args:
        local_path: Base path to save annotation files
        dataset_items: List of dataset items
        dataset_version: Dataset version
    """
    labels_path = f"{local_path}/annotations"
    os.makedirs(labels_path, exist_ok=True)

    train_dataset_items = [
        x for x in dataset_items if get_item_set_type(x, dataset_version) == "train"
    ]
    test_dataset_items = [
        x for x in dataset_items if get_item_set_type(x, dataset_version) == "test"
    ]
    val_dataset_items = [
        x for x in dataset_items if get_item_set_type(x, dataset_version) == "val"
    ]

    categories_id_map = get_categories_id_map(dataset_items, start_id=1)

    if train_dataset_items:
        logging.info("Creating mscoco train.json")
        write_mscoco_annotation_file(
            train_dataset_items,
            categories_id_map,
            f"{local_path}/annotations/train.json",
        )
        logging.info("Created mscoco train.json")

    if test_dataset_items:
        logging.info("Creating mscoco test.json")
        write_mscoco_annotation_file(
            test_dataset_items, categories_id_map, f"{local_path}/annotations/test.json"
        )
        logging.info("Created mscoco test.json")

    if val_dataset_items:
        logging.info("Creating mscoco val.json")
        write_mscoco_annotation_file(
            val_dataset_items, categories_id_map, f"{local_path}/annotations/val.json"
        )
        logging.info("Created mscoco val.json")


def get_data_prep_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    input_format: str,
    base_dataset_path: str,
) -> Pipeline:
    """Get the data prep pipeline.

    Args:
        rpc: RPC client
        dataset_id: Dataset ID
        dataset_version: Dataset version
        input_format: Format of annotations
        base_dataset_path: Base path to save dataset

    Returns:
        Configured Pipeline object
    """
    dataset_items_queue = Queue()

    pipeline = Pipeline()

    pipeline.add_producer(
        process_fn=dataset_items_producer,
        process_params={
            "rpc": rpc,
            "dataset_id": dataset_id,
            "dataset_version": dataset_version,
            "pipeline_queue": dataset_items_queue,
        },
    )

    pipeline.add_stage(
        stage_name="Download Images",
        process_fn=download_images,
        pull_queue=dataset_items_queue,
        process_params={
            "input_format": input_format,
            "base_dataset_path": base_dataset_path,
            "dataset_version": dataset_version,
        },
        num_threads=15,
        is_last_stage=True,
    )
    pipeline.add_stop_callback(
        callback=process_final_annotations,
        process_params={
            "base_dataset_path": base_dataset_path,
            "input_format": input_format,
            "dataset_version": dataset_version,
        },
    )
    return pipeline


class DataPrep:
    """Class to handle dataset preparation."""

    def __init__(self, session: Any, action_record_id: str):
        """Initialize DataPrep.

        Args:
            session: Session object with RPC client
            action_record_id: ID of action record
        """
        self.session = session
        self.rpc = session.rpc
        self.action_record_id = action_record_id
        url = f"/v1/project/action/{self.action_record_id}/details"
        self.action_doc = self.rpc.get(url)["data"]
        self.action_type = self.action_doc["action"]
        self.job_params = self.action_doc["jobParams"]
        self.dataset_id = self.job_params["dataset_id"]
        self.dataset_version = self.job_params["dataset_version"]
        self.input_format = self.job_params["input_formats"][0]
        self.local_path = f"{str(self.dataset_id)}-{str(self.dataset_version)}-{str(self.input_format).lower()}"

        self.update_status(
            "DCKR_ACK",
            "ACK",
            "Action is acknowledged by data processing service",
            str(os.path.join("/usr/src/workspace", self.local_path)),
        )

    def update_status(
        self, stepCode: str, status: str, status_description: str, dataset_path: str = None
    ) -> None:
        """Update status of data preparation.

        Args:
            stepCode: Code indicating current step
            status: Status of step
            status_description: Description of status
            dataset_path: Optional path to dataset
        """
        try:
            logging.info(status_description)
            url = "/v1/project/action"
            payload = {
                "_id": self.action_record_id,
                "action": self.action_type,
                "serviceName": self.action_doc["serviceName"],
                "stepCode": stepCode,
                "status": status,
                "statusDescription": status_description,
            }
            if dataset_path:
                self.job_params["dataset_path"] = dataset_path
                payload["jobParams"] = self.job_params
            self.rpc.put(path=url, payload=payload)

        except Exception as e:
            logging.error("Exception in update_status: %s", str(e))
            raise

    def start_processing(self) -> None:
        """Start dataset preparation processing."""
        try:
            self.update_status(
                "DCKR_PROC",
                "OK",
                "Dataset started preparation",
            )
            self.pipeline = get_data_prep_pipeline(
                self.rpc,
                self.dataset_id,
                self.dataset_version,
                self.input_format,
                self.local_path,
            )
            self.pipeline.start()
            self.pipeline.wait_to_finish_processing_and_stop()
            self.update_status(
                "SUCCESS",
                "SUCCESS",
                "Dataset Preparation completed",
            )
        except Exception as e:
            logging.error(f"Error in start_processing: {str(e)}")
            self.update_status(
                "FAILED",
                "FAILED", 
                f"Dataset preparation failed: {str(e)}",
            )
            raise
