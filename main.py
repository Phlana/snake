import discord
from discord.ext import commands
from config import *
import random

# client = discord.Client()
config = Config()
client = commands.Bot(command_prefix=config.prefix)
client.remove_command("help")
# welcome_channel =


@client.event
async def on_ready():
    # printed when the bot is started
    print("logged in as {0.name} using id {0.id} and discord.py version {1}".format(client.user, discord.__version__))
    await client.change_presence(game=discord.Game(name="wip!٩(｡•‿•｡)۶ do:\"[help\""))


# general commands
# help
@client.command(pass_context=True, aliases=["h", "hlep"])
async def help(ctx):
    help_embed = discord.Embed(colour=discord.Colour.orange())

    help_embed.set_author(name="Snake bot", url="https://github.com/Phlana/snake",
                          icon_url=client.user.avatar_url)
    help_embed.set_thumbnail(url="https://i.ytimg.com/vi/CBdwWaRhUxI/maxresdefault.jpg")
    # help_embed.add_field(name="", value="", inline=False)
    # general commands
    help_embed.add_field(name="commands", value="commands with * in front of command is mod command "
                                                "and requires mod permissions", inline=False)
    help_embed.add_field(name="help", value="prefix is [", inline=False)
    help_embed.add_field(name="members", value="returns number of members in server including bot", inline=False)
    help_embed.add_field(name="sinfo", value="displays server info", inline=False)
    help_embed.add_field(name="roll <number>", value="returns random number from 1 to <number>", inline=False)
    help_embed.add_field(name="e <emoji>", value="posts the image of <emoji>", inline=False)

    # mod commands
    help_embed.add_field(name="*prune <number>", value="removes <number> messages", inline=False)
    help_embed.add_field(name="*mute <@user>", value="mutes <@user> from all text channels", inline=False)
    help_embed.add_field(name="*silence <@user>", value="mutes <@user> from all text and voice channels", inline=False)
    help_embed.add_field(name="*kick <@user>", value="kicks <@user> from server", inline=False)
    help_embed.add_field(name="*ban <@user>", value="bans <@user> from server", inline=False)
    client.send_message(ctx.message.author, embed=help_embed)


# member count
@client.command(pass_context=True)
async def members(ctx):
    member_count = 0
    for m in ctx.message.server.members:
        member_count += 1
    await client.say("{} members found".format(member_count))


# server info
@client.command(pass_context=True, aliases=["serverinfo", "server info", "server", "s"])
async def sinfo(ctx):
    member_count = 0
    online_count = 0
    channel_count = 0
    text_count = 0
    voice_count = 0
    server = ctx.message.server
    # count members and channels of this server
    for member in server.members:
        member_count += 1
        if member.status != discord.Status.offline:
            online_count += 1
    for channel in server.channels:
        channel_count += 1
        if channel.type == discord.ChannelType.text:
            text_count += 1
        elif channel.type == discord.ChannelType.voice:
            voice_count += 1

    server_embed = discord.Embed(colour=discord.Colour.dark_blue())
    server_embed.set_author(name=server.name, icon_url=server.icon_url)
    server_embed.set_thumbnail(url=server.icon_url)
    server_embed.add_field(name="owner:", value=server.owner, inline=False)
    server_embed.add_field(name="{} members".format(member_count),
                           value="{} online".format(online_count), inline=False)
    if channel_count == 1:
        server_embed.add_field(name="{} channel".format(channel_count),
                               value="{} text\n{} voice".format(text_count, voice_count),
                               inline=False)
    else:
        server_embed.add_field(name="{} channels".format(channel_count),
                               value="{} text\n{} voice".format(text_count, voice_count),
                               inline=False)
    server_embed.add_field(name="created on:", value=server.created_at, inline=False)
    await client.say(embed=server_embed)


# roll
@client.command(pass_context=True, aliases=["r"])
async def roll(ctx, num=100):
    await client.say("{} rolls a {}".format(ctx.message.author.mention, random.randint(1, num)))


# enlage emoji
@client.command(aliases=["e"])
async def emoji(emojiobj: discord.Emoji):
    await client.say(emojiobj.url)


# mod commands
# prune
@client.command(pass_context=True)
async def prune(ctx, num=50):
    channel = ctx.message.channel
    msgs = []
    async for msg in client.logs_from(channel, limit=int(num) + 1):
        msgs.append(msg)
    num_msgs = len(msgs) - 1
    try:
        await client.delete_messages(msgs)
        await client.say("cleared {} messages".format(num_msgs))
    except:
        await client.say("failed to clear messages")


# mute
@client.command(pass_context=True)
async def mute(ctx):
    memberlist = ctx.message.mentions
    rolelist = ctx.message.role_mentions
    print(len(memberlist), memberlist)
    print(len(rolelist), rolelist)
    if len(memberlist) == 0 & len(rolelist) == 0:
        await client.say("please mention a user or role")
    if len(memberlist) + len(rolelist) > 1:
        await client.say("please mention only one user or role")
        return
    if len(memberlist) == 1:
        # try:
            for channel in memberlist[0].server.channels:
                if channel.type == discord.ChannelType.text:
                    await client.edit_channel_permissions()
                    await channel.set_permissions(memberlist[0], send_messages=False)
                    await client.say("muted {}".format(memberlist[0]))
        # except:
            await client.say("failed to mute {}".format(memberlist[0]))
    if len(rolelist) == 1:
        # try:
        #     rolelist[0].permissions.send_messages = False
            await client.edit_role(rolelist[0].server, rolelist[0], permissions=discord.Permissions(send_messages=True))
            await client.say("muted {} role".format(rolelist[0]))
        # except:
            await client.say("failed to mute {} role".format(rolelist[0]))

    # async for member in ctx.message.mentions:
    #     async for channel in member.server.channels:
    #         if channel.type == discord.ChannelType.text:
    #             await channel.set_permissions(member, send_messages=False)
    #     await client.say("muted {}".format(member))


# unmute
@client.command(pass_context=True)
async def unmute(ctx):
    async for member in ctx.message.mentions:
        async for channel in member.server.channels:
            if channel.type == discord.ChannelType.text:
                await channel.set_permissions(member, send_messages=True)
        await client.say("unmuted {}".format(member))


# silence
@client.command(pass_context=True)
async def silence(ctx):
    for member in ctx.message.mentions:
        for channel in member.server.channels:
            if channel.type == discord.ChannelType.text:
                await channel.set_permissions(member, send_messages=False)
            elif channel.type == discord.ChannelType.voice:
                await channel.set_permissions(member, speak=False)
        await client.say("silenced {}".format(member))


# unsilence
@client.command(pass_context=True)
async def unsilence(ctx):
    async for member in ctx.message.mentions:
        async for channel in member.server.channels:
            if channel.type == discord.ChannelType.text:
                await channel.set_permissions(member, send_messages=True)
            elif channel.type == discord.ChannelType.voice:
                await channel.set_permissions(member, speak=True)
        await client.say("unsilenced {}".format(member))


# kick
@client.command(pass_context=True)
async def kick(ctx):
    for member in ctx.message.mentions:
        await client.kick(member)
        await client.say("kicked {}".format(member))


# ban
@client.command(pass_context=True)
async def ban(ctx):
    async for member in ctx.message.mentions:
        await member.server.ban(member)
        await client.say("banned {}".format(member))

# # events
# # member join
# @client.event
# async def on_member_join(member):
#     for channel in member.server.channels:


# message sent
@client.event
async def on_message(message):
    # bot doesnt reply to itself
    if message.author == client.user:
        return

    for mention in message.mentions:
        if client.user == mention:
            await client.send_message(message.channel, "type `[help` for help")

    # # moderator commands
    # if message.author.server_permissions.administrator:
    #
    # else:
    #     await client.send_message(message.channel, "Insufficient permissions")
    await client.process_commands(message)


# member join
@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name="Limbo")
    await client.add_roles(member, role)

    for channel in member.server.channels:
        if channel.name == "log":
            await client.send_message(channel, "{} joined".format(member.mention))


# member leave
@client.event
async def on_member_remove(member):
    for channel in member.server.channels:
        if channel.name == "log":
            await client.send_message(channel, "{} left".format(member.mention))

client.run(config.TOKEN)
