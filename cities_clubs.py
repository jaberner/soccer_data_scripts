#   Makes SQL statements in a textfile that update the 'city_id' values in...
#   the CLUB table from null to the correct city id number.  For each club name...
#   (or part of the name) that matches the name of a city already in the database...
#   an SQL statement is written to the textfile to save time looking up city_id...
#   values individually. (ie. the city_id for club team Vancouver Whitecaps would...
#   be upated by the script of SQL statements if Vancouver already exists in the...
#   CITY table)
   

import MySQLdb
import os

clubs_db = []       #array to hold names of new clubs being added to database
cities_db = []      #array to hold all names of cities already in the CITY table


db = MySQLdb.connect(host="localhost",    # host
                     user="root",         # username
                     passwd="",           # password
                     db="soccer")         # name of the data base

cur = db.cursor()

# Select all new clubs from database and add club names to 'clubs_db' array
cur.execute("SELECT * FROM club WHERE club_id > 282")
for row in cur.fetchall():
    clubs_db.append(row[1])

# Select all cities from database and add city names to 'cities_db' array
cur.execute("SELECT * FROM city")
for row in cur.fetchall():
    cities_db.append(row[1])

# make textfile to store SQL update statements
c_file = open("C:/Soccer/clubs_cities.txt", "w")


# For each club name (or part of the name) that matches the name of a city already in the...
# database, an SLQ statement is witten to the textfile that updates the 'city_id' value in...
# the CLUB table from null to the correct city id number
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



