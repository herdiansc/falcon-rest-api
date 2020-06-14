class Http(object):
    def responder(self, resp, code, status, msg, data):
        resp.status = code
        resp.body = {"status": status, "message": msg, 'data': data}