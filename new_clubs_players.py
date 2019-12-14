import MySQLdb
import os

clubs = []
clubs_db = []
clubs_no_db = []

players = []
players_db = []
players_no_db = []

a = open("C:/Soccer/new.txt", "r")
text = a.readlines()
for line in text:
    info = line.split("\t")
    if info[6].rstrip("\n") in clubs:
        pass
    else:
        clubs.append(info[6].rstrip("\n"))
    players.append(info[2].rstrip(" "))


db = MySQLdb.connect(host="localhost",    # host, usually localhost
                     user="root",         # username
                     passwd="",           # password
                     db="soccer")         # name of the data base

cur = db.cursor()

cur.execute("SELECT * FROM club")

for row in cur.fetchall():
    clubs_db.append(row[1])

cur.execute("SELECT * FROM player")

for row in cur.fetchall():
    players_db.append(row[1])

db.close()

for c in clubs:
    if c in clubs_db:
        pass
    else:
        clubs_no_db.append(c)
        
club_file = open("C:/Soccer/clubs.txt", "w")
for new_club in clubs_no_db:
    #print(new_club)
    club_file.write("INSERT INTO club (club_name) VALUES ('" + new_club + "');\n")
club_file.close()


for p in players:
    if p in players_db:
        pass
    else:
        players_no_db.append(p)
        
player_file = open("C:/Soccer/players.txt", "w")
for new_player in players_no_db:
    #print(new_player)
    player_file.write("INSERT INTO player (player_name) VALUES ('" + new_player + "');\n")
player_file.close()


