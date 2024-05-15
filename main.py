import re
import numpy as np
import pandas as pd
from tkinter import messagebox
import matplotlib.pyplot as plt
from Data_scraper import FootballData


# Call the class created to scrape the data
months = ["08", "09", "10", "11", "12", "01", "02", "03", "04", "05"]
scraper = FootballData(months)
scraper.scrape_data()
scraper.save_to_csv("footbal_data.csv")

#Append raw data to csv
raw_data = []
with open("footbal_data.csv", mode="r") as file:
    for element in file:
        raw_data.append(element)

# Split the data into 2 teams with score and start cleaning
home_team_with_score = []
away_team_with_score = []
for data in raw_data:
    segments = data.split(" at Full time")

    for segment in segments:
        teams = segment.split(",")
        if len(teams) < 2:
            away_team_with_score.append(teams[0])
        else:
            home_team_with_score.append(teams[0])
            away_team_with_score.append(teams[1])

for i in away_team_with_score:
    if i == "":
        index = away_team_with_score.index("")
        away_team_with_score.pop(index)

# Split data for home teams into teams and respective score
home_team = []
home_score = []
for i in home_team_with_score:
    element = re.finditer(r"\d", i)
    last_digit_index = None
    for match in element:
        last_digit_index = match.start()
    first_part = i[:last_digit_index]
    second_part = i[last_digit_index:]
    home_team.append(first_part.strip().lower())
    home_score.append(int(second_part))

# Split data for away team into teams and score
away_team = []
away_score = []
for i in away_team_with_score:
    element = re.finditer(r"\d", i)
    last_digit_index = None
    for match in element:
        last_digit_index = match.start()
    first_part = i[:last_digit_index]
    second_part = i[last_digit_index:]
    away_team.append(first_part.strip().lower())
    away_score.append(int(second_part))

# Create dataframe
data = pd.DataFrame({"Home Team": home_team,
                     "Home Score": home_score,
                     "Away Team": away_team,
                     "Away Score": away_score})

# Calculate the scoring rate for home, away and total games
scoring_home = []
goals_home = 0
goals_taken_home = 0
matches_home = 0

scoring_away = []
goals_away = 0
goals_taken_away = 0
matches_away = 0

total_scoring = []
total_goals = 0
total_matches = 0

user_input = input("What team you want to choose?\n").lower()

for index, row in data.iterrows():
    if row["Home Team"] == user_input:
        goals_home += row["Home Score"]
        matches_home += 1
        scoring_rate = goals_home/matches_home
        scoring_home.append(round(scoring_rate, 2))
        goals_taken_home += row["Away Score"]
        total_goals += row["Home Score"]
        total_matches += 1
        total_scoring_rate = total_goals/total_matches
        total_scoring.append(round(total_scoring_rate, 2))
    if row["Away Team"] == user_input:
        goals_away += row["Away Score"]
        matches_away += 1
        scoring_rate = goals_away/matches_away
        scoring_away.append(round(scoring_rate, 2))
        goals_taken_away += row["Home Score"]
        total_goals += row["Away Score"]
        total_matches += 1
        total_scoring_rate = total_goals / total_matches
        total_scoring.append(round(total_scoring_rate, 2))

# Create a chart with data for the requested team
if user_input in data["Home Team"].str.lower().values or user_input in data["Away Team"].str.lower().values:
    x_home = np.arange(matches_home)
    y_home = np.array(scoring_home)

    x_away = np.arange(matches_away)
    y_away = np.array(scoring_away)

    plt.plot(x_home, y_home, label="Home")
    plt.plot(x_away, y_away, label="Away")

    plt.plot(np.arange(total_matches), total_scoring, label="Total")
    plt.legend()
    plt.show()
else:
    messagebox.showerror("Team Not Found", "The team was not found")
