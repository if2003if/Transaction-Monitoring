

import altair as alt
import pandas as pd
import streamlit as st
import datetime
from datetime import date, timedelta

st.set_page_config(page_title="Charts", page_icon="📈")

st.title("Chart Maker (2023 Only)")

# User Filters
PaymentStatus = st.selectbox(
    'What Payment Status Would You Like to See',
    ('All', 'Charge', 'Refund', 'Chargeback')
)

PaymentMethod = st.selectbox(
    'What Payment Method Would You Like to See',
    ['All', 'Goods and Services', 'Friends & Family']
)

PaymentApplication = st.selectbox(
    'What Payment Application Would You Like to See',
    ['All', 'Desktop', 'Tablet', 'Phone']
)

PaymentCountry = st.selectbox(
    'What Payment Country Would You Like to See',
    ('All', 'US', 'UK', 'AU')
)

# Default start and end dates for 2023
start_of_2023 = datetime.datetime(2023, 1, 1)
end_of_2023 = datetime.datetime(2023, 12, 31)

# Date Inputs restricted to 2023
StartDate = st.date_input("Start Date (Only 2023)", start_of_2023, min_value=start_of_2023, max_value=end_of_2023)
EndDate = st.date_input("End Date (Only 2023)", end_of_2023, min_value=start_of_2023, max_value=end_of_2023)

# File Upload
dfpreclean = st.file_uploader("Select Your Local Transactions CSV (default provided)")
if dfpreclean is not None:
    dfpreclean = pd.read_csv(dfpreclean)
else:
    st.stop()

# Data Cleaning and Filtering
dfpreclean.drop(['Transaction_ID', 'Auth_code'], axis=1, inplace=True)
dfpreclean2 = dfpreclean[dfpreclean['Success'] == 1]
dfpreclean2["Transaction_Notes"].fillna("N/A", inplace=True)
dfpreclean2['Day'] = pd.to_datetime(dfpreclean2['Day'])

# Filter dataset to only include 2023
dfpreclean2 = dfpreclean2[(dfpreclean2['Day'] >= start_of_2023) & (dfpreclean2['Day'] <= end_of_2023)]

df = dfpreclean2.loc[:, ['Total', 'Transaction_Type', 'Type', 'Country', 'Source', 'Day', 'Customer_Name', 'Transaction_Notes']]
df['int_created_date'] = df['Day'].dt.year * 100 + df['Day'].dt.month

# Apply User Filters
if PaymentStatus == 'Charge':
    df = df[df['Type'] == 'Charge']
elif PaymentStatus == 'Refund':
    df = df[df['Type'] == 'Refund']
elif PaymentStatus == 'Chargeback':
    df = df[df['Type'] == 'Chargeback']

if PaymentMethod == 'Goods and Services':
    df = df[df['Transaction_Type'] == 'Goods and Services']
elif PaymentMethod == 'Friends & Family':
    df = df[df['Transaction_Type'] == 'Friends & Family']

if PaymentApplication == 'Desktop':
    df = df[df['Source'] == 'Desktop']
elif PaymentApplication == 'Tablet':
    df = df[df['Source'] == 'Tablet']
elif PaymentApplication == 'Phone':
    df = df[df['Source'] == 'Phone']

if PaymentCountry == 'US':
    df = df[df['Country'] == 'US']
elif PaymentCountry == 'UK':
    df = df[df['Country'] == 'UK']
elif PaymentCountry == 'AU':
    df = df[df['Country'] == 'AU']

# Further restrict data to selected date range
df = df[(df['Day'] >= pd.to_datetime(StartDate)) & (df['Day'] <= pd.to_datetime(EndDate))]

# Charts
chart1 = alt.Chart(df).mark_bar().encode(
    alt.X("Total:Q", bin=True),
    y='count()',
).properties(
    title={
        "text": ["Count of Transactions"],
        "subtitle": [f"Payment Status: {PaymentStatus}", f"Payment Method: {PaymentMethod}",
                     f"Payment Application: {PaymentApplication}", f"Payment Country: {PaymentCountry}",
                     f"Start Date: {StartDate}", f"End Date: {EndDate}"],
    },
    width=800,
    height=500
)

chart2 = alt.Chart(df).mark_boxplot(extent='min-max').encode(
    x='int_created_date:O',
    y='Total:Q'
).properties(
    title={
        "text": ["Box & Whisker By Month"],
        "subtitle": [f"Payment Status: {PaymentStatus}", f"Payment Method: {PaymentMethod}",
                     f"Payment Application: {PaymentApplication}", f"Payment Country: {PaymentCountry}",
                     f"Start Date: {StartDate}", f"End Date: {EndDate}"],
    },
    width=800,
    height=500
)

bar3 = alt.Chart(df).mark_bar().encode(
    x=alt.X('int_created_date:O', title='Date'),
    y=alt.Y('sum(Total):Q', title='Total'),
    color=alt.Color('Type:N', title='Payment Type')
)

chart3 = bar3.properties(
    title={
        "text": ["Box Plot Mean Transaction Per Month"],
        "subtitle": [f"Payment Status: {PaymentStatus}", f"Payment Method: {PaymentMethod}",
                     f"Payment Application: {PaymentApplication}", f"Payment Country: {PaymentCountry}",
                     f"Start Date: {StartDate}", f"End Date: {EndDate}"],
    },
    width=800,
    height=500
)

bar4 = alt.Chart(df).mark_bar().encode(
    x=alt.X('int_created_date:O', title='Date'),
    y=alt.Y('count(Total):Q', title='Count'),
    color=alt.Color('Type:N', title='Payment Type')
)

chart4 = bar4.properties(
    title={
        "text": ["Box Plot Transaction Count Per Month"],
        "subtitle": [f"Payment Status: {PaymentStatus}", f"Payment Method: {PaymentMethod}",
                     f"Payment Application: {PaymentApplication}", f"Payment Country: {PaymentCountry}",
                     f"Start Date: {StartDate}", f"End Date: {EndDate}"],
    },
    width=800,
    height=500
)

# Tabs for Visualization
tab1, tab2, tab3, tab4 = st.tabs(["Histogram", "Box and Whiskers", "Box Plot Sum", "Box Plot Count"])

with tab1:
    st.altair_chart(chart1, use_container_width=True)
with tab2:
    st.altair_chart(chart2, use_container_width=True)
with tab3:
    st.altair_chart(chart3, use_container_width=True)
with tab4:
    st.altair_chart(chart4, use_container_width=True)
