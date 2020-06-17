import discord
from discord.ext import commands
import numpy as rand

# List of possible moves (r = rock, p = paper, s = scissors)
moves = ['r', 'p', 's']

# Input the probability % of each element
probabilityOfElm = [.33, .33, .33]

# Number of elements in game (rock, paper, scissors)
numOfElem = 3


async def random():
    if sum(probabilityOfElm) != 1:
        return rand.random.choice(moves)
    else:
        return rand.random.choice(moves, p=probabilityOfElm)


async def question(ctx):
    await ctx.send("(r)ock, (p)aper, (s)cissors? (q)uit")


class RockPaperScissors(commands.Cog):
    currentState = None

    def __init__(self, client):
        self.client = client

    async def setUp(self, ctx):
        await question(ctx)
        while self.currentState:
            playerChoice = await self.client.wait_for('message', timeout=30)
            botChoice = await random()
            await self.winCondition(ctx, botChoice, playerChoice)

    async def winCondition(self, ctx, botChoice, playerChoice):
        if playerChoice.content.lower() == 'q':
            await self.endGame(ctx)

        elif playerChoice.content.lower() not in moves:
            await ctx.send("Check your answer dumbass")
            await question(ctx)

        else:
            indexOfPlayer = moves.index(playerChoice.content.lower())
            indexOfBot = moves.index(botChoice)
            await ctx.send(botChoice)
            winner = (numOfElem + indexOfBot - indexOfPlayer) % numOfElem

            # condition 1, if winner is an even number, the bot wins
            if winner % 2 != 0:
                await ctx.send("I win!")

            # condition 2, if winner is an odd number, the user wins
            elif winner > 0 and winner % 2 == 0:
                await ctx.send("You win!")

            # condition 3, if winner is 0, players tie
            else:
                await ctx.send("It is a tie!")
            await question(ctx)

    async def endGame(self, ctx):
        self.currentState = False
        await ctx.send("Thank you for playing :)")

    @commands.command(aliases=['rps', 'rock', 'paper', 'scissors'])
    async def greeting(self, ctx):

        # if user invokes rps twice, ignore the command and display message
        if self.currentState:
            await ctx.send("Game already started")
        else:
            await ctx.send("Let's play some rock, paper, scissors!")
            self.currentState = True
            await self.setUp(ctx)


def setup(client):
    client.add_cog(RockPaperScissors(client))
