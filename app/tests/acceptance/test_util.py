import jwt
import configparser
import os

def token():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = configparser.ConfigParser()

    config.read(dir_path + '/../../conf/config.ini')
    token = jwt.encode({'some': 'payload'}, config['auth']['secret'], algorithm='HS256')
    return token.decode('utf-8')