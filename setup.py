from commands import server
from commands import rank,messages
from core.CRUD import db
from psycopg2.errors import DuplicateTable

try:
    server.CreateServerTable()
    rank.CreateRankTable()
    messages.CreateMessagesTable()

except DuplicateTable:
    print("Tables already exists")
    print("TYPE 'reset' IN ORDER TO DELETE THE OLD TABLES AND CREATE NEW ONES. BE CAREFULL, THIS WILL ERASE ALL DATA")
    
    if(input().lower() == 'reset'):    
        db.custom_insert("DROP TABLE ServerConfigs")
        db.custom_insert("DROP TABLE Rank")
        db.custom_insert("DROP TABLE Messages")
        
        server.CreateServerTable()
        rank.CreateRankTable()
        messages.CreateMessagesTable()

f = open("localToken.txt", "w")
f.write("Remove this and paste your bot token here")
f.close()
f = open("immoral_chars.json", "w")
f.write("""{
    "𝓘" : "I",
    "𝓪" : "a",
    "𝓶": "m",
    "𝓼" : "s",
    "𝓾" : "u",
    "𝓻" : "r",
    "𝓿" : "v",
    "𝓲" : "i",
    "𝓸" : "o"
}""")
f.close()