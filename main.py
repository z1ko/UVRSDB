from typing import Union, List, Dict, Optional, Any
import discord
from discord.embeds import Embed
from discord.errors import NotFound
from discord.ext import commands

from dotenv import dotenv_values
import json

from univr import BotUniVR, MyBot, CHANNEL_TYPE
from ui import BasicInterfaceView, ExtraInterfaceView, RulesAcceptView

app = MyBot()
bot = app.bot


def main():
    config = dotenv_values('configuration.env')
    bot.run(config['TOKEN'])


@bot.command()
@commands.is_owner()
async def corsi(ctx):
    # Embed per il primo menu sui corsi di studio
    view = BasicInterfaceView()
    title='Menu scelta Corsi di Studio'
    description="""
        Scegliendo il tuo corso di studio dal menu a tendina qui sotto potrai customizzare l'aspetto del server 
        visualizzando solo i canali inerenti al tuo percorso. 
        """
    url = 'https://upload.wikimedia.org/wikipedia/it/thumb/1/1e/Universit%C3%A0Verona.svg/1200px-Universit%C3%A0Verona.svg.png'
    await app.send_embed(ctx, view, title, description, url)

@bot.command()
@commands.is_owner()
async def extra(ctx):
    # Embed per il primo menu sui corsi di studio
    view = ExtraInterfaceView()
    title = 'Menu scelta attività extra'
    description = """
        Scegliendo le attività extra che vuoi seguire potrai customizzare l'aspetto del server
        """
    url = 'https://upload.wikimedia.org/wikipedia/it/thumb/1/1e/Universit%C3%A0Verona.svg/1200px-Universit%C3%A0Verona.svg.png'
    await app.send_embed(ctx, view, title, description, url)


@bot.command()
@commands.is_owner()
async def regole(ctx):
    view = RulesAcceptView()
    title='Regole del server UniVR Science'
    description="""
        Accettando dichiari di aver letto e di accettare le regole del server.
        Ogni abuso verrà punito.
    """
    url='https://upload.wikimedia.org/wikipedia/it/thumb/1/1e/Universit%C3%A0Verona.svg/1200px-Universit%C3%A0Verona.svg.png'

    await app.send_embed(ctx, view, title, description, url)
    await view.wait()

@bot.command()
@commands.is_owner()
async def create_channels(ctx):
    """
    Carica file di configurazione json e crea categorie, canali e ruoli
    TODO: Carica configurazione in un'altra funzione una volta sola
    """
    cat_loaded = 0
    json_data = app.load_configuration()
    for json_category in json_data['categories']:

        role_data = json_category['role']
        role_id = int(role_data['id_role'])
        role_name = role_data['name_role']
        role_color = role_data['color_role']

        category_data = json_category['category']
        category_id = int(category_data['id_category'])
        category_name = category_data['name_category']

        channels_list = json_category['channels']

        ## Role
        role = None
        if role_id != -1: # by id
            role = await app.fetch_role(ctx,role_id)
        else:             # by name
            role = await app.find_role(ctx,role_name)
        if role is None:  # create
            role = await app.create_role(ctx, role_name, role_color=role_color)
        role_data['id_role'] = role.id

        ## Category
        category = None
        if category_id != -1:  # by id
            category = await app.fetch_channel(ctx, category_id)
        else:  # by name
            category = await app.find_channel(ctx, category_name, kind='GUILD_CATEGORY')
        if category is None:  # create
            category = await app.create_category(ctx, category_name)
        category_data['id_category'] = category.id

        ## Permissions ( category <-> role )
        if not await app.private_channel(ctx, category, role):
            return False


        ## Channel(s)
        for channel_data in channels_list:
            channel_id = channel_data["id_channel"]
            channel_name = channel_data["name_channel"]

            channel = None
            if channel_id != -1:  # by id
                channel = await app.fetch_channel(ctx, channel_id)
            else:  # by name
                channel = await app.find_channel(ctx, channel_name, kind='GUILD_TEXT')
            if channel is None:  # create
                channel = await app.create_channel(ctx, channel_name, category=category)
            else:
                await channel.edit(category=category)

            channel_data["id_channel"] = channel.id

        cat_loaded += 1

    app.save_configuration(json_data)


@bot.command()
@commands.is_owner()
async def get_categories(ctx, *except_ids):
    """
    Elimina categoria e tutti i canali contenuti
    """
    ids = []
    for channel in ctx.guild.channels:
        if channel.type.name == "category": # or .value == 4
            id_str = str(channel.id)
            if id_str in except_ids: continue
            ids.append(id_str)

    await app.send(ctx, " ".join(ids))


@bot.command()
@commands.is_owner()
async def delete_category(ctx, *category_ids):
    """
    Elimina categoria e tutti i canali contenuti
    """
    for category_id in category_ids:
        await app.delete_category(ctx, category_id)



if __name__ == '__main__':
    main()
