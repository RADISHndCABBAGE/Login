from Database import user_database

vip = user_database.findByUsername("张三")
print(vip)
print(vip.password)