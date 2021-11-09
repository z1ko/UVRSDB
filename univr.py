
from discord.ext import commands, tasks
from itertools import cycle
import discord

from menu  import TagDropdown, TagView
from rules import ButtonAcceptView
from tags  import TAGS_DEGREE, TAGS_SPECIAL, TAGS_YEAR

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


# ================================================================================================

# Possibili stati divertenti del bot
STATUSES = cycle([

    'Risolvendo le dipendenze circolari della segreteria 🔁',
    'Facendo colazione con caffè e brioche al bar 💞',
    'Costruendo sedie per i tavoli nei corridoi',
    'Mostrando il Green-Pass alle guardie 👮',
    'Pranzando nel tetto di CV3 mentre il Giaco spiega',
    'Cercando le macchinette del caffè nei sotterranei',
    'Facendo l\'esame di Fondamenti dell\'Informatica',
    'Simulando una FSM di Mealy con SIS',
    'Discutendo di matrici e di ponti con Gregorio',
    'Protestando per la mensa di Borgo Roma',
    'Chiudendo i cancelli a quelli di medicina',
    'Annaffiando le piante della serra mentre fuori piove 🪴 ',
    'Contattando Algida per riavere la macchinetta dei gelati 🍦',
    'Attendendo in coda per riempire la borraccia a CV1',
    'Organizzando uno spritz 🍸 alla Bottega  ',
    'Imprecando contro la sbarra del parcheggio',
    'Indagando sulla roulotte nel parcheggio esterno',
    'Aspettando il 21 in stazione alle 7.15 🧊🚌 ',
    'Ammassando un esercito per conquistare gli uffici del CLA ⚔️',
    'Rubando sedie dal laboratorio Delta',
    'Rincorrendo la 🐑 fuori da CV2.'
    
])

class BotUniVR(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix = commands.when_mentioned_or("."))
        self.persistent_views_added = False


    async def on_ready(self):
        print('Motori a curvatura: ingaggio!')

        # Carica views persistente
        if not self.persistent_views_added:

            self.add_view(BasicInterfaceView())
            self.add_view(ExtraInterfaceView())
            self.persistent_views_added = True

        # Cambia stato del bot ogni 10 minuti
        self.update_status.start()


    @tasks.loop(minutes = 10)
    async def update_status(self):
        
        new_status = str(next(STATUSES))
        print(f'Cambio stato bot a "{new_status}"')
        await self.change_presence(activity = discord.Game(new_status))
