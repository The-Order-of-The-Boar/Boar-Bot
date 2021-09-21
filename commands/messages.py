##############################################################################################
import sys
sys.path.append(".")

from core.CRUD import db
from core import utils,comms
from datetime import datetime,timedelta

#################################General#########################################

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



async def UpdateMessages(message):

    args = comms.ParseArguments(message.content)

    date = datetime.strptime(args["d"], '%d/%m/%Y').date()
    
    if(date)>datetime.now().date():
        await message.channel.send("Não é possível definir a quantidade de mensagens do futuro")
        return
    if(int(args["a"])<0):
        await message.channel.send("Não é possível definir a quantidade de mensagens como negativa")
        return  

    db.insert_value("Messages",[message.guild.id,date,args['a']],
        additional=f"ON CONFLICT(Date,Server) DO UPDATE SET Num = {args['a']}")

    await message.channel.send(f"O número de mensagens do dia {args['d']} foi atualizado com sucesso para {args['a']}")


#################################Generic#########################################

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

#################################Commands#########################################

async def Today(message):
    mes = GetMessagesByDay(message.guild.id,datetime.now().date())
    await message.channel.send(f"Hoje foram enviadas {mes} mensagens neste servidor")

async def Yesterday(message):
    y_date = datetime.now().date() - timedelta(days=1)
    mes = GetMessagesByDay(message.guild.id,y_date)            
    await message.channel.send(f"Ontem foram enviadas {mes} mensagens neste servidor")

async def Back(message):

    r_command = message.content.split()

    back = 1
    try:
        back = int(r_command[2])
    except IndexError:
        pass

    if(back<0):
        await message.channel.send("Não há registros do futuro")
        return
    o_date = datetime.now().date() - timedelta(days=back)
    mes = GetMessagesByDay(message.guild.id,o_date)
    if(mes==0):
        await message.channel.send(f"Não há registro de mensagens de {back} dias atrás")
    else:
        await message.channel.send(f"{back} dias atrás foram enviadas {mes} mensagens neste servidor")

async def MessagesTable(message):

    r_command = message.content.split()
    page = 0
    ##Checks if the user specifies a page
    try:
        page = int(r_command[2])
    except IndexError:
        pass

        if(page)<0:
            await("Não há registros do futuro")
            return
    
    data = GetLastMessages(message.guild.id,start=page*10)
    
    if(len(data)==0):
        await message.channel.send("Dados insuficientes")
        return

    table = utils.genTableString(data,["Data","Mensagens"])

    embed = utils.genEmbed("Tabela de mensagens",table,descp="Quantidade de mensagens \nenviadas por dia no servidor")
    await message.channel.send(embed=embed,content=None)

async def GetMessageEmpireWeek(message,client):
    """Gets the amount of messages in all the Empire in the week of the given day"""


    r_command = message.content.split()

    w_ago = 0

    try:
        w_ago = int(r_command[2])
    except IndexError:
        pass

    if(w_ago)<0:
        await message.channel.send("Não há registros do futuro")
        return

    else:
        date = datetime.now().date() - timedelta(7*w_ago)

    

    #Gets the raw data with the messages from the week of the given day
    day_of_w = date.weekday()
    monday = date - timedelta(day_of_w)
    next_monday = monday + timedelta(days=7)

    data = db.custom_retrieve(f""" SELECT Server,Num 
            FROM MESSAGES WHERE Date >= '{monday}' AND Date < '{next_monday}'  
            ORDER BY Num DESC""")
    
    #Parses the raw data
    messages = {}
    for i in range(len(data)):
        if(data[i][0] in messages.keys()):
            messages[data[i][0]] += data[i][1]

                

        else:
            messages[data[i][0]] = data[i][1]

    if len(data)==0:
        await message.channel.send(f"Não há registro do ranking de {w_ago} semanas atrás")
        return

    table = utils.genTableServers(messages,client)
    embed = utils.genEmbed("Ranking de Servidores",table,descp="Ranking de servidores por mensagens \nenviadas essa semana")
    await message.channel.send(embed=embed,content=None)



async def Record(message):
    """Gets the days with the biggest amount of messages"""
    
    data = db.custom_retrieve(f"SELECT date,num FROM Messages WHERE server = {message.guild.id} ORDER BY num DESC LIMIT 20 ")

    table = utils.genTableString(data,["Data","Mensagens"])
    embed = utils.genEmbed("Tabela de Recordes",table,descp="Dias com os maiores recordes \nde mensagens enviadas ")

    await message.channel.send(embed=embed,content=None)

async def AntiRecord(message):
    """Gets the days with the smallest amount of messages"""

    data = db.custom_retrieve(f"SELECT date,num FROM Messages WHERE server = {message.guild.id} ORDER BY num LIMIT 20 ")

    table = utils.genTableString(data,["Data","Mensagens"])
    embed = utils.genEmbed("Tabela de Anti-Recordes",table,descp="Dias com os menores números \nde mensagens enviadas ")

    await message.channel.send(embed=embed,content=None)

async def Average(message):
    """Gets the daily messages average from the given amount of days ago"""

    d_ago = 7


    try:
        r_command = message.content.split()
        d_ago = int(r_command[2])
        if(d_ago<1):
            await message.channel.send("Não é possível calcular a média de dias futuros")
            return
    except :
        pass

    avg = db.custom_retrieve(f"""
    SELECT ROUND(AVG(num))::INTEGER FROM 
    (SELECT num FROM Messages WHERE server = {message.guild.id} ORDER BY date DESC LIMIT {d_ago} ) as mes_num""")[0][0]

    await message.channel.send(f"A média de mensagens dos últimos {d_ago} dias é de {avg}")
