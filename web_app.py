import streamlit as st
import main
import viz

st.title("Real-time Twitter Sentiment Analysis for Brand Improvement and Topic Tracking")
st.markdown("This web application performs anaysis on tweets in real-time based on the company name \
    and present it's Polarity and other insights.")


st.header("Select a Company:")
select = st.selectbox("Please Select a Company from dropdown to Proceed", 
["--select--", 'Amazon', 'Apple', 'Disney', 'Facebook/Meta', 'Google', 'Microsoft', 'Netflix', 'Snapchat', \
    'Tesla', "Yahoo", 'Walmart'], index=0)

if select == '--select--':
    st.write("")
elif select == 'Amazon':
    main.stream('Amazon')
    viz.pie_chart('Amazon')
    viz.topic_tracking('Amazon')
    viz.line_chart('Amazon')
    viz.word_cloud('Amazon')
elif select == 'Apple':
    main.stream('Apple')
    viz.pie_chart('Apple')
    viz.topic_tracking('Apple')
    viz.line_chart('Apple')
    viz.word_cloud('Apple')
elif select == 'Disney':
    main.stream('Disney')
    viz.pie_chart('Disney')
    viz.topic_tracking('Disney')
    viz.line_chart('Disney')
    viz.word_cloud('Disney')
elif select == 'Facebook/Meta':
    main.stream('Facebook')
    viz.pie_chart('Facebook')
    viz.topic_tracking('Facebook')
    viz.line_chart('Facebook')
    viz.word_cloud('Facebook')
elif select == 'Google':
    main.stream('Google')
    viz.pie_chart('Google')
    viz.topic_tracking('Google')
    viz.line_chart('Google')
    viz.word_cloud('Google')
elif select == 'Microsoft':
    main.stream('Microsoft')
    viz.pie_chart('Microsoft')
    viz.topic_tracking('Microsoft')
    viz.line_chart('Microsoft')
    viz.word_cloud('Microsoft')
elif select == 'Netflix':
    main.stream('Netflix')
    viz.pie_chart('Netflix')
    viz.topic_tracking('Netflix')
    viz.line_chart('Netflix')
    viz.word_cloud('Netflix')
elif select == 'Snapchat':
    main.stream('Snapchat')
    viz.pie_chart('Snapchat')
    viz.topic_tracking('Snapchat')
    viz.line_chart('Snapchat')
    viz.word_cloud('Snapchat')
elif select == 'Tesla':
    main.stream('Tesla')
    viz.pie_chart('Tesla')
    viz.topic_tracking('Tesla')
    viz.line_chart('Tesla')
    viz.word_cloud('Tesla')
elif select == 'Yahoo':
    main.stream('Yahoo')
    viz.pie_chart('Yahoo')
    viz.topic_tracking('Yahoo')
    viz.line_chart('Yahoo')
    viz.word_cloud('Yahoo')
elif select == 'Walmart':
    main.stream('Walmart')
    viz.pie_chart('Walmart')
    viz.topic_tracking('Walmart')
    viz.line_chart('Walmart')
    viz.word_cloud('Walmart')