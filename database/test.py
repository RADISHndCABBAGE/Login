from Database import user_database

vip = user_database.findByUsername("alfei")
print(vip)
print(vip.password)