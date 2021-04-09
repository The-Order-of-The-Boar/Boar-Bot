from PIL import Image
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

        if len(r_command) > 4:
            print(r_command)
            cor_esperada = (int(r_command[2]), int(r_command[3]), int(r_command[4]), 255)
            cor_alvo = (int(r_command[2]), int(r_command[3]), int(r_command[4]), 0)
        print(cor_esperada)
        print(cor_alvo)
        #cor_alvo = (255, 255, 255, 255)

        await attachment.save("tmp.png")
        img = Image.open("tmp.png").convert("RGBA")
        
        pixels = img.load()
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

            for A in pegar_lados(px, imgX, imgY):

                if pixels[A[0], A[1]] == cor_esperada:
                    checar.add((A[0], A[1]))


            pixels[px[0], px[1]] = cor_alvo

        img.save("saida.png")

        with open("saida.png", "rb") as fh:
            f = discord.File(fh, filename="saida.png")
        await message.channel.send(file=f)

    else:
        await message.channel.send("Por favor, mande uma imagem.")



def pegar_lados(pos:tuple, tamX, tamY):

    saida = []

    if ((pos[0] - 1) >= 0 and (pos[0] - 1) <= tamX):
        saida.append((pos[0] - 1, pos[1]))

    if ((pos[0] + 1) >= 0 and (pos[0] + 1) <= tamX):
        saida.append((pos[0] + 1, pos[1]))

    if ((pos[1] - 1) >= 0 and (pos[1] - 1) <= tamY):
        saida.append((pos[0], pos[1] - 1))

    if ((pos[1] + 1) >= 0 and (pos[1] + 1) <= tamY):
        saida.append((pos[0], pos[1] + 1))  

    return saida
