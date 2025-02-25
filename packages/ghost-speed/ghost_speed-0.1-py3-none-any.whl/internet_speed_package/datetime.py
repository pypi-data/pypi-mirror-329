# internet_speed_package/datetime.py

import datetime

def get_current_datetime():
    """Returns the current date and time in 'YYYY-MM-DD HH:MM:SS' format."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
