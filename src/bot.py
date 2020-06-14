import discord
from discord.ext import commands
from src.TokenManagement.TokenManager import TokenManager
from src.ExtensionManager import ExtensionManager
import logging

# Ghetto logging
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord_log.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='.')
ext_manager = ExtensionManager(bot, "All")
TOKEN = TokenManager("TokenManagement/token.txt").read_token()


@bot.event
async def on_ready():
    """Tasks to initialize when the bot is finished loading and logged into discord."""

    # Sets bot's status
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('with your girlfriend ;)'))

    # Initial extensions to load. Options: All, Partial, Minimum
    await ext_manager.load()

    print('Bot is ready.')


@bot.command()
async def reinit_manager():
    """Reinitialize the ExtensionManager. Will add any new discovered extension files to the list of all available
    extensions to the manager."""
    await ext_manager.reinit()


@bot.command()
async def reload_all():
    """Reloads all the current loaded extensions"""
    await ext_manager.reload_all()


@bot.event
async def on_member_join(ctx, member):
    await ctx.send(f'Oh god, look at {member}.')


@bot.event
async def on_member_remove(ctx, member):
    await ctx.send(f'Everyone say bye {member}.')


bot.run(TOKEN)
