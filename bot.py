##############################################################################################
import discord
from datetime import datetime

from Internals import commands
from Statistics import messages
import server



client = discord.Client(intents=discord.Intents.all())
#################################Start#####################################################
@client.event
async def on_ready():
    
    print("On")
    print(datetime.now())

#################################Guild Join#####################################################
@client.event
async def on_guild_join(guild):

    server.AddServer(guild.id,guild.text_channels)
    

#################################New Member##################################################
@client.event
async def on_member_join(member):

    welcome = server.GetWelcome(member.guild.id)
    welcome["message"] = welcome["message"].replace("<mention>",member.mention)
    await client.get_channel(welcome["channel"]).send(welcome["message"])



#################################Message#####################################################
@client.event
async def on_message(message):
    
    messages.CountMessage(message.guild.id)
    
    await commands.ParseMessage(message)







#################################Other Events################################################



##############################################################################################
token = open("token.txt", 'r',encoding="utf-8").read()
client.run(token)