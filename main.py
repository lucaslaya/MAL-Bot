import discord
from discord.ext import commands
from discord.ext.commands import Bot

bot = Bot(command_prefix = "mal.")
bot.remove_command('help')

@bot.event
async def on_ready():
    print('/--------------------------------------------------------')
    print('| # BOT STARTING UP #')
    print('|--------------------------------------------------------')
    bot.load_extension("random-cogs")
    print('| random-cogs:                  LOADED')
    bot.load_extension("help-cogs")
    print('| help-cogs:                    LOADED')
    bot.load_extension("search-cogs")
    print('| search-cogs:                  LOADED')
    print('|--------------------------------------------------------')
    print('| BOT IS READY')
    print('|--------------------------------------------------------')
    print('| MyAnimeList (MAL) Companion Bot')
    print('| MADE BY: lucasssssss#0001')
    print('| DESCRIPTION:')
    print('| Companion bot made to interact with MAL API to find ')
    print('| anime, manga, characters, etc. Also features user ')
    print('| account connectivity to edit anime/manga lists and')
    print('| receive recommendations.')
    print('\--------------------------------------------------------')

    await bot.change_presence(activity=discord.Game('anime | mal.help'))

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}ms'.format(round(bot.latency * 1000)))

bot.run("YOUR DISCORD BOT TOKEN")
