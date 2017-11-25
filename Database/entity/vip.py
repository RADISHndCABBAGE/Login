from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from Utils.mylog import log
Base = declarative_base()



class Vip(Base):
    __tablename__ = "vip"
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(20))
    password = Column(String(20))
    gender = Column(String(20), primary_key=True)

    def __init__(self,username,password,gender):
        self.username=username
        self.password=password
        self.gender=gender

    def sayMoney(self):
        log.info(self.value)

    def sayName(self):
        print(self.username)


#
# class Article(Base):
#     __tablename__ = "article"
#     id = Column(Integer,primary_key=True,autoincrement=True)
#     article_value = Column(Integer)
#     article_author = Column(String(20))
#     article_pass = Column(String(20))
#     __table_args__ = {
#         ForeignKeyConstraint(
#             [article_author,article_pass]
#             [Vip.username,Vip.password]
#         )
#     }





class Cus(Base):
    __tablename__ = "customer"
    id = Column(Integer,primary_key=True,autoincrement=True)
    verification = Column(String(20))
    gender = Column(String(20),ForeignKey('vip.gender'))