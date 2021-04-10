from PIL import Image
from requests import get
import discord

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

async def BackgroundRemover(message):
    if len(message.attachments) > 0:
        attachment = message.attachments[0]
    else:
        await message.channel.send("Mande uma imagem em anexo, por favor.")
        return
    
    if attachment.filename.endswith(".jpg") or attachment.filename.endswith(".jpeg") or attachment.filename.endswith(".png") or attachment.filename.endswith(".webp") or attachment.filename.endswith(".gif"):
        await message.channel.send("Processando...")
        r_command = message.content.split()

        cor_esperada = (255, 255, 255, 255)
        cor_alvo = (255, 255, 255, 0)

        await attachment.save("images/tmp.png")
        img = Image.open("images/tmp.png").convert("RGBA")
        
        pixels = img.load()

        if len(r_command) > 4:
            print(r_command)
            cor_esperada = (int(r_command[2]), int(r_command[3]), int(r_command[4]), 255)
        else:
            cor_esperada = img.getpixel((0,0))

        cor_alvo = (0,0,0,0)
        print(cor_esperada)
        print(cor_alvo)
        #cor_alvo = (255, 255, 255, 255)

        imgX, imgY = img.size
        imgX, imgY = imgX-1, imgY-1

        checar = set()

        for A in range(imgX+1):

            if pixels[A, 0] == cor_esperada:
                checar.add((A, 0))

            if pixels[A, imgY] == cor_esperada:
                checar.add((A, imgY))

        for A in range(imgY+1):

            if pixels[0, A] == cor_esperada:
                checar.add((0, A))

            if pixels[imgX, A] == cor_esperada:
                checar.add((imgX, A))

        while len(checar) > 0:

            px = checar.pop()

            if pixels[px[0], px[1]] == cor_alvo:
                checar.pop(0)
                continue

            for A in GetSides(px, imgX, imgY):

                if pixels[A[0], A[1]] == cor_esperada:
                    checar.add((A[0], A[1]))


            pixels[px[0], px[1]] = cor_alvo

        img.save("images/saida.png")

        with open("images/saida.png", "rb") as fh:
            f = discord.File(fh, filename="images/saida.png")
        await message.channel.send(file=f)

    else:
        await message.channel.send("Por favor, mande uma imagem.")


def GetSides(pos:tuple, tamX:int, tamY:int):

    output = []

    if ((pos[0] - 1) >= 0 and (pos[0] - 1) <= tamX):
        output.append((pos[0] - 1, pos[1]))

    if ((pos[0] + 1) >= 0 and (pos[0] + 1) <= tamX):
        output.append((pos[0] + 1, pos[1]))

    if ((pos[1] - 1) >= 0 and (pos[1] - 1) <= tamY):
        output.append((pos[0], pos[1] - 1))

    if ((pos[1] + 1) >= 0 and (pos[1] + 1) <= tamY):
        output.append((pos[0], pos[1] + 1))  

    return output

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