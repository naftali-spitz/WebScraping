# Hacker News Data Analysis

This project fetches data from the Hacker News API, extracts relevant details, and performs various data analysis tasks. The results are saved to CSV files for further exploration and visualization.

## Features

1. **Fetch Top Stories**: The script fetches the IDs of the top stories from the Hacker News API and then retrieves the details (title, URL, score, author, time, and number of comments) for each story.
2. **Save Story Details to CSV**: The story details are saved to a CSV file named `hacker news story details.csv`.
3. **Fetch Top-level Comments**: The script also fetches the top-level comments for the top stories and saves them to a separate CSV file.
4. **Data Analysis**:
   - Generates a bar chart showing the number of stories posted per day of the week.
   - Calculates and saves the summary statistics (mean, standard deviation, min, max) for the 'score' and 'descendants' columns.
   - Calculates and saves the average score for each unique user.
   - Calculates and saves the number of stories posted by each unique user.

## Requirements

- Python 3.6 or higher
- Pandas
- Matplotlib
- Requests
- tqdm

You can install the required packages using pip:


