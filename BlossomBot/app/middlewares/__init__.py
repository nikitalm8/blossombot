from .registration import RegMiddleware

from discord.ext import commands


async def setup(bot: commands.Bot) -> None:

    bot.before_invoke(RegMiddleware.before_invoke)
