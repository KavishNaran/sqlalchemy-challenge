# import Flask
from flask import Flask, jsonify

#Dependencies and Setup
import numpy as np
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPoo

#Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect database
Base = automap_base()
# Reflect the Tables
Base.prepare(engine, reflect=True)

#Save the references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session from Python to the database
session = Session(engine)

#Flask setup application
app = Flask(__name__)

 #Define what to do when a user hits the index route
@app.route("/")
def home():
    """List all available api routes avaliable for the user."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2017-06-20<br/>"
        f"/api/v1.0/2017-06-20/2017-06-28"
    )
#Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        
       #Calculate the Date 1 Year Ago from the Last Data Point in the Database
        data_year = dt.date(2017,8,23) - dt.timedelta(days=365)
        #Retrieve the last year of precipitation data selecting only the 'date' and 'prcp' values
        precipitation_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= data_year).\
                order_by(Measurement.date).all()
        #Convert List of Tuples Into a Dictionary
        precipitation_dictionary= dict(precipitation_data)
        #Return JSON Representation of Dictionary
        return jsonify(precipitation_dictionary)

@app.route("/api/v1.0/stations")
def stations():
        #Return a list of all the stations from the dataset
        station_data = session.query(Station.station, Station.name).all()
        #Convert list of tuples into List
        station_list = list(station_data)
        #Return JSON list of all the stations in the dataset
        return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
     #Calculate the Date 1 Year Ago from the Last Data Point in the Database
        year_data = dt.date(2017,8,23) - dt.timedelta(days=365)
        #Retrieve the Last 12 Months of date and prcp Precipitation Data
        tob_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= year_data).\
                order_by(Measurement.date).all()
        #Convert List of Tuples Into List
        tob = list(tob_data)
        #Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(tob)

@app.route("/api/v1.0/start")
def start(start_input):

    #Query all tobs
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_input).all()

    #Create a dictionary from the row data and append to a list of start_date_tobs
    start_date_tobs = []
    for min, avg, max in result:
        start_date_dict = {}
        start_date_dict["min_temp"] = min
        start_date_dict["avg_temp"] = avg
        start_date_dict["max_temp"] = max
        start_date_tobs.append(start_date_dict) 
    return jsonify(start_date_tobs)


@app.route("/api/v1.0/start/end")
def end(start_date, end_date):
    #Query all tobs
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
  
    #Create a dictionary from the row data and append to a list of start_end_date_tobs
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    

    return jsonify(start_end_tobs)


if __name__ == "__main__":
    app.run(debug=True)