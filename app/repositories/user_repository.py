import falcon
import psycopg2 as pg

class UserRepository(object):
    def __init__(self, conn):
        self.conn = conn

    def upsert(self, q, values):
        try:
            cursor = self.conn.cursor()
            cursor.execute(q, tuple(values))
            self.conn.commit()

            id = cursor.fetchone()[0]
            return {"success":True, "message":"", "data":id}
        except pg.InternalError as e:
            conn.rollback()
            return {"success":False, "message":str(e), "data":None}

    def set_columns(self, data, cursor):
        items = []
        for x in data:
            item = {}
            c = 0
            for col in cursor.description:
                item.update({col[0]: x[c]})
                c = c + 1
            items.append(item)
        return items

    def list(self):
        try:
            cursor = self.conn.cursor()

            query = "SELECT * FROM Users ORDER BY id ASC"
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            return {"code": falcon.HTTP_200, "status":"success", "message":"users found!", "data":self.set_columns(records, cursor)}
        except Exception as error:
            return {"code": falcon.HTTP_500, "status":"error", "message":"exception: " + str(error), "data":None}

    def create(self, args):
        try:
            q = "INSERT INTO users(name) VALUES (%s) RETURNING id;"
            result = self.upsert(q, [args['name']])
            if result["success"]:
                return {"code": falcon.HTTP_201, "status":"success", "message":"user is added successfully!", "data":None}
            else:
                return {"code": falcon.HTTP_500, "status":"error", "message":"InternalError: " + result["message"], "data":None}
        except Exception as error:
            return {"code": falcon.HTTP_500, "status":"error", "message":"Exception: " + str(error), "data":None}

    def detail(self, id):
        try:
            cursor = self.conn.cursor()

            q = "SELECT * FROM users WHERE id = %s LIMIT 1"
            try:
                cursor.execute(q, [id])
                records = cursor.fetchone()
                if records is None:
                    return {"code": falcon.HTTP_404, "status":"error", "message":"user not found!", "data":None}
                else:
                    return {"code": falcon.HTTP_200, "status":"success", "message":"user found!", "data":dict(zip([c[0] for c in cursor.description], records))}
            except pg.InternalError as e:
                return {"code": falcon.HTTP_500, "status":"error", "message":"InternalError: " + str(e), "data":None}
        except Exception as error:
            return {"code": falcon.HTTP_500, "status":"error", "message":"Exception: " + str(error), "data":None}

    def delete(self, id):
        try:
            q = "DELETE FROM users WHERE id = %s"

            try:
                cursor = self.conn.cursor()
                cursor.execute(q, tuple([id]))
                self.conn.commit()
                return {"code": falcon.HTTP_200, "status":"success", "message":"user was deleted successfully!", "data":None}
            except pg.InternalError as e:
                conn.rollback()
                return {"code": falcon.HTTP_500, "status":"error", "message":"InternalError: " + str(e), "data":None}
        except Exception as error:
            return {"code": falcon.HTTP_500, "status":"error", "message":"Exception: " + str(error), "data":None}

    def update(self, args, id):
        try:
            cursor = self.conn.cursor()
            q = "SELECT id FROM users WHERE id = %s LIMIT 1"
            cursor.execute(q, [id])
            records = cursor.fetchone()
            if records is not None:
                q = "UPDATE users SET name=%s WHERE id=%s RETURNING  id;"
                result = self.upsert(q, [args['name'], id])
                if result["success"]:
                    return {"code": falcon.HTTP_201, "status":"success", "message":"user was updated successfully!", "data":None}
                else:
                    return {"code": falcon.HTTP_500, "status":"error", "message":"InternalError: " + result["message"], "data":None}
            else:
                return {"code": falcon.HTTP_404, "status":"error", "message":"user not found!", "data":None}
        except Exception as error:
            return {"code": falcon.HTTP_500, "status":"error", "message":"Exception: "+str(error), "data":None}

    def update_picture(self, filename, id):
        try:
            cursor = self.conn.cursor()
            q = "SELECT id FROM users WHERE id = %s LIMIT 1"
            cursor.execute(q, [id])
            records = cursor.fetchone()
            if records is not None:
                q = "UPDATE users SET picture=%s WHERE id=%s RETURNING  id;"
                result = self.upsert(q, [filename, id])
                if result["success"]:
                    return {"code": falcon.HTTP_201, "status":"success", "message":"picture was updated successfully!", "data":None}
                else:
                    return {"code": falcon.HTTP_500, "status":"error", "message":"InternalError: " + result["message"], "data":None}
            else:
                return {"code": falcon.HTTP_404, "status":"error", "message":"user not found!", "data":None}
        except Exception as error:
            return {"code": falcon.HTTP_500, "status":"error", "message":"Exception: "+str(error), "data":None}