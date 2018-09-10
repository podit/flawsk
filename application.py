# Import Flask and a library to handle JSON responses
from flask import Flask, jsonify
# Import Flask-CORS to allow data to be used in web apps
from flask_cors import CORS
# Import libraries for JSON data handling and processing
import json
import os
import statistics as stat


# Display simple message at base url
def home():
    return '<h1>Flask AWS Application</h1><p>Python3.6 Flask application build for AWS</p>'


# Show different response when '/hi' is appended to the url
def hi():
    return 'Hello there...'


# Allow for calculation to demonstrate url inputs by raising a number to a power
def power(num, exp):
    pwr = num ** exp
    return str(pwr)


# Respond with raw JSON data for graphing (warning this is too much data and causes slow rendering on web end)
def jdata():
    time = []
    close = []
    fname = os.path.join(application.static_folder, 'jdat.json')
    with open(fname) as jdatr:
        data = json.load(jdatr)
        for item in data:
            time.append(item['<TIME>'])
            close.append(item['<CLOSE>'])
    return jsonify(time, close)


# Reponds with daily average of JSON data for CLOSE
# Probably a more nuanced solution for calculating averages should be used. This is a dev placeholder
def jdatdavg():
    fname = os.path.join(application.static_folder, 'jdat.json')
    x = 0
    time = []
    close = []
    close_avg = []
    with open(fname) as jdatr:
        data = json.load(jdatr)
        for item in data:
            if x < 6:
                x += 1
                close.append(float(item['<CLOSE>']))
            if x == 6:
                close.append(float(item['<CLOSE>']))
                closeav = stat.mean(close)
                time.append(item['<TIME>'])
                close_avg.append(closeav)
                x = 0
                close = []
    return jsonify(time, close_avg)


# Weekly close ('<CLOSE>') averages from JSON
def jdatwcavg():
    fname = os.path.join(application.static_folder, 'jdat.json')
    x = 0
    time = []
    close = []
    close_avg = []
    with open(fname) as jdatr:
        data = json.load(jdatr)
        for item in data:
            if x < 30:
                x += 1
                close.append(float(item['<CLOSE>']))
            if x == 30:
                close.append(float(item['<CLOSE>']))
                closeav = stat.mean(close)
                time.append(item['<TIME>'])
                close_avg.append(closeav)
                x = 0
                close = []
    return jsonify(time, close_avg)


# Reponds with weekly average of JSON data for CLOSE, OPEN, HIGH & LOW
def jdatwavg():
    # Set path to JSON file
    fname = os.path.join(application.static_folder, 'jdat.json')
    # Create values for recording output from JSON file
    x = 0
    time = []
    close = []
    opn = []
    high = []
    low = []
    close_avg = []
    opn_av = []
    high_av = []
    low_av = []
    # Open JSON file using filepath set earlier
    with open(fname) as jdatr:
        data = json.load(jdatr)
        # Iterate theough items in JSON file
        for item in data:
            # Iterate through each week (approximate) and record values
            if x < 30:
                x += 1
                close.append(float(item['<CLOSE>']))
                opn.append(float(item['<OPEN>']))
                high.append(float(item['<HIGH>']))
                low.append(float(item['<LOW>']))
            # At end of week record last values and calculate averages. Recording them in lists as well as the week time (approximate). Finally the iterator is reset and lists cleared to free up resources. These lists are returned as JSON objects with the jsonify function.
            if x == 30:
                close.append(float(item['<CLOSE>']))
                opn.append(float(item['<OPEN>']))
                high.append(float(item['<HIGH>']))
                low.append(float(item['<LOW>']))
                closeav = stat.mean(close)
                opnav = stat.mean(opn)
                highav = stat.mean(high)
                lowav = stat.mean(low)
                time.append(item['<TIME>'])
                close_avg.append(closeav)
                opn_av.append(opnav)
                high_av.append(highav)
                low_av.append(lowav)
                x = 0
                close = []
                opn = []
                high = []
                low = []
    return jsonify(time, close_avg, opn_av, high_av, low_av)


# Returns weekly average of volume ('<VOL>') data from JSON
def jdatvol():
    fname = os.path.join(application.static_folder, 'jdat.json')
    x = 0
    time = []
    vol = []
    vol_av = []
    with open(fname) as jdatr:
        data = json.load(jdatr)
        for item in data:
            if x < 30:
                x += 1
                vol.append(float(item['<VOL>']))
            if x == 30:
                vol.append(float(item['<VOL>']))
                volav = stat.mean(vol)
                time.append(item['<TIME>'])
                vol_av.append(volav)
                x = 0
                vol = []
    return jsonify(time, vol_av)


# Takes two dates and returns the data between them
def dates(sd, ed):
    fname = os.path.join(application.static_folder, 'jdat.json')
    t = 0
    time = []
    close = []
    with open(fname) as jdatr:
        data = json.load(jdatr)
        for item in data:
            if sd in item['<TIME>']:
                t = 1
            if ed in item['<TIME>']:
                t = 2
            if t == 1:
                time.append(item['<TIME>'])
                close.append(float(item['<CLOSE>']))
    return jsonify(time, close)


# Define the name of the application and set up CORS headers
application =  Flask(__name__)
CORS(application)

# Define urls as well as how they should be processed
application.add_url_rule('/', 'home', (lambda: home()))
application.add_url_rule('/hi', 'hi', (lambda: hi()))
# '/pwr' demonstrates how to pass values in the url
application.add_url_rule('/pwr/<int:num>/<int:exp>', 'power', (lambda num, exp: power(num, exp)))
# Calls functions for graph data requests
application.add_url_rule('/jdatdavg', 'jdatdavg', (lambda: jdatdavg()))
application.add_url_rule('/jdat', 'jdat', (lambda: jdata()))
application.add_url_rule('/jdatwavg', 'jdatwavg', (lambda: jdatwavg()))
application.add_url_rule('/jdatvol', 'jdatvol', (lambda: jdatvol()))
application.add_url_rule('/jdatwcavg', 'jdatwcavg', (lambda: jdatwcavg()))
application.add_url_rule('/dates/<sd>/<ed>', 'dates', (lambda sd, ed: dates(sd, ed)))

# Initialize and run the app. The if statement is required by AWS
if __name__ == "__main__":
    application.run(debug=True)

