import streamlit as st
import pandas as pd
import datetime
import altair as alt
import os

import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load credentials
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']


name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Username or password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
else:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome, {name} 👋")

    st.set_page_config(page_title="Fitness Tracker", layout="centered")
    st.title("🏋️‍♂️ Fitness Tracker")

    # File paths
    WORKOUT_LOG = "workout_data.csv"
    NUTRITION_LOG = "nutrition_log.csv"
    WATER_LOG = "water_log.csv"
    SLEEP_LOG = "sleep_log.csv"

    # Load or initialize logs
    def load_csv(log_path, columns):
        if os.path.exists(log_path):
            return pd.read_csv(log_path, parse_dates=["Date"])
        else:
            return pd.DataFrame(columns=columns)

    # You can continue the rest of your app code from here...
