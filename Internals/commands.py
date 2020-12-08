import discord
from datetime import datetime,timedelta
from os import environ

import server
from Statistics import messages
from Internals import utils

async def ParseMessage(message):

    s_id = message.guild.id
    c_id = message.channel.id

    prefix = {"std":"b","mod":"bm"}

    #Defines the prefix accordingly to the bot host
    if("DYNO" in environ):
        prefix = {"std":"d","mod":"dm"}

    #Returns if doesn't have the command prefix
    if(not message.content.startswith(prefix["std"])):
        return

    com = message.content.split()
    #Returns if doesn't have the command 
    if(len(com)<2):
        return
    
    ######Management Commands
    #Check if it's a management command and if the user has enough permissions
    if(com[0]==prefix["mod"]):
        manager = message.author.permissions_in(message.channel).manage_channels

        if (not manager):
            await message.channel.send("Permissões insuficientes")
            return
        ##Welcome
        if(com[1]=="setWelcome"):
            
            mes = message.content.split('"')[1]
            server.SetWelcome(s_id,c_id,mes)
            await message.channel.send(f"""A partir de agora este é o canal de recepção,com a seguinte mensagem: `{mes}`""")
        
        ##Listen and Ignore
        elif(com[1]=="ignoreChannel"):
            
            server.IgnoreChannel(s_id,c_id)
            await message.channel.send("A partir de agora ignorarei comandos neste canal")
        
        elif(com[1]=="listenChannel"):
            
            server.ListenChannel(s_id,c_id)
            await message.channel.send("A partir de agora receberei comandos neste canal")
        
        elif(com[1]=="listenHere"):
            
            server.ListenThisChannel(s_id,c_id)
            await message.channel.send("A partir de agora receberei comandos exclusivamente neste canal")

        ##Statistics Management

        elif(com[1]=="setMessagesDay"):

            messages.UpdateMessages(s_id,com[3],com[2])
            await message.channel.send(f"O número de mensagens do dia {com[3]} foi atualizado com sucesso para {com[2]}")


            
            





        
    
    #Returns if the message was sent in a ignored channel
    if(not c_id in server.GetListen(s_id)):
        return
    
    #Returns if it's another word that starts with b
    if(com[0]!="b"):
        return
    

    #######General Commands
    if(com[1]=="boar" or com[1]=="Boar"):
        await message.channel.send("Ninguém é maior que o Javali!!!!")
    
    elif(com[1]=="capital"):
        await message.channel.send("Junte-se aos nossos desenvolvedores em Vai-Quem-Quer, nossa Capital: https://discord.gg/wH44qTp")


    #######Statistics Commands
    elif(com[1]=="today"):
        
        mes = messages.GetMessagesByDay(s_id,datetime.now().date())
        await message.channel.send(f"Hoje foram enviadas {mes} mensagens neste servidor")
    
    elif(com[1]=="yesterday"):
        
        y_date = datetime.now().date() - timedelta(days=1)
        mes = messages.GetMessagesByDay(s_id,y_date)            
        await message.channel.send(f"Ontem foram enviadas {mes} mensagens neste servidor")

    elif(com[1]=="back"):
        
        back = int(com[2])
        o_date = datetime.now().date() - timedelta(days=back)
        mes = messages.GetMessagesByDay(s_id,o_date)
        if(mes==0):
            await message.channel.send(f"Não há registro de mensagens de {back} dias atrás")
        else:
            await message.channel.send(f"{back} dias atrás foram enviadas {mes} mensagens neste servidor")

    elif(com[1]=="table"):


        ##Checks if the user specifies a page
        if(len(com)>2):
            data = messages.GetLastMessages(s_id,start=(int(com[2])-1)*10)
        else:
            data = messages.GetLastMessages(s_id)
        
        if(len(data)==0):
            await message.channel.send("Dados insuficientes")
            return

        table = utils.genTableString(data,["Data","Mensagens"])

        embed = utils.genEmbed("Tabela de mensagens",table,descp="Quantidade de mensagens \nenviadas por dia no servidor")
        await message.channel.send(embed=embed,content=None)

