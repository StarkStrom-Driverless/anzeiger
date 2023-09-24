from flask import Flask, render_template, jsonify
import datetime
from typing import List
from pyhafas import HafasClient
from pyhafas.profile import DBProfile
from pyhafas.types.fptf import Leg

app = Flask(__name__)

# Define the HafasClient outside of the index function
client = HafasClient(DBProfile())
@app.route('/')
def index():
    # Part 1

    # Part 2
    locations_haunstetterstr = client.locations("Augsburg Haunstetterstraße")
    best_found_location_haunstetterstr = locations_haunstetterstr[0] if locations_haunstetterstr else None

    # Part 3
    departures_haunstetterstr: List[Leg] = client.departures(
        station=best_found_location_haunstetterstr.id if best_found_location_haunstetterstr else None,
        date=datetime.datetime.now(),
        max_trips=20,
        products={
            'long_distance_express': True,
            'regional_express': True,
            'regional': True,
            'suburban': True,
            'bus': False,
            'ferry': True,
            'subway': True,
            'tram': False,
            'taxi': True
        }
    )

    # Fetch departures for Augsburg Sportanlage Süd P+R
    locations_sportanlage = client.locations("Augsburg Sportanlage Süd P+R")
    best_found_location_sportanlage = locations_sportanlage[0] if locations_sportanlage else None

    departures_sportanlage: List[Leg] = client.departures(
        station=best_found_location_sportanlage.id if best_found_location_sportanlage else None,
        date=datetime.datetime.now(),
        max_trips=20,
        products={
            'long_distance_express': True,
            'regional_express': True,
            'regional': True,
            'suburban': True,
            'bus': True,
            'ferry': True,
            'subway': True,
            'tram': True,
            'taxi': True
        }
    )

    return render_template('dashboard.html',
                           best_found_location=best_found_location_haunstetterstr,
                           departures_haunstetterstr=departures_haunstetterstr,
                           departures_sportanlage=departures_sportanlage)

if __name__ == '__main__':
    from waitress import serve

    serve(app, host='0.0.0.0', port=8080)