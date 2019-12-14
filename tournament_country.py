import MySQLdb
import os

db = MySQLdb.connect(host="localhost",    # host, usually localhost
                     user="root",         # username
                     passwd="",           # password
                     db="soccer")         # name of the data base

cur = db.cursor()

a = open("C:/Soccer/nations_input.txt", "r")
b = open("C:/Soccer/tournament_nations.txt", "w")
text = a.readlines()
for line in text:
    cur.execute("SELECT country_id FROM country WHERE country_name = '" + line.rstrip("\n") + "'")
    row = cur.fetchone()
    b.write("INSERT INTO tournament_country (tournament_id, country_id) VALUES (3, " + str(row[0]) + ");\n")
            
db.close()
        
a.close()
b.close()



