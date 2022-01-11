#help, bot info

import discord
from discord.ext import commands
from discord.ext.commands import Bot

class helpcogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send(
            "```\nCOMMANDS\nBot command prefix = mal.\nExample: mal.anime Attack on Titan\n\n<Random>\ncats = Print a random cat fact. (Made this to learn the very basics of API)\ncoinflip = Flip a coin\n\n<Search>\nanime [title] = Search MAL for anime and display the info\nmanga [title] = Search MAL for manga and display the info\n\n<Logistical>\nping = Check bot response time\nbotinfo (Not yet enabled) = Display information about the bot\n\n<Extra Info>\nThis bot is still very new and I am working on adding more stuff to it which will allow you to do more things with MAL and your personal anime/manga lists. I'll update this command screen as I add them.\n```")

    @help.error
    async def help_error(self, error, ctx):
        print(f'⚠ An error ({error}) has occured while {error.author} used the HELP command in {error.channel.name}.')

    @commands.command()
    async def botinfo(self, ctx):
        pass

    @botinfo.error
    async def botinfo_error(self, error, ctx):
        print(f'⚠ An error ({error}) has occured while {error.author} used the BOTINFO command in {error.channel.name}.')

def setup(bot):
    bot.add_cog(helpcogs(bot))