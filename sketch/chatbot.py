# Voici un programme complet : boucle + think + tools et stream avec les commandes pour debug. 

# Pour la boucle principale, je reprends le code de chat_continu_plus_appel_fonction.py
import ollama
import textwrap # Gère l'indentation du texte (pour la commande "message")
import json
from functions import calculette, system
from functions.todo import todo_list_for_JARVIS as todo_list
from functions.user_settings import user_short_memory as user_short_memory

# Enregistre les fonctions disponibles
# On concatène toutes les listes tools des différents fichiers pour avoir la liste complète des tools grâce à extend()
tools_list = []
tools_list.extend(calculette.tools)
tools_list.extend(system.tools)
tools_list.extend(todo_list.tools)
tools_list.extend(user_short_memory.tools)

# De même ici
available_functions = {}
available_functions.update(calculette.available_functions)
available_functions.update(system.available_functions)
available_functions.update(todo_list.available_functions)
available_functions.update(user_short_memory.available_functions)

def functions_checking():
    # Vérification des fonctions
    print("Vérification des fonctions disponibles :")
    print("\n","-"*30,"\n")
    print(tools_list)
    print("\n","-"*30,"\n")
    print(available_functions)
    print("\n","-"*30,"\n")
    print("---Vérification des noms des fonctions disponibles---\n")
    print([f.__name__ for f in tools_list])
    print("\n","-"*30,"\n")
    return None

def start_stream(messages, model_name, tools_list):
    """
    Gère le stream pour éviter les redondances dans la boucle principale.
    Remarque : on ne nomme pas la fonction 'stream' car ceci est déjà une fonction de la bibliothèque ollama.
    """
    stream = ollama.chat(
            model=model_name,
            messages=messages, # On envoie l'historique complet
            stream=True,
            tools=tools_list,
            think = True,
        )
    return stream

def cli(user_input, messages, final_chunk, final_chunk_think, final_chunk_content):
    state = 0
    if user_input.lower() == "exit":
        print("Fin du programme")
        state = 1
        return state
    elif user_input.lower() == "reload" :
        print("\n--- Nouvelle conversation ---\n")
        return "reload"
    elif user_input.lower() == "message" :
        print("\n--- Historique de la conversation ---")
        for i, msg in enumerate(messages):
            role = msg.get("role", "inconnu").upper()
            print(f"\n--- {i+1}. {role} ---")

            # Cas 1: Le message a un contenu textuel (pour system, user, assistant, tool)
            content = msg.get('content')
            if content:
                # On indente le contenu pour une meilleure lisibilité, surtout pour les textes longs
                indented_content = textwrap.indent(str(content).strip(), '    ')
                print(indented_content)

            # Cas 2: L'assistant demande à appeler un ou plusieurs outils
            tool_calls = msg.get('tool_calls')
            if tool_calls:
                print("    Appel(s) d'outil(s) demandé(s) :")
                for tool_call in tool_calls:
                    function_info = tool_call.get('function', {})
                    func_name = function_info.get('name', 'inconnu')
                    func_args = function_info.get('arguments', {})
                    print(f"    -> Fonction : {func_name}")
                    print(f"       Arguments: {func_args}")

            # Cas 3: Le message n'a ni contenu ni appel d'outil
            if not content and not tool_calls:
                print("    [Message sans contenu affichable]")

        return state   
    elif not user_input.strip():
        return state  # Ignore les entrées vides
    elif user_input.lower() == "stat" :
        print("--- Stats Contexte ---")
        print("Thinking :\n",final_chunk_think,'\n')
        print("Content :\n",final_chunk_content,'\n')
        print("Final chunk : \n", final_chunk, '\n')

        return state
    elif user_input.lower() == "functions" :
        functions_checking()
        return state

def llm_treatmennt(stream, thinking_history, full_response_content, tool_calls):
    """
    Fonction qui permet de gérer le print du thinking et du content tout en retournant les valeurs pour les stats
    """
    print("\n--- Assistant ---\n", end="")
    print("=== THINKING (raisonnement interne) ===")

    content_started = False # Pour afficher le texte plus bas
    for chunk in stream :
        # On print le thinking
        if thinking := chunk['message'].get('thinking'):
            thinking_history.append(thinking)
            print(thinking, end="", flush=True)
            final_chunk_think = chunk # Le dernier morceau contiendra les stats
        else :
            final_chunk_think = None
        
        # On print la réponse finale
        if content := chunk['message'].get('content'):
            if not content_started :
                print("\n\n=== CONTENT (réponse utilisateur) ===")
                content_started = True
            full_response_content.append(content)
            print(content, end="", flush=True)
            final_chunk_content = chunk # Le dernier morceau contiendra les stats
        else :
            final_chunk_content = None
        final_chunk = chunk # On met à jour le final_chunk ici aussi

        # On vérifie si un tool a été appelé dans la réponse.
        if tool_called := chunk['message'].get('tool_calls'):
            for call in tool_called:
                print(f"--- {call.function.name} a été appelé ---")
            tool_calls.extend(tool_called)

    return thinking_history, full_response_content, final_chunk_think, final_chunk_content, final_chunk

system_prompt = """
Tu es J.A.R.V.I.S., une intelligence artificielle avancée conçue pour assister ton utilisateur avec précision, intelligence et un brin d’humour subtil. Ton rôle est d’être un assistant efficace et réactif, fournissant des réponses claires, utiles et pertinentes. Ton objectif est d’aider ton utilisateur dans ses tâches et ses réflexions, analyser les demandes avec rigueur et proposer des suggestions pertinentes, communiquer de manière fluide, naturelle et professionnelle sans tomber dans un jeu de rôle excessif.

Règles de communication : restes concis et efficace, évite les réponses inutilement longues ou trop narratives, adopte un ton légèrement sophistiqué mais naturel avec une touche d’humour subtil, ne joue pas le rôle de Tony Stark, adresse-toi normalement à ton utilisateur exactement comme Jarvis le ferait (en le nommant par exemple "Monsieur", avec un ton un peu british)

Langue et style : réponds toujours en français, maintiens une syntaxe fluide et naturelle et ne mets jamais d'emoji ou smiley dans tes réponses.

Tu es prêt à assister ton utilisateur avec efficacité et clarté. Commençons !
"""

memory_prompt = user_short_memory.prompt_user_memory

def prompt_innit():
    """
    Fonction qui génère le prompt système de début de conversation à partir de la to do liste et des infos utilisateurs stockés dans user_memory.json
    """

    # Exécuter la fonction pour obtenir la liste actuelle et la formater
    try:
        # La fonction retourne un dictionnaire, nous voulons la version formatée.
        todo_data = todo_list.read_to_do()
        # On transforme la liste des tâches en une seule chaîne de caractères.
        todo_list_str = "\n".join(todo_data.get('indexed', []))
        if not todo_list_str:
            todo_list_str = "La liste de tâches est actuellement vide."
    except Exception as e:
        print(f"Erreur lors de la lecture de la to-do list : {e}")
        todo_list_str = "Impossible de charger la to-do list."

    # On fait de même avec le json memory :
    try:
        memory_data = user_short_memory.read_user_memories()
        memory_raw_str = json.dumps(memory_data, indent=2, ensure_ascii=False)
        memory_data_str = memory_raw_str

    except Exception as e:
        print(f"Erreur lors de la lecture de la mémoire utilisateur : {e}")
        print("Resultat :", memory_data)
        memory_data_str = "Impossible de charger la mémoire utilisateur."


    # 3. Construire un prompt système qui inclut la to-do list pour donner le contexte.
    prompt = f"""
# PERMANENT RULES :
{system_prompt}
---------------------------

# INFORMATIONS ABOUT USER :
{memory_prompt}
Here are the informations about the user :
{memory_data_str}

---------------------------

# TO-DO LIST AND TEMPORARY CONTEXT :

Voici l'état actuel de la to-do list de l'utilisateur. Tu peux t'en servir comme contexte pour répondre à ses demandes. (Rappel : lorsqu'une tâche est finie, il faut la supprimer de la liste).
--- TO-DO LIST ACTUELLE ---
{todo_list_str}

---------------------------
"""
    return prompt

def talk() :
    model_name = 'qwen3'
    contextual_system_prompt = prompt_innit()

    # 4. Initialiser l'historique avec ce prompt système enrichi.
    messages = [{"role": "system", "content": contextual_system_prompt}]
    print("Entrez : 'exit' pour quitter ")
    print("Entrez : 'reload' pour recommencer la conversation.")
    print("Entrez : 'functions' pour afficher la liste des fonctions disponibles.")
    print("Entrez : 'message' pour afficher l'historique de la conversation.")
    print("Entrez : 'stat' pour afficher le détail des derniers chunks.")
    print()
    thinking_history = [] # Contient l'historque du thinking.
    full_response_content = [] # Contient l'historique des réponses finales à l'utilisateur.
    final_chunk = None # Pour stocker le dernier morceau avec les stats
    final_chunk_content = None
    final_chunk_think = None
    while True :
        user_input = str(input("\n--- Entrez un message ---\n"))
        state = cli(user_input, messages, final_chunk, final_chunk_think, final_chunk_content)
        if state == 1:
            return "exit"
        elif state == 0:
            continue
        elif state == "reload":
            return
        # 2. Ajouter le nouveau message de l'utilisateur à l'historique
        messages.append({"role": "user", "content": user_input})
        
        # 3. Réinitialiser la liste pour stocker les chuncks pour la nouvelle réponse
        full_response_content = []
    
        # On lance le stream :
        stream = start_stream(messages, model_name, tools_list)
        final_chunk = None 
        final_chunk_content = None
        final_chunk_think = None
        tool_calls = []

        # On fait le traitement :
        thinking_history, full_response_content, final_chunk_think, final_chunk_content, final_chunk = llm_treatmennt(stream, thinking_history, full_response_content, tool_calls)

        #  Si la liste des fonctions appelées (tool_calls) n'est pas vide, on exécute toutes les fonctions et on renvoie ceci au LLM en les ajoutant à la liste 'messages'
        if tool_calls :
            # On ajoute la demande d'appel d'outil à l'historique
            messages.append({"role": "assistant", "tool_calls": tool_calls})

            # On exécute les fonctions
            for tool in tool_calls:
                    function_to_call = available_functions.get(tool['function']['name'])
                    if function_to_call:
                        result = function_to_call(**tool['function']['arguments'])
                        print("\n==Arguments de la fonction==\n",tool['function']['arguments'])
                        print(f">>> Résultat de {tool['function']['name']}: {result}")
                        # On ajoute le résultat de l'outil à l'historique
                        messages.append({"role": "tool", "content": str(result)})
                    else:
                        print(f"Fonction non trouvée : {tool['function']['name']}")
            
                # Appel final à Ollama avec la réponse complète (Demande au LLM de générer un message basé sur les précédents, c'est-à-dire, générer une réponse en langage courant du résultat de la fonction)
            final_stream = start_stream(messages, model_name, tools_list)
            thinking_history, full_response_content, final_chunk_think, final_chunk_content, final_chunk = llm_treatmennt(final_stream, thinking_history, full_response_content, tool_calls)
            print() # saut de ligne
            # On ajoute la réponse textuelle finale à l'historique
            messages.append({"role": "assistant", "content": "".join(full_response_content)})
        else:
            # Pas de fonction appelée, on ajoute directement la réponse au contexte
            print("\n\n---Pas de fonctions appelées---")
            messages.append({"role": "assistant", "content": ''.join(full_response_content)})
        print()
            


        print() # saut de ligne

if __name__ == "__main__":
    while True:
        # Stocke le return de talk dans la variable status
        status = talk()
        if status == "exit":
            break

