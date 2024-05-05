import string
from venv import logger
import discord, os, random, requests
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
#El simbolo que deceas usar para diferenciar un comando.. en este caso es "!"
bot = commands.Bot(command_prefix= '!', intents=intents)

@bot.event
async def on_ready():
    print(f'Ha iniciado sesión como {bot.user}')

#Generadores de botones
class Simpleview(discord.ui.View):
    info : bool = False
    foo : bool = None
    #Deshabilita los botones al llamar a esta funcion
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
    #Funcion que determina un tiempo para deshabilitar los botones
    async def on_timeout(self) -> None:
        await self.message.channel.send("Tiempo Máximo")
        await self.disable_all_items()
    #Boton 1
    @discord.ui.button(label="Que sabes de la contaminacion?", #Nombre del boton
                       style= discord.ButtonStyle.success) #Tipo de boton (color)
    async def info(self,interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Uff... Se mucho 🤣\nPero primero.. visita esta sitio para saber más") # type: ignore/// Respuesta
        self.info = True

        self.foo = True
        self.stop()

    
    @discord.ui.button(label="Cancelar", #nombre del boton
                       style= discord.ButtonStyle.red) #Tipo del boton (Color)
    async def cancel(self,interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("No hay problema 😉👍") # type: ignore /// Respuesta
        self.foo = False
        self.stop()


#Ejecutado al poner comando "!hola"
@bot.command()
async def hola(ctx):
    await ctx.send("Hola 😉, Vengo a ayudarte... Puedo brindarte informacion de la contaminacion ambiental.\nPuedes consular aqui: ")
    view = Simpleview(timeout = 50) #Tiempo de espera para deshabilitar los botones
    message = await ctx.send(view=view)
    view.message = message
    await view.wait()
    await view.disable_all_items()

    if view.info is True:
        await ctx.send("https://es.wikipedia.org/wiki/Contaminaci%C3%B3n")
    #Esto solo se muestra en la Terminal de Visual /////////////////////////////
    if view.foo is None:
        logger.error("Tiempo de espera al límite")

    elif view.foo is True:
        logger.error("OK")
        
    else:
        logger.error("cancelando")
    #///////////////////////////////////////////////////////////////////////////
#Al entrar un mienbro al grupo:
@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')
#Muestra la lista de comandos establecidos
@bot.command()
async def comandos(ctx):
    list_comandos = "!hola\n" 
    await ctx.send("Esta es la lista de comandos:")
    await ctx.send(list_comandos)

bot.run("TOKEN") #Pon tu token!!!!!!!!!
