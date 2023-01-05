import config
import discord
import asyncio

from app import (
    handlers,
    middlewares,
    database,
)
from app.database.models.guild import Guild

from discord.ext import commands
from sqlalchemy import select


async def setup(client: commands.Bot) -> None:

    client.database = await database.create_instance(config.DATABASE_URL)

    await middlewares.setup(client)
    await handlers.setup(client)


async def prefix(bot: commands.Bot, message: discord.Message) -> str:

    if not message.guild:

        return config.PREFIX

    query = select(Guild).where(Guild.Id == message.guild.id)
    guild = (await bot.database.execute(query, commit=False)).scalars().first()

    return guild.Prefix if guild else config.PREFIX


def main() -> None:

    client = commands.Bot(
        command_prefix=prefix, 
        intents=discord.Intents.all(),
        case_insensitive=True, 
        help_command=None,
    )
    
    asyncio.run(setup(client))
    client.run(config.BOT_TOKEN)


if __name__ == '__main__':

    try:

        main()

    except (
        KeyboardInterrupt,
        SystemExit,
    ):

        exit(0)
