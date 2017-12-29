import discord

def getIdFromName(server : discord.Server, name : str) -> str:
    for member in server.members:
        if member.name == name:
            return member.id
    return ""

def getDiscriminatorFromName(server : discord.Server, name : str) -> str:
    for member in server.members:
        if member.name == name:
            return member.discriminator
    return ""

async def mention(client, dist, name : str, message : str) -> bool:
    toId = getIdFromName(dist.server, name)
    if toId != "":
        await client.send_message(dist, "<@" + toId + "> " + message)
    else:
        return False
    return True