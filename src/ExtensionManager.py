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
        value = file_path.replace('.py', '')
        key = value[value.rindex('.') + 1:]
        file_dict[key] = value
    return file_dict


async def get_list_of_files(directory):
    all_files = []

    def helper(path_dir, ext_path):
        for p in os.listdir(path_dir):
            if p.startswith('__'):
                continue
            path = os.path.join(path_dir, p)
            new_ext_path = ext_path + '.' + p
            if os.path.isdir(path):
                helper(path, new_ext_path)
            else:
                all_files.append(new_ext_path)

    helper(directory, directory)
    return all_files


async def format_helper(list_of_extensions):
    msg = "```"
    for extension in list_of_extensions:
        msg = msg + "{}/n".format(extension)
    msg += "```"
    return msg


class ExtensionManager:
    def __init__(self, bot, level="Minimum"):
        self.bot = bot
        self.extension_dict = {}
        self.extension_level = {}
        self.level = level
        self.loaded_extensions = []

    async def _create(self):
        """"Adds extensions_dict and extension_level as attributes."""
        self.extensions_dict = await create_file_dict("Extensions")
        self.extension_level = {
            # Dictionary for how many extensions to add during the initialization of the bot.
            # All of the values are lists of extension names.
            'All': list(self.extensions_dict.keys()),
            'Partial': ['Greetings'],
            'Minimum': []
        }

    async def load(self):
        """"Calls _create() to add the required attributes. Then loads the number of extensions based on level."""
        await self._create()
        self.loaded_extensions = self.extension_level[self.level]
        for extension in self.loaded_extensions:
            self.bot.load_extension(self.extensions_dict[extension])
            print("Finished loading: {}".format(extension))
        self.bot.add_cog(
            ExtensionLoader(self.bot, self.loaded_extensions.append('ExtensionLoader'), self.extension_dict))

    async def change_level(self, level):
        self.level = level

    async def reinit(self):
        for extension in self.loaded_extensions:
            self.bot.unload_extension(self.extensions_dict[extension])
        await self.load()

    async def reload_all(self):
        for extension in self.loaded_extensions:
            self.bot.reload_extension(self.extensions_dict[extension])


class ExtensionLoader(commands.Cog):
    def __init__(self, bot, loaded_extensions, extension_dict):
        self.bot = bot
        self.loaded_extensions = loaded_extensions
        self.extension_dict = extension_dict

    @commands.command()
    async def load(self, ctx, extension):
        """Load the named extension using the extension dictionary"""
        if not (extension in list(self.xtensions_dict.keys())):
            ctx.send("Extension not found")
        elif extension in self.loaded_extensions:
            ctx.send("Extension already loaded. Do you want to reload it? (Y/N)")
            try:
                def check(m):
                    m = m.upper().lower()
                    return m == 'y' or m == 'n'

                msg = await self.bot.wait_for('message', timeout=60, check=check)
                if msg.content.upper().lower() == 'y':
                    self.bot.reload_extension(self.extensions_dict[extension])
                    await ctx.send("Successfully reloaded {}".format(extension))
                else:
                    return
            except asyncio.TimeoutError:
                await ctx.send('No answer received.')
        else:
            self.bot.load_extension(self.extensions_dict[extension])
            self.loaded_extensions.append(extension)
            await ctx.send("Successfully loaded {}".format(extension))

    @commands.command()
    async def loaded(self, ctx):
        """Sends the list of all loaded extensions to the channel that the user issued the command"""
        msg = await format_helper(self.loaded_extensions)
        await ctx.send(msg)

    @commands.command()
    async def listext(self, ctx):
        """Sends the list of all available """
        msg = format_helper(list(self.extensions_dict.keys()))
        await ctx.send(msg)
