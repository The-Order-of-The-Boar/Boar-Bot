import discord


def genEmbed(title:str,body:str,descp="Boar",color=990033):
    """Generates a embed with the given Title and Content"""
    embed = discord.Embed(title=title,description=descp,color=color)
    embed.add_field(name="Content", value=body, inline=False)
    
    return embed




def covertDateFormat(data:list,date_index:int):
    """Converts the date to the one that is used in the output, it recieves the return of a 
    query and the position that the date is on it """
    for i in range(len(data)):
        blocks = str(data[i][date_index]).split("-")
        data[i][date_index] = f"{blocks[2]}/{blocks[1]}"
    
    return data

def genTableString(data:list,row_names:list,width=20):
    
    
    table = "```md\n"

    table += f"{row_names[0]} ".ljust(3+width-len(row_names[1])) + f"{row_names[1]}\n"
    
    line = 0
    for row in data:
        if(line%2)==0: 
            table+="<><"
        else:
            table+="<< "
        line+=1

        table += f"{row[0]}:".ljust(width-len(str(row[1])),'-') + f"{row[1]}\n"
    
    table+= "```"


    return table


