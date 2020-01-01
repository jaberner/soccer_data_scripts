#   Processes data copied from Wikipedia.org for all of the...
#   soccer players on the rosters of teams participating in...
#   major international tournaments (ie. the FIFA World Cup)

#Mines and old personal datbase.
#Searches old database for PLAYER names that match players...
#that need to be added to new database.  If a match is...
#found, the city where the player was born is added to...
#the new database if necessary OR if already in the new...
#database, the 'city_id' field is added where necessary.


import MySQLdb
import os


cities = []
old_players = []
new_clubs = [];

a = open("C:/Soccer/soccermap.txt", "r")
text = a.readlines()
for line in text:
        info = line.split("^")
        old_players.append(info[3])


db = MySQLdb.connect(host="localhost",    # host
                     user="root",         # username
                     passwd="",           # password
                     db="soccer")         # name of the data base

player_file2 = open("C:/Soccer/players2.txt", "w")

cur = db.cursor()
cur.execute("SELECT * FROM city")
for row in cur.fetchall():
    cities.append(row[1])      
        

cur.execute("SELECT * FROM player WHERE player_id > 705")

for row in cur.fetchall():                                              #step through new players
    if row[1] in old_players:                                                   #if player name appears in the old list ->
        for line in text:                                                               #step through each line of old text file
            info = line.split("^")                                                              #split each line                                        
            if row[1] == info[3]:                                                                       #when the player name is equal a player name in a line from the text file ->
                if info[9] in cities:                                                                           #and if the birth city in the line of the old text file is already in the database ->
                        player_file2.write("UPDATE player SET city_id = (SELECT city_id FROM city WHERE city_name = '" + info[9] + "') WHERE player_id = " + str(row[0]) + ";\n")                     #UPDATE city_id in player table
                else:                                       #else ->
                        if info[9] in new_clubs:                    #already added - > pass
                                pass
                        else:
                                player_file2.write("INSERT INTO city (city_name, country_id, X, Y) VALUES ('" + info[9] + "',(SELECT country_id FROM country WHERE country_name = '" + info[10] + "'), " + info[16] + ", " + info[15] + ");\n")                             #INSERT city into city table
                                new_clubs.append(info[9])               #else - > INSERT new city if city not already in database
                                
db.close()



