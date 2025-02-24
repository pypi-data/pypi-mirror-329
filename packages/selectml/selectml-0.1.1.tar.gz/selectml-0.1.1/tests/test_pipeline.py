import pandas as pd
from selectml.pipeline import ModelSelectionPipeline

def test_model_selection_pipeline():
    data = {
        'age': [25, 32, 47, 51, 23, 45, 36, 29, 40, 33, 28, 52, 37, 46, 31, 44, 39, 27, 50, 35],
        'income': [50000, 60000, 80000, 90000, 40000, 75000, 65000, 55000, 70000, 62000,
                   48000, 91000, 68000, 77000, 59000, 80000, 72000, 53000, 85000, 66000],
        'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 
                 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 
                 'Fort Worth', 'Columbus', 'Charlotte', 'Indianapolis', 'San Francisco', 
                 'Seattle', 'Denver', 'Washington'],
        'purchased': [0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0]
    }
    df = pd.DataFrame(data)
    
    numerical_features = ['age', 'income']
    categorical_features = ['city']
    
    pipeline = ModelSelectionPipeline(model_type='random_forest')
    result = pipeline.run_pipeline(df, target='purchased', 
                                   numerical_features=numerical_features, 
                                   categorical_features=categorical_features)
    
    assert 'accuracy' in result
    assert 'report' in result
    print("Test passed with accuracy:", result['accuracy'])
