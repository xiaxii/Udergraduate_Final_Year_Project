import os
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestRegressor

training_set_path = '../../out/one_class_svm_55/training_set.csv'
testing_set_path = '../../out/one_class_svm_55/testing_set.csv'
predict_path = '../../out/random_forest_predict_results.csv'


training_set_data = pd.read_csv(training_set_path)
X_train = pd.DataFrame(training_set_data)
testing_set_data = pd.read_csv(testing_set_path)
X_test = pd.DataFrame(testing_set_data)

X_train.set_index(['tweet_id'], inplace=True)
X_test.set_index(['tweet_id'], inplace=True)

testing_tweet_id = X_test.index.values

# Transform into ndarray
x_train = np.array(X_train)
x_test = np.array(X_test)
print ("Training Set Shape: " + str(x_train.shape))
print ("First 5 rows of training set:")
print X_train.head()
print ("")
print ("Describe training set:")
print X_train.describe()
print ("")

print ("Testing Set Shape: " + str(x_test.shape))
print ("First 5 rows of testing set:")
print X_test.head()
print ("")
print ("Describe testing set:")
print X_test.describe()
print ("")
print ("")

if os.path.exists("random_forest.m"):
    print ("Load RandomForest...")
    RF = joblib.load("random_forest.m")
else:
    print ("Train RandomForest...")
    train_labels = np.ones(len(x_train))
    start = time.clock()
    # fit the Classifier model
    RF = RandomForestRegressor(n_estimators=1000, random_state=42)
    RF.fit(x_train, train_labels);
    # IF = IsolationForest(contamination=0.01, behaviour='new')
    # IF.fit(x_train)
    elapsed1 = (time.clock() - start)
    print ("RandomForest trained...")
    print ("Time used for training: " + str(elapsed1) + " seconds")
    joblib.dump(RF, "random_forest.m")
    print ("RandomForest model saved...")

print ("Predicting...")
# predict_train = time.clock()
# y_pred_train = RF.predict(x_train)
# elapsed2 = (time.clock() - predict_train)
predict_test = time.clock()
y_pred_test = RF.predict(x_test)
elapsed3 = (time.clock() - predict_test)
print ("Prediction finished...")
# print ("Time used for predict training set: " + str(elapsed2) + " seconds")
print ("Time used for predict testing set: " + str(elapsed3) + " seconds")

print ("")
print ("Results:")
# n_error_train = y_pred_train[y_pred_train == -1].size
n_error_test = y_pred_test[y_pred_test == -1].size
# print ("# of error - train: " + str(n_error_train))
print ("# of error - test: " + str(n_error_test))

testing_result_df = pd.DataFrame({'tweet_id': testing_tweet_id, 'predict': y_pred_test})
testing_result_df.to_csv(predict_path, index=False)

# n_error_train = y_pred_train[y_pred_train == -1].size
n_error_test = y_pred_test[y_pred_test == -1].size
# print ("# of error - train: " + str(n_error_train))
print ("# of error - test: " + str(n_error_test))

