# -*- coding: utf-8 -*-
"""Step 5 Class Updates on Data Preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RmfyP3iWYgMxEssVPT8zF4Z0yIYx94oW

# Data Preprocessing - After Class Update
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
import os
import json
# from pickle import dump
from google.colab import files

# !gdown --id 11n0QOY5LuFQBfZSYrwJuQWVtYohFMjoy

data = pd.read_csv("filtered_data.csv")

data.head()

data.architecturalStyle.value_counts(dropna=False)

data["architecturalStyle"] = data["architecturalStyle"].fillna("Others")

data.architecturalStyle.value_counts(dropna=False)

data.heating.value_counts(dropna=False)

# Because we don't know what type of heating is "Yes"
data = data.drop(data[data["heating"] == "Yes"].index)

data["heating"] = data["heating"].fillna("Others")

data.heating.value_counts(dropna=False)

data.fireplace.value_counts(dropna=False)

data["fireplace"] = data["fireplace"].fillna("Others")

data.fireplace.value_counts(dropna=False)

data.airConditioning.value_counts(dropna=False)

data["airConditioning"] = data["airConditioning"]

data = data.drop(data[data["airConditioning"] == "Partial"].index)

data.airConditioning.value_counts(dropna=False)

data.foundation.unique()

data["foundation"] = data["foundation"].fillna("Others")

data.foundation.unique()

housePrice = data["housePrice"]
data.drop(columns="housePrice", inplace=True)

data["soldYear"] = 2021

data.head()

data["housePrice"] = housePrice

data.head()

data.drop(columns=["unit", "zip4", "water", "sewer", "house"], inplace=True)

data.head()

data["city"].value_counts(dropna=False)

len(data["city"].unique())

data["city"] = data["city"].fillna("Others")

data.city.value_counts(dropna=False)

len(data["city"].unique())

data["street"].value_counts(dropna=False)

data["street"] = data["street"].fillna("Others")

data["street"].value_counts(dropna=False)

len(data["street"].unique())

data["streetSuffix"].value_counts(dropna=False)

data["streetSuffix"].isna().sum()

data["streetSuffix"] = data["streetSuffix"].fillna("Others")

data.isna().sum()

data["zoningDescription"] = data["zoningDescription"].fillna("Others")

data["landUseDescription"] = data["landUseDescription"].fillna("Others")

data["lotTopography"] = data["lotTopography"].fillna("Others")

data.isna().sum()

cols = data.columns
data.dropna(subset=cols, inplace=True)

data.describe()

data.shape



import numpy as np
iqr_hp = np.quantile(data['housePrice'],0.75) - np.quantile(data['housePrice'],0.25)
lower_out_hp = np.quantile(data['housePrice'],0.25) - 1.5* iqr_hp
higher_out_hp = np.quantile(data['housePrice'],0.75) + 1.5* iqr_hp
data = data.drop(data[data["housePrice"] > higher_out_hp].index) 
data = data.drop(data[data["housePrice"] < lower_out_hp].index)
data.head()

data.describe()

data.shape

# iqr_la = np.quantile(data['lotSizeAcres'],0.75) - np.quantile(data['lotSizeAcres'],0.25)
# lower_out_la = np.quantile(data['lotSizeAcres'],0.25) - 1.5*iqr_la
# higher_out_la = np.quantile(data['lotSizeAcres'],0.75) + 1.5*iqr_la
# data = data[data['lotSizeAcres'] < higher_out_la]
# data = data[data['lotSizeAcres'] > lower_out_la] 
# data.describe()

iqr_lsf = np.quantile(data['lotSizeSquareFeet'],0.75) - np.quantile(data['lotSizeSquareFeet'],0.25)
lower_out_lsf = np.quantile(data['lotSizeSquareFeet'],0.25) - 1.5*iqr_lsf
higher_out_lsf = np.quantile(data['lotSizeSquareFeet'],0.75) + 1.5*iqr_lsf
data = data.drop(data[data["lotSizeSquareFeet"] > higher_out_lsf].index) 
data = data.drop(data[data["lotSizeSquareFeet"] < lower_out_lsf].index)
data.describe()



data.head()

iqr_tr = np.quantile(data['totalRooms'],0.75) - np.quantile(data['totalRooms'],0.25)
#lower_out_tr = np.quantile(data['totalRooms'],0.25) - 1.5*iqr_tr
higher_out_tr = np.quantile(data['totalRooms'],0.75) + 1.5*iqr_tr
data = data.drop(data[data["totalRooms"] > higher_out_tr].index) 
#data = data.drop(data[data["lotSizeSquareFeet"] < lower_out_lsf].index)
data.describe()

data.head()

def label_encode(data, column):
  data_copy = data.copy()
  data_copy[column] = data_copy[column].str.lower()
  le = LabelEncoder()
  le.fit(data_copy[column])
  data_copy[column] = le.fit_transform(data_copy[column])
  
  noClasses = le.classes_
  encodings = list(range(len(noClasses)))
  encoding_map = dict(zip(noClasses, encodings))

  return data_copy, encoding_map

categorical_cols = ["city", "street", "streetSuffix", "landUseDescription", "zoningDescription", "lotTopography", "architecturalStyle", "condition", "heating", "airConditioning",	"foundation", "fireplace"]
numerical_cols = ["zip", "latitude", "longitude", "lotSizeAcres",	"lotSizeSquareFeet",	"yearBuilt",	"totalStories",	"totalRooms",	"bedrooms",	"baths", "soldYear"]

data.head()

encodings_database = dict()
for column in categorical_cols:
  data, encoding_map = label_encode(data, column)
  encodings_database[column] = encoding_map

# Encoding State
states = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN",
          "IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV",
          "NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN",
          "TX","UT","VT","VA","WA","WV","WI","WY"]

states = list(map(str.lower, states))
states_dict = dict(zip(states, list(range(50))))
print(states_dict)
encodings_database["state"] = states_dict

for state in data.state.unique():
  data["state"][data["state"] == state] = encodings_database["state"][state.lower()]

data["state"]

data.head()

encodings_database.keys()

encodings_database.values()

for key, values in encodings_database.items():
  print(f"{key}: {len(values)}")

assert len(encodings_database.keys()) == len(encodings_database.values())

data.head()

data.corr()

data["state"]

# NORMALIZATION:
# Now we will be using MinMax Scalar for the Categorical Features
categorical_data = data[categorical_cols]

minMaxScalar = MinMaxScaler()
data[categorical_cols] = minMaxScalar.fit_transform(categorical_data)
data["state"] = data["state"]/49  # For state: Min: 0, Max: 49

data.head()

# Converting the dataframe to numeric
data = data.apply(pd.to_numeric, errors="coerce")

# We use Standard Scalar to scale our numerical data since we have the continuous values without any maximum and minimum values.
numerical_data = data[numerical_cols]

standardScalar = StandardScaler()
data[numerical_cols] = standardScalar.fit_transform(numerical_data)

if not os.path.exists("/content/Output"):
  os.mkdir("/content/Output")

with open("/content/Output/encodings_database.json", "w") as f:
  json.dump(encodings_database, f, indent=3)

data.to_csv("/content/Output/processedData.csv", index=False)

from joblib import dump

dump(minMaxScalar, "/content/Output/minMaxScalar.joblib")
dump(standardScalar, "/content/Output/standardScalar.joblib")

BASE_DIR = "/content/Output/"
filenames = os.listdir(BASE_DIR)
for filename in filenames:
  file_path = os.path.join(BASE_DIR, filename)
  files.download(file_path)

"""# SUMMARY

Since we have only the data for Gwinnett County of GA, the model may be more specific to that county. But we have tried to generalized to other places as well, by introducing the term "Others" for the state, cities, street other than in the Gwinnett County.

We did the following in this notebook:
* We incorporated "**Architectural Style**", "**Fireplace**", "**Heating**" and "**airConditioning**".
* We added two featues i.e. **soldYear** and **lastPriceSold** which are the simulated data from the actualMarketValue.
* Then we encoded all the categorical features using SKLearn **Label Encoder**, and for the **states** we explicitly encoded the values.
* The label encodings are saved in a **JSON file** which provided the information of the mapping of categorical features with exact index used while data preprocessing.
* After that, we normalized the categorical data using **MinMaxScalar** since we had the minimum and maximum values after the label encoding part. 
* For the numerical data, we performed the **Standard Scaling Normalization**, by obtaining the mean and standard deviation.
* The minMaxScalar and standardScalar are dumped into a **pickle file** to use them again while preprocessing the test data.



"""