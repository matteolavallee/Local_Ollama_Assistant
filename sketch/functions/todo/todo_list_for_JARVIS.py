# Programme de to-do list pour jarvis
# Code adapté pour l'usage des tools
import json
import os

# --- Constantes ---
# FICHIER est une constante, non mutable donc, par convention en python, on les note en majuscule.
FICHIER = "todo.json"
DIR = os.path.dirname(__file__)
CHEMIN_TODO = os.path.join(DIR,FICHIER)


def init():
    """
    Initialise le programme en vérifiant l'existance du fichier.
    Vérifie si le json est vide ou pas, le remplace par {"taches": []}
    """ 
    # Vérifie si le fichier existe
    if not os.path.exists(CHEMIN_TODO):
        # S'il n'existe pas, on crée une structure vide
        with open(CHEMIN_TODO, "w") as f:
            json.dump({"taches": []}, f, indent=4)
            print("Fichier 'todo.json' créé.")
    else:
            print("Fichier 'todo.json' déjà existant.")

    try:
        with open(CHEMIN_TODO, "r") as f:
            data = json.load(f)
            if not data:
                 with open(CHEMIN_TODO, "w") as f:
                    json.dump({"taches": []}, f, indent=4)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        data = {"taches": []}
        with open(CHEMIN_TODO, "w") as f:
            json.dump(data, f, indent=4)
    return

def read_to_do():
    """
    Permet de lire le fichier en retournant le dictionnaire brut des tâches. 
    Exemple : {"taches": [to_do_list]}
    Retourne également pour chaque item de la liste un uméro associé à sa position dans la liste sous cette forme :
    ['0 : tache1', '1 : tache2']
    La fonction ne doit surtout pas avoir d'argument.
    """
    init()
    with open(CHEMIN_TODO, "r") as f :
        raw_data = json.load(f)
        content =  []
        for i, item in enumerate(raw_data["taches"]):
            content.append(f"Index {i} : {item}")

    return {"indexed": content, "raw": raw_data["taches"]}

def add_item_to_list(new_items_list:list) -> None:
    """
    Ajoute une nouvelle tâche à la liste dans le fichier JSON.
    Prends en argument une liste de tâches à ajouter.
    Exemple : ["tache1", "tache2", ...]
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
    with open(CHEMIN_TODO, "r") as f:
        data = json.load(f)

    # Crée la liste si elle n'existe pas encore
    if "taches" not in data:
        data["taches"] = []
    # Ajoute la tâche
    data["taches"].extend(new_items_list)

    # Réécrire le fichier
    with open(CHEMIN_TODO, "w") as f:
        json.dump(data, f, indent=4)
    return

def remove_an_item(liste_to_remove:list) -> None:
    """
    Lorsque l'utilisateur a fini une tâche, cette fonction permet de la supprimer de la liste, ce qui équivaut à "marquer comme terminée".
    Avant d'exécuter cette fonction, JARVIS doit impérativement lire le fichier avec read_to_do()
    Prend en argument une liste avec les index des tâches à supprimer dans la liste.
    Exemple : remove_an_item([0, 1])
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
    with open(CHEMIN_TODO, "r") as f:
        data = json.load(f)
    taille = len(data["taches"])
    supprimés = []
    ignorés = []
    for i in final_list:
        if 0 <= i < taille:
            supprimés.append(data["taches"][i])
            data["taches"].pop(i)
        else:
            ignorés.append(i)

    # Réécrire le fichier
    with open(CHEMIN_TODO, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "supprimés": supprimés,
        "ignorés (index invalides)": ignorés,
        "to_do_restante": data["taches"]
    }

tools = [read_to_do, add_item_to_list, remove_an_item]
available_functions = {"read_to_do": read_to_do, "add_item_to_list": add_item_to_list, "remove_an_item": remove_an_item}


