from app.utils import ytdl
from app.utils.check_for_command import answer_or_react
from app.templates import queue as texts

from app.utils import client

from discord.ext import commands
from discord import MessageType

dummysong = client.Song(
    'test', 'test', 22
)

class QueueHandlers(commands.Cog):


    def __init__(self, bot: commands.Bot) -> None:

        self.bot = bot


    @commands.hybrid_command(description='Shows the queue')
    async def queue(self, ctx: commands.Context):

        await ctx.send(
            texts.queue(
                nowplaying=ctx.queue.nowplaying,
                songs=ctx.queue.queue,
                lang=ctx.guild_info.Language,
            )
        )
        

    @commands.hybrid_command(description='Adds a song to the queue')
    async def add(self, ctx: commands.Context, *, song: str):

        song = await ytdl.search(ctx.bot.loop, song)

        if not song:

            return await ctx.send(
                texts.notfound[ctx.guild_info.Language]
            )

        ctx.queue.add(
            song
        )
        await ctx.send(
            texts.add(
                song=song,
                lang=ctx.guild_info.Language,
            )
        )


    @commands.hybrid_command(description='Removes the song')
    async def remove(self, ctx: commands.Context, *, position: int):

        song = ctx.queue.remove(position)
        await ctx.send(
            texts.remove(
                song=song,
                lang=ctx.guild_info.Language,
            )
        )

    
    @commands.hybrid_command(description='Clears the queue')
    async def clear(self, ctx: commands.Context):

        ctx.queue.clear()

        await ctx.send(
            texts.clear[ctx.guild_info.Language]
        )

    
    @commands.hybrid_command(description='Loop the queue | song | off')
    async def loop(self, ctx: commands.Context, *, mode: str=None):

        if not mode:

            ctx.queue.loop = False if ctx.queue.loop else True
            mode = 0 if ctx.queue.loop else 2

        elif mode == 'queue':

            ctx.queue.loop = True
            mode = 0

        elif mode == 'song':

            ctx.queue.loop = False
            ctx.queue.singleloop = True
            mode = 1

        elif mode == 'off':

            ctx.queue.loop = False
            ctx.queue.singleloop = False
            mode = 2

        else:

            return await ctx.send(
                texts.choose[ctx.guild_info.Language]
            )

        await ctx.send(
            texts.looped(
                mode=mode,
                lang=ctx.guild_info.Language,
            )
        )


    @commands.hybrid_command(description='Shuffles the queue')
    async def shuffle(self, ctx: commands.Context):

        ctx.queue.shuffle()
        await answer_or_react(
            ctx,
            texts.shuffle[ctx.guild_info.Language],
            '🔀',
        )
