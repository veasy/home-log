import datetime
from flask import request
from iso8601 import iso8601
from homelog import config

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
    data = request.json

    with DataProvider() as ctx:
        latest = ctx.get_latest_log()
        current = datetime.datetime.fromtimestamp(int(data[config.TIME_STAMP]))

        # log only every 60 seconds
        if latest is None or (current - latest['observation']).seconds >= 60:
            ctx.add_log(data)
            print("data logged!")
    return 200


def get_dataset(start_time, end_time, instrument):
    with DataProvider() as ctx:
        return map(lambda x: x.get_record()[instrument], ctx.get_dataset(start_time, end_time, instrument))
