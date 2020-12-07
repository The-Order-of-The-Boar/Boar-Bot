##############################################################################################
import sys
sys.path.append(".")

from Internals.CRUD import db
from datetime import datetime,timedelta

def CountMessage(server_id:int):
    db.custom_insert(f"""INSERT INTO Messages 
    VALUES ({server_id},'{datetime.now().date()}',1) ON CONFLICT(Date,Server) 
    DO UPDATE SET Num = Messages.Num+1""")


def UpdateMessages(server_id:id,day:str,value:int):
    db.insert_value("Messages",[server_id,day,value],
        additional=f"ON CONFLICT(Date,Server) DO UPDATE SET Num = {value}")


#################################Text Comands#########################################


def GetMessagesByDay(server_id:int,date):
    messages = db.custom_retrieve(f"""SELECT Num FROM Messages 
                        WHERE Date='{date}' AND Server={server_id}""")
    
    if(len(messages)==0):
        return 0
    return messages[0][0]


def GetLastMessages(server_id:int,amount:int=10,start:int=0):

    messages = db.custom_retrieve(f"""
    SELECT Date,Num FROM Messages WHERE Server={server_id} 
    ORDER BY Date DESC LIMIT {amount} OFFSET {start}
    """)

    return messages



from Internals import utils
utils.genTableString(GetLastMessages(272166101025161227),["Data","Mensagens"])

                    