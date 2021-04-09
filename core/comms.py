import discord
from requests import get
from datetime import datetime,timedelta
from time import time
from os import environ

from commands import messages,rank,server,misc

prefix = {"std":"b","mod":"bm"}
#Defines the prefix accordingly to the bot host
if(not "DYNO" in environ):
    prefix = {"std":"d","mod":"dm"}


            
def ParseArguments(message:str):
    args = {}
    #Parses the optional arguments as a dictionary
    r_command = message.split()
    if(len(r_command)>2):
        

        #Searchs for a text argument and replaces "-" in order to don't split texts
        inside_text = False
        start = len(r_command[0])+len(r_command[1])
        for i in range(start,len(message)):
            if(message[i]=='"'):
                inside_text = not inside_text
            elif(message[i]=='-' and inside_text):
                message = message[:i]+"¬"+message[i+1:]



        #Splits the command text using "-", geting the arg name and it's value
        r_args = message.split("-")[1:]

        for arg in r_args:

            #Arg with no value
            if(len(arg)==1 or arg[1]==' '):
                args[arg[0]] = 0
            #Arg with  value
            else:
                args[arg[0]] = arg[1:]
                if(not arg[0]=="t"):#Remove spaces from args that aren't text
                    args[arg[0]] = args[arg[0]].replace(' ','')
        
        return args

async def ParseCommand(message,client):


    start_t = time()
    ########################Raw data parsing
    r_command = message.content.split()
    
    #Returns if doesn't have the command 
    if(len(r_command)<2):
        return


    c_prefix = r_command[0]
    command = r_command[1]



    ########################Ignore cases



    #If the message was sent in a ignored channel
    if(not message.channel.id in server.GetListen(message.guild.id) and c_prefix==prefix["std"]):
        return

    #If doesn't have the command prefix
    if(len(c_prefix)>2 or not c_prefix  in prefix.values()):
        return
    


    
    ########################Command matching
    
    ###############################################Management Commands
    #Check if it's a management command and if the user has enough permissions
    if(c_prefix==prefix["mod"]):
        manager = message.author.permissions_in(message.channel).manage_channels

        if (not manager):
            await message.channel.send("Permissões insuficientes")
            return

        ##Welcome
        if(command=="setWelcome"):
            
            await server.SetWelcome(message)
        
        elif(command=="remWelcome"):

            await server.UnsetWelcome(message)

        ##Autorole
        elif(command=="setAutorole"):
            
            await server.SetAutorole(message)

        elif(command=="unsetAutorole"):

            await server.UnsetAutorole(message)
            
        ##Listen and Ignore
        elif(command=="ignoreChannel"):
            
            await server.IgnoreChannel(message)
        
        elif(command=="listenChannel"):
            
            await server.ListenChannel(message)
        
        elif(command=="listenHere"):
            
            await server.ListenThisChannel(message)
            
        ##Statistics Management

        elif(command=="setMessagesDay"):

            await messages.UpdateMessages(message)


    ###############################################Misc Commands
    if(command=="boar" or command=="Boar"):
        await misc.Boar(message)
    
    elif(command=="capital"):
        await misc.Capital(message)
    
    elif(command == "cTest"):

        await misc.Ctest(message)

    elif(command=="backup"):

        await server.Backup(message)


    ###############################################Messages Commands

    elif(command=="today"):
        
        await messages.Today(message)
    
    elif(command=="yesterday"):
        
        await messages.Yesterday(message)

    elif(command=="back"):
        
        await messages.Back(message)

    elif(command=="table"):

        await messages.MessagesTable(message)
    
    elif(command=="record"):

        await messages.Record(message)

    elif(command=="average"):
        
        await messages.Average(message)

    ###############################################Rank Commands
    elif(command=="rank"):

        await rank.getRankByWeek(message,client)

    elif(command=="serverRank"):

        await messages.GetMessageEmpireWeek(message,client)
    
    elif(command=="remove"):

        await misc.BackgroundRemover(message)




    if("-m" in message.content):
        end_t = round((time() - start_t)*1000,6)
        await message.channel.send(f"`O comando foi executado em {end_t}ms`")
