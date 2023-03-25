import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

# helps in creating the pipeline for onehotencoding,standardscaling or other techniques
from sklearn.compose import ColumnTransformer

# for missing values 
from sklearn.impute import SimpleImputer

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

@dataclass
class dataTransformationConfig:
    preprocessor_ob_file_path = os.path.join('artifacts', "preprocessor.pkl")
    
class dataTransformation:
    def __init__(self):
        self.data_transformation_config = dataTransformationConfig()
        
    def get_data_transformer(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]
            #handeling missing value
            #handle standard scaler
            
            num_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy = "median")),
                    ("scaler", StandardScaler()) 
                ]
            )
            #we can use target guided encoder..but generally we have less number of categories we use onehotencoder
            
            cat_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy = "most_frequent")),
                    ("onehotencoder",OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean = False))
                ]
            )
            
            logging.info(f"Numerical columns: {numerical_columns}")
            
            logging.info(f"Categorical columns: {categorical_columns}")
            
            '''
            To combine the both num_pipeline and cat_pipeline we use ColumnTransfomer
            '''
            
            pre_processor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline,numerical_columns),
                    ("cat_pipeline", cat_pipeline,categorical_columns)
                ]
            )
            
            return pre_processor
            
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("Reading trainning ans testing data")
            
            logging.info("Obtaining pre-processing object")
            
            preprocessing_obj = self.get_data_transformer()
            
            target_columns_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]
            
            input_feature_train_df = train_df.drop(columns = [target_columns_name],axis = 1)
            target_feature_train_df = train_df[target_columns_name]
            
            input_feature_test_df = test_df.drop(columns = [target_columns_name],axis = 1)
            target_feature_test_df = test_df[target_columns_name]
            
            logging.info(
                f"Applying pre-processing object on training dataframes and testing dataframes."
            )
            
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr =  preprocessing_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]
            
            logging.info(f"Saved pre-processing object.")
            
            save_object(
                file_path = self.data_transformation_config.preprocessor_ob_file_path,
                obj = preprocessing_obj
            )
            
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_ob_file_path,
            )
        
        except Exception as e:
            raise CustomException(e,sys)