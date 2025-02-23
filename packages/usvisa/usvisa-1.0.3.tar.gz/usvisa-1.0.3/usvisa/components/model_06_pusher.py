import sys

from usvisa.cloud_storage.aws_storage import SimpleStorageService
from usvisa.exception import USvisaException
from usvisa.logger import logging
from usvisa.entity.artifact_entity import ModelPusherArtifact, ModelValidateArtifact
from usvisa.entity.config_entity import ModelPusherConfig
from usvisa.entity.s3_estimator import USvisaEstimator


class ModelPusher:
    def __init__(self, model_validate_artifact: ModelValidateArtifact,model_pusher_config: ModelPusherConfig):
        self.s3 = SimpleStorageService()
        self.model_validate_artifact = model_validate_artifact
        self.model_pusher_config = model_pusher_config
        self.usvisa_estimator = USvisaEstimator(bucket_name=model_pusher_config.bucket_name,model_path=model_pusher_config.s3_model_key_path)


    def initiate_model_pusher(self) -> ModelPusherArtifact:
        logging.info("Entered initiate_model_pusher method of ModelTrainer class")

        try:
            logging.info("Uploading artifacts folder to s3 bucket")

            self.usvisa_estimator.save_model(from_file=self.model_validate_artifact.trained_model_path)

            model_pusher_artifact = ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name,s3_model_path=self.model_pusher_config.s3_model_key_path)

            logging.info("Uploaded artifacts folder to s3 bucket")
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelTrainer class")
            
            return model_pusher_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e