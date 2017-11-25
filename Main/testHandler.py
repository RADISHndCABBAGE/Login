import json
import os
import ujson
import traceback
import pyrestful
from Database import db_operation
from Database.db_link import Vip
from Handler.base import BaseHandler
from Utils.mylog import log
from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete




class registerHandler(pyrestful.rest.RestHandler):

    @post(_path="/register", type=[str,str,str],_produces=mediatypes.APPLICATION_JSON,charset='utf8')
    def register(self,username,password,hobby):
        try:
            if(username!=None and password!=None and hobby!=None):
                if(db_operation.wetherExisted(username)=="no"):
                    try:
                        db_operation.insert(Vip(username,password,hobby))
                        self.write(json.dumps({"verification":"true"}))
                    except Exception as e:
                        log.info(e)
                        self.write(json.dumps({"verification":"false"}))

                else:
                    self.write(json.dumps({"verification":"false"}))
            else:
                raise Exception("字段非法")
        except Exception as e:
            print(e)

    @get(_path="/test", _produces=mediatypes.APPLICATION_JSON, charset='utf8')
    def test(self):
        par = self.get_argument('par',None)
        if par == None:
            print('none1')
        else:
            print(par+"1")


class loginHandler(BaseHandler):

    '''
    def post(self):
        try:
            username = self.get_argument('username')
            password = self.get_argument('password')
            vip = db_operation.findByUsername(username)
            log.info("vip: %",vip)
            if vip.password == password:
                self.session['username']= username
                self.session['password']= password
                self.session.save()
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(ujson.dumps({"ok":"yes"}))
            else:
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(ujson.dumps({"ok":"no"}))
        except Exception as e:
            log.info(e)
    '''

    @post(_path="/login",type=[str,str])
    def login(self):
        try:
            username = self.get_argument('username')
            password = self.get_argument('password')
            vip = db_operation.findByUsername(username)
            if vip.password == password:
                self.session['username']= username
                self.session['password']= password
                self.session.save()
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(ujson.dumps({"ok":"yes"}))
            else:
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(ujson.dumps({"ok":"no"}))
        except Exception as e:
            log.info(e)

class indexHandler(BaseHandler):
    @get(_path="/index",_produces=mediatypes.APPLICATION_JSON)
    def showMessage(self):
        try:
            basicDict = dict(self.session.items())
            hobby = db_operation.findHobby(basicDict['username'])
            basicDict['hobby'] = hobby
            self.write(json.dumps(basicDict))
        except Exception as e:
            log.info(e)
        finally:
            self.finish()


class quitHandler(BaseHandler):
    @get(_path="/quit")
    def quit(self):
        try:
            self.application.session_manager.redis.delete(self.session.session_id)
            self.clear_cookie("session_id")

        except Exception as e:
            log.info(e)


class FileUploadHandler(BaseHandler):
    @post(_path="/file",_produces=mediatypes.APPLICATION_JSON)
    def fileUpload(self):
        upload_path = os.path.join(os.path.dirname(__file__),'upload_files')
        # file_metas = self.get_argument('file',None)
        # file_metas = self.request.files.get('filename_first',None)
        file_metas = self.request.files['filename_first']
        for meta in file_metas:
            filename = meta['filename']
            file_local_path = os.path.join(upload_path,filename)
            try:
                with open(file_local_path, 'wb') as x:
                    x.write(meta['body'])
            except Exception as e:
                # traceback.print_exc(e)
                print(e)
