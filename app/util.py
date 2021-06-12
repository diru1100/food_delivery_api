import sqlite3
import os
basedir = os.path.abspath(os.path.dirname(__file__))


# raw sqlite queries to create needed tables
sql_create_customers_table = """CREATE TABLE IF NOT EXISTS customers(
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                cash_balance REAL NOT NULL
                            );"""

sql_create_purchase_history_table = """CREATE TABLE IF NOT EXISTS purchase_history(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                customer_id INTEGER,
                                dish_id INTEGER NOT NULL,
                                transaction_date TEXT NOT NULL,
                                FOREIGN KEY (customer_id) REFERENCES customers (ID)
                            );"""


sql_create_restaurants_table = """CREATE TABLE IF NOT EXISTS restaurants(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                cash_balance REAL NOT NULL
                            );"""


sql_create_dishes_table = """CREATE TABLE IF NOT EXISTS dishes(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                restaurant_id INTEGER,
                                name TEXT NOT NULL,
                                price REAL NOT NULL,
                                FOREIGN KEY (restaurant_id) REFERENCES restaurants (ID)
                            );"""

sql_create_restuarent_opening_hours_table = """CREATE TABLE IF NOT EXISTS opening_hours(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                restaurant_id INTEGER,
                                day TEXT,
                                open_time TEXT,
                                close_time TEXT,                                
                                FOREIGN KEY (restaurant_id) REFERENCES restaurants (ID)
                            );"""


def create_tables():
    conn = sqlite3.connect(basedir+'/data/etl_application.db')
    conn.execute("PRAGMA foreign_keys = 1")
    curr = conn.cursor()
    curr.execute(sql_create_customers_table)
    curr.execute(sql_create_purchase_history_table)
    curr.execute(sql_create_restaurants_table)
    curr.execute(sql_create_dishes_table)
    curr.execute(sql_create_restuarent_opening_hours_table)
