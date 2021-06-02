import sqlite3


conn = sqlite3.connect('tutorial.db')
curr = conn.cursor()

sql_create_customers_table = """CREATE TABLE IF NOT EXISTS customers(
                                ID INTEGER PRIMARY KEY,
                                NAME TEXT NOT NULL,
                                cashBalance INTEGER DEFAULT 0 NOT NULL,
                            );"""

sql_create_purchase_history_table = """CREATE TABLE IF NOT EXISTS purchase_history(
                                ID INTEGER PRIMARY KEY,
                                CUSTOMER_ID INTEGER UNIQUE NOT NULL,
                                DISH_ID INTEGER UNIQUE NOT NULL,
                                cashBalance INTEGER DEFAULT 0 NOT NULL,
                            );"""


sql_create_restuarents_table = """CREATE TABLE IF NOT EXISTS purchase_history(
                                ID INTEGER PRIMARY KEY,
                                NAME TEXT NOT NULL,
                                cashBalance INTEGER DEFAULT 0 NOT NULL,
                            );"""


sql_create_dishes_table = """CREATE TABLE IF NOT EXISTS purchase_history(
                                ID INTEGER PRIMARY KEY,
                                RESTAURENT_ID FORIEGN KEY,
                                NAME TEXT NOT NULL,
                                PRICE INTEGER DEFAULT 0 NOT NULL,
                            );"""

sql_create_restuarent_opening_hours_table = """CREATE TABLE IF NOT EXISTS purchase_history(
                                ID INTEGER PRIMARY KEY,
                                RESTAURENT_ID FORIEGN KEY,
                                OPEN_TIME 
                                CLOSE_TIME
                            );"""


def create_tables():
    curr.execute()
