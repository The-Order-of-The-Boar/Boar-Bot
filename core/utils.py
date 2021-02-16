import discord
from dateutil import tz
from datetime import datetime
from json import loads
import sys



##########################################Generators############################################
def genEmbed(title:str,body:str,descp="Boar",color=990033):
    """Generates a embed with the given Title and Content"""
    embed = discord.Embed(title=title,description=descp,color=color)
    embed.add_field(name="Content", value=body, inline=False)
    
    return embed

immoral_chars = loads(open("immoral_chars.json", 'r',encoding="utf-8").read())

def replaceImmoralChars(word:str):

    forbidden_chars = ["#","`","<"]
    
    for char in forbidden_chars:
        word = word.replace(char,"")

    for char in immoral_chars.keys():
        word = word.replace(char,immoral_chars[char])



    return word




def genTableServers(r_data:dict,client):
    """Preparates the data to generate a Server Table,then call the generic generator """


    #Formats the raw data in order to send to the generic table generator
    data = []

    for server in sorted(r_data.items(), key=lambda item: item[1],reverse=True):
        name = client.get_guild(server[0]).name
        messages = server[1]

        data.append([name,messages])

    return genTableString(data,["Servidor","Mensagens"],width=40)


def genTableString(data:list,row_names:list,width:int=20):
    """Generates a generic string in the form of a table in order to the sent """
    
    
    table = "```md\n"

    table += f"  {row_names[0]} ".ljust(width-len(row_names[1])) + f"{row_names[1]}\n"
    
    
    line = 0
    for row in data:
        
        #Char that formats the row
        if(line%2)==0: 
            f_c =["# "," #"]
        else:
            f_c =["< "," >"]
        line+=1

        table += f"{f_c[0]}{row[0]}:".ljust(width-len(str(row[1])),'-') + f"{row[1]}{f_c[1]}\n"
    
    table+= "```"

    return table

##########################################Conversors############################################

def utcToLocal(utc:datetime):

    utc = utc.replace(tzinfo=tz.tzutc())
    local = utc.astimezone(tz.tzlocal())

    return local


##########################################Misc############################################



            

        


