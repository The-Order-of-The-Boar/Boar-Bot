##############################################################################################
from core.CRUD import db
from core import comms
from os import getcwd,path
from discord import File


#################################General#########################################

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

def getAutorole(server_id:int):

    role = db.retrieve_value("ServerConfigs","role",["id",server_id])
    return role[0][0]

#################################Welcome#########################################


async def SetWelcome(message):

    args = comms.ParseArguments(message.content)

    text = args["t"].split('"')[1]
    text = text.replace("¬","-")

    db.custom_insert(f"""UPDATE ServerConfigs SET
    welcome_channel={message.channel.id},
    welcome_message='{text}'
    WHERE id = {message.guild.id}
     """)

    await message.channel.send(f"""A partir de agora este é o canal de recepção,com a seguinte mensagem: `{text}`""")



    
async def UnsetWelcome(message):


    db.custom_insert(f"""UPDATE ServerConfigs SET
    welcome_channel= NULL ,
    welcome_message= NULL
    WHERE id = {message.guild.id}
     """)

    await message.channel.send("O sistema de recepção de membros foi desativado com sucesso")
    

def GetWelcome(server_id:int):

    welcome = {}
    welcome["channel"],welcome["message"] = db.retrieve_value("ServerConfigs","welcome_channel,welcome_message",["id",server_id])[0]

    return welcome


#################################Autorole#########################################

async def SetAutorole(message):

    args = comms.ParseArguments(message.content)

    role_id = int(args["r"])
    role = message.guild.get_role(role_id)

    if(role == None):
        await message.channel.send("ID inválido")
        return

    role_id = int(args["r"])

    
    db.custom_insert(f"""UPDATE ServerConfigs SET
            role = {role_id}
            WHERE id = {message.guild.id}
            """)
    
    await message.channel.send(f"A partir de agora todos os novos membros receberão o cargo {role.name}")

async def UnsetAutorole(message):
    db.custom_insert(f"""UPDATE ServerConfigs SET
            role = Null
            WHERE id = {message.guild.id}
            """)

    await message.channel.send("O sistema de autorole foi desativado com sucesso")





#################################Listen Channels#########################################

async def IgnoreChannel(message):
    db.custom_insert(f"""UPDATE ServerConfigs SET 
    listen_channels = array_remove(listen_channels,'{message.channel.id}')
    WHERE id={message.guild.id}""")

    await message.channel.send("A partir de agora ignorarei comandos neste canal")

async def ListenChannel(message):
    db.custom_insert(f"""UPDATE ServerConfigs SET 
    listen_channels = array_cat(listen_channels,'{{ {message.channel.id} }}')
    WHERE id={message.guild.id}""")

    await message.channel.send("A partir de agora receberei comandos neste canal")

async def ListenThisChannel(message):
    db.custom_insert(f"""UPDATE ServerConfigs SET 
    listen_channels = '{{"{message.channel.id}"}}' WHERE id={message.guild.id}""")

    await message.channel.send("A partir de agora receberei comandos exclusivamente neste canal")


def GetListen(server_id:int):
    return db.retrieve_value("ServerConfigs","listen_channels",["id",server_id])[0][0]

#################################Backup#########################################

def GetBackup(table:str):
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

async def Backup(message):

    args = comms.ParseArguments(message.content)

    table = args["t"].split('"')[1]
    backup = GetBackup(table)

    if(backup==None):
        await message.channel.send("Tabela inexistente")
    else:
        await message.channel.send(f"Backup da tabela {table}",file=File(backup))


##############################################################################################
