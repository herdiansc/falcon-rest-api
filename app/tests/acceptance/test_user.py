import falcon
from falcon import testing
import unittest
from unittest.mock import MagicMock
import pytest
import app 
import json
from urllib.parse import urlencode

import jwt
import configparser
import os

@pytest.fixture
def mock_conn():
    return MagicMock()

@pytest.fixture
def mock_image():
    return MagicMock()

@pytest.fixture
def client(mock_conn, mock_image):
    api = app.create_app(mock_conn, mock_image)
    return testing.TestClient(api)

@pytest.fixture
def token():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = configparser.ConfigParser()

    config.read(dir_path + '/../../conf/config.ini')
    token = jwt.encode({'some': 'payload'}, config['auth']['secret'], algorithm='HS256')
    return token.decode('utf-8')

def test_list(client, token):
    content = {"status": "success", "message": "users found!", "data": []}

    response = client.simulate_get('/users', headers={'token':token})
    print(response.content)
    assert json.loads(response.content.decode('utf-8')) == content
    assert response.status == falcon.HTTP_200

def test_get_detail(client, token):
    content = {"status": "success", "message": "user found!", "data": {}}

    response = client.simulate_get('/users/1', headers={'token':token})
    assert json.loads(response.content.decode('utf-8')) == content
    assert response.status == falcon.HTTP_200

def test_create(client, token):
    content = {'status': 'success', 'message': 'user is added successfully!', 'data': None} 
    payload = json.dumps({"name":"herdian"}).encode('utf-8')

    response = client.simulate_post('/users', body=b'{"name":"herdian"}', headers={'content-type': 'application/json', 'token':token})
    assert json.loads(response.content.decode('utf-8')) == content
    assert response.status == falcon.HTTP_201

def test_update(client, token):
    content = {'status': 'success', 'message': 'user was updated successfully!', 'data': None} 
    payload = json.dumps({"name":"herdian"}).encode('utf-8')

    response = client.simulate_put('/users/1', body=b'{"name":"herdian"}', headers={'content-type': 'application/json', 'token':token})
    assert json.loads(response.content.decode('utf-8')) == content
    assert response.status == falcon.HTTP_201

def test_delete(client, token):
    content = {'status': 'success', 'message': 'user was deleted successfully!', 'data': None}

    response = client.simulate_delete('/users/1', headers={'token':token})
    assert json.loads(response.content.decode('utf-8')) == content
    assert response.status == falcon.HTTP_200