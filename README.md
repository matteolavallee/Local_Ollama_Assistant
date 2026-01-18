# Prototype d'Assistant IA avec Ollama

Voici mon prototype d'assistant personnel intelligent conçu pour fonctionner localement grâce à [Ollama](https://ollama.com/). Ce projet vise à explorer les capacités des modèles de langage locaux pour créer une expérience d'assistance personnalisée et évolutive.

---

## À propos de ce projet

Ce prototype est la première étape vers la création d'un assistant IA personnel. Cette première étape comprend un prototype de chatbot qui peut activer des fonctions python (function calling), en mode stream afin d'avoir une interface plus fluide, et en mode think pour qu'il puisse prendre de meilleures décisions sur la manière dont répondre à l'utilisateur.

L'objectif final est de construire un assistant qui apprend de manière autonome et s'intègre de façon transparente dans le quotidien de l'utilisateur.

---

## Architecture du projet

Le projet est structuré pour séparer la logique de l'assistant, les outils et les différents scripts de test. Voici une description détaillée de l'arborescence :

*   `1-Prototype_Chatbot_Ollama/`:
    *   `sketch/`:
        *   `chatbot.py`: Le script principal et le plus abouti pour lancer l'assistant en ligne de commande. Il intègre la gestion du contexte, les outils et le mode "réflexion" (`think`).
    *   `functions/`: Regroupe tous les "outils" (fonctions Python) que l'assistant peut utiliser.
        *   `system.py`: Fonctions liées au système (date, heure, OS...).
        *   `todo/`: Module de gestion de la todo list.
        *   `user_settings/`: Module de gestion de la mémoire de l'utilisateur (`user_short_memory.py`). Le fichier `user_memory.json` est généré ici.
        *   `prompt_system.py`: Fichier contenant différentes versions des prompts système qui ont été testées.
    *   `tests/`: Contient des scripts de test et des versions alternatives du chatbot pour expérimenter des fonctionnalités spécifiques.
    *   `requirements.txt`

Cette organisation a pour but de rendre le projet modulaire et facile à faire évoluer. De nouvelles fonctionnalités (connexion à des APIs, recherche web, etc.) peuvent par exemple être ajoutées comme de nouveaux modules dans le dossier `functions`.

---

## Comment l'utiliser

Le programme utilise Ollama, un logiciel permettant de télécharger des modèles d'IA open source en local et de les faire tourner, voir [mon cours sur Ollama](https://github.com/matteolavallee/Cours_Ollama) pour voir comment je m'y suis pris.

Pour utiliser simplement le chatbot, je conseille
qwen 3 (modèle qui peut utiliser le mode think).

Pour désactiver le think, il suffit de retirer, commenter ou passer en false la ligne ci-dessous dans le fichier `chatbot.py` :
```python
think = True
```

Je conseille, sans think les modèles llama2 ou llama3.1.

Pour interagir avec, exécutez le fichier suivant :
```bash
python 1-Prototype_Chatbot_Ollama/sketch/chatbot.py
```
---

## Fonctionnalités actuelles

Le chatbot est en mode think afin qu'il puisse fournir les meilleures réponses possibles et traiter de la meilleure manière les fonctions à sa disposition. En effet, sans le mode think le LLM ne peut pas exécuter des instructions implicites (par exemple, mettre à jour la todo list). Il faudrait sinon que l'utilisateur lui spécifie "Modifie tel paramètre dans la todolist".

Ce prototype est doté de plusieurs "outils" (fonctions) que l'assistant peut décider d'utiliser pour accomplir des tâches. J'ai d'ailleurs fait en sorte d'ajouter des vérifications à chaque utilisation de fonction pour être sûr que le LLM les exécute correctement.
*   **Gestion de la mémoire utilisateur (`user_short_memory.py`) :** Permet à l'assistant de se souvenir d'informations sur vous (nom, âge, préférences...) entre les conversations. Les données sont stockées dans `user_memory.json`.
*   **Gestion de liste de tâches (`todo.py`) :** Une fonction simple pour ajouter, supprimer et consulter des éléments dans une liste de tâches, permettant à l'assistant de vous aider à vous organiser.
*   **Fonctions système (`system.py`):** Donne à l'assistant l'accès à des informations de base comme la date et l'heure actuelles. Il y a aussi un fichier `calculette.py` qui contient des exemples de fonctions de calculette de base. 

## Installation et Configuration

1.  **Prérequis :**
    *   Assurez-vous d'avoir Python installé sur votre machine.
    *   Installez et configurez Ollama pour faire tourner un modèle de langage localement (je recommande qwen3 pour l'utiliser en mode think) :
        * Installez Ollama depuis cette page : https://ollama.com/download
        * Exécutez les commandes ci-dessous :
        
        ```
        ollama pull qwen3
        ```
        * Si ollama ne tourne pas encore, exécuter cette commande :
        ```
        ollama serve
        ```
        Cette dernière permet de faire tourner l'instance d'Ollama sur le port 11434 du pc. En tapant cette adresse : `http://localhost:11434/`, vous devriez voir "Ollama is running".
        * Il est maintenant prêt à être utilisé.

2.  **Cloner le dépôt :**
    ```bash
    git clone https://github.com/matteolavallee/1-Prototype_Chatbot_Ollama.git
    ```

3.  **Installer les dépendances :**
    ```bash
    pip install -r 1-Prototype_Chatbot_Ollama/requirements.txt
    ```

4.  **Configuration de la mémoire utilisateur :**
    Le système de mémoire est conçu pour s'initialiser tout seul. Lors du premier lancement de l'application, un fichier `user_memory.json` sera créé dans le répertoire `1-Prototype_Chatbot_Ollama/sketch/functions/user_settings/` avec les valeurs par défaut suivantes :

    ```json
    {
        "Name": "",
        "Age": [
            ""
        ],
        "Birthday": "",
        "saved_memories": []
    }
    ```
    Il est donc conseillé pour éviter toute confusion de la part du LLM, de changer ces valeurs manuellement.
    Ce fichier est **essentiel** pour que l'assistant puisse stocker et récupérer des informations sur vous.

## 🎓 Apprenez à créer votre propre assistant !

Au cours du développement de ce prototype, j'ai pris des notes détaillées et créé un cours complet pour vous guider pas à pas dans la création de votre propre assistant IA avec Ollama.

Si vous êtes intéressé, vous pouvez retrouver ce cours [**ici**](https://github.com/matteolavallee/Cours_Ollama).
