import config

from app.utils.client import VoiceClient
from app.database.models.guild import Guild

from sqlalchemy import select
from discord.ext import commands


class RegMiddleware:
    """
    Simple middleware which registers guilds in database and provides guild info
    """

    @staticmethod
    async def before_invoke(ctx: commands.Context):

        db = ctx.bot.database

        query = select(Guild).where(Guild.Id == ctx.guild.id)
        guild = (await db.execute(query, commit=False)).scalars().first()

        if not bool(guild):

            guild = await db.insert(
                Guild(Id=ctx.guild.id)
            )

        if not ctx.guild.id in config.data:

            config.data[ctx.guild.id] = VoiceClient(ctx.channel)

        ctx.guild_info: Guild = guild
        ctx.queue: dict = config.data.get(ctx.guild.id, VoiceClient(ctx.channel))
