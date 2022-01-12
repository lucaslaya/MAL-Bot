#anime search, manga search, seasonal search, user search
#TODO:
#- anime, manga, seasonal: add more genres to display in the embed
#- seasonal (possibly also in anime and manga): cycle pages to find the desired show
#- seasonal: change the embed to feature airing times of the show

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import requests
import json
import asyncio
from typing import Union
from datetime import datetime

CLIENT_ID = 'YOUR CLIENT ID'
CLIENT_SECRET = 'YOUR CLIENT SECRET'

current_season = int(datetime.now().month)
current_year = int(datetime.now().year)

if current_season < 4:
    current_season = str('winter')
elif 4 <= current_season < 7:
    current_season = str('spring')
elif 7 <= current_season < 10:
    current_season = str('summer')
else:
    current_season = str('fall')

class searchcogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def anime(self, ctx, *, anime):
        search_url = f'https://api.myanimelist.net/v2/anime?q={anime}'
        search_response = requests.get(search_url, headers=
        {
            'X-MAL-CLIENT-ID': CLIENT_ID
        })

        search = search_response.json()

        search_options = await ctx.send('```Select an option by reacting to the message:\n\n1. {name1}\n2. {name2}\n3. {name3}\n4. {name4}\n5. {name5}```'.format(
            name1=search['data'][0]['node']['title'],
            name2=search['data'][1]['node']['title'],
            name3=search['data'][2]['node']['title'],
            name4=search['data'][3]['node']['title'],
            name5=search['data'][4]['node']['title']
        ))

        selected_id = 0

        search_emojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣']
        await search_options.add_reaction(search_emojis[0])
        await search_options.add_reaction(search_emojis[1])
        await search_options.add_reaction(search_emojis[2])
        await search_options.add_reaction(search_emojis[3])
        await search_options.add_reaction(search_emojis[4])

        def check(r: discord.Reaction,u: Union[discord.Member, discord.User]):  # r = discord.Reaction, u = discord.Member or discord.User.
            return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and str(r.emoji) in search_emojis

        try:
            reaction, user = await self.bot.wait_for(event='reaction_add', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Please react faster next time. Message has timed out.')
            return
        else:
            if str(reaction.emoji) == search_emojis[0]:
                selected_id = 0
            if str(reaction.emoji) == search_emojis[1]:
                selected_id = 1
            if str(reaction.emoji) == search_emojis[2]:
                selected_id = 2
            if str(reaction.emoji) == search_emojis[3]:
                selected_id = 3
            if str(reaction.emoji) == search_emojis[4]:
                selected_id = 4

        await ctx.channel.purge(limit=1)

        search_id = search['data'][selected_id]['node']['id']

        url = f'https://api.myanimelist.net/v2/anime/{search_id}?fields=title,main_picture,alternative_titles,synopsis,mean,rank,genres,status'
        response = requests.get(url, headers=
        {
            'X-MAL-CLIENT-ID': CLIENT_ID
        })

        anime_info = response.json()

        #print(json.dumps(anime_info, sort_keys=True, indent=4))

        #Might what to change the status format before printing as it isn't clean

        #Shorten synopsis that are too long for embed
        synopsis_raw = anime_info['synopsis']
        synopsis = (synopsis_raw[:1020] + ' ...') if len(synopsis_raw) > 1020 else synopsis_raw

        #Check if anime is missing some info
        try:
            score = anime_info['mean']
            rank = anime_info['rank']
        except KeyError:
            score = 'N/A'
            rank = 'N/A'

        eng_title_check = anime_info['alternative_titles']['en']

        if eng_title_check == '':
            eng_title = anime_info['title']
        else:
            eng_title = eng_title_check

        embed = discord.Embed(title="Score: {score}| Rank: {rank}".format(score=score, rank=rank), color=0xd6386f)
        embed.set_author(name="{ENG} | {JAP}".format(ENG=eng_title, JAP=anime_info['alternative_titles']['ja']), url="https://myanimelist.net/anime/{id}".format(id=search_id))
        embed.set_thumbnail(url=anime_info['main_picture']['large'])
        embed.add_field(name="Synopsis:", value=synopsis, inline=False)
        embed.set_footer(text="Status: {status} | Genres: {genre1}, {genre2}".format(status=anime_info['status'], genre1=anime_info['genres'][0]['name'], genre2=anime_info['genres'][1]['name']))
        await ctx.send(embed=embed)

    @anime.error
    async def anime_error(self, error, ctx):
        print(f'⚠ An error ({error}) has occured while {error.author} used the ANIME command in {error.channel.name}.')

    @commands.command()
    async def manga(self, ctx, *, manga):
        search_url = f'https://api.myanimelist.net/v2/manga?q={manga}'
        search_response = requests.get(search_url, headers=
        {
            'X-MAL-CLIENT-ID': CLIENT_ID
        })

        search = search_response.json()

        search_options = await ctx.send(
            '```Select an option by reacting to the message:\n\n1. {name1}\n2. {name2}\n3. {name3}\n4. {name4}\n5. {name5}```'.format(
                name1=search['data'][0]['node']['title'],
                name2=search['data'][1]['node']['title'],
                name3=search['data'][2]['node']['title'],
                name4=search['data'][3]['node']['title'],
                name5=search['data'][4]['node']['title']
            ))

        selected_id = 0

        search_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        await search_options.add_reaction(search_emojis[0])
        await search_options.add_reaction(search_emojis[1])
        await search_options.add_reaction(search_emojis[2])
        await search_options.add_reaction(search_emojis[3])
        await search_options.add_reaction(search_emojis[4])

        def check(r: discord.Reaction, u: Union[discord.Member, discord.User]):  # r = discord.Reaction, u = discord.Member or discord.User.
            return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and str(r.emoji) in search_emojis

        try:
            reaction, user = await self.bot.wait_for(event='reaction_add', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Please react faster next time. Message has timed out.')
            return
        else:
            if str(reaction.emoji) == search_emojis[0]:
                selected_id = 0
            if str(reaction.emoji) == search_emojis[1]:
                selected_id = 1
            if str(reaction.emoji) == search_emojis[2]:
                selected_id = 2
            if str(reaction.emoji) == search_emojis[3]:
                selected_id = 3
            if str(reaction.emoji) == search_emojis[4]:
                selected_id = 4

        await ctx.channel.purge(limit=1)

        search_id = search['data'][selected_id]['node']['id']

        url = f'https://api.myanimelist.net/v2/manga/{search_id}?fields=title,main_picture,alternative_titles,synopsis,mean,rank,genres,status'
        response = requests.get(url, headers=
        {
            'X-MAL-CLIENT-ID': CLIENT_ID
        })

        manga_info = response.json()

        # print(json.dumps(anime_info, sort_keys=True, indent=4))

        # Shorten synopsis that are too long for embed
        synopsis_raw = manga_info['synopsis']
        synopsis = (synopsis_raw[:1020] + ' ...') if len(synopsis_raw) > 1020 else synopsis_raw

        # Check if manga is missing some info
        try:
            score = manga_info['mean']
            rank = manga_info['rank']
        except KeyError:
            score = 'N/A'
            rank = 'N/A'

        eng_title_check = manga_info['alternative_titles']['en']

        if eng_title_check == '':
            eng_title = manga_info['title']
        else:
            eng_title = eng_title_check

        embed = discord.Embed(title="Score: {score}| Rank: {rank}".format(score=score, rank=rank), color=0xd6386f)
        embed.set_author(name="{ENG} | {JAP}".format(ENG=eng_title, JAP=manga_info['alternative_titles']['ja']), url="https://myanimelist.net/manga/{id}".format(id=search_id))
        embed.set_thumbnail(url=manga_info['main_picture']['large'])
        embed.add_field(name="Synopsis:", value=synopsis, inline=False)
        embed.set_footer(text="Status: {status} | Genres: {genre1}, {genre2}".format(status=manga_info['status'], genre1=manga_info['genres'][0]['name'], genre2=manga_info['genres'][1]['name']))
        await ctx.send(embed=embed)

    @manga.error
    async def manga_error(self, error, ctx):
        print(f'⚠ An error ({error}) has occured while {error.author} used the MANGA command in {error.channel.name}.')

    @commands.command()
    async def season(self, ctx, season=current_season, year=current_year):
        url = f'https://api.myanimelist.net/v2/anime/season/{year}/{season}?sort=anime_num_list_users'
        response = requests.get(url, headers=
        {
            'X-MAL-CLIENT-ID': CLIENT_ID
        })

        season_info = response.json()

        page = 0
        selected_id = 0

        seasonal_anime = await ctx.send('```Seasonal Anime {season} {year}\nSelect an option by reacting to the message:\n\n1. {name1}\n2. {name2}\n3. {name3}\n4. {name4}\n5. {name5}\n6. {name6}\n7. {name7}\n8. {name8}\n9. {name9}\n10. {name10}```'.format(
                season=season,
                year=year,
                name1=season_info['data'][0]['node']['title'],
                name2=season_info['data'][1]['node']['title'],
                name3=season_info['data'][2]['node']['title'],
                name4=season_info['data'][3]['node']['title'],
                name5=season_info['data'][4]['node']['title'],
                name6=season_info['data'][5]['node']['title'],
                name7=season_info['data'][6]['node']['title'],
                name8=season_info['data'][7]['node']['title'],
                name9=season_info['data'][8]['node']['title'],
                name10=season_info['data'][9]['node']['title']
            ))

        search_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        await seasonal_anime.add_reaction(search_emojis[0])
        await seasonal_anime.add_reaction(search_emojis[1])
        await seasonal_anime.add_reaction(search_emojis[2])
        await seasonal_anime.add_reaction(search_emojis[3])
        await seasonal_anime.add_reaction(search_emojis[4])
        await seasonal_anime.add_reaction(search_emojis[5])
        await seasonal_anime.add_reaction(search_emojis[6])
        await seasonal_anime.add_reaction(search_emojis[7])
        await seasonal_anime.add_reaction(search_emojis[8])
        await seasonal_anime.add_reaction(search_emojis[9])

        def check(r: discord.Reaction, u: Union[discord.Member, discord.User]):  # r = discord.Reaction, u = discord.Member or discord.User.
            return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and str(r.emoji) in search_emojis

        try:
            reaction, user = await self.bot.wait_for(event='reaction_add', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Please react faster next time. Message has timed out.')
            return
        else:
            if str(reaction.emoji) == search_emojis[0]:
                selected_id = 0
            if str(reaction.emoji) == search_emojis[1]:
                selected_id = 1
            if str(reaction.emoji) == search_emojis[2]:
                selected_id = 2
            if str(reaction.emoji) == search_emojis[3]:
                selected_id = 3
            if str(reaction.emoji) == search_emojis[4]:
                selected_id = 4
            if str(reaction.emoji) == search_emojis[5]:
                selected_id = 5
            if str(reaction.emoji) == search_emojis[6]:
                selected_id = 6
            if str(reaction.emoji) == search_emojis[7]:
                selected_id = 7
            if str(reaction.emoji) == search_emojis[8]:
                selected_id = 8
            if str(reaction.emoji) == search_emojis[9]:
                selected_id = 9

        await ctx.channel.purge(limit=1)

        search_id = season_info['data'][selected_id]['node']['id']

        url = f'https://api.myanimelist.net/v2/anime/{search_id}?fields=title,main_picture,alternative_titles,synopsis,mean,rank,genres,status'
        response = requests.get(url, headers=
        {
            'X-MAL-CLIENT-ID': CLIENT_ID
        })

        anime_info = response.json()

        # print(json.dumps(anime_info, sort_keys=True, indent=4))

        # Might what to change the status format before printing as it isn't clean

        # Shorten synopsis that are too long for embed
        synopsis_raw = anime_info['synopsis']
        synopsis = (synopsis_raw[:1020] + ' ...') if len(synopsis_raw) > 1020 else synopsis_raw

        # Check if anime is missing some info
        try:
            score = anime_info['mean']
            rank = anime_info['rank']
        except KeyError:
            score = 'N/A'
            rank = 'N/A'

        eng_title_check = anime_info['alternative_titles']['en']

        if eng_title_check == '':
            eng_title = anime_info['title']
        else:
            eng_title = eng_title_check

        embed = discord.Embed(title="Score: {score}| Rank: {rank}".format(score=score, rank=rank), color=0xd6386f)
        embed.set_author(name="{ENG} | {JAP}".format(ENG=eng_title, JAP=anime_info['alternative_titles']['ja']), url="https://myanimelist.net/anime/{id}".format(id=search_id))
        embed.set_thumbnail(url=anime_info['main_picture']['large'])
        embed.add_field(name="Synopsis:", value=synopsis, inline=False)
        embed.set_footer(text="Status: {status} | Genres: {genre1}, {genre2}".format(status=anime_info['status'], genre1=anime_info['genres'][0]['name'], genre2=anime_info['genres'][1]['name']))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(searchcogs(bot))
