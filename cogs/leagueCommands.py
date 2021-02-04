# import os
# import discord
# from discord.ext import commands
# from dotenv import load_dotenv
# from riotwatcher import LolWatcher, ApiError
# import json

# load_dotenv()
# KEY = os.getenv('RIOT_KEY')

# LolUsers = {}

# class LeagueCommands(commands.Cog):
#     '''
#     A cog for getting information from the Riot games API using riotwatcher.
#     '''

#     watcher = LolWatcher(KEY)
#     region = 'na1'

#     @commands.command()
#     async def register_username(ctx, payload):
