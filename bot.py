import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    print(f'Oh god, look at {member}.')

@client.event
async def on_member_remove(member):
    print(f'Everyone say bye {member}.')

@client.command()
async def 













client.run("NzIxMDY5NjAxMjIzNjA2Mzkz.XuP0Mg.PS9J2DIJmXau8nczJwbY4QYU8sA")
