import json
import sqlite3


def extract(file):
    return json.load(file)


def transform(data):
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
