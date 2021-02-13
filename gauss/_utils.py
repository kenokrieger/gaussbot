"""Contains utility functions for the gauss package"""
import pickle5 as pickle
import calendar

from datetime import datetime, timedelta


def save_obj(obj, filename):
    """
    Saves an object as a pkl file.

    :param obj: The object to save.
    :param filename: The name of the file to save the object to.
    :type filename: str or path
    """
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(filename):
    """
    Loads an object from a given file.

    :param filename: The file where the object is located.
    :return: The stored object.
    """
    with open(filename, 'rb') as f:
        return pickle.load(f)


def find_date_interval(timeframe):
    """
    Finds a date interval of either this or last week, month or year.

    :param timeframe: The desired timeframe.
    :type timeframe: str
    :return: The date interval.
    :rtype: tuple
    """
    today = datetime.today()

    if "week" in timeframe:
        if "last" in timeframe:
            today -= timedelta(days=7)
        return _this_week(today)
    elif "month" in timeframe:
        if "last" in timeframe:
            today = datetime(today.year, today.month - 1, today.day)
        return _this_month(today)
    elif "year" in timeframe:
        if "last" in timeframe:
            today -= timedelta(days=366)
        return _this_year(today)


def _this_week(today):
    """
    Finds the first and last day of this week.

    :param today: The date of today.
    :return: The first and last day of the week
    :rtype: tuple
    """
    monday = today
    for diff in range(7):
        date_to_check = today - timedelta(days=diff)
        if not date_to_check.weekday():
            monday = date_to_check
            break
    sunday = (monday + timedelta(days=6))
    return monday, sunday


def _this_month(today):
    """
    Finds the first and last day of this month.

    :param today: The date of today.
    :return: The first and last day of this month.
    :rtype: tuple
    """
    first_day_this_month = 1
    last_day_this_month = calendar.monthrange(today.year, today.month)[1]
    first_day = datetime(today.year, today.month, first_day_this_month)
    last_day = datetime(today.year, today.month, last_day_this_month)
    return first_day, last_day


def _this_year(today):
    """
    Finds the first and last day of this year.

    :param today: The date of today.
    :return: The first and last day of this year.
    :rtype: tuple
    """
    first_day = datetime(today.year, 1, 1)
    last_day = datetime(today.year, 12, 31)
    return first_day, last_day
