#   Processes data copied from Wikipedia.org for all of the...
#   soccer players on the rosters of teams participating in...
#   major international tournaments (ie. the FIFA World Cup)

#   Reads text file containing information on each player. ...
#   Checks if the players and their professional club team...
#   are already in the database.  SQL statements are written...
#   for each player and/or club not already in the database...
#   in a textfile so each can be added.


import MySQLdb
import os

#arrays
clubs = []          #holds CLUB names that appear in data from Wikipedia
clubs_db = []       #holds CLUB names that already exist in database
clubs_no_db = []    #holds CLUB names that don't already exist in database

#arrays
players = []        #holds PLAYER names that appear in data from Wikipedia
players_db = []     #holds PLAYER names that already exist in database
players_no_db = []  #holds PLAYER names that don't already exist in database

#open textfile with data copied from Wikipedia
a = open("C:/Soccer/new.txt", "r")

#read each line, find the CLUB name, check if already in array "clubs", if not -> add it to array.  Add all PLAYER names to array "players"
text = a.readlines()
for line in text:
    info = line.split("\t")
    if info[6].rstrip("\n") in clubs:
        pass
    else:
        clubs.append(info[6].rstrip("\n"))
    players.append(info[2].rstrip(" "))

#connect to database
db = MySQLdb.connect(host="localhost",    # host
                     user="root",         # username
                     passwd="",           # password
                     db="soccer")         # name of the data base

cur = db.cursor()

#select all CLUB names already in DB, add them to "clubs_db" array
cur.execute("SELECT * FROM club")       
for row in cur.fetchall():
    clubs_db.append(row[1])
    
#select all PLAYER names already in DB, add them to "players_db" array
cur.execute("SELECT * FROM player")
for row in cur.fetchall():
    players_db.append(row[1])

db.close()


#if CLUB names in "clubs" array aren't in "clubs_db" array (already exist in DB) -> add club name to "clubs_no_db" array
for c in clubs:
    if c in clubs_db:
        pass
    else:
        clubs_no_db.append(c)

#create new textfile, for each CLUB name not in DB -> write a line of SQL to insert value into DB table
club_file = open("C:/Soccer/clubs.txt", "w")
for new_club in clubs_no_db:
    club_file.write("INSERT INTO club (club_name) VALUES ('" + new_club + "');\n")
club_file.close()


#if PLAYER names in "players" array aren't in "players_db" array (already exist in DB) -> add player name to "players_no_db" array
for p in players:
    if p in players_db:
        pass
    else:
        players_no_db.append(p)

#create new textfile, for each PLAYER name not in DB -> write a line of SQL to insert value into DB table   
player_file = open("C:/Soccer/players.txt", "w")
for new_player in players_no_db:
    player_file.write("INSERT INTO player (player_name) VALUES ('" + new_player + "');\n")
player_file.close()


