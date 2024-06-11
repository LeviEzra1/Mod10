# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Mea = Base.classes.measurement
Sta = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Test session
# print(session.query(Mea.station, Mea.date).limit(5).all())

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Rosutes
#################################################

@app.route("/")
def root():
    return (
        f"Available Routes:<br>"
        f"api/v1.0/precipitation<br>"
        f"api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/[start]<br>"
         f"/api/v1.0/[start]/[end]<br>"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():

    results = session.query(Mea.date, Mea.prcp).filter(Mea.date > "2016-08-23").order_by(Mea.date.desc()).all()
    all_perc = {}
    for date, prcp in results:
        all_perc[date] = prcp

    return jsonify(all_perc)



@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Sta.station).all()

    all_stations = []
    for station, in results:
        all_stations.append(station)

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Mea.date, Mea.tobs).filter(Mea.date > "2016-08-23").filter(Mea.station == 'USC00519281').all()

    all_tobs = []
    for date, tobs in results:
        all_tobs.append({"date": date, "tobs": tobs})

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def something(start, end="2017-08-23"):
    # query for the min, max and average temperature for all dates in start to end, exclusive
    results = session.query(func.min(Mea.tobs), func.max(Mea.tobs), func.avg(Mea.tobs)).filter(Mea.date >= start).filter(Mea.date <= end).all()

    # get list
    TMIN, TMAX, TAVG = results[0]
    all_data = {"TMIN": TMIN, "TAVG": TAVG, "TMAX": TMAX}

    # return jsonified list
    return jsonify(all_data)

if __name__ == "__main__":
    app.run(debug=True)