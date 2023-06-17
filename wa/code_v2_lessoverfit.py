
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 21:59:36 2023

@author: abdullahalbinsaleh
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 06:20:43 2023

@author: abdullahalbinsaleh

This version uses normal random data splitting technique 
"""

#-------------------------import librarires-------------------------#
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.feature_selection import RFECV
#-------------------------Load dataset-------------------------#
moneyFlow = pd.read_excel("/Users/abdullahalbinsaleh/Documents/Master of Business Analytics /223 Term/Capstone Project/Dataset/moneyFlow.xlsx")
#moneyFlow = pd.read_excel("moneyFlow.xlsx")

#-------------------------Data Exploration-------------------------#
moneyFlow.head()
moneyFlow.info()
moneyFlow.columns


#-------------------------Data Preparation & Pre-Processing-------------------------#
#drop $ sign from Spot feature 
# convert the 'Spot' column to a string
moneyFlow['Spot'] = moneyFlow['Spot'].astype(str)
moneyFlow['Spot'] = moneyFlow['Spot'].str.replace("$", "")

# convert the 'Spot' column back to float
moneyFlow['Spot'] = moneyFlow['Spot'].astype(float)


#Split Details feature into two features 
moneyFlow[["Size", "Price"]] = moneyFlow["Details"].str.split("@", expand=True)

#drop the Details feature 
moneyFlow.drop(columns=["Details"], inplace=True)

#Find options duration in days 
moneyFlow["Date"] = pd.to_datetime(moneyFlow["Date"])
moneyFlow["Expiration"] = pd.to_datetime(moneyFlow["Expiration"])
moneyFlow["Duration"] = (moneyFlow["Expiration"]-moneyFlow["Date"]).dt.days

#drop the Date, Expiration, and Time Featuers 
moneyFlow.drop(columns=["Time", "Date", "Expiration", "Ticker"], inplace=True)


#Convert categoircal variables into dummy variables 
moneyFlow = pd.get_dummies(moneyFlow, columns=["Type", "Execution", "C/P"])

#Drop missing values 
moneyFlow.dropna(inplace=True)


#-------------------------Feature Selection-------------------------#
# Separate features and target variable
X = moneyFlow.drop("Sentiment", axis=1)
y = moneyFlow["Sentiment"]



#assign selected features using RFE to X
X = moneyFlow[['Strike', 'Spot', 'Open Interest', 'Size', 'Price', 'Duration',
       'Type_SWEEP', 'Execution_ABOVE ASK', 'Execution_AT ASK',
       'Execution_AT BID', 'Execution_AT MIDPOINT', 'Execution_BELOW BID',
       'C/P_CALL', 'C/P_PUT']]

#-------------------------Data Split-------------------------#
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# The dataset is imbalanced due to the underrepresentation of the NEUTRAL class
print(moneyFlow["Sentiment"].value_counts())


# You were using fit_transform for both training and testing data, this is incorrect 
# we should only fir the scaler to the training data and then transform both training and testing data using the fit

#-------------------------Feature Scaling-------------------------#
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)



#-------------------------Logisitc Regression-------------------------#
lr = LogisticRegression(max_iter=10000)
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)

#-------------------------Logisitc Regression Classification Report and Confusion Matrix-------------------------#
print("Logistic Regression classification report:")
print(classification_report(y_test, lr_pred))
print("Logistic Regression confusion matrix:")
print(confusion_matrix(y_test, lr_pred))

# This model may be too Complex and have a tendency to overfit especially if they dont have their hyperparemters optimally tuned
# I lowered n_estimators to 50 and max_depth to 2, to reduce model complexity
#-------------------------Random Forest-------------------------#
rf = RandomForestClassifier(n_estimators=50, max_depth=2, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

#-------------------------Random Forest Classification Report and Confusion Matrix-------------------------#
print("Random Forest classification report:")
print(classification_report(y_test, rf_pred))
print("Random Forest confusion matrix:")
print(confusion_matrix(y_test, rf_pred))

# Modified  regularization parameter

#-------------------------Neural Netowrk-------------------------#
nn = MLPClassifier(hidden_layer_sizes=(16,),max_iter=1000,alpha=1, early_stopping=True, validation_fraction=0.2, random_state=42)
nn.fit(X_train, y_train)
nn_pred = nn.predict(X_test)


#-------------------------Neural Network Classification Report and Confusion Matrix-------------------------#
print("Neural Network classification report:")
print(classification_report(y_test, nn_pred))
print("Neural Network confusion matrix:")
print(confusion_matrix(y_test, nn_pred))



#-------------------------KNN-------------------------#
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
knn_pred = knn.predict(X_test)
#-------------------------KNN Classification Report and Confusion Matrix-------------------------#
print("KNN Confusion Matrix:")
print(confusion_matrix(y_test, knn_pred))
print("\nKNN Classification Report:")
print(classification_report(y_test, knn_pred))

