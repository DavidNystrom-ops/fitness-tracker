import csv
from datetime import datetime

# File to store your workout log
FILENAME = "workout_log.csv"
import matplotlib.pyplot as plt

def log_workout():
    exercise = input("Exercise name: ")
    sets = input("Number of sets: ")
    reps = input("Reps per set: ")
    weight = input("Weight used (lbs): ")

    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), exercise, sets, reps, weight])
    print("Workout logged!")

def view_log():
    print("\n--- Workout History ---")
    start_date_str = input("Start date (YYYY-MM-DD) or press Enter to skip: ")
    end_date_str = input("End date (YYYY-MM-DD) or press Enter to skip: ")

    try:
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if not row:
                    continue
                date_str = row[0]
                try:
                    log_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                except ValueError:
                    continue

                # Filter by dates if provided
                if start_date_str:
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                    if log_date < start_date:
                        continue
                if end_date_str:
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                    if log_date > end_date:
                        continue

                print(row)
    except FileNotFoundError:
        print("No workouts logged yet!")


# Main menu
while True:
    print("\n1. Log a workout")
    print("2. View workout log")
    print("3. Graph progress")
    print("4. Quit")
    choice = input("Choose an option: ")

    if choice == '1':
        log_workout()
    elif choice == '2':
        view_log()
    elif choice == '3':
        graph_progress()
    elif choice == '4':
        break
    else:
        print("Invalid choice. Try again.")

def graph_progress():
    exercise_filter = input("Enter an exercise name to graph (or press Enter to show all): ").lower()
    dates = []
    weights = []

    try:
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if not row or len(row) < 5:
                    continue
                date_str, exercise, _, _, weight = row
                if exercise_filter and exercise.lower() != exercise_filter:
                    continue
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                    weight = float(weight)
                except ValueError:
                    continue
                dates.append(date)
                weights.append(weight)
    except FileNotFoundError:
        print("No workouts logged yet!")
        return

    if not dates:
        print("No matching data to graph.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(dates, weights, marker='o')
    plt.xlabel("Date")
    plt.ylabel("Weight (lbs)")
    plt.title(f"Progress for '{exercise_filter}'" if exercise_filter else "All Exercises Progress")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

