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


@homelog_service_app.app.route('/plot/hour')
def plot_hour():
    with DataProvider() as ctx:
        data = ctx.get_dataset(datetime.datetime.now() - datetime.timedelta(hours=1),
                               datetime.datetime.now())[::2]

        temperature_data = get_chart_data('temperature', data)
        pressure_data = get_chart_data('pressure', data)
        humidity_data = get_chart_data('humidity', data)
        luminosity_data = get_chart_data('luminosity', data)

        return render_template('plot.html',
                               temperature_data=temperature_data,
                               pressure_data=pressure_data,
                               humidity_data=humidity_data,
                               luminosity_data=luminosity_data,
                               divisor=5)


@homelog_service_app.app.route('/plot')
def plot_day():
    with DataProvider() as ctx:
        data = ctx.get_dataset(datetime.datetime.now() - datetime.timedelta(days=1),
                               datetime.datetime.now())[::15]

        temperature_data = get_chart_data('temperature', data)
        pressure_data = get_chart_data('pressure', data)
        humidity_data = get_chart_data('humidity', data)
        luminosity_data = get_chart_data('luminosity', data)

        return render_template('plot.html',
                               temperature_data=temperature_data,
                               pressure_data=pressure_data,
                               humidity_data=humidity_data,
                               luminosity_data=luminosity_data,
                               divisor=5)


@homelog_service_app.app.route('/plot/week')
def plot_week():
    with DataProvider() as ctx:
        data = ctx.get_dataset(datetime.datetime.now() - datetime.timedelta(days=7),
                               datetime.datetime.now())[::120]

        temperature_data = get_chart_data('temperature', data)
        pressure_data = get_chart_data('pressure', data)
        humidity_data = get_chart_data('humidity', data)
        luminosity_data = get_chart_data('luminosity', data)

        return render_template('plot.html',
                               temperature_data=temperature_data,
                               pressure_data=pressure_data,
                               humidity_data=humidity_data,
                               luminosity_data=luminosity_data,
                               divisor=5)


@homelog_service_app.app.route('/plot/month')
def plot_month():
    with DataProvider() as ctx:
        data = ctx.get_dataset(datetime.datetime.now() - datetime.timedelta(days=30),
                               datetime.datetime.now())[::3600]

        temperature_data = get_chart_data('temperature', data)
        pressure_data = get_chart_data('pressure', data)
        humidity_data = get_chart_data('humidity', data)
        luminosity_data = get_chart_data('luminosity', data)

        return render_template('plot.html',
                               temperature_data=temperature_data,
                               pressure_data=pressure_data,
                               humidity_data=humidity_data,
                               luminosity_data=luminosity_data,
                               divisor=5)


def get_chart_data(field, data):
    return ',\n'.join(map(lambda x: "{ x: %s, y: %.2f }" % (
        int(time.mktime(x.get_record()['observation'].timetuple())), x.get_record()[field]), data))


if __name__ == '__main__':
    homelog_service_app.run(use_reloader=False)
