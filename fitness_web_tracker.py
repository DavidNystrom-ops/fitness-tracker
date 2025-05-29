
import streamlit as st
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

FILENAME = "workout_log.csv"
FOOD_LOG = "food_log.csv"
GOALS_FILE = "goals.csv"

st.set_page_config(page_title="Fitness Tracker", layout="centered")
tab1, tab2 = st.tabs(["🏋️ Workout Tracker", "🍽️ Food & Nutrition"])

# Load persistent goals
def load_goals():
    if os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    return int(row[0]), float(row[1])
                except:
                    return 2000, 150.0
    return 2000, 150.0

# Save updated goals
def save_goals(calories, protein):
    with open(GOALS_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([calories, protein])

# Workout Tracker Tab
with tab1:
    st.header("🏋️ Log Workout")

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

    st.subheader("📋 Workout History")
    try:
        df = pd.read_csv(FILENAME, header=None)
        df.columns = ["Date", "Exercise", "Sets", "Reps", "Weight"]
        st.dataframe(df)
    except FileNotFoundError:
        st.info("No workout data found yet.")

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

# Food Tracker Tab
with tab2:
    st.header("🍽️ Log Your Meals")

    meal_categories = ["Breakfast", "Lunch", "Dinner", "Snack", "Other"]

    with st.form("food_form"):
        meal = st.text_input("Meal description")
        category = st.selectbox("Category", meal_categories)
        calories = st.number_input("Calories", min_value=0)
        protein = st.number_input("Protein (g)", min_value=0.0, step=0.1)
        submit_food = st.form_submit_button("Log Meal")

        if submit_food:
            with open(FOOD_LOG, mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), meal, category, calories, protein])
            st.success("Meal logged!")

    st.subheader("📋 Meal History")
    try:
        food_df = pd.read_csv(FOOD_LOG, header=None)
        food_df.columns = ["Date", "Meal", "Category", "Calories", "Protein"]

        filter_cat = st.selectbox("Filter by category (optional)", ["All"] + meal_categories)
        if filter_cat != "All":
            food_df = food_df[food_df["Category"] == filter_cat]

        st.dataframe(food_df)
    except FileNotFoundError:
        st.info("No meals logged yet.")

    st.subheader("🎯 Daily Nutrition Goals")

    default_cal, default_protein = load_goals()
    goal_calories = st.number_input("Set your daily calorie goal", min_value=0, value=default_cal)
    goal_protein = st.number_input("Set your daily protein goal (g)", min_value=0.0, value=default_protein, step=0.1)

    if st.button("💾 Save Goals"):
        save_goals(goal_calories, goal_protein)
        st.success("Goals saved!")

    today = datetime.now().date()
    try:
        food_df["Date"] = pd.to_datetime(food_df["Date"])
        today_df = food_df[food_df["Date"].dt.date == today]
        total_calories = today_df["Calories"].sum()
        total_protein = today_df["Protein"].sum()

        st.write(f"**Calories today:** {int(total_calories)} / {int(goal_calories)}")
        st.progress(min(total_calories / goal_calories, 1.0))

        st.write(f"**Protein today:** {round(total_protein, 1)}g / {round(goal_protein, 1)}g")
        st.progress(min(total_protein / goal_protein, 1.0))
    except Exception as e:
        st.warning("No meal data available for today.")
