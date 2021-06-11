from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
basedir = os.path.abspath(os.path.dirname(__file__))

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cash_balance = Column(String)


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cash_balance = Column(String)


class Dish(Base):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    name = Column(String)
    price = Column(Float)


class OpeningHour(Base):
    __tablename__ = "Opening_hours"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    day = Column(String)
    open_time = Column(String)
    close_time = Column(String)


class PurchaseHistory(Base):
    __tablename__ = "purchase_history"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    dish_id = Column(Integer)
    transaction_date = Column(String)


# class Publisher(Base):
#     __tablename__ = "publisher"
#     publisher_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     authors = relationship(
#         "Author", secondary=author_publisher, back_populates="publishers"
#     )
#     books = relationship(
#         "Book", secondary=book_publisher, back_populates="publishers"
#     )

if __name__ == "__main__":

    sqlite_filepath = 'sqlite:///' + os.path.join(basedir, 'application.db')
    print(sqlite_filepath, '\n\n\n')
    engine = create_engine(f"{sqlite_filepath}")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    # customer = Customer(id=1,
    #                     name="John Snow",
    #                     cash_balance=22.2)
    # customer2 = Customer(id=2,
    #                      name="Karen",
    #                      cash_balance=14.5)

    # # session.add(customer)
    # session.add(customer2)
    # session.commit()
