from turtle import onclick
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
import streamlit_authenticator as stauth
from time import sleep

@st.experimental_singleton
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

supabase = init_connection()

@st.experimental_memo(ttl=600)
def get_assignments():
    return supabase.table("assignments").select("*").execute()

existing_assignments_rows = get_assignments()

existing_assignments = []

for row in existing_assignments_rows.data:
    existing_assignments.append([row['device_no'], row['device_type'], row['assigned_to'], row['assigned_from'], row['assigned_till'], row['assigned_current'], row['assigned_by']])

def get_existing_users():
    return supabase.table("users").select("*").execute()

existing_users_rows = get_existing_users()

existing_users_names = []
existing_users_emails = []
existing_users_passwords = []
existing_users_types = []

for row in existing_users_rows.data:
    existing_users_names.append(row['name'])
    existing_users_emails.append(row['email'])
    existing_users_passwords.append(row['password'])
    existing_users_types.append(row['user_type'])

def insert_new_user(name, email, password):
    return supabase.table("users").insert({'name': name, 'email': email, 'password': password, 'user_type': 'user'}).execute()

st.title("Welcome to R&TT's Inventory Management System")

# Login page
login_heading = st.empty()
login_heading_show = login_heading.subheader("Login")
login_email = st.empty()
login_email_show = login_email.text_input("Email")
login_password = st.empty()
login_password_show = login_password.text_input("Password", type = "password")
login_button = st.empty()
login_button_show = login_button.button("Login")

def viewYourCurrentAssg(name, email):
    myAssg_heading = st.empty()
    myAssg_heading_show = myAssg_heading.subheader("My Current Assignments")
    your_current_assg = []
    for row in existing_assignments:
        if row[2] == name and row[5]:
            your_current_assg.append([row[0], row[1], row[3], row[6]])
    your_current_assg_df = pd.DataFrame(your_current_assg, columns = ["Device No.", "Device Type", "Assigned From", "Assigned By"])
    your_current_assg_df_show = st.dataframe(your_current_assg_df)
    return

def viewAssg(name, email):
    searchAssg_heading = st.empty()
    searchAssg_heading_show = searchAssg_heading.subheader("View All Assignments")
    existing_assignments_df = st.empty()
    existing_assignments_df_actual = pd.DataFrame(existing_assignments, columns = ["Device No.", "Device Type", "Assigned To", "Assigned From", "Assigned Till", "Current Assignment", "Assigned By"])
    existing_assignments_df_show = existing_assignments_df.dataframe(existing_assignments_df_actual)
    return

if login_button_show:
    not_filled = st.empty()
    if login_email_show == "" or login_password_show == "":
        not_filled_show = not_filled.markdown("Please enter your Email and Password.")
    else:
        not_signedup = st.empty()
        if login_email_show not in existing_users_emails:
            not_signedup_show = not_signedup.markdown("You have not signed up yet. Please contact your Administrator for help.")
        else:
            not_signedup.empty()
            login_email_index = existing_users_emails.index(login_email_show)
            correct_password = existing_users_passwords[login_email_index]
            wrong_password = st.empty()
            if login_password_show != correct_password:
                wrong_password_show = wrong_password.markdown("You have entered the wrong Password. Please enter the correct Password or contact your Administrator for help.")
            else:
                wrong_password.empty()
                login_heading.empty()
                login_email.empty()
                login_password.empty()
                login_button.empty()
                user_type = existing_users_types[login_email_index]
                name = existing_users_names[login_email_index]
                if user_type == "admin":
                    viewYourCurrentAssg(name, login_email_show)
                    viewAssg(name, login_email_show)
                elif user_type == "user":
                    viewYourCurrentAssg(name, login_email_show)