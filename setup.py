from Management import server
from Statistics import rank,messages
from psycopg2.errors import DuplicateTable

try:
    server.CreateServerTable()
    rank.CreateRankTable()
    messages.CreateMessagesTable()
except DuplicateTable:
    print("Tables already exists")

f = open("localToken.txt", "w")
f.write("Remove this and paste your bot token here")
f.close()