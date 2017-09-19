import json
import ujson
import tornado
from Database import user_database
from Handler.base import BaseHandler
from Utils.mylog import log


class loginHandler(BaseHandler):
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        vip = user_database.findByUsername(username)
        if vip.password == password:
            self.session['username']= username
            self.session['password']= password
            self.session.save()
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            self.write(ujson.dumps({"ok":"yes"}))
        else:
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            self.write(ujson.dumps({"ok":"no"}))


class indexHandler(BaseHandler):
    def get(self):
        data = json.dumps(dict(self.session.items()))
        log.info(data)
        self.write(data)
        self.finish()


class Handler(tornado.web.RequestHandler):
    def get(self):
        print(self.get_cookie("session_id"))


