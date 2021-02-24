import os
import sys
from cassiopeia.core import summoner
import discord
from discord.ext import commands
from cassiopeia import Summoner
from datapipelines import NotFoundError
from pymongo import MongoClient

MONGO_CONNECT_STRING = os.getenv('MONGODB_STRING')
region = 'NA'
checkmark = '✅'

client = MongoClient(MONGO_CONNECT_STRING) #client
db = client.main #database
summoner_names = db.summoner_names #collection


class LeagueCommands(commands.Cog):
    '''
    A cog for getting information from the Riot games API using Cassiopeia.
    '''
    @commands.command(aliases=['ru'])
    async def register_username(self, ctx, user):
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
                await ctx.message.add_reaction(checkmark)
    
    @commands.command(aliases=['uu'])
    async def update_username(self, ctx, user):
        try:
            summoner_names.update_one({'discord_name': ctx.author.name}, {"$set": {'summoner_name': user}})
            await ctx.message.add_reaction(checkmark)
        except:
            await ctx.send("Something went wrong, tag Kevin")
            await ctx.send(sys.exc_info()[0])

    @commands.command(aliases=['si'])
    async def summoner_info(self, ctx, passed_name: str=None):
        if passed_name is None:
            summoner_name_dict = summoner_names.find_one({'discord_name': ctx.author.name})
            summoner = Summoner(name=summoner_name_dict['summoner_name'], region=region)
        else:
            # currently, except not being reached
            try:
                summoner = Summoner(name=passed_name, region=region)
            except NotFoundError:
                await ctx.send("Summoner could not be found")
                return

        formatted_summoner_name = summoner.name.replace(' ', '%20')

        #create embed object
        embed = discord.Embed(
            title=f'{summoner.name}\'s Summoner Stats',
            url=f'https://na.op.gg/summoner/userName={formatted_summoner_name}',
            description=f'Display of summoner information, click on link for op.gg page.')
        
        #Add summoner icon thumbnail to embed
        embed.set_thumbnail(url=summoner.profile_icon.url)

        #level field
        embed.add_field(
            name="Level",
            value=summoner.level)
        
        # champ_masteries = summoner.champion_masteries.filter(lambda cm: cm.level >= 5)

        # #need to find way to format these and print them
        # formatted_champ_masteries = ''

        # embed.add_field(
        #     name="Champion Masteries",
        #     value=formatted_champ_masteries
        # )
        await ctx.send(embed=embed)

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