import logging
from matrice.data_processing.pipeline import Pipeline
from matrice.data_processing.server import (
    get_mscoco_server_processing_pipeline,
    get_imagenet_server_processing_pipeline,
    get_pascalvoc_server_processing_pipeline,
    get_labelbox_server_processing_pipeline,
    get_yolo_server_processing_pipeline,
    get_unlabelled_server_processing_pipeline,
    get_labelbox_classification_server_processing_pipeline
)
from matrice.data_processing.client import (
    handle_client_processing_pipelines
)
from matrice.data_processing.server import download_dataset

class DataProcessor:
    def __init__(self, session, action_record_id):
        self.session = session
        self.rpc = session.rpc
        self.action_record_id = action_record_id

        url = f"/v1/project/action/{self.action_record_id}/details"
        self.action_doc = self.rpc.get(url)["data"]
        self.action_type = self.action_doc["action"]
        logging.info("Action doc: %s", self.action_doc)
        self.action_details = self.action_doc["actionDetails"]
        logging.info("Action details: %s", self.action_details)
        self.job_params = self.action_doc["jobParams"]
        logging.info("Job params: %s", self.job_params)
        self.account_number = self.action_doc.get("account_number", "")
        logging.info("Account number: %s", self.account_number)
        self.update_status(
            "DCKR_ACK", "ACK", "Action is acknowledged by data processing microservice"
        )

        self.dataset_id = self.job_params["dataset_id"]
        self.source = self.job_params["source"]
        self.source_URL = self.job_params["source_URL"]
        self.input_type = self.job_params["input_type"].lower()
        self.source_version = self.job_params["source_version"]
        self.target_version = self.job_params["target_version"]

        self.destination_bucket_alias = self.job_params.get(
            "destination_bucket_alias", ""
        )
        self.source_bucket_alias = self.job_params.get("source_bucket_alias", "")

        self.PROCESSING_PIPELINES = {
            "mscoco": get_mscoco_server_processing_pipeline,
            "imagenet": get_imagenet_server_processing_pipeline,
            "pascalvoc": get_pascalvoc_server_processing_pipeline,
            "labelbox": get_labelbox_server_processing_pipeline,
            "labelbox_classification": get_labelbox_classification_server_processing_pipeline,
            "yolo": get_yolo_server_processing_pipeline,
            "unlabeled": get_unlabelled_server_processing_pipeline,  # TODO: unlabelled Spelling needs to be corrected from BE
        }
        logging.info("Processing pipelines: %s", self.PROCESSING_PIPELINES.keys())

    def update_status(self, stepCode, status, status_description):
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
            self.rpc.put(path=url, payload=payload)

        except Exception as e:
            logging.error("Exception in update_status: %s", str(e))

    def get_server_processing_pipeline(self) -> Pipeline:
        if self.input_type in self.PROCESSING_PIPELINES:
            logging.info(f"Processing {self.input_type} dataset")
            server_processing_pipeline = self.PROCESSING_PIPELINES[self.input_type](
                self.rpc,
                self.dataset_id,
                self.target_version,
                self.action_record_id,
                self.destination_bucket_alias,
                self.account_number,
            )
        else:
            error_msg = f"Unsupported input type: {self.input_type}. Only mscoco, imagenet, pascalvoc and labelbox are supported of now."
            logging.error(error_msg)
            raise ValueError(error_msg)

        return server_processing_pipeline

    def start_processing(self):
        self.update_status(
            "DCKR_PROC",
            "OK",
            "Dataset processed for importing",
        )
        if self.input_type == "labelbox" or self.input_type == "labelbox_classification" or self.source_URL:
            logging.info("Downloading dataset from source to start client processing")
            dataset_path = download_dataset(self.source_URL, self.input_type, self.dataset_id, self.rpc, self.target_version)

            handle_client_processing_pipelines(
                self.rpc,
                self.dataset_id,
                self.source_version,
                self.target_version,
                self.input_type,
                self.source_URL,
                dataset_path,
                self.destination_bucket_alias,
                self.account_number,
            )

        self.server_processing_pipeline = self.get_server_processing_pipeline()
        logging.info("Starting server processing pipeline")
        self.server_processing_pipeline.start()
        logging.info("Waiting for server processing pipeline to complete")
        self.server_processing_pipeline.wait_to_finish_processing_and_stop()

        self.update_status(
            "SUCCESS",
            "SUCCESS",
            "Dataset processed successfully",
        )
