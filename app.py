from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/hotell'
db = SQLAlchemy(app)
migrate = Migrate(app, db)




class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_in_time = db.Column(db.DateTime, index=True)
    check_out_time = db.Column(db.DateTime, index=True)
    is_reserved = db.Column(db.Boolean, default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship('Customer')
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room')


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(64), index=True)


@app.route('/occupied_rooms', methods=['GET'])
def occupied_rooms():
    max_room = 10

    occupied_room = Reservation.query.filter_by(is_reserved='True').all()
    print(occupied_room)
    print(len(occupied_room))
    if not len(occupied_room) == 0:
        print(len(occupied_room), "rooms are available")
        return {len(occupied_room), "rooms are available"}
    return {'message': 'no rooms are available'}

    # if len(occupied_room) == 0:
    #
    #     return {'message': 'All the rooms are available'}
    #
    # elif len(occupied_room) < max_room:
    #     return {'message': 'rooms are available '}
    #
    # else:
    #     return {'message': 'no rooms are available'}



@app.route('/reservation',methods=['POST'])
def create_reservation():

        customer = Customer.query.filter_by(phone_number=request.form['phone_number']).first()
        if customer is None:
            customer = Customer(name=request.form['name'], phone_number=request.form['phone_number'])
            db.session.add(customer)
            db.session.commit()

        reservation = Reservation(check_in_time=request.form['check_in_time'], check_out_time=request.form['check_out_time'],
                                  customer_id=customer.id, room_id=request.form['room_id'], is_reserved=True)
        db.session.add(reservation)
        db.session.commit()
        reserv ={
            'name': customer.name,
            'date': reservation.check_in_time,
            'id':reservation.customer_id,
            'reserve':reservation.is_reserved

        }
        return {'user': reserv}


@app.route('/add_room', methods=['POST', 'GET'])
def add_room():

       room = Room(id=request.form['id'], room_type=request.form['room_type'])
       return{'room_id': room.id, 'room_type':room.room_type}


@app.route('/')
def index():
    return "hey"


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    occupied_rooms()






