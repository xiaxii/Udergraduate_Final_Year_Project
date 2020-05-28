from wordcloud import WordCloud
from scipy.misc import imread
import re
# NLTK: https://gist.github.com/sebleier/55428
# Method 1. PYTHON CONSOLE:
# nltk.download()
# Method 2. TERMINAL:
# python -m nltk.downloader -u http://nltk.github.com/nltk_data/
# Method 3. DOWNLOAD AT: http://www.nltk.org/nltk_data/
import nltk
from nltk.corpus import stopwords
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')
hashtag_path = "../../out/dataset_prepared/hashtags.txt"
content_path = "../../out/dataset_prepared/content.txt"


def split_text(file_path):
    text = open(file_path).read()
    # to find the 's following the pronouns. re.I is refers to ignore case
    pat_is = re.compile("(it|he|she|that|this|there|here)(\'s)", re.I)
    # to find the 's following the letters
    pat_s = re.compile("(?<=[a-zA-Z])\'s")
    # to find the ' following the words ending by s
    pat_s2 = re.compile("(?<=s)\'s?")
    # to find the abbreviation of not
    pat_not = re.compile("(?<=[a-zA-Z])n\'t")
    # to find the abbreviation of would
    pat_would = re.compile("(?<=[a-zA-Z])\'d")
    # to find the abbreviation of will
    pat_will = re.compile("(?<=[a-zA-Z])\'ll")
    # to find the abbreviation of am
    pat_am = re.compile("(?<=[I|i])\'m")
    # to find the abbreviation of are
    pat_are = re.compile("(?<=[a-zA-Z])\'re")
    # to find the abbreviation of have
    pat_ve = re.compile("(?<=[a-zA-Z])\'ve")

    text = pat_is.sub(r"\1 is", text)
    text = pat_s.sub("", text)
    text = pat_s2.sub("", text)
    text = pat_not.sub(" not", text)
    text = pat_would.sub(" would", text)
    text = pat_will.sub(" will", text)
    text = pat_am.sub(" am", text)
    text = pat_are.sub(" are", text)
    text = pat_ve.sub(" have", text)
    text = text.replace('\'', ' ')

    word_list = re.split(' |!|\?|\.|\,|\n|\t', text)
    word_list = filter(lambda x: x, word_list)  # filter blanks

    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '_', '-',
                            '&amp;']
    word_list = [word for word in word_list if word not in english_punctuations]
    stops = set(stopwords.words("english"))
    stops = [x.encode('UTF8') for x in stops]
    stops.append("tweet")
    stops.append("amp")
    word_list = [word for word in word_list if word.lower() not in stops]

    return word_list


def word_cloud(file_path, name):
    mask = imread("./mask/"+name+".png")
    file_content = split_text(file_path)
    wordcloud = WordCloud(scale=4,
                          width=800,
                          height=300,
                          background_color='white',
                          max_words=500,
                          max_font_size=150,
                          random_state=60,
                          collocations=False,
                          mask=mask).generate(" ".join(file_content))

    plt.imshow(wordcloud)
    plt.axis("off")
    wordcloud.to_file("../../out/wordCloud_" + name + ".png")

    plt.show()


# Helper function
def print_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        print("\nTopic #%d:" % topic_idx)
        print(" ".join([words[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))


def frequency(file_path, file_name, color):
    word_list = split_text(file_path)
    word_count = nltk.FreqDist(w.lower() for w in word_list)
    result = word_count.most_common(10)
    for word, frequency in result:
        print('%s: %d' % (word, frequency))

    count_dict = word_count.most_common(10)
    words = [w[0] for w in count_dict]
    counts = [w[1] for w in count_dict]
    x_pos = np.arange(len(words))

    plt.figure(2, figsize=(15, 15 / 1.6180))
    # plt.subplot(title='10 most common words - ' + file_name)
    # sns.set_context("notebook", font_scale=2.5, rc={"lines.linewidth": 1.5})
    if color == 1:
        sns.barplot(x_pos, counts, palette= sns.color_palette("Blues_r",10))
    else:
        sns.barplot(x_pos, counts, palette= sns.color_palette("BuGn_r",10))
    plt.xticks(x_pos, words, rotation=30)
    plt.xlabel('words', fontsize=18)
    plt.ylabel('counts', fontsize=18)
    plt.tick_params(labelsize=18)
    plt.subplots_adjust(left=0.15, bottom=0.128)
    plt.savefig('../../out/10_frequent_words_' + file_name + '_inReport.png')
    plt.show()


# Helper function
def print_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        print("\nTopic #%d:" % topic_idx)
        print(" ".join([words[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
def profile_dataset():
    # Generate Word Clouds
    word_cloud(hashtag_path, "hashtag")
    word_cloud(content_path, "content")

    # Analyse the Word Frequency
    print ("In hashtags: ")
    frequency(hashtag_path, 'hashtag', 1)
    print ("")
    print ("In tweets: ")
    frequency(content_path, 'content', 2)


# Load the LDA model from sklearn
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.feature_extraction.text import CountVectorizer

# def lda_analysis(file_path):
#     with open(file_path) as f:
#         text = f.readlines()
#     # Initialise the count vectorizer with the English stop words
#     count_vectorizer = CountVectorizer(stop_words='english')
#     # Fit and transform the processed titles
#     count_data = count_vectorizer.fit_transform(text)
#
#     # Tweak the two parameters below
#     number_topics = 30
#     number_words = 10
#     # Create and fit the LDA model
#     lda = LDA(n_components=number_topics, n_jobs=-1)
#     lda.fit(count_data)
#     # Print the topics found by the LDA model
#     print("Topics found via LDA:")
#     print_topics(lda, count_vectorizer, number_words)

# Tried LDA
# lda_analysis(content_path)
