#################################################
# Import Dependencies
# Reference 10.3 Exercise #10
#################################################

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import datetime as dt
import datetime as dt
from datetime import datetime

from flask import Flask, jsonify

#################################################
# Database Setup
# Reference 10.3 Exercise #10
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

#################################################
# Set References to tables
# Reference 10.3 Exercise #1
#################################################
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Create session link
# Reference 10.3 Exercise #10
#################################################
session = Session(engine)

#################################################
# Flask Setup
# Reference 10.3 Exercise #10
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#Reference 10.3 Exercise #10
#################################################
@app.route("/")
def welcome():

# Determine first data point in database
   
    """List of all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query for the dates and temperature observations from the last year
    date_prcp = dt.datetime(2016, 8, 23)
    
    #Query data and create tuple
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > date_prcp).group_by(Measurement.date).order_by(Measurement.date).all()
    session.close()

    #Create dictionary
    prcp_data = dict(results)

    #Return JSON file
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    #Query data and create tuple
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    # Return JSON file
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Determine most recent data point
    # Use the strptime() method to create a datetime object from the given string.
    # Reference https://www.programiz.com/python-programming/datetime/strptime
    result = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    query_date = datetime.strptime(result,'%Y-%m-%d')

    # Calculate one year ago using timedelta
    # https://docs.python.org/3/library/datetime.html#datetime.timedelta
    year_ago = query_date - dt.timedelta(days=365)

    # Query temperature data for one year ago
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).filter(Measurement.date <= query_date).all()

    # Create dictionary of results
    all_tobs = dict(results)

    # Return jsonified dictionary
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    
    # Check if the date entered is available
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    # If not, return an error message
    if start > latest_date:
        return(f"No data is available for the date entered.  Please enter a date before {latest_date}.")

    # Query temperature data
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    summary = list(np.ravel(results))
    
    # Return results
    return(
        f"Minimum Temperature (Fahrenheit): {'{:.1f}'.format(summary[0])}<br/>"
        f"Average Temperature (Fahrenheit): {'{:.1f}'.format(summary[1])}<br/>"
        f"Maximum Temperature (Fahrenheit): {'{:.1f}'.format(summary[2])}"
        )


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):

     # Check if the date entered is available
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    # If not, return an error message
    if start > latest_date:
        return(f"No data is available for the date entered.  Please enter a date before {latest_date}.")

    # Check if the start is more recent than the start date
    start_date = session.query(Measurement.date).order_by(Measurement.date).first()[0]
    
    # If not, return an error message
    if end < start_date:
        return(f"No data is available for the date entered.  Please enter a date after {start_date}.")

    # Check if the start is before end date
    # If not, return an error message
    if start > end:
        return(f"<Please enter a start date that is before the end date.")

    # Query temperature data
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # Convert list of tuples into normal list
    summary = list(np.ravel(results))

    # Return results
    return(
        f"Minimum Temperature (Fahrenheit): {'{:.1f}'.format(summary[0])}<br/>"
        f"Average Temperature (Fahrenheit): {'{:.1f}'.format(summary[1])}<br/>"
        f"Maximum Temperature (Fahrenheit): {'{:.1f}'.format(summary[2])}"
        )

if __name__ == '__main__':
    app.run(debug=True)





