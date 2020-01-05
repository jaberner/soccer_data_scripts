#   Processes data copied from Wikipedia.org for all of the...
#   soccer players on the rosters of teams participating in...
#   major international tournaments (ie. the FIFA World Cup)




import MySQLdb
import os


#textfiles
data_file = open("C:/Soccer/new.txt", "r")                          #textfile with raw data copied from Wikipedia.org
insert_file = open("C:/Soccer/player_tournament2.txt", "w")         #holds processed data, lines of INSERT SQL statements


db = MySQLdb.connect(host="localhost",    # host
                     user="root",         # username
                     passwd="",           # password
                     db="soccer")         # name of the data base

cur = db.cursor()

#read data copied from Wikipedia
text = data_file.readlines()
for line in text:
    info = line.split("\t")     #tab deliminated
    #select player from database and get player_id
    cur.execute("SELECT player_id FROM player WHERE player_name = '" + info[2] + "'")
    if cur.rowcount == 1:
        row = cur.fetchone()
        player = str(row[0])    #player_id
    else:       #player not in database
        player = "error: " + info[2].rstrip("\n")
    print(player)
    #gets ALL the info (id numbers) related to the player's club team from the database
    cur.execute("SELECT * FROM league WHERE league.country_id = (" + \
            "SELECT country.country_id FROM country WHERE country.country_id = (" + \
		"SELECT city.country_id FROM city WHERE city.city_id = (" + \
			"SELECT club.city_id FROM club WHERE club.club_name = '" + info[6].rstrip("\n") + "')));")
    if cur.rowcount > 1:    #in some cases more than one league in database per country
        for row in cur.fetchall():
            if row[2] == 1:                 #if league is TOP division -> choose it
                league = "*" + str(row[0])  #but add '*' in order to flag it, manually check it's the correct league later
            else:
                pass
    elif cur.rowcount == 1:
        row = cur.fetchone()
        league = str(row[0])
    else:
        league = "error: " + info[6].rstrip("\n")
    n = info[3].find(")")
    age = info[3][n-2:n]
    cur.execute("SELECT club_id FROM club WHERE club_name = '" + info[6].rstrip("\n") + "'")
    if cur.rowcount == 1:
        row = cur.fetchone()
        club = str(row[0])
    else:
        club = "error: " + info[6].rstrip("\n")
    insert_file.write("INSERT INTO player_tournament (player_id, tournament_id, position, number, age, club_id, league_id) VALUES (" + player + ", 2, '" +  \
                      info[1].rstrip(" ") + "', " + info[0].rstrip(" ") + ", " + age + ", " + club + ", " + league + ");\n")


 
db.close()
insert_file.close()
data_file.close()


