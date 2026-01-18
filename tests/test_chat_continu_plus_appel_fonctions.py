# Chat en continu, mode stream, avec historique et compteur de context auquel on a ajouté l'appel de fonctions
import ollama
from prompt_system import system_prompt 
from functions import calculette, system
from functions.todo import todo_list_for_JARVIS as todo_list
import textwrap # D'après Gemini, gère l'indentation du texte (pour la commande "message")

# Enregistre les fonctions disponibles
# On concatène toutes les listes tools des différents fichiers pour avoir la liste complète des tools grâce à extend()
tools_list = []
tools_list.extend(calculette.tools)
tools_list.extend(system.tools)
tools_list.extend(todo_list.tools)

# De même ici, où update() est l'équivalent de extend() mais sur les dictionnaires
available_functions = {}
available_functions.update(calculette.available_functions)
available_functions.update(system.available_functions)
available_functions.update(todo_list.available_functions)

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


def talk() :
    model_name = 'llama3.1'

    # 1. Initialiser l'historique de la conversation (vide au début)
    messages = [{"role": "system", "content": system_prompt}]
    print("Entrez : 'exit' pour quitter ")
    print("Entrez : 'context' pour afficher les stats du contexte")
    print("Entrez : 'reload' pour recommencer la conversation.")
    print("Entrez : 'functions' pour afficher la liste des fonctions disponibles.")
    print("Entrez : 'message' pour afficher l'historique de la conversation.")
    print()

    while True :
        user_input = str(input("--- Entrez un message ---\n"))
        if user_input.lower() == "exit":
            print("Fin du programme")
            return "exit"
        elif user_input.lower() == "context" :
            context_window_stat(final_chunk)
            continue
        elif user_input.lower() == "reload" :
            print("\n--- Nouvelle conversation ---\n")
            return "reload"
        elif user_input.lower() == "functions" :
            functions_checking()
            continue
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

            continue
        
        elif not user_input.strip():
            continue  # Ignore les entrées vides


        # 2. Ajouter le nouveau message de l'utilisateur à l'historique
        messages.append({"role": "user", "content": user_input})
        
        # 3. Réinitialiser la liste pour stocker les chuncks pour la nouvelle réponse
        full_response_content = []
    
        # On lance le stream :
        stream = ollama.chat(
            model=model_name,
            messages=messages, # On envoie l'historique complet
            stream=True,
            # tools=tools_list,
            # think = True,
            # options={"temperature": 0.6}
        )

        tool_calls = []

        # On boucle et on affiche en temps réel
        print("\n--- Assistant ---\n", end="")

        final_chunk = None # Pour stocker le dernier morceau avec les stats

        for chunk in stream:
            # On vérifie si un tool a été appelé dans la réponse.
            if tool_called := chunk['message'].get('tool_calls'):
                for call in tool_called:
                    print(f"--- {call.function.name} a été appelé ---")
                tool_calls.extend(tool_called)

            # On vérifie si le chunk contient du contenu avant de l'afficher/stocker
            # Ces lignes permettent d'afficher une réponse du LLM lorsqu'aucune fonciton n'est appelée.
            if content := chunk['message'].get('content'):
                print(content, end='', flush=True)
                full_response_content.append(content)
            final_chunk = chunk # Le dernier morceau contiendra les stats


         # Exécution des fonctions demandées, si besoin
        if tool_calls:
            # On ajoute la demande d'appel d'outil à l'historique
            messages.append({"role": "assistant", "tool_calls": tool_calls})

            # On exécute les fonctions
            for tool in tool_calls:
                function_to_call = available_functions.get(tool['function']['name'])
                if function_to_call:
                    result = function_to_call(**tool['function']['arguments'])
                    print(f">>> Résultat de {tool['function']['name']}: {result}")
                    # On ajoute le résultat de l'outil à l'historique
                    messages.append({"role": "tool", "content": str(result)})
                else:
                    print(f"Fonction non trouvée : {tool['function']['name']}")
        
            # Appel final à Ollama avec la réponse complète (Demande au LLM de générer un message basé sur les précédents, c'est-à-dire, générer une réponse en langage courant du résultat de la fonction)
            final_stream = ollama.chat(model=model_name, messages=messages, stream=True)
            print("\n>>> Réponse finale de l'assistant <<<")
            final_answer_chunks = []
            for chunk in final_stream:
                if content := chunk['message'].get('content'):
                    print(content, end='', flush=True)
                    final_answer_chunks.append(content)
                final_chunk = chunk # On met à jour le final_chunk ici aussi
            print() # saut de ligne
            # On ajoute la réponse textuelle finale à l'historique
            messages.append({"role": "assistant", "content": "".join(final_answer_chunks)})
        else:
            # Pas de fonction appelée, on ajoute directement la réponse au contexte
            print("\nPas de fonctions appelées.")
            messages.append({"role": "assistant", "content": ''.join(full_response_content)})
        print()


max_context = 131072 # Taille max du contexte pour llama3.1
def context_window_stat(final_chunk) :

# Calculer et afficher l'utilisation du contexte
    if final_chunk:
        prompt_tokens = final_chunk.get('prompt_eval_count', 0)
        response_tokens = final_chunk.get('eval_count', 0)
        # L'historique complet (prompt + réponse) consomme ce total de tokens
        total_tokens_in_history = prompt_tokens + response_tokens
        remaining_context = max_context - total_tokens_in_history
        print(f"\n--- Stats Contexte ---")
        print(f"Requête envoyée: {prompt_tokens} tokens | Réponse générée: {response_tokens} tokens")
        print(f"Taille totale de l'historique: {total_tokens_in_history} tokens")
        print(f"Contexte restant estimé: {remaining_context} / {max_context} tokens")
        print(f"-"*30,"\n")
    elif not final_chunk:
        print("Aucun message n'a encore été envoyé :")
        print(f"Contexte restant : {max_context} tokens")


# Fonction principale pour run le programme
def main():
    while True:
        # Stocke le return de talk dans la variable status
        status = talk()
        if status == "exit":
            break

if __name__ == "__main__":
    main()
