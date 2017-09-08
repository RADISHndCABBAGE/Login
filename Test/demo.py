import os

import tornado
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

from Session.session import SessionManager
from Test.testHandler import loginHandler, indexHandler, homeHandler

temp_path = os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir))
template_path = os.path.join(temp_path, "Template")

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            cookie_secret="e446976943b4e8442f099fed1f3fea28462d5832f483a0ed9a3d5d3859f==78d",
            session_secret="3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
            session_timeout=600,
            store_options={
                'redis_host': 'localhost',
                'redis_port': 6379,

            },
        )
        handlers = [
            # (r"/home",  homeHandler),
            (r"/login", loginHandler),
            (r"/index", indexHandler)
        ]
        tornado.web.Application.__init__(self, handlers,cookie_secret='abcde')
        self.session_manager = SessionManager(settings["session_secret"], settings["store_options"], settings["session_timeout"])



define('port', default=8888, group='application')

if __name__ == "__main__":
    application = Application()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()