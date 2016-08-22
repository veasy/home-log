import datetime
from pg4nosql.PostgresNoSQLClient import PostgresNoSQLClient

from homelog import config


class DataProvider(object):
    def __init__(self):
        self.__pg4nosql = PostgresNoSQLClient(host=config.DB_HOST,
                                              user=config.DB_USER,
                                              password=config.DB_PASSWORD)
        self.__db_name = 'homelog'
        self.__data_table_name = 'data'

    def __enter__(self):
        self.db = self.__pg4nosql[self.__db_name]
        return self

    def __exit__(self, type, value, traceback):
        self.db.close()

    def create_schema(self):
        # data table
        self.db.get_or_create_table(self.__data_table_name,
                                    time='timestamp',
                                    observation='timestamp',
                                    wireless_strength='integer',
                                    luminosity='double precision',
                                    pressure='double precision',
                                    temperature='double precision',
                                    humidity='double precision')

    def add_log(self, data):
        table = self.db[self.__data_table_name]
        table.insert(time=datetime.datetime.now(),
                     observation=datetime.datetime.fromtimestamp(int(data[config.TIME_STAMP])).isoformat(),
                     wireless_strength=data[config.WIRELESS_STRENGTH].replace('%', ''),
                     luminosity=data[config.LIGHT_SENSOR],
                     pressure=data[config.METEO_PRESSURE],
                     temperature=data[config.METEO_TEMPERATURE],
                     humidity=data[config.METEO_HUMIDITY])

    def get_dataset(self, start_time, end_time, instrument='*'):
        table = self.db[self.__data_table_name]
        query = "'%s'<observation AND observation<'%s'" % (start_time, end_time)
        print(query)
        return table.query(query, '%s, %s' % ('observation', instrument))

    def get_latest_log(self):
        table = self.db[self.__data_table_name]
        return table.query_one('TRUE ORDER BY observation DESC LIMIT 1')
