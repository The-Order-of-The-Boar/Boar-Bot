#################################Server Management#####################################################
from Internals.CRUD import db


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
    """Creates the ServerConfigs table, not to be used regularly, but stays as a reference"""
    db.create_table("ServerConfigs",[
        ["id", " BIGINT PRIMARY KEY"],
        ["listen_channels", " BIGINT[]"],
        ["welcome_channel", " BIGINT"],
        ["welcome_message", " VARCHAR(200)"]
        ])

#################################Welcome#########################################


def SetWelcome(server_id:int,channel_id:int,message:str="Seja Bem-vindo"):

    db.custom_insert(f"""UPDATE ServerConfigs SET
    welcome_channel={channel_id},
    welcome_message='{message}'
    WHERE id = {server_id}
     """)
    

def GetWelcome(server_id:int):

    welcome = {}
    welcome["channel"] = db.retrieve_value("ServerConfigs","welcome_channel",["id",server_id])[0][0]
    welcome["message"] = db.retrieve_value("ServerConfigs","welcome_message",["id",server_id])[0][0]

    return welcome

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



    


##############################################################################################
