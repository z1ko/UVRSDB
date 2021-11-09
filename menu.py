
from typing import List, Union
from discord.ext import commands
import discord

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
