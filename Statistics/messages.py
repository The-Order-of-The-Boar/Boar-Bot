##############################################################################################
import sys
sys.path.append(".")

from CRUD import db
from datetime import datetime,timedelta

def CountMessage(server_id:int):
    db.custom_insert(f"""INSERT INTO Messages 
    VALUES ({server_id},'{datetime.now().date()}',1) ON CONFLICT(Date,Server) 
    DO UPDATE SET Num = Messages.Num+1""")



#################################Text Comands#########################################


def GetMessagesByDay(server_id:int,date):
    messages = db.custom_retrieve(f"""SELECT Num FROM Messages 
                        WHERE Date='{date}' AND Server={server_id}""")
    
    if(len(messages)==0):
        return 0
    return messages[0][0]



print(datetime.now().date())


                    