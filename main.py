import math
import random
from typing import Union, List, Dict, Optional, Any
import discord
import discord.ui
from discord.embeds import Embed
from discord.errors import NotFound
from discord.ext import commands
from discord.utils import get

from dotenv import dotenv_values

from univr import BotUniVR, MyBot
from ui import Select, Button, BasicInterfaceView,BasicInterfaceViewT,BasicInterfaceViewM, ExtraInterfaceView, RulesAcceptView

app = MyBot()
bot = app.bot


def main():
    config = dotenv_values('configuration.env')
    bot.run(config['TOKEN'])

@bot.command()
@commands.has_permissions(administrator=True)
async def get_config(ctx):
    file = discord.File("configuration.json")  # an image in the same folder as the main bot file
    embed = discord.Embed()  # any kwargs you want here
    await ctx.send(file=file)

@bot.command()
@commands.has_permissions(administrator=True)
async def test0(ctx):
    cats = app.get_categories(triennali=True, magistrali=True)
    view = discord.ui.View()
    """ add_button
    label: Optional[str] = None,
    custom_id: Optional[str] = None,
    disabled: bool = False,
    style: ButtonStyle = ButtonStyle.secondary,
    emoji: Optional[Union[str, Emoji, PartialEmoji]] = None,
    row: Optional[int] = None,
    """

    for cat in cats:
        cat_data = cat["category"]
        btn_view = Button()
        await btn_view.add_button(toggle_tag, label=cat_data["name_category"], custom_id=cat_data["id_category"])
        view.add_item(btn_view)
    title = "Selezione corsi"
    description = """
        Scegliendo il tuo corso di studio dal menu a tendina qui sotto potrai customizzare l'aspetto del server 
        visualizzando solo i canali inerenti al tuo percorso. 
    """
    url = 'https://upload.wikimedia.org/wikipedia/it/thumb/1/1e/Universit%C3%A0Verona.svg/1200px-Universit%C3%A0Verona.svg.png'
    await app.send_embed(ctx, view, title, description, url)


@bot.command()
@commands.has_permissions(administrator=True)
async def test1(ctx):
    catss = {
        "Triennali": app.get_categories(triennali=True, magistrali=False),
        "Magistrali": app.get_categories(triennali=False, magistrali=True)
    }
    view = discord.ui.View()

    title = "Selezione corsi"
    description = """
        Scegliendo il tuo corso di studio dal menu a tendina qui sotto potrai customizzare l'aspetto del server 
        visualizzando solo i canali inerenti al tuo percorso. 
    """
    url = 'https://upload.wikimedia.org/wikipedia/it/thumb/1/1e/Universit%C3%A0Verona.svg/1200px-Universit%C3%A0Verona.svg.png'
    await app.send_embed(ctx, view, title, description, url)

    for name, cats in catss.items():
        view = discord.ui.View()
        title = name
        subgroups = set([cat['category']['subgroup_category'] for cat in cats])
        subgroups = list(sorted(subgroups))
        subgroups_cnt = len(subgroups)
        max_cnt = 5  # hard limit on discord
        cnt = 0
        limit_cnt = max_cnt if subgroups_cnt <= max_cnt else math.ceil(subgroups_cnt / 2)

        sub_stack = []
        view = discord.ui.View()

        for subgroup in subgroups:
            sub_cats = list(filter(lambda cat: cat['category']['subgroup_category'] == subgroup, cats))
            options_tags = app.get_role_options(sub_cats)
            print(f"dropdown:{name}_{subgroup}")

            dropdown_select = Select(custom_id=f"select:{subgroup}_{name}", placeholder=subgroup,
                                     max_values=len(options_tags), min_values = 1)
            dropdown_select.add_callback(ctx, toggle_tag)

            for option in options_tags:
                dropdown_select.append_option(option)

            cnt += 1
            view.add_item(dropdown_select)
            sub_stack.append(subgroup)

            if cnt >= limit_cnt:
                print(f"---- FLUSH ----")
                await app.send_embed(ctx, view=view, title=title, description=", ".join(sub_stack))
                view = discord.ui.View()
                cnt = 0
                sub_stack = []
                title = ""

        if cnt > 0:
            print(f"---- FLUSH ----")
            await app.send_embed(ctx, view=view, title=title, description=", ".join(sub_stack))
            view = discord.ui.View()

async def toggle_tag(ctx: discord.ext.commands.Context, itm: Select, interaction: discord.interactions.Interaction):

    # print(itm, interaction)
    user = interaction.user
    role_ids_all = [option.value for option in itm.options]
    role_ids_user = [role.id for role in user.roles]

    role_ids_selected = [int(role_id) for role_id in interaction.data['values']]
    role_ids_selected = list(filter(lambda role_id: role_id in role_ids_all, role_ids_selected))

    role_ids_off = list(filter(lambda role_id: role_id not in role_ids_selected, role_ids_all))
    role_ids_off = list(filter(lambda role_id: role_id in role_ids_user, role_ids_off))


    role_ids_on = list(filter(lambda role_id: role_id not in role_ids_user, role_ids_selected))

    # print("role_ids_selected",role_ids_selected)
    # print("role_ids_user",role_ids_user)
    # print("role_ids_all",role_ids_all)
    # print("role_ids_on",role_ids_on)
    # print("role_ids_off",role_ids_off)

    roles_off = list(filter(lambda role: role.id in role_ids_off, interaction.guild.roles))
    roles_on = list(filter(lambda role: role.id in role_ids_on, interaction.guild.roles))

    await user.remove_roles(*roles_off)
    await user.add_roles(*roles_on)

"""
    for role_off in roles_off:
        await user.remove_roles(role_off)

    for role_on in roles_on:
        await user.add_roles(role_on)
"""

@bot.command()
@commands.has_permissions(administrator=True)
async def corsi(ctx):
    cat_triennali = app.get_categories(triennali=True, magistrali=False)
    cat_magistrali = app.get_categories(triennali=False, magistrali=True)

    # emoji_t = [cat['role']['emoji_role'] for cat in cat_triennali]
    # emoji_m = [cat['role']['emoji_role'] for cat in cat_magistrali]
    # await app.send(ctx, " ".join(emoji_t) )
    # await app.send(ctx, " ".join(emoji_m))
    role_ids_user = [] # [role.id for role in ctx.author.roles] # activate for ephemerial messages

    options_tags_t = app.get_role_options(cat_triennali,  role_ids_user)
    options_tags_m = app.get_role_options(cat_magistrali, role_ids_user)

    dropdown_select_t = Select(custom_id="select_triennali", placeholder="Seleziona corsi: Triennali", max_values=len(options_tags_t))
    dropdown_select_m = Select(custom_id="select_magistrali", placeholder="Seleziona corsi: Magistrali", max_values=len(options_tags_m))

    dropdown_select_t.add_callback(ctx, toggle_tag)
    dropdown_select_m.add_callback(ctx, toggle_tag)

    for option in options_tags_t:
        dropdown_select_t.append_option(option)

    for option in options_tags_m:
        dropdown_select_m.append_option(option)

    view = discord.ui.View()
    view.add_item(dropdown_select_t)
    view.add_item(dropdown_select_m)

    title = 'Menu scelta Corsi di Studio'
    description = """
        Scegliendo il tuo corso di studio dal menu a tendina qui sotto potrai customizzare l'aspetto del server 
        visualizzando solo i canali inerenti al tuo percorso. 
        """
    url = 'https://upload.wikimedia.org/wikipedia/it/thumb/1/1e/Universit%C3%A0Verona.svg/1200px-Universit%C3%A0Verona.svg.png'
    await app.send_embed(ctx, view, title, description, url)

@bot.command()
@commands.has_permissions(administrator=True)
async def corsi_old(ctx):
    # Embed per il primo menu sui corsi di studio
    view = BasicInterfaceView()
    title = 'Menu scelta Corsi di Studio'
    description = """
        Scegliendo il tuo corso di studio dal menu a tendina qui sotto potrai customizzare l'aspetto del server 
        visualizzando solo i canali inerenti al tuo percorso. 
        """
    url = 'https://upload.wikimedia.org/wikipedia/it/thumb/1/1e/Universit%C3%A0Verona.svg/1200px-Universit%C3%A0Verona.svg.png'
    await app.send_embed(ctx, view, title, description, url)

@bot.command()
@commands.has_permissions(administrator=True)
async def corsi_msg(ctx):
    # Embed per il primo menu sui corsi di studio
    view = discord.ui.View()
    title = 'Menu scelta Corsi di Studio'
    description = """
        Scegliendo il tuo corso di studio dal menu a tendina qui sotto potrai customizzare l'aspetto del server 
        visualizzando solo i canali di tuoi interesse.  
        """
    url = 'https://upload.wikimedia.org/wikipedia/it/thumb/1/1e/Universit%C3%A0Verona.svg/1200px-Universit%C3%A0Verona.svg.png'
    await app.send_embed(ctx, view, title, description, url)

@bot.command()
@commands.has_permissions(administrator=True)
async def corsi_t(ctx):
    # Embed per il primo menu sui corsi di studio
    view = BasicInterfaceViewT()
    title = 'Triennali                                        '
    await app.send_embed(ctx, view, title)

@bot.command()
@commands.has_permissions(administrator=True)
async def corsi_m(ctx):
    # Embed per il primo menu sui corsi di studio
    view = BasicInterfaceViewM()
    title = 'Magisatrali                                      '
    await app.send_embed(ctx, view, title)


@bot.command()
@commands.has_permissions(administrator=True)
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
@commands.has_permissions(administrator=True)
async def regole(ctx):
    view = RulesAcceptView()
    title = 'Regole del server UniVR Science'
    description = """
        Accettando dichiari di aver letto e di accettare le regole del server.
        Ogni abuso verrà punito.
    """
    url = 'https://upload.wikimedia.org/wikipedia/it/thumb/1/1e/Universit%C3%A0Verona.svg/1200px-Universit%C3%A0Verona.svg.png'

    await app.send_embed(ctx, view, title, description, url)
    await view.wait()


@bot.command()
@commands.has_permissions(administrator=True)
async def create_channels(ctx):
    """
    Carica file di configurazione json e crea categorie, canali e ruoli
    TODO: Carica configurazione in un'altra funzione una volta sola
    """

    cat_loaded = 0
    json_data = app.load_configuration()
    num_cats = len(json_data['categories'])
    for json_category in json_data['categories']:

        role_data = json_category['role']
        role_id = int(role_data['id_role'])
        role_name = role_data['name_role']
        role_color = role_data['color_role']

        category_data = json_category['category']
        category_id = int(category_data['id_category'])
        category_name = category_data['name_category']

        channels_list = json_category['channels']

        print(f"[{cat_loaded}/{num_cats}] {category_name}")
        ## Role
        role = None
        if role_id != -1: # by id
            role = await app.fetch_role(ctx, role_id)
        if role is None:  # by name
            role = await app.find_role(ctx, role_name)
        if role is None:  # create
            role = await app.create_role(ctx, role_name, role_color=role_color)
        role_data['id_role'] = role.id

        ## Category
        category = None
        if category_id != -1: # by id
            category = await app.fetch_channel(ctx, category_id)
        if category is None:  # by name
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
            if channel_id != -1: # by id
                channel = await app.fetch_channel(ctx, channel_id)
            if channel is None:  # by name
                channel = await app.find_channel(ctx, channel_name, kind='GUILD_TEXT')
            if channel is None:  # create
                channel = await app.create_channel(ctx, channel_name, category=category)
            else:
                await channel.edit(category=category)

            channel_data["id_channel"] = channel.id

        cat_loaded += 1

    app.save_configuration(json_data)


@bot.command()
@commands.has_permissions(administrator=True)
async def get_categories(ctx, *except_ids):
    """
    ritorna gli id di tutte le categorie
    """
    ids = []
    for channel in ctx.guild.channels:
        if channel.type.name == "category":  # or .value == 4
            id_str = str(channel.id)
            if id_str in except_ids: continue
            ids.append(id_str)

    await app.send(ctx, " ".join(ids))


@bot.command()
@commands.has_permissions(administrator=True)
async def get_roles(ctx, *except_ids):
    """
    ritorna gli id di tutti i ruoli
    """
    ids = []
    for role in ctx.guild.roles:
        id_str = str(role.id)
        if id_str in except_ids: continue
        ids.append(id_str)

    await app.send(ctx, " ".join(ids))


@bot.command()
@commands.has_permissions(administrator=True)
async def delete_category(ctx, *category_ids):
    """
    Elimina categoria e tutti i canali contenuti, supporta id multipli.
    """
    for category_id in category_ids:
        await app.delete_category(ctx, category_id)


@bot.command()
@commands.has_permissions(administrator=True)
async def delete_role(ctx, *role_ids):
    """
    Elimina una serie di ruoli, data una lista di id.
    """
    for role_id in role_ids:
        await app.delete_role(ctx, role_id)



if __name__ == '__main__':
    main()
