#coding=utf-8
from Session.session import Session

__author__ = 'karldoenitz'

import tornado.web



class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.session = Session(self.application.session_manager, self)