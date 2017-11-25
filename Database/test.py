from Database import db_link
from Database import db_operation
from Database.db_link import session, Vip

from Utils.mylog import log
try:
    first_vip = Vip("nihc","123","asonJJ")
    session.add(first_vip)
    session.commit()
except Exception as e:
    log.info(e)

session.close()
session.remove()
second_ivp = Vip("xuanle","xxxxx","董卓")
try:
    session.add(second_ivp)
    session.commit()
except Exception as e:
    log.info(e)
goldvip = db_operation.findByUsername("abc")
goldvip.sayName()


