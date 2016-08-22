import datetime
from flask import request
from iso8601 import iso8601
from homelog import config

from homelog.data.data_provider import DataProvider
from homelog.data.data_utils import data_to_tuple, sub_sample, data_to_string


def get_temperature():
    start_time = iso8601.parse_date(request.args['startTime'])
    end_time = iso8601.parse_date(request.args['endTime'])
    sampling_rate = request.args.get('samplingRate', None)
    return get_dataset(start_time, end_time, 'temperature', sampling_rate=sampling_rate)


def get_pressure():
    start_time = iso8601.parse_date(request.args['startTime'])
    end_time = iso8601.parse_date(request.args['endTime'])
    sampling_rate = request.args.get('samplingRate', None)
    return get_dataset(start_time, end_time, 'pressure', sampling_rate=sampling_rate)


def get_humidity():
    start_time = iso8601.parse_date(request.args['startTime'])
    end_time = iso8601.parse_date(request.args['endTime'])
    sampling_rate = request.args.get('samplingRate', None)
    return get_dataset(start_time, end_time, 'humidity', sampling_rate=sampling_rate)


def get_luminosity():
    start_time = iso8601.parse_date(request.args['startTime'])
    end_time = iso8601.parse_date(request.args['endTime'])
    sampling_rate = request.args.get('samplingRate', None)
    return get_dataset(start_time, end_time, 'luminosity', sampling_rate=sampling_rate)


def get_wireless():
    start_time = iso8601.parse_date(request.args['startTime'])
    end_time = iso8601.parse_date(request.args['endTime'])
    sampling_rate = request.args.get('samplingRate', None)
    return get_dataset(start_time, end_time, 'wireless_strength', sampling_rate=sampling_rate)


def get_latest():
    with DataProvider() as ctx:
        return ctx.get_latest_log().get_record()


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


def get_dataset(start_time, end_time, instrument, sampling_rate=None):
    with DataProvider() as ctx:
        data = ctx.get_dataset(start_time, end_time, instrument)

        if sampling_rate is not None:
            return sub_sample(data_to_tuple(instrument, data), int(sampling_rate))
        else:
            return data_to_tuple(instrument, data)
