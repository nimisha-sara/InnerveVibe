import discord
from discord.ext import commands

from musicCog import MusicBot
from FunCog import FunBot

import os
import dotenv

dotenv.load_dotenv()

bot = commands.Bot(command_prefix = '%')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('\n---------------')
    print('Bot is online')
    print('---------------\n')

bot.add_cog(MusicBot(bot))
bot.add_cog(FunBot(bot))


@bot.command()
async def clear(ctx, amount=5):
    # Purges last 5 messages in the channel
    await ctx.channel.purge(limit=amount)

# HELP COMMAND    
@bot.group(invoke_without_command=True)
async def helpcmd(ctx):
    em = discord.Embed(title="Help", description="Use %help <command> for more info on that command")
    em.add_field(name="Music", value="`play`, `pause`, `resume`, `skip`, `queue`, `leave`, `lyrics`",  inline=False)
    em.add_field(name="Fun", value="`roll_die`, `coin_toss`, `wiki`, `m8ball`, `dumb_charades`, `text_ascii`, `team`, `poll`",  inline=False)
    em.add_field(name="Utility", value="`helpcmd`, `clear`",  inline=False)
    await ctx.send(embed=em)

@helpcmd.command()
async def play(ctx):
    em = discord.Embed(title="Play", description="Plays the song specified by member")
    em.add_field(name="**Syntax**", value="`%play <name of song>`")
    await ctx.send(embed=em)

@helpcmd.command()
async def resume(ctx):
    em = discord.Embed(title="Resume", description="Resumes the song if paused")
    em.add_field(name="**Syntax**", value="`%play <name of song>`")
    await ctx.send(embed=em)

@helpcmd.command()
async def pause(ctx):
    em = discord.Embed(title="Pause", description="Pauses the current song")
    em.add_field(name="**Syntax**", value="`%pause`")
    await ctx.send(embed=em)

@helpcmd.command()
async def skip(ctx):
    em = discord.Embed(title="Skip", description="Skips the current song and plays the next song in queue")
    em.add_field(name="**Syntax**", value="`%skip`")
    await ctx.send(embed=em)

@helpcmd.command()
async def queue(ctx):
    em = discord.Embed(title="Queue", description="Displays the songs in the current queue")
    em.add_field(name="**Syntax**", value="`%queue`")
    await ctx.send(embed=em)

@helpcmd.command()
async def leave(ctx):
    em = discord.Embed(title="Leave", description="Bot leaves the voice  channel")
    em.add_field(name="**Syntax**", value="`%leave`")
    await ctx.send(embed=em)

@helpcmd.command()
async def lyrics(ctx):
    em = discord.Embed(title="Lyrics", description="Displays the lyrics of the now playing song")
    em.add_field(name="**Syntax**", value="`%lyrics`")
    await ctx.send(embed=em)

@helpcmd.command()
async def roll_die(ctx):
    em = discord.Embed(title="Roll Die", description="Display a no between 1 and 6")
    em.add_field(name="**Syntax**", value="`%roll_die`")
    await ctx.send(embed=em)

@helpcmd.command()
async def toss_coin(ctx):
    em = discord.Embed(title="Toss Coin", description="Chooses heads or tails")
    em.add_field(name="**Syntax**", value="`%toss_coin`")
    await ctx.send(embed=em)

@helpcmd.command()
async def wiki(ctx):
    em = discord.Embed(title="Random Wiki", description="Display a random wikipedia article")
    em.add_field(name="**Syntax**", value="`%wiki`")
    await ctx.send(embed=em)

@helpcmd.command()
async def m8ball(ctx):
    em = discord.Embed(title="Magic 8 ball", description="Displays a magic 8 ball reply")
    em.add_field(name="**Syntax**", value="`%m8ball <question>`")
    await ctx.send(embed=em)

@helpcmd.command()
async def dumb_charades(ctx):
    em = discord.Embed(title="Dumb charades", description="Sents a movie to name and details to tagged member")
    em.add_field(name="**Syntax**", value="`%dumb_charades <tag member>`")
    await ctx.send(embed=em)

@helpcmd.command()
async def text_ascii(ctx):
    em = discord.Embed(title="Text Ascii", description="Displays ascii art of the text entered")
    em.add_field(name="**Syntax**", value="`%text_ascii <text>`")
    await ctx.send(embed=em)

@helpcmd.command()
async def team(ctx):
    em = discord.Embed(title="Team split", description="Splits the users who react to a msg into specified no of teams")
    em.add_field(name="**Syntax**", value="`%team <no_of_teams, default=2>`")
    await ctx.send(embed=em)

@helpcmd.command()
async def poll(ctx):
    em = discord.Embed(title="Poll", description="Displays a poll message in the server")
    em.add_field(name="**Syntax**", value="`%poll <question> <options, min=2, max=6>`")
    await ctx.send(embed=em)

@helpcmd.command()
async def clear(ctx):
    em = discord.Embed(title="Clear", description="clears specified no of msgs frm channel")
    em.add_field(name="**Syntax**", value="`%clear <number, default=5>`")
    await ctx.send(embed=em)


bot.run(os.getenv('TOKEN')) # use os.gtenv('') to call a particular variable
