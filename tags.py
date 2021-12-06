
# Rappresenta un'associazione Ruolo - Nome, utilizzata per personalizzare
# la struttura del server
class RoleTag:
    def __init__(self, role_id, emoji, name):
        self.role_id = role_id
        self.emoji = emoji
        self.name = name
        

# Rappresentano le tag dei vari corsi di studio
TAGS_DEGREE = [

    # Corsi base
    RoleTag(role_id = 897744705062830122, emoji = '🖥️', name = 'Informatica'),
    RoleTag(role_id = 897744852689768458, emoji = '⚗️', name = 'Bioinformatica'),
    RoleTag(role_id = 897745033636233238, emoji = '🧮', name = 'Matematica Applicata'),
    RoleTag(role_id = 897745828968534067, emoji = '🦿', name = 'Ingegneria dei Sistemi Medicali'),

    # Corsi magistrali
    RoleTag(role_id = 897476170122145834, emoji = '💾', name = 'Ingegneria e scienze informatiche'),
    RoleTag(role_id = 906178441706102784, emoji = '🤖', name = 'Computer Engineering for Robotics and Smart Industry')

]

# Rappresentano le tag dei vari anno accademici
TAGS_YEAR = [
    
    RoleTag(role_id = 874320494499868752, emoji = '', name = '1° Anno'),
    RoleTag(role_id = 874324456305217566, emoji = '', name = '2° Anno'),
    RoleTag(role_id = 874324885390897162, emoji = '', name = '3° Anno')

]

# Rappresentano tag speciali non strutturate
TAGS_SPECIAL = [

    RoleTag(role_id = 907657580933947413, emoji = '👩‍💻', name = 'CyberChallenge'),
    RoleTag(role_id = 907657792024895578, emoji = '🎥', name = 'Cineforum'),
    RoleTag(role_id = 907657843774210049, emoji = '🍹', name = 'AperiScienze'),
    RoleTag(role_id = 907667976491270195, emoji = '🕹️', name = 'Global Game Jam'),

]