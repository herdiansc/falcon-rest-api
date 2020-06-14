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
    content = {"status": "success", "message": "clothes found!", "data": []}

    response = client.simulate_get('/clothes', headers={'token': token})
    assert json.loads(response.content.decode('utf-8')) == content
    assert response.status == falcon.HTTP_200

def test_get_detail(client, token):
    content = {"status": "success", "message": "clothes found!", "data": {}}

    response = client.simulate_get('/clothes/1', headers={'token': token})
    assert json.loads(response.content.decode('utf-8')) == content
    assert response.status == falcon.HTTP_200

def test_create(client, token):
    content = {'status': 'success', 'message': 'clothes is added successfully!', 'data': None} 
    payload = b'{"name":"herdian", "email":"herdian@mail.com","size":"S"}'

    response = client.simulate_post('/clothes', body=payload, headers={'content-type': 'application/json', 'token': token})
    assert json.loads(response.content.decode('utf-8')) == content
    assert response.status == falcon.HTTP_201

    content = {'errors': {'json': {'name': ['Missing data for required field.'], 'email': ['Missing data for required field.'], 'size': ['Missing data for required field.']}}, 'title': '422 Unprocessable Entity'} 
    payload = b'{}'

    response = client.simulate_post('/clothes', body=payload, headers={'content-type': 'application/json', 'token': token})
    assert json.loads(response.content.decode('utf-8')) == content
    assert response.status == falcon.HTTP_422

def test_update(client, token):
    content = {'status': 'success', 'message': 'clothes was updated successfully!', 'data': None} 
    payload = b'{"name":"herdian", "email":"herdian@mail.com","size":"S"}'

    response = client.simulate_put('/clothes/1', body=payload, headers={'content-type': 'application/json', 'token': token})
    assert json.loads(response.content.decode('utf-8')) == content
    assert response.status == falcon.HTTP_201

def test_delete(client, token):
    content = {'status': 'success', 'message': 'clothes was deleted successfully!', 'data': None}

    response = client.simulate_delete('/clothes/1', headers={'token': token})
    assert json.loads(response.content.decode('utf-8')) == content
    assert response.status == falcon.HTTP_200