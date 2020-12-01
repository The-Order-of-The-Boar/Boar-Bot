from CRUD import db
from time import time
from datetime import datetime


a = time()
#db.insert_value("ServerConfigs",[45,'{12,14,15}'])

#db.custom_insert("DROP TABLE Messages")
#db.create_table("Messages",[["Server","BIGINT"],["Date","DATE"],["Num","SMALLINT"],["","PRIMARY KEY(Server,Date)"],["","FOREIGN KEY(Server) REFERENCES ServerConfigs(id) ON DELETE CASCADE"]])

#db.insert_value("Messages",[35,'2020-11-29',0])

db.custom_insert(f"INSERT INTO Messages VALUES (35,'2020-11-30',0) ON CONFLICT(Date,Server) DO UPDATE SET Num = Messages.Num+1")

print(db.retrieve_table("Messages"))

print("Runtime",time()-a)


print(datetime.now().date())