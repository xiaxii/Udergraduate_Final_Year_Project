# Extract reported_tweet.csv to reported_tweet_10num.txt
# Tweet JSON -> JSON of
# ['tweet_id', 'friend_count', 'followers_count',
# 'status_count', 'list_count', 'user_favorites_count'
# 'retweet_count', 'favorite_count', 'urls_num'
# 'media_num', 'mention_users_num', 'hashtags']

import json
import csv

reported_tweet_path = '../../dataset/reported_tweet.csv'
complaint_tweet_path = '../../dataset/complaint_tweet.csv'
notices_path = '../../dataset/notices.csv'
extracted_reported_tweet_path = '../../out/dataset_prepared/reported_tweet_10num.txt'

def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


def judge_pure_english(keyword):
    return all(ord(c) < 128 for c in keyword)

with open(extracted_reported_tweet_path, 'w') as output_file:
    with open(reported_tweet_path) as tweets:
        reader = csv.reader(tweets)
        for row in reader:
            if row[2]:
                my_dict = {}
                if is_json(row[2]):
                    parse_tweet = (json.loads(row[2]))
                    lang = parse_tweet.get("lang").encode("utf-8")
                    if (lang == "en"):
                        # tweet_id = "".join(parse_tweet['id_str'])
                        # match complaints

                        my_dict['tweet_id'] = "".join(parse_tweet['id_str'])
                        my_dict['friend_count'] = parse_tweet['user']['friends_count']
                        my_dict['followers_count'] = parse_tweet['user']['followers_count']
                        my_dict['status_count'] = parse_tweet['user']['statuses_count']
                        my_dict['list_count'] = parse_tweet['user']['listed_count']
                        my_dict['user_favorites_count'] = parse_tweet['user']['favourites_count']
                        my_dict['retweet_count'] = parse_tweet['retweet_count']
                        my_dict['favorite_count'] = parse_tweet['favorite_count']
                        my_dict['urls_num'] = len(parse_tweet['entities']['urls'])
                        if ('media' in parse_tweet):
                            my_dict['media_num'] = len(parse_tweet['entities']['media'])
                        else:
                            my_dict['media_num'] = 0
                        my_dict['mention_users_num'] = len(parse_tweet['entities']['user_mentions'])

                        hashtag_texts = []
                        hashtags = parse_tweet['entities']['hashtags']
                        for i in range(len(hashtags)):
                            this_hashtag = {}
                            if (judge_pure_english(hashtags[i]['text'])):
                                this_hashtag['hashtag_text'] = hashtags[i]['text']
                                hashtag_texts.append(this_hashtag)
                        my_dict['hashtags'] = hashtag_texts

                        back_json = json.dumps(my_dict)
                        output_file.write(back_json + '\n')
                        print is_json(back_json)

output_file.close()