import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load config
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Auth
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login(
    form_name="Login", location="main"
)

if authentication_status is False:
    st.error("Username or password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
elif authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome, {name} 👋")
    st.title("🏋️ Fitness Tracker")


    # File paths
    WORKOUT_LOG = "workout_data.csv"
    NUTRITION_LOG = "nutrition_log.csv"
    WATER_LOG = "water_log.csv"
    SLEEP_LOG = "sleep_log.csv"

    # Example: Load one log
    workout_df = load_csv(WORKOUT_LOG, ["Date", "Exercise", "Weight", "Reps", "Sets"])
    st.write("Workout Log", workout_df)


workout_df = load_csv(WORKOUT_LOG, ["Date", "Exercise", "Weight", "Reps", "Sets", "Volume"])
nutrition_df = load_csv(NUTRITION_LOG, ["Date", "Meal", "Protein", "Carbs", "Fats", "Calories"])
water_df = load_csv(WATER_LOG, ["Date", "Ounces"])
sleep_df = load_csv(SLEEP_LOG, ["Date", "Hours"])

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Nutrition", "Workout Tracker", "Water", "Sleep", "Progress"])

# ---------- NUTRITION ----------
with tab1:
    st.header("🥗 Nutrition Log")
    with st.form("nutrition_form"):
        meal = st.text_input("Meal Description")
        protein = st.number_input("Protein (g)", min_value=0)
        carbs = st.number_input("Carbs (g)", min_value=0)
        fats = st.number_input("Fats (g)", min_value=0)
        calories = st.number_input("Calories", min_value=0)
        submitted = st.form_submit_button("Log Meal")
        if submitted:
            entry = {
                "Date": datetime.date.today(),
                "Meal": meal,
                "Protein": protein,
                "Carbs": carbs,
                "Fats": fats,
                "Calories": calories
            }
            nutrition_df = pd.concat([nutrition_df, pd.DataFrame([entry])], ignore_index=True)
            nutrition_df.to_csv(NUTRITION_LOG, index=False)
            st.success("Meal logged!")

    st.subheader("Meal History")
    st.dataframe(nutrition_df.tail(10))
    st.download_button("Download Nutrition Log", nutrition_df.to_csv(index=False), "nutrition_log.csv")

# ---------- WORKOUT ----------
with tab2:
    st.header("🏋️ Log Workout")
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
        workout_df.to_csv(WORKOUT_LOG, index=False)
        st.success(f"Logged {sets} sets of {reps} reps at {weight} lbs for {exercise}")

    st.subheader("Workout History")
    st.dataframe(workout_df.tail(10))
    st.download_button("Download Workout Log", workout_df.to_csv(index=False), "workout_data.csv")

# ---------- WATER ----------
with tab3:
    st.header("💧 Water Intake")
    ounces = st.number_input("Ounces Drank Today", min_value=0)
    if st.button("Log Water"):
        new_entry = pd.DataFrame([{
            "Date": datetime.date.today(),
            "Ounces": ounces
        }])
        water_df = pd.concat([water_df, new_entry], ignore_index=True)
        water_df.to_csv(WATER_LOG, index=False)
        st.success("Water intake logged!")

    st.subheader("Water Log")
    st.dataframe(water_df.tail(10))
    st.download_button("Download Water Log", water_df.to_csv(index=False), "water_log.csv")

# ---------- SLEEP ----------
with tab4:
    st.header("😴 Sleep Log")
    hours = st.number_input("Hours Slept", min_value=0.0, step=0.5)
    if st.button("Log Sleep"):
        new_entry = pd.DataFrame([{
            "Date": datetime.date.today(),
            "Hours": hours
        }])
        sleep_df = pd.concat([sleep_df, new_entry], ignore_index=True)
        sleep_df.to_csv(SLEEP_LOG, index=False)
        st.success("Sleep logged!")

    st.subheader("Sleep Log")
    st.dataframe(sleep_df.tail(10))
    st.download_button("Download Sleep Log", sleep_df.to_csv(index=False), "sleep_log.csv")

# ---------- PROGRESS ----------
with tab5:
    st.header("📈 Progress Tracker")
    if not workout_df.empty:
        selected = st.selectbox("Select Exercise", sorted(workout_df["Exercise"].unique()))
        filtered = workout_df[workout_df["Exercise"] == selected]

        st.subheader("Volume Over Time")
        chart = alt.Chart(filtered).mark_line(point=True).encode(
            x="Date:T",
            y="Volume:Q"
        ).properties(title=f"{selected} Volume Progress")
        st.altair_chart(chart, use_container_width=True)

        st.subheader("Weekly Volume Summary")
        workout_df["Week"] = workout_df["Date"].dt.to_period("W").astype(str)
        weekly = workout_df.groupby(["Week", "Exercise"])["Volume"].sum().reset_index()
        weekly_filtered = weekly[weekly["Exercise"] == selected]
        st.bar_chart(data=weekly_filtered, x="Week", y="Volume")
    else:
        st.info("No workout data yet.")
import streamlit_authenticator
st.write("Streamlit Authenticator version:", streamlit_authenticator.__version__)

