# -*- coding: utf-8 -*

import json
import csv
import pandas as pd
import re
import string

complaint_tweet_path = '../../dataset/complaint_tweet.csv'
nonreported_tweet_path = '../../dataset/non_reported_tweets.csv'
notices_path = '../../dataset/notices.csv'
extract_tweet_path = "../../out/dataset_numerical_attributes/nonreported_tweets.csv"
extract_user_path = "../../out/dataset_statistics/user.csv"
hashtag_path = "../../out/dataset_prepared/hashtags.txt"
plain_tweet_path = "../../out/dataset_prepared/content.txt"
complaint = pd.read_csv(complaint_tweet_path)


def check_json_format(raw_msg):
  if isinstance(raw_msg, str):
    try:
      json.loads(raw_msg, encoding='utf-8')
    except ValueError:
      return False
    return True
  else:
    return False

def create_csv(path, csv_head):
    with open(path, 'wb') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(csv_head)


def write_csv(path, data_row):
    with open(path, 'a+') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(data_row)


def strip_links(text):
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text


def strip_all_entities(text):
    entity_prefixes = ['@', '#']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


def extract_info():
    extract_tweet_head = ["tweet_id", "user_id", "friend_count", "followers_count", "status_count", "list_count",
                          "user_favorites_count", "retweet_count", "favorite_count", "urls_num", "has_media",
                          "mention_users"]
    create_csv(extract_tweet_path, extract_tweet_head)
    extract_user_head = ["id", "name", "description"]
    create_csv(extract_user_path, extract_user_head)
    # hashtag_file = open(hashtag_path, 'w')
    # plain_tweet_file = open(plain_tweet_path, "w")
    with open(nonreported_tweet_path) as tweets:
        reader = csv.reader(tweets)
        for row in reader:
            if check_json_format(row[2]):
                parse_tweet = (json.loads(row[2]))
                lang = parse_tweet.get("lang").encode("utf-8")
                if (lang == "en"):
                    tweet_id = "".join(parse_tweet['id_str']).encode("utf-8")
                    user_id = parse_tweet['user']['id_str'].encode("utf-8")
                    friend_count = parse_tweet['user']['friends_count']
                    followers_count = parse_tweet['user']['followers_count']
                    status_count = parse_tweet['user']['statuses_count']
                    list_count = parse_tweet['user']['listed_count']
                    user_favorites_count = parse_tweet['user']['favourites_count']
                    retweet_count = parse_tweet['retweet_count']
                    favorite_count = parse_tweet['favorite_count']
                    urls_num = len(parse_tweet['entities']['urls'])
                    media_num = 0
                    if (parse_tweet['entities'].has_key('media') == True):
                        media_num = (len(parse_tweet['entities']['media']))
                    mention_users_num = len(parse_tweet['entities']['user_mentions'])

                    data_row = []
                    data_row.append(tweet_id)
                    data_row.append(user_id)
                    data_row.append(friend_count)
                    data_row.append(followers_count)
                    data_row.append(status_count)
                    data_row.append(list_count)
                    data_row.append(user_favorites_count)
                    data_row.append(retweet_count)
                    data_row.append(favorite_count)
                    data_row.append(urls_num)
                    data_row.append(media_num)
                    data_row.append(mention_users_num)

                    write_csv(extract_tweet_path, data_row)

                    hashtag_text = []
                    hashtags = parse_tweet['entities']['hashtags']
                    for i in range(len(hashtags)):
                        this_hashtag = hashtags[i]['text'].encode("utf-8")
                        hashtag_text.append(this_hashtag)
                        hashtag_file.write(this_hashtag + ", ")
                    hashtag_file.write("\n")

                    tweet_fulltext = ""
                    if (parse_tweet.has_key('text') == True):
                        tweet_fulltext = parse_tweet['text'].encode("utf-8")
                    tweet_plaintext = re.sub(r"This Tweet from", "", tweet_fulltext)
                    tweet_plaintext = re.sub(r"has been withheld in response to a report from the copyright holder", "",
                                             tweet_plaintext)
                    tweet_plaintext = re.sub(r"Learn more", "", tweet_plaintext)
                    tweet_plaintext = strip_all_entities(strip_links(tweet_plaintext))
                    plain_tweet_file.write(tweet_plaintext + "\n")
                    print tweet_plaintext

                    user_name = parse_tweet['user']['name'].encode("utf-8")
                    user_description = ""
                    if (parse_tweet['user'].has_key('description') == True):
                        user_description = parse_tweet['user']['description'].encode("utf-8")
                        user_description = strip_links(user_description)
                    user_row = []
                    user_row.append(user_id)
                    user_row.append(user_name)
                    user_row.append(user_description)
                    print user_row
                    write_csv(extract_user_path, user_row)


extract_info()
