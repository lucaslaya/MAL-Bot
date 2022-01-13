#help, bot info

import discord
from discord.ext import commands
from discord.ext.commands import Bot

class helpcogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send("```\nCOMMANDS\nBot command prefix = mal.\nExample: mal.anime Attack on Titan\n\n<Random>\ncats = Print a random cat fact. (Made this to learn the very basics of API)\ncoinflip = Flip a coin\n\n<Search>\nanime [title] = Search MAL for anime and display the info\nmanga [title] = Search MAL for manga and display the info\n\nseason [season (default is current)] [year (default is current)] = Shows the seasonal anime for the selected season.\nFormat for seasons is:\n - winter\n - spring\n - summer\n - fall\n\nExample: mal.season spring 2019\n\nanimerank [type (default is all)] = Displays the top anime in the order selected. Type means the how the anime are ranked.\nFormat for rank types is:\n - all = Top anime series\n - airing = Top airing series\n - upcoming = Top upcoming series\n - tv = Top anime TV series\n - ova = Top anime OVA series\n - movie = Top anime movies\n - special = Top anime specials\n - bypopularity = Top anime by popularity\n - favorite = Top favorited anime\n\nExample: mal.animerank bypopularity\n\nmangarank [type (default is all)] = Displays the top manga in the order selected. Type means how the manga are ranked.\nFormat for rank types is:\n - all = All\n - manga = Top manga\n - novels = Top novels\n - oneshots = Top one-shots\n - doujin = Top doujinshi\n - manhwa = Top manhwa\n - manhua = Top manhua\n - bypopularity = Most popular\n - favorite = Most favorited\n\nExample: mal.mangarank manhua\n\n<Logistical>\nping = Check bot response time\nbotinfo (Not yet enabled) = Display information about the bot\n\n<Extra Info>\nThis bot is still very new and I am working on adding more stuff to it which will allow you to do more things with MAL and your personal anime/manga lists. I'll update this command screen as I add them.\n```\n")

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
