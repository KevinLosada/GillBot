import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Spotify(commands.Cog):

    '''
    Handles all events and commands that use the Spotify API through the use of spotipy.
    '''

    def __init__(self, bot):
        self.bot = bot

    #actual functionality

def setup(bot):
    bot.add_cog(Spotify(bot))