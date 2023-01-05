import asyncio
import pytube

from discord import (
    FFmpegPCMAudio,
    PCMVolumeTransformer,
)


async def get_source(url, loop=None, stream=True):

    for _ in range(3):

        try:

            return await YTDLSource.from_url(url, loop=loop, stream=stream)

        except:
            
            continue


class YTDLSource(PCMVolumeTransformer): # TODO: Refactor this class

    DEFAULT_OPTIONS = {
        'options': '-vn',
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    } 


    def __init__(self, source, *, data=None, volume=0.5):
        
        super().__init__(source, volume)


    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, play=False):
        """
        This method was first implemented via YoutubeDl, but it was replaced with Pytube
        The other code was not refactored, so some params are useless
        """

        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: pytube.YouTube(url).streams.filter(only_audio=True)[-1].url)

        return cls(FFmpegPCMAudio(data, **cls.DEFAULT_OPTIONS))


async def search(loop: asyncio.AbstractEventLoop, query: str) -> pytube.YouTube:

    for _ in range(3):

        try:

            return (await loop.run_in_executor(
                None, 
                lambda: pytube.Search(query).results[0]
            ))

        except:

            continue
