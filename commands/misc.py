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