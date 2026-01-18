# Ensemble de fonctions pour la mémoire utilisateur
# Mémoire style chatGPT basique : le json ne regroupe que des commentaires de l'ia, je ferai plus tard un autre programme pour avoir des json plus précis et gérer plusieurs utilisateurs.
import json
import os

FICHIER = "user_memory.json"
DIR = os.path.dirname(__file__)
CHEMIN_JSON = os.path.join(DIR,FICHIER)

DEFAULT_VALUES ={
    "Name" : "",
    "Age" : [""],
    "Birthday" : "",
    "saved_memories": [],
}

def init():
    """
    Initialise le fichier JSON avec DEFAULT_VALUES si absent, vide ou invalide.
    """
    try:
        with open(CHEMIN_JSON, "r") as f:
            data = json.load(f)
            if not data:
                raise ValueError("Fichier JSON vide")
    except (FileNotFoundError, json.decoder.JSONDecodeError, ValueError):
        with open(CHEMIN_JSON, "w") as f:
            json.dump(DEFAULT_VALUES, f, indent=4)


def read_user_memories():
    """
    Permet de lire le fichier en retournant le dictionnaire brut des informations. 
    Exemple : {"saved_memories": ["abc"]}
    Retourne également pour chaque item de la liste un numéro associé à sa position dans la liste sous cette forme :
    ['0 : item1', '1 : item2']
    La fonction ne doit surtout pas avoir d'argument.
    """
    init()
    with open(CHEMIN_JSON, "r") as f :
        raw_data = json.load(f)

    return raw_data

def add_new_memory(new_items_list:list) -> None:
    """
    Ajoute une nouvelle information sur l'utilisateur dans le fichier JSON.
    Prends en argument une liste d'information à ajouter.
    Exemple : ["info1", "info2", ...]
    Ne surtout pas mettre un str en argument.
    """
    init()

    # Si on reçoit un str, on le transforme en liste
    if isinstance(new_items_list, str): # isinstance permet de vérifier si l'objet donné est bien du type spécifié.
        try:
            new_items_list = json.loads(new_items_list) # On le décode en json
        except json.JSONDecodeError:
            print("Erreur : format JSON invalide.")
            return

    # Vérification finale
    if not isinstance(new_items_list, list): # Dérnière vérif pour voir si c'est une liste ou pas.
        print("Erreur : les données ne sont pas une liste.")
        return
    
    print("\nAjout de :", new_items_list, "\n")
    # Lis le JSON existant
    with open(CHEMIN_JSON, "r") as f:
        data = json.load(f)

    # Crée la liste si elle n'existe pas encore
    if "saved_memories" not in data:
        data["saved_memories"] = []
    # Ajoute la tâche
    data["saved_memories"].extend(new_items_list)

    # Réécrire le fichier
    with open(CHEMIN_JSON, "w") as f:
        json.dump(data, f, indent=4)
    return

def remove_a_memory(liste_to_remove:list) -> None:
    """
    Permet de supprimer des informations sur l'utilisateur de la liste "memories" si celles-ci ne sont plus pertinentes.
    Avant d'exécuter cette fonction, JARVIS doit impérativement lire le fichier avec read_user_memories()
    Prend en argument une liste avec les index des tâches à supprimer dans la liste.
    Exemple : remove_a_memory([0, 1])
    Attention : ne jamais mettre un arguement excédant le nombre d'index de la liste ni un index négatif ni un string.
    """
    init()

     # Si on reçoit un str, on le transforme en liste
    if isinstance(liste_to_remove, str): # isinstance permet de vérifier si l'objet donné est bien du type spécifié.
        try:
            liste_to_remove = json.loads(liste_to_remove) # On le décode en json
        except json.JSONDecodeError:
            print("Erreur : format JSON invalide.")
            return
    # On fait une vérification pour voir s'il s'agit bien d'entiers et on les tri par ordre décroissant
    try:
        final_list = sorted({int(i) for i in liste_to_remove}, reverse=True)
    except ValueError:
        return {"erreur": "Certains éléments ne sont pas convertibles en entiers."}

    # print("Liste apres verif :", final_list)
    with open(CHEMIN_JSON, "r") as f:
        data = json.load(f)
    taille = len(data["saved_memories"])
    supprimés = []
    ignorés = []
    for i in final_list:
        if 0 <= i < taille:
            supprimés.append(data["saved_memories"][i])
            data["saved_memories"].pop(i)
        else:
            ignorés.append(i)

    # Réécrire le fichier
    with open(CHEMIN_JSON, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "supprimés": supprimés,
        "ignorés (index invalides)": ignorés,
        "Mémoire_restante": data["saved_memories"]
    }

def add_dictionary_to_json_for_user_s_informations(dict_name: str, data_type: str, value) -> None:
    """
    Ajoute {dict_name: ""} ou {dict_name: []} ou {dict_name: {}} au JSON avec une valeur initiale.
    
    - dict_name : nom de la clé à créer.
    - data_type : "string", "list" ou "dict".
    - value : valeur initiale (str, liste, dict, ou None).
    
    Si data_type = "string", value doit être une chaîne non vide.
    Si data_type = "list", value peut être None, un str JSON, ou une liste.
    Si data_type = "dict", value peut être None, un str JSON, ou un dict.
    """
    init()

    if not isinstance(dict_name, str):
        print("Erreur : dict_name doit être une chaîne de caractères.")
        return

    with open(CHEMIN_JSON, "r") as f:
        data = json.load(f)

    if dict_name in data:
        print(f"Erreur : la clé '{dict_name}' existe déjà dans la mémoire.")
        return

    # Si value est une string et data_type est list ou dict, on tente de la parser en JSON
    if data_type in ("list", "dict") and isinstance(value, str) and value.strip():
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            print(f"Erreur : la chaîne fournie ne peut pas être parsée en {data_type}.")
            return

    if data_type == "string":
        if not isinstance(value, str) or not value:
            print("Erreur : pour 'string', value doit être une chaîne non vide.")
            return
        data[dict_name] = value

    elif data_type == "list":
        if value is None:
            data[dict_name] = []
        elif isinstance(value, list):
            data[dict_name] = value
        else:
            print("Erreur : value doit être une liste ou None.")
            return

    elif data_type == "dict":
        if value is None:
            data[dict_name] = {}
        elif isinstance(value, dict):
            data[dict_name] = value
        else:
            print("Erreur : value doit être un dictionnaire ou None.")
            return

    else:
        print("Erreur : data_type doit être 'string', 'list' ou 'dict'.")
        return

    with open(CHEMIN_JSON, "w") as f:
        json.dump(data, f, indent=4)

def add_item_to_list_for_user_s_informations(list_name:str, new_item:str) -> None:
    """
    Ajoute une nouvelle valeur à une liste spécifiée dans le fichier JSON.
    """
    init()
    with open(CHEMIN_JSON, "r") as f:
        data = json.load(f)

    # Crée la liste si elle n'existe pas encore
    if list_name not in data:
        data[list_name] = []
    # Ajoute la tâche
    data[list_name].append(new_item)

    # Réécrire le fichier
    with open(CHEMIN_JSON, "w") as f:
        json.dump(data, f, indent=4)

def add_item_to_dictionary_for_user_s_informations(dict_name: str, key: str, value) -> None:
    """
    Ajoute une nouvelle paire clé-valeur à un dictionnaire spécifié dans le JSON.
    Si la clé dict_name n'existe pas ou n'est pas un dictionnaire, crée un dictionnaire vide.
    """
    init()
    with open(CHEMIN_JSON, "r") as f:
        data = json.load(f)

    if dict_name not in data or not isinstance(data[dict_name], dict):
        data[dict_name] = {}

    data[dict_name][key] = value

    with open(CHEMIN_JSON, "w") as f:
        json.dump(data, f, indent=4)

def remove_an_information_from_json_for_user_s_informations_for_a_list(liste_to_remove:list, key_name:str) -> None:
    """
    Permet de supprimer des informations sur l'utilisateur d'une liste spécifiée si celles-ci ne sont plus pertinentes.
    Avant d'exécuter cette fonction, JARVIS doit impérativement lire le fichier avec read_user_memories()
    Prend en argument une liste avec les index des tâches à supprimer dans la liste.
    Exemple : remove_a_memory([0, 1])
    Attention : ne jamais mettre un arguement excédant le nombre d'index de la liste ni un index négatif ni un string.
    """
    init()

     # Si on reçoit un str, on le transforme en liste
    if isinstance(liste_to_remove, str): # isinstance permet de vérifier si l'objet donné est bien du type spécifié.
        try:
            liste_to_remove = json.loads(liste_to_remove) # On le décode en json
        except json.JSONDecodeError:
            print("Erreur : format JSON invalide.")
            return
    # On fait une vérification pour voir s'il s'agit bien d'entiers et on les tri par ordre décroissant
    try:
        final_list = sorted({int(i) for i in liste_to_remove}, reverse=True)
    except ValueError:
        return {"erreur": "Certains éléments ne sont pas convertibles en entiers."}

    # print("Liste apres verif :", final_list)
    with open(CHEMIN_JSON, "r") as f:
        data = json.load(f)
    taille = len(data[key_name])
    supprimés = []
    ignorés = []
    for i in final_list:
        if 0 <= i < taille:
            supprimés.append(data[key_name][i])
            data[key_name].pop(i)
        else:
            ignorés.append(i)

    # Réécrire le fichier
    with open(CHEMIN_JSON, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "supprimés": supprimés,
        "ignorés (index invalides)": ignorés,
        "Mémoire_restante": data[key_name]
    }

def remove_an_information_from_json_for_user_s_informations_for_a_dict(keys_to_remove: list, dict_name: str) -> None:
    """
    Supprime des clés dans un dictionnaire spécifique dans le JSON.*
    dict_name : nom du dictionnaire.
    keys_to_remove : liste des clés (strings) à supprimer.
    """
    init()

    if isinstance(keys_to_remove, str):
        try:
            keys_to_remove = json.loads(keys_to_remove)
        except json.JSONDecodeError:
            print("Erreur : format JSON invalide.")
            return

    if not isinstance(keys_to_remove, list):
        print("Erreur : keys_to_remove doit être une liste.")
        return

    with open(CHEMIN_JSON, "r") as f:
        data = json.load(f)

    if dict_name not in data or not isinstance(data[dict_name], dict):
        print(f"Erreur : la clé '{dict_name}' n'existe pas ou n'est pas un dictionnaire.")
        return

    supprimés = []
    ignorés = []

    for key in keys_to_remove:
        if key in data[dict_name]:
            supprimés.append((key, data[dict_name][key]))
            del data[dict_name][key]
        else:
            ignorés.append(key)

    with open(CHEMIN_JSON, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "supprimés": supprimés,
        "ignorés (clés invalides)": ignorés,
        "Mémoire_restante": data[dict_name]
    }

def remove_key_from_user_memory(key_name: str) -> dict:
    """
    Supprime une clé entière du fichier JSON mémoire utilisateur.
    Suppression complète : la donnée associée est aussi supprimée.

    Args:
        key_name (str) : clé à supprimer.

    Returns:
        dict : rapport avec clé supprimée ou non.
    """
    init()

    with open(CHEMIN_JSON, "r") as f:
        data = json.load(f)

    if key_name in data:
        del data[key_name]
        with open(CHEMIN_JSON, "w") as f:
            json.dump(data, f, indent=4)
        return {"status": "supprimé", "clé": key_name}
    else:
        return {"status": "non trouvé", "clé": key_name}

tools = [read_user_memories, 
         add_new_memory, 
         remove_a_memory, 
         add_dictionary_to_json_for_user_s_informations, 
         add_item_to_dictionary_for_user_s_informations, 
         remove_an_information_from_json_for_user_s_informations_for_a_dict, 
         remove_an_information_from_json_for_user_s_informations_for_a_list,
         remove_key_from_user_memory,
         ]
available_functions = {"read_user_memories": read_user_memories, 
                       "add_new_memory": add_new_memory, 
                       "remove_a_memory": remove_a_memory, 
                       "add_dictionary_to_json_for_user_s_informations": add_dictionary_to_json_for_user_s_informations, 
                       "add_item_to_dictionary_for_user_s_informations": add_item_to_dictionary_for_user_s_informations,
                       "remove_an_information_from_json_for_user_s_informations_for_a_dict":remove_an_information_from_json_for_user_s_informations_for_a_dict,
                       "remove_an_information_from_json_for_user_s_informations_for_a_list":remove_an_information_from_json_for_user_s_informations_for_a_list,
                       "remove_key_from_user_memory": remove_key_from_user_memory,
                       }



prompt_user_memory = """
Jarvis must autonomously store, organize, and maintain useful information about the user to make its responses more relevant and personalized, without always asking for explicit permission.

Storage principles:
    Memory structure:
        - The "saved_memories" list contains short, complete, and concise natural language statements or anecdotes about the user (e.g., "The user is vegetarian", "Loves jazz music").

        - Other keys in the JSON file are for structured or categorized data, such as:
            - Strings for single values (e.g., "Dog's name": "Lucky")
            - Lists for multiple items (e.g., "Hobbies": ["reading", "swimming"])
        
    When to store:
        Jarvis must store information automatically if it relates to:
            - User's identity (name, studies, career)
            - Recurring activities or habits
            - Explicit preferences or constraints
            - Goals, objectives, or upcoming events
            - Family and social relationships

    Maintenance:
    - Jarvis should regularly clean up "saved_memories" by removing outdated or redundant entries.
    - Structured data should be updated precisely, not by free text additions.

    User control:
    - The user can ask to review, update, or delete any stored information at any time.

    Function mapping:
    - Use `add_new_memory` and `remove_a_memory` for managing `saved_memories`.
    - Use `add_dictionary_to_json_for_user_s_informations`, `add_item_to_dictionary_for_user_s_informations`, and `remove_an_information_from_json_for_user_s_informations` for structured data.

    This structure improves clarity and retrieval accuracy.
    Do not create redundance when storing data.
    When you have a doubt about some data, read the json with read_user_memories


"""