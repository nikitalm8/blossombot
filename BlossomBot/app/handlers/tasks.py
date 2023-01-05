import config
import discord

from app.templates import play as texts
from app.utils.ytdl import get_source
from app.database.models.guild import Guild

from discord import PartialEmoji
from discord.ext import commands, tasks
from discord.ui import (
    View, 
    Button, 
    button
)
from discord.ui.button import ButtonStyle
from sqlalchemy import select


class PlayerView(View):

    def __init__(self, voice_client) -> None:

        super().__init__(timeout=None)
        self.voice_client = voice_client

        data = config.data[self.voice_client.guild.id]
        loop = data.loop
        single = data.singleloop

        if single: emoji = '<:blackescape:1060166452310716416>'
        elif loop: emoji = '<:blackrepeatsingle:1060166184139509891>'
        else: emoji = '<:blackrepeat:1060166186010165278>'

        self.loop.emoji = emoji


    @button(label='', style=ButtonStyle.blurple)
    async def loop(self, interaction: discord.Interaction, button: Button) -> None:

        data = config.data[self.voice_client.guild.id]
        loop = data.loop
        single = data.singleloop

        if single: 
            
            emoji = '<:blackrepeat:1060166186010165278>'
            config.data[self.voice_client.guild.id].loop = False
            config.data[self.voice_client.guild.id].singleloop = False

        elif loop: 
            
            emoji = '<:blackescape:1060166452310716416>'
            config.data[self.voice_client.guild.id].loop = False
            config.data[self.voice_client.guild.id].singleloop = True
  
        else: 
            
            emoji = '<:blackrepeatsingle:1060166184139509891>'
            config.data[self.voice_client.guild.id].loop = True

        self.loop.emoji = emoji
        await interaction.response.edit_message(view=self)


    @button(label='', emoji='<:blackpause:1060166187872419850>', style=ButtonStyle.blurple)
    async def pause(self, interaction: discord.Interaction, button: Button) -> None:
            
        if self.voice_client.is_paused():

            self.voice_client.resume()
            self.pause.emoji = '<:blackpause:1060166187872419850>'

        else:

            self.voice_client.pause()
            self.pause.emoji = '<:blackplay:1060168321091260420>' 

        await interaction.response.edit_message(view=self)


    @button(label='', emoji='<:blackskip:1060166189680181259>', style=ButtonStyle.blurple)
    async def skip(self, interaction: discord.Interaction, button: Button) -> None:
            
        self.voice_client.stop()
        await interaction.response.edit_message(
            content='Skipped', view=None
        )

    
    @button(label='', emoji='<:blackshuffle:1060166181413199924>', style=ButtonStyle.blurple)
    async def shuffle(self, interaction: discord.Interaction, button: Button) -> None:
            
        config.data[self.voice_client.guild.id].shuffle()


class TaskHandlers(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot


    @tasks.loop(seconds=0.5)
    async def player(self):
    
        for client in self.bot.voice_clients:
            
            try:

                paused = client.is_paused()

                if not client.is_playing() and not paused and client.guild.id in config.data: 

                    data = config.data[client.guild.id]
                    song = data.next()

                    if not song and not data.suppress:

                        guild = (await self.bot.database.execute(
                            select(Guild).where(Guild.Id == client.guild.id)
                        )).scalars().first()

                        await data.channel.send(texts.endqueue[guild.Language])
                        del config.data[client.guild.id]
                        return

                    elif not song:

                        return

                    async with data.channel.typing():
                            
                        player = await get_source(song.url, stream=True)
                        client.play(player)

                    guild = (await self.bot.database.execute(
                        select(Guild).where(Guild.Id == client.guild.id)
                    )).scalars().first()


                    channel = await self.bot.fetch_channel(data.channel.id)

                    if channel.last_message_id == data.message_id:

                        msg = await channel.fetch_message(data.message_id)
                        await msg.edit(
                            content=texts.nowplaying[guild.Language] % song.title,
                            view=PlayerView(client),
                        )

                    else:

                        msg = await data.channel.send(
                            texts.nowplaying[guild.Language] % song.title, 
                            view=PlayerView(client),
                        )
                        data.message_id = msg.id

                    data.suppress = False

            except Exception as e:
            
                print(e)
                continue


    @tasks.loop(seconds=10)
    async def afk(self):

        for client in self.bot.voice_clients:

            try:

                if client.channel.members == [client.guild.me]:
                    
                    await client.disconnect()
                    del config.data[client.guild.id]

                elif client.is_paused() or not client.is_playing():

                    if config.data[client.guild.id].checkafk():

                        del config.data[client.guild.id]
                        await client.disconnect()

            except Exception as e:

                print(e)
                continue


async def setup(client: commands.Bot):

    tasks = TaskHandlers(client)
    await client.add_cog(tasks)

    tasks.player.start()
    tasks.afk.start()
