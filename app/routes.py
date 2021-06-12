from . import app, db
from .models import *
from flask import request, jsonify
from datetime import datetime
from sqlalchemy import and_


@app.route('/v1/open-restaurants', methods=['GET', 'POST'])
def open_restaurants():
    '''
        This API endpoint fetches restaurants that are available 
        at a certain datetime. 
        The logic followed is to extract the day using datetime object
        and respectively checking restaurants open at that day 
        with the time part of the datetime object.
    '''

    # converting given string into datetime object
    input_date_time = request.get_json(force=True)
    input_date_time = input_date_time['time']
    input_date_time = datetime.strptime(input_date_time, "%Y-%m-%d  %H:%M:%S")

    # extracting day from datetime object
    list_of_days = ['Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat', 'Sun']
    week_day_num = input_date_time.weekday()
    given_day = list_of_days[week_day_num]

    # extracting time string from datetime object
    given_time = str(datetime.time(input_date_time))

    # finding open hours of restaurants that fall under given given time
    matching_opening_hours_details = OpeningHour.query.filter(
        OpeningHour.day == given_day, OpeningHour.open_time <= given_time, OpeningHour.close_time >= given_time).all()

    restaurants_available_at_given_datetime = list()
    # collecting open restaurant names
    for opening_hour_details in matching_opening_hours_details:
        temp_restaurant = Restaurant.query.filter_by(
            id=opening_hour_details.restaurant_id).first()
        restaurants_available_at_given_datetime.append(temp_restaurant.name)

    return jsonify(restaurants_available_at_given_datetime)


@app.route('/v1/restaurants-with-budget-dishes', methods=['POST'])
def restaurants_with_budget_dishes():
    '''
        This API endpoint fetches top y(considered as limit), which has
        dishes more or less than x(taken as "do_not_have_dishes") and under the given
        price range.

    '''

    input_data = request.get_json(force=True)

    min_price = input_data["price_range"][0]
    max_price = input_data["price_range"][1]

    # fetch relevant details from database
    budget_dishes = Dish.query.filter(
        Dish.price >= min_price, Dish.price <= max_price).all()

    restaurants_with_budget_dishes = dict()
    set_of_restaurant_ids = set()

    for budget_dish in budget_dishes:

        set_of_restaurant_ids.add(budget_dish.restaurant_id)

    # Making a dictionary of restaurants detailswhich have budget dishes
    for restaurant_id in set_of_restaurant_ids:
        restaurants_with_budget_dishes[restaurant_id] = dict()
        restaurants_with_budget_dishes[restaurant_id]["restaurantName"] = Restaurant.query.filter_by(
            id=restaurant_id).first().name
        restaurants_with_budget_dishes[restaurant_id]["Dishes"] = list()
    for budget_dish in budget_dishes:
        temp_dish = {"name": budget_dish.name, "price": budget_dish.price}
        restaurants_with_budget_dishes[budget_dish.restaurant_id]["Dishes"].append(
            temp_dish)

    restaurants_with_given_criteria = list()
    for restaurant_id in set_of_restaurant_ids:
        dishes = len(restaurants_with_budget_dishes[restaurant_id]['Dishes'])
        if input_data["do_not_have_dishes"] != dishes:
            restaurants_with_given_criteria.append(
                restaurants_with_budget_dishes[restaurant_id]["restaurantName"])

    return jsonify(restaurants_with_given_criteria[:input_data["limit_of_results"]])


@app.route('/v1/search', methods=['POST'])
def search_data():
    ''' 
        This API endpoint seaches the relevant Dishes/Restaurant names 
        w.r.t the given input string. The precedence I followed in results is:
        1) Matches with Dishes + Restaurants
        2) Matches with Dishes 
        3) Matches with Restaurants
    '''
    input_data = request.get_json(force=True)

    # creating regex which machtes with anything containing given input as substring
    search = "%{}%".format(input_data["search_string"])

    # fetch relevant details from database
    relevant_restaurants = Restaurant.query.filter(
        Restaurant.name.like(search)).all()
    relevant_dishes = Dish.query.filter(Dish.name.like(search)).all()

    dishes_restaurant_id_set = set()
    relevant_results = list()
    # take restaurant ids from matched dishes in a set to exclude duplicates
    for dish in relevant_dishes:
        dishes_restaurant_id_set.add(dish.restaurant_id)

    completed_dishes = list()
    left_out_relevant_restaurants = list()

    for restaurant in relevant_restaurants:
        # checking if restaurant name is also matched on top of matching dish name
        if restaurant.id in dishes_restaurant_id_set:
            temp_dishes = [
                dish.name for dish in relevant_dishes if dish.restaurant_id == restaurant.id]
            completed_dishes += temp_dishes
            relevant_results += [(dish_name, restaurant.name)
                                 for dish_name in temp_dishes]

        else:
            left_out_relevant_restaurants.append((restaurant.name))

    # add left out matched dishes
    for dish in relevant_dishes:
        if dish not in completed_dishes:
            relevant_results.append((dish.name))
    #  at the end add left out matched restaurants
    relevant_results += left_out_relevant_restaurants

    return jsonify(relevant_results)


@app.route('/v1/purchase', methods=['POST'])
def customer_purchase():
    '''
        This API completes a transaction which reflects on consumer and restaurant 
        cashBalance in a transaction. If any exception occcurs the transaction is 
        rolledback to ensure safety.
    '''
    input_data = request.get_json(force=True)

    given_customer_id = input_data["customer_id"]
    given_dish_name = input_data["dish_name"]

    try:
        temp_purchase = PurchaseHistory()
        temp_purchase.customer_id = given_customer_id
        temp_purchase.transaction_date = str(datetime.now())

        # fetch relevant details from database
        temp_dish = Dish.query.filter_by(name=given_dish_name).first()
        temp_customer = Customer.query.filter_by(
            id=given_customer_id).first()
        temp_restaurant = Restaurant.query.filter_by(
            id=temp_dish.restaurant_id).first()

        temp_purchase.dish_id = temp_dish.id

        if temp_customer.cash_balance < temp_dish.price:
            return " Transaction Unsuccessful, insufficient balance: {} \n".format(temp_customer.cash_balance)

        # deducts money from customer account
        temp_customer.cash_balance -= temp_dish.price

        # deposits money to restaurant account
        temp_restaurant.cash_balance += temp_dish.price

        db.session.add(temp_restaurant)
        db.session.add(temp_customer)
        db.session.commit()

    except:
        db.session.rollback()
        return "Transaction Unsuccessful, Error during handling transaction"

    return "Transaction Successful, Purchase completed \n Customer Balance: {} \n".format(temp_customer.cash_balance)
