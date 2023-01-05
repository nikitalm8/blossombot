import discord

from app.templates import play as texts
from app.database.models.guild import Guild

from discord.ext import commands
from discord.ui import (
    Button,
    View,
    button,
)
from discord.ui.button import ButtonStyle
from sqlalchemy import update


class LanguageSelector(View):


    def __init__(self, bot: commands.Bot) -> None:
        
        self.bot = bot
        super().__init__(timeout=None)


    @button(label=f"{'English': ^27}", style=ButtonStyle.blurple)
    async def english(self, interaction: discord.Interaction, button: Button) -> None:

        await interaction.response.edit_message(
            content='**English selected**', view=None,
        )
        self.stop()
        
        await self.bot.database.execute(
            update(Guild).where(Guild.Id == interaction.guild.id).values(
                Language=0,
            ),
        )

    @button(label=f"{'Русский': ^27}", style=ButtonStyle.red)
    async def russian(self, interaction: discord.Interaction, button: Button) -> None:

        await interaction.response.edit_message(
            content='**Выбран Русский**', view=None,
        )
        self.stop()
        self.remove_item(self.english)

        await self.bot.database.execute(
            update(Guild).where(Guild.Id == interaction.guild.id).values(
                Language=1,
            ),
        )

class CommonHandler(commands.Cog):


    def __init__(self, bot: commands.Bot) -> None:

        self.bot = bot


    @commands.hybrid_command(description='Shows the language selector')
    async def lang(self, ctx: commands.Context) -> str:

        await ctx.send(
            '**Select language | Выберите язык**',
            view=LanguageSelector(ctx.bot),
        )


    @commands.hybrid_command(description='Changes the prefix')
    async def prefix(self, ctx: commands.Context, *, prefix: str) -> None:

        await ctx.send(
            texts.prefix[ctx.guild_info.Language] % prefix,
        )
        await self.bot.database.execute(
            update(Guild).where(Guild.Id == ctx.guild.id).values(
                Prefix=prefix,
            ),
        )


    @commands.hybrid_command(description='Shows the help message')
    async def help(self, ctx: commands.Context) -> None:
            
        await ctx.send(
            'Help message',
            
        )
