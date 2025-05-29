import streamlit as st
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

FILENAME = "workout_log.csv"

# --- Log Workout ---
st.title("🏋️‍♂️ Fitness Tracker")

with st.form("log_form"):
    exercise = st.text_input("Exercise")
    sets = st.number_input("Sets", min_value=1, step=1)
    reps = st.number_input("Reps", min_value=1, step=1)
    weight = st.number_input("Weight (lbs)", min_value=0.0, step=0.5)
    submitted = st.form_submit_button("Log Workout")

    if submitted:
        with open(FILENAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), exercise, sets, reps, weight])
        st.success("Workout logged!")

# --- View History ---
st.subheader("📋 Workout History")
try:
    df = pd.read_csv(FILENAME, header=None)
    df.columns = ["Date", "Exercise", "Sets", "Reps", "Weight"]
    st.dataframe(df)
except FileNotFoundError:
    st.info("No workout data found yet.")

# --- Graph Progress ---
st.subheader("📈 Graph Progress")
selected_exercise = st.text_input("Enter exercise to graph (optional)")

if st.button("Show Graph"):
    try:
        if selected_exercise:
            filtered_df = df[df["Exercise"].str.lower() == selected_exercise.lower()]
        else:
            filtered_df = df

        if not filtered_df.empty:
            filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])
            filtered_df = filtered_df.sort_values("Date")

            plt.figure(figsize=(10, 5))
            plt.plot(filtered_df["Date"], filtered_df["Weight"], marker='o')
            plt.xlabel("Date")
            plt.ylabel("Weight (lbs)")
            plt.title(f"Progress: {selected_exercise}" if selected_exercise else "All Exercises")
            plt.grid(True)
            st.pyplot(plt)
        else:
            st.warning("No data to graph for that exercise.")
    except Exception as e:
        st.error(f"Error generating graph: {e}")
