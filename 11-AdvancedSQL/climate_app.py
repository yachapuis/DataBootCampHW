# 1. import libraries
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np

import datetime as dt

# 2. Setup Database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# 3. Create an app, being sure to pass __name__
app = Flask(__name__)

# 4. Setup Flask Routes
@app.route("/")
def homepage():
    """List of all returnable API routes."""
    return (
        f"<h1>Climate app</h1><br/><br/>"
        f"Available Routes:<br/>"
        """<a href= "/api/v1.0/precipitation">Precipitations in Hawaii for the last year: /api/v1.0/precipitation </a><br/>"""
        """<a href="/api/v1.0/stations">Names of stations in Hawaii for weather metrology: /api/v1.0/stations </a><br/>"""
        """<a href="/api/v1.0/tobs">Temperature observations in Hawaii for the previous year: /api/v1.0/tobs </a><br/>"""
        """<a href="/api/v1.0/2016-08-23">Temperature statistics in Hawaii from a given date: /api/v1.0/start </a><br/>"""
        """<a href="/api/v1.0/2016-08-23/2017-08-23">Temperature statistics within a start-end range of dates: /api/v1.0/start/end </a><br/>"""
)

# 5. Flask Route for precipitations
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Get date with last measurement data 
    measure_dates = session.query(Measurement).order_by(Measurement.date.desc()).limit(1)
    for date in measure_dates:
        last_measure_date = date.date
    
    # Calculate the date 1 year ago from today
    last_measure_date = dt.datetime.strptime(last_measure_date, "%Y-%m-%d") # Date convertion
    one_year_ago_date = last_measure_date - dt.timedelta(days=365)
    start = one_year_ago_date
    end = last_measure_date 
    
    # Query the dates and the precipitations from the last year
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= one_year_ago_date).\
            all()
    
    # Create a list of dictionaries
    dicts_prcp = []
    for data in prcp_data:
        dict_prcp = {}
        dict_prcp["date"] = data.date
        dict_prcp["prcp"] = data.prcp
        dicts_prcp.append(dict_prcp)
    
    # Return a JSON of the dates and precipitations
    return jsonify(dicts_prcp)

# 6. Flask Route for stations
@app.route("/api/v1.0/stations")
def stations():
   
   # Query for the stations from the dataset
    station_data = session.query(Station.name).all()
   
    # Convert list of tuples into a normal list
    stations_list = list(np.ravel(station_data))
    
    # Return a JSON of the stations 
    return jsonify(stations_list)

# 7. Flask Route for temperature observations
@app.route("/api/v1.0/tobs")
def tobs():
   
    # Query for the temperature observations for the previous year
    tobs_data = session.query(Measurement.tobs).all()
    
    # Convert list of tuples into a normal list
    tobs_list = list(np.ravel(tobs_data))
    
    # Return a JSON of the temperature observations
    return jsonify(tobs_data)

# 8. Flask Route for temperature statistics from a given start
@app.route("/api/v1.0/<start>")
def temps_start(start):
    
    # Query for calculating temperature statistics for a given start
    temps_start = session.query(func.min(Measurement.tobs),\
                    func.avg(Measurement.tobs),\
                    func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).\
                    all()
    
    # Convert list of tuples into normal list
    start_list = list(np.ravel(temps_start))
    
    # Create a dictionary using TMIN, TAVG, and TMAX as keys and temperature calculations as the respecive values. 
    for temp in start_list:
        start_dict = {}
        start_dict["TMIN"] = start_list[0]
        start_dict["TAVG"] = start_list[1]
        start_dict["TMAX"] = start_list[2]
    
    # Return a JSON of the temperature statistics
    return jsonify(start_dict)

# 9. Flask Route for temperature statistics from a start-end range
@app.route("/api/v1.0/<start>/<end>")
def temps_range(start, end):
    
    # Query for calculating temperature statistics within a start-end range 
    temps_start_end = session.query(func.min(Measurement.tobs), \
                         func.avg(Measurement.tobs), \
                         func.max(Measurement.tobs)).\
                            filter(Measurement.date >= start).\
                            filter(Measurement.date <= end).\
                            all()
    
    # Convert list of tuples into normal list
    start_end_list = list(np.ravel(temps_start_end))
    
    # Create a dictionary using TMIN, TAVG, and TMAX as keys and temperature calculations as the respecive values. 
    for temp in start_end_list:
        start_end_dict = {}
        start_end_dict["TMIN"] = start_end_list[0]
        start_end_dict["TAVG"] = start_end_list[1]
        start_end_dict["TMAX"] = start_end_list[2]
    
    # Return a JSON of the temperature statistics
    return jsonify(start_end_dict)

# 10. Run app
if __name__ == "__main__":
    app.run(debug=True)