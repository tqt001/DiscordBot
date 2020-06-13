import random
import os
import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')
TOKEN = "NzIxMDY5NjAxMjIzNjA2Mzkz.XuQFZw.JfEsOFthbPgispobyOFiA7Jwuok"


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('with your girlfriend ;)'))
    print('Bot is ready.')


@client.event
async def on_member_join(ctx, member):
    await ctx.send(f'Oh god, look at {member}.')


@client.event
async def on_member_remove(ctx, member):
    await ctx.send(f'Everyone say bye {member}.')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command()
async def clear(ctx, amount=50):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Clear complete.')


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

client.run(TOKEN)
