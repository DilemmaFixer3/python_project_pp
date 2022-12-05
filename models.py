#from main import *
from Base import Base
import datetime

from sqlalchemy.orm import relationship

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum


class user(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    firstName = Column(String(45), nullable=False)
    lastName = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False)
    password = Column(Integer, nullable=False)  # додано для ідентифікації
    username = Column(String(45), nullable=False)  # додано для ідентифікації
    role = Column(Enum('user', 'admin'), nullable = False, default= 'user')
    rental = relationship("rental", overlaps="rental")

class car(Base):
    __tablename__ = 'car'
    idcar = Column(Integer(), primary_key=True)
    model = Column(String(45), nullable=False)
    fuelConsumption = Column(Integer(), nullable=False)
    status = Column(String(45), nullable=False)
    rental = relationship("rental", overlaps="rental")
    user_id = Column(Integer, ForeignKey('user.id'))


class rental(Base):
    __tablename__ = 'rental'
    idrental = Column(Integer(), primary_key=True)
    startTime = Column(DateTime(), default=datetime)
    endTime = Column(DateTime(), default=datetime)
    price = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("user", overlaps="rental")
    car_idcar = Column(Integer, ForeignKey('car.idcar'))
    car = relationship("car", overlaps="rental")
