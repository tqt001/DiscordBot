import discord
import os
import random
from discord.ext import commands


class Fortune(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['fortune', '8ball', 'question', 'helpMe'])
    async def fortuneTeller(self, ctx, *, question):
        choices = ['I am going to say no.',
                   'Your mom!',
                   "He said to Jacob, Let me gulp down some of that red stuff; I’m starving.",
                   "These people are not drunk, as you suppose, for it is only nine o’clock in the morning.",
                   'I am going to say yes.',
                   "I don't know."]
        await ctx.send(f'Question: {question}\nResponse: {random.choice(choices)}')


def setup(client):
    client.add_cog(Fortune(client))
