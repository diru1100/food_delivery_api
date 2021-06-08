import json
import sqlite3
from .format import *


def extract(file):
    return json.load(file)


def transform_data(customers_data, restaurants_data):

    for customer_data in customers_data:
        for purchase in customer_data["purchaseHistory"]:
            purchase["transactionDate"] = preprocess_datetime(
                purchase["transactionDate"])

    for restaurant_data in restaurants_data:
        day_wise_opening_hours = list()
        split_data = restaurants_data["openingHours"].split("/")

        for data in split_data:
            multiple_days_same_time = data.split(",")
            last_day_with_same_time = multiple_days_same_time[-1](" ", 1)
            operating_hours = last_day_with_same_time[1]
            last_day_with_same_time = last_day_with_same_time[0]
            operating_hours = operating_hours.split("-")

            open_time = last_day_with_same_time[0]
            open_time = open_time.strip()
            open_time = preprocess_time(open_time)

            close_time = last_day_with_same_time[1]
            close_time = close_time.strip()
            close_time = preprocess_time(close_time)

            map_day_to_hours[last_day_with_same_time]["Open"] = list()

        # only data which requires transformation are attributes involving date(time)
        # i.e transanctionDate and openingHours

    pass


def load():

    # Have to store openingHours in a different table to extract easily
    # a = "Mon, Weds 5:15 am - 8:30 pm / Tues, Sat 1:30 pm - 3:45 pm / Thurs 7:45 am - 8:15 am / Fri 1:30 pm - 7 pm / Sun 12:45 pm - 6:15 pm"
    # b = a.split("/")
    # parse timings

    pass


if __name__ == "__main__":

    restaurant_with_menu_file = open(
        'data/input/restaurant_with_menu.json')
    users_with_purchase_history_file = open(
        'data/input/users_with_purchase_history.json')

    restaurant_with_menu_data = extract(restaurant_with_menu_file)
    users_with_purchase_history_data = extract(
        users_with_purchase_history_file)

    restaurant_with_menu_transformed_data, users_with_purchase_history_transformed_data = transform_data(
        restaurant_with_menu_data, users_with_purchase_history_data)
