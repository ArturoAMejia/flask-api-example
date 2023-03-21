from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
app = Flask(__name__)

load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy()

class Flight(db.Model):
    __tablename__ = "flights"
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)


class Passenger(db.Model):
    __tablename__ = "passengers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)

db.init_app(app)



@app.route('/flight/<int:id>', methods=['GET'])
def index(id):
    flights = db.session.query(Flight).filter_by(id=id).first()

    return jsonify({'origin': flights.origin, "destination": flights.destination, "duration": flights.duration})


@app.route('/flight/', methods=["POST"])
def flight():

    print(request.json)
    origin= request.json["origin"]
    destination= request.json["destination"]
    duration= request.json["duration"]
    
    f = Flight(origin=origin, destination=destination, duration=duration)
    db.session.add(f)
    db.session.commit()

    return jsonify({"message": "Vuelo creado exitosamente!"}), 201


@app.route('/flight/<int:id>', methods=["PUT"])
def update_flight(id):

    f = db.session.query(Flight).filter_by(id=id).first()

    origin= request.json["origin"]
    destination= request.json["destination"]
    duration= request.json["duration"]

    f.origin = origin
    f.destination = destination
    f.duration = duration

    db.session.commit()

    
    return jsonify({"message": "Vuelo actualizado exitosamente!"}), 200


@app.route('/flight/<int:id>', methods=["DELETE"])
def delete_flight(id):

    f = db.session.query(Flight).filter_by(id=id).first()

    db.session.delete(f)

    db.session.commit()

    
    return jsonify({"message": "Vuelo borrado exitosamente!"}), 200


    