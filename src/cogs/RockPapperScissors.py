import discord
from discord.ext import commands
import random


class RockPaperScissors(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def setUp(self, ctx, currentState):
        moves = ['r', 'p', 's']
        await self.question(ctx)

        while currentState:
            bot = random.randint(0, 2)
            player = await self.client.wait_for('message', timeout=30)

            if player.content.lower() == 'q':
                await ctx.send("Thank you for playing :)")
                currentState = False
                break

            if player.content.lower() not in moves:
                await ctx.send("Check your answer dumbass")
                await self.question(ctx)

            else:
                indexOfPlayer = moves.index(player.content.lower())
                await ctx.send(moves[bot])
                winner = (3 + bot - indexOfPlayer) % 3
                if winner == 1:
                    await ctx.send("I win!")
                elif winner == 2:
                    await ctx.send("You win!")
                else:
                    await ctx.send("It is a tie!")
                await self.question(ctx)

    async def question(self, ctx):
        await ctx.send("(r)ock, (p)aper, (s)cissors? (q)uit")

    @commands.command(aliases=['rps', 'rock', 'paper', 'scissors'])
    async def greeting(self, ctx):
        await ctx.send("Let's play some rock, paper, scissors!")
        currentState = True
        await self.setUp(ctx, currentState)


def setup(client):
    client.add_cog(RockPaperScissors(client))
