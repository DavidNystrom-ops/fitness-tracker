
import streamlit as st
import pandas as pd
import datetime

# File to store food log
FOOD_LOG_FILE = "meal_log.csv"
WORKOUT_LOG_FILE = "workout_log.csv"

# --- Utility functions ---
def load_food_log():
    try:
        return pd.read_csv(FOOD_LOG_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Meal", "Category", "Calories", "Protein", "Carbs", "Fat"])

def save_food_log(df):
    df.to_csv(FOOD_LOG_FILE, index=False)

def suggest_meal(meal_type):
    suggestions = {
        "Breakfast": ["Oatmeal with banana", "Scrambled eggs", "Greek yogurt with honey"],
        "Lunch": ["Grilled chicken salad", "Turkey sandwich", "Rice and beans"],
        "Dinner": ["Salmon with veggies", "Steak and potatoes", "Pasta with marinara"],
        "Snack": ["Protein bar", "Almonds", "Apple slices with peanut butter"]
    }
    return suggestions.get(meal_type, [])

def suggest_workout():
    return [
        "Push-ups + Pull-ups",
        "Leg day: Squats & Lunges",
        "Cardio: 20 min run",
        "HIIT session: 15 minutes",
        "Core: Planks, Crunches"
    ]

# --- Streamlit App ---
st.set_page_config(page_title="Fitness Tracker", layout="centered")
st.title("🏋️‍♂️ Fitness Tracker")

tab1, tab2 = st.tabs(["Workout Tracker", "🍔 Food & Nutrition"])

# --- Workout Tracker ---
with tab1:
    st.header("Log Your Workouts")
    exercise = st.text_input("Exercise:")
    sets = st.number_input("Sets:", min_value=0, step=1)
    reps = st.number_input("Reps:", min_value=0, step=1)
    weight = st.number_input("Weight (lbs):", min_value=0.0, step=0.5)

    if st.button("Log Workout"):
        new_workout = {
            "Date": datetime.date.today(),
            "Exercise": exercise,
            "Sets": sets,
            "Reps": reps,
            "Weight": weight
        }
        try:
            df = pd.read_csv(WORKOUT_LOG_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=new_workout.keys())
        df = pd.concat([df, pd.DataFrame([new_workout])], ignore_index=True)
        df.to_csv(WORKOUT_LOG_FILE, index=False)
        st.success("Workout logged!")

    if st.button("View Workout Log"):
        try:
            df = pd.read_csv(WORKOUT_LOG_FILE)
            st.dataframe(df)
        except FileNotFoundError:
            st.info("No workouts logged yet.")

    if st.button("Auto-Suggest Workout"):
        st.write("💡 Try this workout:")
        st.code(suggest_workout()[datetime.datetime.now().day % 5])

# --- Food & Nutrition ---
with tab2:
    st.header("🍽️ Log Your Meals")
    meal = st.text_input("Meal description")
    category = st.selectbox("Category", ["Breakfast", "Lunch", "Dinner", "Snack"])
    calories = st.number_input("Calories", min_value=0)
    protein = st.number_input("Protein (g)", min_value=0.0)
    carbs = st.number_input("Carbs (g)", min_value=0.0)
    fat = st.number_input("Fat (g)", min_value=0.0)

    if st.button("Log Meal"):
        new_entry = {
            "Date": datetime.date.today(),
            "Meal": meal,
            "Category": category,
            "Calories": calories,
            "Protein": protein,
            "Carbs": carbs,
            "Fat": fat
        }
        food_df = load_food_log()
        food_df = pd.concat([food_df, pd.DataFrame([new_entry])], ignore_index=True)
        save_food_log(food_df)
        st.success("Meal logged!")

    st.subheader("📋 Meal History")
    food_df = load_food_log()
    st.dataframe(food_df)

    st.subheader("🥅 Daily Nutrition Goals")
    calorie_goal = st.number_input("Set your daily calorie goal", value=2000)
    protein_goal = st.number_input("Set your daily protein goal (g)", value=150)
    carb_goal = st.number_input("Set your daily carb goal (g)", value=250)
    fat_goal = st.number_input("Set your daily fat goal (g)", value=70)

    today_log = food_df[food_df["Date"] == str(datetime.date.today())]
    if not today_log.empty:
        cal = today_log["Calories"].sum()
        pro = today_log["Protein"].sum()
        carbs_total = today_log["Carbs"].sum()
        fat_total = today_log["Fat"].sum()
        st.metric("Calories", f"{cal} / {calorie_goal}")
        st.metric("Protein (g)", f"{pro} / {protein_goal}")
        st.metric("Carbs (g)", f"{carbs_total} / {carb_goal}")
        st.metric("Fat (g)", f"{fat_total} / {fat_goal}")
    else:
        st.info("No meal data available for today.")
