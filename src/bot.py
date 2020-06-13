import os
import discord
from discord.ext import commands
from src.TokenManagement import TokenManager

bot = commands.Bot(command_prefix='.')
TOKEN = TokenManager.TokenManager("TokenManagement/token.txt").read_token()


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('with your girlfriend ;)'))
    print('Bot is ready.')


@bot.event
async def on_member_join(ctx, member):
    await ctx.send(f'Oh god, look at {member}.')


@bot.event
async def on_member_remove(ctx, member):
    await ctx.send(f'Everyone say bye {member}.')


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command()
async def clear(ctx, amount=50):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Clear complete.')


for file in os.listdir('cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(TOKEN)
