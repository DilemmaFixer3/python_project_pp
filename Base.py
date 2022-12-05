from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from pymysql import *


Base = declarative_base()
engine = create_engine("mysql+pymysql://root:mira0369B@localhost:3306/mydb02", echo=True)
Base.metadata.create_all(engine)