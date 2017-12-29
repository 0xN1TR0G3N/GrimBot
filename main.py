import discord
import grimbot

client = discord.Client()

cmdManager = grimbot.CommandManager("!")

@client.event
async def on_message(message: discord.Message):
    if len(message.content) == 0:
        return
    try:
        await cmdManager.execute(message.content, client, message)
    except grimbot.CommandArgsPatternDoesntMatchException as ex:
        await client.send_message(message.channel, ex.message)
    except grimbot.CommandLengthDoesntMatchException as ex:
        await client.send_message(message.channel, str(ex))
        await client.send_message(message.channel, "HELP: " + ex.help)

cmdManager.commands.append(
    grimbot.CreateCommand(
        "create",
        []
    )
)

cmdManager.commands.append(
    grimbot.AddressCommand(
        "address",
        []
    )
)

cmdManager.commands.append(
    grimbot.DepositCommand(
        "deposit",
        []
    )
)

cmdManager.commands.append(
    grimbot.BalanceCommand(
        "balance",
        []
    )
)

cmdManager.commands.append(
    grimbot.WithdrawCommand(
        "withdraw",
        [
            grimbot.RegexArgsPattern("G[a-zA-Z0-9]{23}", "アドレスの形式が不正です!"),
            grimbot.PositiveNumberArgsPattern()
        ]
    )
)

cmdManager.commands.append(
    grimbot.TipCommand(
        "tip",
        [
            grimbot.RegexArgsPattern(".*", ""),
            grimbot.PositiveNumberArgsPattern()
        ]
    )
)

cmdManager.commands.append(
    grimbot.RainCommand(
        "rain",
        [
            grimbot.PositiveNumberArgsPattern()
        ]
    )
)

cmdManager.commands.append(
    grimbot.PriceCommand(
        "grim",
        [
            grimbot.PositiveNumberArgsPattern(numberOfArgs_=-1)
        ]
    )
)

cmdManager.commands.append(
    grimbot.FXCalcCommand(
        "fx",
        [
            grimbot.StringArgsPattern("lev"),
            grimbot.RegexArgsPattern("([+-]?[0-9]+(\.[0-9]*)?([eE][+-]?[0-9]+)?)x([+-]?[0-9]+(\.[0-9]*)?([eE][+-]?[0-9]+)?)", "掛け金または倍率が数値ではありません!"),
            grimbot.RegexArgsPattern(".*", ""),
            grimbot.PositiveNumberArgsPattern(),
            grimbot.StringArgsPattern("to"),
            grimbot.PositiveNumberArgsPattern(),
            grimbot.StringArgsPattern("with"),
            grimbot.RegexArgsPattern("[LS]", "LongまたはShortを指定してください!")
        ]
    )
)

client.run('MzkzOTczODgxODg4NzAyNDY2.DR9kSQ.Sz8lXQb3DshzMTOiKSKSN9uqdIY')