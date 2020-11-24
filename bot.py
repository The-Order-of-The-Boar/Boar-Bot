##############################################################################################
import discord
from datetime import datetime

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
    await client.get_channel(welcome["channel"]).send(welcome["message"])

#################################Message#####################################################
@client.event
async def on_message(message):
    
    s_id = message.guild.id
    c_id = message.channel.id

    #Returns if doesn't have the command prefix
    if(not message.content.startswith("b")):
        return

    com = message.content.split()
    #Returns if doesn't have the command 
    if(len(com)<2):
        return
    
    
    #Management commands
    manager = message.author.permissions_in(message.channel).manage_channels
    if(com[1]=="setWelcome"):
        if(not manager):
            await message.channel.send("Permissões insuficientes")
            return
        
        mes = message.content.split('"')[1]
        server.SetWelcome(s_id,c_id,mes)
        await message.channel.send(f"""A partir de agora este é o canal de recepção,com a seguinte mensagem: `{mes}`""")
    
    elif(com[1]=="ignoreChannel"):
        if(not manager):
            await message.channel.send("Permissões insuficientes")
            return
        
        server.IgnoreChannel(s_id,c_id)
        await message.channel.send("A partir de agora ignorarei comandos neste canal")
    
    elif(com[1]=="listenChannel"):
        if(not manager):
            await message.channel.send("Permissões insuficientes")
            return
        
        server.ListenChannel(s_id,c_id)
        await message.channel.send("A partir de agora receberei comandos neste canal")
    
    elif(com[1]=="listenHere"):
        if(not manager):
            await message.channel.send("Permissões insuficientes")
            return
        
        server.ListenThisChannel(s_id,c_id)
        await message.channel.send("A partir de agora receberei comandos exclusivamente neste canal")

    #Returns if the message was sent in a ignored channel
    if(not c_id in server.GetListen(s_id)):
        return
    

    #General Commands
    if(com[1]=="boar" or com[1]=="Boar"):
        await message.channel.send("Ninguém é maior que o Javali!!!!")
    elif(com[1]=="capital"):
        await message.channel.send("Junte-se aos nossos desenvolvedores em Vai-Quem-Quer, nossa Capital: https://discord.gg/wH44qTp")






#################################Other Events################################################



##############################################################################################
token = open("token.txt", 'r',encoding="utf-8").read()
client.run(token)