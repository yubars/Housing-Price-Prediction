# -*- coding: utf-8 -*-
"""findZipAverage.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QrRkKdVtB62Gqp-ho7y9OaeaDaXGWEYG
"""

import pandas as pd

data = pd.read_csv("to_bimal_sir.csv")

data.head()

interest = data[["zip", "housePrice"]]

interest.head()

len(interest)

groups = interest.groupby("zip")

len(groups.first())

averagePrice = interest.groupby('zip', as_index=False)['housePrice'].mean()

len(interest["zip"].unique())

averagePrice

averagePrice.to_csv("zipAveragePrice.csv", index=False)
