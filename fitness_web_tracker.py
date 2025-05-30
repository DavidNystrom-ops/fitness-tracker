
import streamlit as st
import pandas as pd
import datetime
import altair as alt

st.set_page_config(page_title="Fitness Tracker", layout="centered")
st.title("🏋️‍♂️ Fitness Tracker")

# Initialize session states
if "goals" not in st.session_state:
    st.session_state.goals = {"Calories": 0, "Protein": 0, "Carbs": 0, "Fat": 0}
if "meals" not in st.session_state:
    st.session_state.meals = []
if "workout_data" not in st.session_state:
    st.session_state.workout_data = []

# Tabs
tab1, tab2, tab3 = st.tabs(["Nutrition", "Workout Tracker", "Progress Charts"])

# NUTRITION TAB
with tab1:
    st.header("Set Daily Nutritional Goals")
    cal = st.number_input("Calories", value=st.session_state.goals["Calories"])
    protein = st.number_input("Protein (g)", value=st.session_state.goals["Protein"])
    carbs = st.number_input("Carbs (g)", value=st.session_state.goals["Carbs"])
    fat = st.number_input("Fat (g)", value=st.session_state.goals["Fat"])
    if st.button("Save Goals"):
        st.session_state.goals = {
            "Calories": cal,
            "Protein": protein,
            "Carbs": carbs,
            "Fat": fat,
        }
        st.success("Goals saved!")

    st.divider()
    st.header("Log Meals")
    with st.form("meal_form", clear_on_submit=True):
        meal = st.text_input("Meal Description")
        mcal = st.number_input("Calories", key="meal_calories")
        mpro = st.number_input("Protein (g)", key="meal_protein")
        mcarbs = st.number_input("Carbs (g)", key="meal_carbs")
        mfat = st.number_input("Fat (g)", key="meal_fat")
        submitted = st.form_submit_button("Log Meal")
        if submitted:
            st.session_state.meals.append(
                {"Meal": meal, "Calories": mcal, "Protein": mpro, "Carbs": mcarbs, "Fat": mfat}
            )
            st.success(f"{meal} logged!")

    st.subheader("Today's Meals")
    if st.session_state.meals:
        df_meals = pd.DataFrame(st.session_state.meals)
        st.dataframe(df_meals)
        totals = df_meals.sum(numeric_only=True)
        st.write("**Total Consumed:**")
        st.write(totals)

# WORKOUT TAB
with tab2:
    st.header("Log Workout")

    exercise = st.selectbox("Exercise", [
        "Chest Press", "Overhead Shoulder Press", "Triceps Pushdown", "Incline Chest Fly", "Shoulder Lateral Raise",
        "Goblet Squat", "Romanian Deadlift", "Step-ups or Split Squats", "Glute Kickback", "Calf Raises",
        "Lat Pulldown", "Seated Row", "Bicep Curl", "Rear Delt Fly", "Face Pulls",
        "Deadlift", "Squat to Overhead Press", "Bent Over Row", "Core: Plank Hold", "Core: Cable Woodchoppers"
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

    st.subheader("📜 Workout History")
    if st.session_state.workout_data:
        df = pd.DataFrame(st.session_state.workout_data)
        st.dataframe(df)

# PROGRESS CHART TAB
with tab3:
    st.header("📈 Volume Progress by Exercise")
    if st.session_state.workout_data:
        df = pd.DataFrame(st.session_state.workout_data)
        exercise_selected = st.selectbox("Select Exercise", sorted(df["Exercise"].unique()))
        filtered = df[df["Exercise"] == exercise_selected]

        chart = alt.Chart(filtered).mark_line(point=True).encode(
            x="Date:T",
            y="Volume:Q"
        ).properties(title=f"Volume Over Time: {exercise_selected}")
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No workout data available yet.")
