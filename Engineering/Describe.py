import pandas as pd
# fully display descriptions on Python console
pd.set_option('display.max_columns', None)

def discribe_dataset():
    nd_array_path = "../../out/one_class_svm_60/withID_dataset_ndarray.csv"
    csv_file = nd_array_path
    csv_data = pd.read_csv(csv_file, index_col=0)
    data_df = pd.DataFrame(csv_data)
    data_df = data_df[['retweet_count', 'favorite_count', 'urls_num',
                       'media_num', 'mention_users_num']]
    print ("Dataset Shape: " + str(data_df.shape))
    print ("(one column for tweet_id)")
    print ("Describing:")
    print data_df.describe()

def describe_results():
    result_path = "../../out/one_class_svm_55/merged_results_hashtags.csv"
    result_file = result_path
    result_data = pd.read_csv(result_file, index_col=0)
    data_df = pd.DataFrame(result_data)
    data_df = data_df[['retweet_count', 'favorite_count', 'urls_num',
                       'media_num', 'mention_users_num']]
    print ("Dataset Shape: " + str(data_df.shape))
    print ("(one column for tweet_id)")
    print ("Describing:")
    print data_df.describe()

describe_results()