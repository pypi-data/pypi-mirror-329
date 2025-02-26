import os
import logging
from collections import defaultdict
from matrice.data_processing.server_utils import get_corresponding_split_type
from matrice.data_processing.server_utils import generate_short_uuid


def add_unlabelled_dataset_items_details(batch_dataset_items):
    processed_batch = []
    logging.debug(f"Batch dataset items: {batch_dataset_items}")
    for dataset_item in batch_dataset_items:
        split, category, annotations = get_unlabelled_dataset_item_details(dataset_item.get('fileLocation'))
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




def get_unlabelled_dataset_item_details(image_path):
    parts = os.path.normpath(image_path).split(os.sep)

    # Assuming the prefix is not part of the {split}/{category}/{image} structure
    #split = get_corresponding_split_type(image_path)  # e.g., "val"
    split="unassigned"
    category = ""

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
        "category": category,
        "masks": []
    }]
    return split, category, annotations
