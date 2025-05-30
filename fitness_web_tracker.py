import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Fitness Tracker", layout="centered")

# Load or initialize workout log
def load_workout_log():
    if os.path.exists("workout_log.csv"):
        return pd.read_csv("workout_log.csv")
    else:
        return pd.DataFrame(columns=["Date", "Exercise", "Sets", "Reps", "Weight"])

# Load or initialize food log
def load_food_log():
    if os.path.exists("food_log.csv"):
        return pd.read_csv("food_log.csv")
    else:
        return pd.DataFrame(columns=["Date", "Meal", "Category", "Calories", "Protein"])

# Save workout log
def save_workout_log(df):
    df.to_csv("workout_log.csv", index=False)

# Save food log
def save_food_log(df):
    df.to_csv("food_log.csv", index=False)

# Get or initialize daily goals
def get_goals():
    if os.path.exists("goals.txt"):
        with open("goals.txt", "r") as f:
            cal, protein = f.read().split(",")
            return int(cal), float(protein)
    return 2000, 150.0

def save_goals(cal, protein):
    with open("goals.txt", "w") as f:
        f.write(f"{cal},{protein}")

# Preloaded exercises
preloaded_exercises = {
    "Chest": ["Chest Press", "Incline Chest Fly", "Overhead Shoulder Press", "Triceps Pushdown", "Shoulder Lateral Raise"],
    "Legs": ["Goblet Squat", "Romanian Deadlift", "Step-ups or Split Squats", "Glute Kickback", "Calf Raises"],
    "Back/Arms": ["Lat Pulldown", "Seated Row", "Bicep Curl", "Rear Delt Fly", "Face Pulls"],
    "Full Body/Core": ["Deadlift", "Squat to Overhead Press", "Bent Over Row", "Core: Plank Hold", "Core: Cable Woodchoppers"]
}

# Tabs for Workout and Food/Nutrition
tab1, tab2 = st.tabs(["🏋️‍♂️ Workout Tracker", "🍽️ Food & Nutrition"])

with tab1:
    st.header("Log Your Workout")
    exercise = st.text_input("Exercise")
    col1, col2, col3 = st.columns(3)
    sets = col1.number_input("Sets", 0, 20, step=1)
    reps = col2.number_input("Reps", 0, 50, step=1)
    weight = col3.number_input("Weight (lbs)", 0, 1000, step=5)

    if st.button("Log Workout"):
        new_entry = {"Date": datetime.now().strftime("%Y-%m-%d"), "Exercise": exercise, "Sets": sets, "Reps": reps, "Weight": weight}
        workout_df = load_workout_log()
        workout_df = pd.concat([workout_df, pd.DataFrame([new_entry])], ignore_index=True)
        save_workout_log(workout_df)
        st.success("Workout logged successfully!")

    st.subheader("Preloaded Exercises")
    for category, exercises in preloaded_exercises.items():
        with st.expander(category):
            for ex in exercises:
                if st.button(ex, key=ex):
                    st.experimental_set_query_params(ex=ex)
                    st.rerun()

    st.subheader("Workout History")
    st.dataframe(load_workout_log())

with tab2:
    st.header("Log Your Meals")
    meal = st.text_input("Meal description", key="meal_input")
    category = st.selectbox("Category", ["Breakfast", "Lunch", "Dinner", "Snack"], key="cat_input")
    calories = st.number_input("Calories", 0, 2000, key="cal_input")
    protein = st.number_input("Protein (g)", 0.0, 200.0, step=0.5, key="prot_input")

    if st.button("Log Meal"):
        food_df = load_food_log()
        new_meal = {"Date": datetime.now().strftime("%Y-%m-%d"), "Meal": meal, "Category": category, "Calories": calories, "Protein": protein}
        food_df = pd.concat([food_df, pd.DataFrame([new_meal])], ignore_index=True)
        save_food_log(food_df)
        st.success("Meal logged successfully!")

        # Clear inputs
        st.rerun()

    st.subheader("📋 Meal History")
    food_df = load_food_log()
    st.dataframe(food_df)

    st.subheader("🎯 Daily Nutrition Goals")
    cal_goal, protein_goal = get_goals()
    new_cal_goal = st.number_input("Set your daily calorie goal", 0, 5000, value=cal_goal)
    new_protein_goal = st.number_input("Set your daily protein goal (g)", 0.0, 300.0, value=protein_goal)

    if st.button("Save Nutrition Goals"):
        save_goals(new_cal_goal, new_protein_goal)
        st.success("Nutrition goals saved successfully!")

    today = datetime.now().strftime("%Y-%m-%d")
    today_food = food_df[food_df["Date"] == today]
    total_cals = today_food["Calories"].sum()
    total_protein = today_food["Protein"].sum()

    st.markdown(f"**Calories consumed today:** {total_cals} / {new_cal_goal}")
    st.markdown(f"**Protein consumed today:** {total_protein}g / {new_protein_goal}g")

    fig, ax = plt.subplots()
    ax.bar(["Calories", "Protein"], [total_cals, total_protein], color=["orange", "blue"])
    ax.axhline(y=new_cal_goal, color="orange", linestyle="--", label="Calorie Goal")
    ax.axhline(y=new_protein_goal, color="blue", linestyle="--", label="Protein Goal")
    ax.legend()
    ax.set_ylabel("Amount")
    ax.set_title("Today's Nutrition Progress")
    st.pyplot(fig)
