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

st.title("Hello")

def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

names = ['Jahnvi Raj Singh', 'Ben Low']
emails = ['jahnvi.singh@rttechlaw.com', 'ben.low@rttechlaw.com']
passwords = ['123', '456']
hashed_passwords = stauth.hasher(passwords).generate()

authenticator = stauth.authenticate(names, emails, hashed_passwords, 'Jahnvi203', '83582042', cookie_expiry_days = 30)

name, authentication_status = authenticator.login('Login', 'sidebar')

if authentication_status:
    st.write('Welcome *%s*' % (name))
 # your application
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

# users_rows = run_query("select * from users")
# for row in users_rows:
#     st.write(f"{row[0]}'s email is {row[1]}")