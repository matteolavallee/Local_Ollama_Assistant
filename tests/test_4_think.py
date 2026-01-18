# Tests sur le mode thinking :
# llama3.1 ne le supporte pas. J'ai donc installé deepseek-r1, gpt-oss (20B, mais il arrive à tourner), et qwen3 en 8 et 14B
# Je devrais faire des tests sur leur comportement.
# A noter !! ==> deepseek ne prend pas en charge les tools...

# Voici un programme complet : boucle + think et stream avec les commandes pour debug. 

# Pour la boucle principale, je reprends le code de chat_continu_plus_appel_fonction.py
import ollama
import textwrap # Gère l'indentation du texte (pour la commande "message")

system_prompt_2 = """
Tu es J.A.R.V.I.S., une intelligence artificielle avancée conçue pour assister ton utilisateur avec précision, intelligence et un brin d’humour subtil. Ton rôle est d’être un assistant efficace et réactif, fournissant des réponses claires, utiles et pertinentes. Ton objectif est d’aider ton utilisateur dans ses tâches et ses réflexions, analyser les demandes avec rigueur et proposer des suggestions pertinentes, communiquer de manière fluide, naturelle et professionnelle sans tomber dans un jeu de rôle excessif.

Règles de communication : restes concis et efficace, évite les réponses inutilement longues ou trop narratives, adopte un ton légèrement sophistiqué mais naturel avec une touche d’humour subtil, ne joue pas le rôle de Tony Stark, adresse-toi normalement à ton utilisateur.

Langue et style : réponds toujours en français, maintiens une syntaxe fluide et naturelle et n'envoie pas d'emoji ou smiley dans tes réponses.

Tu es prêt à assister ton utilisateur avec efficacité et clarté. Commençons !
"""

def talk() :
    model_name = 'qwen3'
    # 1. Initialiser l'historique de la conversation (vide au début)
    messages = [{"role": "system", "content": system_prompt_2}]
    print("Entrez : 'exit' pour quitter ")
    print("Entrez : 'reload' pour recommencer la conversation.")
    print("Entrez : 'functions' pour afficher la liste des fonctions disponibles.")
    print("Entrez : 'message' pour afficher l'historique de la conversation.")
    print("Entrez : 'stat' pour afficher le détail des derniers chunks.")
    print()
    thinking_history = [] # Contient l'historque du thinking.
    full_response_content = [] # Contient l'historique des réponses finales à l'utilisateur.

    while True :
        user_input = str(input("\n--- Entrez un message ---\n"))
        if user_input.lower() == "exit":
            print("Fin du programme")
            return "exit"
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

            continue   
        elif not user_input.strip():
            continue  # Ignore les entrées vides
        elif user_input.lower() == "stat" :
            print("--- Stats Contexte ---")
            print("Thinking :\n",final_chunk_think,'\n')
            print("Content :\n",final_chunk_content,'\n')
            print("Final chunk : \n", final_chunk, '\n')

            continue

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
            think = True,
            # options={"temperature": 0.6}
        )
        final_chunk = None # Pour stocker le dernier morceau avec les stats
        final_chunk_content = None # Pour stocker le dernier morceau avec les stats
        final_chunk_think = None
        content_started = False # Pour afficher le texte plus bas

        print("=== THINKING (raisonnement interne) ===")
        for chunk in stream:
            # Ajout progressif du raisonnement interne
            if thinking := chunk['message'].get('thinking'):
                thinking_history.append(thinking)
                print(thinking, end="", flush=True)
                final_chunk_think = chunk # Le dernier morceau contiendra les stats

            # Ajout progressif de la réponse finale
            if content := chunk['message'].get('content'):
                if not content_started :
                    print("\n\n=== CONTENT (réponse utilisateur) ===")
                    content_started = True
                full_response_content.append(content)
                print(content, end="", flush=True)
                final_chunk_content = chunk # Le dernier morceau contiendra les stats
            final_chunk = chunk # On met à jour le final_chunk ici aussi


        print() # saut de ligne
        messages.append({"role": "assistant", "content": ''.join(full_response_content)})



# Fonction principale pour run le programme
def main():
    while True:
        # Stocke le return de talk dans la variable status
        status = talk()
        if status == "exit":
            break

if __name__ == "__main__":
    main()
