import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask
app= Flask(__name__)

@app.route("/")
def welcome():
    return(f'''
        Available routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
        /api/v1.0/tobs
    ''')

@app.route("/api/v1.0/precipitation")
def prep():
    session=Session(engine)
    result = session.query(Measurement.date,Measurement.prcp).all()
    #aqui va el diccionario
    session.close() 

@app.route("/api/v1.0/stations")
def stat():
    session=Session(engine)
    result1 = session.query(Station.station).grouped_by(Station.station).all()
    session.close()
    return jsonify(result1)

@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    result2 = session.query(Measurements.date,Measurements.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date > '2016-08-18').all()
    session.close()
    return jsonify(result2)


if __name__=="__main__":
    app.run(debug=True)