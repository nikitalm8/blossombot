import asyncio
import pytube

from asyncio import AbstractEventLoop
from discord import (
    FFmpegPCMAudio,
    PCMVolumeTransformer,
)


async def get_source(url, loop=None) -> PCMVolumeTransformer:

    for _ in range(3):

        try:

            return (await VolumeTransformer.from_url(url, loop=loop))

        except:
            
            continue


class VolumeTransformer(PCMVolumeTransformer): 
    """
    A PCMVolumeTransformer subclass that fetches YouTube audio streams
    """

    DEFAULT_OPTIONS = {
        'options': '-vn',
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    } 


    def __init__(self, source: FFmpegPCMAudio, volume: int=0.5) -> None:
        
        super().__init__(source, volume)


    @classmethod
    async def from_url(cls, url: str, loop: AbstractEventLoop=None, volume: int=0.5) -> PCMVolumeTransformer:

        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, 
            lambda: pytube.YouTube(url).streams.filter(only_audio=True)[-1].url
        )

        return cls(FFmpegPCMAudio(data, **cls.DEFAULT_OPTIONS), volume)


async def search(loop: AbstractEventLoop, query: str) -> pytube.YouTube:

    for _ in range(3):

        try:

            return (await loop.run_in_executor(
                None, 
                lambda: pytube.Search(query).results[0]
            ))

        except:

            continue
