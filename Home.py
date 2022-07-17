import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
from csv import reader, writer
from pandas import ExcelWriter, read_csv
from copy import deepcopy
import altair as alt
from datetime import datetime as dt
from supabase import create_client, Client

# Connecting to Supabase database
@st.experimental_singleton
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

supabase = init_connection()

@st.experimental_memo(ttl=600)
def run_query():
    return supabase.table("users").select("*").execute()

rows = run_query()

for row in rows.data:
    st.write(f"{row['name']}'s email is {row['email']}")