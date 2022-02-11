import pandas as pd
import json
from sklearn.metrics import r2_score

import warnings
warnings.filterwarnings("ignore")

file_path = "New Output/encodings_database.json"
with open(file_path, "r") as file:
	encodings_database = json.load(file)

def encode_state(state):
	'''
	This function returns the label of the code of the entered state.
	Args:
		state: str
			- accepts states in USA

	Returns:
		state_code: int
			- -1 for invalid
			- 0 to 50 for actual state codes
	'''
	state = state.lower()
	if state not in encodings_database["state"].keys():
		state_code = -1
	else:
		print("Passed")
		state_code = encodings_database["state"][state]
	return state_code


def validate_numerical_data(num_col_val):
	'''
	This function validates whether the input numerical column actually has the numerical data
	Args:
		num_col_val: str
			- string with an integer e.g. '56'
	Returns:
		number_flag: bool
			- True if all the data are real numbers
			- False if the data is other than real number
	'''
	valid_number_flag = True
	try:
		float(num_col_val)
	except:
		valid_number_flag = False
		print("Please enter a valid number!")
	else:
		print("Numerical Data: Detected and Validated")

	return valid_number_flag


def validate_categorical_data(cat_col_val):
	'''
	This function validates whether the input categorical column actually has the categorical data
	Args:
		cat_col_val: str
			- actual string value
	Returns:
		valid_categorical_flag: bool
			- True if all the data are strings
			- False if the data is other than strings
	'''
	print(cat_col_val)
	valid_categorical_flag = True
	try:
		float(cat_col_val)
	except:
		if bool(cat_col_val) is False:
			valid_categorical_flag = False
			return valid_categorical_flag
		print("Categorical Data: Detected and Validated!")
	else:
		print("You tried to enter numerical data in categorical column!")
		valid_categorical_flag = False

	return valid_categorical_flag


def calculate_r2_score(X, y, rf_model):
	'''
	This function tests the random forest regression model on new data and returns the performance
	Args:
		X: numpy.array
			- New Test Data
		y: numpy.array
			- Label for new test data
		rf_model: sklearn.RandomForest
			- Random Forest Regression Model

	Returns:
		r2: float
			- The r2 score of the input data X

	'''
	preds = rf_model.predict(X)
	r2 = r2_score(y, preds)
	print(f"The test r2-score is: {r2}.")
	return r2 * 100


