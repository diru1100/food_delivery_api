from util import create_tables
import json
import sqlite3
from format import preprocess_datetime, preprocess_opening_hours_data
from itertools import cycle
from data.sqlalchemy_util import Customer, Restaurant, Dish, PurchaseHistory, OpeningHour
from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
basedir = os.path.abspath(os.path.dirname(__file__))


def extract(file):
    return json.load(file)


def transform_data(customers_data, restaurants_data):
    ''' Trasform/preprocess given data in required format to handle it easily.
        Main preprocessing is done on fields which invovle time, datetime
    '''

    # transforming customer 'transactionDate' attribute
    for customer_data in customers_data:

        for purchase in customer_data['purchaseHistory']:
            purchase['transactionDate'] = str(preprocess_datetime(
                purchase['transactionDate']))

    # transforming restaurannt 'openingHours' attribute
    for restaurant_data in restaurants_data:

        day_wise_opening_hours = list()

        split_opening_hours_data = restaurant_data['openingHours'].split('/')

        for opening_hours_data in split_opening_hours_data:

            day_wise_opening_hours += preprocess_opening_hours_data(
                opening_hours_data)
            restaurant_data['openingHours'] = day_wise_opening_hours


def load_data(customers_data, restaurants_data):
    ''' Loads data into the database in different tables
        Restaurant, Customer, Dish, OpeningHour, PurchaseHistory
    '''

    # creating db session to load data
    sqlite_filepath = 'sqlite:///' + \
        os.path.join(basedir, 'data/etl_application.db')
    engine = create_engine(f"{sqlite_filepath}")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    # load Restaurant data in database
    for restaurant_data in restaurants_data:
        temp_restaurant = Restaurant()
        temp_restaurant.name = restaurant_data['restaurantName']
        temp_restaurant.cash_balance = restaurant_data['cashBalance']
        session.add(temp_restaurant)
        session.commit()

    for restaurant_data in restaurants_data:

        # extract restaurant id to map relevant information
        temp_restaurant_details = session.query(Restaurant).filter_by(
            name=restaurant_data['restaurantName']).first()

        # load Dish data in database
        for dish in restaurant_data['menu']:
            temp_dish = Dish()
            temp_dish.restaurant_id = temp_restaurant_details.id
            temp_dish.name = dish['dishName']
            temp_dish.price = dish['price']
            session.add(temp_dish)
            session.commit()

        # load OpeningHour data in database
        for day in restaurant_data['openingHours']:

            # considering if given time extends beyond 1 day
            if len(day[1]['openTime']) == 1:
                temp_opening_hour = OpeningHour()
                temp_opening_hour.restaurant_id = temp_restaurant_details.id
                temp_opening_hour.day = day[0]
                temp_opening_hour.open_time = day[1]['openTime'][0]
                temp_opening_hour.close_time = day[1]['closeTime'][0]

                session.add(temp_opening_hour)
                session.commit()
            else:
                for opening_time, closing_time in day[1]['openTime'], day[1]['closeTime']:
                    temp_opening_hour = OpeningHour()
                    temp_opening_hour.restaurant_id = temp_restaurant_details.id
                    temp_opening_hour.day = day[0]
                    temp_opening_hour.open_time = opening_time
                    temp_opening_hour.close_time = closing_time

                    session.add(temp_opening_hour)
                    session.commit()

    for customer_data in customers_data:

        # load Customer data in database
        temp_customer = Customer()
        temp_customer.id = customer_data['id']+1
        temp_customer.name = customer_data['name']
        temp_customer.cash_balance = customer_data['cashBalance']
        session.add(temp_customer)
        session.commit()

        # load PurchaseHistory data in database
        for purchase in customer_data['purchaseHistory']:

            temp_purchase = PurchaseHistory()
            temp_purchase.customer_id = customer_data['id']+1
            temp_dish_deet = session.query(Dish).filter_by(
                name=purchase['dishName']).first()

            temp_purchase.dish_id = temp_dish_deet.id
            temp_purchase.transaction_date = purchase['transactionDate']
            session.add(temp_purchase)
            session.commit()


if __name__ == "__main__":

    # create respective tables needed to load data from given json datasets
    create_tables()

    restaurant_with_menu_file = open(
        'data/input/restaurant_with_menu.json')
    users_with_purchase_history_file = open(
        'data/input/users_with_purchase_history.json')

    # ETL steps are done in the following code

    restaurant_with_menu_data = extract(restaurant_with_menu_file)
    users_with_purchase_history_data = extract(
        users_with_purchase_history_file)

    transform_data(
        users_with_purchase_history_data, restaurant_with_menu_data)

    load_data(users_with_purchase_history_data, restaurant_with_menu_data)
