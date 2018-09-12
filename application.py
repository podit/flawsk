# Import Flask and a library to handle JSON responses
from flask import Flask, jsonify
# Import Flask-CORS to allow data to be used in web apps
from flask_cors import CORS
# Import libraries for JSON data handling and processing
import json
import os
import statistics as stat
import gviz_api
import collections


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
    fname = os.path.join(application.static_folder, 'jdat.json')
    close = []
    obj = []
    with open(fname) as jdatr:
        data = json.load(jdatr)
        for item in data:
            d = collections.OrderedDict()
            d['time'] = item['<TIME>']
            d['open'] = float(item['<OPEN>'])
            d['high'] = float(item['<HIGH>'])
            d['low'] = float(item['<LOW>'])
            d['vol'] = float(item['<VOL>'])
            d['close'] = item['<CLOSE>']
            obj.append(d)
    return jsonify(obj)


# Reponds with daily average of JSON data for CLOSE
# Probably a more nuanced solution for calculating averages should be used. This is a dev placeholder
def jdatdavg():
    fname = os.path.join(application.static_folder, 'jdat.json')
    x = 0
    close = []
    obj = []
    with open(fname) as jdatr:
        data = json.load(jdatr)
        for item in data:
            d = collections.OrderedDict()
            if x < 6:
                x += 1
                close.append(float(item['<CLOSE>']))
            if x == 6:
                close.append(float(item['<CLOSE>']))
                closeav = stat.mean(close)
                d['time'] = item['<TIME>']
                d['close'] = closeav
                obj.append(d)
                x = 0
                close = []
    return jsonify(obj)


# Weekly close ('<CLOSE>') averages from JSON
def jdatwcavg():
    fname = os.path.join(application.static_folder, 'jdat.json')
    x = 0
    close = []
    obj = []
    with open(fname) as jdatr:
        data = json.load(jdatr)
        for item in data:
            d = collections.OrderedDict()
            if x < 29:
                x += 1
                close.append(float(item['<CLOSE>']))
            if x == 29:
                close.append(float(item['<CLOSE>']))
                d['close'] = stat.mean(close)
                d['time'] = item['<TIME>']
                obj.append(d)
                x = 0
                close = []
    return jsonify(obj)


#=========================GVIZ function========================#
def j():
    fname = os.path.join(application.static_folder, 'jdat.json')
    x = 0
    close = []
    opn = []
    high = []
    low = []
    #vol = []
    obj = []
    description = {"time":("string","DaTi"),
            "low":("number","Low"),
            "open":("number","Open"),
            "close":("number","Close"),
            "high":("number","High")}
    with open(fname) as jdatr:
        data = json.load(jdatr)
        for item in data:
            d = collections.OrderedDict()
            if x < 5:
                x += 1
                close.append(float(item['<CLOSE>']))
                opn.append(float(item['<OPEN>']))
                high.append(float(item['<HIGH>']))
                low.append(float(item['<LOW>']))
                #vol.append(float(item['<VOL>']))
            if x == 5:
                close.append(float(item['<CLOSE>']))
                opn.append(float(item['<OPEN>']))
                high.append(float(item['<HIGH>']))
                low.append(float(item['<LOW>']))
                #vol.append(float(item['<VOL>']))
                closeav = stat.mean(close)
                opnav = stat.mean(opn)
                highav = stat.mean(high)
                lowav = stat.mean(low)
                #volav = stat.mean(vol)
                d['time'] = item['<TIME>']
                d['low'] = lowav
                d['open'] = opnav
                d['close'] = closeav
                d['high'] = highav
                obj.append(d)
                x = 0
                time = []
                close = []
                opn = []
                high = []
                low = []
                #vol = []
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(obj)
    return data_table.ToJSon(columns_order=("time", "low", "open", "close", "high"), order_by="time")


# Reponds with weekly average of JSON data for CLOSE, OPEN, HIGH & LOW
def jdatwavg():
    # Set path to JSON file
    fname = os.path.join(application.static_folder, 'jdat.json')
    # Create values for recording output from JSON file
    x = 0
    close = []
    opn = []
    high = []
    low = []
    vol = []
    obj = []
    # Open JSON file using filepath set earlier
    with open(fname) as jdatr:
        data = json.load(jdatr)
        # Iterate theough items in JSON file
        for item in data:
            d = collections.OrderedDict()
            # Iterate through each week (approximate) and record values
            if x < 29:
                x += 1
                close.append(float(item['<CLOSE>']))
                opn.append(float(item['<OPEN>']))
                high.append(float(item['<HIGH>']))
                low.append(float(item['<LOW>']))
                vol.append(float(item['<VOL>']))
            # At end of week record last values and calculate averages. Recording them in lists as well as the week time (approximate). Finally the iterator is reset and lists cleared to free up resources. These lists are returned as JSON objects with the jsonify function.
            if x == 29:
                close.append(float(item['<CLOSE>']))
                opn.append(float(item['<OPEN>']))
                high.append(float(item['<HIGH>']))
                low.append(float(item['<LOW>']))
                vol.append(float(item['<VOL>']))
                d['close'] = stat.mean(close)
                d['open'] = stat.mean(opn)
                d['high'] = stat.mean(high)
                d['low'] = stat.mean(low)
                d['vol'] = stat.mean(vol)
                d['time'] = item['<TIME>']
                obj.append(d)
                x = 0
                close = []
                opn = []
                high = []
                low = []
                vol = []
    return jsonify(obj)


# Returns weekly average of volume ('<VOL>') data from JSON
def jdatvol():
    fname = os.path.join(application.static_folder, 'jdat.json')
    x = 0
    vol = []
    obj = []
    with open(fname) as jdatr:
        data = json.load(jdatr)
        for item in data:
            d = collections.OrderedDict()
            if x < 29:
                x += 1
                vol.append(float(item['<VOL>']))
            if x == 29:
                vol.append(float(item['<VOL>']))
                d['vol'] = stat.mean(vol)
                d['time'] = item['<TIME>']
                obj.append(d)
                x = 0
                vol = []
    return jsonify(obj)


# Takes two dates and returns the data between them
def dates(sd, ed):
    fname = os.path.join(application.static_folder, 'jdat.json')
    t = 0
    obj = []
    with open(fname) as jdatr:
        data = json.load(jdatr)
        for item in data:
            d = collections.OrderedDict()
            if sd in item['<TIME>']:
                t = 1
            if ed in item['<TIME>']:
                t = 2
            if t == 1:
                d['time'] = item['<TIME>']
                d['open'] = float(item['<OPEN>'])
                d['high'] = float(item['<HIGH>'])
                d['low'] = float(item['<LOW>'])
                d['vol'] = float(item['<VOL>'])
                d['close'] = float(item['<CLOSE>'])
                obj.append(d)
    return jsonify(obj)


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
application.add_url_rule('/j', 'j', (lambda: j()))

# Initialize and run the app. The if statement is required by AWS
if __name__ == "__main__":
    application.run(debug=True)

