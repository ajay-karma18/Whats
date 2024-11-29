from textblob import TextBlob
from urlextract import URLExtract
import pandas as pd
from collections import Counter

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user] #select the no. of messages by individual user

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

# wordcloud
from wordcloud import WordCloud, STOPWORDS , ImageColorGenerator
import matplotlib.pylab as plt
def create_wordcloud(selected_user, df):
    # Load stop words
    stopwords = set(STOPWORDS)
    # Filter the DataFrame based on selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove group notifications and media messages
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]

    # generate word cloud
    wc= WordCloud(stopwords=stopwords, width=1600, height=800, background_color="Black",
                          colormap="Set2").generate(''.join(temp['message']))

    # Display the WordCloud
    plt.figure(figsize=(20, 10), facecolor='k')
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

    return wc

# most common words

def most_common_words(selected_user,df):

    f = open('stop_words.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']         #remove user name called group_notification
    temp = temp[temp['message'] != '<Media omitted>\n']   #remove all messages named <Media omitted>\n

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# emoji's operation
import emoji
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

# monthly timeline

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

# daily timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


#  weekly timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

# activity heatmap

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


# check validation of whatsapp file or not

def is_valid_whatsapp_file(file_content):
    # Split the content into lines
    lines = file_content.splitlines()

    # Check the first few lines for WhatsApp-like patterns
    # Typically, WhatsApp messages start with a timestamp
    # e.g., "12/31/21, 9:12 PM - John Doe: Message text"
    if len(lines) > 0:
        first_line = lines[0]
        # Example format for WhatsApp exported files
        # It starts with a date, followed by a comma, time, and a hyphen
        if (first_line[:2].isdigit() and
            first_line[2] == '/' and
            first_line[5] == '/' and
            '-' in first_line and
            ':' in first_line):
            return True
    return False

def analyze_sentiment(message):
    """Analyze sentiment of a message and return polarity and subjectivity."""
    analysis = TextBlob(message)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity









