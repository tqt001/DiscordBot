import os
import discord
from discord.ext import commands
from src.TokenManagement.TokenManager import TokenManager
import logging

# Ghetto logging
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord_log.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='.')
TOKEN = TokenManager("TokenManagement/token.txt").read_token()


@bot.event
async def on_ready():
    bot.load_extension('Extensions.Misc.Checker')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('with your girlfriend ;)'))
    print('Bot is ready.')


@bot.command()
async def list_extensions():
    """Lists all the extensions available to the bot."""
    pass


@bot.command()
async def load(ctx, extension):
    """Load the named extension using the extension dictionary"""
    bot.load_extension(extension)


@bot.command()
async def reload(ctx, extension):
    """Reload the named extension"""
    bot.reload_extension(extension)


@bot.event
async def on_member_join(ctx, member):
    await ctx.send(f'Oh god, look at {member}.')


@bot.event
async def on_member_remove(ctx, member):
    await ctx.send(f'Everyone say bye {member}.')


@bot.command()
async def clear(ctx, amount=50):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Clear complete.')


'''for file in os.listdir('cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')'''

bot.run(TOKEN)
