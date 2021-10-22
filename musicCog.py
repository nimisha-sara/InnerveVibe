import discord
from discord.ext import commands

import youtube_dl

import urllib.request
import json

import os
import dotenv
dotenv.load_dotenv()

class MusicBot(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
        self.is_playing = False
        self.songs_queue = []
        self.current_song = ''
        self.ydl_fomratting = {'format': 'bestaudio/worst', 'noplaylist':'True'}
        self.ffmpeg_formatting = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.voice = ''

    def song_lyrics(self, song):
        from lyrics_extractor import SongLyrics
        extract_lyrics = SongLyrics(os.getenv('GCS_API_KEY'), os.getenv('GCS_ENGINE_ID'))
        try:
            data = extract_lyrics.get_lyrics(song)
        except:
            return "No lyrics found"
        return data['lyrics']

    def search_song(self, song):
        '''
        Search for a song on youtube and get the most relevent search result
        '''
        with youtube_dl.YoutubeDL(self.ydl_fomratting) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % song, download=False)['entries'][0]
            except Exception: 
                return False
        
        search = info['title'].replace('-', '')
        search = search.replace('|', '')
        search = search.replace('@', '')
        search = search.replace(' ', '+')
        print(search)
        url = "https://www.googleapis.com/youtube/v3/search?key="+os.getenv('API_KEY')+"&part=snippet&q="+search+"&maxResults=1&videoDuration=short&type=video"
        url = url.encode("utf-8")
        response = urllib.request.urlopen(url.decode('ASCII')).read()
        data = json.loads(response)['items'][0]
        thumbnail_img = data['snippet']['thumbnails']['high']['url']
        video_url = f"https://www.youtube.com/watch?v={data['id']['videoId']}"

        return {'url': info['formats'][0]['url'], 'song-title': info['title'], 'image_url': thumbnail_img, 'video_url': video_url, 'user_search': song}

    def play_next(self):

        if len(self.songs_queue) > 0:
            self.is_playing = True

            url = self.songs_queue[0][0]['url']        
            self.current_song = self.songs_queue[0][0]['song-title']
            self.songs_queue.pop(0)

            self.voice.play(discord.FFmpegPCMAudio(url, **self.ffmpeg_formatting), after=lambda e: self.play_next())
        else:
            self.is_playing = False


    async def play_music(self):
        if len(self.songs_queue) > 0:
            self.is_playing = True

            url = self.songs_queue[0][0]['url']

            if self.voice == "" or not self.voice.is_connected() or self.voice == None:
                self.voice = await self.songs_queue[0][1].connect()
            else:
                await self.voice.move_to(self.songs_queue[0][1])
            
            self.current_song = self.songs_queue[0][0]['song-title']
            self.songs_queue.pop(0)

            self.voice.play(discord.FFmpegPCMAudio(url, **self.ffmpeg_formatting), after=lambda e: self.play_next())
        else:
            self.is_playing = False


    @commands.command(name="play")
    async def play(self, ctx, *song_str):
        song_name = " ".join(song_str)      
       
        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        else:
            song = self.search_song(song_name)
            self.songs_queue.append([song, voice_channel])

            embed=discord.Embed(title=f"\n{self.songs_queue[-1][0]['song-title']}", url=self.songs_queue[-1][0]['video_url'], description='**Added to queue**')
            embed.set_thumbnail(url=self.songs_queue[0][0]['image_url'])
            await ctx.send(embed=embed)

            if self.is_playing == False:
                await self.play_music()


    @commands.command(name="queue")
    async def queue(self, ctx):
        song_list = ""
        for i in range(0, len(self.songs_queue)):
            song_list += str(i + 1) + ". **" + self.songs_queue[i][0]['song-title'] + "**\n\n"

        if song_list != "":
            embed=discord.Embed(title="Queue", description=song_list)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Queue", description="No songs in queue")
            await ctx.send(embed=embed)


    @commands.command(name="skip")
    async def skip(self, ctx):
        if self.voice != "" and self.voice:
            self.voice.stop()
            await self.play_music()
        await ctx.message.channel.purge(limit=1)


    @commands.command(name="leave")
    async def leave(self, ctx):
        if self.voice.is_connected():
            await self.voice.disconnect()
        else:
            await ctx.send("InnerveVibe is not connected to any voice channel")
        await ctx.message.channel.purge(limit=1)


    @commands.command(name="pause")
    async def pause(self, ctx):
        if self.voice.is_playing():
            self.voice.pause()
        else:
            await ctx.send("No audio playing !")
        await ctx.message.channel.purge(limit=1)


    @commands.command(name="resume")
    async def resume(self, ctx):
        if self.voice.is_paused():
            self.voice.resume()
        else:
            await ctx.send("The audio is already running !")
        await ctx.message.channel.purge(limit=1)


    @commands.command(name="lyrics")
    async def lyrics(self, ctx):
        lyrics = self.song_lyrics(self.current_song)
        if lyrics != "No lyrics found":
            embed=discord.Embed(title=f"{self.current_song}", description=lyrics)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Lyrics not found")


    @commands.command(name="now")
    async def now(self, ctx):
        embed=discord.Embed(title=f"\n{self.current_song}")
        embed.set_thumbnail(url=self.songs_queue[0][0]['image_url'])
        await ctx.send(embed=embed)
