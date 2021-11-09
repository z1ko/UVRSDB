
import discord


# Cliccando sul bottone l'utente riceve una tag
class ButtonAcceptView(discord.ui.View):
    def __init__(self, role_id):
        self.role_id = role_id
        super().__init__()

    #Messaggio customizzato quando si accetta
    def response(self, user) -> str:
        raise NotImplementedError

    @discord.ui.button(label='Accetta')
    async def accept(self, button, interaction):
        
        user = interaction.user
        response = self.response(user)
        await interaction.response.send_message(response, ephemeral = True)

        role = interaction.guild.get_role(self.role_id)
        await user.add_roles(role)

        self.stop()