import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cassiopeia import Summoner, NotFoundError
from pymongo import MongoClient

load_dotenv()
KEY = os.getenv('RIOT_KEY')
MONGO_CONNECT_STRING = os.getenv('MONGODB_STRING')
region = 'NA'

client = MongoClient(MONGO_CONNECT_STRING)
db = client.main
summoner_names = db.summoner_names


class LeagueCommands(commands.Cog):
    '''
    A cog for getting information from the Riot games API using Cassiopeia.
    '''
    @commands.command(aliases=['ru'])
    async def register_username(self, ctx, user):
        emoji = '✅'
        username = user
        user = {'discord_name': ctx.author.name,
                'summoner_name': username}
        
        #check if user exists
        try:
            sum = Summoner(name=username, region='NA')
        except NotFoundError:
            ctx.send("Summoner could not be found")
            return
        
        #check if summoner is registered, if not then register
        if summoner_names.count_documents(user, limit=1) != 0:
            await ctx.send(f'{ctx.author.name} you are already registered with {username}.')
            return
        else: 
            added = summoner_names.insert_one(user)
            if added is not None:
                await ctx.message.add_reaction(emoji)

    @commands.command(aliases=['si'])
    async def summoner_info(self, ctx):
        summ_name_dict = summoner_names.find_one({'discord_name': ctx.author.name})
        summ_name = summ_name_dict['summoner_name']
        summoner = Summoner(name=summ_name, region=region)

        #create embed object
        embed = discord.Embed(
            title=f'{summ_name}\'s Summoner Stats',
            url=f'https://u.gg/lol/profile/na1/{summ_name}/overview',
            description=f'Collection of summoner info, click link to access u.gg summoner page')
        
        await ctx.send(embed=embed)
        #Add summoner icon thumbnail to embed
        embed.set_thumbnail(url=summoner.profile_icon.url)

        #level field
        embed.add_field(
            name="Level",
            value=summoner.level)

    # @commands.command(aliases=['si'])
    # async def summoner_info(self, ctx, name):
    #     summoner = Summoner(name=name, region=region)

    #     #create embed object
    #     embed = discord.Embed(
    #         title=f'{name}\'s Summoner Stats',
    #         url=f'https://u.gg/lol/profile/na1/{name}/overview',
    #         description=f'Collection of summoner info, click link to access u.gg summoner page')
        
    #     await ctx.send(embed=embed)
    #     # #Add summoner icon thumbnail to embed
    #     # embed.set_thumbnail(url=summoner.profile_icon.url)

    #     # #level field
    #     # embed.add_field(
    #     #     name="Level",
    #     #     value=summoner.level)

def setup(bot):
    bot.add_cog(LeagueCommands(bot))