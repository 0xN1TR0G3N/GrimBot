import ssl

import aiohttp
import discord
import grimbot
import logging
import traceback
from GrimChanThrower import GrimChanThrower, ServerCommandsLoader

client = discord.Client(connector=aiohttp.TCPConnector(verify_ssl=False))

cmdManager = grimbot.CommandManager(",")

thrower = GrimChanThrower()

wordList = ['ゆみ', '亀山', '三重', 'yumi', 'うんち']

@client.event
async def on_message(message: discord.Message):
    if len(message.content) == 0:
        return

    thrower.transferIfMatched(message.content, message.server.id)

    if any([(word in message.content) for word in wordList]):
        await client.add_reaction(message, '💩')

    try:
        await cmdManager.execute(message.content, client, message)
    except grimbot.CommandArgsPatternDoesntMatchException as ex:
        await client.send_message(message.channel, ex.message)
    except grimbot.CommandLengthDoesntMatchException as ex:
        await client.send_message(message.channel, str(ex))
        await client.send_message(message.channel, "HELP: " + ex.help)
    except Exception:
        print(traceback.format_exc())

cmdManager.commands.append(
    grimbot.CreateCommand(
        "register",
        [],
        ['fiat_bot', 'register_room']
    )
)


cmdManager.commands.append(
    grimbot.AddressCommand(
        "address",
        [],
        ['fiat_bot', 'address_deposit_room']
    )
)

cmdManager.commands.append(
    grimbot.DepositCommand(
        "deposit",
        [],
        ['fiat_bot', 'address_deposit_room']
    )
)

cmdManager.commands.append(
    grimbot.BalanceCommand(
        "balance",
        [],
        ['fiat_bot', 'balance_room']
    )
)

cmdManager.commands.append(
    grimbot.WithdrawCommand(
        "withdraw",
        [
            grimbot.RegexArgsPattern("G[a-zA-Z0-9]{23}", "アドレスの形式が不正です!"),
            grimbot.PositiveNumberArgsPattern()
        ],
        ['fiat_bot']
    )
)

cmdManager.commands.append(
    grimbot.TipCommand(
        "tip",
        [
            grimbot.RegexArgsPattern(".*", ""),
            grimbot.PositiveNumberArgsPattern()
        ],
        ['fiat_bot', 'tip_room', 'event_room']
    )
)

cmdManager.commands.append(
    grimbot.RainCommand(
        "rain",
        [
            grimbot.PositiveNumberArgsPattern()
        ],
        ['rain_room']
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

cmdManager.commands.append(
    grimbot.PriceCommand(
        "grim",
        [
            grimbot.PositiveNumberArgsPattern(numberOfArgs_=-1)
        ],
        ['fiat_bot']
    )
)

cmdManager.commands.append(
    grimbot.TalkCommand(
        "talk",
        [
            grimbot.RegexArgsPattern(".*", "")
        ],
        ['fiat_bot']
    )
)

cmdManager.commands.append(
    grimbot.TranslateJPIntoENCommand(
        "trjp",
        [
            grimbot.RegexArgsPattern('.*', '')
        ]
    )
)

cmdManager.commands.append(
    grimbot.TranslateENIntoJPCommand(
        "tren",
        [
            grimbot.RegexArgsPattern('.*', '')
        ]
    )
)

cmdManager.commands.append(
    grimbot.Mine29Command(
        "mine29",
        [],
        ['chat_room']
    )
)

cmdManager.commands.append(
    grimbot.ProfileCommand(
        "profile",
        [],
        ['chat_room']
    )
)

print('GRIM Bot has started.')
print('Commands: %s' % (cmdManager.commands))

thrower.serverCommandsList = ServerCommandsLoader.loadsFrom('./GrimChanThrowerServers')

client.run('Mzk3MzY0NjgxMDAzNjMwNTky.DSu6Ng.Uel-GVoa8gXKWi9JM8eli5HaCiI')