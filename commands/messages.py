##############################################################################################
import sys
sys.path.append(".")

from core.CRUD import db
from core import utils
from datetime import datetime,timedelta


def CreateMessagesTable():
    """Creates the Messages table, not to be used , but stays as a reference"""
    db.create_table("Messages",[
        ["server", " BIGINT "],
        ["date","DATE"],
        ["num", " SMALLINT"],
        ["PRIMARY KEY(server, date)", ""],
        ["FOREIGN KEY(server) REFERENCES ServerConfigs(id)"," ON DELETE CASCADE"],
        ])


def CountMessage(server_id:int):
    db.custom_insert(f"""INSERT INTO Messages 
    VALUES ({server_id},'{datetime.now().date()}',1) ON CONFLICT(Date,Server) 
    DO UPDATE SET Num = Messages.Num+1""")

def UncountMessage(message):

    date = utils.utcToLocal(message.created_at).date()

    db.update_value("Messages",["Date",date],["Num","Num-1",int])



def UpdateMessages(server_id:id,day:str,value:int):
    db.insert_value("Messages",[server_id,day,value],
        additional=f"ON CONFLICT(Date,Server) DO UPDATE SET Num = {value}")


#################################Text Commands#########################################


def GetMessagesByDay(server_id:int,date):
    """Gets the amount of messages from the given server in the give day  """

    messages = db.custom_retrieve(f"""SELECT Num FROM Messages 
                        WHERE Date='{date}' AND Server={server_id}""")
    
    if(len(messages)==0):
        return 0
    return messages[0][0]


def GetLastMessages(server_id:int,amount:int=10,start:int=0):
    """Gets the amount of messages from the given server in the given interval """

    messages = db.custom_retrieve(f"""
    SELECT Date,Num FROM Messages WHERE Server={server_id} 
    ORDER BY Date DESC LIMIT {amount} OFFSET {start}
    """)

    return messages

def GetMessageEmpireWeek(date:datetime):
    """Gets the amount of messages in all the Empire in the week of the given day"""


    #Gets the raw data with the messages from the week of the given day
    day_of_w = date.weekday()
    monday = date - timedelta(day_of_w)
    next_monday = monday + timedelta(days=7)

    data = db.custom_retrieve(f""" SELECT Server,Num 
            FROM MESSAGES WHERE Date >= '{monday}' AND Date < '{next_monday}'  
            ORDER BY Num DESC""")
    print(data)
    #Parses the raw data
    messages = {}
    for i in range(len(data)):
        if(data[i][0] in messages.keys()):
            messages[data[i][0]] += data[i][1]

                

        else:
            messages[data[i][0]] = data[i][1]

    return messages

def GetRecord(server_id:int):
    """Gets the days with the biggest amount of messages"""
    
    data = db.custom_retrieve(f"SELECT date,num FROM Messages WHERE server = {server_id} ORDER BY num DESC LIMIT 20 ")

    table = utils.genTableString(data,["Data","Mensagens"])
    embed = utils.genEmbed("Tabela de Recordes",table,descp="Dias com os maiores recordes \nde mensagens enviadas ")

    return embed

def GetAverage(server_id:int,ago:int=7):
    """Gets the daily messages average from the given amount of days ago"""

    avg = db.custom_retrieve(f"""
    SELECT AVG(num)::numeric(100,2) FROM 
    (SELECT num FROM Messages WHERE server = {server_id} ORDER BY date DESC LIMIT {ago} ) as mes_num""")[0][0]

    return f"A média de mensagens dos últimos {ago} dias é de {avg}"
