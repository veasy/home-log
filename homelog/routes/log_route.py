from flask import request

from homelog.data.data_provider import DataProvider


def get_temperature():
    return "hello world: temperature"


def post_raw():
    print("raw data logged")
    with DataProvider() as ctx:
        ctx.add_log(request.json)
    return 200
