# RapidUseML

Minimalistic Machine Learning Toolset used for quick training and usage of various models. 
One click for training, one click for prediction.


## Usage:

### Basics:

Prepare basic necessities for usage.

```
import RapidUse                                            # Ensure class is imported.
ml = RapidUse.ML()                                         # Create instance of class.
from pandas import read_csv                                # Get pandas to read CSVs.
```


### Prediction:

Predicts target value(s) based on input data provided, with automated model identification.
Note: ML.prdict(...) checks the folder and all directories within the folder its located in for the relevant model. 

```
input_dataset = read_csv("input_dataset.csv")              # Load dataset for pred.
target_column = "column_d"                                 # Prediction target.
prediction_set = ml.predict(input_dataset, target_column)  # Try to obtain ML pred.
```

### Training:

Trains many models based on dataset, select top 3 and optimise them for better performance.

```
training_dataset = read_csv("training_dataset.csv")        # Load dataset for training.
input_column_names = ["column_a", "column_b", "column_c"]  # What features to predict with.
target_column = "column_d"                                 # What component you want predicted.
train_test_ratio = 0.8                                     # What data % to dedicate to training.
ml.train(training_dataset, input_column_names, target_column, train_test_ratio)
```
