import json
import pandas as pd
from sklearn import svm
import gensim
from gensim.models import Word2Vec
import os
import numpy as np
from sklearn.model_selection import train_test_split
import time
from sklearn.externals import joblib

# JSON format
extracted_reported_tweet_path = '../../out/dataset_prepared/reported_tweet_10num.txt'
dataset_ndarry_path = '../../out/withID_dataset_ndarray.csv'
training_set_path = '../../out/one_class_svm_55/training_set.csv'
testing_set_path = '../../out/one_class_svm_55/testing_set.csv'
predict_path = '../../out/one_class_svm_55/predict_results.csv'
one_class_svm_file = 'one_class_svm_55.m'

# fully display descriptions on Python console
# pd.set_option('display.max_columns', None)

def word_to_vec (hashtag_array, model):
    hashtags_matrix = []
    for hashtag in hashtag_array:
        if hashtag in model:
            hashtags_matrix.append(np.array(model[hashtag]))
    average_vector = []
    column_num = model.vector_size
    for i in range(0, column_num,1):
        average_vector.append(0)
    row_num = len(hashtags_matrix)
    row_i = 0
    for weight_index, vector in enumerate(hashtags_matrix):
        for i in range(0, column_num, 1):
            average_vector[i] += float(vector[i])
            row_i +=1
    for i in range(0, column_num, 1):
        if row_num!=0:
            average_vector[i] = average_vector[i] / row_num
    return average_vector


def features_for_svm():
    # 1. Train the word2vec model, to express word in vectors
    if os.path.exists("./model"):
        model = gensim.models.Word2Vec.load("./model")
    else:
        hashtags_matrix = []
        with open(extracted_reported_tweet_path) as f:
            data = f.readlines()
            # print ("Dataset Shape: ("+str(len(data))+", "+str(len(data[0]))+")")
            for row in data:
                parse_tweet = json.loads(row)
                parse_tweet_hashtags = parse_tweet["hashtags"]
                this_hashtags = []
                for i in range(len(parse_tweet_hashtags)):
                    this_hashtags.append(parse_tweet_hashtags[i]["hashtag_text"])
                hashtags_matrix.append(this_hashtags)
        model = Word2Vec(hashtags_matrix, min_count=1, size=50)  # train the model
        model.save("./model")

    dataset = []
    dataset_head = ['tweet_id', 'retweet_count',
                    'favorite_count', 'urls_num',
                    'media_num', 'mention_users_num']
    for i in range(50):
        dataset_head.append("hashtag_vec_"+str(i))
    # 5 numerical attributes and 50D hashtag vector

    with open(extracted_reported_tweet_path) as f:
        data = f.readlines()
        for row in data:
            parse_tweet = json.loads(row)
            hashtags_array = []
            hashtags_json = parse_tweet["hashtags"]
            for i in range(len(hashtags_json)):
                hashtags_array.append(hashtags_json[i]["hashtag_text"])
            # 2. Hashtag words to vec
            hashtags_vec = word_to_vec(hashtags_array, model)

            this_data = []
            this_data.append("".join(parse_tweet['tweet_id']))
            this_data.append(parse_tweet['retweet_count'])
            this_data.append(parse_tweet['favorite_count'])
            this_data.append(parse_tweet['urls_num'])
            this_data.append(parse_tweet['media_num'])
            this_data.append(parse_tweet['mention_users_num'])
            this_data.extend(hashtags_vec)
            dataset.append(this_data)
    data_df = pd.DataFrame(dataset, columns=dataset_head)
    data_df.to_csv(dataset_ndarry_path, index=False)


def split_train_test():
    csv_file = dataset_ndarry_path
    csv_data = pd.read_csv(csv_file)
    data_df = pd.DataFrame(csv_data)
    print ("Dataset Shape: " + str(data_df.shape))
    print ("(one column for tweet_id)")

    # 3. separate in to (train):(test)= 8:2
    train_target = [i for i in range(len(data_df))]
    # X is the data, Y stands for label
    X_train, X_test, Y_train, Y_test = train_test_split(data_df, train_target, test_size=0.2, random_state=0)
    # data type of X_train, X_test: dataframe
    X_train.to_csv(training_set_path, index=False)
    X_test.to_csv(testing_set_path, index=False)

def one_class_svm(num):
    training_set_data = pd.read_csv(training_set_path)
    testing_set_data = pd.read_csv(testing_set_path)
    X_train = pd.DataFrame(training_set_data)
    X_test = pd.DataFrame(testing_set_data)
    if (num == 5):
        X_train = X_train['retweet_count', 'favorite_count', 'urls_num',
                           'media_num', 'mention_users_num']
        X_test = X_test['retweet_count', 'favorite_count', 'urls_num',
                          'media_num', 'mention_users_num']
    if (num == 50):
        X_train = X_train.drop(['retweet_count', 'favorite_count', 'urls_num',
                          'media_num', 'mention_users_num'])
        X_test = X_test['retweet_count', 'favorite_count', 'urls_num',
                        'media_num', 'mention_users_num']


    X_train.set_index(['tweet_id'], inplace=True)
    X_test.set_index(['tweet_id'], inplace=True)

    testing_tweet_id = X_test.index.values

    # Transform into ndarray
    x_train = np.array(X_train)
    x_test = np.array(X_test)
    print ("Training Set Shape: "+str(x_train.shape))
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

    # 4. One-Class SVM
    if os.path.exists(one_class_svm_file):
        print ("Load OneClassSVM...")
        clf = joblib.load(one_class_svm_file)
    else:
        print ("Train OneClassSVM...")
        start = time.clock()
        # fit the One-Class SVM model
        clf = svm.OneClassSVM(nu=0.1, kernel='rbf', gamma=0.1)
        # clf = IsolationForest(max_samples=256, random_state=rng)
        clf.fit(x_train)
        elapsed1 = (time.clock() - start)
        print ("OneClassSVM trained...")
        print ("Time used for training: " + str(elapsed1) + " seconds")
        joblib.dump(clf, one_class_svm_file)
        print ("OneClassSVM model saved...")

    print ("")
    print ("Predicting...")
    # predict_train = time.clock()
    # y_pred_train = clf.predict(x_train)
    # elapsed2 = (time.clock() - predict_train)
    predict_test = time.clock()
    y_pred_test = clf.predict(x_test)
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

    testing_result_df = pd.DataFrame({'tweet_id':testing_tweet_id, 'predict': y_pred_test})
    testing_result_df.to_csv(predict_path, index=False)

# run only features_for_svm() once before one_class_svm()
# features_for_svm()
# split_train_test()
one_class_svm()


