
import streamlit as st
import pandas as pd
import datetime
import altair as alt
import os

st.set_page_config(page_title="Fitness Tracker", layout="centered")
st.title("🏋️‍♂️ Fitness Tracker")

# File path
LOG_FILE = "workout_data.csv"

# Load or initialize workout data
if os.path.exists(LOG_FILE):
    workout_df = pd.read_csv(LOG_FILE, parse_dates=["Date"])
else:
    workout_df = pd.DataFrame(columns=["Date", "Exercise", "Weight", "Reps", "Sets", "Volume"])

# UI tabs
tab1, tab2, tab3 = st.tabs(["Nutrition", "Workout Tracker", "Progress"])

# Nutrition tab (simplified placeholder)
with tab1:
    st.subheader("Nutrition tracking coming soon...")

# Workout logging tab
with tab2:
    st.header("Log Workout")
    exercise = st.selectbox("Exercise", [
        "Chest Press", "Overhead Shoulder Press", "Triceps Pushdown", "Incline Chest Fly", "Shoulder Lateral Raise",
        "Goblet Squat", "Romanian Deadlift", "Step-ups or Split Squats", "Glute Kickback", "Calf Raises",
        "Lat Pulldown", "Seated Row", "Bicep Curl", "Rear Delt Fly", "Face Pulls",
        "Deadlift", "Squat to Overhead Press", "Bent Over Row", "Core: Plank Hold", "Core: Cable Woodchoppers"
    ])
    weight = st.number_input("Weight (lbs)", min_value=0.0, step=0.5)
    reps = st.number_input("Reps", min_value=1)
    sets = st.number_input("Sets", min_value=1)

    if st.button("Log Workout"):
        volume = weight * reps * sets
        new_entry = pd.DataFrame([{
            "Date": datetime.date.today(),
            "Exercise": exercise,
            "Weight": weight,
            "Reps": reps,
            "Sets": sets,
            "Volume": volume
        }])
        workout_df = pd.concat([workout_df, new_entry], ignore_index=True)
        workout_df.to_csv(LOG_FILE, index=False)
        st.success(f"Logged {sets} sets of {reps} reps at {weight} lbs for {exercise}")

    st.subheader("Workout History")
    st.dataframe(workout_df.tail(10))

# Progress tab
with tab3:
    st.header("📈 Progress Tracker")
    if not workout_df.empty:
        selected = st.selectbox("Select Exercise", sorted(workout_df["Exercise"].unique()))
        filtered = workout_df[workout_df["Exercise"] == selected]

        # Daily chart
        st.subheader("Volume Over Time")
        chart = alt.Chart(filtered).mark_line(point=True).encode(
            x="Date:T",
            y="Volume:Q"
        ).properties(title=f"{selected} Volume Progress")
        st.altair_chart(chart, use_container_width=True)

        # Weekly summary
        st.subheader("Weekly Volume Summary")
        workout_df["Week"] = workout_df["Date"].dt.to_period("W").astype(str)
        weekly = workout_df.groupby(["Week", "Exercise"])["Volume"].sum().reset_index()
        weekly_filtered = weekly[weekly["Exercise"] == selected]
        st.bar_chart(data=weekly_filtered, x="Week", y="Volume")

        # CSV export
        st.subheader("📤 Export Workout Log")
        csv = workout_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="workout_data.csv",
            mime="text/csv"
        )
    else:
        st.info("No workout data yet. Log workouts to see progress!")
