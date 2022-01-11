#Catfacts, coinflip, 8ball

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import requests
import json
import random
import asyncio

class randomcogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cats(self, ctx):
        catfact = requests.get("https://catfact.ninja/fact")
        print('Cat Facts API response = {0}'.format(catfact.status_code))

        catfact_out = json.loads(catfact.text)

        await ctx.send(catfact_out["fact"])

    @cats.error
    async def cats_error(self, error, ctx):
        print(f'⚠ An error ({error}) has occured while {error.author} used the CATS command in {error.channel.name}.')

    @commands.command()
    async def coinflip(self, ctx, *, choices="Heads|Tails"):
        answer = random.choice(list(map(str.strip, choices.split('|'))))

        flipping = await ctx.send("Flipping...")
        await asyncio.sleep(1.5)
        await flipping.delete()

        await ctx.send(answer)

    @coinflip.error
    async def coinflip_error(self, error, ctx):
        print(
            f'⚠ An error ({error}) has occured while {error.author} used the COINFLIP command in {error.channel.name}.')

def setup(bot):
    bot.add_cog(randomcogs(bot))