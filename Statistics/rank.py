
from Internals.CRUD import db
from Internals import utils
from datetime import datetime,timedelta

#################################Rank Mangement#########################################

def CreateRankTable():
    """Creates the Rank table, not to be used , but stays as a reference"""
    db.create_table("Rank",[
        ["user_id", " BIGINT "],
        ["server_id", " BIGINT "],
        ["date","DATE"],
        ["messages", " INTEGER"],
        ["chars", " INTEGER"],
        ["PRIMARY KEY(user_id, server_id,date)", ""],
        ["FOREIGN KEY(server_id) REFERENCES ServerConfigs(id)"," ON DELETE CASCADE"],
        ])



def countPoints(server_id:int, user_id:int, chars:int):

    date  = datetime.now().date()
    date -= timedelta(days=date.weekday())

    db.custom_insert(f"""INSERT INTO Rank 
    VALUES ({user_id},{server_id},'{date}',1,{chars}) 
    ON CONFLICT(user_id,server_id,date) DO UPDATE SET 
    messages = Rank.messages+1,chars = Rank.chars+{chars} """)

    pass


#################################Rank Querys#########################################


def getRankByWeek(server_id:int,ago:int = 0):

    date  = datetime.now().date()
    date -= timedelta(days=date.weekday()+(ago*7))


    data = db.custom_retrieve(f""" SELECT user_id,messages 
            FROM Rank WHERE date = '{date}' AND server_id = {server_id}  
            ORDER BY messages DESC""")


    return data



