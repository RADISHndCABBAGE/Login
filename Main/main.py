import pyrestful as pyrestful
import pyrestful.rest
import tornado
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
import re
from Utils.session import SessionManager
from Main.testHandler import loginHandler, indexHandler,  registerHandler, quitHandler, FileUploadHandler


class Application(tornado.web.Application):
    def __init__(self,handlers):
        settings = dict(
            cookie_secret="e446976943b4e8442f099fed1f3fea28462d5832f483a0ed9a3d5d3859f==78d",
            session_secret="3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
            session_timeout=600,
            store_options={
                'redis_host': 'localhost',
                'redis_port': 6379,

            },
        )
        # handlers = [
        #     (r"/test",  Handler),
        #     (r"/login", loginHandler),
        #     (r"/index", indexHandler)
        # ]
        tornado.web.Application.__init__(self,handlers)
        self.session_manager = SessionManager(settings["session_secret"], settings["store_options"], settings["session_timeout"])


class RestService(Application):
    """
    Class to create Rest services in tornado web server
    """
    resource = None

    def __init__(self, rest_handlers,resource=None,handlers=None):
        restservices = []
        self.resource = resource
        for r in rest_handlers:
            svs = self._generateRestServices(r)
            restservices += svs
        if handlers != None:
            restservices += handlers
        Application.__init__(self, restservices)

    def _generateRestServices(self, rest):
        svs = []
        paths = rest.get_paths()
        for p in paths:
            s = re.sub(r'(?<={)\w+}', '.*', p).replace('{', '')
            o = re.sub(r'(?<=<)\w+', '', s).replace('<', '').replace('>', '').replace('&', '').replace('?', '')
            svs.append((o, rest, self.resource))

        return svs



define('port', default=8888, group='application')

if __name__ == "__main__":
    debug = True
    # application = Application()
    # application.listen(options.port)
    app = RestService([registerHandler,loginHandler,indexHandler,quitHandler,FileUploadHandler])
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()