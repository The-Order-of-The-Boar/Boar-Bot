#################################Server Management#####################################################
from Internals.CRUD import db
from os import getcwd,path


#################################Server Setup#########################################

def AddServer(idd:int,channels:list):
    """Adds a new entry to the ServerConfigs table, with the id from server and it's channels"""

    channels_ids = "{"
    for ch in channels:
        channels_ids+=f'"{ch.id}",'
    channels_ids = channels_ids[:-1] + "}"

    db.insert_value("ServerConfigs",[idd,channels_ids])

def RemoveServer(idd:int):
    db.delete_value("ServerConfigs","id",idd)

def CreateServerTable():
    """Creates the ServerConfigs table, not to be used , but stays as a reference"""
    db.create_table("ServerConfigs",[
        ["id", " BIGINT PRIMARY KEY"],
        ["listen_channels", " BIGINT[]"],
        ["welcome_channel", " BIGINT"],
        ["role", "BIGINT"],
        ["welcome_message", " VARCHAR(200)"]
        ])

#################################Welcome#########################################


def SetWelcome(server_id:int,channel_id:int,message:str):

    db.custom_insert(f"""UPDATE ServerConfigs SET
    welcome_channel={channel_id},
    welcome_message='{message}',
    WHERE id = {server_id}
     """)
    
def UnsetWelcome(server_id:int):

    db.custom_insert(f"""UPDATE ServerConfigs SET
    welcome_channel= NULL ,
    welcome_message= NULL,
    WHERE id = {server_id}
     """)
    pass
    

def GetWelcome(server_id:int):

    welcome = {}
    welcome["channel"],welcome["message"] = db.retrieve_value("ServerConfigs","welcome_channel,welcome_message",["id",server_id])[0]

    return welcome


#################################Autorole#########################################

def setAutorole(server_id:int,role:int):
    
    db.custom_insert(f"""UPDATE ServerConfigs SET
            role ={role}
            WHERE id = {server_id}
            """)

def unsetAutorole(server_id:int):
    db.custom_insert(f"""UPDATE ServerConfigs SET
            role = Null
            WHERE id = {server_id}
            """)


def getAutorole(server_id:int):

    role = db.retrieve_value("ServerConfigs","role",["id",server_id])
    return role[0][0]



#################################Listen Channels#########################################

def IgnoreChannel(server_id:int,channel_id:int):
    db.custom_insert(f"""UPDATE ServerConfigs SET 
    listen_channels = array_remove(listen_channels,'{channel_id}')
    WHERE id={server_id}""")

def ListenChannel(server_id:int,channel_id:int):
    db.custom_insert(f"""UPDATE ServerConfigs SET 
    listen_channels = array_cat(listen_channels,'{{ {channel_id} }}')
    WHERE id={server_id}""")

def ListenThisChannel(server_id:int,channel_id:int):
    db.custom_insert(f"""UPDATE ServerConfigs SET 
    listen_channels = '{{"{channel_id}"}}' WHERE id={server_id}""")
    pass


def GetListen(server_id:int):
    return db.retrieve_value("ServerConfigs","listen_channels",["id",server_id])[0][0]

#################################Backup#########################################

def backup(table:str):
    """Returns a CSV file with the backup of the given table """

    tables = db.custom_retrieve("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    
    valid_table = False
    for t in tables:
        print(t[0])
        print(table)
        if(table==t[0]):
            valid_table = True
            continue
    
    if(not valid_table):
        return None
    
    o_path = path.join(getcwd(),f"{table}.csv")

    db.copy_to(o_path,table)
    return o_path


##############################################################################################
