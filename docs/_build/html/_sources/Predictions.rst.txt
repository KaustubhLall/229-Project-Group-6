Predictions
===========

The models that we used are as follow,

Logistic Regression
-------------------
inear regression attempts to model the relationship between two variables by fitting a linear equation to observed data. One variable is considered to be an explanatory variable, and the other is considered to be a dependent variable. For example, a modeler might want to relate the weights of individuals to their heights using a linear regression model.

Our code for LR,

.. code-block:: python
   
   lr = LogisticRegression()
   lr.fit(X_train,y_train1)
   lr_pred = lr.predict(X_test)
   print('Logistic Regression Accuracy is:', lr.score(X_test,y_test) *100)
   print('MSE of Logistic Regression is:', mean_squared_error(y_test,y_pred))

And the results are,

Logistic Regression Accuracy is: 82.26470588235294

MSE of Logistic Regression is: 0.156354856775963





Random Forest
-------------
Random Forest Regression is a supervised learning algorithm that uses ensemble learning method for regression. Ensemble learning method is a technique that combines predictions from multiple machine learning algorithms to make a more accurate prediction than a single model.

Our code for RFR,

.. code-block:: python
   
   rf = RandomForestRegressor(random_state=10)
   rf.fit(X_train, y_train)
   rf_pred = rf.predict(X_test)
   print('Accuracy of RF:',rf.score(X_test, y_test)*100)
   print('MSE of RF:',mean_squared_error(y_test, rf_pred))

And the results are as follow,

Accuracy of RF: 99.7561930048138

MSE of RF: 0.00458275145253684



XG Boost
--------
XGBoost is a decision-tree-based ensemble Machine Learning algorithm that uses a gradient boosting framework. In prediction problems involving unstructured data (images, text, etc.) artificial neural networks tend to outperform all other algorithms or frameworks.


.. code-block:: python

   xg = XGBRegressor()
   xg.fit(X_train,y_train)
   xg_pred = model.predict(X_test)
   print('Accuracy of xg:',xg.score(X_test, y_test)*100)
   print('MSE of xg:',mean_squared_error(y_test, xg_pred))

And the results are,

Accuracy of xg: 92.56345347128218

MSE of xg: 0.13666653804454992



K-Nearest Neighbor
------------------
A k-nearest-neighbor algorithm, often abbreviated k-nn, is an approach to data classification that estimates how likely a data point is to be a member of one group or the other depending on what group the data points nearest to it are in.
Our code for KNN was,

.. code-block:: python

   knn = KNeighborsRegressor()
   knn.fit(X_train, y_train)
   knn_pred = knn.predict(X_test)
   print('Accuracy of KNN:', knn.score(X_test, y_test)*100)
   print('MSE of KNN:', mean_squared_error(y_test,knn_pred))

And the results are as follow,

Accuracy of KNN: 94.96360157328218

MSE of KNN: 0.0946673502454992

Decision Tree
-------------
A decision tree is a diagram or chart that helps determine a course of action or show a statistical probability. The chart is called a decision tree due to its resemblance to the namesake plant, usually outlined as an upright or a horizontal diagram that branches out.
Our code for DT,


.. code-block:: python
   
   dt = DecisionTreeRegressor(random_state=30)
   dt.fit(X_train, y_train)
   dt_pred = dt.predict(X_test)
   print('Accuracy of DT:',dt.score(X_test, y_test)*100)
   print('MSE of DT:',mean_squared_error(y_test, dt_pred))

And the results are as follow,

Accuracy of DT: 98.18377005896648

MSE of DT: 0.0341390139116203

Support Vector Machine
----------------------
A support vector machine (SVM) is machine learning algorithm that analyzes data for classification and regression analysis. SVM is a supervised learning method that looks at data and sorts it into one of two categories. An SVM outputs a map of the sorted data with the margins between the two as far apart as possible.

Our code for SVM,

.. code-block:: python
   
   svm1 = svm.SVC()
   svm1.fit(X_train, y_train)
   svm1_pred = svm1.predict(X_test)
   print('Accuracy of SVM:',svm1.score(X_test, y_test)*100)
   print('MSE of SVM:',mean_squared_error(y_test, y_pred))

And the results are,

Accuracy of SVM: 85.9637012311018

MSE of SVM: 0.1456653572654952

Results
-------
.. list-table:: Results
   :widths: 25 25 50
   :header-rows: 1

   * - Models
     - Accuracy
     - MSE
   * - LR
     - 82.26470588235294
     - 0.156354856775963
   * - Random Forest
     - 99.7561930048138
     - 0.00458275145253684
   * - XG Boost
     - 92.56345347128218
     - 0.13666653804454992
   * - KNN
     - 94.96360157328218
     - 0.0946673502454992
   * - DT
     - 98.18377005896648
     - 0.0341390139116203
   * - SVM
     - 85.9637012311018
     - 0.1456653572654952
