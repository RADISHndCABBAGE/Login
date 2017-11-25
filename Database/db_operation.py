import json
import traceback

from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from Database.db_link import session, Vip, Cus, Student, Grade, Course
from Utils.Sqlsys import profile, _profile
from Utils.mylog import log


def findByUsername(username):
    vip = session.query(Vip).filter(Vip.username==username).first()
    return vip


def saveCus(customer):
    session.add(customer)
    session.commit()
    print(session)
    session.close()

def limitFromCus(hobby):
    result = session.query(Cus).filter_by(cus_hobby = '哈林').limit(5)
    # row = result.fetchone()
    for row in result:
        log.info("row_id:%d" % row.id)


def limitFromCus_byself(hobby):
    result = session.query(Cus).filter_by(cus_hobby='哈林').limit(5).from_self()
    for row in result:
        log.info("row_id: %d" % row.id)


def findStu_idViaScore():
    result = session.query(Student).join(Grade,Student.stu_id==Grade.grade_stu_id).all()
    print(result)

def findStu_idCus_nameScore():
    result = session.query(Student.stu_id,Grade.score,Course.cou_name).filter(Student.stu_id == Grade.grade_stu_id).join(Course,Grade,Grade,Grade.grade_cou_id == Course.cou_id).all()
    # result = session.query(Grade.grade_stu_id,Grade.score,Course.cou_name).join(Student,Grade.grade_stu_id == Student.stu_id).join(Course,Grade.grade_cou_id == Course.cou_id).all()
    # result = session.query(Course.cou_name,Grade.grade_stu_id,Grade.score).filter(Grade.grade_stu_id == Student.stu_id).join(Course,Grade.grade_cou_id == Course.cou_id).all()
    # result = session.query(Grade.score,Student.stu_id).join(Grade,Grade.grade_stu_id == Student.stu_id).all()
    print(result)


def findSomething():
    result = session.query(Student.stu_id).all()
    print(result)

def findTwothing():
    result = session.query(Student.stu_id,Course.cou_name).all()
    print(result)

def findTwothingSpecial():
    result = session.query(Student.stu_id).filter(Grade.grade_stu_id==Student.stu_id,Grade.score>70.0).all()
    print(result)

# def findTwothingAnother():
#     """
#     这个报错了
#     :return:
#     """
#     result = session.query(Student.stu_id).join(Grade.grade_stu_id == Student.stu_id, Grade.score > 70.0).all()
#     print(result)

@profile
def testJoin():
    result = session.query(Cus.verification,Vip.username).join(Vip,Cus.verification.op('regexp')('3$')).filter(Vip.hobby == Cus.cus_hobby).all()
    print(result)

#     查询课程1的成绩比课程2的成绩高的同一个同学的id
def joinTest():
    result_1 = session.query(Grade.grade_stu_id,Grade.score).filter_by(grade_cou_id = 1).all()
    result_2 = session.query(Grade.grade_stu_id,Grade.score).filter_by(grade_cou_id = 2).all()
    result_3 = session.query(result_1.grade_stu_id).filter(result_1.grade_stu_id == result_2.grade_stu_id,result_1.score < result_2.score).all()
    result_final = session.query(Student.stu_name,Student.stu_id).filter(Student.stu_id == result_3.grade_stu_id ).all()
    result = json.dumps(result_final)
    log.info(result)


def wetherExisted(username):

    result = session.query(Vip).filter(Vip.username == username).count()
    session.rollback()
    if(result ==0):
        return "no"
    else:
        return "yes"


def insert(v):
    if(isinstance(v,Vip)):
        session.add(v)
        try:
            session.commit()
        except:
            session.rollback()
            raise Exception("插入失败")
    else:
        raise Exception("插入类型非Vip")

def findHobby(username):
    try:
        result = session.query(Vip.hobby).filter(Vip.username == username).first()
    except Exception as e:
        raise e
    return result

def findStuName(stu_id):
    result = session.query(Student.stu_name).filter(Student.stu_id==stu_id).first()
    print(type(result))
    print(result.stu_name)
    return result

setting = {
    'stu_id':3,
    'stu_age':21
}

def testParameter(**kwargs):
    result = session.query(Student.stu_name).filter_by(**kwargs).first()
    print(result.stu_name)
    return result

def testParameterFilter(**kwargs):
    result = session.query(Student.stu_name).filter(**kwargs).first()
    print(result.stu_name)
    return result

def testFilterAndFilterby():
    result = session.query(Student.stu_name).filter(Student.stu_id == 5).filter_by(stu_age=21).all()
    for row in result:
        print(row.stu_name)

    return result

def testColumnString(id_string,key_word):
    # result = Student.__dict__
    # print(result)
    # result = session.query(Student.stu_name).filter(Student.__dict__[id_string].like(key_word+"%")).first() 字符串开始
    # result = session.query(Student.stu_name).filter(Student.__dict__[id_string].like(key_word+"$")).first()
    # result = session.query(Student.stu_name).filter(Student.__dict__[id_string].op('regexp')('^'+key_word)).all()
    # result = session.query(func.count(Student.stu_id)).filter(Student.__dict__[id_string].op('regexp')(key_word)).all()
    result = session.query(Student.stu_age).filter(Student.stu_name == '' ).all()
    for row in result:
        print(row.stu_name)
    # print(result[0][0])
    # print()
    return result

def testRebackEntity():
    result = session.query(Student).filter(Student.stu_age == None).first()
    if not result:
        print(1)
    return result

def slice():
    result = session.query(Student).filter(Student.stu_name.op('regexp')('节')).slice(1,4).all()
    for row in result:
        print(row.stu_name)
    return result

list = [Student.stu_name.op('regexp')('节')]
def testFilter(list):
    result = session.query(Student).filter(list).all()
    return result

def testIn():
    result = session.query(Student.stu_name).filter(Student.stu_id.in_([1,2,3])).all()
    return result

def testList():
    result = session.query(Student.stu_name).filter(Student.stu_id == 9).limit(3).offset(0)
    # if result:
    #     print('true')
    for row in result:
        print(row.stu_name +'\n')
    return result

def insertStu():
    student = Student(stu_name="低调",stu_id=9,stu_age=30)
    try:
        # 1/0
        session.add(student)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def testDel():
    try:
        row = session.query(Student).filter(Student.stu_id == 1).delete()
        session.commit()
        log.info(row)
    except Exception as e:
        session.rollback()
        log.error(e,exc_info=True)

def testAdd():
    try:
        student = Student(stu_id=11,stu_name='Ingram',stu_age=25)
        row = session.add(student)
        #row一直为None， add方法没有返回值
        session.commit()
    except IntegrityError as e:
        print(type(e))
        session.rollback()
        log.error(e,exc_info=True)
        raise e
    return row
def countgroup():
    # age_list = [19,30,21,31]
    id_list = [2,2,1,3]
    # cond = and_(Student.stu_age.in_(age_list))
    cond = and_(Student.stu_id.in_(id_list))
    result = session.query(Student.stu_name, Student.stu_id).group_by(Student.stu_name, Student.stu_id).filter(cond).all()
    # result = session.query(Student.stu_id).filter(cond).all()
    print(result)
    return result

def raise_demo():
    if 1 == 1:
        raise Exception()

def update():
    try:
        row = session.query(Student).filter(Student.stu_id == 1).update({Student.stu_age: 26})
        session.commit()
        if row:
            print('update success')
    except Exception as e:
        session.rollback()
        log.error(e, exc_info=True)

def testRegexp():
    result = session.query(Student).filter(Student.stu_name.op('regexp')('步')).one_or_none()
    result.name = '123'
    print(type(result))
    print(result.name)
    return result

def test_exce(stu_id):
    int('nihc')
    result = session.query(Student).filter(Student.stu_id == stu_id).one_or_none()
    if not result:
        raise Parameter_Exception(100, 'stu_id is not exists')
    else:
        print(result.stu_name)
def test_in(list):
    result = session.query(Student).filter(Student.stu_id.in_(list)).all()
    return result

class A():
    def __init__(self):
        self.ppt = 'ppt'


class Parameter_Exception(Exception):
    def __init__(self, status, msg):
        self.status = status
        self.msg = msg


def ku():
    a = A()
    a.name = 'aaa'
    print(a.name)


# findByUsername('abc').assembling()
# limitFromCus('哈林')
# limitFromCus_byself('哈林')
# findStu_idViaScore()
# findStu_idCus_nameScore()
# findSomething()
#findTwothing()
# findTwothingSpecial()
# findTwothingAnother()
# testJoin()
# joinTest()
# findStuName(1)
#testParameter(**setting)
# testParameterFilter(**setting)
# testFilterAndFilterby()
# testColumnString('stu_name',"")
# wetherExisted('')
# testRebackEntity()
# plus()
# slice()
# testFilter(*list)
# testIn()
# testList()
# try:
#     # result = testDel()
#     testAdd()
# except Exception as e:
#     # log.info(e.args[0])
#     log.info(e.orig.args[0])
# testDel()
# countgroup()
# try:
#     raise_demo()
# except Exception as e:
#     log.error(e, exc_info=True)

# update()
# testRegexp()
# ku()
# result = testAdd()
# try:
#     test_exce(113)
# except Parameter_Exception as e:
#     log.error(e, exc_info=True)
#     print(e.status)
#     print(e.msg)
# except Exception as e:
#     log.error(e, exc_info=True)
#     print('error')
#
# test_in([])
testRebackEntity()