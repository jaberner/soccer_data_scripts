import MySQLdb
import os

clubs_db = []
cities_db = []


db = MySQLdb.connect(host="localhost",    # host, usually localhost
                     user="root",         # username
                     passwd="",           # password
                     db="soccer")         # name of the data base

cur = db.cursor()

cur.execute("SELECT * FROM club WHERE club_id > 282")

for row in cur.fetchall():
    clubs_db.append(row[1])

cur.execute("SELECT * FROM city")

for row in cur.fetchall():
    cities_db.append(row[1])

c_file = open("C:/Soccer/clubs_cities.txt", "w")

for c in clubs_db:
    club_words = c.split(" ")
    for x in club_words:
        if x in cities_db:
            cur.execute("SELECT city_id FROM city WHERE city_name = '" + x + "'")
            if cur.rowcount == 1:
                for row in cur.fetchall():
                    c_file.write("UPDATE club SET city_id = " + str(row[0]) + " WHERE club_name = '" + c + "';\n")
        
db.close()
        
c_file.close()



