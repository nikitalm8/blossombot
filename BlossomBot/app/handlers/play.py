from app.utils import ytdl
from app.utils.check_for_command import answer_or_react
from app.templates import play as texts, queue

from discord.ext import commands

    
class PlayerHandlers(commands.Cog):
    """
    Cog for handling player commands
    """

    def __init__(self, bot: commands.Bot) -> None:

        self.bot = bot


    @commands.hybrid_command(description='Plays the song')
    async def play(self, ctx: commands.Context, *, song: str=None):

        from_this_song = False

        if not ctx.voice_client:

            from_this_song = True

        await self.join(ctx)

        if not song and ctx.voice_client.is_paused() and ctx.queue.queue:

            ctx.voice_client.resume()
            return await answer_or_react(
                ctx,
                texts.resume[ctx.guild_info.Language],
                '<:botplay~2:892866024670646322>',
            )

        msg = await ctx.send(
            texts.searching[ctx.guild_info.Language] % song
        )

        song = await ytdl.search(ctx.bot.loop, song)

        if not song:

            return await msg.edit(
                content=queue.notfound[ctx.guild_info.Language]
            )

        if from_this_song:

            ctx.queue.addfirst(song)

        else:

            ctx.queue.add(song)

        if ctx.voice_client.is_playing():

            await msg.edit(
                content=queue.add(
                    song=song,
                    lang=ctx.guild_info.Language,
                ),
            )   

    
    @commands.hybrid_command(description='Pauses the song')
    async def pause(self, ctx: commands.Context):

        if ctx.voice_client:

            ctx.voice_client.pause()

        await answer_or_react(
            ctx,
            texts.pause[ctx.guild_info.Language],
            '<:botpause~2:892866024616132608>',
        )


    @commands.hybrid_command(description='Skips the song')
    async def skip(self, ctx: commands.Context):
            
        if ctx.voice_client:

            ctx.voice_client.stop()

        await answer_or_react(
            ctx, 
            texts.skip[ctx.guild_info.Language],
            '<:skip~2:892998428609642506>'
        )


    @commands.hybrid_command(description='Leave the voice channel')
    async def leave(self, ctx: commands.Context):

        if ctx.voice_client:

            await ctx.voice_client.disconnect()
            await ctx.send(
                texts.left[ctx.guild_info.Language]
            )
        
        del ctx.queue


    @commands.hybrid_command(description='Joins the voice channel')
    async def join(self, ctx: commands.Context):

        if not ctx.author.voice:

            return await ctx.send(
                texts.notconnected[ctx.guild_info.Language]
            )

        if ctx.voice_client and ctx.voice_client.channel != ctx.author.voice.channel:

            await ctx.voice_client.disconnect()

        elif ctx.voice_client:

            return

        await ctx.author.voice.channel.connect()
        await ctx.send(
            texts.joined[ctx.guild_info.Language] % ctx.author.voice.channel.mention
        )
