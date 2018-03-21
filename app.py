# Import flask
from flask import Flask, render_template, url_for, request, jsonify, redirect
# Import bike_data.py
import bike_data as bd
# Convert month int to month string
import calendar as cal


# Create flask app
app = Flask(__name__)


# Web page
@app.route("/")
def main():
    # Renders home page with data-summary answers
    return render_template('index.html',
        max_start_month=bd.max_start_month,
        max_start_dow=bd.max_start_dow,
        max_start_hod=bd.max_start_hod,
        total_trip_duration=bd.total_trip_duration,
        avg_trip_duration=bd.avg_trip_duration,
        max_start_station=bd.max_start_station,
        max_end_station=bd.max_end_station,
        max_start_end_station=bd.max_start_end_station,
        customers=bd.customers,
        subscribers=bd.subscribers,
        males=bd.males,
        females=bd.females,
        by_oldest=bd.by_oldest,
        by_youngest=bd.by_youngest,
        by_popular=bd.by_popular
    )


# Helper function
def city_to_name(month_abbrev):
    if month_abbrev == 'chi':
        month = 'Chicago'
    elif month_abbrev == 'ny':
        month = 'New York City'
    elif month_abbrev == 'dc':
        month = 'Washington DC'
    return month


# Web page
@app.route("/data", methods=['GET', 'POST'])
def data():
    # POST requests
    if request.method == 'POST':
        city = request.form.get('city')
        month = request.form.get('month')
        dow = request.form.get('dow')
        data = bd.data_inquiry(city=city, month=month, dow=dow)
        return render_template('data.html',
            data=data
        )


# Check if this file is the main program
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # flash will use to create sessions for users.
    app.secret_key = 'super_secret_key'
    # Server reloads itself each time a load change,
    # and gives helpful debugger.
    app.debug = True
    # Run function used to run local server with application.
    # By default, server only accessible on host machine
    # But because using Vagrant, must change port to 0.0.0.0 to state that
    # web server should listen on all public IP Addresses
    # and make server publicly available
    app.run(host='0.0.0.0', port=5000)