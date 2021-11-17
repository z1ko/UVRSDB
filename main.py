
from discord.embeds import Embed
from discord.errors import NotFound
from discord.ext import commands
import discord

from dotenv import dotenv_values
import json

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


#Configurazione del BOT
JSON_CONFIG = { }

@bot.command()
@commands.is_owner()
async def load_configuration():
    with open('configuration.json', 'r') as f:
        print('Caricamento configurazione...')
        JSON_CONFIG = json.load(f)


# Crea nuova categoria
async def create_custom_category(guild, json_category):
    category_name = json_category['name']

    try:
        # Crea nuovo ruolo associato alla categoria
        print(f'Creazione nuovo ruolo per la categoria "{category_name}"...')
        role = await guild.create_role(name = category_name)
        json_category['id_role'] = str(role.id)

    except discord.HTTPException as e:
        print('Errore creazione nuovo ruolo: ' + e.text)
        return 0

    overwrites = {
        # TODO
    }

    try:
        # Permetti al solo nuovo ruolo di visualizzare la categoria
        print(f'Creazione nuova categoria "{category_name}"...')
        category = await guild.create_category_channel(category_name, overwrites = overwrites)
        json_category['id_cat'] = str(category.id)

    except discord.HTTPException as e:
        print('Errore creazione nuova categoria:' + e.text)
        return 0

    # Crea i canali testuali della categoria
    for json_channel in json_category['channels']:
        channel_name = json_channel['name']

        try:
            print(f'Creazione nuovo canale testuale "{channel_name}" per la categoria {category_name}...')
            channel = await category.create_text_channel(name = channel_name)
            json_channel['id_channel'] = str(channel.id)

        except discord.HTTPException as e:
            print('Errore creazione nuovo canale testuale:' + e.text)
            return 0

    return 1


@bot.command()
@commands.is_owner()
async def create_channels(ctx):
    """
    Carica file di configurazione json e crea categorie, canali e ruoli
    TODO: Carica configurazione in un'altra funzione una volta sola
    """

    # Carica file configurazione
    with open('configuration.json', 'r') as f:
        print('Caricamento configurazione...')
        json_data = json.load(f)

    guild = ctx.guild
    for json_category in json_data['categories']:
            
        category_id   = int(json_category['id_cat'])
        category_name = json_category['name']

        if category_id == -1:
            await create_custom_category(guild, json_category)
        else:
            try:
                # Controlla se esiste già, in tal caso skippa
                print(f'Controllo se la categoria "{category_name}" esiste già...')
                category = await guild.fetch_channel(int(json_category['id_cat']))
                print('Categoria già esistente: skippo')
                continue

            # Crea nuova categoria
            except discord.NotFound:
                await create_custom_category(guild, json_category)
                continue
                    
            except discord.HTTPException as e:
                print('Errore controllo esistenza nuova categoria:' + e.text)
                continue

    # Salva modifiche al file
    with open('configuration.json', 'w') as f:
        print('Salvataggio nuova configurazione...')
        json.dump(json_data, f, indent = 4)


@bot.command()
@commands.is_owner()
async def delete_category(ctx, category_id: int):
    """
    Elimina categoria e tutti i canali contenuti
    """

    try:
        print(f'Ottenimento categoria con ID {category_id}...')
        category = await ctx.guild.fetch_channel(category_id)
        for channel in category.text_channels:
            try:
                print(f'Rimozione canale testuale {str(channel)}...')
                await channel.delete()

            except discord.HTTPException as e:
                print('Errore rimozione canale testuale: ' + e.text)
                continue
        try:
            print('Rimozione categoria...')
            await category.delete()

        except discord.HTTPException as e:
            print('Errore rimozione categoria: ' + e.text)


    except discord.HTTPException as e:
        print('Errore ottenimento  categoria: ' + e.text)

    except discord.NotFound as e:
        print('Categoria non trovata: ' + e.text)



config = dotenv_values('configuration.env')
bot.run(config['TOKEN'])
