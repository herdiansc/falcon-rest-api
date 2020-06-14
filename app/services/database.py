import psycopg2
import configparser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()

config.read(dir_path + '/../conf/config.ini')


def connect():
    try:
        connection = psycopg2.connect(user=config['postgresqlDB']['user'],
                                      password=config['postgresqlDB']['pass'],
                                      host=config['postgresqlDB']['host'],
                                      port="5432",
                                      database=config['postgresqlDB']['db'])
        print("You are connected!")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)