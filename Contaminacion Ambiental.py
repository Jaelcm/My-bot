import string
from venv import logger
import discord, os, random, requests
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix= '!', intents=intents)

@bot.event
async def on_ready():
    print(f'Ha iniciado sesión como {bot.user}')


class Simpleview(discord.ui.View):
    info : bool = False
    foo : bool = None

    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        await self.message.channel.send("Tiempo Máximo")
        await self.disable_all_items()

    @discord.ui.button(label="Que sabes de la contaminacion?",
                       style= discord.ButtonStyle.success)
    async def info(self,interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Uff... Se mucho 🤣\nPero primero.. visita esta sitio para saber más") # type: ignore
        self.info = True

        self.foo = True
        self.stop()

    
    @discord.ui.button(label="Cancelar",
                       style= discord.ButtonStyle.red)
    async def cancel(self,interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("No hay problema 😉👍") # type: ignore
        self.foo = False
        self.stop()



@bot.command()
async def hola(ctx):
    await ctx.send("Hola 😉, Vengo a ayudarte... Puedo brindarte informacion de la contaminacion ambiental.\nPuedes consular aqui: ")
    view = Simpleview(timeout = 50)
    message = await ctx.send(view=view)
    view.message = message
    await view.wait()
    await view.disable_all_items()

    if view.info is True:
        await ctx.send("https://es.wikipedia.org/wiki/Contaminaci%C3%B3n")

    if view.foo is None:
        logger.error("Tiempo de espera al límite")

    elif view.foo is True:
        logger.error("OK")
        
    else:
        logger.error("cancelando")

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def comandos(ctx):
    list_comandos = "!hola\n"
    await ctx.send("Esta es la lista de comandos:")
    await ctx.send(list_comandos)

bot.run("TOKEN")
