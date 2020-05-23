# Final Year Project
## Scope of the project

A final year project must involve substantial work by an individual student in one or both of the following areas:

**Implementation**: this must involve the development of a system. This can be software or hardware design. For software systems, the project should involve a substantial amount of programming with proper software engineering principles being used.

**Research**: this should be real academic research carried out with one of the research teams in BUPT or QM and must include identifying something novel and getting results. It usually involves using a simulator or a tool such as MATLAB – it is not just reading papers and writing a summary.

**My project's scope: software and research.**

## Specification

**Titel**: 
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

## Dataset
| Dataset (csv) | # of Records | Content |
|-------------:| -------------:| -----:|
| reported_tweet | 737,689 | **tweet_id**, user_id, JSON format tweet |
| complaint_tweet |1,863,979 | **tweet_id**, **notice_id**, user_id, tweet_url |
| notices | 157,868 | **notice_id**, notice_type, notice_date_sent, notice_sender_name, notice_action_taken, notice_principal_name, notice_recipient_name |
  
## Early Term Progress



