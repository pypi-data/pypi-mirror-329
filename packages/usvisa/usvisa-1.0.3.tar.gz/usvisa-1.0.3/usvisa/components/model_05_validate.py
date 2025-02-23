from usvisa.entity.config_entity import ModelValidateConfig,ModelTrainerConfig
from usvisa.entity.artifact_entity import ModelTrainerArtifact, DataIngestionArtifact, ModelValidateArtifact
from sklearn.metrics import f1_score
from usvisa.exception import USvisaException
from usvisa.constants import TARGET_COLUMN, CURRENT_YEAR
from usvisa.logger import logging
import sys
import pandas as pd
from typing import Optional
from usvisa.entity.s3_estimator import USvisaEstimator
from dataclasses import dataclass
from usvisa.entity.estimator import TargetValueMapping

@dataclass
class ValidateModelResponse:
    trained_model_test_data_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool


class ModelValidate:

    def __init__(self, model_trainer_config:ModelTrainerConfig, model_val_config: ModelValidateConfig, data_ingestion_artifact: DataIngestionArtifact,model_trainer_artifact: ModelTrainerArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.model_val_config = model_val_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e

    def get_best_model(self) -> Optional[USvisaEstimator]:
        try:
            bucket_name = self.model_val_config.bucket_name
            model_path=self.model_val_config.s3_model_key_path
            usvisa_estimator = USvisaEstimator(bucket_name=bucket_name,model_path=model_path)

            if usvisa_estimator.is_model_present(model_path=model_path):
                return usvisa_estimator
            return None
        except Exception as e:
            raise  USvisaException(e,sys)
        
    def validate_model(self) -> ValidateModelResponse:
        try:
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            test_df['company_age'] = CURRENT_YEAR - test_df['yr_of_estab']

            x, y = test_df.drop(TARGET_COLUMN, axis=1), test_df[TARGET_COLUMN]
            y = y.replace(TargetValueMapping()._asdict())

            best_model = self.get_best_model()
            best_model_f1_score = None

            if best_model is not None:
                y_hat_best_model = best_model.predict(x)
                best_model_f1_score = f1_score(y, y_hat_best_model)
            else:
                best_model_f1_score = 0

            trained_model_test_data_f1_score = None  
            if self.model_trainer_artifact is not None:

                trained_model_test_data_f1_score = self.model_trainer_artifact.test_data_metric_artifact.get('f1_score') if isinstance(self.model_trainer_artifact.test_data_metric_artifact, dict) else self.model_trainer_artifact.test_data_metric_artifact.f1_score

            if trained_model_test_data_f1_score is not None:
                logging.info(f"Expected_f1_score_train_test is {self.model_trainer_config.expected_f1_score_test_data}")
                is_model_accepted = trained_model_test_data_f1_score > best_model_f1_score
                logging.info(f"Model_f1_score_train_test is {trained_model_test_data_f1_score}")
            elif best_model_f1_score > 0:
                logging.info(f"Best_Model_Expected_f1_score_new_test_data is {self.model_trainer_config.expected_best_model_f1_score_new_test_data}")
                is_model_accepted = best_model_f1_score >= self.model_trainer_config.expected_best_model_f1_score_new_test_data
                logging.info(f"Best_Model_f1_score_new_test_data is {best_model_f1_score}")
            else:
                logging.info("No trained or best model available, forcing retraining.")
                is_model_accepted = False


            return ValidateModelResponse(
                trained_model_test_data_f1_score=trained_model_test_data_f1_score,
                best_model_f1_score=best_model_f1_score,
                is_model_accepted=is_model_accepted
            )

        except Exception as e:
            raise USvisaException(e, sys)


    def initiate_model_Validate(self) -> ModelValidateArtifact:  
        try:
            validate_model_response = self.validate_model()
            s3_model_path = self.model_val_config.s3_model_key_path

            model_validate_artifact = ModelValidateArtifact(
                is_model_accepted=validate_model_response.is_model_accepted,
                s3_model_path=s3_model_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path if self.model_trainer_artifact else None
            )

            logging.info(f"Model validate artifact: {model_validate_artifact}")
            return model_validate_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e
