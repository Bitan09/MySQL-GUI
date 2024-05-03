import mysql.connector as sql
con1 = sql.connect(host='localhost',user='root',passwd='234')
if con1.is_connected():
    print('done')
else:
    print('not done')
