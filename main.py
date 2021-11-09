
from discord.embeds import Embed
from discord.ext import commands

from univr import BasicInterfaceView, BotUniVR, ExtraInterfaceView, RulesAcceptView

bot = BotUniVR()

@bot.command()
@commands.is_owner()
async def corsi(ctx):

    # Embed per il primo menu sui corsi di studio
    embed_degrees = Embed( 
        title = 'Menu scelta Corsi di Studio',
        description = """\
        Scegliendo il tuo corso di studio dal menu a tendina qui sotto potrai customizzare l'aspetto del server \
        visualizzando solo i canali inerenti al tuo percorso. \
        """
    )
    embed_degrees.set_thumbnail(url = 'https://upload.wikimedia.org/wikipedia/it/thumb/1/1e/Universit%C3%A0Verona.svg/1200px-Universit%C3%A0Verona.svg.png')
    await ctx.send(view = BasicInterfaceView(), embed = embed_degrees)

@bot.command()
@commands.is_owner()
async def extra(ctx):

    # Embed per le tag extra
    embed_degrees = Embed( 
        title = 'Menu scelta attività extra',
        description = """\
        Scegliendo le attività extra che vuoi seguire potrai customizzare l'aspetto del server \
        """
    )
    embed_degrees.set_thumbnail(url = 'https://upload.wikimedia.org/wikipedia/it/thumb/1/1e/Universit%C3%A0Verona.svg/1200px-Universit%C3%A0Verona.svg.png')
    await ctx.send(view = ExtraInterfaceView(), embed = embed_degrees)


@bot.command()
@commands.is_owner()
async def regole(ctx):

    # Embed per le regole
    embed_degrees = Embed( 
        title = 'Regole del server UniVR Science',
        description = """\
        Accettando dichiari di aver letto e di accettare le regole del server. \
        Ogni abuso verrà punito. \
        """
    )

    embed_degrees.set_thumbnail(url = 'https://upload.wikimedia.org/wikipedia/it/thumb/1/1e/Universit%C3%A0Verona.svg/1200px-Universit%C3%A0Verona.svg.png')
    accept_view = RulesAcceptView()
    
    await ctx.send(view = accept_view, embed = embed_degrees)
    await accept_view.wait()


bot.run('OTA3MzEzNjM4NTYwMzgyOTc2.YYlXrA.kfq7btPVrTYBaBzvN73HONcomGY')