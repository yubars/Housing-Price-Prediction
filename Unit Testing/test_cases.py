import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from test_functions import encode_state, validate_numerical_data, validate_categorical_data, calculate_r2_score

data = pd.read_csv("New Output/processedData.csv")
X = data.iloc[:, :-1]
y = data["housePrice"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=27)

# Loading our regression model
rf_model = joblib.load("rf_model_95_86_randomState27.joblib")

def test_encode_state():
	assert encode_state("GA") == 9  # Georgia
	assert encode_state("md") == 19  # Maryland
	assert encode_state("ON") == -1  # Ontario
	assert encode_state("bc") == -1  # British Columbia

def test_validate_numerical_features():
	assert validate_numerical_data("Masonry") == False  # User cannot enter a string
	assert validate_numerical_data(9) == True  # User can enter an integer
	assert validate_numerical_data(145.23) == True  # User can enter the float values
	assert validate_numerical_data(4j+2) == False  # User cannot enter the complex numbers
	assert validate_numerical_data(None) == False  # User cannot leave the field empty

def test_validate_categorical_features():
	assert validate_categorical_data("Masonry") == True  # User can enter a string
	assert validate_categorical_data("Rancher123") == True # User can enter a string
	assert validate_categorical_data("") == False  # User cannot enter empty string
	assert validate_categorical_data("2021") == False  # User cannot enter an integer
	assert validate_categorical_data("145.23") == False  # User cannot enter the float values
	assert validate_categorical_data(None) == False  # User cannot leave the field empty

def test_calculate_r2_score():
	assert calculate_r2_score(X_train, y_train, rf_model) >= 90  # Training R2 should exceed 90%
	assert calculate_r2_score(X_test, y_test, rf_model) >= 85  # Test R2 should exceed 85%
