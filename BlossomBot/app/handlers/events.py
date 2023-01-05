import discord

from . import tasks
from app.database.models.guild import Guild

from discord.ext import commands
from sqlalchemy import delete


class EventHandlers(commands.Cog):
    """
    Cog for all common events
    """

    FIRST_RUN = False

    def __init__(self, bot: commands.Bot) -> None:

        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self) -> None:

        await self.bot.change_presence(activity=discord.Game(name='Try out button menu!'))

        if not self.FIRST_RUN: 

            await self.bot.tree.sync()
            await tasks.setup(self.bot)


    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:

        await self.bot.database.execute(
            delete(Guild).where(Guild.Id == guild.id)
        )
