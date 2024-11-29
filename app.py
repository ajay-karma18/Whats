import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import helper
import preprocessor

st.sidebar.markdown('<h1 class="sidebar-title">Text Explorer Pro</h1>', unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp export .txt file", type=["txt"])  # Restrict file types to .txt

if uploaded_file is not None:
    if uploaded_file.name.endswith('.txt'):  # Additional check for .txt extension
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")   # convert into string

        if helper.is_valid_whatsapp_file(data): #check for validation of whatsapp file
            st.success("Valid WhatsApp file uploaded.")

            df = preprocessor.preprocess(data) # pass the data to preprocess function and return df

            st.dataframe(df)

            # fetch unique users
            user_list = df['user'].unique().tolist()
            user_list.remove('group_notification')
            user_list.sort()
            user_list.insert(0,"Overall")

            selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

            if st.sidebar.button("Show Analysis"):
                # Stats Area
                num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

                #The unsafe_allow_html=True parameter in Streamlit’s st.markdown() function allows you to include and render raw HTML
                # within your Streamlit app.
                st.markdown("""
                <h1 style="font-size: 2.5rem; font-weight: bold; color: #4CAF50; text-align: center;"> Top Statistics </h1>
                """, unsafe_allow_html=True)

                # Create a layout with columns
                col1, col2, col3, col4 = st.columns(4)

                # Display statistics using st.metric
                with col1:
                    st.metric(label="Total Messages", value=num_messages, delta=None, help="Total number of messages sent")

                with col2:
                    st.metric(label="Total Words", value=words, delta=None, help="Total number of words used in the messages")

                with col3:
                    st.metric(label="Media Shared", value=num_media_messages, delta=None, help="Total number of media files shared")

                with col4:
                    st.metric(label="Links Shared", value=num_links, delta=None, help="Total number of links shared")


                # monthly timeline
                st.markdown("""
                        <h1 style="font-size: 2.5rem; font-weight: bold; color: #4CAF50; text-align: center;"> Monthly Timeline </h1>
                        """, unsafe_allow_html=True)
                timeline = helper.monthly_timeline(selected_user,df)
                fig,ax = plt.subplots()
                ax.plot(timeline['time'], timeline['message'],color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                # daily timeline
                st.markdown("""
                        <h1 style="font-size: 2.5rem; font-weight: bold; color: #4CAF50; text-align: center;"> Daily Timeline </h1>
                        """, unsafe_allow_html=True)
                daily_timeline = helper.daily_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                # activity map
                st.markdown("""
                        <h1 style="font-size: 2.5rem; font-weight: bold; color: #4CAF50; text-align: center;"> Activity Map </h1>
                        """, unsafe_allow_html=True)
                col1,col2 = st.columns(2)

                with col1:
                    st.markdown("""
                            <h2 style="font-size: 2.5rem; color: #1d4ed8; text-align: center;"> Most busy day </h2>
                            """, unsafe_allow_html=True)
                    busy_day = helper.week_activity_map(selected_user,df)
                    fig,ax = plt.subplots()
                    ax.bar(busy_day.index,busy_day.values,color='purple')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2:
                    st.markdown("""
                            <h2 style="font-size: 2.5rem; color: #1d4ed8; text-align: center;"> Most busy month </h2>
                            """, unsafe_allow_html=True)
                    busy_month = helper.month_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_month.index, busy_month.values,color='orange')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)


                st.markdown("""
                        <h1 style="font-size: 2.5rem; font-weight: bold; color: #4CAF50; text-align: center;"> Weekly Activity Map </h1>
                        """, unsafe_allow_html=True)
                user_heatmap = helper.activity_heatmap(selected_user,df)
                fig,ax = plt.subplots()
                ax = sns.heatmap(user_heatmap)
                st.pyplot(fig)

                # finding the busiest users in the group(Group level)
                if selected_user == 'Overall':
                    st.markdown("""
                                   <h1 style="font-size: 2.5rem; color: #4CAF50; text-align: center;"> Most busy users </h1>
                                   """, unsafe_allow_html=True)
                    x,new_df = helper.most_busy_users(df)
                    fig, ax = plt.subplots()

                    col1, col2 = st.columns(2)

                    with col1:
                        ax.bar(x.index, x.values,color='red')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    with col2:
                        st.dataframe(new_df)

                # WordCloud
                st.markdown("""
                               <h1 style="font-size: 2.5rem; font-weight: bold; color: #4CAF50; text-align: center;"> Word cloud </h1>
                               """, unsafe_allow_html=True)
                df_wc = helper.create_wordcloud(selected_user,df)
                fig,ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)

                # most common words
                most_common_df = helper.most_common_words(selected_user,df)

                fig,ax = plt.subplots()

                ax.barh(most_common_df[0],most_common_df[1])
                plt.xticks(rotation='vertical')

                st.markdown("""
                                      <h1 style="font-size: 2.5rem; font-weight: bold; color: #4CAF50; text-align: center;"> Most Common Words </h1>
                                      """, unsafe_allow_html=True)
                st.pyplot(fig)

                # emoji analysis
                emoji_df = helper.emoji_helper(selected_user,df)
                st.markdown("""
                <h1 style="font-size: 2.5rem; font-weight: bold; color: #4CAF50; text-align: center;"> Emoji Analysis </h1>
                """, unsafe_allow_html=True)

                col1,col2 = st.columns(2)

                with col1:
                    st.dataframe(emoji_df)
                with col2:
                    fig,ax = plt.subplots()
                    ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                    st.pyplot(fig)

                # Sentiment Analysis
                st.markdown("""
                <h1 style="font-size: 2.5rem; font-weight: bold; color: #4CAF50; text-align: center;"> Sentiment Analysis </h1>
                """, unsafe_allow_html=True)

                # Show average polarity and subjectivity
                avg_polarity = df['polarity'].mean()
                avg_subjectivity = df['subjectivity'].mean()

                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Average Polarity", value=round(avg_polarity, 2), delta=None,
                              help="Range from -1 (negative) to 1 (positive)")
                with col2:
                    st.metric(label="Average Subjectivity", value=round(avg_subjectivity, 2), delta=None,
                              help="Range from 0 (objective) to 1 (subjective)")


        else:
            st.error("The uploaded file is not a valid WhatsApp export file. Please upload the correct file.") #added

    else:
        st.error("Please upload a .txt file.")
