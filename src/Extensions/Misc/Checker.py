from discord.ext import commands
import datetime


class StatChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        msg = ctx.message
        msg_time = msg.created_at.replace(tzinfo=datetime.timezone.utc)
        time_now = datetime.datetime.now(datetime.timezone.utc)
        print(msg_time)
        print(time_now)
        # ping = round((time_now - msg.created_at).total_seconds() * 1000)
        #  = round(self.bot.latency * 1000)
        # msg_send = "```Your latency to the bot is {}ms.\nDiscord API latency is: {}ms```".format(ping, discord_latency)
        # await msg.channel.send(msg_send)
        # await msg.channel.send("{} and {}".format(msg_time, time_now))


def setup(bot):
    bot.add_cog(StatChecker(bot))
