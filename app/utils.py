import os
import json
from datetime import datetime, timedelta
import pytz
from collections import Counter

# Use consistent timezone across the app
EASTERN = pytz.timezone('America/New_York')


def get_now():
    """Return the current datetime in US/Eastern timezone."""
    return datetime.now(EASTERN)


def get_user_data_path(user_id):
    """
    Construct the full path to the user's data file.
    Automatically creates the data directory if it doesn't exist.
    """
    data_folder = os.path.join(os.getcwd(), 'data')
    os.makedirs(data_folder, exist_ok=True)
    return os.path.join(data_folder, f"{user_id}.json")


def load_data(user_id):
    """
    Load and return the carb log data for the given user.
    Also prunes any entries older than 30 days.
    Returns an empty dict if no file exists or it's unreadable.
    """
    path = get_user_data_path(user_id)
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    # Prune entries older than 30 days
    cutoff_date = get_now() - timedelta(days=30)
    data = {
        date_str: log for date_str, log in data.items()
        if EASTERN.localize(datetime.strptime(date_str, "%Y-%m-%d")) >= cutoff_date
    }

    # Save cleaned data back to disk
    save_data(user_id, data)
    return data


def save_data(user_id, data):
    """
    Save the given carb log data to disk for the specified user.
    """
    path = get_user_data_path(user_id)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def get_suggestions(all_data):
    """
    Return a list of the top 10 most frequently entered food names
    across all of the user's logs.
    """
    all_foods = []
    for date_log in all_data.values():
        for item in date_log:
            all_foods.append(item['food'].title())  # Normalize capitalization

    return [food for food, count in Counter(all_foods).most_common(10)]
