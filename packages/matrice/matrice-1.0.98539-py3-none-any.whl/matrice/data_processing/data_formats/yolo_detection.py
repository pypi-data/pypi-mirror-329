import os
import logging
from collections import defaultdict
import yaml
import traceback

from matrice.data_processing.server_utils import (
    get_corresponding_split_type,
    generate_short_uuid
)

def yolo_to_coco_bbox(yolo_bbox, img_width, img_height):
    """
    Convert YOLO bbox format to MS COCO format.

    Args:
        yolo_bbox (list): [x_center, y_center, width, height] (normalized)
        img_width (int): Image width in pixels
        img_height (int): Image height in pixels

    Returns:
        tuple: (
            coco_bbox [x_min, y_min, width, height],
            coco_bbox_height,
            coco_bbox_width,
            coco_bbox_center [x_center, y_center] in absolute pixels,
            coco_bbox_area
        )
    """
    x_center, y_center, width, height = yolo_bbox

    # Convert to absolute pixel values
    x_min = (x_center - width / 2) * img_width
    y_min = (y_center - height / 2) * img_height
    width = width * img_width
    height = height * img_height

    # COCO bbox center in absolute pixel values
    coco_x_center = x_min + (width / 2)
    coco_y_center = y_min + (height / 2)

    # COCO bbox area
    area = width * height

    # Return results
    return [x_min, y_min, width, height], height, width, [coco_x_center, coco_y_center], area

def convert_payload_to_coco_format(payload):
    """
    Converts YOLO bbox format in payload to MS COCO format.
    
    Args:
        payload (dict): The original payload containing YOLO bbox details.

    Returns:
        dict: Updated payload with COCO bbox format.
    """
    from matrice.data_processing.data_formats.yolo_detection import yolo_to_coco_bbox
    for item in payload["items"]:
        img_width = item["width"]
        img_height = item["height"]
    
        updated_annotations = []
        
        for annotation in item["annotations"]:
            yolo_bbox = annotation["bbox"]  # Extract YOLO bbox [x_center, y_center, width, height]

            # Convert YOLO bbox to COCO format
            coco_bbox, coco_height, coco_width, coco_center, coco_area = yolo_to_coco_bbox(yolo_bbox, img_width, img_height)

            # Update annotation with COCO bbox values
            updated_annotation = {
                "id": annotation["id"],
                "segmentation": annotation["segmentation"],
                "isCrowd": annotation["isCrowd"],
                "confidence": annotation["confidence"],
                "bbox": coco_bbox,  
                "height": float(coco_height),
                "width": float(coco_width),
                "center": coco_center,
                "area": float(coco_area),
                "category": annotation["category"],
                "masks": annotation["masks"],
            }
            updated_annotations.append(updated_annotation)
        
        # Replace annotations with updated COCO annotations
        item["annotations"] = updated_annotations

    return payload

def get_yolo_image_details(annotation_files):
    """Process YOLO annotation files and extract image details.

    Args:
        annotation_files: List of paths to YOLO annotation files (.txt) and data.yaml

    Returns:
        Tuple containing:
        - Dictionary of image details indexed by file location
        - List of image filenames missing annotations
        - Dictionary of class-wise splits from data.yaml
    """
    complete_images = {}
    missing_annotations = []
    classwise_splits = {}
    
    logging.info(f"Processing {len(annotation_files)} annotation files")

    if not annotation_files:
        logging.warning("No annotation files provided")
        return complete_images, missing_annotations, classwise_splits

    # Separate TXT and YAML files
    txt_files = [f for f in annotation_files if f.lower().endswith('.txt')]
    yaml_files = [f for f in annotation_files if f.lower().endswith('.yaml')]

    # Load class names from YAML file
    if yaml_files:
        yaml_file = yaml_files[0]
        try:
            with open(yaml_file, 'r') as f:
                yaml_data = yaml.safe_load(f)
                class_names = yaml_data.get('names', [])
                classwise_splits = {
                    name: {"train": 0, "val": 0, "test": 0, "unassigned": 0}
                    for name in class_names
                }
        except Exception as e:
            logging.error(f"Error reading YAML file {yaml_file}: {e}")
            class_names = []
    else:
        logging.warning("No data.yaml file found. Class splits will not be initialized.")
        class_names = []


    # Process TXT files to extract annotations
    for file_index, txt_file in enumerate(txt_files, 1):
        logging.debug(f"\nProcessing file {file_index}/{len(txt_files)}: {txt_file}")

        if not os.path.exists(txt_file):
            logging.warning(f"File not found: {txt_file}")
            continue

        try:
            filename = os.path.splitext(os.path.basename(txt_file))[0] + ".jpg" # TODO: change to the actual image extension
            split_type = get_corresponding_split_type(txt_file)
            
            if filename.lower().startswith('readme'):
                continue

            annotations = []
            processed = 0
            skipped = 0

            with open(txt_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        parts = line.strip().split()
                        
                        if len(parts) < 5:
                            skipped += 1
                            continue
                        
                        class_id = int(parts[0])
                        bbox = [float(x) for x in parts[1:5]]  # x_center, y_center, width, height
                        
                        # Validate bbox values
                        if not all(0 <= x <= 1 for x in bbox):
                            logging.warning(f"Invalid bbox values in {txt_file}, line {line_num}")
                            skipped += 1
                            continue
                        
                        category = class_names[class_id] if class_id < len(class_names) else str(class_id)
                        
                        
                        bbox_center = [bbox[0], bbox[1]]  
                        bbox_width = bbox[2]  
                        bbox_height = bbox[3]  
                        bbox_area = bbox_width * bbox_height  
                        
                        annotation_json = {
                            "id": str(generate_short_uuid()),
                            "segmentation": [],
                            "isCrowd": [],
                            "confidence": 0.0,
                            "bbox": bbox,  
                            "height": float(bbox_height),
                            "width": float(bbox_width),
                            "center": bbox_center,
                            "area": float(bbox_area),
                            "category": str(category),
                            "masks": []
                        }
                        
                        annotations.append(annotation_json)
                        
                        if category in classwise_splits:
                            classwise_splits[category][split_type] += 1
                        
                        processed += 1
                        
                    except Exception as e:
                        logging.error(f"Error processing line {line_num} in {txt_file}: {e}")
                        skipped += 1
                        continue

            if annotations:
                key = f"{filename}"
                complete_images[key] = {
                    "splitType": split_type,
                    "file_name": filename,
                    "annotations": annotations
                }
            else:
                missing_annotations.append(filename)

        except Exception as e:
            logging.error(f"Error processing file {txt_file}: {e}")
            traceback.print_exc()
            continue

    # Update class-wise splits with totals
    for category, counts in classwise_splits.items():
        counts['total'] = sum(counts.values())

    logging.info("\nFinal summary:")
    logging.info(f"Complete images: {len(complete_images)}")
    logging.info(f"Missing annotations: {len(missing_annotations)}")

    return complete_images, missing_annotations, classwise_splits



def add_yolo_dataset_items_details(batch_dataset_items, images_details):
    processed_batch = []
    for dataset_item in batch_dataset_items:
        image_key = f"{dataset_item.get('filename')}"
        if image_key not in images_details:
            logging.warning(f"'{image_key}' not found in images_details")
            continue
        dataset_item.update(images_details[image_key])
        processed_batch.append(
            {
                "sample_details": dataset_item,
                "is_complete": all(
                    dataset_item.get(k) is not None
                    for k in ["image_height", "image_width"]
                ),
            }
        )
    return processed_batch
