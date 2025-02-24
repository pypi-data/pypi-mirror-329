# SelectML

**SelectML** is an all‑in‑one pipeline for model selection, data preprocessing, training, and evaluation tailored for classification tasks. Designed for data scientists, it streamlines the process of choosing the most suitable model without requiring additional imports.

## Features

- **Data Preprocessing:** Automatic scaling and one‑hot encoding.
- **Model Selection:** Choose between logistic regression, random forest, or SVM.
- **Integrated Pipeline:** Automatically split data, train models, and evaluate performance.

## Installation

Install via pip (after publishing):

```bash
pip install selectml
```

## Quick Start
```python
import pandas as pd
from selectml import ModelSelectionPipeline

# Sample dataset
data = {
    'age': [25, 32, 47, 51, 23, 45, 36, 29],
    'income': [50000, 60000, 80000, 90000, 40000, 75000, 65000, 55000],
    'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego'],
    'purchased': [0, 1, 0, 1, 0, 1, 1, 0]
}
df = pd.DataFrame(data)

numerical_features = ['age', 'income']
categorical_features = ['city']

# Initialize pipeline with desired model type
pipeline = ModelSelectionPipeline(model_type='random_forest')
result = pipeline.run_pipeline(df, target='purchased', 
                               numerical_features=numerical_features, 
                               categorical_features=categorical_features)

print("Accuracy:", result['accuracy'])
print("Classification Report:\n", result['report'])
```

## License
This project is licensed under the MIT License.
