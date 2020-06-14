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
# Options: All, Partial, Minimum
ext_manager = ExtensionManager(bot, "All")
TOKEN = TokenManager("TokenManagement/token.txt").read_token()


@bot.event
async def on_ready():
    """Tasks to initialize when the bot is finished loading and logged into discord."""

    # Sets bot's status
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('with your girlfriend ;)'))

    # Initial extensions to load.
    await ext_manager.load()

    print('Bot is ready.')


@bot.command()
async def change_extlevel(ctx):
    message = ctx.message
    if message.content not in list(ext_manager.extension_level.keys()):
        await message.channel.send("Level not found")
        return
    else:
        await ext_manager.change_level(message.content)


@bot.command()
async def reinit_manager(ctx):
    """Reinitialize the ExtensionManager with the current extension_levle. Will add any new discovered extension files
    to the list of all available extensions to the manager."""
    await ext_manager.reinit()
    await ctx.send("Successfully reinitialize.")


@bot.command()
async def reload_all(ctx):
    """Reloads all the current loaded extensions"""
    await ext_manager.reload_all()
    await ctx.send("Successfully reloaded.")


@bot.event
async def on_member_join(ctx, member):
    await ctx.send(f'Oh god, look at {member}.')


@bot.event
async def on_member_remove(ctx, member):
    await ctx.send(f'Everyone say bye {member}.')


bot.run(TOKEN)
