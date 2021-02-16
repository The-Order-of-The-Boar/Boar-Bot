##############################################################################################
from core.CRUD import db
from core import comms,utils
from datetime import datetime,timedelta
import sys

#################################General#########################################

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

    #Limits the amount of points from one message to 100
    chars = min(chars,100)

    db.custom_insert(f"""INSERT INTO Rank 
    VALUES ({user_id},{server_id},'{date}',1,{chars}) 
    ON CONFLICT(user_id,server_id,date) DO UPDATE SET 
    messages = Rank.messages+1,chars = Rank.chars+{chars} """)

def GenTableRank(r_data:list,guild,client):
    """Preparates the data to generate a Rank Table,then call the generic generator """
    
    #Formats the raw data in order to send to the generic table generator
    data = []

    

    for i,user in enumerate(r_data):

        #Gets the name in of three cases:User in guild with nick;without nick;without guild
        try:
            member = (guild.get_member(user[0]))
            if member != None:
                name = member.nick
                if name == None:
                    name = client.get_user(user[0]).name
            else:
                name = client.get_user(user[0]).name

            if(len(name)>22):
                name = name[:21]+"."

            messages = user[1]

            name = utils.replaceImmoralChars(name)
            data.append([f"{i+1}-{name}",messages])
        except:
            exp = sys.exc_info()
            print(exp)
            print(f"Error with user {user[0]}")


    return utils.genTableString(data,["Membro","Pontos"],width=35)


#################################Commands#########################################


async def getRankByWeek(message,client):

    args = comms.ParseArguments(message.content)

    d_ago = 0
    points = "messages"
    if args != None:
        if("c" in args.keys()):
            points = "chars"
        if("b" in args.keys()):
            d_ago = int(args["b"])
            if(d_ago)<0:
                await message.channel.send("Não há registros do futuro")
                return

    date  = datetime.now().date()
    date -= timedelta(days=date.weekday()+(d_ago*7))


    data = db.custom_retrieve(f""" SELECT user_id,{points}
            FROM Rank WHERE date = '{date}' AND server_id = {message.guild.id}  
            ORDER BY {points} DESC LIMIT 20""")


    if len(data)==0:
        await message.channel.send(f"Não há registro do ranking de {d_ago} semanas atrás")
        return

    if(points=="messages"):
        points = "mensagens"
    elif(points=="chars"):
        points = "caracteres"

    table = GenTableRank(data,message.guild,client) 
    embed = utils.genEmbed("Ranking",table,descp=f"Ranking de membros por {points} \nenviadas na semana")
    await message.channel.send(embed=embed,content=None)



