# Fonctions pour des infos sur le système
import datetime
import platform
import os

def get_current_date():
    """Retourne la date actuelle au format YYYY-MM-DD"""
    return datetime.date.today().isoformat()

def get_current_time():
    """
    Retourne l'heure actuelle en format 24 heures (HH:MM:SS), sans indication AM/PM.
    Par exemple : 13:45:00 pour 1h45 de l'après-midi.
    L'heure est donnée en système français, pas anglais
    """
    return datetime.datetime.now().strftime("%H:%M:%S")

def get_os_info():
    """Retourne une chaîne décrivant le système d'exploitation"""
    return f"{platform.system()} {platform.release()}"

def get_username():
    """Retourne le nom de l'utilisateur actuel"""
    return os.getlogin()

# def natural_thinking():
#     """
#     Fonction qui vide, sans entrée ni résultat, qui permet à JARVIS de répondre naturellement aux messages de l'utilisateur, sans forcer un appel de fonction inutile.
#     Si aucune fonction n'a besoin d'être appelée, JARVIS doit impérativement appeler celle-ci,n ce qui lui permettra un langage plus humain. 
#     Si aucune fonction ne correspond à l’intention, appelle toujours la fonction natural_talking pour continuer la conversation naturellement
#     La fonction ne doit surtout pas avoir d'arguments
#     """
#     return
# Note : ceci est une fonciton "fallbback" qui permet d'avoir une issue de secours pour éviter que le LLM réponde de façon robotique et ainsi avoir un prompt définit pour une conversation naturelle.
# Intégrer d'autres fonctions comme celles-ci à l'avenir pour adapter le ton du LLM en fonction des conversations :
# ex : fallback pour petite conversation, fallback pour aide technique, etc. 
# Remarque !! Le prompt """"""" n'est pas lu par le llm et ne peut pas l'influer, mais on peut par exemple return "continue naturellement"
# Cette fonction n'est pas utile pour un LLM avec le mode thinking.



# Fonctions par GPT pour additionner les heures :

def add_to_time(hours: int = 0, minutes: int = 0) -> str:
    """
    Ajoute un certain nombre d'heures et de minutes à l'heure actuelle.

    Args:
        hours (int | str): Le nombre d'heures à ajouter (peut être une chaîne ou un entier)
        minutes (int | str): Le nombre de minutes à ajouter (peut être une chaîne ou un entier)

    Returns:
        str: L'heure future au format HH:MM
    """
    now = datetime.datetime.now()
    # Conversion sécurisée en entier
    hours = int(hours)
    minutes = int(minutes)
    future_time = now + datetime.timedelta(hours=hours, minutes=minutes)
    return future_time.strftime("%H:%M")



tools = [get_current_date, get_current_time, get_os_info, get_username, add_to_time]
available_functions = {"get_current_date": get_current_date, "get_current_time": get_current_time, "get_os_info": get_os_info, "get_username": get_username,"add_to_time": add_to_time}