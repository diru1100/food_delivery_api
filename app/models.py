from . import db


class Customer(db.Model):
    __table__ = db.Model.metadata.tables['customers']


class Restaurant(db.Model):
    __table__ = db.Model.metadata.tables['restaurants']


class PaymentHistory(db.Model):

    __table__ = db.Model.metadata.tables['purchase_history']


class Dish(db.Model):

    __table__ = db.Model.metadata.tables['dishes']


class OpeningHours(db.Model):

    __table__ = db.Model.metadata.tables['opening_hours']
