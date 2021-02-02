from Management import server
from Statistics import rank,messages
from Internals.CRUD import db
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