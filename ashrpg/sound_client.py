import asyncio
import discord
import json
import os
import random
import youtube_dl
from functools import partial
from time import sleep

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.mp3',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class SoundClient():

    SOUND_LIST_FILE = 'assets/sound_list.json'

    def __init__(self):
        with open(f"{os.path.dirname(__file__)}/{self.SOUND_LIST_FILE}", 'r') as f:
            self.sounds = json.load(f)

    async def play_sound(self, sound, ctx, loop):
        to_play = self.sounds.get(sound, '')
        if not to_play:
            to_play = random.choice(list(self.sounds.values()))

        voice_channel = ctx.author.voice.channel

        if voice_channel:
            await voice_channel.connect()

            player = await YTDLSource.from_url(to_play, loop=loop, stream=False)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

            while ctx.voice_client.is_playing():
                sleep(1)

            await ctx.voice_client.disconnect()
        else:
            print("User is not in a voice channel")

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
