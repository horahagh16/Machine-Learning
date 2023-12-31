# -*- coding: utf-8 -*-
"""ML2-99243032-Haghighatkhah.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ovvu2-JOGja5QrXHibDrSdZ_XrYd-FWg
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from google.colab import drive

drive.mount('drive')

dataset_address = 'drive/MyDrive/Car_prices_classification.csv'
df = pd.read_csv(dataset_address)
df

df.isnull().sum()

del df['generation_name']
del df['city']
del df['province']
del df['Unnamed: 0']
df

#one hot encoding
mark = pd.get_dummies(df['mark'])
df = pd.concat([df,mark],axis=1)

model = pd.get_dummies(df['model'])
df = pd.concat([df,model],axis=1)

fuel = pd.get_dummies(df['fuel'])
df = pd.concat([df,fuel],axis=1)

df

del df['mark']
del df['model']
del df['fuel']

from sklearn.preprocessing import StandardScaler
df[['year', 'mileage', 'vol_engine']] = StandardScaler().fit_transform(df[['year', 'mileage', 'vol_engine']])
df

from sklearn.model_selection import train_test_split

X = df.drop(['price_class'],axis=1)
y = df['price_class']
#80-20
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Fit logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Make predictions on test data
y_pred = model.predict(X_test)

# Calculate accuracy score
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("Accuracy:", accuracy*100,'%')

#implementation



def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def cost_function(X, y, theta):
    m = y.size
    h = sigmoid(X @ theta)
    J = -1 / m * (y @ np.log(h) + (1 - y) @ np.log(1 - h))
    grad = 1 / m * X.T @ (h - y)
    return J, grad

def gradient_descent(X, y, theta, alpha, num_iters):
    m = y.size
    J_history = np.zeros(num_iters)

    for i in range(num_iters):
        cost, grad = cost_function(X, y, theta)
        theta -= alpha * grad
        J_history[i] = cost

    return theta, J_history

# Initialize parameters to zeros
theta = np.zeros(360)

# Set hyperparameters
alpha = 0.1
num_iters = 1000

# Train logistic regression model
theta, J_history = gradient_descent(X_train, y_train, theta, alpha, num_iters)

# Make predictions on test data
y_pred = sigmoid(X_test @ theta)
y_pred = y_pred >= 0.5

# Calculate accuracy on test set
accuracy2 = np.mean(y_pred == y_test) *100
print("Accuracy:", accuracy2,'%')

import numpy as np
from scipy.optimize import fmin_tnc


class my_class:

    @staticmethod
    def sigmoid(x):
        # Activation function used to map any real value between 0 and 1
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def net_input(theta, x):
        # Computes the weighted sum of inputs Similar to Linear Regression

        return np.dot(x, theta)

    def probability(self, theta, x):
        # Calculates the probability that an instance belongs to a particular class

        return self.sigmoid(self.net_input(theta, x))

    def cost_function(self, theta, x, y):
        # Computes the cost function for all the training samples
        m = x.shape[0]
        total_cost = -(1 / m) * np.sum(
            y * np.log(self.probability(theta, x)) + (1 - y) * np.log(
                1 - self.probability(theta, x)))
        return total_cost

    def gradient(self, theta, x, y):
        # Computes the gradient of the cost function at the point theta
        m = x.shape[0]
        return (1 / m) * np.dot(x.T, self.sigmoid(self.net_input(theta, x)) - y)

    def fit(self, x, y, theta):
        opt_weights = fmin_tnc(func=self.cost_function, x0=theta, fprime=self.gradient,
                               args=(x, y.flatten()))
        self.w_ = opt_weights[0]
        return self

    def predict(self, x):
        theta = self.w_[:, np.newaxis]
        return self.probability(theta, x)

    def accuracy(self, x, actual_classes, probab_threshold=0.5):
        predicted_classes = (self.predict(x) >= probab_threshold).astype(int)
        predicted_classes = predicted_classes.flatten()
        accuracy = np.mean(predicted_classes == actual_classes)
        return accuracy * 100

X = df.drop(['price_class'],axis=1)
y = df['price_class']

    # filter out the applicants that got admitted
admitted = df.loc[y == 1]

    # filter out the applicants that din't get admission
not_admitted = df.loc[y == 0]

    # preparing the data for building the model

X = np.c_[np.ones((X.shape[0], 1)), X]
y = y[:, np.newaxis]
theta = np.zeros((X.shape[1], 1))

    # Logistic Regression from scratch using Gradient Descent
model = my_class()
model.fit(X, y, theta)
accuracy = model.accuracy(X, y.flatten())
parameters = model.w_
print("accuracy",accuracy,'%')

x_values = [np.min(X[:, 1] - 2), np.max(X[:, 2] + 2)]
y_values = - (parameters[0] + np.dot(parameters[1], x_values)) / parameters[2]

thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
accuracy_scores = []
for threshold in thresholds:
    y_pred_thresh = [1 if proba >= threshold else 0 for proba in y_pred]
    accuracy = accuracy_score(y_test, y_pred_thresh)
    accuracy_scores.append(accuracy)

# Plot accuracy scores over different threshold values
plt.plot(thresholds, accuracy_scores)
plt.title('Logistic Regression Accuracy Rate over Thresholds')
plt.xlabel('Thresholds')
plt.ylabel('Accuracy')
plt.show()

model = LogisticRegression(max_iter=1000)
# Train model for decreasing values of regularization strength (C)
C_values = [10 ** i for i in range(-1, 1)]
train_errors = []
test_errors = []
accuracies = []
for C in reversed(C_values):
    model.set_params(C=C)
    model.fit(X_train, y_train)
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    train_error = 1 - accuracy_score(y_train, train_pred)
    test_error = 1 - accuracy_score(y_test, test_pred)
    accuracy = accuracy_score(y_test, test_pred)
    train_errors.append(train_error)
    test_errors.append(test_error)
    accuracies.append(accuracy)

# Plot graphs of error reduction and increasing accuracy
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(C_values, train_errors, label='Training error')
plt.plot(C_values, test_errors, label='Test error')
plt.xscale('log')
plt.xlabel('Regularization strength (C)')
plt.ylabel('Error rate')
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(C_values, accuracies)
plt.xscale('log')
plt.xlabel('Regularization strength (C)')
plt.ylabel('Accuracy')
plt.tight_layout()
plt.show()

# Report final score
print('Final accuracy score:', accuracies[-1])




############################################################


# -*- coding: utf-8 -*-
"""ML2-proj2-99243032-haghighatkhah.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YWaQhj9Y_Vudw9dfe1YMbCr9w64PXyRi
"""

from sklearn.datasets import load_iris
iris = load_iris()
X = iris.data
y = iris.target

# Import necessary libraries
from sklearn.datasets import load_iris
import numpy as np
import matplotlib.pyplot as plt

# Load the iris dataset
iris = load_iris()

# Define the input and output data for Setosa and Versicolor classes
X = iris.data[:100, (0,1)]  # use sepal length and width as input for first 100 rows
y = iris.target[:100]       # consider only first 100 rows, where 0 corresponds to Setosa and 1 to Versicolor
y[y == 0] = -1              # convert Setosa class label from 0 to -1

# Define the perceptron class
class Perceptron:
    def __init__(self, eta=0.1, n_iter=100):
        self.eta = eta                 # learning rate
        self.n_iter = n_iter           # number of iterations
        self.weights = None            # weights after fitting
        self.bias = None               # bias after fitting
        self.errors = []               # list to store number of misclassifications at each epoch
        
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)  # initialize weights to 0
        self.bias = 0                        # initialize bias to 0
        for _ in range(self.n_iter):
            error_count = 0
            for i in range(n_samples):
                linear_model = np.dot(X[i], self.weights) + self.bias  # calculate linear model output
                y_predicted = np.where(linear_model > 0, 1, -1)         # predict class label
                error = y[i] - y_predicted                              # calculate error
                self.weights += self.eta * error * X[i]                 # update weights
                self.bias += self.eta * error                            # update bias
                if error != 0:
                    error_count += 1
            self.errors.append(error_count)
                
    def predict(self, X):
        linear_model = np.dot(X, self.weights) + self.bias  # calculate linear model output
        return np.where(linear_model > 0, 1, -1)             # predict class label
    
# Create a perceptron object and fit the data
perceptron = Perceptron()
perceptron.fit(X, y)
cr=0
total = len(X)
for x, label in zip(X, y):
    if perceptron.predict(x) == label:
        cr += 1
print("Accuracy",cr / total*100,'%')
# Plot the samples and decision boundary
x1_min, x1_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
x2_min, x2_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, 0.1), np.arange(x2_min, x2_max, 0.1))
Z = perceptron.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
Z = Z.reshape(xx1.shape)
plt.contourf(xx1, xx2, Z, alpha=0.4)
plt.scatter(X[:, 0], X[:, 1], c=y, alpha=0.8)

# Plot the weight vector
w1, w2 = perceptron.weights
xmin, xmax = plt.xlim()
ymin, ymax = plt.ylim()
xvals = np.array([xmin, xmax])
yvals = -(xvals * w1 + perceptron.bias) / w2
plt.plot(xvals, yvals, '--', c='red', label='Decision boundary')

plt.xlabel("sepal length")
plt.ylabel("sepal width")
plt.title("Perceptron decision boundary")
x1_min, x1_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
x2_min, x2_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
x1_mid = (x1_min + x1_max)/2
x2_mid = (x2_min + x2_max)/2
plt.arrow(x1_mid,x2_mid, w1, w2, head_width=0.1, head_length=0.1, label='Weight vector')
plt.legend()
plt.show()

# Plot the error change graph
plt.plot(range(1, len(perceptron.errors) + 1), perceptron.errors, marker='o')
plt.xlabel('Epochs')
plt.ylabel('Number of misclassifications')
plt.title('Perceptron error change')
plt.show()

# Print the final error value
print("Final error:", perceptron.errors[-1])