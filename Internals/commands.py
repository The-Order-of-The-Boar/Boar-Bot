import discord
from datetime import datetime,timedelta
from time import time
from os import environ

from Management import server
from Statistics import messages,rank
from Internals import utils

prefix = {"std":"b","mod":"bm"}
#Defines the prefix accordingly to the bot host
if(not "DYNO" in environ):
    prefix = {"std":"d","mod":"dm"}


            
            



async def ParseCommand(message,client):


    start_t = time()
    ########################Raw data parsing
    r_command = message.content.split()
    
    #Returns if doesn't have the command 
    if(len(r_command)<2):
        return


    c_prefix = r_command[0]
    command = r_command[1]

    s_id = message.guild.id
    c_id = message.channel.id


    ########################Ignore cases



    #If the message was sent in a ignored channel
    if(not c_id in server.GetListen(s_id) and c_prefix==prefix["std"]):
        return

    #If doesn't have the command prefix
    if(len(c_prefix)>2 or not c_prefix  in prefix.values()):
        return
    


    args = {}
    #Parses the optional arguments as a dictionary
    if(len(r_command)>2):
        

        #Searchs for a text argument and replaces "-" in order to don't split texts
        inside_text = False
        start = len(r_command[0])+len(r_command[1])
        for i in range(start,len(message.content)):
            if(message.content[i]=='"'):
                inside_text = not inside_text
            elif(message.content[i]=='-' and inside_text):
                message.content = message.content[:i]+"¬"+message.content[i+1:]



        #Splits the command text using "-", geting the arg name and it's value
        r_args = message.content.split("-")[1:]

        for arg in r_args:

            #Arg with no value
            if(len(arg)==1 or arg[1]==' '):
                args[arg[0]] = 0
            #Arg with  value
            else:
                args[arg[0]] = arg[1:]
                if(not arg[0]=="t"):#Remove spaces from args that aren't text
                    args[arg[0]] = args[arg[0]].replace(' ','')

    
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
            
            text = args["t"].split('"')[1]
            text = text.replace("¬","-")
            server.SetWelcome(s_id,c_id,text)
            await message.channel.send(f"""A partir de agora este é o canal de recepção,com a seguinte mensagem: `{text}`""")
        
        elif(command=="remWelcome"):


            server.UnsetWelcome(s_id)
            await message.channel.send("O sistema de recepção de membros foi desativado com sucesso")

        ##Autorole
        elif(command=="setAutorole"):
            
            role_id = int(args["r"])
            role = client.get_guild(s_id).get_role(role_id)

            if(role == None):
                await message.channel.send("ID inválido")
                return

            role_id = int(args["r"])
            server.setAutorole(s_id,role_id)
            await message.channel.send(f"A partir de agora todos os novos membros receberão o cargo {role.name}")

        elif(command=="unsetAutorole"):

            server.unsetAutorole(s_id)
            await message.channel.send("O sistema de autorole foi desativado com sucesso")
        


        ##Listen and Ignore
        elif(command=="ignoreChannel"):
            
            server.IgnoreChannel(s_id,c_id)
            await message.channel.send("A partir de agora ignorarei comandos neste canal")
        
        elif(command=="listenChannel"):
            
            server.ListenChannel(s_id,c_id)
            await message.channel.send("A partir de agora receberei comandos neste canal")
        
        elif(command=="listenHere"):
            
            server.ListenThisChannel(s_id,c_id)
            await message.channel.send("A partir de agora receberei comandos exclusivamente neste canal")

        ##Statistics Management

        elif(command=="setMessagesDay"):

            date = datetime.strptime(args["d"], '%d/%m/%Y').date()
            
            if(date)>datetime.now().date():
                await message.channel.send("Não é possível definir a quantidade de mensagens do futuro")
                return
            if(int(args["a"])<0):
                await message.channel.send("Não é possível definir a quantidade de mensagens como negativa")
                return  

            messages.UpdateMessages(s_id,date,args["a"])
            await message.channel.send(f"O número de mensagens do dia {args['d']} foi atualizado com sucesso para {args['a']}")

            
            





        
    
    

    #######General Commands
    if(command=="boar" or command=="Boar"):
        await message.channel.send("Ninguém é maior que o Javali!!!!")
    
    elif(command=="capital"):
        await message.channel.send("Junte-se aos nossos desenvolvedores em Vai-Quem-Quer, nossa Capital: https://discord.gg/wH44qTp")


    ###############################################Statistics Commands

    ########################Messages
    elif(command=="today"):
        
        mes = messages.GetMessagesByDay(s_id,datetime.now().date())
        await message.channel.send(f"Hoje foram enviadas {mes} mensagens neste servidor")
    
    elif(command=="yesterday"):
        
        y_date = datetime.now().date() - timedelta(days=1)
        mes = messages.GetMessagesByDay(s_id,y_date)            
        await message.channel.send(f"Ontem foram enviadas {mes} mensagens neste servidor")

    elif(command=="back"):
        
        back = int(args["b"])
        if(back<0):
            await message.channel.send("Não há registros do futuro")
            return
        o_date = datetime.now().date() - timedelta(days=back)
        mes = messages.GetMessagesByDay(s_id,o_date)
        if(mes==0):
            await message.channel.send(f"Não há registro de mensagens de {back} dias atrás")
        else:
            await message.channel.send(f"{back} dias atrás foram enviadas {mes} mensagens neste servidor")

    elif(command=="table"):


        ##Checks if the user specifies a page
        page = 0
        if("b" in args.keys()):
            page = int(args["b"])

            if(page)<0:
                await("Não há registros do futuro")
                return
        
        data = messages.GetLastMessages(s_id,start=page*10)
        
        if(len(data)==0):
            await message.channel.send("Dados insuficientes")
            return

        table = utils.genTableString(data,["Data","Mensagens"])

        embed = utils.genEmbed("Tabela de mensagens",table,descp="Quantidade de mensagens \nenviadas por dia no servidor")
        await message.channel.send(embed=embed,content=None)
    
    ########################Ranks
    elif(command=="rank"):

        d_ago = 0
        points = "mensagens"
        if("c" in args.keys()):
            points = "caracteres"
        if("b" in args.keys()):
            d_ago = int(args["b"])
            if(d_ago)<0:
                await message.channel.send("Não há registros do futuro")
                return


        
        data = rank.getRankByWeek(s_id,points[0],ago=d_ago)
        
        if len(data)==0:
            await message.channel.send(f"Não há registro do ranking de {d_ago} semanas atrás")
            return


        table = utils.genTableRank(data,message.guild,client) 
        embed = utils.genEmbed("Ranking",table,descp=f"Ranking de membros por {points} \nenviadas na semana")
        if("n" in args.keys()):
            end_t = round((time() - start_t)*1000,6)
            await message.channel.send(f"`O comando foi executado em {end_t}ms`")
        await message.channel.send(embed=embed,content=None)

    elif(command=="serverRank"):

        if("b" in args.keys()):
            d_ago = int(args["b"])
            if(d_ago)<0:
                await message.channel.send("Não há registros do futuro")
                return

            date = datetime.now().date() - timedelta(7*d_ago)
        else:
            date = datetime.now().date()

        
        data = messages.GetMessageEmpireWeek(date)
        if len(data)==0:
            await message.channel.send(f"Não há registro do ranking de {d_ago} semanas atrás")
            return

        table = utils.genTableServers(data,client)
        embed = utils.genEmbed("Ranking de Servidores",table,descp="Ranking de servidores por mensagens \nenviadas essa semana")
        await message.channel.send(embed=embed,content=None)

    elif(command == "cTest"):

        import ctypes
        test = ctypes.CDLL("libtest.so")

        test.disc_test.restype = ctypes.c_char_p
        a = test.disc_test().decode()

        await message.channel.send(a)
    


    if("m" in args.keys()):
        end_t = round((time() - start_t)*1000,6)
        await message.channel.send(f"`O comando foi executado em {end_t}ms`")
