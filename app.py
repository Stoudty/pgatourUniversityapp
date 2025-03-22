import streamlit as st
import pandas as pd

st.title("PGA TOUR University Rankings Dashboard")

# A button to update rankings by triggering the scraper
# (Make sure you have your scraper function ready in scraper/scrape_rankings.py)
from scraper.scrape_rankings import update_rankings_csv

if st.button("Update Rankings Data"):
    update_rankings_csv()  # This will update data/rankings.csv
    st.success("Rankings data updated!")

# Try to load the CSV data from the data folder
try:
    data = pd.read_csv("data/rankings.csv")
except FileNotFoundError:
    st.error("No rankings data found. Please update the rankings data first.")
    st.stop()  # Stop the app if no data is found

st.write("### Current Rankings Data")
st.write(data)

# Convert 'date' column to datetime
if "date" in data.columns:
    data["date"] = pd.to_datetime(data["date"])

# Add a search input to filter players (default is "Luke Sample")
player_name = st.text_input("Search for a player:", "Luke Sample")

# Filter data by player name (case-insensitive)
filtered_data = data[data["name"].str.contains(player_name, case=False, na=False)]

# Display filtered data and a line chart of ranking trends if available
if not filtered_data.empty:
    st.write(f"### Ranking Trend for '{player_name}'")
    # Assuming multiple entries per player over time, we set the date as index and plot rank.
    # Lower ranking values are better, so you may want to reverse the y-axis if needed.
    st.line_chart(filtered_data.set_index("date")["rank"])
else:
    st.write("No data found for the specified player.")
