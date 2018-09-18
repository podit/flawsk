Python3.6 Flask API configured for AWS
=====================================

Uses [Flask](https://github.com/pallets/flask)
- A Python micro framework for web applications.

Configuration
-------------

Should also work with other versions of python3.3+.

- Python version 3.6 was used initially but 3.7 was used in final development. Previous versions of 3.3+ should work although I doubt 2.7 would work.

I would advise a virtual environment to host the flask server.

- Installing required packages:
	- Flask `pip install flask`
	- Flask CORS headers `pip install flask-cors`
		- This handles API requests from javascript.
    - [Goodle Visualizaition API](https://github.com/google/google-visualization-python) `pip install gviz_api`
        - Allows for JSON outputs to be configured for Google Charts

Alternatively the 'requirements.txt' lists all individual dependencies and their versions.

Usage
-----

The 'application.py' script is the flask application and currently has no external file dependencies. To run use the command:

- `python application.py`

The application will be hosted at:

- `http://127.0.0.1:5000/`

- Additional responses can be accessed by appending information to the host url:
	- `/hi` will give the response: 'Hello there...'
	- `/pwr/<num>/<exp>` will respond with `<num>` raised to the power `<exp>`.

AWS
---

To implement this on AWS I would reccomend using [EBCLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html) (the AWS Elastic Beanstalk Command Line Interface).

The application is already configured for Elastic Beanstalk (EB) deployment. However these settings may possibly not be transferable. Either way it is configured for AWS deployment and so initializing an EB environment should be fast and painless.

Additional files
----------------

The 'frontend.html' file is a testbase for more advanced API features.

- Warning this file is now depreciated see the [frontend](https://github.com/podit/flawsk-web) repo for the updated version.

The 'jsonify.py' script is used to convert .csv files into .json for more flexibility in data usage.

- Warning that the jsonify.py script currently requires python2.7
