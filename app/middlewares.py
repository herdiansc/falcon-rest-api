import falcon
import json
from datetime import date, datetime
import jwt

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        if isinstance(obj, (date, datetime)):
            return str(obj.isoformat())
        return super(JSONEncoder, self).default(obj)


class JsonMiddleware(object):
    def process_response(self, req, resp, _, req_succeeded):
        if not req_succeeded:
            return
        if req.client_accepts_json:
            resp.set_header('Content-Type', 'application/json')
            resp.body = json.dumps(resp.body, cls=JSONEncoder)

class AuthMiddleware(object):
    def process_request(self, req, resp):
        try:
            token_content = jwt.decode(req.headers["TOKEN"], 'secret', algorithms=['HS256'])
        except:
            raise falcon.HTTPUnauthorized()