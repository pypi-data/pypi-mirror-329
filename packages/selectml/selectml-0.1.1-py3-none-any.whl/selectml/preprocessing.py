import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

class DataPreprocessor:
    def __init__(self):
        self.preprocessor = None

    def fit_transform(self, df, numerical_features, categorical_features):
        """Fits transformers on numerical and categorical features and transforms the data."""
        numeric_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(handle_unknown='ignore')
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numerical_features),
                ('cat', categorical_transformer, categorical_features)
            ]
        )
        return self.preprocessor.fit_transform(df)

    def transform(self, df):
        """Transforms new data using the previously fitted transformer."""
        if self.preprocessor is None:
            raise ValueError("The preprocessor has not been fitted. Call fit_transform() first.")
        return self.preprocessor.transform(df)
