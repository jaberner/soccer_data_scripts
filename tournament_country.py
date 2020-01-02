#   Processes data copied from Wikipedia.org for all of the...
#   soccer players on the rosters of teams participating in...
#   major international tournaments (ie. the FIFA World Cup)

#Creates textfile with SQL statements that insert one row into...
#the database's TOURNAMENT_COUNTRY table for each country in a...
#tournamemt.  Reads a textfile containing the names of each...
#country in the tournament.  Then selects the country_id for...
#each and also adds the tournament_id to each insert statement.


import MySQLdb
import os

db = MySQLdb.connect(host="localhost",    # host
                     user="root",         # username
                     passwd="",           # password
                     db="soccer")         # name of the data base

cur = db.cursor()

a = open("C:/Soccer/nations_input.txt", "r")        #textfile with name of each country in tournament
b = open("C:/Soccer/tournament_nations.txt", "w")   #textfile that will hold the insert SQL statements
text = a.readlines()
for line in text:
    #get 'country_id' value from COUNTRY table in database
    cur.execute("SELECT country_id FROM country WHERE country_name = '" + line.rstrip("\n") + "'")
    row = cur.fetchone()
    #write SQL insert statement in textfile
    b.write("INSERT INTO tournament_country (tournament_id, country_id) VALUES (3, " + str(row[0]) + ");\n")
            
db.close()
a.close()
b.close()



