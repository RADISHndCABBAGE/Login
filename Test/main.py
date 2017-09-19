import tornado
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

from Utils.session import SessionManager
from Test.testHandler import loginHandler, indexHandler, Handler



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
            (r"/test",  Handler),
            (r"/login", loginHandler),
            (r"/index", indexHandler)
        ]
        tornado.web.Application.__init__(self,handlers)
        self.session_manager = SessionManager(settings["session_secret"], settings["store_options"], settings["session_timeout"])



define('port', default=8888, group='application')

if __name__ == "__main__":
    debug = True
    application = Application()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()