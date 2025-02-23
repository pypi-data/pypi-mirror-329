import sys
from typing import Tuple
import mlflow
from urllib.parse import urlparse
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from neuro_mf  import ModelFactory
from usvisa.exception import USvisaException
from usvisa.logger import logging
from usvisa.utils.main_utils import load_numpy_array_data, load_object, save_object
from usvisa.entity.config_entity import ModelTrainerConfig
from usvisa.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifactTestData
from usvisa.entity.estimator import USvisaModel

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,model_trainer_config: ModelTrainerConfig):
        
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config



    def eval_metrics(self,y_test, y_pred):
            accuracy = accuracy_score(y_test, y_pred) 
            f1 = f1_score(y_test, y_pred)  
            precision = precision_score(y_test, y_pred)  
            recall = recall_score(y_test, y_pred)
            return accuracy, f1, precision, recall

    def get_model_object(self, train: np.array, test: np.array) -> Tuple[object, object]:
        try:
            logging.info("Model Hyperparametertuning and track metrics in mlflow Start")
            logging.info("Wait................")

            mlflow.set_registry_uri("DAGSHUB_URL")
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            with mlflow.start_run():
            
                model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)
                
                x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]

                best_model_detail = model_factory.get_best_model(X=x_train,y=y_train,base_accuracy=self.model_trainer_config.expected_f1_score_train_data)
                model = best_model_detail.best_model
                model_name = best_model_detail.model
                params = best_model_detail.best_parameters
                model_score = best_model_detail.best_score

                logging.info(f"Expected_f1_score_train_data is {self.model_trainer_config.expected_f1_score_train_data}")
                logging.info(f"Model_f1_score_train_data is {model_score}")

    
                y_pred = model.predict(x_test)

                (accuracy, f1, precision, recall) = self.eval_metrics(y_test, y_pred)
            
                mlflow.log_metric('accuracy', accuracy)
                mlflow.log_metric('f1', f1)
                mlflow.log_metric('precision', precision)
                mlflow.log_metric('recall', recall)
                mlflow.log_param("model_name", model_name)
                mlflow.log_param("best_params", params)

                if tracking_url_type_store != "file":

                    mlflow.sklearn.log_model(model, "model")
                else:
                    mlflow.sklearn.log_model(model, "model")
                

                logging.info("Model Hyperparametertuning and track metrics in mlflow End")

                test_data_metric_artifact = ClassificationMetricArtifactTestData(accuracy=accuracy, f1_score=f1, precision_score=precision, recall_score=recall)
            
                return best_model_detail, test_data_metric_artifact
        
        except Exception as e:
            raise USvisaException(e, sys) from e
        

    def initiate_model_trainer(self, ) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        try:
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
            
            best_model_detail ,test_data_metric_artifact = self.get_model_object(train=train_arr, test=test_arr)
            
            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)


            if best_model_detail.best_score < self.model_trainer_config.expected_f1_score_train_data:
                logging.info("No best model found with score more than base score")
                raise Exception("No best model found with score more than base score")

            usvisa_model = USvisaModel(preprocessing_object=preprocessing_obj,trained_model_object=best_model_detail.best_model)
            logging.info("Created usvisa model object with preprocessor and model")
            logging.info("Created best model file path.")
            save_object(self.model_trainer_config.trained_model_file_path, usvisa_model)

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,test_data_metric_artifact=test_data_metric_artifact)
            logging.info(f"Model trainer artifact on test data: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e