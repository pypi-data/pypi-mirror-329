import os
import logging
from collections import defaultdict
from matrice.data_processing.server_utils import get_corresponding_split_type
from matrice.data_processing.server_utils import generate_short_uuid


def add_imagenet_dataset_items_details(batch_dataset_items):
    processed_batch = []
    logging.debug(f"Batch dataset items: {batch_dataset_items}")
    for dataset_item in batch_dataset_items:
        split, category, annotations = get_imagenet_dataset_item_details(dataset_item.get('fileLocation'))
        dataset_item.update({
            "splitType": split,
            "category": category,
            "annotations": annotations
        })
        processed_batch.append({
                "sample_details": dataset_item,
                "is_complete": all(
                    k in dataset_item
                    for k in ["image_height", "image_width"]
                ),
            })
    logging.debug(f"Processed batch: {processed_batch}")
    return processed_batch




def get_imagenet_dataset_item_details(image_path):
    parts = os.path.normpath(image_path).split(os.sep)

    # Assuming the prefix is not part of the {split}/{category}/{image} structure
    split = get_corresponding_split_type(image_path)  # e.g., "val"
    category = parts[-2]  # e.g., "motor_scooter"

    annotations = [{
        "id": str(generate_short_uuid()),  # Shorter Unique ID
        "segmentation": [],
        "isCrowd": [],
        "confidence": 0.0,
        "bbox": [],
        "height": 0.0,
        "width": 0.0,
        "center": [],
        "area": 0.0,
        "category": str(category),
        "masks": []
    }]

    if split == "unassigned":
        logging.warning(f"No split type for image: {image_path}, category: {category}")

    return split, category, annotations


def get_classwise_splits_imagenet(dataset_items_batches):
    classwise_splits = defaultdict(lambda: {"train": 0, "test": 0, "val": 0, "unassigned": 0})
    logging.debug(f"Dataset items batches: {dataset_items_batches}")
    for batch in dataset_items_batches:
        for item in batch:
            category = item.get('category')
            split_type = item.get('splitType')
            if category is not None and split_type is not None:
                classwise_splits[category][split_type] += 1

    # Only return if there are actual classes found
    if not classwise_splits:
        return None
    # Calculate total for each category
    for category, counts in classwise_splits.items():
        counts['total'] = sum(counts.values())
    return classwise_splits

# def submit_classwise_splits_imagenet(dataset_items_batches, rpc, dataset_id, version):
#     classwise_splits = get_classwise_splits_imagenet(dataset_items_batches)
#     if classwise_splits is not None:
#         add_dataset_class_splits_info(rpc, dataset_id, version, classwise_splits)
#     else:
#         logging.error("No classes found in the dataset")
