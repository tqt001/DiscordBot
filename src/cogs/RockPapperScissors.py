import discord
from discord.ext import commands

class RockPaperScissors(commands.Cog):
    def __init__(self, client):
        self.client = client
    #
    # @commands.Cog.listener()
    # def listenForResponse(self, ctx):
    #     if ctx ==

def setup(client):
    client.add_cog(RockPaperScissors(client))
