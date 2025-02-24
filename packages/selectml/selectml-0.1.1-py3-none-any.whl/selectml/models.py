from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

class ModelSelector:
    def __init__(self, model_type='logistic'):
        self.model_type = model_type
        if model_type == 'logistic':
            self.model = LogisticRegression()
        elif model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100)
        elif model_type == 'svm':
            self.model = SVC(probability=True)
        else:
            raise ValueError("Unsupported model type. Choose 'logistic', 'random_forest', or 'svm'.")

    def train(self, X, y):
        """Fits the selected model on the training data."""
        self.model.fit(X, y)
        return self

    def predict(self, X):
        """Generates predictions from the fitted model."""
        return self.model.predict(X)

    def predict_proba(self, X):
        """Provides probability estimates if available."""
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X)
        else:
            raise AttributeError("This model does not support probability estimates.")
