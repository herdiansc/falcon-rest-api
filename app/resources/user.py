import falcon
from webargs import fields
from webargs.falconparser import use_args
import psycopg2 as pg
from repositories.user_repository import UserRepository 
from services.http import Http

class UserResource(object):
    def __init__(self, conn, image):
        self.conn = conn
        self.http = Http()
        self.user = UserRepository(conn)
        self.image = image

    def on_get(self, req, resp):
        result = self.user.list()
        self.http.responder(resp, result["code"], result["status"], result["message"], result["data"])

    @use_args({
        "name": fields.Str(required=True)
    })
    def on_post(self, req, resp, args):
        result = self.user.create(args)
        self.http.responder(resp, result["code"], result["status"], result["message"], result["data"])

    def on_get_single(self, req, resp, id):
        result = self.user.detail(id)
        self.http.responder(resp, result["code"], result["status"], result["message"], result["data"])

    def on_delete_single(self, req, resp, id):
        result = self.user.delete(id)
        self.http.responder(resp, result["code"], result["status"], result["message"], result["data"])

    @use_args({
        "name": fields.Str(required=True)
    })
    def on_put_single(self, req, resp, args, id):
        result = self.user.update(args, id)
        self.http.responder(resp, result["code"], result["status"], result["message"], result["data"])

    # @use_args({
    #     "picture": fields.Str(required=True)
    # })
    def on_patch_single(self, req, resp, id):
        filename = self.image.save(req.stream, req.content_type)
        result = self.user.update_picture(filename, id)
        self.http.responder(resp, result["code"], result["status"], result["message"], {"path":"/images/" + filename})