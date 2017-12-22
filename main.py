import discord
import grimbot

client = discord.Client()

cmdManager = grimbot.CommandManager("!")

@client.event
async def on_message(message: discord.Message):
    try:
        await cmdManager.execute(message.content, client, message)
    except grimbot.CommandArgsPatternDoesntMatchException as ex:
        await client.send_message(message.channel, ex.message)
    except grimbot.CommandLengthDoesntMatchException as ex:
        await client.send_message(message.channel, str(ex))

cmdManager.commands.append(
    grimbot.RainCommand(
        "rain",
        [
            grimbot.PositiveNumberArgsPattern()
        ]
    )
)

client.run('MzkzNTcwMzQzODAyODk2Mzg1.DR3s9Q.t6VyMgrZTCWaVIvz9rWRw0ggnaU')