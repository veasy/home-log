import os
import json
import logging

import connexion
from flask.ext.compress import Compress
from flask.ext.cors import CORS

from homelog import config
from homelog.data.data_provider import DataProvider
from homelog.service_response import ServiceResponse


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
ecallisto_service_app = start_server()
application = ecallisto_service_app.app

if __name__ == '__main__':
    ecallisto_service_app.run(use_reloader=False)
