# -*- coding: utf-8 -*-
from configparser import ConfigParser
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

from Utils.mylog import log

cf = ConfigParser()
cf.read("../Conf/link.ini")
db_username = cf.get("database","db_username")
db_password = cf.get("database","db_password")
db_host = cf.get("database","db_host")
db_port = cf.getint("database","db_port")
db_database = cf.get("database","db_database")


#解决编码问题。
engine = create_engine('mysql+pymysql://'+db_username+':'+db_password+'@'+db_host+':'+str(db_port)+'/'+db_database,connect_args={'charset':'utf8'})
con = engine.connect()
base = declarative_base(engine)
con.execute()

'''
vip表与cus表示一对多的关系
'''

class Vip(base):
    __tablename__ = "vip"
    __table_args__ = {'mysql_charset':'utf8'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20))
    password = Column(String(20))
    hobby = Column(String(20), unique=True)
    children = relationship("Cus")


    def __init__(self, username, password, hobby):
        self.username = username
        self.password = password
        self.hobby = hobby

    def sayName(self):
        log.info(self.username)

class Cus(base):
    __tablename__ = "cus"
    __table_args__ = {'mysql_charset':'utf8'}
    id = Column(Integer,primary_key=True,autoincrement=True)
    verification = Column(String(20))
    cus_hobby = Column(None, ForeignKey('vip.hobby'))


base.metadata.create_all()
