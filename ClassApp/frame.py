# from fla import Flask, jsonify
# import mysql.connector

# conn = mysql.connector.connect(user='adm_1', password='ssu_serverprog', host='10.29.112.30', database='AppClassDB', port='3306')
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM carttable")
# cart = cursor.fetchall()
# cursor.execute("SELECT * FROM logintable")
# account = cursor.fetchall()
# cursor.execute("SELECT * FROM subinfotable")
# subs = cursor.fetchall()


# data_list = []
# for row in [cart, account, subs]:
#     print(row)

# cursor.close()
# conn.close()