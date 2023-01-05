from .queues import QueueHandlers
from .events import EventHandlers
from .play import PlayerHandlers
from .commands import CommonHandler

from discord.ext import commands


async def setup(bot: commands.Bot) -> None:

    cogs = [
        QueueHandlers,
        PlayerHandlers,
        CommonHandler,
        EventHandlers,
    ]

    for cog in cogs:

        await bot.add_cog(cog(bot))
