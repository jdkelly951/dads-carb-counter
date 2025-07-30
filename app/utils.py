import os
import json
from datetime import datetime
import pytz
from collections import Counter

EASTERN = pytz.timezone('America/New_York')

def get_now():
    """Returns the current datetime in US/Eastern timezone."""
    return datetime.now(EASTERN)


def get_user_data_path(user_id):
    """Returns the full path to the user-specific data file."""
    data_folder = os.path.join(os.getcwd(), 'data')
    os.makedirs(data_folder, exist_ok=True)
    return os.path.join(data_folder, f"{user_id}.json")


def load_data(user_id):
    """Loads the carb log data for a specific user."""
    path = get_user_data_path(user_id)
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data(user_id, data):
    """Saves the carb log data for a specific user."""
    path = get_user_data_path(user_id)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def get_suggestions(all_data):
    """Returns the top 10 most commonly entered food names across all logs."""
    all_foods = []
    for date_log in all_data.values():
        for item in date_log:
            all_foods.append(item['food'].title())

    return [food for food, count in Counter(all_foods).most_common(10)]
