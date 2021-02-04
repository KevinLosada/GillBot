import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# important declarations
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')


admin_id = 0  # DOUBLE CHECK THIS ONE
ticket_channel_id = 0
template_channel_id = 0
voice_template_channel_id = 0
checkin_channel_id = 0


def createListFromFile(file):
    with open(file) as f:
        temp = f.read().splitlines()
        for i in temp:
            i.lower()
        return temp


hackers = createListFromFile("hackers.txt")
mentors = createListFromFile("mentors.txt")
# sponsors = []
organizers = createListFromFile("organizers.txt")

channels_dict = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected!')

@bot.command()
async def checked_in_hackers(ctx):
    members = ctx.guild.members
    counter = 0
    hacker = discord.utils.get(ctx.guild.roles, id=)
    for i in members:
        if hacker in i.roles:
            counter += 1
    await ctx.send(counter)
    

@bot.command()
async def checkin(ctx, email):
    # ShellHacks-Check-In channel ID

    checkin_channel = bot.get_channel(checkin_channel_id)
    if ctx.channel.id != checkin_channel_id:
        return
    
    hacker = discord.utils.get(ctx.guild.roles, id=)
    mentor = discord.utils.get(ctx.guild.roles, id=)
    organizer = discord.utils.get(ctx.guild.roles, id=)

    roles = [organizer, mentor, hacker]

    # check if user has a role already
    for value in ctx.author.roles:
        if value in roles:
            await ctx.author.create_dm()
            await ctx.author.dm_channel.send('You have already been checked in, if there was a mistake please message an organizer.')
            return

    if email.lower() in organizers:
        await ctx.author.add_roles(organizer)
        await ctx.author.create_dm()
        await ctx.author.dm_channel.send(f'{ctx.author.mention} you now have {organizer} role!')
        return
    elif email.lower() in mentors:
        await ctx.author.add_roles(mentor)
        await ctx.author.create_dm()
        await ctx.author.dm_channel.send(f'{ctx.author.mention} you now have {mentor} role!')
        return
    elif email.lower() in hackers:
        await ctx.author.add_roles(hacker)
        await ctx.author.create_dm()
        await ctx.author.dm_channel.send(f'{ctx.author.mention} you now have {hacker} role!')
        return
    else:
        await ctx.author.create_dm()
        await ctx.author.dm_channel.send('Email not found, please make sure you are writing the email and command correctly (Ex: !checkin email@example.com).')
        return

# Delete messages in create a ticket channel


@bot.event
async def on_message(payload):
    checkin = bot.get_channel(checkin_channel_id)  # Check in channel ID
    ticket = bot.get_channel(ticket_channel_id)
    if payload.channel == checkin or payload.channel == ticket:
        await payload.delete()
    await bot.process_commands(payload)

# FIX THE CHANNEL TO SEARCH FOR ID

@bot.command()
async def linked_in(ctx):
    channel = bot.get_channel()
    messages = await channel.history().flatten()

@bot.command()
async def guide(ctx):
    link = "http://go.fiu.edu/shellhacksguide"

    message = "Hey there, please refer to the hackers guide to find the answer to your question:\n" + link
    await ctx.send(message)
    await ctx.message.delete()

@bot.command()
async def ticket(ctx):
    print("I'm in ticket")
    create_ticket_channel = bot.get_channel(ticket_channel_id)
    if ctx.channel != create_ticket_channel:
        return

    # declarations
    guild = ctx.guild
    template_channel = guild.get_channel(template_channel_id)
    voice_template_channel = guild.get_channel(voice_template_channel_id)
    name = ctx.author.name.replace(' ', '-')

    # cloning happens
    ticket_channel = await template_channel.clone(name='ticket-' + name)
    voice_ticket_channel = await voice_template_channel.clone(name='ticket-' + name)

    # add to dict
    channels_dict[ticket_channel.id] = voice_ticket_channel.id
    print(channels_dict[ticket_channel.id])
    print(ticket_channel.id)
    print(channels_dict)

    #set permissions
    await ticket_channel.set_permissions(target=ctx.author, read_messages=True, send_messages=True, read_message_history=True)
    await voice_ticket_channel.set_permissions(target=ctx.author, connect=True, speak=True, view_channel=True)
    await ticket_channel.send(ctx.author.mention + ' you can ask the mentors questions in this channel, please close it using !close_ticket when you\'re satisfied with the help you\'ve received.')

    # await ctx.message.delete()

# ADD MESSAGE DELETION IN THE ON MESSAGE FUNCTION

@bot.command()
async def close_ticket(ctx):
    if 'ticket' in ctx.channel.name and ctx.channel.id != ticket_channel_id and ctx.channel.id != template_channel_id:
        voice_ticket_channel = bot.get_channel(channels_dict[ctx.channel.id])
        channels_dict.pop(ctx.channel.id)
        await ctx.channel.delete()
        await voice_ticket_channel.delete()
    else:
        await ctx.send("Sorry, this command only works for ticket channels")


# Deletes as many messages as passed in parameter
@bot.command()
async def purge(ctx, num_messages):
    roles = ctx.author.roles
    admin = ctx.guild.get_role(admin_id)

    if admin not in roles:
        await ctx.send(
            f'{ctx.author.mention} this command is only usable by organizers.')
    else:
        await ctx.channel.purge(limit=int(num_messages) + 1)


# Copies the message from ID with the bot's perspective
@bot.command()
async def copy(ctx, id):
    message = await ctx.channel.fetch_message(id)
    await ctx.send(message.content)

    bot.run(TOKEN)

def handle_team_size(ctx):
    org_channel = bot.get_channel()
    

bot.run(TOKEN)

# Not in use currently but below functions are reaction roles functions

# @bot.event
# async def on_raw_reaction_add(payload):
#     if payload.message_id == 733885294016987196:
#         print(payload.emoji.name)
#         # Find a role corresponding to the Emoji name.
#         guild_id = payload.guild_id
#         guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

#         role = discord.utils.find(
#             lambda r: r.name == payload.emoji.name, guild.roles)

#         if role is not None:
#             print(role.name + " was found!")
#             print(role.id)
#             member = discord.utils.find(
#                 lambda m: m.id == payload.user_id, guild.members)
#             await member.add_roles(role)
#             print("done")


# @bot.event
# async def on_raw_reaction_remove(payload):
#     if payload.message_id == 733885294016987196:
#         print(payload.emoji.name)

#         guild_id = payload.guild_id
#         guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
#         role = discord.utils.find(
#             lambda r: r.name == payload.emoji.name, guild.roles)

#         if role is not None:
#             member = discord.utils.find(
#                 lambda m: m.id == payload.user_id, guild.members)
#             await member.remove_roles(role)
#             print("done")
