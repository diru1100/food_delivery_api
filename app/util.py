import sqlite3


conn = sqlite3.connect('application.db')
conn.execute("PRAGMA foreign_keys = 1")
curr = conn.cursor()

sql_create_customers_table = """CREATE TABLE IF NOT EXISTS customers(
                                ID INTEGER PRIMARY KEY,
                                NAME TEXT NOT NULL,
                                CASH_BALANCE REAL NOT NULL
                            );"""

sql_create_purchase_history_table = """CREATE TABLE IF NOT EXISTS purchase_history(
                                ID INTEGER PRIMARY KEY,
                                CUSTOMER_ID INTEGER,
                                DISH_ID INTEGER UNIQUE NOT NULL,
                                TRANSACTION_DATE TEXT NOT NULL,
                                FOREIGN KEY (CUSTOMER_ID) REFERENCES customers (ID)
                            );"""


sql_create_restaurants_table = """CREATE TABLE IF NOT EXISTS restaurants(
                                ID INTEGER PRIMARY KEY,
                                NAME TEXT NOT NULL,
                                CASH_BALANCE REAL NOT NULL
                            );"""


sql_create_dishes_table = """CREATE TABLE IF NOT EXISTS dishes(
                                ID INTEGER PRIMARY KEY,
                                RESTAURANT_ID INTEGER,
                                NAME TEXT NOT NULL,
                                PRICE REAL NOT NULL,
                                 FOREIGN KEY (RESTAURANT_ID) REFERENCES restaurants (ID)
                            );"""

sql_create_restuarent_opening_hours_table = """CREATE TABLE IF NOT EXISTS opening_hours(
                                ID INTEGER PRIMARY KEY,
                                RESTAURANT_ID INTEGER,
                                DAY TEXT,
                                OPEN_TIME TEXT,
                                CLOSE_TIME TEXT,                                
                                FOREIGN KEY (RESTAURANT_ID) REFERENCES restaurants (ID)
                            );"""

# sql_create_periods_table = """CREATE TABLE IF NOT EXISTS opening_hours(
#                                 ID INTEGER PRIMARY KEY,
#                                 OPEN_TIME TEXT,
#                                 CLOSE_TIME TEXT,
#                                 RESTAURANT_ID INTEGER,
#                                 FOREIGN KEY (RESTAURANT_ID) REFERENCES restaurants (ID)
#                             );"""


def create_tables():
    curr.execute(sql_create_customers_table)
    curr.execute(sql_create_purchase_history_table)
    curr.execute(sql_create_restaurants_table)
    curr.execute(sql_create_dishes_table)
    curr.execute(sql_create_restuarent_opening_hours_table)


create_tables()
