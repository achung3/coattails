import streamlit as st
import pandas as pd
import altair as alt
import yfinance as yf
import datetime as dt

house = pd.read_csv('all_transactions_house.csv')
senate = pd.read_csv('all_transactions_senate.csv')

house = house.dropna()
senate = senate.dropna()
#Remove "Hon. or Mr./Mrs. from front of rep names"
house['representative'] = house['representative'].str.split(n=1).str[1]

#Remove observations with no ticker
senate = senate[senate.ticker != '--']
#st.title("Coattails")

#st.subheader("Find out where to invest!")

#Select either senate or house

def tickerToString(tickerList):
    tickerString = ""
    for item in tickerList:
        tickerString = tickerString + item + " "
    tickerString = tickerString.strip()
    return tickerString

body = st.sidebar.radio('Select a political body',('Senate','House of Representatives'))
if body == 'Senate':
    politician = st.sidebar.selectbox('Select a senator', senate.senator.unique())
    displaySenate = senate[senate.senator == politician]
    shortDisplaySenate = displaySenate[['transaction_date','ticker','type','amount']].head(5)
    tickerList = shortDisplaySenate.ticker.unique()
    start = shortDisplaySenate.iat[-1,0]
    date_str = start
    format_str = '%m/%d/%Y'
    startDate = dt.datetime.strptime(date_str, format_str)
    startDate = startDate.date()
    end = dt.date.today()
    stockDF = yf.download(tickerToString(tickerList), start = startDate, end = end)
    st.line_chart(stockDF.Close)
    st.dataframe(shortDisplaySenate)
else:
    politician = st.sidebar.selectbox('Select a representative', house.representative.unique())
    displayHouse = house[house.representative == politician]
    shortDisplayHouse = displayHouse[['transaction_date','ticker','type','amount']].head(5)
    tickerList = shortDisplayHouse.ticker.unique()
    start = shortDisplayHouse.iat[-1,0]
    date_str = start
    format_str = '%Y-%m-%d'
    startDate = dt.datetime.strptime(date_str, format_str)
    startDate = startDate.date()
    end = dt.date.today()
    stockDF = yf.download(tickerToString(tickerList), start = startDate, end = end)
    st.line_chart(stockDF.Close)
    st.dataframe(shortDisplayHouse)


