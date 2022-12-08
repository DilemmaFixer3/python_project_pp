from flask import *
from waitress import serve
from sqlalchemy import *
from models import *
from Base import engine
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from flask_swagger_ui import *
from sqlalchemy import and_

def create_app(test_config=None):
    global app
    app = Flask(__name__)
    return app

app = create_app()

# global app
# app = Flask(__name__)

#SQLalchemy
# Base = declarative_base()
# engine = create_engine("mysql+pymysql://root:mira0369B@localhost:3306/mydb02", echo=True)
# Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)
s = session()

ma = Marshmallow(app)
#auth = HTTPBasicAuth()

#SwaggerUrL
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Car Rental Service API'})   #поміняти назву
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)



@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response


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

# @auth.get_user_roles
# def get_user_role(user):
#    return user.role

#User methods

@app.route("/user/register", methods=["POST"])
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

@app.route("/user/deleteUser/<int:id>", methods=["DELETE"])
def deleteUser(id):
    user1 = s.query(user).filter(user.id == id).one()
    s.delete(user1)
    s.commit()
    return jsonify({"Success":"User deleted."})

@app.route("/user/editingUser/<int:id>", methods=["PUT"])
def updateUserById(id):
    user1 = s.query(user).filter(user.id == id).one()
    try:

        id = request.json['id']
        firstName = request.json['firstName']
        lastName = request.json['lastName']
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']


        user1.id = id
        user1.firstName = firstName
        user1.lastName = lastName
        user1.email = email
        user1.username = username
        user1.password = password

        s.commit()
    except Exception as e:
        return jsonify({"Error": "Invalid request, please try again."})

    return user_schema.jsonify(user1)

#Rental_methods

@app.route("/rental/create", methods=["POST"])
def createRental():
    try:
        idrental = request.json['idrental']
        startTime = request.json['startTime']
        endTime = request.json['endTime']
        price = request.json['price']
        user_id = request.json['user_id']
        car_idcar = request.json['car_idcar']

        new_rental = rental(idrental=idrental,
                        startTime=datetime.strptime(startTime, "%Y-%m-%d %H:%M"),
                        endTime=datetime.strptime(endTime, "%Y-%m-%d %H:%M"),
                        price=price,
                        user_id = user_id,
                        car_idcar=car_idcar)

        exists = s.query(rental).filter(and_(rental.startTime >=
                                             datetime.strptime(startTime, "%Y-%m-%d %H:%M"),
                                             rental.endTime <= datetime.strptime(endTime, "%Y-%m-%d %H:%M"),
                                             rental.car_idcar == car_idcar)).first() is not None

        dif = datetime.strptime(endTime, "%Y-%m-%d %H:%M") - datetime.strptime(startTime, "%Y-%m-%d %H:%M")

        if exists:
            return jsonify({"Error": "Car is already booked."})

        if datetime.strptime(startTime, "%Y-%m-%d %H:%M") >= datetime.strptime(endTime, "%Y-%m-%d %H:%M"):
            return jsonify({"Error": "Invalid date input"})

        s.add(new_rental)
        s.commit()
        return rental_schema.jsonify(new_rental)
    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})

@app.route("/rental/deleteRental/<int:idrental>", methods=["DELETE"])
def deleteRental(idrental):
    rental1 = s.query(rental).filter(rental.idrental == idrental).one()
    s.delete(rental1)
    s.commit()
    return jsonify({"Success":"Rental deleted."})

@app.route("/rental/editingRental/<int:idrental>", methods=["PUT"])
def updateRentalById(idrental):
    rental1 = s.query(rental).filter(rental.idrental == idrental).one()
    try:
        startTime = request.json['startTime']
        endTime = request.json['endTime']
        price = request.json['price']
        user_id = request.json['user_id']
        car_idcar = request.json['car_idcar']

        rental1.startTime=startTime
        rental1.endTime=endTime
        rental1.price =price
        rental1.user_id=user_id
        rental1.car_idcar=car_idcar

        s.commit()
    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})

    return rental_schema.jsonify(rental1)

@app.route("/rental/<startTime>/<endTime>/<int:car_idcar>", methods=["GET"])
def getRental():
    try:
        startTime = request.json['startTime']
        endTime = request.json['endTime']
        car_idcar = request.json['car_idcar']

        exists = s.query(rental).filter(and_(rental.startTime >= datetime.strptime(startTime, "%Y-%m-%d %H:%M"),
                                             rental.endTime <= datetime.strptime(endTime, "%Y-%m-%d %H:%M"),
                                             rental.car_idcar == car_idcar)).first() is not None

        if exists:
            return jsonify({"State": "Reserved"})
        else:
            return jsonify({"State": "Available"})

    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})

#Method_cars
@app.route("/cars/getList", methods=["GET"])
def getAllCars():
    cars = s.query(car).all()
    result_set = cars_schema.dump(cars)
    return jsonify(result_set)

#Method_car
@app.route("/cars/create", methods=["POST"])
def createCar():
    try:
        idcar = request.json['idcar']
        model = request.json['model']
        fuelConsumption = request.json['fuelConsumption']
        status = request.json['status']
        #user_id = request.json['user_id']
        # password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        new_car = user(idcar=idcar,
                       model=model,
                       fuelConsumption=fuelConsumption,
                        status=status
                       #,user_id = user_id
        )

        s.add(new_car)
        s.commit()
        return car_schema.jsonify(new_car)

    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})

@app.route("/car/<int:idcar>", methods=["GET"])
def getCarById(idcar):
    car1 = s.query(car).filter(car.idcar == idcar).one()
    return car_schema.jsonify(car1)

@app.route("/car/deleteCar/<int:idcar>", methods=["DELETE"])
def deleteCarById(idcar):
    car1 = s.query(car).filter(car.idcar == idcar).one()
    s.delete(car1)
    s.commit()
    return jsonify({"Success":"Car deleted."})

@app.route("/car/editingCar/<int:idcar>", methods=["PUT"])
def updateCarById(idcar):
    car1 = s.query(car).filter(car.idcar == idcar).one()
    try:
        model = request.json['model']
        fuelConsumption = request.json['fuelConsumption']
        status = request.json['status']
        user_id = request.json['user_id']

        car1.model=model
        car1.fuelConsumption=fuelConsumption
        car1.status =status
        car1.user_id=user_id

        s.commit()
    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})

    return car_schema.jsonify(car1)

if __name__=="__main__":
    #serve(app)
    app.run(debug=True)


#poetry run waitress-serve --listen=*:8000 main:app
#http://localhost:8000/swagger
#####http://127.0.0.1:5000/swagger/#/cars/getAllCars