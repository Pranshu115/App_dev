import datetime

# Set the threshold for the 100m race (in seconds)
THRESHOLD = 20

# List to store race data
race_data = []

# Define improvement tips based on timing ranges
# Define improvement tips based on timing ranges
IMPROVEMENT_TIPS = {
    "Elite": (0, 15, (
        "Outstanding! Keep up the training to maintain your edge.",
        "Focus on recovery techniques like ice baths and massage therapy to avoid injuries.",
        "Experiment with advanced speed training drills like overspeed running to break your limits."
    )),
    "Intermediate": (15, 17, (
        "Great performance! Focus on speed drills and endurance.",
        "Incorporate interval training into your routine to enhance both speed and stamina.",
        "Refine your running technique to minimize energy wastage during sprints."
    )),
    "Novice": (17, 20, (
        "Good effort! Work on strength training and agility.",
        "Add hill sprints to your workouts to build power and explosiveness.",
        "Improve your diet by including more protein-rich foods to support muscle recovery."
    )),
    "Beginner": (20, 25, (
        "You're getting there! Focus on basic conditioning.",
        "Start a consistent training schedule with gradual increases in intensity.",
        "Work on improving your cardiovascular endurance with steady-state runs."
    )),
    "Needs Improvement": (25, float('inf'), (
        "Consider starting with consistent running practice and building stamina.",
        "Walk/run intervals can help build your endurance if you're just beginning.",
        "Consult a coach or join a running group to stay motivated and get guidance."
    ))
}

def get_improvement_tip(timing):
    """Get improvement tips based on the timing."""
    for level, (min_time, max_time, tips) in IMPROVEMENT_TIPS.items():
        if min_time <= timing < max_time:
            return level, tips
    return "Undefined", ("No tips available.",)

def add_race_result(name, timing):
    """Add a race result for a user."""
    date = datetime.date.today().strftime('%Y-%m-%d')
    status = "Below Threshold" if timing <= THRESHOLD else "Above Threshold"
    level, tips = get_improvement_tip(timing)
    race_data.append({"name": name, "timing": timing, "date": date, "status": status, "level": level, "tips": tips})
    print(f"Race result added: {name} completed the race in {timing}s ({status}).")
    print(f"Performance Level: {level}")
    print("Improvement Tips:")
    for tip in tips:
        print(f"- {tip}")

def view_performance(name):
    """View performance metrics for a specific user."""
    user_results = [entry for entry in race_data if entry['name'].lower() == name.lower()]
    
    if not user_results:
        print(f"No data found for {name}.")
        return

    total_races = len(user_results)
    below_threshold = sum(1 for result in user_results if result["status"] == "Below Threshold")
    above_threshold = total_races - below_threshold
    average_timing = sum(result["timing"] for result in user_results) / total_races

    print(f"\nPerformance for {name}:")
    print(f"Total Races: {total_races}")
    print(f"Average Timing: {average_timing:.2f}s")
    print(f"Below Threshold: {below_threshold}")
    print(f"Above Threshold: {above_threshold}")
    print("\nDetails:")
    for result in user_results:
        print(f"- Date: {result['date']}, Timing: {result['timing']}s, Status: {result['status']}, Level: {result['level']}")
        print("  Tips:")
        for tip in result['tips']:
            print(f"    - {tip}")


def main():
    """Main function to manage the application."""
    while True:
        print("\nMenu:")
        print("1. Add Race Result")
        print("2. View Performance")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter Name: ")
            try:
                timing = float(input("Enter Race Timing (in seconds): "))
                add_race_result(name, timing)
            except ValueError:
                print("Invalid timing. Please enter a number.")
        
        elif choice == '2':
            name = input("Enter Name to view performance: ")
            view_performance(name)
        
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
