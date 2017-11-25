from Database.db_link import Cus
from Database.db_operation import saveCus

customer = Cus()
customer.cus_hobby='哈林'
customer.verification=1423412

ex_customer= Cus()
ex_customer.cus_hobby="Eason"
ex_customer.verification='1423413'
saveCus(ex_customer)
saveCus(customer)
