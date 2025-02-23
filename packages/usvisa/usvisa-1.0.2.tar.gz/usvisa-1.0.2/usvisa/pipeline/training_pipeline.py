import sys
from usvisa.exception import USvisaException
from usvisa.logger import logging
from usvisa.components.data_01_ingestion import DataIngestion
from usvisa.components.data_02_validation import DataValidation
from usvisa.components.data_03_transformation import DataTransformation
from usvisa.components.model_04_trainer import ModelTrainer
from usvisa.components.model_05_validate import ModelValidate
from usvisa.components.model_06_pusher import ModelPusher


from usvisa.entity.config_entity import (DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig,ModelValidateConfig,ModelPusherConfig)

from usvisa.entity.artifact_entity import (DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,ModelValidateArtifact,ModelPusherArtifact)



class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_validate_config = ModelValidateConfig()
        self.model_pusher_config = ModelPusherConfig()


    def start_data_ingestion(self) -> DataIngestionArtifact:

        try:
            logging.info("<----------Entered the start_data_ingestion method of TrainPipeline class---------->")
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact, data_value = data_ingestion.initiate_data_ingestion()
            logging.info("----->Exited the start_data_ingestion method of TrainPipeline class<-----")
            return data_ingestion_artifact, data_value
        except Exception as e:
            raise USvisaException(e, sys) from e
        


    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        logging.info("<----------Entered the start_data_validation method of TrainPipeline class---------->")

        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=self.data_validation_config)
            data_validation_artifact, drift_status = data_validation.initiate_data_validation()
            logging.info("Performed the data validation operation")
            logging.info("----->Exited the start_data_validation method of TrainPipeline class<-----")
            return data_validation_artifact, drift_status

        except Exception as e:
            raise USvisaException(e, sys) from e



    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        logging.info("<----------Entered the start_data_transformation method of TrainPipeline class---------->")
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,data_transformation_config=self.data_transformation_config,data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("----->Exited the start_data_transformation method of TrainPipeline class<-----")
            return data_transformation_artifact
        
        except Exception as e:
            raise USvisaException(e, sys)
        



    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        logging.info("<----------Entered the start_model_trainer method of TrainPipeline class---------->")
        try:
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,model_trainer_config=self.model_trainer_config)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("----->Exited the start_model_trainer method of TrainPipeline class<-----")
            return model_trainer_artifact

        except Exception as e:
            raise USvisaException(e, sys)
        

    def start_model_validate(self, data_ingestion_artifact: DataIngestionArtifact, model_trainer_artifact: ModelTrainerArtifact) -> ModelValidateArtifact:
        logging.info("<----------Entered the start_model_validate method of TrainPipeline class---------->")
        try:
            model_validate = ModelValidate(model_trainer_config=self.model_trainer_config, model_val_config=self.model_validate_config, data_ingestion_artifact=data_ingestion_artifact,model_trainer_artifact=model_trainer_artifact)
            model_validate_artifact = model_validate.initiate_model_Validate()
            logging.info("----->Exited the start_model_validate method of TrainPipeline class<-----")
            return model_validate_artifact
        
        except Exception as e:
            raise USvisaException(e, sys)
        


    def start_model_pusher(self, model_validate_artifact: ModelValidateArtifact) -> ModelPusherArtifact:
        logging.info("<----------Entered the start_model_pusher method of TrainPipeline class---------->")
        try:
            model_pusher = ModelPusher(model_validate_artifact=model_validate_artifact,model_pusher_config=self.model_pusher_config)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info("----->Exited the start_model_pusher method of TrainPipeline class<-----")
            return model_pusher_artifact
        
        except Exception as e:
            raise USvisaException(e, sys)
        

    
    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact,data_value = self.start_data_ingestion()

            if data_value:
                data_validation_artifact, drift_status = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

                if drift_status:  
                    logging.info("Drift detected! Proceeding with retraining...")
                    data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)
                    model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

                else:
                    logging.info("No drift found, validating model performance on new data...")
                    model_validate_artifact = self.start_model_validate(data_ingestion_artifact=data_ingestion_artifact, model_trainer_artifact=None)

                    if model_validate_artifact is None or not model_validate_artifact.is_model_accepted:
                        logging.info("Model performance degraded or no valid model found! Retraining required...")
                        data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)
                        model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
                    else:
                        logging.info("Model is performing well, skipping pipeline.")
                        return
                    
                f1_score = model_trainer_artifact.test_data_metric_artifact.get('f1_score') if isinstance(model_trainer_artifact.test_data_metric_artifact, dict) else model_trainer_artifact.test_data_metric_artifact.f1_score

                if f1_score > self.model_trainer_config.expected_f1_score_test_data:
                    model_validate_artifact = self.start_model_validate(data_ingestion_artifact=data_ingestion_artifact, model_trainer_artifact=model_trainer_artifact)

                    if model_validate_artifact.is_model_accepted:
                        model_pusher_artifact = self.start_model_pusher(model_validate_artifact=model_validate_artifact)
                    else:
                        logging.info("Model not accepted // Model is performing well  skipping push to production.")
                else:
                    logging.info(f"Model F1-score in test data ({f1_score}) is not better than expected ({self.model_trainer_config.expected_f1_score_test_data}), skipping pipeline.")
            else:
                logging.info("<---------->No data change detected. Skipping All Pipeline<---------->")
        except Exception as e:
            logging.error(f"An error occurred during pipeline execution: {str(e)}")
            raise e
        