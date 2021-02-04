import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

Sydney = discord.utils.get()

# important declarations
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_message(self, message):
    Sydney =  discord.utils.get(message.guild.members, id = 257372338868191233)
    Kevin = discord.utils.get(message.guild.members, id = 182650505699393536)

    bot_channel = discord.utils.get(message.guild.channels, id=805906867104514050)
    test_channel = discord.utils.get(message.guild.channels, id=806670890170974208)

    if message.author == self.user:
        return
    
    if message.user == Kevin and message.channel == test_channel:
        await bot.send_message(bot_channel, "Fuck you too bitch " + Kevin.mention)



bot.run(TOKEN)