import config

from app.database.models.guild import Guild

from sqlalchemy import select
from discord.ext import commands


async def prefix_middleware(database, client: commands.Bot, ctx: commands.Context):

    return '!'