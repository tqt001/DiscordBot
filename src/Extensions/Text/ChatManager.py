from discord.ext import commands


class ChatManager(commands.bot):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, amount=50):
        await ctx.channel.purge(limit=amount)
        await ctx.channel.send('Clear complete.')


def setup(bot):
    bot.add_cog(ChatManager(bot))
