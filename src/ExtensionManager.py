import asyncio
import os

from discord.ext import commands


async def create_file_dict(directory):
    """Creates a dict with all the files available in the directory.
    Sets the file name as the key and its path using '.' as a delimiter instead of '/'
    """
    file_paths = await get_list_of_files(directory)
    file_dict = {}
    for file_path in file_paths:
        value = file_path.replace('/', '.').replace('.py', '')
        key = value[value.rindex('.') + 1:]
        file_dict[key] = value
    return file_dict


async def get_list_of_files(directory):
    all_files = []
    for i in os.listdir(directory):
        path = os.path.join(directory, i)
        if os.path.isdir(path):
            all_files = all_files + await get_list_of_files(path)
        else:
            all_files.append(path)
    return all_files


extensions_dict = await create_file_dict("Extensions")


class ExtensionManager:
    extension_level = {
        # Dictionary for how many extensions to add during the initialization of the bot.
        # All of the values are lists of extension names.
        'All': list(extensions_dict.keys()),
        'Partial': ['Greetings'],
        'Minimum': []
    }

    def __init__(self, bot, level='Minimum'):
        self.bot = bot
        self.level = level

    def load(self):
        extensions = ExtensionManager.extension_level[self.level]
        for extension in extensions:
            self.bot.load_extension(extensions_dict[extension])
            print("Finished loading: {}".format(extension))
        self.bot.add_cog(ExtensionLoader(self.bot, extensions.append('ExtensionLoader')))


class ExtensionLoader(commands.bot):
    def __init__(self, bot, loaded_extensions):
        self.bot = bot
        self.loaded_extensions = loaded_extensions

    @commands.command()
    async def load(self, ctx, extension):
        """Load the named extension using the extension dictionary"""
        channel = ctx.message.channel
        if not (extension in list(extensions_dict.keys())):
            channel.send("Extension not found")
        elif extension in self.loaded_extensions:
            channel.send("Extension already loaded. Do you want to reload it? (Y/N)")
            try:
                def check(m):
                    m = m.upper().lower()
                    return m == 'y' or m == 'n'

                msg = await self.bot.wait_for('message', timeout=60, check=check)
                if msg.content.upper().lower() == 'y':
                    self.bot.reload_extension(extensions_dict[extension])
                    await channel.send("Successfully reloaded {}".format(extension))
                else:
                    return
            except asyncio.TimeoutError:
                await channel.send('No answer received.')
        else:
            self.bot.load_extension(extensions_dict[extension])
            self.loaded_extensions.append(extension)
            await channel.send("Successfully loaded {}".format(extension))

    @commands.command()
    async def loaded(self, ctx):
        """Sends the list of all loaded extensions to the channel that the user issued the command"""
        channel = ctx.message.channel
        msg = await self.format_helper(self.loaded_extensions)
        await channel.send(msg)

    @commands.command()
    async def listext(self, ctx):
        channel = ctx.message.channel
        msg = self.format_helper(list(self.extensions_dict.keys()))
        await channel.send(msg)

    async def format_helper(self, list_of_extensions):
        msg = "```"
        for extension in self.list_of_extensions:
            msg = msg + "{}/n".format(extension)
        msg += "```"
        return msg
