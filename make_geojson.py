#   Make geo_json files

import MySQLdb
import os

players_geojson = open("C:/Soccer/players_geojson.geojson", "w")          #textfile with name of each country in tournament
clubs_geojson = open("C:/Soccer/clubs_geojson.geojson", "w")              #textfile that will hold the insert SQL statements

#variables
country_num = 9
tournament_num = 3

#class for members of team
class Player:
    name = ""
    position = ""
    number = ""
    age = ""
    club = ""
    league = ""
    birthplace = ""
    birthplace_country = ""
    birthplace_x = ""
    birthplace_y = ""
    club_location = ""
    club_location_x = ""
    club_location_y = ""


#connect to database
db = MySQLdb.connect(host="localhost",    # host
                     user="root",         # username
                     passwd="",           # password
                     db="soccer")         # name of the data base
#database cursor
cur = db.cursor()

#select a roster
cur.execute("SELECT * FROM player " + \
            "INNER JOIN player_tournament ON player.player_id = player_tournament.player_id " + \
            "INNER JOIN club ON player_tournament.club_id = club.club_id " + \
            "INNER JOIN city C2 ON club.city_id = C2.city_id " + \
            "INNER JOIN city ON player.city_id = city.city_id " + \
            "INNER JOIN country ON city.country_id = country.country_id " + \
            "INNER JOIN league ON player_tournament.league_id = league.league_id " + \
            "WHERE player.country_id = " + str(country_num) + \
            " AND player_tournament.tournament_id = " + str(tournament_num) + \
            " ORDER BY player_tournament.number + 0 ")

players_geojson.write("{\n  " + '"type"' + ": " + '"FeatureCollection"' + ",\n  ")
players_geojson.write('"features"' + ": [\n    ")

#step through result set, write geojson file
for row in cur.fetchall():
    soccer_player = Player()
    soccer_player.name = row[1]
    soccer_player.position = row[7]
    soccer_player.number = row[8]
    soccer_player.age = row[9]
    soccer_player.club = row[13]
    soccer_player.league = row[33]
    soccer_player.birthplace = row[23]
    soccer_player.birthplace_country = row[29]
    soccer_player.birthplace_x = row[26]
    soccer_player.birthplace_y = row[27]
    soccer_player.club_location = row[17]
    soccer_player.club_location_x = row[20]
    soccer_player.club_location_y = row[21]
    players_geojson.write("{\n  " + '"type"' + ": " + '"Feature"' + ",\n    ")
    players_geojson.write('"geometry"' + ": {\n      ")
    players_geojson.write('"type"' + ": " + '"Point"' + ",\n      ")
    players_geojson.write('"coordinates"' + ": [" + str(soccer_player.birthplace_y) + ", " + str(soccer_player.birthplace_x) + "]\n    ")
    players_geojson.write("},\n    ")
    players_geojson.write('"properties"' + ": {\n      ")
    players_geojson.write('"name"' + ": " + '"' + soccer_player.name + '"' + ",\n      ")
    players_geojson.write('"position"' + ": " + '"' + soccer_player.position + '"' + ",\n      ")
    players_geojson.write('"number"' + ": " + '"' + soccer_player.number + '"' + ",\n      ")
    players_geojson.write('"age"' + ": " + '"' + soccer_player.age + '"' + ",\n      ")
    players_geojson.write('"club"' + ": " + '"' + soccer_player.club + '"' + ",\n      ")
    players_geojson.write('"league"' + ": " + '"' + soccer_player.league + '"' + ",\n      ")
    players_geojson.write('"birthplace"' + ": " + '"' + soccer_player.birthplace + '"' + ",\n      ")
    players_geojson.write('"birthplace_country"' + ": " + '"' + soccer_player.birthplace_country + '"' + "\n    ")
    players_geojson.write("}\n  ")
    players_geojson.write("},\n  ")
    print(soccer_player.birthplace_country)

players_geojson.write("  ]\n")
players_geojson.write("}")


db.close()
players_geojson.close()
clubs_geojson.close()



