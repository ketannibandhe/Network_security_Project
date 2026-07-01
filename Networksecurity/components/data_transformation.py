import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from Networksecurity.constant.training_pipeline import TARGET_COLUMN
# we should be knowing which column to drop ad hence we are import target column

from Networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
# data_transformation imputer parameters which we are going to apply in the KNN imputer

from Networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from Networksecurity.entity.config_entity import DataTransformationConfig
from Networksecurity.exception.exception import NetworkSecurityException 
from Networksecurity.logging.logger import logging
from Networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:  ## these 2 are the inputs we initially want for the data transformation
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_transformer_object(cls)->Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
        logging.info(
            "Entered get_data_trnasformer_object method of Trnasformation class"
        )
        try:
           imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
        # ** means whatever parameters we provide to the function, it will consider them as a Key-Value Pair

           logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
           processor:Pipeline=Pipeline([("imputer",imputer)])
           return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        # Note that DataTransformationArtifact:is the output of our data transformation

        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            # Once we run the main.py file then, 2 files train and test files will be created.
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            #then we will remove the target column from the train path

            ## training dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            # we will replace the classification problem, change -1 to 0 because we will not use -1 foe calculation
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            #testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor=self.get_data_transformer_object()

            preprocessor_object=preprocessor.fit(input_feature_train_df)
            # learns the preprocessing parameters.
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            # applies those learned parameters. 
            transformed_input_test_feature =preprocessor_object.transform(input_feature_test_df)
             

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ]
            test_arr = np.c_[ transformed_input_test_feature, np.array(target_feature_test_df) ]

            #save numpy array data
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessor_object,)

            save_object( "final_model/preprocessor.pkl", preprocessor_object,)


            #preparing artifacts

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact


            
        except Exception as e:
            raise NetworkSecurityException(e,sys)