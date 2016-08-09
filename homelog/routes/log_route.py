from flask import request
from iso8601 import iso8601

from homelog.data.data_provider import DataProvider


def get_temperature():
    start_time = iso8601.parse_date(request.args['startTime'])
    end_time = iso8601.parse_date(request.args['endTime'])
    return get_dataset(start_time, end_time, 'temperature')


def get_pressure():
    start_time = iso8601.parse_date(request.args['startTime'])
    end_time = iso8601.parse_date(request.args['endTime'])
    return get_dataset(start_time, end_time, 'pressure')


def get_humidity():
    start_time = iso8601.parse_date(request.args['startTime'])
    end_time = iso8601.parse_date(request.args['endTime'])
    return get_dataset(start_time, end_time, 'humidity')


def post_raw():
    print("raw data logged")
    with DataProvider() as ctx:
        ctx.add_log(request.json)
    return 200


def get_dataset(start_time, end_time, instrument):
    with DataProvider() as ctx:
        return map(lambda x: x.get_record()[instrument], ctx.get_dataset(start_time, end_time, instrument))
