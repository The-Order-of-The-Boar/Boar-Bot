##############################################################################################
import discord
from datetime import datetime
import sys
from psycopg2.errors import ForeignKeyViolation




client = discord.Client(intents=discord.Intents.all())
from commands import messages
from commands import rank
from commands import server
from commands import misc
from core import comms
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
        
        #Welcome image in the capital
        image = None
        if(member.guild.id == 272166101025161227):
            misc.WelcomeImage(member.nick,member.avatar_url,member.guild.id)
            image=discord.File(f"images/{member.nick}.png")
    
        welcome["message"] = welcome["message"].replace("<mention>",member.mention)
        await client.get_channel(welcome["channel"]).send(welcome["message"],file=image)
    

    #Autorole  if exists
    role_id = server.getAutorole(server_id)
    if (not role_id == None):
        guild = client.get_guild(server_id)
        role = guild.get_role(role_id)
        await member.add_roles(role)




#################################Message#####################################################
@client.event
async def on_message(message):
    try:
        messages.CountMessage(message.guild.id)
        if(message.channel.id != 770107741585932339):
            char_amount = len(message.content) - message.content.count(" ")
            rank.countPoints(message.guild.id,message.author.id,char_amount)
    except ForeignKeyViolation:
        print("Reinvite the bot to the server!")
        await message.channel.send("Reinvite the bot to the server!")
        
        sys.exit()
    #Ignores bot commands and rank
    if message.author.bot:
        return

    await comms.ParseCommand(message,client)


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
