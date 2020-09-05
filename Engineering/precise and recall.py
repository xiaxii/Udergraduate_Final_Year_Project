import nltk
import pandas as pd
import csv
import json
from wordcloud import WordCloud
from scipy.misc import imread
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
import matplotlib.pyplot as plt
from Analysis.text_analysis import split_text



complaints_path = '../../dataset/complaint_tweet.csv'
notices_type_path = '../../out/dataset_statistics/notice_type.csv'
predict_path = '../../out/one_class_svm_55/predict_results.csv'
merged_results_path = '../../out/one_class_svm_55/merged_results.csv'
testset_complaint_notice = '../../out/one_class_svm_55/testset_complaint_notice.csv'
merged_withNoticeType_path = '../../out/one_class_svm_55/merged_results_noticeType.csv'
extracted_reported_tweet_path = '../../out/dataset_prepared/reported_tweet_10num.txt'
hashtags_merged_reported_tweet_path = '../../out/dataset_prepared/hashtags_merged_tweets.txt'
merged_withHashtags_path = '../../out/one_class_svm_55/merged_results_hashtags.csv'
positive_hashtags_path = '../../out/one_class_svm_55/positive_hashtags.txt'
negative_hashtags_path = '../../out/one_class_svm_55/negative_hashtags.txt'
positive_mask_path = '../../src/Engineering/mask/positive.png'
negative_mask_path = '../../src/Engineering/mask/negative.png'
positive_wordcloud_path = '../../out/one_class_svm_55/wordCloud_positive_hashtags.png'
negative_wordclouds_path = '../../out/one_class_svm_55/wordCloud_negative_hashtags.png'

def join_value(df):
    return','.join(df.values)

def merge():
    complaints_data = pd.read_csv(complaints_path)
    complaints_df = pd.DataFrame(complaints_data)
    complaints_df = complaints_df
    complaints_df.drop(columns=['user_id', 'tweet_url'], inplace=True)
    print complaints_df.head()
    notices_type_data = pd.read_csv(notices_type_path)
    notices_type_df = pd.DataFrame(notices_type_data)
    print notices_type_df.head()

    complaints_notice = pd.merge(complaints_df, notices_type_df, how='left', on='notice_id')
    print complaints_notice.head()
    print complaints_df.shape

    predict = pd.read_csv(predict_path)
    predict_df = pd.DataFrame(predict)
    print predict_df.head()
    print predict_df.shape

    test_complaint_notice = pd.merge(predict_df['tweet_id'], complaints_notice, how='left', on='tweet_id')
    print test_complaint_notice.head()
    print test_complaint_notice.shape
    test_complaint_notice.to_csv(testset_complaint_notice, index=False)

    grouped_results = test_complaint_notice.groupby('tweet_id')
    id = []
    times_complained = []
    for index, data in grouped_results:
        id.append(index)
        times_complained.append(len(data))
    complained_df = pd.DataFrame({'tweet_id': id, 'complained_times': times_complained})
    print complained_df.head()
    print complained_df.shape

    result_df = pd.merge(predict_df, complained_df, how='left', on='tweet_id')
    print result_df.head()
    print result_df.shape

    result_df.to_csv(merged_results_path, index=False)

# TP: complained=1 && predict=1
# TN: complained=-1 && predict=-1
# FP: complained=-1 && predict=1
# FN: complained=1 && predict=-1
# Precise: P=TP/TP+FP
# Recall: R=TP/TP+FN
# F1=(1+a^2)P*R/a^2(P+R), where a=1
def precise_recall():
    result_data = pd.read_csv(merged_results_path)
    result_df = pd.DataFrame(result_data)
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i in range(len(result_df)):
        this_predict = result_df['predict'].iloc[i]
        this_complained = result_df['complained_times'].iloc[i]
        if (this_complained > 0 and this_predict == 1):
            TP += 1
        if (this_complained == 0 and this_predict == -1):
            TN += 1
        if (this_complained == 0 and this_predict == 1):
            FP += 1
        if (this_complained > 0 and this_predict == -1):
            FN += 1
    print ("TP=" + str(TP) + " ,TN=" + str(TN) + ", FP=" + str(FP) + ", FN=" + str(FN))

def merge_with_type():
    test_complaint_notice_data = pd.read_csv(testset_complaint_notice)
    test_complaint_notice_df = pd.DataFrame(test_complaint_notice_data)
    test_complaint_notice_series = test_complaint_notice_df.groupby(['tweet_id'])['notice_type'].apply(join_value)
    test_complaint_notice_df = pd.DataFrame({'tweet_id': test_complaint_notice_series.index,
                                             'notice_type': test_complaint_notice_series.values})
    print test_complaint_notice_df.head()
    print test_complaint_notice_df.shape

    predict = pd.read_csv(predict_path)
    predict_df = pd.DataFrame(predict)
    print predict_df.head()
    print predict_df.shape

    result_df = pd.merge(predict_df, test_complaint_notice_df, how='left', on='tweet_id')
    print result_df.head()
    print result_df.shape
    result_df.to_csv(merged_withNoticeType_path, index=False)

def profile_nonDCMA():
    count = -1
    with open(merged_withNoticeType_path) as results:
        reader = csv.reader(results)
        for row in reader:
            this_row = row
            if row[2].find('DMCA') < 0:
                print this_row
                count += 1
        print ("non-DMCA complained tweets: " + str(count))

def mergeHashtags():
    dataset_head = ['tweet_id', 'retweet_count',
                    'favorite_count', 'urls_num',
                    'media_num', 'mention_users_num','hashtags']
    dataset = []
    with open(extracted_reported_tweet_path) as f:
        data = f.readlines()
        for row in data:
            parse_tweet = json.loads(row)
            hashtags_array = []
            hashtags_json = parse_tweet["hashtags"]
            for i in range(len(hashtags_json)):
                hashtags_array.append(hashtags_json[i]["hashtag_text"])
            # 2. Hashtag words to a string
            hashtags_str = ','.join(hashtags_array)

            this_data = []
            this_data.append("".join(parse_tweet['tweet_id']))
            this_data.append(parse_tweet['retweet_count'])
            this_data.append(parse_tweet['favorite_count'])
            this_data.append(parse_tweet['urls_num'])
            this_data.append(parse_tweet['media_num'])
            this_data.append(parse_tweet['mention_users_num'])
            this_data.append(hashtags_str)
            dataset.append(this_data)
    data_df = pd.DataFrame(dataset, columns=dataset_head)
    data_df.to_csv(hashtags_merged_reported_tweet_path, index=False)

def matchHashtags():
    merged_result = pd.read_csv(merged_withNoticeType_path)
    merged_result_df = pd.DataFrame(merged_result)
    print merged_result_df.columns.values.tolist()
    print merged_result_df.shape

    withHashtags = pd.read_csv(hashtags_merged_reported_tweet_path)
    withHashtags_df = pd.DataFrame(withHashtags)
    print withHashtags_df.columns.values.tolist()
    print withHashtags_df.shape

    result_df = pd.merge( merged_result_df, withHashtags_df, how='left', on='tweet_id')
    print result_df.head()
    print result_df.shape
    result_df.to_csv(merged_withHashtags_path, index=False)

def profile_hashtags():
    predict_result = pd.read_csv(merged_withHashtags_path)
    results_df = pd.DataFrame(predict_result)
    print results_df.head()
    print results_df.shape

    positive_hashtags= []
    negative_hashtags = []
    for i in range(len(results_df)):
        this_hashtags = ''
        if (isinstance(results_df.ix[i,'hashtags'],str)):
            this_hashtags = results_df.ix[i,'hashtags']
        this_predict = results_df.ix[i,'predict']
        if this_predict==1:
            positive_hashtags.append(this_hashtags)
        else:
            negative_hashtags.append(this_hashtags)

    positive_hashtags_file = open(positive_hashtags_path, 'w')
    for j in range(len(positive_hashtags)):
        positive_hashtags_file.write(positive_hashtags[j])
        positive_hashtags_file.write("\n")

    negative_hashtags_file = open(negative_hashtags_path, 'w')
    for k in range(len(negative_hashtags)):
        negative_hashtags_file.write(negative_hashtags[k])
        negative_hashtags_file.write("\n")

def hashtag_word_cloud(file_path, posiNega):
    if (posiNega>0):
        mask = imread(positive_mask_path)
    else:
        mask = imread(negative_mask_path)
    file_content = split_text(file_path)
    wordcloud = WordCloud(scale=4,
                          width=800,
                          height=300,
                          background_color='white',
                          max_words=500,
                          max_font_size=200,
                          random_state=60,
                          collocations=False,
                          mask=mask).generate(" ".join(file_content))

    plt.imshow(wordcloud)
    plt.axis("off")
    if (posiNega>0):
        wordcloud.to_file(positive_wordcloud_path)
    else:
        wordcloud.to_file(negative_wordclouds_path)

    plt.show()


# Run merge() once to merge test_result, complaint and notice
# merge()
# merge_with_type()
# precise_recall()
# profile_nonDCMA()
# mergeHashtags()
# matchHashtags()
# profile_hashtags()
# hashtag_word_cloud(positive_hashtags_path,1)
# hashtag_word_cloud(negative_hashtags_path,-1)


word_list = split_text(positive_hashtags_path)
word_count = nltk.FreqDist(w.lower() for w in word_list)
result = word_count.most_common(10)
for word, frequency in result:
    print('%s: %d' % (word, frequency))