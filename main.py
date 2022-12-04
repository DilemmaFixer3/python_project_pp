from flask import *
#from flask_mysql_connector import *

from waitress import serve
from sqlalchemy import create_engine

from pymysql import *
from models import *
from sqlalchemy.orm import relationship
from datetime import datetime
import bcrypt as bcrypt
from sqlalchemy import *
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from flask_swagger_ui import *
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import and_

app = Flask(__name__)

#SQLalchemy
engine = create_engine("mysql+pymysql://root:mira0369B@localhost:3306/mydb02", echo=True)
session = sessionmaker(bind=engine)
s = session()

ma = Marshmallow(app)
auth = HTTPBasicAuth()

#SwaggerUrL
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
#API_URL = '/docs/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Car Rental Service API'})   #поміняти назву
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

# для відловлення помилок при автентифікації
@app.errorhandler(401)
def handle_401_error(_error):
    return make_response(jsonify({'error': 'Unauthorised'}), 401)

@app.errorhandler(403)
def handle_403_error(_error):
    return make_response(jsonify({'error': 'Forbidden'}), 403)

@app.errorhandler(404)
def handle_404_error(_error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def handle_500_error(_error):
    return make_response(jsonify({'error': 'Server error'}), 500)

##########Schemas

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstName', 'lastName', 'email',
                  'username')


user_schema = UserSchema(many=False)
users_schema = UserSchema(many=True)

class CarSchema(ma.Schema):
    class Meta:
        fields = ('idcar', 'model',
                  'fuelConsumption',
                  'status')

car_schema = CarSchema(many=False)
cars_schema = CarSchema(many=True)


class RentalSchema(ma.Schema):
    class Meta:
        fields = ('idrental', 'startTime', 'endTime', 'price')


rental_schema = RentalSchema(many=False)
rentals_schema = RentalSchema(many=True)

@auth.get_user_roles
def get_user_role(user):
   return user.role

#User methods

@app.route("/user", methods=["POST"])
def createUser():
    try:
        id = request.json['id']
        firstName = request.json['firstName']
        lastName = request.json['lastName']
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        # password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        new_user = user(id=id, firstName=firstName, lastName=lastName,
                        email=email,
                        username = username,
                        password=password)

        s.add(new_user)
        s.commit()
        return user_schema.jsonify(new_user)

    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})


@app.route("/user/<int:id>", methods=["GET"])
def getUserById(id):
    user1 = s.query(user).filter(user.id == id).one()
    return user_schema.jsonify(user1)


# @app.route("/user/<int:id>", methods=["PUT"])
# def updateUserById(id):
#     user1 = s.query(user).filter(user.id == id).one()
#     username = user.username
#     current = auth.username()
#     if current != Username:
#         return Response(status=405, response='Access denied')
#     try:
#         carId = request.json['carId']
#         brand = request.json['brand']
#         model = request.json['model']
#         maxSpeed = request.json['maxSpeed']
#         yearProduction = request.json['yearProduction']
#         fuelConsumption = request.json['fuelConsumption']
#         seatsNumber = request.json['seatsNumber']
#         status = request.json['status']
#         RentalService_serviceId = request.json['serviceId']
#
#         car.carId = carId
#         car.brand = brand
#         car.model = model
#         car.maxSpeed = maxSpeed
#         car.yearProduction = yearProduction
#         car.fuelConsumption = fuelConsumption
#         car.seatsNumber = seatsNumber
#         car.status = status
#         car.RentalService_serviceId = RentalService_serviceId
#
#         s.commit()
#
#     except Exception as e:
#         return jsonify({"Error": "Invalid Request, please try again."})
#
#     return Car_schema.jsonify(car)