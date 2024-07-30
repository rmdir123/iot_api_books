from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Student(Base):
    __tablename__ = 'students'

    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)
    dob = Column(String, index=True)
    gender = Column(String, index=True)

class Coffee(Base):
    __tablename__ = 'coffee'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(String, index=True)
    order_coffees = relationship("OrderCoffee", back_populates="coffee")

class Order(Base):
    __tablename__ = 'order'
    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_coffees = relationship("OrderCoffee", back_populates="order")

class OrderCoffee(Base):
    __tablename__ = 'order_coffee'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.order_id'), index=True)
    coffee_id = Column(Integer, ForeignKey('coffee.id'), index=True)
    quantity = Column(Integer, index=True)
    total = Column(Integer, index=True)
    order = relationship("Order", back_populates="order_coffees")
    coffee = relationship("Coffee", back_populates="order_coffees")
