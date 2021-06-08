
from . import app, db
from .models import *
from flask import request

# print(app)


@app.route('/', methods=['GET', 'POST'])
def test():
    x = Customer.query.all()
    print(x)
    return "Hello World!!"
# @app.route('/open-restaurants', methods=['GET', 'POST'])
# def open_restaurants():


# @app.route('/restaurants-with-budget-dishes', methods=['POST'])
# def restaurants_with_budget_dishes():


# @app.route('/purchase/<int:id>', methods=['POST'])
# def customer_purchase(id):


# @app.route('/search', methods=['POST'])
# def search_data():
