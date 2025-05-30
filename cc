cimport streamlit as st
import datetime

def workout_tab():
    # Initialize session state
    if "workout_data" not in st.session_state:
        st.session_state.workout_data = []

    # Workout Logging Section
    st.header("Log Workout")
    exercise = st.selectbox("Exercise", [
        "Chest Press", "Overhead Shoulder Press", "Triceps Pushdown", "Incline Chest Fly", "Shoulder Lateral Raise",
        "Goblet Squat", "Romanian Deadlift", "Step-ups or Split Squats", "Glute Kickback", "Calf Raises",
        "Lat Pulldown", "Seated Row", "Bicep Curl", "Rear Delt Fly", "Face Pulls",
        "Deadlift", "Squat to Overhead Press", "Bent Over Row",
        "Core: Plank Hold", "Core: Cable Woodchoppers"
    ])

    weight = st.number_input("Weight (lbs)", min_value=0.0, step=0.5)
    reps = st.number_input("Reps", min_value=1, step=1)
    sets = st.number_input("Sets", min_value=1, step=1)

    if st.button("Log Workout"):
        volume = weight * reps * sets
        st.session_state.workout_data.append({
            "Date": datetime.date.today(),
            "Exercise": exercise,
            "Weight": weight,
            "Reps": reps,
            "Sets": sets,
            "Volume": volume
        })
        st.success(f"Logged {sets} sets of {reps} reps at {weight} lbs for {exercise}")
