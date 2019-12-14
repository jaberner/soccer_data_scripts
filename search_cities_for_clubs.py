import MySQLdb
import os

clubs_db = []
old_clubs = []
new_clubs = []
club_end = 282

players_db = []
old_players = []
player_end = 705

cities = []


a = open("C:/Soccer/soccermap.txt", "r")
text = a.readlines()
for line in text:
        info = line.split("^")
        old_players.append(info[3])
        old_clubs.append(info[4])


db = MySQLdb.connect(host="localhost",    # host, usually localhost
                     user="root",         # username
                     passwd="",           # password
                     db="soccer")         # name of the data base

club_file2 = open("C:/Soccer/clubs2.txt", "w")
player_file2 = open("C:/Soccer/players2.txt", "w")

cur = db.cursor()

cur.execute("SELECT * FROM city")

for row in cur.fetchall():
    cities.append(row[1])
    

cur.execute("SELECT * FROM club WHERE club_id > 282")

for row in cur.fetchall():                  #step through new clubs
    if row[1] in old_clubs:                     #if club name appears in the old list ->
        for line in text:                           #step through each line of old text file
            info = line.split("^")                      #split each line
            if row[1] == info[4]:                       #when the club name is equal a club name in a line from the text file ->
                if info[6] in cities:                       #and if the city for the club in the line of the old text file is already in the database ->
                    club_file2.write("UPDATE club SET city_id = (SELECT city_id FROM city WHERE city_name = '" + info[6] + "') WHERE club_id = " + str(row[0]) + ";\n")                     #UPDATE city_id in club table
                else:                                       #else ->
                    if info[6] in new_clubs:                    #already added - > pass
                        pass
                    else:
                        club_file2.write("INSERT INTO city (city_name, country_id, X, Y) VALUES ('" + info[6] + "',(SELECT country_id FROM country WHERE country_name = '" + info[7] + "'), " + info[14] + ", " + info[13] + ");\n")                             #INSERT city into city table
                        new_clubs.append(info[6])               #else - > INSERT new city if city not already in database
                break
print("DONE")


