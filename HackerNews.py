import requests
import csv
import pandas as pd
import tqdm
import matplotlib.pyplot as plt
from datetime import datetime

headers = ['id', 'deleted', 'type', 'by', 'time', 'text', 'dead', 'parent', 'poll', 'kids', 'url', 'score', 'title', 'parts', 'descendants']
def main():
    """
    The main function that prompts the user to perform various actions.

    The function presents the user with two actions: "create csv file for Hacker News" and "data analysis".
    For each action, the user is prompted to enter 'y' or 'n' to indicate whether they want to perform the action.

    If the user enters 'y', the corresponding function is called to perform the action.
    If the user enters 'n', the loop for the current action is broken, and the program moves on to the next action.
    If the user enters anything else, an error message is displayed, and the user is prompted again.
    """
    
    for action in ["create csv file for Hacker News", "data analysis"]:
        while True:
            user_response = input(f"Do you want to {action}? (y/n) ")
            if user_response.lower() == 'y':
                if action == "create csv file for Hacker News":
                    create_csv_file_for_Hacker_News()
                elif action == "data analysis":
                    data_analysis()
                break
            elif user_response.lower() == 'n':
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
                 
def get_data_HN_from_url(url, name=None):
    """
    Fetches data from the Hacker News API using the provided URL.

    Args:
        url (str): The URL endpoint to fetch data from the Hacker News API.
        name (str, optional): The name of the data being fetched (e.g., "top stories"). Defaults to None.

    Returns:
        dict: The JSON data fetched from the Hacker News API.
    """
    
    HN_api_url = f'https://hacker-news.firebaseio.com/v0{url}.json'
    HN_api_response = requests.get(HN_api_url)
    
    #Fetch the IDs of the top stories using the Hacker News API.
    if HN_api_response.status_code == 200:
        return HN_api_response.json()
    else:
        print("Uh oh, looks like the Hacker News API decided to take a coffee break! Can't fetch the data.")

def create_csv_file(file_path, headers, row_data):
    with open(file_path, 'w', newline='') as csvfile:
        header = headers
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for row in row_data:
            writer.writerow(row)
            
def create_csv_file_for_Hacker_News_Comments(data):
    """
    Creates a CSV file with the provided data.

    Args:
        file_path (str): The full path (including the file name) where the CSV file will be created.
        headers (list): A list of column names (headers) for the CSV file.
        row_data (list): A list of dictionaries, where each dictionary represents a row of data in the CSV file.
            The keys in the dictionaries should match the headers.

    Returns:
        None
    """
    kids_data = []
    for story in data:
        # if story['kids'] == None:
        #     continue
        for kid in story['kids'][:1]:
            try:
                kid_url = f'/item/{kid}'
                kid_data = get_data_HN_from_url(kid_url)
                kids_data.append(kid_data)
            except:
                continue
    file_name = 'hacker news top stories top level comments.csv'
    create_csv_file(file_name, headers, kids_data)

def create_csv_file_for_Hacker_News():
    """
    Fetches the top stories from the Hacker News API, extracts the relevant details, and saves them to a CSV file.
    It also calls the `create_csv_file_for_Hacker_News_Comments()` function to fetch and save the top-level comments for the top stories.
    """
    
    #Fetch and Save Top Stories
    top_stories_url = '/topstories'
    top_stories_ids = get_data_HN_from_url(top_stories_url)

    #list for story data
    stories_data = []

    #For each story ID, fetch the details (e.g., title, URL, score, author, time, and number of comments).
    for story_id in tqdm.tqdm(top_stories_ids[:5], desc='Fetching Story Details'):
        story_url = f'/item/{story_id}'
        story_data = get_data_HN_from_url(story_url)
        
        if story_data['type'] == 'story':
            # story_data['time'] = pd.to_datetime(story_data['time'], unit='s')
            stories_data.append(story_data)

    file_name = 'hacker news story details.csv'
    create_csv_file(file_name, headers, stories_data)
    create_csv_file_for_Hacker_News_Comments(stories_data)
    
def story_posting_by_day(data):
    """
    Generates a bar chart showing the number of Hacker News stories posted per day of the week.

    Args:
        data (pandas.DataFrame): A DataFrame containing the story details, including the 'time' column.

    Returns:
        plt.show
    """
    story_days = [int(timestamp // (24 * 60 * 60)) % 7 for timestamp in data['time']]

    # Count the occurrences of each day of the week 0 for Sunday, 6 for Saturday
    day_counts = [story_days.count(i) for i in range(7)]

    # Define days of the week as labels for the graph
    day_labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    plt.figure(figsize=(8, 6))
    plt.bar(day_labels, day_counts)
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Stories Posted')
    plt.title('Hacker News Stories Posted per Day of the Week')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()

def data_analysis():
    """
    Performs various data analysis tasks on the Hacker News story details and saves the results to CSV files.

    The following analyses are performed:
    1. Generates a bar chart showing the number of stories posted per day of the week.
    2. Calculates and saves the summary statistics (mean, standard deviation, min, max) for the 'score' and 'descendants' columns.
    3. Calculates and saves the average score for each unique user.
    4. Calculates and saves the number of stories posted by each unique user.
    """
    
    story_details = pd.read_csv('hacker news story details.csv')

    story_posting_by_day(story_details)

    analysis1 = story_details[['score', 'descendants']].describe().round(2)
    analysis1.to_csv('analysis1.csv', index=True)
    
    avg_scores = story_details.groupby('by')['score'].mean().reset_index()
    path = 'avg score by user.csv'
    avg_scores.to_csv(path, index=False)
    
    num_stories_per_user = story_details['by'].value_counts()
    num_stories_per_user.to_csv('num_stories_per_user.csv')
        
if __name__ == "__main__":
    main()


    