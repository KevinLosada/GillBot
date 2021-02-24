import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

'''
Main bot file, loads all cogs and sets status, all other functionality is inside the cogs
'''

load_dotenv()

# important declarations
TOKEN = os.getenv('DISCORD_TOKEN')
command_prefix = '!'
bot = commands.Bot(command_prefix)

MODERATOR_ROLE_ID = 750821675670568970

# Bot code begins
@bot.event
async def on_ready():
    print(f'Bot is online~\n{bot.user.name}, (ID: {bot.user.id})\n')

    #Load cogs
    print('Cogs loading:')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'- {(filename[:-3]).title()} commands loaded')

    #Set status
    await bot.change_presence(status = discord.Status.online, activity=discord.Game("Ready to"))

@bot.command()
async def load(ctx, extension):
    roles = ctx.author.roles
    mod_role = ctx.guild.get_role(MODERATOR_ROLE_ID)

    if mod_role not in roles:
        await ctx.send(
            f'{ctx.author.mention} this command is only meant to be used by Moderators.')
    else:
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension.title()} cog has been loaded')

@bot.command()
async def unload(ctx, extension):
    roles = ctx.author.roles
    mod_role = ctx.guild.get_role(MODERATOR_ROLE_ID)

    if mod_role not in roles:
        await ctx.send(
            f'{ctx.author.mention} this command is only meant to be used by Moderators.')
    else:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'{extension.title()} cog was unloaded')

@bot.command(aliases=['r'])
async def reload(ctx):
    roles = ctx.author.roles
    mod_role = ctx.guild.get_role(MODERATOR_ROLE_ID)

    if mod_role not in roles:
        await ctx.send(
            f'{ctx.author.mention} this command is only meant to be used by Moderators.')
    else:
        try:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    bot.unload_extension(f'cogs.{filename[:-3]}')
                    bot.load_extension(f'cogs.{filename[:-3]}')
                    print(f'- {(filename[:-3]).title()} commands reloaded')
            await ctx.send(f'Cogs reloaded succesfully')
            print(f'Cogs reloaded succesfully\n')
        except Exception:
            await ctx.send(f"Something's not right...")
            print(Exception)

bot.run(TOKEN)