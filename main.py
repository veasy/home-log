import os
import json
import logging

import connexion
import datetime

from flask import render_template
from flask.ext.compress import Compress
from flask.ext.cors import CORS

from homelog import config
from homelog.data.data_provider import DataProvider
from homelog.data.data_utils import data_to_string, sub_sample, data_to_tuple
from homelog.service_response import ServiceResponse

import time


def all_exception_handler(error):
    print('Error: %s' % error)
    return json.dumps({'message': error.message}), 500


def start_server():
    logging.basicConfig(level=logging.INFO)

    print("starting server...")
    app = connexion.App(
        __name__,
        port=config.WEBSERVICE_PORT,
        specification_dir='homelog/swagger/',
        debug=True
    )

    # set own default response class
    # to support direct passthrough
    app.app.response_class = ServiceResponse

    app.add_api('api.yaml')

    app.debug = True

    Compress(app.app)
    CORS(app.app)

    # add error handler
    if not bool(os.environ.get("DEBUG", 1)):
        app.app.register_error_handler(Exception, all_exception_handler)

    with DataProvider() as ctx:
        ctx.create_schema()

    return app


# uwsgi app variable
homelog_service_app = start_server()
application = homelog_service_app.app


def plot(rate, delta, divisor, time_format):
    with DataProvider() as ctx:
        data = ctx.get_dataset(datetime.datetime.now() - delta,
                               datetime.datetime.now())

        temperature_data = data_to_string(sub_sample(data_to_tuple('temperature', data), rate))
        pressure_data = data_to_string(sub_sample(data_to_tuple('pressure', data), rate))
        humidity_data = data_to_string(sub_sample(data_to_tuple('humidity', data), rate))
        luminosity_data = data_to_string(sub_sample(data_to_tuple('luminosity', data), rate))

        return render_template('plot.html',
                               temperature_data=temperature_data,
                               pressure_data=pressure_data,
                               humidity_data=humidity_data,
                               luminosity_data=luminosity_data,
                               divisor=divisor,
                               time_format=time_format)


@homelog_service_app.app.route('/plot/hour')
def plot_hour():
    return plot(2, datetime.timedelta(hours=1), 5, 'HH:mm:ss')


@homelog_service_app.app.route('/plot')
def plot_day():
    return plot(15, datetime.timedelta(days=1), 5, 'ddd HH:mm')


@homelog_service_app.app.route('/plot/week')
def plot_week():
    return plot(120, datetime.timedelta(days=7), 5, 'ddd DD MMM YY')


@homelog_service_app.app.route('/plot/month')
def plot_month():
    return plot(3600, datetime.timedelta(days=30), 5, 'ddd DD MMM YY')


if __name__ == '__main__':
    homelog_service_app.run(use_reloader=False)
