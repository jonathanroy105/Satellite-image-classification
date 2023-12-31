# -*- coding: utf-8 -*-
"""PA_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dd9bqafjbPLDt2axryVSsKacsGTchmkg
"""

#Importing packages
import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import itertools

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split

# Define the path to the image folder and the target size of the images
img_dir = '/content/drive/MyDrive/data'

# Define the image size
img_size = (32, 32)

def load_images_from_folder(folder):
    images = []
    labels = []
    for filename in os.listdir(folder):
        label = filename.split("_")[0]
        img_path = os.path.join(folder, filename)
        img = Image.open(img_path)
        img = img.convert("RGB")  # Convert to RGB format if needed
        img = img.resize(img_size)
        images.append(np.array(img))
        labels.append(label)
    return np.array(images), np.array(labels)

# Load the images and labels from the directory
X, y = load_images_from_folder(img_dir)

# Reshape the images
X = X.reshape(X.shape[0], -1)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

logreg = LogisticRegression(solver='sag')

# LogisticRegression(max_iter=500)

classifiers = [
    SGDClassifier(loss='log'),
    DecisionTreeClassifier(),
    SVC(),
    KNeighborsClassifier(),
    GaussianNB(),
    RandomForestClassifier()
]

# Define the classifiers to use
classifiers = [
    LogisticRegression(max_iter=1000),
    DecisionTreeClassifier(),
    SVC(),
    KNeighborsClassifier(),
    GaussianNB(),
    RandomForestClassifier()
]

classifiers = [
    LogisticRegression(solver='sag'),
    DecisionTreeClassifier(),
    SVC(),
    KNeighborsClassifier(),
    GaussianNB(),
    RandomForestClassifier()
]

accuracies = []

# Subsample the dataset
X_train_sub, X_test_sub, y_train_sub, y_test_sub = train_test_split(X, y, test_size=0.2)

for clf, accuracy in zip(classifiers, accuracies):
    print(f"{clf.__class__.__name__} Accuracy: {accuracy:.2f}")

for clf in classifiers:
    clf.fit(X_train_scaled, y_train)
    y_pred = clf.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)

# Train the classifiers and get their accuracies
accuracies = []
for clf in classifiers:
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracies.append(accuracy_score(y_test, y_pred))

# Print the accuracies
for i in range(len(classifiers)):
    print("{} accuracy: {:.2f}%".format(classifiers[i].__class__.__name__, accuracies[i] * 100))

# Plot the confusion matrix for each classifier in a single figure
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
for i, clf in enumerate(classifiers):
    ax = axes.ravel()[i]
    y_pred = clf.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    ax.set_xticks(np.arange(len(np.unique(y))))
    ax.set_yticks(np.arange(len(np.unique(y))))
    ax.set_xticklabels(np.unique(y))
    ax.set_yticklabels(np.unique(y))
    ax.set_title("{} Confusion Matrix".format(clf.__class__.__name__))
    fmt = "d"
    thresh = cm.max() / 2.0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        ax.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
plt.tight_layout()
plt.show()