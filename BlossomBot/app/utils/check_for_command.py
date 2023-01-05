from discord.ext.commands import Context


async def answer_or_react(ctx: Context, text: str, emoji: str) -> None:
    """
    Answers or reacts to the message
    Seeking for better implementation
    """

    try:

        await ctx.message.add_reaction(emoji)

    except:

        await ctx.reply(text)
