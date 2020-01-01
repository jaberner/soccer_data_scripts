#   Processes data copied from Wikipedia.org for all of the...
#   soccer players on the rosters of teams participating in...
#   major international tournaments (ie. the FIFA World Cup)

#Mines and old personal datbase.
#Searches old database for CLUB names that match clubs...
#that need to be added to new database.  If a match is...
#found, the city where the club is located is added to...
#the new database if necessary OR if already in the new...
#database, the 'city_id' field is added where necessary.


import MySQLdb
import os


old_clubs = []          #array to hold CLUB names that exist in old database
new_clubs = []          #array to hold CLUB names that are being added to new datbase
cities = []             #array to hold CITY names already in database

club_end = 282          #number of last record already in CLUBS database table


## Open soccermap.txt.  Contains rows of data from my old database
a = open("C:/Soccer/soccermap.txt", "r")
text = a.readlines()
for line in text:
        info = line.split("^")
        old_clubs.append(info[4])       #add club names to 'old_clubs' array


db = MySQLdb.connect(host="localhost",    # host
                     user="root",         # username
                     passwd="",           # password
                     db="soccer")         # name of the data base

club_file2 = open("C:/Soccer/clubs2.txt", "w")          #textfile that will hold UPDATE SQL statements for CLUBS


#SELECT all CITIES from database and add city names to 'cities' array
cur = db.cursor()
cur.execute("SELECT * FROM city")
for row in cur.fetchall():
    cities.append(row[1])
    
#Select all NEW clubs being added to database. 
cur.execute("SELECT * FROM club WHERE club_id > " + str(club_end))
for row in cur.fetchall():                              #step through new clubs
    if row[1] in old_clubs:                             #if club name appears in the old list (existed in old database) ->
        for line in text:                               #step through each line of old text file
            info = line.split("^")                      #split each line
            if row[1] == info[4]:                       #if the club name is equal a club name in a line from the text file ->
                if info[6] in cities:                   #and if the city for the club in the line of the old text file is already in the database -> UPDATE city_id in club table
                    club_file2.write("UPDATE club SET city_id = (SELECT city_id FROM city WHERE city_name = '" + info[6] + "') WHERE club_id = " + str(row[0]) + ";\n")
                else:                                   #else ->
                    if info[6] in new_clubs:            #already exists - > pass
                        pass
                    else:                               #else - > INSERT new city if city not already in database
                        club_file2.write("INSERT INTO city (city_name, country_id, X, Y) VALUES ('" + info[6] + "',(SELECT country_id FROM country WHERE country_name = '" + info[7] + "'), " + info[14] + ", " + info[13] + ");\n")                             #INSERT city into city table
                        new_clubs.append(info[6])       
                break
print("DONE")


