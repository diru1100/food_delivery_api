
# from .data.sqlalchemy_util import PurchaseHistory
from itertools import groupby
from . import app, db
from .models import *
from flask import request, jsonify
from datetime import datetime
from sqlalchemy import and_
# print(app)


@app.route('/', methods=['GET', 'POST'])
def test():
    x = Customer.query.filter_by(id=6).first()

    y = OpeningHour.query.filter_by(id=6).first()

    z = Dish.query.filter_by(id=6).first()

    a = PurchaseHistory.query.filter_by(id=1000).first()

    print(x.name)
    print(z.name, z.id, z.price, '\n')
    print(y.restaurant_id, y.id, y.open_time, y.close_time, '\n')

    print(a.id, a.transaction_date, a.dish_id, a.customer_id)

    # print(x.query)
    # print(x.metadata)
    return "Hello World!!"


@app.route('/open-restaurants', methods=['GET', 'POST'])
def open_restaurants():

    input_date_time = request.get_json(force=True)
    input_date_time = input_date_time['time']
    input_date_time = datetime.strptime(input_date_time, "%Y-%m-%d  %H:%M:%S")

    list_of_days = ['Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat', 'Sun']

    week_day_num = input_date_time.weekday()

    given_day = list_of_days[week_day_num]

    given_time = str(datetime.time(input_date_time))

    matching_opening_hours = OpeningHour.query.filter(
        OpeningHour.day == given_day, OpeningHour.open_time <= given_time, OpeningHour.close_time >= given_time).all()

    # print(restaurants_available_at_given_datetime)
    restaurants_available_at_given_datetime = list()
    for opening_hour in matching_opening_hours:
        temp_restaurant = Restaurant.query.filter_by(
            id=opening_hour.restaurant_id).first()
        restaurants_available_at_given_datetime.append(temp_restaurant.name)

    # print(restaurants_available_at_given_datetime)

    return jsonify(restaurants_available_at_given_datetime)


@app.route('/restaurants-with-budget-dishes', methods=['POST'])
def restaurants_with_budget_dishes():

    input_data = request.get_json(force=True)

    min_price = input_data["price_range"][0]
    max_price = input_data["price_range"][1]

    budget_dishes = Dish.query.filter(
        Dish.price >= min_price, Dish.price <= max_price).all()

    restaurants_with_budget_dishes = dict()
    set_of_restaurant_ids = set()

    for budget_dish in budget_dishes:

        set_of_restaurant_ids.add(budget_dish.restaurant_id)

        # print(budget_dish.restaurant_id, '\n')
    for restaurant_id in set_of_restaurant_ids:
        restaurants_with_budget_dishes[restaurant_id] = dict()
        restaurants_with_budget_dishes[restaurant_id]["restaurantName"] = Restaurant.query.filter_by(
            id=restaurant_id).first().name
        restaurants_with_budget_dishes[restaurant_id]["Dishes"] = list()

    for budget_dish in budget_dishes:

        temp_dish = {"name": budget_dish.name, "price": budget_dish.price}
        restaurants_with_budget_dishes[budget_dish.restaurant_id]["Dishes"].append(
            temp_dish)

    for restaurant_id in set_of_restaurant_ids:
        print(
            len(restaurants_with_budget_dishes[restaurant_id]['Dishes']), '\n hi?')

    restaurants_with_given_criteria = list()
    for restaurant_id in set_of_restaurant_ids:
        dishes = len(restaurants_with_budget_dishes[restaurant_id]['Dishes'])
        if input_data["not_have"] != dishes:
            restaurants_with_given_criteria.append(
                restaurants_with_budget_dishes[restaurant_id]["restaurantName"])

    return jsonify(restaurants_with_given_criteria[:input_data["limit"]])
    # print(restaurants_with_budget_dishes["restaurant_id"])


@app.route('/search', methods=['POST'])
def search_data():
    # tag = request.form["tag"]
    input_data = request.get_json(force=True)
    search = "%{}%".format(input_data["search_string"])
    relevant_restaurants = Restaurant.query.filter(
        Restaurant.name.like(search)).all()
    relevant_dishes = Dish.query.filter(Dish.name.like(search)).all()

    # go_through_dishes = 0
    # go_through_restaurants = 0
    # number_of_relevant_restaurants = len(relevant_restaurants)
    # number_of_relevant_dishes = len(relevant_dishes)

    # while go_through_dishes < number_of_relevant_dishes and go_through_restaurants < number_of_relevant_restaurants:

    dishes_restaurant_id_set = set()
    relevant_results = list()

    for dish in relevant_dishes:
        dishes_restaurant_id_set.add(dish.restaurant_id)

    # for dish in relevant_dishes:
    #     print(dish.name, '\n')

    completed_dishes = list()
    left_out_restaurants = list()
    for restaurant in relevant_restaurants:
        if restaurant.id in dishes_restaurant_id_set:
            temp_dishes = [
                dish.name for dish in relevant_dishes if dish.restaurant_id == restaurant.id]
            completed_dishes += temp_dishes
            relevant_results += [(dish_name, restaurant.name)
                                 for dish_name in temp_dishes]

        else:
            left_out_restaurants.append((restaurant.name))

    for dish in relevant_dishes:
        if dish not in completed_dishes:
            relevant_results.append((dish.name))

    relevant_results += left_out_restaurants

    return jsonify(relevant_results)


@app.route('/purchase', methods=['POST'])
def customer_purchase():

    input_data = request.get_json(force=True)

    given_customer_id = input_data["customer_id"]
    given_dish_name = input_data["dish_name"]

    # with db.engine.connect() as connection:
    #     with connection.begin() as transaction:
    try:
        temp_purchase = PurchaseHistory()
        temp_purchase.customer_id = given_customer_id
        temp_purchase.transaction_date = str(datetime.now())

        temp_dish = Dish.query.filter_by(name=given_dish_name).first()
        temp_purchase.dish_id = temp_dish.id

        temp_customer = Customer.query.filter_by(
            id=given_customer_id).first()

        temp_customer.cash_balance -= temp_dish.price

        temp_restaurant = Restaurant.query.filter_by(
            id=temp_dish.restaurant_id).first()
        temp_restaurant.cash_balance += temp_dish.price

        db.session.add(temp_restaurant)
        db.session.add(temp_customer)
        db.session.commit()

    except:
        db.session.rollback()
        return "Transaction Unsuccessful"

    return "Transaction Successful"
