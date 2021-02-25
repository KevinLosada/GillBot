import os
import sys
import cassiopeia as cass
import discord
from discord.ext import commands
from cassiopeia import Summoner, Champion, Champions, Queue
from datapipelines import NotFoundError
from pymongo import MongoClient

MONGO_CONNECT_STRING = os.getenv('MONGODB_STRING')
region = 'NA'
checkmark = '✅'

client = MongoClient(MONGO_CONNECT_STRING)  # client
db = client.main  # database
summoner_names = db.summoner_names  # collection


class LeagueCommands(commands.Cog):
    """
    A cog for getting information from the Riot games API using Cassiopeia.
    """

    @commands.command(aliases=['ru'])
    async def register_username(self, ctx, user):
        """Usage: type the command followed by your riot summoner name to register yourself to the bot"""
        username = user
        user = {'discord_name': ctx.author.name,
                'summoner_name': username}

        # check if user exists
        try:
            sum = Summoner(name=username, region='NA')
        except NotFoundError:
            ctx.send("Summoner could not be found")
            return

        # check if summoner is registered, if not then register
        if summoner_names.count_documents(user, limit=1) != 0:
            await ctx.send(f'{ctx.author.name} you are already registered with {username}.')
            return
        else:
            added = summoner_names.insert_one(user)
            if added is not None:
                await ctx.message.add_reaction(checkmark)

    @commands.command(aliases=['uu'])
    async def update_username(self, ctx, user):
        """Update your information to the bot"""
        try:
            summoner_names.update_one({'discord_name': ctx.author.name}, {"$set": {'summoner_name': user}})
            await ctx.message.add_reaction(checkmark)
        except:
            await ctx.send("Something went wrong, tag Kevin")
            await ctx.send(sys.exc_info()[0])

    @commands.command(aliases=['si'])
    async def summoner_info(self, ctx, passed_name: str = None):
        """Pass a name for that summoner's info, no name for your own if registered. """
        if passed_name is None:
            summoner_name_dict = summoner_names.find_one({'discord_name': ctx.author.name})
            summoner = Summoner(name=summoner_name_dict['summoner_name'], region=region)
        else:
            # currently, except not being reached
            try:
                summoner = Summoner(name=passed_name, region=region)
                summoner.level  # simple call to api to trigger exception if not found
            except NotFoundError:
                await ctx.send("Summoner could not be found")
                return

        formatted_summoner_name = summoner.name.replace(' ', '%20')

        # create embed object
        embed = discord.Embed(
            title=f'{summoner.name}\'s Summoner Stats',
            url=f'https://na.op.gg/summoner/userName={formatted_summoner_name}',
            description=f'Display of summoner information, click on link for op.gg page.')

        # Add summoner icon thumbnail to embed
        embed.set_thumbnail(url=summoner.profile_icon.url)

        # level field
        embed.add_field(
            name="Level",
            value=summoner.level)

        # TO DO: Add prettified champ masteries to the embed

        await ctx.send(embed=embed)

    @commands.command(aliases=['ci'])
    async def champion_information(self, ctx, champ):
        """Provide the champion name you want after command and it will provide a link for the wikipedia page on said champ. This command is still in progress, so please put multi-word names in quotes."""

        try:
            champion = Champion(name=champ.title(), region=region)
            champion.blurb  # call to trigger exception if not found
        except NotFoundError:
            await ctx.send("Sorry, that champion could not be found. Please make sure you spelled the name correctly.")

        wiki_champ_name = champion.name.replace(' ', '_').replace('\'', '%27')

        # create embed
        embed = discord.Embed(
            title=f'{champion.name}, {champion.title}',
            url=f'https://leagueoflegends.fandom.com/wiki/{wiki_champ_name}/LoL',
            description=f'{champion.blurb}'
        )
        embed.set_thumbnail(url=f'http://ddragon.leagueoflegends.com/cdn/11.4.1/img/champion/{champion.name}.png')
        embed.add_field(name='Passive', value=champion.passive.description)
        embed.add_field(name='Q', value=champion.spells['Q'].description, inline=False)
        embed.add_field(name='E', value=champion.spells['E'].description, inline=False)
        embed.add_field(name='W', value=champion.spells['W'].description, inline=False)
        embed.add_field(name='R', value=champion.spells['R'].description, inline=False)
        await ctx.send(embed=embed)


# def get_win_rate(player: cass.Summoner):
#     match_history=player.match_history(queues={Queue.normal_draft_fives})
#     return sum([1 for match in match_history if match.participants[player].stats.win])/len(match_history)

def setup(bot):
    bot.add_cog(LeagueCommands(bot))
