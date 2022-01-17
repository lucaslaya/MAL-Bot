#user manga/anime list update, get user information

import discord
from discord.ext import commands
from discord.ext.commands import Bot

class usercogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send('User cogs test')

def setup(bot):
    bot.add_cog(usercogs(bot))
