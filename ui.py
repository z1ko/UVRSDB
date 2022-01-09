
from typing import List, Union
from discord.ext import commands
import discord


from discord.ext import commands, tasks
from itertools import cycle
import discord

from tags import TAGS_DEGREE, TAGS_DEGREE_T, TAGS_DEGREE_M, TAGS_SPECIAL, TAGS_YEAR


class Select(discord.ui.Select):
    def __init__(self, **kargv):
        super().__init__(**kargv)
        self.event_callback = []

    def add_callback(self, ctx, cb_function):
        self.event_callback.append([ctx, cb_function])

    # Aggiorna tag dell'utente che ha usato il dropdown
    async def callback(self, event):
        for ctx, cb_function in self.event_callback:
            await cb_function(ctx, self, event)

class Button(discord.ui.View):
    def __init__(self, **kargv):
        super().__init__(**kargv)
        self.button_callback = []


    async def add_button(self, cb_function, **kargv):
        btn = discord.ui.button(**kargv)(cb_function)
        self.button_callback.append(btn)
        self.stop()

# ================================================================================================

    # Rappresenta un insieme di tag selezionabili
class TagDropdown(discord.ui.Select):
    def __init__(self, custom_id, placeholder, tags, max_values):
        self.id = custom_id
        self.tags = tags

        options = []
        for tag in tags:
            options.append(discord.SelectOption(
                value=str(tag.role_id),
                label=str(tag.name),
                emoji=tag.emoji
            ))

        options.append(discord.SelectOption(value="-1", label="none"))

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
        print(user)
        print(self.values)

        role_ids_all = [int(tag.role_id) for tag in self.tags]
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

        #response = self.response(user, target_roles)
        await interaction.response.send_message("ok!", ephemeral=True)


        """
        # Rimuovo tutte le tags relative a questo dropdown
        role_ids = [int(tag.role_id) for tag in self.tags]
        roles = list(filter(lambda role: role.id in role_ids, interaction.guild.roles))

        await user.remove_roles(*roles)

        role_ids = [int(role_id) for role_id in self.values]
        roles = list(filter(lambda role: role.id in role_ids, interaction.guild.roles))
        await user.add_roles(*roles)
        """

        """
        # Setta le tag corrette

        for tag in self.tags:
            if tag.role_id == "-1": continue
            tag_role = interaction.guild.get_role(int(tag.role_id))
            if tag_role is None: continue
            print(f'Removing role {tag_role}')
            await user.remove_roles(roles)
        """

        """
        # Setta le tag corrette

        for role_id in self.values:
            if role_id == "-1": continue
            target_role = interaction.guild.get_role(int(role_id))
            if target_role is None: continue
            print(f'Adding role {target_role}')
            await user.add_roles(target_role)
        """
        #print(f'Aggiunti Tag corsi di studio per {user.nick}')

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

# Dropdown per i corsi di studio
class DegreeDropdownT(TagDropdown):
    def __init__(self):
        super().__init__(
            'dropdown:menu_t',
            'Scegli il corso di studi che stai seguendo',
            TAGS_DEGREE_T, len(TAGS_DEGREE_T)
        )

    def response(self, user, tag) -> str:
        return f'🎉 Ora segui il corso di {tag.name}!'

# Dropdown per i corsi di studio
class DegreeDropdownM(TagDropdown):
    def __init__(self):
        super().__init__(
            'dropdown:menu_m',
            'Scegli il corso di studi che stai seguendo',
            TAGS_DEGREE_M, len(TAGS_DEGREE_M)
        )

    def response(self, user, tag) -> str:
        return f'🎉 Ora segui il corso di {tag.name}!'


# Interfaccia per controllare l'aspetto del server in base ai corsi
class BasicInterfaceView(TagView):
    def __init__(self):
        super().__init__([DegreeDropdown()])

# Interfaccia per controllare l'aspetto del server in base ai corsi
class BasicInterfaceViewT(TagView):
    def __init__(self):
        super().__init__([DegreeDropdownT()])

# Interfaccia per controllare l'aspetto del server in base ai corsi
class BasicInterfaceViewM(TagView):
    def __init__(self):
        super().__init__([DegreeDropdownM()])

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

