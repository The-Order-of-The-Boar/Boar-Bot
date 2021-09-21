from requests import get
from datetime import datetime
import discord
import remove_boar


async def Boar(message):
    await message.channel.send("Ninguém é maior que o Javali!!!!")

async def Capital(message):
    await message.channel.send("Junte-se aos nossos desenvolvedores em Vai-Quem-Quer, nossa Capital: https://discord.gg/wH44qTp")

async def Ctest(message):
    import ctypes
    test = ctypes.CDLL("libtest.so")

    test.disc_test.restype = ctypes.c_char_p
    a = test.disc_test().decode()

    await message.channel.send(a)

async def first500(message):
    if (not message.guild.id == 272166101025161227):
        return
    
    date500 = datetime(2021, 5, 10, 23, 10)
    if(message.author.joined_at < date500):   
        role = message.guild.get_role(841500835409952818)
        await message.author.add_roles(role)
        await message.channel.send("Parabéns camarada! Você está apto a receber o cargo dos primeiros 500 camaradas a pisarem em Vai-Quem-Quer!")
    else:
        await message.channel.send("Seu pilantra! Você não é um dos 500 primeiros camaradas :rage: ")

async def BackgroundRemover(message):
    if len(message.attachments) > 0:
        attachment = message.attachments[0]
    else:
        await message.channel.send("Mande uma imagem em anexo, por favor.")
        return
    
    if attachment.filename.endswith(".jpg") or attachment.filename.endswith(".jpeg") or attachment.filename.endswith(".png") or attachment.filename.endswith(".webp") or attachment.filename.endswith(".gif"):
        await message.channel.send("Processando...")
        r_command = message.content.split()

        await attachment.save("images/tmp.png")
        remove_boar.background_remover("images/tmp.png")
        with open("images/saida.png", "rb") as fh:
            f = discord.File(fh, filename="images/saida.png")
        await message.channel.send(file=f)
    else: 
        await message.channel.send("Por favor, mande uma imagem.")

def DownloadImage(url:str):
    image = get(url).content
    file = open("images/tmp.png","wb")
    file.write(image)

def WelcomeImage(username:str,image:str,server:int):
    DownloadImage(image)
    base = Image.open(f"images/back{server}.png")
    user = Image.open("images/tmp.png").resize((128,128))
    base.paste(user,(20,348))
    base.save(f"images/{username}.png")
