import os
import pandas as pd
import requests
from datetime import datetime

# Function to get nutrition info from Edamam API
def get_nutrition_info(food_item, APP_ID, APP_KEY):
    url = f"https://api.edamam.com/api/nutrition-data?app_id={APP_ID}&app_key={APP_KEY}&ingr={food_item}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("calories") is not None:
            return {
                "calories": data.get("calories"),
                "protein": data.get("totalNutrients", {}).get("PROCNT", {}).get("quantity", 0),
                "fat": data.get("totalNutrients", {}).get("FAT", {}).get("quantity", 0),
                "carbs": data.get("totalNutrients", {}).get("CHOCDF", {}).get("quantity", 0)
            }
        else:
            return "not_found"
    else:
        print(f"Error fetching data for {food_item}. Status Code: {response.status_code}")
        return None

# Function to manually enter nutrition info
def manual_entry(food_item):
    print(f"Information for {food_item} not available. Please enter the values manually or modify the food item name.")
    choice = input("Enter 'm' to manually input values, or 'r' to rename the food item: ")
    if choice.lower() == 'm':
        calories = float(input("Enter calories: "))
        protein = float(input("Enter protein (g): "))
        carbs = float(input("Enter carbohydrates (g): "))
        fat = float(input("Enter fat (g): "))
        return {
            "calories": calories,
            "protein": protein,
            "fat": fat,
            "carbs": carbs
        }
    elif choice.lower() == 'r':
        new_food_item = input("Enter the new food item name: ")
        return get_nutrition_info(new_food_item, APP_ID, APP_KEY)
    else:
        print("Invalid choice. Skipping this food item.")
        return None

# Your Edamam API credentials
# APP_ID = "your_app_id"
# APP_KEY = "your_app_key"

# Specify the full path to the folder where you want to save the Excel file
folder_path = "C:\\Users\\malla\\OneDrive\\Documents\\Apps created by me"
excel_file = f"{folder_path}\\food&exercise_tracker.xlsx"

# Check if the folder exists, if not, create it
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Check if the Excel file exists and change the mode accordingly
if os.path.exists(excel_file):
    mode = 'a'  # Append mode if file exists
    if_sheet_exists = 'replace'
else:
    mode = 'w'  # Write mode if file does not exist
    if_sheet_exists = None
    
# Ask user for the meal category
meal_input = input("Enter 'B' for Breakfast, 'L' for Lunch, or 'D' for Dinner: ").upper()
meal_dict = {'B': 'Breakfast', 'L': 'Lunch', 'D': 'Dinner'}
meal = meal_dict.get(meal_input, None)

if meal is None:
    print("Invalid meal option. Exiting.")
else:
    # User input for foods
    foods_input = input(f"Enter the foods you've eaten for {meal} (comma-separated): ")
    foods = foods_input.split(',')

    # Get current date and time
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Load existing Excel file or create new DataFrame for food log
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file, sheet_name='Food Log')
    else:
        df = pd.DataFrame(columns=["Date", "Time", "Meal", "Food", "Calories", "Protein", "Carbs", "Fat"])

    # Check for duplicates and update if necessary in food log
    existing_entries_index = df[(df['Date'] == date_str) & (df['Meal'] == meal)].index
    if not existing_entries_index.empty:
        # Remove existing entries
        df = df.drop(existing_entries_index)

    # Add new entries to food log
    for food in foods:
        food = food.strip()
        nutrition_info = get_nutrition_info(food, APP_ID, APP_KEY)
        if nutrition_info == "not_found":
            nutrition_info = manual_entry(food)
        if nutrition_info:
            entry = {
                "Date": date_str,
                "Time": time_str,
                "Meal": meal,
                "Food": food,
                "Calories": nutrition_info["calories"],
                "Protein": nutrition_info["protein"],
                "Carbs": nutrition_info["carbs"],
                "Fat": nutrition_info["fat"]
            }
            
            df.loc[len(df)] = entry 

    # Load existing Excel file or create new DataFrame for exercise log
    if os.path.exists(excel_file):
        exercise_df = pd.read_excel(excel_file, sheet_name='Exercise Log')
    
    else:
        exercise_df = pd.DataFrame(columns=["Date", "Time", "Meal", "Exercise Type", "Calories Burnt"])
        exercise_df['Calories Burnt'] = exercise_df['Calories Burnt'].astype(float)


    # Ask user for exercise details
    exercise_input = input("Enter exercise type and calories burnt (comma-separated): ")
    exercise_data = exercise_input.split(',')
    exercise_type = exercise_data[0].strip()
    exercise_calories = float(exercise_data[1].strip())
    exercise_meal = meal

    # Get current date and time for exercise log
    exercise_entry_date = now.strftime("%Y-%m-%d")
    exercise_entry_time = now.strftime("%H:%M:%S")

    # Add exercise entry to exercise log
    exercise_entry = {
    "Date": exercise_entry_date,
    "Time": exercise_entry_time,
    "Meal": meal,  # Include the meal
    "Exercise Type": exercise_type,
    "Calories Burnt": exercise_calories
    }
    # Find the index of the row to be replaced
# Find the index of the row to be replaced
    replace_index = exercise_df[(exercise_df['Date'] == exercise_entry_date) & (exercise_df['Meal'] == exercise_meal)].index
    if not replace_index.empty:
        for column in ['Time', 'Calories Burnt']:  # Update specific columns
            exercise_df.loc[replace_index[0], column] = exercise_entry[column] 
    else:
        new_index = len(exercise_df)
        exercise_df.loc[new_index, :] = exercise_entry

    # Export both DataFrames to Excel
    with pd.ExcelWriter(excel_file, mode=mode, if_sheet_exists=if_sheet_exists) as writer: 
        df.to_excel(writer, index=False, header=True, sheet_name='Food Log')

        # Calculate daily totals for food log
        daily_totals_food = df.groupby(["Date", "Meal"]).agg({
            "Protein": "sum",
            "Carbs": "sum",
            "Fat": "sum",
            "Calories": "sum"
        }).reset_index()
        daily_totals_food.columns = ["Date", "Meal", "Protein", "Carbs", "Fat", "Total Calories (Food)"]

        # Calculate daily totals for exercise log
        daily_totals_exercise = exercise_df.groupby(["Date", "Meal"]).agg({
            "Calories Burnt": "sum"
        }).reset_index()
        daily_totals_exercise.columns = ["Date","Meal", "Calories Burnt"]
        
        BMR = 1500

       # Merge daily totals for food and exercise
        daily_totals = pd.merge(daily_totals_food, daily_totals_exercise, on=["Date", "Meal"], how="left")
        

        # Calculate final total calories
        daily_totals["Final Total Calories"] = daily_totals["Total Calories (Food)"] - daily_totals["Calories Burnt"]

        # Calculate calories difference
        daily_totals["Calories Difference"] = daily_totals["Final Total Calories"] - BMR

        # Add a row for the total of the day
        daily_totals_summary = daily_totals.groupby("Date").sum().reset_index()
        daily_totals_summary["Meal"] = "Total"

        # Modify 'Calories Difference' for the 'Total' row 
        daily_totals_summary["Calories Difference"] = (
            daily_totals_summary["Final Total Calories"] - BMR
        )  
        daily_totals = pd.concat([daily_totals, daily_totals_summary])
        # Export daily tracker to Excel
        daily_totals.to_excel(writer, index=False, header=True, sheet_name='Daily Tracker')

        # Export exercise log to Excel
        exercise_df.to_excel(writer, index=False, header=True, sheet_name='Exercise Log')

    print(f"Data exported to {excel_file}")
