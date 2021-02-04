import discord
from discord.ext import commands

class Miscellaneous(commands.Cog):

    '''
    Any commands that do not fit into a cog of their own are stored here.
    '''

    def __init__(self, bot):
        self.bot = bot

    #trolling sydney
    @commands.Cog.listener()
    async def on_message(self, message):
        BOT_CHANNEL_ID = 805906867104514050
        SYDNEY_ID = 257372338868191233

        if message.channel.id == BOT_CHANNEL_ID and message.author.id == SYDNEY_ID and message.content.lower() == 'bitch':
            await message.reply("No you're the bitch")

    @commands.command(aliases=['p'])
    async def ping(self, ctx):
        await ctx.send(f'I\'m alive! Latency is {round(self.bot.latency * 1000)}ms')

def setup(bot):
    bot.add_cog(Miscellaneous(bot))