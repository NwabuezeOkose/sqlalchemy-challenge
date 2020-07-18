import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy.orm import create_engine, func

from sqlalchemy import Flask, jsonify

import datetime as dt


##############################
# Database Setup
##############################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/<end>" 
    )


#################################################
# For Precipitation
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    my_max_date = dt.date(2017, 8, 23)
    one_year_ago = my_max_date - dt.timedelta(days=365)

    past_temp = (session.query(Measurement.date, Measurement.prcp)
                .filter(Measurement.date <= my_max_date)
                .filter(Measurement.date >= one_year_ago)
                .order_by(Measurement.date).all())
    
    precipitation = {date: precip for date, precip in past_temp}

    return jsonify(precipitation)
    
#################################################
# For Stations
#################################################
@app.route("/api/v1.0/stations")
def stations():

    all_stations = session.query(Station.station).all()

    return jsonify(all_stations)


#################################################
# For tobs
#################################################
@app.route("/api/v1.0/tobs")
def precipitation():
    # Create our session (link) from Python to the DB
    my_max_date = dt.date(2017, 8, 23)
    one_year_ago = my_max_date - dt.timedelta(days=365)

    lastyear = (session.query(Measurement.tobs)
                .filter(Measurement.station=='USC00519281')
                .filter(Measurement.date <= my_max_date)
                .filter(Measurement.date <= one_year_ago)
                .order_by(Measurement.tobs).all())
    
    return jsonify(lastyear)


#################################################
# For start
#################################################
@app.route("/api/v1.0/<start>")
def start():
    only_tobs = (session.query(Measurement.tobs).filter(Measurement.date.between(start, '2017-08-23')).all())

    temp_obs_df = pd.DataFrame(only_tobs)

    tavg = temp_obs_df["tobs"].mean()
    tmin = temp_obs_df["tobs"].min()
    tmax = temp_obs_df["tobs"].max()
    
    return jsonify(tavg, tmin, tmax)

#################################################
# For start & end
#################################################
@app.route("/api/v1.0/<start>/<end>")
def startend(start=None, end=None):
    only_tobs = (session.query(Measurement.tobs).filter(Measurement.date.between(start, end)).all())

    temp_obs_df = pd.DataFrame(only_tobs)

    tavg = temp_obs_df["tobs"].mean()
    tmin = temp_obs_df["tobs"].min()
    tmax = temp_obs_df["tobs"].max()
    
    return jsonify(tavg, tmin, tmax)


if __name__ == '__main__':
    app.run(debug=True)
