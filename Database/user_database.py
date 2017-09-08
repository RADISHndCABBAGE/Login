# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
import re



Base = declarative_base()
flag = ""


#解决编码问题。
engine = create_engine('mysql+pymysql://root:newcger@localhost:3306/test',connect_args={'charset':'utf8'})
DBSession = sessionmaker(bind=engine)
session = DBSession()

class Vip(Base):
    __tablename__ = "vip"
    id = Column(Integer,primary_key=True)
    username = Column(String(20))
    password = Column(String(20))

def findByUsername(username):
    try:
        vip = Vip()
        for entity in session.query(Vip).filter(Vip.username == username):
            vip.username = entity.username
            vip.password = entity.password
        return vip
    except Exception as e:
        print(e)
    finally:
        session.close()





