import os
import json
import traceback
import logging
from matrice.data_processing.server_utils import (
get_corresponding_split_type,
generate_short_uuid
)

def calculate_bbox_properties(bbox):
    if len(bbox) != 4:
        raise ValueError("Bounding box must be in the format [x_min, y_min, width, height].")
    
    x_min, y_min, width, height = bbox
    
    center_x = x_min + width / 2
    center_y = y_min + height / 2
    
    area = width * height
    
    return {
        "height": float(height),
        "width": float(width),
        "center": [float(center_x), float(center_y)],
        "area": float(area)
    }

def get_msococo_images_details(annotation_files):
    """Process MSCOCO annotation files and extract image details.

    Args:
        annotation_files: List of paths to MSCOCO annotation JSON files

    Returns:
        Tuple containing:
        - Dictionary of image details indexed by file location
        - List of image IDs missing annotations
    """
    complete_images = {}
    missing_annotations = []
    missing_dimensions = {}
    classwise_splits={}

    logging.info(f"Processing {len(annotation_files)} annotation files")

    if not annotation_files:
        logging.error("No annotation files provided")
        return complete_images, missing_annotations

    for file_index, file_path in enumerate(annotation_files, 1):
        logging.debug(f"\nProcessing file {file_index}/{len(annotation_files)}: {file_path}")

        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            continue

        try:
            with open(file_path) as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    logging.error(f"Invalid JSON in {file_path}: {e}")
                    continue

                images = data.get("images", [])
                categories = data.get("categories", [])
                annotations = data.get("annotations", [])


            if not images or not annotations:
                logging.error(f"Missing images or annotations in {file_path}")
                continue

            # Build lookup maps
            image_info = {
                img["id"]: img
                for img in images
                if isinstance(img, dict) and "id" in img
            }
            category_map = {
                cat["id"]: cat["name"]
                for cat in categories
                if isinstance(cat, dict) and "id" in cat
            }
            category_name_to_id = {v: k for k, v in category_map.items()}
            for k, v in category_name_to_id.items():
                if k not in classwise_splits:
                    classwise_splits[str(k)] = {"train": 0, "test": 0, "val": 0, "unassigned": 0}

            processed = 0
            skipped = 0

            for annotation in annotations:
                if not isinstance(annotation, dict) or "image_id" not in annotation:
                    skipped += 1
                    continue

                image_id = annotation["image_id"]
                image = image_info.get(image_id)
                if not image:
                    skipped += 1
                    continue

                bbox = [float(coord) for coord in annotation.get("bbox", [])]
                if not bbox or len(bbox) != 4:
                    skipped += 1
                    continue

                try:
                    bbox_properties = calculate_bbox_properties(bbox)

                    annotation_json = {
                        "id": str(generate_short_uuid()),
                        "segmentation": [
                            [float(coord) for coord in segment]
                            for segment in annotation.get("segmentation", [])  if isinstance(segment, list)
                        ],
                        "isCrowd": [
                            float(item) if isinstance(item, (int, float)) else 0
                            for item in (
                                annotation.get("iscrowd", [0])
                                if isinstance(annotation.get("iscrowd"), list)
                                else [annotation.get("iscrowd", 0)]
                            )
                        ],
                        "confidence": float(annotation.get("confidence", 0.0)),
                        "bbox": bbox,
                        "height": bbox_properties["height"],
                        "width": bbox_properties["width"],
                        "center": bbox_properties["center"],
                        "area": float(annotation.get("area", bbox_properties["area"])),
                        "category": str(
                            category_map.get(annotation.get("category_id"), "Unknown")
                        ),
                        "masks": annotation.get("segmentation", []),
                    }

                    details = {
                        "splitType": get_corresponding_split_type(
                            file_path, include_year=False
                        ),
                        "file_name": image.get("file_name", "unknown"),
                        "annotations": [annotation_json],
                    }

                    key = f"{details['splitType']}/{details['file_name']}"
                    if key in complete_images:
                        complete_images[key]["annotations"].extend(
                            details["annotations"]
                        )
                    else:
                        complete_images[key] = details

                    if "height" in image and "width" in image:
                        details.update(
                            {
                                "image_height": int(image["height"]),
                                "image_width": int(image["width"]),
                                "image_area": int(
                                    image.get(
                                        "area",
                                        float(image["height"]) * float(image["width"]),
                                    )
                                ),
                            }
                        )
                    else:
                        missing_dimensions[key] = details

                    classwise_splits[annotation_json['category']][details['splitType']] += 1
                    processed += 1

                except Exception as e:
                    logging.error(f"Error processing annotation: {e}")
                    skipped += 1
                    continue

            if not annotations:
                missing_annotations.extend(
                    img["id"] for img in images if isinstance(img, dict) and "id" in img
                )

        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")
            traceback.print_exc()

    logging.info("\nFinal summary:")
    logging.info(f"Complete images: {len(complete_images)}")
    logging.info(f"Missing annotations: {len(missing_annotations)}")
    logging.info(f"Missing dimensions: {len(missing_dimensions)}")

    for category, counts in classwise_splits.items():
        counts['total'] = sum(counts.values())
    return {**complete_images, **missing_dimensions}, missing_annotations, classwise_splits


def add_mscoco_dataset_items_details(batch_dataset_items, images_details):
    processed_batch = []
    for dataset_item in batch_dataset_items:
        image_key = f"{get_corresponding_split_type(dataset_item.get('fileLocation'))}/{dataset_item.get('filename')}"
        if image_key not in images_details:
            logging.warning(f"'{image_key}' not found in images_details")
            continue
        dataset_item.update(images_details[image_key])
        processed_batch.append(
            {
                "sample_details": dataset_item,
                "is_complete": all(
                    k in dataset_item
                    for k in ["image_height", "image_width"]
                ),
            }
        )
    return processed_batch