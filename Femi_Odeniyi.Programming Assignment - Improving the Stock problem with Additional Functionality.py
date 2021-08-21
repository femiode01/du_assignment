import sqlite3
import json
from sqlite3.dbapi2 import Date
import pandas as pd
from sqlite3 import Error
import matplotlib.pyplot as plt
from datetime import datetime
import pygal as py
from dateutil import parser
import plotly.express as px


#create a list
data_store = ()


#Connects to the database and returns an error if there's issue connecting
try: 
        conn = sqlite3.connect('stock_objects_files.db')
        c = conn.cursor()
except Error as e:
        print("Failed to connect to db", e)

# create a connection
conn = sqlite3.connect('stock_objects_files.db')

# create a cursor
c = conn.cursor()

# c.execute("PRAGMA table_info(stocks_table)")
c.execute("select * from stocks_table")


first_item = c.fetchall()
second_item = ()

#CREATE TABLE
# c.execute(""" CREATE TABLE other_stocks (
#        [symbol] TEXT,
#        [date] DATE,
#        [open] TEXT,
#        [high] TEXT,
#        [low] TEXT,
#        [close] INTEGER
#        [volume] FLOAT
# )""") 


#locates the json file 
try:
    filename = '/Users/fll/Desktop/Assignment/AllStocks.json'
    with open(filename) as f:
        stocks_data = json.load(f)
except FileNotFoundError:
    print("The file does not exist")

#inserts new stocks data to the databae
# for v in stocks_data:
#         c.execute("insert into other_stocks values (?, ?, ?, ?, ?, ?, ?)", 
#                          (v['Symbol'], v['Date'], v['Open'], v['High'], 
#                           v['Low'], v['Close'], v['Volume'] ))


#create a list for each stock data
aig_data, googl_data, ibm_data, msft_data, rds_data, fb_data, m_data, f_data = [], [], [], [], [], [], [], []


#Create Class
class stock():
    def __init__(self, stocSymbol, stocDate, stocOpen, stocHigh, stocLow, stocClose, stocVolume):
        self.symbol = stocSymbol
        self.date = stocDate
        self.open = stocOpen
        self.high = stocHigh
        self.low = stocLow
        self.close = stocClose
        self.volume = stocVolume
        self.dateStock = []
        self.closedate = []


    def add_date(self, close, date):
        self.dateStock.append(date)
        self.closedate.append(close)

#create dictionary
stocks_dictionary = {}

#loop through json and add data
for stocker in stocks_data:
    if stocker["Symbol"] not in stocks_dictionary:
        new_Dict= stock(stocker['Symbol'], stocker['Date'], stocker['Open'],stocker['High'], stocker['Low'], stocker['Close'], stocker['Volume'] )
        
        stocks_dictionary[stocker['Symbol']] = new_Dict
        
    stocks_dictionary[stocker['Symbol']].add_date(stocker["Close"], parser.parse(stocker["Date"]))

#Plot a line chart using pygal
line_chart = py.Line()
line_chart.x_labels = map(str, range(1,50))
for k,v in stocks_dictionary.items():
    line_chart.add(v.symbol,v.closedate)
    line_chart.render_to_file('play_around.svg')


#Plot a line chart using plotly
for k,v in stocks_dictionary.items():
    fig = px.line(x= v.dateStock, y=v.closedate, title = "Stock vs Closing Amount")
    fig.show()


#commit and close the database
conn.commit()
conn.close()










