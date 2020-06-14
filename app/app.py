import falcon
from resources import user, clothes
from services import database, image

from middlewares import (
   JsonMiddleware,
   AuthMiddleware
)

def create_app(conn, image):
    api = falcon.API(middleware=[JsonMiddleware(), AuthMiddleware()])

    user_resource = user.UserResource(conn, image)
    api.add_route('/users/{id}', user_resource, suffix='single')
    api.add_route('/users', user_resource)

    clothes_resource = clothes.ClothesResource(conn)
    api.add_route('/clothes/{id}', clothes_resource, suffix='single')
    api.add_route('/clothes', clothes_resource)
    return api

api = create_app(database.connect(), image.Image('images/.'))