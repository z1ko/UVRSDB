
from typing import List, Union
from discord.ext import commands
import discord


from discord.ext import commands, tasks
from itertools import cycle
import discord

from tags import TAGS_DEGREE, TAGS_SPECIAL, TAGS_YEAR


class Select(discord.ui.Select):
    def __init__(self, **kargv):
        super().__init__(**kargv)
        self.event_callback = []

    def add_callback(self, cb_function):
        self.event_callback.append(cb_function)

    # Aggiorna tag dell'utente che ha usato il dropdown
    async def callback(self, interaction):
        for cb in self.event_callback:
            cb(self, interaction)

class Button(discord.ui.View):
    def __init__(self, **kargv):
        super().__init__(**kargv)
        self.button_callback = []


    async def add_button(self, cb_function, **kargv):
        btn = discord.ui.button(**kargv).decorator(cb_function)
        self.button_callback.append(btn)
        self.stop()

    # Rappresenta un insieme di tag selezionabili
class TagDropdown(discord.ui.Select):
    def __init__(self, custom_id, placeholder, tags, max_values):
        self.id = custom_id
        self.tags = tags

        options = []
        for tag in tags:
            options.append(discord.SelectOption(
                value = tag.role_id, 
                label = tag.name,
                emoji = tag.emoji
            ))

        super().__init__(
            placeholder = placeholder, 
            max_values = max_values,
            min_values = 1,
            custom_id = custom_id,
            options = options
        )


    # Aggiorna tag dell'utente che ha usato il dropdown
    async def callback(self, interaction):
        user: discord.Member = interaction.user

        # Rimuovo tutte le tags relative a questo dropdown
        for tag in self.tags:
            tag_role = interaction.guild.get_role(int(tag.role_id))
            await user.remove_roles(tag_role)

        # Setta le tag corrette
        for role_id in self.values:
            target_role = interaction.guild.get_role(int(role_id))
            await user.add_roles(target_role)

        print(f'Aggiunti Tag corsi di studio per {user.nick}')

        # Informa l'utente
        #response = self.response(user, target_roles)
        #await interaction.response.send(response)


    # Messaggio customizzato inviato all'utente
    # quando questo cambia tag
    def response(self, user: discord.User, tag) -> str:
        raise NotImplementedError

# ================================================================================================

# Rappresenta una view dalla UI persistente per tag
class TagView(discord.ui.View):
    def __init__(self, items: List[TagDropdown]):
        super().__init__(timeout = None)
        
        for item in items:
            self.add_item(item)


# Cliccando sul bottone l'utente riceve una tag
class ButtonAcceptView(discord.ui.View):
    def __init__(self, role_id):
        self.role_id = role_id
        super().__init__()

    # Messaggio customizzato quando si accetta
    def response(self, user) -> str:
        raise NotImplementedError

    @discord.ui.button(label='Accetta')
    async def accept(self, button, interaction):
        user = interaction.user
        response = self.response(user)
        await interaction.response.send_message(response, ephemeral=True)

        role = interaction.guild.get_role(self.role_id)
        await user.add_roles(role)

        self.stop()



# ================================================================================================

# Dropdown per i corsi di studio
class DegreeDropdown(TagDropdown):
    def __init__(self):
        super().__init__(
            'dropdown:menu',
            'Scegli il corso di studi che stai seguendo',
            TAGS_DEGREE, len(TAGS_DEGREE)
        )

    def response(self, user, tag) -> str:
        return f'🎉 Ora segui il corso di {tag.name}!'


# Interfaccia per controllare l'aspetto del server in base ai corsi
class BasicInterfaceView(TagView):
    def __init__(self):
        super().__init__([DegreeDropdown()])

# ================================================================================================

# Dropdown per le tag secondarie/miste
class OtherDropdown(TagDropdown):
    def __init__(self):
        super().__init__(
            'dropdown:other',
            'Scegli altre tag secondarie per attività non legate allo studio',
            TAGS_SPECIAL, len(TAGS_SPECIAL)
        )

    def response(self, user, tag) -> str:
        return f'TODO'


# Interfaccia per le attività extra
class ExtraInterfaceView(TagView):
    def __init__(self):
        super().__init__([OtherDropdown()])

# ================================================================================================

# Promp per le regole
class RulesAcceptView(ButtonAcceptView):
    def __init__(self):
        super().__init__(874325424816144405)

    def response(self, user) -> str:
        return f'Grazie {user.nick}, ora sei una Matricola!'

