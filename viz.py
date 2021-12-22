import pandas as pd
import streamlit as st
import re
import mysql.connector
import plotly.express as px
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import plotly.graph_objects as go

db_connection = mysql.connector.connect(
    host="localhost",
    user="root2",
    password="password",
    database="TwitterDB",
    charset = 'utf8',
    auth_plugin='mysql_native_password'
)

def pie_chart(search_for):
    #pie_chart_1
    query = "SELECT id_str, text, created_at, polarity, user_location FROM {}".format(search_for)
    df = pd.read_sql(query, con=db_connection)
    df['sentiment'] = df['polarity'].apply(lambda x: 'Positive' if x > 0 else ('Neutral' if x == 0 else "Negative"))
    fig = px.pie(df, values=df['sentiment'].value_counts(), names=df['sentiment'].value_counts().index)
    st.title('Polarity of overall tweets in the Database.')
    st.plotly_chart(fig)
    #pie_chart_2
    query = "SELECT id_str, text, created_at, polarity, user_location FROM {} order by created_at desc limit 1000".format(search_for)
    df = pd.read_sql(query, con=db_connection)
    df['sentiment'] = df['polarity'].apply(lambda x: 'Positive' if x > 0 else ('Neutral' if x == 0 else "Negative"))
    fig = px.pie(df, values=df['sentiment'].value_counts(), names=df['sentiment'].value_counts().index)
    st.title('Polarity of most recent 1000 tweets.')
    st.plotly_chart(fig)

def topic_tracking(search_for):
    query = "SELECT id_str, text, created_at, polarity, user_location FROM {}".format(search_for)
    df = pd.read_sql(query, con=db_connection)
    content = ' '.join(df["text"])
    content = re.sub(r"http\S+", "", content)
    content = content.replace('RT ', ' ').replace('&amp;', 'and').replace('amp', '')
    content = re.sub('[^A-Za-z0-9]+', ' ', content)
    content = content.lower()
    tokenized_word = word_tokenize(content)
    stop_words=set(stopwords.words("english"))
    filtered_sent=[]
    for w in tokenized_word:
        if w not in stop_words:
            filtered_sent.append(w)
    fdist = FreqDist(filtered_sent)
    fd = pd.DataFrame(fdist.most_common(10), columns = ["Word","Frequency"]).drop([0]).reindex()
    fig = px.bar(fd, x="Word", y="Frequency")
    st.title('Topic Tracking')
    st.write(fig)

def line_chart(search_for):
    query = "SELECT id_str, text, created_at, polarity, user_location FROM {} order by created_at desc limit 1000".format(search_for)
    df = pd.read_sql(query, con=db_connection)
    df['created_at'] = pd.to_datetime(df['created_at'])
    result = df.groupby([pd.Grouper(key='created_at', freq='5s'), 'polarity']).count().unstack(fill_value=0).stack().reset_index()
    result = result.rename(columns={ "id_str": "Num of '{}' mentions".format(search_for), "created_at":"Time in UTC" })
    fig = px.area(result, x='Time in UTC', y="Num of '{}' mentions".format(search_for), color='polarity')
    st.title('Polarity over Time')
    st.write(fig)


'''def word_cloud(search_for):
    query = "SELECT id_str, text, created_at, polarity, user_location FROM {}".format(search_for)
    df = pd.read_sql(query, con=db_connection)
    all_tweets = ' '.join(tweet for tweet in df['text'])
    words = WordCloud(stopwords=STOPWORDS).generate(all_tweets)
    plt.figure(figsize = (20, 20))
    plt.imshow(words, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)
'''

def word_cloud(search_for):
    query = "SELECT id_str, text, created_at, polarity, user_location FROM {}".format(search_for)
    df = pd.read_sql(query, con=db_connection)
    content = ' '.join(df["text"])
    content = re.sub(r"http\S+", "", content)
    content = content.replace('RT ', ' ').replace('&amp;', 'and').replace('amp', '')
    content = re.sub('[^A-Za-z0-9]+', ' ', content)
    content = content.lower()
    '''
    tokenized_word = word_tokenize(content)
    stop_words=set(stopwords.words("english"))
    filtered_sent=[]
    for w in tokenized_word:
        if w not in stop_words:
            filtered_sent.append(w)
    '''
    #all_tweets = ' '.join(tweet for tweet in df['text'])
    new_stopwords = [search_for] + list(STOPWORDS)
    words = WordCloud(stopwords=new_stopwords).generate(content)
    plt.figure(figsize = (30, 20))
    plt.imshow(words, interpolation='bilinear')
    plt.axis("off")
    st.title('WordCloud')
    st.pyplot(plt)

'''
def line_chart(search_for):
    fig = go.Figure()
    query = "SELECT id_str, text, created_at, polarity, user_location FROM {} order by created_at desc limit 1000".format(search_for)
    df = pd.read_sql(query, con=db_connection)
    result = df.groupby([pd.Grouper(key='created_at', freq='2s'), 'polarity']).count().unstack(fill_value=0).stack().reset_index()
    result = result.rename(columns={"id_str": "Num of '{}' mentions".format(search_for[0]), "created_at":"Time in UTC"})  
    time_series = result["Time in UTC"][result['polarity']==0].reset_index(drop=True)
    fig.add_trace(go.Scatter(
        x=time_series,
        y=result["Num of '{}' mentions".format(search_for[0])][result['polarity']==0].reset_index(drop=True),
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(131, 90, 241)'),
        stackgroup='one')) # define stack group  
    fig.add_trace(go.Scatter(
        x=time_series,
        y=result["Num of '{}' mentions".format(search_for[0])][result['polarity']==-1].reset_index(drop=True),
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        stackgroup='one'))
    fig.add_trace(go.Scatter(
        x=time_series,
        y=result["Num of '{}' mentions".format(search_for[0])][result['polarity']==1].reset_index(drop=True),
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(184, 247, 212)'),
        stackgroup='one'))
    st.write(fig)
'''