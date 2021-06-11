from util import create_tables
import json
import sqlite3
from format import preprocess_time, preprocess_datetime
from itertools import cycle
from data.sqlalchemy_util import Customer, Restaurant, Dish, PurchaseHistory, OpeningHour
from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
basedir = os.path.abspath(os.path.dirname(__file__))


def extract(file):
    return json.load(file)


def convert_range_of_days(input_days):

    list_of_days = ['Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat', 'Sun']

    start_day, end_day = input_days.split("-")
    start_day = start_day.strip()
    end_day = end_day.strip()
    if start_day == 'Thu':
        start_day = 'Thurs'
    if end_day == 'Thu':
        end_day = 'Thurs'

    if start_day == 'Wed':
        start_day = 'Weds'
    if end_day == 'Wed':
        end_day = 'Weds'

    start_pos = list_of_days.index(start_day)
    end_pos = list_of_days.index(end_day)
    if start_pos <= end_pos:
        return list_of_days[start_pos:end_pos+1]

    return list_of_days[start_pos:] + list_of_days[:end_pos+1]


def generate_operating_hours(input_hours_string):
    input_hours_string = input_hours_string.split("-")
    open_time = input_hours_string[0]
    open_time = open_time.strip()
    try:
        open_time = preprocess_time(open_time)
    except:
        print(input_hours_string)
        print(open_time, 'hi')

    close_time = input_hours_string[1]
    close_time = close_time.strip()
    try:
        close_time = preprocess_time(close_time)
    except:
        print(close_time, 'Bye \n')

    operating_hours = dict()
    operating_hours['openTime'] = list()
    operating_hours['closeTime'] = list()
    operating_hours['openTime'].append(
        str(open_time))

    if close_time < open_time:
        operating_hours['openTime'].append(
            '00:00:00')
        operating_hours['closeTime'].append(
            '23:59:59')

    operating_hours['closeTime'].append(
        str(close_time))

    return operating_hours


def transform_data(customers_data, restaurants_data):

    for customer_data in customers_data:

        for purchase in customer_data['purchaseHistory']:
            purchase['transactionDate'] = str(preprocess_datetime(
                purchase['transactionDate']))

    for restaurant_data in restaurants_data:
        day_wise_opening_hours = list()
        '''
            [
                "Mon" : {
                    openTime: [1, 2],
                    closeTime: [2, [4]]
                },

            ]
        '''

        split_data = restaurant_data['openingHours'].split('/')

        for data in split_data:

            operating_hours_string = ' '.join(data.strip().split(' ')[-5:])

            operating_hours = generate_operating_hours(
                operating_hours_string)

            only_days_string = data.replace(operating_hours_string, '')

            temp_list_of_days = only_days_string.split(",")

            multiple_days_with_same_time = list()

            for day in temp_list_of_days:
                if '-' in day:
                    multiple_days_with_same_time += convert_range_of_days(day)
                else:
                    multiple_days_with_same_time.append(day)

        # "Mon, Sat 3:45 pm - 10 pm / Tues 1:15 pm - 2:30 pm /
        #  Weds - Fri 2:30 pm - 9:30 pm / Sun 12:15 pm - 7 pm",

            for day in multiple_days_with_same_time:
                map_day_to_hours = list()
                map_day_to_hours.append(day)
                map_day_to_hours.append(operating_hours)
                day_wise_opening_hours.append(map_day_to_hours)

            restaurant_data['openingHours'] = day_wise_opening_hours


def load_data(customers_data, restaurants_data):

    # Loads data into the database

    # Have to store openingHours in a different table to extract easily
    # a = "Mon, Weds 5:15 am - 8:30 pm / Tues, Sat 1:30 pm - 3:45 pm / Thurs 7:45 am - 8:15 am / Fri 1:30 pm - 7 pm / Sun 12:45 pm - 6:15 pm"
    # b = a.split("/")
    # parse timings

    sqlite_filepath = 'sqlite:///' + \
        os.path.join(basedir, 'data/application.db')
    engine = create_engine(f"{sqlite_filepath}")

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    for restaurant_data in restaurants_data:
        temp_restaurant = Restaurant()
        # temp_restaurant.id = restaurant_data["id"]
        temp_restaurant.name = restaurant_data['restaurantName']
        temp_restaurant.cash_balance = restaurant_data['cashBalance']
        session.add(temp_restaurant)
        session.commit()

    for restaurant_data in restaurants_data:

        temp_restaurant_deet = session.query(Restaurant).filter_by(
            name=restaurant_data['restaurantName']).first()
        # print(temp_restaurent_id)
        # break
        for dish in restaurant_data['menu']:

            temp_dish = Dish()
            temp_dish.restaurant_id = temp_restaurant_deet.id
            temp_dish.name = dish['dishName']
            temp_dish.price = dish['price']

            session.add(temp_dish)
            session.commit()

        # ['Mon', {'openTime': ['11:45:00'], 'closeTime': ['16:45:00']}]
        # [' Weds  ', {'openTime': ['11:45:00'], 'closeTime': ['16:45:00']}]
        # [' Tues  ', {'openTime': ['07:45:00', '00:00:00'], 'closeTime': ['23:59:59', '02:00:00']}]
        # [' Thurs  ', {'openTime': ['17:45:00', '00:00:00'], 'closeTime': ['23:59:59', '00:00:00']}]
        # [' Fri', {'openTime': ['06:00:00'], 'closeTime': ['21:00:00']}]
        # [' Sun  ', {'openTime': ['06:00:00'], 'closeTime': ['21:00:00']}]
        # [' Sat ', {'openTime': ['10:15:00'], 'closeTime': ['21:00:00']}]

        for day in restaurant_data['openingHours']:
            # print(day)
            if len(day[1]['openTime']) == 1:
                temp_opening_hour = OpeningHour()
                temp_opening_hour.restaurant_id = temp_restaurant_deet.id
                temp_opening_hour.day = day[0]
                temp_opening_hour.open_time = day[1]['openTime'][0]
                temp_opening_hour.close_time = day[1]['closeTime'][0]

                session.add(temp_opening_hour)
                session.commit()
            else:
                for opening_time, closing_time in day[1]['openTime'], day[1]['closeTime']:
                    temp_opening_hour = OpeningHour()
                    temp_opening_hour.restaurant_id = temp_restaurant_deet.id
                    temp_opening_hour.day = day[0]
                    temp_opening_hour.open_time = opening_time
                    temp_opening_hour.close_time = closing_time

                    session.add(temp_opening_hour)
                    session.commit()

    for customer_data in customers_data:
        # print(customer_data, "\n\n\n")
        temp_customer = Customer()
        temp_customer.id = customer_data['id']+1
        temp_customer.name = customer_data['name']
        temp_customer.cash_balance = customer_data['cashBalance']
        session.add(temp_customer)
        session.commit()

        for purchase in customer_data['purchaseHistory']:

            temp_purchase = PurchaseHistory()
            temp_purchase.customer_id = customer_data['id']+1
            temp_dish_deet = session.query(Dish).filter_by(
                name=purchase['dishName']).first()
        # print(temp_restaurent_id)
            temp_purchase.dish_id = temp_dish_deet.id
            temp_purchase.transaction_date = purchase['transactionDate']
            session.add(temp_purchase)
            session.commit()


if __name__ == "__main__":

    create_tables()

    restaurant_with_menu_file = open(
        'data/input/restaurant_with_menu.json')
    users_with_purchase_history_file = open(
        'data/input/users_with_purchase_history.json')

    restaurant_with_menu_data = extract(restaurant_with_menu_file)
    users_with_purchase_history_data = extract(
        users_with_purchase_history_file)

    # print('\n', restaurant_with_menu_data[1]['openingHours'], '\n')

    transform_data(
        users_with_purchase_history_data, restaurant_with_menu_data)

    # for opening_hour in restaurant_with_menu_data[1]['openingHours']:

    #     print(opening_hour)

    load_data(users_with_purchase_history_data, restaurant_with_menu_data)

    # os.remove(os.path.join(basedir, 'data/application.db'))
