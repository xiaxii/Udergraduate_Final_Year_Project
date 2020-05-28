# Final Year Project
## Scope of the project
This is an individual substantial work of a real academic research carried out with my supervisor at Queen Mary University of London. It includes identifying something novel and getting results. 
**My project's scope: software and research.**

## Specification

**Title**: 
Classifying Web Complaints to Twitter

**Scope**: 
Data Science and Artificial Intelligence
 
**Project description**:
Twitter is a popular microblogging platform, similar to Weibo. Users can post short messages that are then sent to their ’followers’. If somebody posts a message that contravenes Twitter’s policies, it is possible for third party organisations to send a complaint. We have been gathering these complaints, and have a large dataset containing over 1 million complained about tweets. The project will involve performing a detailed statistical analysis of this dataset to understand its properties, e.g. how gets complained about, what is contained within their tweets, who send complaints, and how are complaints distributed across accounts? Once the statistical analysis is complete, you will then be expected to build a binary classifier that can automatically identify tweets that may receive complaints. As such, this will allow Twitter to predict which tweets may go on to receive complaints.

**Keywords**: Social media, machine learning, natural language processing 
Main tasks:
1. Collate existing Twitter datasets which contains complaints
2. Perform statistical analysis of complaints to Twitter
3. Build classifier to identify tweets that may receive complaints 
4. Evaluate classifier to profile its precision and recall

**Measurable outcomes**:
1. A collated dataset containing both tweets and complaints 
2. A classifier that can predict if a tweet might get complaints
3. An detailed evaluation of the classifier to show precision and recall

# Introduction
On Twitter, people can post short messages to their followers, which are called tweets. For contents presented on the platform, Twitter has its rules and policy to manage tweets. And Twitter responds to copyright complaints with the guide of the Digital Millennium Copyright Act (DMCA). Web complaint is a common mechanism for reporting offensive content to Twitter.
In practice, the interactions between users, content moderators, and social media platforms are complex and highly strategic.

The most frequently applied response strategy to complaints is asking complainants for further information. However, this does not appease the complainants. (Einwiller and Steilen, 2015) Significantly, complaints are bearing a great deal of weight, arbitrating both the relationship between users, the platform and the negotiation around contentious public issues (Crawford and Gillespie, 2014). As such, it is necessary to build an intelligent classifier to ease the pressure of scrutiny.

## Dataset
| Dataset (csv) | # of Records | Content |
|-------------:| -------------:| -----:|
| reported_tweet | 737,689 | **tweet_id**, user_id, JSON format tweet |
| complaint_tweet |1,863,979 | **tweet_id**, **notice_id**, user_id, tweet_url |
| notices | 157,868 | **notice_id**, notice_type, notice_date_sent, notice_sender_name, notice_action_taken, notice_principal_name, notice_recipient_name |

## Code
Environment: Python 2.7

### Fold 'Analysis':
#### Analysis/extract_reported_tweet.py
1. CSV format reported tweets 
(10 attributes, no hashtags)
2. Hashtags 
(all hashtag text)
3. Plain tweet text 
(just tweet text, no @ # or links)
4. Users 
(user_id, user_name, user_description)

#### Analysis/notice_statistics.py
(notice_id, notice_type)

#### Analysis/statistic_analysis.py
1. Notice type 
(notice_id, notice_type)
2. Notice count
(notice_type,count)

#### Analysis/text_analysis.py
1. Word cloud 
2. Word frequency



### Fold 'Engineering':
#### Engineering/extract_for_classifying.py
Extract reported_tweet.csv to reported_tweet_10num.txt
Tweet JSON -> JSON of ['tweet_id', 'friend_count', 'followers_count','status_count', 'list_count', 'user_favorites_count'， 'retweet_count', 'favorite_count', 'urls_num', 'media_num', 'mention_users_num', 'hashtags']

#### Engineering/one_class_svm_precise_recall_55.py
1. Selected features for SVM
2. Vectorise data
3. Split training set and testing set
4. One-Class SVM, record results (predict,tweet_id,)

#### Engineering/one_class_svm_precise_recall_60.py
Same logic as Engineering/one_class_svm_precise_recall_55.py

#### Engineering/precise and recall.py
1. Collate results to notice type
predict,tweet_id,notice_type
2. Collate results to hashtags
(predict,tweet_id,notice_type,retweet_count,favorite_count,urls_num,media_num,mention_users_num,hashtags)
3. Precise and Recall, F1 Score
4. Word Clouds of both positive and negative hashtag groups
5. Word Frequency of both positive and negative hashtag groups

### Fold 'Other scripts'
Random Forest/ Isolation Forest



