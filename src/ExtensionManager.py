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


async def format_helper(list_of_extensions):
    msg = "```"
    for extension in list_of_extensions:
        msg = msg + "{}/n".format(extension)
    msg += "```"
    return msg


class ExtensionManager:
    def __init__(self, bot, level='Minimum'):
        self.bot = bot
        self.level = level
        self.extension_dict = {}

    async def _create(self):
        self.extensions_dict = await create_file_dict("Extensions")
        self.extension_level = {
            # Dictionary for how many extensions to add during the initialization of the bot.
            # All of the values are lists of extension names.
            'All': list(self.extensions_dict.keys()),
            'Partial': ['Greetings'],
            'Minimum': []
        }

    async def load(self):
        await self._create()
        extensions = self.extension_level[self.level]
        for extension in extensions:
            self.bot.load_extension(self.extensions_dict[extension])
            print("Finished loading: {}".format(extension))
        self.bot.add_cog(ExtensionLoader(self.bot, extensions.append('ExtensionLoader'), self.extension_dict))

    async def reinit(self):
        pass

    async def reload_all(self):
        pass


class ExtensionLoader(commands.bot):
    def __init__(self, bot, loaded_extensions, extension_dict):
        self.bot = bot
        self.loaded_extensions = loaded_extensions
        self.extension_dict = extension_dict

    @commands.command()
    async def load(self, ctx, extension):
        """Load the named extension using the extension dictionary"""
        channel = ctx.message.channel
        if not (extension in list(self.xtensions_dict.keys())):
            channel.send("Extension not found")
        elif extension in self.loaded_extensions:
            channel.send("Extension already loaded. Do you want to reload it? (Y/N)")
            try:
                def check(m):
                    m = m.upper().lower()
                    return m == 'y' or m == 'n'

                msg = await self.bot.wait_for('message', timeout=60, check=check)
                if msg.content.upper().lower() == 'y':
                    self.bot.reload_extension(self.extensions_dict[extension])
                    await channel.send("Successfully reloaded {}".format(extension))
                else:
                    return
            except asyncio.TimeoutError:
                await channel.send('No answer received.')
        else:
            self.bot.load_extension(self.extensions_dict[extension])
            self.loaded_extensions.append(extension)
            await channel.send("Successfully loaded {}".format(extension))

    @commands.command()
    async def loaded(self, ctx):
        """Sends the list of all loaded extensions to the channel that the user issued the command"""
        channel = ctx.message.channel
        msg = await format_helper(self.loaded_extensions)
        await channel.send(msg)

    @commands.command()
    async def listext(self, ctx):
        """Sends the list of all available """
        channel = ctx.message.channel
        msg = format_helper(list(self.extensions_dict.keys()))
        await channel.send(msg)
