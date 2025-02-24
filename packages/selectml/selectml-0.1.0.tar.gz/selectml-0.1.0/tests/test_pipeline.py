# tests/test_pipeline.py
import pandas as pd
from selectml.pipeline import ModelSelectionPipeline

def test_model_selection_pipeline():
    # Create a dummy dataset
    data = {
        'age': [25, 32, 47, 51, 23, 45, 36, 29],
        'income': [50000, 60000, 80000, 90000, 40000, 75000, 65000, 55000],
        'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego'],
        'purchased': [0, 1, 0, 1, 0, 1, 1, 0]
    }
    df = pd.DataFrame(data)
    
    numerical_features = ['age', 'income']
    categorical_features = ['city']
    
    # Initialize the pipeline with a Random Forest model
    pipeline = ModelSelectionPipeline(model_type='random_forest')
    result = pipeline.run_pipeline(df, target='purchased', 
                                   numerical_features=numerical_features, 
                                   categorical_features=categorical_features)
    
    # Check that the pipeline returns expected results
    assert 'accuracy' in result
    assert 'report' in result
    print("Test passed with accuracy:", result['accuracy'])

# Run the test with:
# pytest tests/test_pipeline.py
