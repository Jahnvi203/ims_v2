import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
from csv import reader, writer
from pandas import ExcelWriter, read_csv
from copy import deepcopy
import altair as alt
from datetime import datetime as dt
import mysql.connector
import streamlit_authenticator as stauth
import pymongo

st.title("Hello")

def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

@st.experimental_memo(ttl=600)
def get_data():
    db = client.ims
    items = db.mycollection.find()
    items = list(items)
    return items

items = get_data()

for item in items:
    st.write(f"{item['name']}'s email is {item['email']}")