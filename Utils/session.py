# -*- coding:utf-8 -*-
import hashlib
import hmac
import ujson
import uuid

import redis

from Utils.mylog import log


class SessionManager(object):

    def __init__(self,secret,store_options,session_timeout):
        self.secret = secret
        self.session_timeout = session_timeout
        try:
            self.redis = redis.StrictRedis(host=store_options['redis_host'],
                                           port=store_options['redis_port']
                                           )
        except Exception as e:
                print(e)

    def _fetch(self,session_id):
        try:
            session_data = raw_data = self.redis.get(session_id)
            if raw_data:
                self.redis.setex(session_id,self.session_timeout,raw_data)
                session_data = ujson.loads(raw_data)
            if isinstance(session_data,dict):
                return session_data
            else:
                return {}
        except IOError:
            return {}

    def get(self,request_handler=None):


        try:

            if not request_handler:
                session_id = None
                # hmac_key = None
            else:

                session_id = request_handler.get_cookie("session_id")
                # hmac_key = request_handler.get_cookie("verification")

            if not session_id:

                session_exists = False
                session_id = self._generate_id()
                hmac_key = self._generate_hmac(session_id)
            else:
                session_exists = True

            # check_hmac = self._generate_hmac(session_id)

            # if not session_exists:
            #     hmac_key_byte = hmac_key.encode('utf-8')
            # if hmac_key_byte != check_hmac.encode('utf-8'):
            #     raise InvalidSessionException()

            # session = SessionData(session_id,hmac_key)
            session = SessionData(session_id)


            if session_exists:
                session_data = self._fetch(session_id)
                for key,data in session_data.items():
                    session[key] = data
        except Exception as e:
            log.info(e)

        return session

    def set(self,request_handler,session):
        try:
            request_handler.set_cookie("session_id",session.session_id)
        except Exception as e:
            log.info(e)
        # request_handler.set_cookie("verification",session.hmac_key)
        session_data = ujson.dumps(dict(session.items()))
        try:
            flag = self.redis.setex(session.session_id,self.session_timeout,session_data)
            log.info("flag:",flag)
        except Exception as e:
            log.info(e)


    def _generate_id(self):
        new_id = hashlib.sha256(self.secret.encode()+str(uuid.uuid4()).encode())
        return new_id.hexdigest()

    #
    # def _generate_hmac(self, session_id):
    #     if isinstance(session_id,bytes):
    #         return hmac.new(session_id, self.secret.encode('utf-8'), hashlib.sha256).hexdigest()
    #     else:
    #         return hmac.new(session_id.encode('utf-8'), self.secret.encode('utf-8'), hashlib.sha256).hexdigest()
    #

class InvalidSessionException(Exception):
    pass




class SessionData(dict):
    def __init__(self,session_id):
        self.session_id = session_id
        # self.hmac_key = hmac_key



class Session(SessionData):
    def __init__(self,session_manager,request_handler):
        self.session_manager = session_manager
        self.request_handler = request_handler
        try:
            current_session = session_manager.get(request_handler)
        except Exception as e:
            log.info(e)
        for key,data in current_session.items():
            self[key] = data
        self.session_id = current_session.session_id
        # self.hmac_key = current_session.hmac_key

    def save(self):
        self.session_manager.set(self.request_handler,self)



