import re
import pandas as pd

from helper import analyze_sentiment


def preprocess(data):
    line1 = data.splitlines()[0]

    def time_format(line1):
        # First, check if there's a comma to split on
        if ',' in line1:
            # Extract the time part from the string
            time_part = line1.split(",")[1].strip().split(" ")[0]

            # Check for the presence of "am" or "pm" (with or without a preceding space)
            if "am" in line1.lower() or "pm" in line1.lower():
                return 0  # 12 hr format
            else:
                return 1  # 24 hr format
        else:
            # If there's no comma, handle the case appropriately
            return None  # or any default value or raise an exception

    if(time_format(line1) == 1):
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    else:
        pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s?\u202f?[apm]{2}\s-\s' #expression of data
    messages = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)
    date = [date.replace('\u202f', ' ') for date in date]

    if(time_format(line1) == 1):
        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)
    else:
        from datetime import datetime
        # Convert to 24-hour format
        dates = []
        for timestamp in date:
            # Remove the trailing '- ' part for conversion
            date_str = timestamp.rstrip(' - ')

            # Convert to datetime object
            date_obj = datetime.strptime(date_str, '%d/%m/%y, %I:%M %p')

            # Convert back to string in 24-hour format
            converted_timestamp = date_obj.strftime('%d/%m/%y, %H:%M - ')

            # Add to the list of dates
            dates.append(converted_timestamp)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime using 24-hour format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')

    # Rename the column from 'message_date' to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    df['polarity'], df['subjectivity'] = zip(*df['message'].apply(analyze_sentiment))

    return df