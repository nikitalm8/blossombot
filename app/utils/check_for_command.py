from discord.ext.commands import Context


async def answer_or_react(ctx: Context, text: str, emoji: str) -> None:

    try:

        await ctx.message.add_reaction(emoji)

    except:

        await ctx.reply(text)
