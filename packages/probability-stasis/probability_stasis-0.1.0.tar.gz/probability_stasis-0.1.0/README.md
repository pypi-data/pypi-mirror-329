# Probability Stasis Filter Library

A Python library for filtering and stabilizing probability predictions from multiple models.

## Installation
Clone this repository and install locally or just pip install it:
```
pip install .
```

## Usage

### Basic Example
```python
from probability_stasis import StasisFilter
import numpy as np

# Define a simple model
class DummyModel:
    def predict_proba(self, X):
        return np.random.random((len(X), 2))

# Initialize filter and model
filter = StasisFilter(threshold=0.1, window_size=3)
filter.add_model(DummyModel())

# Make predictions
X = np.random.random((5, 10))
predictions = filter.predict(X)
print(predictions[0])  # Filtered probabilities from model 0
```

## API Documentation

### StasisFilter
Main class for probability stasis filtering.

#### Parameters
- `threshold` (float): Maximum allowed probability deviation (default: 0.1)
- `window_size` (int): Number of predictions to track (default: 3)
- `models` (List[PredictionModel], optional): Initial list of prediction models

#### Methods
- `add_model(model)`: Add a new prediction model
- `predict(X)`: Make filtered predictions
- `reset_history()`: Clear prediction history

### PredictionModel
Abstract base class for models. Must implement:
- `predict_proba(X)`: Return probability predictions as numpy array

## Features
- Maintains probability stability within threshold
- Supports multiple models simultaneously
- Rolling window of predictions
- Automatic stabilization when thresholds are exceeded

#### `example_usage.py`
```python
import numpy as np
from probability_stasis import StasisFilter

class SimpleModel:
    def predict_proba(self, X):
        return np.random.random((len(X), 2))

def main():
    # Initialize filter with two models
    filter = StasisFilter(threshold=0.05, window_size=4)
    filter.add_model(SimpleModel())
    filter.add_model(SimpleModel())
    
    # Generate sample data
    X = np.random.random((3, 5))
    
    # Make multiple predictions to demonstrate stasis
    for _ in range(5):
        preds = filter.predict(X)
        print(f"\nPredictions:")
        for model_idx, probs in preds.items():
            print(f"Model {model_idx}: {probs}")

if __name__ == "__main__":
    main()
```

### How to Use the Library

1. **Installation**:
   - Place all files in the directory structure as shown
   - Install using `pip install .` from the `probability_stasis` directory

2. **Basic Usage**:
   - Create a model class that inherits from `PredictionModel` or implements `predict_proba`
   - Initialize `StasisFilter` with desired threshold and window size
   - Add models using `add_model()`
   - Call `predict()` with input data

3. **Key Features**:
   - The filter maintains a history of predictions per model
   - Checks if new predictions deviate beyond the threshold from recent history
   - Stabilizes predictions by averaging when stasis is broken
   - Handles multiple models independently

4. **Customization**:
   - Adjust `threshold` for sensitivity to probability changes
   - Modify `window_size` for how many past predictions to consider
   - Add as many models as needed

This implementation provides a robust, reusable library that can be integrated with various prediction models while ensuring probability stability across predictions. The example shows how to use it with dummy models, but you can replace these with real ML models (e.g., from scikit-learn) that implement the `predict_proba` method.