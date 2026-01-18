# Programme de to-do list pour jarvis
# Code général de tests pour json avec terminal interactif
import json
import os

# --- Constantes ---
# FICHIER est une constante, non mutable donc, par convention en python, on les note en majuscule.
FICHIER = "todo.json"
DIR = os.path.dirname(__file__)
CHEMIN_TODO = os.path.join(DIR,FICHIER)


print("---Initialisation---")
# Vérifie si le fichier existe
if not os.path.exists(CHEMIN_TODO):
    # S'il n'existe pas, on crée une structure vide
    with open(CHEMIN_TODO, "w") as f:
        json.dump({"taches": []}, f, indent=4)
        print("Fichier 'todo.json' créé.")
else:
        print("Fichier 'todo.json' déjà existant.")

def init():
    """
    Vérifie si le json est vide ou pas, le remplace par {} et return was_empty pour rendre compte de l'état.
    """
    print("Vérification :")
    try:
        with open(CHEMIN_TODO, "r") as f:
            data = json.load(f)
            was_empty = False
            if data == {}:
                was_empty = True
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        data = {}
        with open(CHEMIN_TODO, "w") as f:
            json.dump(data, f, indent=4)
            was_empty = True
    print("Fin de vérification")
    return was_empty


def read_to_do():
    print("-"*10)
    print("\nLecture du fichier\n")

    with open(CHEMIN_TODO, "r") as f :
        content = json.load(f)
        print(content)
        print("Fin de lecture\n")
        print("-"*10)

    return content

def add_dict(json_item: dict, content: dict) -> None:
    """
    Ajoute un élément au fichier sous format json
    """
    print("-"*10)
    print("\nOn ajoute :", json_item, "\n à")
    print(content)

    print("-"*10)
    # Utilise was_empty pour savoir quelle méthode utiliser pour ajouter ou concaténer un dict
    if not was_empty :
        content.update(json_item)
        print("Contenu final :", content)
    elif was_empty :
        content = json_item
        print("Contenu final :", content)

    with open(CHEMIN_TODO, "w") as f :
        json.dump(content, f, indent=4)


def add_item_to_list(list_name:str, new_item:str) -> None:
    """
    Ajoute une nouvelle tâche à la liste dans le fichier JSON.
    """
    print("-" * 10)
    print("\nAjout d'une tâche :", new_item, "à la liste", list_name, "\n")

    # Utilise was_empty pour vérifier si une liste existe ou pas
    if not was_empty :
        # Étape 1 : Lire le JSON existant
        with open(CHEMIN_TODO, "r") as f:
            data = json.load(f)
    elif was_empty :
        print("Le fichier est vide, veuillez ajouter un dictionnaire")
        return

    # Crée la liste si elle n'existe pas encore
    if list_name not in data:
        data[list_name] = []
    # Ajoute la tâche
    data[list_name].append(new_item)

    # Réécrire le fichier
    with open(CHEMIN_TODO, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    
    
    while True :
        was_empty =init()
        print("\nQue souhaitez-vous faire ?")
        print(" - 'y' : ajouter quelque chose")
        print(" - 'n' : ignorer et relancer")
        print(" - 'read' : lire le fichier")
        print(" - 'empty' : vider le fichier")
        print(" - 'exit' : quitter\n")

        content = read_to_do()
        response = str(input("Voulez vous ajouter du contenu ? (y/n)"))
        if response.lower() =="exit":
            print("Fin du programme")
            break

        elif response.lower() == "empty":
            with open(CHEMIN_TODO, "w") as f:
                json.dump({}, f, indent=4)
                was_empty = True
            continue


        elif response.lower() == "read":
            read_to_do()
            continue

        elif response.lower() == "y" :
            type_input = int(input("1 : update une liste\n2 : Ajouter un dictionnaire\n"))

            if type_input == 1 :
                list_name = str(input("Entrez la liste à modifier"))
                new_item = str(input("Entrez la nouvelle tâche"))
                add_item_to_list(list_name, new_item)

            elif type_input == 2 :
                try :
                    json_item = str(input("Entrez le dictionnaire à ajouter"))
                    json_item = json.loads(json_item)
                    add_dict(json_item, content)
                except json.JSONDecodeError:
                    print("Format invalide. Entrez un dictionnaire JSON valide.")
                    continue
                
        elif response.lower() == "n":
            continue
