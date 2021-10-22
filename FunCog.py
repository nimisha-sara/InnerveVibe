import discord
from discord.ext import commands

import random
import wikipedia
import pyfiglet

import json
import urllib.request

import asyncio

from bs4 import BeautifulSoup
import requests
import re



class FunBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def roll_die(self):
        return random.randint(1, 6)


    def toss_coin(self):
        return random.choice(['Head', 'Tail'])


    def random_wiki(self):
        wiki_article = wikipedia.random(1)
        wikipage = wikipedia.page(wiki_article)
        summary = wikipedia.summary(wiki_article, sentences = 6)
        url = wikipage.url
        return {'title': wiki_article,'summary': summary, 'url': url}


    def movie(self):
        url = 'http://www.imdb.com/chart/top'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        movies = soup.select('td.titleColumn')
        cast = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
        movie_list = []

        for index in range(0, len(movies)):
            movie_string = movies[index].get_text()
            movie = (' '.join(movie_string.split()).replace('.', ''))
            movie_title = movie[len(str(index))+1:-7]
            year = re.search('\((.*?)\)', movie_string).group(1)
            data = {"movie_title": movie_title,
                    "year": year,
                    "star_cast": cast[index]}
            movie_list.append(data)

        movie_index = random.randint(0, 249)
        return movie_list[movie_index]

    def team_split(self, members, num):
        no_of_members = len(members)
        teams = []
        while no_of_members > 0 and num > 0:
            team = random.sample(members, int(no_of_members/num))
            for x in team:
                members.remove(x)
            no_of_members -= int(no_of_members/num)
            num -= 1
            teams.append(team)
        return teams


    @commands.command(name="roll_die")
    async def rollDie(self, ctx):
        embed=discord.Embed(description=f"The die rolled a  **{self.roll_die()}**")
        await ctx.send(embed=embed)


    @commands.command(name="toss_coin")
    async def tossCoin(self, ctx):
        embed=discord.Embed(description=f"The coin tossed **{self.toss_coin()}**")
        await ctx.send(embed=embed)


    @commands.command(name="wiki")
    async def randWiki(self, ctx):
        data = self.random_wiki()
        embed=discord.Embed(title=data['title'], url=data['url'], description=data['summary'])
        await ctx.send(embed=embed)

    @commands.command(name="m8ball")
    async def eightBall(self, ctx, question = ""):
        if question == "":
            await ctx.send("Ask me a question first")
        else:
            choices = [
                       '🟢 It is certain.', '🟢 It is decidedly so.', '🟢 Without a doubt.', '🟢 Yes definitely.',
                       '🟢 You may rely on it.', '🟢 As I see it, yes.', '🟢 Most likely.', '🟢 Outlook good.',
                       '🟢 Yes.', '🟢 Signs point to yes.', '🟡 Reply hazy, try again.', '🟡 Ask again later.',
                       '🟡 Better not tell you now.', '🟡 Cannot predict now.', '🟡 Concentrate and ask again.',
                       "🔴 Don't count on it.", '🔴 My reply is no.', '🔴 My sources say no.', 
                       '🔴 Outlook not so good.', '🔴 Very doubtful.'
                      ]
            embed=discord.Embed(title='The magic 8ball says', description=random.choice(choices))
            await ctx.send(embed=embed)


    @commands.command(name='dumb_charades')
    async def dumbCharades(self, ctx, user : discord.User):
        msg = self.movie()
        embed=discord.Embed(title=msg['movie_title'], description=f"\n\n**Year** : {msg['year']}\n**Cast** : {msg['star_cast']}")
        try:
            await user.send(embed=embed)
            await ctx.send(f':white_check_mark: Movie sent')
        except:
            await ctx.send(f':x: {user} had their dm close')
        

    @commands.command(name="text_ascii")
    async def asciiArt(self, ctx, *text):
        text = " ".join(text) 
        ascii_banner = pyfiglet.figlet_format("Hello!!")
        embed=discord.Embed(description=f"```{ascii_banner}```")
        await ctx.send(embed=embed)


    @commands.command(name="team")
    async def team(self, ctx, num=2):

        embed=discord.Embed(title="Team split", description="**No of teams : ** `2`\n\n**React** to this msg to be included in the pool\n\n\n")
        embed.set_footer(text="NOTE: Poll ends in 30 sec.")
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

        await asyncio.sleep(30)

        channel = self.bot.get_channel(message.channel.id)        
        poll_message = await channel.fetch_message(message.id)

        await ctx.send(f"reactions: {poll_message.reactions}")
        user_names = []
        for reaction in poll_message.reactions:
            users = await reaction.users().flatten()
            for user in users:
                user_names.append(f"{user.name} #{user.discriminator}")
        user_names = list(set(user_names))

        await poll_message.delete()
        embed = discord.Embed(description="Time Over!!\nGenerating teams...")
        await ctx.send(embed=embed)
        await asyncio.sleep(1)
        await ctx.message.channel.purge(limit=1)

        user_names.remove('InnerveVibe #0999')

        if len(user_names) <= 2:
            embed = discord.Embed(description="Poll did not have any reaction.\nEnding poll")
            await ctx.send(embed=embed)
            return 
        random.shuffle(user_names)
        user_names = self.team_split(user_names, num)
        text = ''
        for i in range(len(user_names)):
            text += f'Team {i + 1}\n```'
            for player in user_names[i]:
                text += f"  {player}\n"
            text += '```\n\n'
        embed = discord.Embed(title="Teams", description=text)
        await ctx.send(embed=embed)

    @commands.command(name='poll')
    async def pollGenerate(self, ctx, question, *options):
        if len(options) <= 1:
            await ctx.send('Give atleast two options to start a a poll')
            return
        if len(options) > 6:
            await ctx.send("Yo! the poll's too big\n\nMax no of poll options : **6**")
            return

        if len(options) == 2 and options ==  ['yes', 'no'] or options == ['no', 'yes']:
            reactions = ['✅', '❌']
        else:
            reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']

        description = []
        for i, option in enumerate(options):
            description += '\n {} {}'.format(reactions[i], option)
        embed = discord.Embed(title=question, description=''.join(description))

        react_message = await ctx.send(embed=embed)

        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        await react_message.edit(embed=embed)
        
