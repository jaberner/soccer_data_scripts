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


cities = []             #array to hold CITY names already in database
old_players = []        #array to hold PLAYER names that exist in old database
new_players = [];       #array to hold PLAYER names that are being added to new datbase

player_end = 705        #number of last record already in PLAYERS database table


# Open soccermap.txt.  Contains rows of data from my old database (to be mined)
a = open("C:/Soccer/soccermap.txt", "r")
text = a.readlines()
for line in text:
        info = line.split("^")
        old_players.append(info[3])


db = MySQLdb.connect(host="localhost",    # host
                     user="root",         # username
                     passwd="",           # password
                     db="soccer")         # name of the data base

#textfile that will hold UPDATE SQL statements for PLAYERS
player_file2 = open("C:/Soccer/players2.txt", "w")

#SELECT all CITIES from database and add city names to 'cities' array
cur = db.cursor()
cur.execute("SELECT * FROM city")
for row in cur.fetchall():
    cities.append(row[1])      
        
#Select all NEW players being added to database.
cur.execute("SELECT * FROM player WHERE player_id > " + str(player_end))
for row in cur.fetchall():                                                      #step through new players
    if row[1] in old_players:                                                   #if player name appears in the old list ->
        for line in text:                                                       #step through each line of old text file
            info = line.split("^")                                              #split each line                                        
            if row[1] == info[3]:                                               #when the player name is equal a player name in a line from the text file ->
                if info[9] in cities:                                           #and if the birth city in the line of the old text file is already in the database -> #UPDATE city_id in player table
                        player_file2.write("UPDATE player SET city_id = (SELECT city_id FROM city WHERE city_name = '" + info[9] + "') WHERE player_id = " + str(row[0]) + ";\n")
                else:                                                           #else ->
                        if info[9] in new_players:                              #already added - > pass
                                pass
                        else:
                                player_file2.write("INSERT INTO city (city_name, country_id, X, Y) VALUES ('" + info[9] + "',(SELECT country_id FROM country WHERE country_name = '" + info[10] + "'), " + info[16] + ", " + info[15] + ");\n")                             #INSERT city into city table
                                new_players.append(info[9])                     #else - > INSERT new city if city not already in database
                                
db.close()



