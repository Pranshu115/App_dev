import datetime

# Set the threshold for the 100m race (in seconds)
THRESHOLD = 20

# List to store race data
race_data = []

def add_race_result(user_id, timing):
    """Add a race result for a user."""
    date = datetime.date.today().strftime('%Y-%m-%d')
    status = "Below Threshold" if timing <= THRESHOLD else "Above Threshold"
    race_data.append({"user_id": user_id, "timing": timing, "date": date, "status": status})
    print(f"Race result added: User {user_id} completed the race in {timing}s ({status}).")

def view_performance(user_id):
    """View performance metrics for a specific user."""
    user_results = [entry for entry in race_data if entry['user_id'] == user_id]
    
    if not user_results:
        print(f"No data found for User {user_id}.")
        return

    total_races = len(user_results)
    below_threshold = sum(1 for result in user_results if result["status"] == "Below Threshold")
    above_threshold = total_races - below_threshold
    average_timing = sum(result["timing"] for result in user_results) / total_races

    print(f"\nPerformance for User {user_id}:")
    print(f"Total Races: {total_races}")
    print(f"Average Timing: {average_timing:.2f}s")
    print(f"Below Threshold: {below_threshold}")
    print(f"Above Threshold: {above_threshold}")
    print("\nDetails:")
    for result in user_results:
        print(f"- Date: {result['date']}, Timing: {result['timing']}s, Status: {result['status']}")

def main():
    """Main function to manage the application."""
    while True:
        print("\nMenu:")
        print("1. Add Race Result")
        print("2. View Performance")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            user_id = input("Enter User ID: ")
            try:
                timing = float(input("Enter Race Timing (in seconds): "))
                add_race_result(user_id, timing)
            except ValueError:
                print("Invalid timing. Please enter a number.")
        
        elif choice == '2':
            user_id = input("Enter User ID to view performance: ")
            view_performance(user_id)
        
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

## going to set the range of the timing aprat from the threshold like if you are in range of 15-17 then improvemet tips will be differnt from
## the person who has run the race in 25 sec 