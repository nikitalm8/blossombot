import discord
import youtube_dl
import pytube
import asyncio

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
} 

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)




async def get_source(url, loop=None, stream=True):
    attempt = 0
    while attempt <= 3:
        try:
            return await YTDLSource.from_url(url, loop=loop, stream=stream)
        except Exception:
            print(
                'Exception thrown when attempting to run get_source, attempt '
                f'{attempt} of 3'
            )
        attempt += 1



class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data=None, volume=0.5):
        
        super().__init__(source, volume)


    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, play=False):

        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: pytube.YouTube(url).streams.filter(only_audio=True)[-1].url)

        filename = data
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options))


async def search(loop: asyncio.AbstractEventLoop, query: str) -> pytube.YouTube:

    for _ in range(3):

        try:

            return (await loop.run_in_executor(None, lambda: pytube.Search(query).results[0]))

        except Exception as e:

            print(e)
            continue