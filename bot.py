##############################################################################################
import discord
from datetime import datetime

from Internals import commands
from Statistics import messages,rank
from Management import server





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

    server_id = member.guild.id

    #Welcome message if exists
    welcome = server.GetWelcome(server_id)
    if (not welcome["message"] == None):
        welcome["message"] = welcome["message"].replace("<mention>",member.mention)
        await client.get_channel(welcome["channel"]).send(welcome["message"])
    

    #Autorole  if exists
    role_id = server.getAutorole(server_id)
    if (not role_id == None):
        guild = client.get_guild(server_id)
        role = guild.get_role(role_id)
        await member.add_roles(role)




#################################Message#####################################################
@client.event
async def on_message(message):
    
    messages.CountMessage(message.guild.id)

    #Ignores bot commands and rank
    if message.author.bot:
        return

    if(message.channel.id != 770107741585932339):
        rank.countPoints(message.guild.id,message.author.id,len(message.content))
    await commands.ParseCommand(message,client)


@client.event
async def on_message_delete(message):



    messages.UncountMessage(message)




#################################Other Events################################################



##############################################################################################



from os import environ

token = "" 
if("DYNO" in environ):
    token = environ['TOKEN']
else:
    token = open("localToken.txt", 'r',encoding="utf-8").read()

client.run(token)