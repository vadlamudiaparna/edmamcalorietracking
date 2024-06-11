# Food and Exercise Tracking App
This repository contains a simple tracking application written in Python for monitoring food intake and exercise. The app fetches nutritional information using the Edamam API and tracks the calories consumed and burned throughout the day.

## Description
The Food and Exercise Tracking App allows users to:

Track food intake by fetching nutritional information from the Edamam API.
Manually input nutritional information if it is not available through the API.
Log daily exercise activities and calculate the calories burned.
Export the data to an Excel file for further analysis.
Features
Food Tracking: Enter food items to fetch their nutritional information (calories, protein, fat, carbs) from the Edamam API.
Manual Entry: If the food item is not found in the API, users can manually input the nutritional information.
Exercise Logging: Record exercise activities and the calories burned.
Daily Summary: Calculate and display the total calories consumed, calories burned, and the net calories for each day.
Export to Excel: Save the food and exercise logs, along with daily summaries, to an Excel file.
Installation
To run this app locally, you need to have Python installed on your system. Follow these steps to set up the project:


## Install the required packages:

bash
Copy code
pip install pandas requests openpyxl
Set up API credentials:

Replace APP_ID and APP_KEY in the notebook with your Edamam API credentials.
Usage
Open the Jupyter notebook Food and Exercise simple tracking app_python code.ipynb.

## Run the cells in the notebook to:

Input your food items and fetch nutritional information.
Log your exercise activities.
Export the data to an Excel file.
Review the exported Excel file to analyze your food and exercise data.# edmamcalorietracking
An end to end app to track calories of exercise and food for breakfast, lunch and dinner by entering foods in natural language interface seperated by commas
