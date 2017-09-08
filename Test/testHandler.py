import ujson
import json
import tornado

from Database import user_database
from Handler.base import BaseHandler


class loginHandler(BaseHandler):
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        vip = user_database.findByUsername(username)
        if vip.password == password:
            self.session['username']= username
            self.session['password']= password
            data = ujson.dumps(dict(self.session.items()))
            self.write(data)
            self.render("../Template/index.html")
        else:
            self.render("../Template/login.html")
        #self.finish()


class indexHandler(tornado.web.RequestHandler):
    def get(self):
        data = ujson.dumps(dict(self.session.items()))
        self.write(data)
        self.finish()

# class homeHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render("../Template/login.html")

