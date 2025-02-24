# selectml/pipeline.py
from .preprocessing import DataPreprocessor
from .models import ModelSelector
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

class ModelSelectionPipeline:
    def __init__(self, model_type='logistic'):
        self.preprocessor = DataPreprocessor()
        self.model_selector = ModelSelector(model_type=model_type)

    def run_pipeline(self, df, target, numerical_features, categorical_features, test_size=0.2, random_state=42):
        """
        Executes the full pipeline:
         - Preprocesses the data
         - Splits into training and test sets
         - Trains the selected model
         - Evaluates model performance
        """
        # Separate features and target
        X = df.drop(columns=[target])
        y = df[target]
        
        # Preprocess features
        X_processed = self.preprocessor.fit_transform(X, numerical_features, categorical_features)
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=test_size, random_state=random_state)
        
        # Train the model
        self.model_selector.train(X_train, y_train)
        
        # Generate predictions and evaluate
        predictions = self.model_selector.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        
        return {
            'accuracy': acc,
            'report': report,
            'model': self.model_selector.model
        }
