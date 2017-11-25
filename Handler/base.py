import pyrestful.rest

from Utils.session import Session

import tornado.web


'''
class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.session = Session(self.application.session_manager, self)
'''
class BaseHandler(pyrestful.rest.RestHandler):
    def __init__(self,*args,**kargs):
        super(BaseHandler,self).__init__(*args,**kargs)
        self.session = Session(self.application.session_manager,self)
        print(self.application.session_manager)