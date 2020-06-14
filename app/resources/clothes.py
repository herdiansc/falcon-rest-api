import falcon
from webargs import fields
from webargs.falconparser import use_args
import psycopg2 as pg
from repositories.clothes_repository import ClothesRepository 
from services.http import Http

class ClothesResource(object):
    def __init__(self, conn):
        self.conn = conn
        self.http = Http()
        self.clothes = ClothesRepository(conn)

    def on_get(self, req, resp):
        result = self.clothes.list()
        self.http.responder(resp, result["code"], result["status"], result["message"], result["data"])

    @use_args({
        "name": fields.Str(required=True),
        "email": fields.Str(required=True),
        "size": fields.Str(required=True)
    })
    def on_post(self, req, resp, args):
        result = self.clothes.create(args)
        self.http.responder(resp, result["code"], result["status"], result["message"], result["data"])

    def on_get_single(self, req, resp, id):
        result = self.clothes.detail(id)
        self.http.responder(resp, result["code"], result["status"], result["message"], result["data"])

    def on_delete_single(self, req, resp, id):
        result = self.clothes.delete(id)
        self.http.responder(resp, result["code"], result["status"], result["message"], result["data"])

    @use_args({
        "name": fields.Str(required=True),
        "email": fields.Str(required=True),
        "size": fields.Str(required=True)
    })
    def on_put_single(self, req, resp, args, id):
        result = self.clothes.update(args, id)
        self.http.responder(resp, result["code"], result["status"], result["message"], result["data"])