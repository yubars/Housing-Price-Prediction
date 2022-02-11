# -*- coding: utf-8 -*-
"""Step 11 Online Learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mPem1WmxODvG0M-SXzks63HrmBNCTAM1
"""

import warnings
warnings.filterwarnings("ignore")

# Installing the packages

# !pip install tensorflow-io
# !pip install kafka-python

# Importing the packages

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
import time 
from kafka import KafkaProducer
import tensorflow as tf
import tensorflow_io as tfio
# import pickle as pkl
from joblib import load

"""Download and setup Kafka for real time data stream simulation. 

"""

# !curl -sSOL https://downloads.apache.org/kafka/2.8.1/kafka_2.12-2.8.1.tgz
# !tar -xzf kafka_2.12-2.8.1.tgz

"""Start Kafka and Zookeeper servers as a daemon processes. Zookeeper is a centralized service for maintaing configuration information, naming, providing distributed synchronization, and providing group services."""

# !./kafka_2.12-2.8.1/bin/zookeeper-server-start.sh -daemon ./kafka_2.12-2.8.1/config/zookeeper.properties
# !./kafka_2.12-2.8.1/bin/kafka-server-start.sh -daemon ./kafka_2.12-2.8.1/config/server.properties

"""### Create a topic to store partitions
Create topic for train and test dataset to store events in Kafka. Kafka is a distributed event streaming platform that lets you read, write, store and process partitions. These events or messages are organized and stored in topics. In simple terms, topic is similar to a folder in a filesystem, and the message are the file in that folder.
"""

# !./kafka_2.12-2.8.1/bin/kafka-topics.sh --create --topic home-train --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
# !./kafka_2.12-2.8.1/bin/kafka-topics.sh --create --topic home-test --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2

"""### Describe the topic for details
Describe command helps us gather details on topic, it's partitions, replicas, and other important information.

"""

# !./kafka_2.12-2.8.1/bin/kafka-topics.sh --describe --topic home-train --bootstrap-server localhost:9092
# !./kafka_2.12-2.8.1/bin/kafka-topics.sh --describe --topic home-test --bootstrap-server localhost:9092

from google.colab import drive
drive.mount('/content/drive')

data = pd.read_csv("/content/drive/MyDrive/Software Engg Regression Analysis/[LATEST] Manish New Data/onlineLearningData.csv")

data.head(10)

train_df, test_df = train_test_split(data, test_size=0.3, shuffle=True)
test_df, validate_df = train_test_split(test_df, test_size= 0.3, shuffle= True)
x_train_df = train_df.drop(["housePrice"], axis=1)
y_train_df = train_df["housePrice"]

x_test_df = test_df.drop(["housePrice"], axis=1)
y_test_df = test_df["housePrice"]

x_validate_df = validate_df.drop(["housePrice"], axis = 1)
y_validate_df = validate_df["housePrice"]

print("Number of training samples: ",len(train_df))
print("Number of testing sample: ",len(test_df))

"""### Convert data to list format
Read each row from the dataframe and convert it to the list format to feed to Kafka.
"""

#Convert each test and train dataframe to list form to feed to kafka
x_train = list(filter(None, x_train_df.to_csv(index=False).split("\n")[1:]))
y_train = list(filter(None, y_train_df.to_csv(index=False).split("\n")[1:]))

x_test = list(filter(None, x_test_df.to_csv(index=False).split("\n")[1:]))
y_test = list(filter(None, y_test_df.to_csv(index=False).split("\n")[1:]))
len(x_train), len(y_train), len(x_test), len(y_test)

NUM_COLUMNS = len(x_train_df.columns)

"""### Create Kafka Producer 
Create Kafka producer which takes in data and sends the record to the partition within a topic in Kafka cluster. 
"""

#send each record to a partition within a topic in kafka cluster
def write_to_kafka(topic, items):
  count=0
  producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
  for message, key in items:
    producer.send(topic, key=key.encode('utf-8'), value=message.encode('utf-8'))
    count += 1 
  producer.flush()
  print("Wrote {0} messages into topic: {1}".format(count, topic))

write_to_kafka("home-train", zip(x_train, y_train))
write_to_kafka("home-test", zip(x_test, y_test))

"""### Online Learning
Unlike traditional training of machine learning models, online learning is based on incrementally learning or updating parameters as soon as the new data points are available. This process continues indefinitely. In the code below, stream_timeout is set to 10000 milliseconds which means as all the messages are consumed from the topic, the dataset will wait for 10 more seconds before timing out and disconnecting from the Kafka cluster. If additional data arrives in that time period, model training resumes. 
"""

online_train_ds = tfio.experimental.streaming.KafkaGroupIODataset(
    topics=["home-train"],
    group_id="cgonline",
    servers="localhost:9092",
    stream_timeout=10000, # in milliseconds, to block indefinitely, set it to -1.
    configuration=[
        "session.timeout.ms=7000",
        "max.poll.interval.ms=8000",
        "auto.offset.reset=earliest"
    ],
)

def decode_kafka_online_item(raw_message, raw_key):
  message = tf.io.decode_csv(raw_message, [[0.0] for i in range(NUM_COLUMNS)])
  key = tf.strings.to_number(raw_key)
  return (message, key)

# We decode the data and their corresponding labels, and store them as a simple array

online_train_ds_temp = online_train_ds.map(decode_kafka_online_item)

final_online_data = list()
final_online_label = list()

for data, label in online_train_ds_temp:
  data = np.array(data)
  label = np.array(label)
  final_online_data.append(data)
  final_online_label.append(label)

final_online_data[:5]

final_online_label[:5]

# Loading the pretrained random forest model

import joblib

rf_model = joblib.load("/content/drive/MyDrive/Software Engg Regression Analysis/[LATEST] Manish New Data/final_rf_model.joblib")

type(rf_model)

# Fitting the pretrained random forest model using the online data

rf_model.fit(final_online_data, final_online_label)

# Now testing the new model predictions on the new online data

preds = rf_model.predict(final_online_data)

from sklearn.metrics import r2_score

print(f"R2-Score: {round(r2_score(final_online_label, preds), 3)}")

# Plotting the predictions on new online data

plt.scatter(final_online_label, preds, c='w', edgecolors='b')
plt.plot(final_online_label, final_online_label, c='r')
plt.xlabel(f"Actual House Price")
plt.ylabel(f"Predicted House Price")
plt.savefig("Validation Regression Calibration Plot.png", dpi=300)
plt.show()