"Je vais te donner l'architecture complète de mon projet FORPY. Lis la attentivement avant de commencer à coder. Une fois que tu as bien compris l'architecture, commence par mettre en place la Phase 1 uniquement : crée la structure complète du projet avec tous les dossiers et fichiers définis.
For Python (FORPY) - Architecture IA “prompt-driven”

1) Énoncé du projet


Projet : Application d'apprentissage interactif de Python

Contexte métier : L'intelligence artificielle et le vibe coding transforment profondément les pratiques de développement. Il faut donc apprendre Python pour être rapidement autonome. Ce projet open source vise à développer une application installable permettant de générer, via l'IA, des mini-exercices personnalisés avec leurs corrections, afin d'apprendre Python de manière interactive et progressive.
Fonctionnement : L'utilisateur renseigne sa propre clé API directement dans l'application — celle de son fournisseur IA personnel (Anthropic, OpenAI, ou autre). Il peut ensuite générer des exercices adaptés à son niveau. La consommation API est facturée directement entre l'utilisateur et son fournisseur IA, sans aucun intermédiaire. Pour garantir une sécurité maximale, la clé API est stockée exclusivement en local sur l'appareil, sans aucune transmission vers un serveur externe.


Domaine métier : Éducation / EdTech
Langage : Python
Framework : Flet (multiplateforme, un seul codebase)
Plateforme : Application installable multiplateforme (Windows, macOS, Linux, Android, iOS) — distribuée via un site web dédié avec deux options :
Téléchargement direct de l'application prête à l'emploi
Accès au code source complet via GitHub (projet open source)


Modèle économique :
L'application est fournie gratuitement
L'utilisateur apporte et gère sa propre clé API
Aucun coût serveur ni de trafic après téléchargement pour le créateur.


Fonctionnalités principales :
Parcours d'apprentissage structuré par niveau : Noob → Débutant → Intermédiaire → Intermédiaire ++ → POO → Expert Architecture
Exercices interactifs générés par IA avec correction détaillée




Contraintes techniques
Application multiplateforme installable (PC & mobile)
Temps de réponse rapide pour la génération des exercices
Aucun serveur backend — tout fonctionne en local
MVP réalisable en 1 semaine


Stack technique
Langage : Python
Framework UI : Flet
Stockage local : fichiers JSON ou SQLite
Appels IA : API du fournisseur choisi par l'utilisateur






Phase 1 — Fondations

Objectif : Définir l'architecture globale de l'application et mettre en place les bases du projet.
Tâches concrètes
Définir l'architecture globale de l'application
Choisir l'architecture interne (découpage en couches)
Concevoir le modèle de données pédagogique
Mettre en place l'environnement de développement
Créer la structure de projet
Configurer le repository GitHub (code source + releases)
Mettre en place le système de gestion de la clé API en local
Concevoir l'écran Paramètres (clé API, fournisseur IA, langue)
Mettre en place le système de gestion des langues (interface + exercices)


Architecture globale

Utilisateur
    ↓
App Flet (local)
    ↓
Choix du Chapter (Python — extensible : Python ML, Python IA...)
    ↓
Choix du Level + SubLevel
    ↓
Appel du prompt correspondant
    ↓
API IA (Claude / OpenAI / Gemini / autre)
    ↓
Exercice généré (JSON)
    ↓
Affichage de l'exercice complet



Modèles de données principaux
Chapter — domaine d'apprentissage (Python pour le MVP, extensible dans le futur)
Level — 6 niveaux principaux, chacun avec ses sous-niveaux :

0. Noob
   └── Noob

1. Débutant
   ├── Débutant
   ├── Débutant ++
   └── DEBUG Débutant

2. Intermédiaire
   ├── Intermédiaire
   ├── Intermédiaire Avancé
   ├── DEBUG Intermédiaire
   ├── Pythonique Intermédiaire
   └── Pattern

3. Intermédiaire ++
   ├── Fonctions avancées
   ├── Manipulation structure
   ├── Entrée/Sortie et erreurs
   ├── Organisation du code
   ├── DEBUG Intermédiaire ++
   ├── Pythonique Intermédiaire ++
   └── Pattern

4. POO
   ├── Intro POO
   ├── POO ++
   ├── DEBUG POO
   ├── POO Pythonique
   └── Pattern

5. Expert Architecture
   ├── Architecture
   ├── DEBUG Architecture
   ├── Architecture Pythonique
   └── Pattern




Exercise — généré dynamiquement par l'IA (JSON structuré)
UserSettings — langue interface, langue exercices, clé API, fournisseur IA
Relation simplifiée :
UserSettings (langue interface, langue exercices, clé API, fournisseur IA)
    ↓
Chapter (Python)
└── Level
    └── SubLevel
        └── Prompt dédié → Exercise (généré par l'IA)



Structure du projet


forpy/
├── screens/
│   ├── home_screen.py        # Écran d'accueil
│   ├── chapter_screen.py     # Choix du Chapter (Python, Python ML...)
│   ├── level_screen.py       # Choix du Level
│   ├── sublevel_screen.py    # Choix du SubLevel
│   ├── exercise_screen.py    # Affichage exercice complet + bouton
│   └── settings_screen.py    # Clé API, fournisseur IA, langues
├── services/
│   ├── ai_service.py         # Appels API IA
│   └── prompt_builder.py     # Sélection et appel du prompt
├── prompts/
│   └── python/               # MVP — extensible (python_ml/, python_ia/...)
│       ├── noob.txt
│       ├── debutant.txt
│       ├── debutant_plus.txt
│       ├── debug_debutant.txt
│       ├── intermediaire.txt
│       ├── intermediaire_avance.txt
│       ├── debug_intermediaire.txt
│       ├── pythonique_intermediaire.txt
│       ├── pattern_intermediaire.txt
│       ├── fonctions_avancees.txt
│       ├── manipulation_structure.txt
│       ├── entree_sortie_erreurs.txt
│       ├── organisation_code.txt
│       ├── debug_intermediaire_plus.txt
│       ├── pythonique_intermediaire_plus.txt
│       ├── pattern_intermediaire_plus.txt
│       ├── intro_poo.txt
│       ├── poo_plus.txt
│       ├── debug_poo.txt
│       ├── poo_pythonique.txt
│       ├── pattern_poo.txt
│       ├── architecture.txt
│       ├── debug_architecture.txt
│       ├── architecture_pythonique.txt
│       └── pattern_expert.txt
├── utils/
│   ├── translations.json     # Toutes les langues de l'interface
│   └── session_state.py      # Mémorisation dernière session + langues
└── logs/
    ├── api_errors.log        # Erreurs d'appel API IA
    ├── json_errors.log       # Erreurs de parsing JSON
    └── app.log               # Logs généraux de l'app





Fichier settings.example.json


{
    "api_key": "votre-clé-api-ici",
    "provider": "anthropic",
    "interface_language": "english",
    "exercise_language": "english"
}



Fichier translations.json


{
    "english": {
        "welcome": "Welcome to FORPY",
        "settings": "Settings",
        "api_key": "API Key",
        "another_exercise": "Another exercise",
        "level": "Level",
        "interface_language": "Interface language",
        "exercise_language": "Exercise language"
    },
    "french": {
        "welcome": "Bienvenue sur FORPY",
        "settings": "Paramètres",
        "api_key": "Clé API",
        "another_exercise": "Un autre exercice",
        "level": "Niveau",
        "interface_language": "Langue de l'interface",
        "exercise_language": "Langue des exercices"
    }
}




Livrables
Architecture documentée
Schéma des données
Repository GitHub initialisé
Structure de projet mise en place
Prototype de navigation (écrans principaux)
Fichier translations.json avec anglais et français
Fichier settings.example.json documenté


Points de vigilance
Séparation claire UI / logique métier
Modularité pour faciliter les contributions open source
Sécurité du stockage local de la clé API
Structure des prompts organisée par Chapter pour faciliter l'évolutivité
Un fichier prompt par SubLevel pour faciliter la maintenance et les contributions
settings.json ajouté au .gitignore pour ne jamais exposer la clé API
translations.json facilement extensible pour ajouter de nouvelles langues







Phase 2 — Cœur métier pédagogique

Objectif : Implémenter la logique de génération des exercices et l'affichage des corrections.


Tâches concrètes
Implémenter le gestionnaire de prompts (prompt_builder.py)
Implémenter le service d'appels API IA (ai_service.py)
Construire le parser JSON universel
Construire l'affichage complet de l'exercice
Implémenter le bouton "Un autre exercice"
Gérer les erreurs d'appel API (timeout, clé invalide, quota dépassé)
Implémenter la gestion du state de session
Implémenter l'injection de la langue des exercices dans les prompts




Design Patterns utilisés
Strategy Pattern — supporter plusieurs fournisseurs IA :

class AIProvider:
    def call(self, prompt, api_key):
        pass

class ClaudeProvider(AIProvider):
    def call(self, prompt, api_key):
        # Appel API Anthropic
        pass

class OpenAIProvider(AIProvider):
    def call(self, prompt, api_key):
        # Appel API OpenAI
        pass

class GeminiProvider(AIProvider):
    def call(self, prompt, api_key):
        # Appel API Google
        pass



Factory Pattern — sélectionner le bon prompt selon le Chapter + SubLevel :

class PromptFactory:
    def get_prompt(self, chapter, sublevel, exercise_language):
        path = f"prompts/{chapter}/{sublevel}.txt"
        prompt = open(path).read()
        # Injection de la langue des exercices
        prompt = prompt.replace("{language}", exercise_language)
        return prompt



Format JSON universel
Un seul format de réponse pour tous les types de prompts (standard, debug, pythonique, pattern) :

{
    "enonce": "...",      # 1) L'énoncé clair et simple
                          #    (avec code si liste, sans code sinon)
    "correction": "...",  # 2) La correction en code Python
                          #    prêt à être copié
    "explication": "...", # 3) L'explication ligne par ligne
                          #    sans jargon
    "deroulement": "..."  # 4) Le paragraphe fluide oral
                          #    décrivant le déroulement
}
```

**Flux de génération d'un exercice**
```
Utilisateur choisit Chapter + Level + SubLevel
    ↓
PromptFactory charge le prompt correspondant
    ↓
Injection de la langue des exercices dans le prompt
    ↓
AIService envoie le prompt au fournisseur IA sélectionné
    ↓
Réponse JSON parsée (format universel)
    ↓
Affichage complet :
    ├── Énoncé
    ├── Correction (code Python)
    ├── Explication ligne par ligne
    └── Déroulement oral
    ↓
Bouton "Un autre exercice"
```

**Flux "Un autre exercice"**
```
Bouton "Un autre exercice"
    ↓
Récupère le dernier sujet généré (session_state)
    ↓
Injecte le sujet dans le prompt comme contrainte
    ↓
Injecte la langue des exercices dans le prompt
    ↓
IA génère un exercice sur un sujet différent
    ↓
Met à jour le session_state avec le nouveau sujet
    ↓
Affichage du nouvel exercice
State de session


# utils/session_state.py
{
    "last_exercise_topic": "listes",
    "last_sublevel": "debutant",
    "interface_language": "english",    
    "exercise_language": "english"      
}
```

**Gestion des erreurs**
```
Clé API invalide       → Message clair + redirection Paramètres
Quota dépassé          → Message clair + lien fournisseur IA
Timeout API            → Retry automatique (x2) puis message erreur
Réponse JSON invalide  → Retry automatique puis message erreur



Livrables
Gestionnaire de prompts fonctionnel
Intégration API IA (Claude, OpenAI, Gemini, compatible OpenAI)
Parser JSON universel robuste
Affichage complet de l'exercice (énoncé, correction, explication, déroulement)
Bouton "Un autre exercice" fonctionnel
State de session fonctionnel (anti-répétition des exercices)
Injection de la langue des exercices dans chaque prompt



Points de vigilance
Feedback rapide à l'utilisateur (indicateur de chargement pendant l'appel IA)
Gestion robuste des erreurs API
Parser JSON tolérant aux variations de format de l'IA
Séparation claire entre la logique IA et l'affichage
Un fichier prompt par SubLevel pour faciliter la maintenance et les contributions open source
State réinitialisé automatiquement au changement de SubLevel
Vérifier que {language} est présent dans chaque fichier prompt .txt
La langue des exercices est indépendante de la langue de l'interface


Phase 3 — Interface utilisateur


Objectif : Construire une interface claire, fluide et agréable pour naviguer entre les niveaux et consulter les exercices.


Tâches concrètes
Construire l'écran d'accueil (home_screen.py)
Construire l'écran de choix du Chapter (chapter_screen.py)
Construire l'écran de choix du Level (level_screen.py)
Construire l'écran de choix du SubLevel (sublevel_screen.py)
Construire l'écran d'affichage de l'exercice (exercise_screen.py)
Construire l'écran Paramètres (settings_screen.py)
Implémenter la navigation entre les écrans
Implémenter le système de traduction de l'interface
Appliquer le changement de langue en temps réel sans redémarrer l'app



Flux de navigation


Écran d'accueil
    ↓
Choix du Chapter (Python)
    ↓
Choix du Level (ex: Intermédiaire)
    ↓
Choix du SubLevel (ex: Intermédiaire Avancé)
    ↓
Affichage de l'exercice généré :
    ├── Énoncé
    ├── Correction
    ├── Explication ligne par ligne
    └── Déroulement oral
    ↓
[Un autre exercice] → nouvel exercice généré
[← Retour]          → retour au choix du SubLevel
Structure de chaque écran
Écran d'accueil :

┌─────────────────────────────┐
│  FORPY                      │
│  ─────────────────────────  │
│  [Python]                   │
│                             │
│  ⚙️ Settings                │
└─────────────────────────────┘



Écran Level :

┌─────────────────────────────┐
│  ← Python                   │
│  ─────────────────────────  │
│  [Noob]                     │
│  [Débutant]                 │
│  [Intermédiaire]            │
│  [Intermédiaire ++]         │
│  [POO]                      │
│  [Expert Architecture]      │
└─────────────────────────────┘


Écran exercice :


┌─────────────────────────────┐
│  ← Intermédiaire Avancé     │
│  ─────────────────────────  │
│  📝 Énoncé                  │
│  ─────────────────────────  │
│  ✅ Correction              │
│  ─────────────────────────  │
│  💡 Explication             │
│  ─────────────────────────  │
│  🎙️ Déroulement             │
│  ─────────────────────────  │
│  [Un autre exercice]        │
└─────────────────────────────┘



Écran Paramètres :


┌─────────────────────────────┐
│  ⚙️ Settings                │
│  ─────────────────────────  │
│  AI Provider                │
│  [Claude] [OpenAI] [Gemini] │
│  ─────────────────────────  │
│  API Key                    │
│  [••••••••••••••••••]       │
│  ─────────────────────────  │
│  Interface Language         │
│  [English ▼]                │
│  ─────────────────────────  │
│  Exercise Language          │
│  [English ▼]                │
└─────────────────────────────┘



Système de traduction


# Chargement des traductions depuis translations.json
import json

def load_translations(language):
    with open("utils/translations.json") as f:
        translations = json.load(f)
    return translations[language]

# Utilisation dans les écrans
t = load_translations(user_settings["interface_language"])
button_text = t["another_exercise"]
title_text = t["welcome"]



Livrables
Tous les écrans implémentés et connectés
Navigation fluide entre les écrans
Écran Paramètres fonctionnel (clé API, fournisseur IA, langues)
Indicateur de chargement pendant la génération de l'exercice
Bouton "Un autre exercice" fonctionnel
Système de traduction de l'interface fonctionnel
Changement de langue appliqué en temps réel

Points de vigilance
Interface simple et intuitive
Lisibilité du code affiché (police monospace pour le code)
Expérience fluide sur PC et mobile (responsive)
Indicateur de chargement clair pendant l'appel API IA
Message d'erreur clair si la clé API n'est pas renseignée
Tous les textes de l'interface chargés depuis translations.json
Aucun texte en dur dans le code — tout passe par le système de traduction
Changement de langue instantané sans redémarrage de l'app




Phase 4 — Qualité, packaging et distribution


Objectif : Stabiliser l'application, la tester, la packager et la distribuer via GitHub et le site web.


Tâches concrètes
Écrire les tests unitaires
Tester l'intégration API IA (tous les fournisseurs)
Tester la navigation et l'affichage sur PC et mobile
Corriger les bugs identifiés
Packager l'application pour chaque plateforme
Créer le repository GitHub et publier la première release
Mettre en ligne le site web de distribution
Tester le système de traduction sur toutes les langues disponibles
Vérifier que {language} est bien injecté dans tous les prompts


Tests & qualité
Tests unitaires :

prompt_builder.py      → vérifier que le bon prompt est chargé
                         selon le Chapter + SubLevel
                       → vérifier que {language} est bien
                         injecté dans chaque prompt
ai_service.py          → vérifier que l'appel API fonctionne
                         et retourne un JSON valide
parser JSON            → vérifier que le parser gère correctement
                         les 4 champs (enonce, correction,
                         explication, deroulement)
settings.json          → vérifier que la clé API est bien
                         sauvegardée et chargée en local
session_state.py       → vérifier que le state est bien mis à jour
                         et réinitialisé au changement de SubLevel
translations.json      → vérifier que toutes les clés existent
                         dans chaque langue disponible



Tests d'intégration :

Claude (Anthropic)     → appel réel + parsing JSON
OpenAI                 → appel réel + parsing JSON
Gemini                 → appel réel + parsing JSON
Compatible OpenAI      → appel réel + parsing JSON (Mistral, Groq...)


Tests UI :

Navigation complète         → home → chapter → level
                              → sublevel → exercice
Bouton "Un autre exercice"  → nouvel exercice différent
                              du précédent
Écran Paramètres            → clé API sauvegardée
                            → langue interface modifiée
                            → langue exercices modifiée
Gestion des erreurs         → clé API invalide, timeout,
                              JSON invalide
Affichage PC                → mise en page correcte
                              sur grand écran
Affichage mobile            → mise en page correcte
                              sur petit écran
Changement de langue        → interface mise à jour
                              en temps réel
Exercices en anglais        → vérifier que l'IA répond
                              bien en anglais
Exercices en français       → vérifier que l'IA répond
                              bien en français





Packaging & distribution
Génération des fichiers installables avec Flet :

Windows   → forpy-v1.0.exe
Linux     → forpy-v1.0.AppImage
Android   → forpy-v1.0.apk


Structure des releases GitHub :


GitHub Releases v1.0
├── forpy-v1.0.exe            # Windows
├── forpy-v1.0.AppImage       # Linux
├── forpy-v1.0.apk            # Android
├── README.md                 # Guide d'installation
└── CHANGELOG.md              # Notes de version


Site web de distribution
Contenu minimal du site :



├── Présentation du projet (1 page)
├── Boutons de téléchargement par plateforme
│   ├── [Download Windows]   → GitHub Release .exe
│   ├── [Download Linux]     → GitHub Release .AppImage
│   └── [Download Android]   → GitHub Release .apk
├── Lien GitHub → code source complet
└── Guide de démarrage rapide
    ├── Install the app
    ├── Get your API key
    └── Start your first exercise



Monitoring local

logs/
├── api_errors.log      # Erreurs d'appel API IA
├── json_errors.log     # Erreurs de parsing JSON
└── app.log             # Logs généraux de l'app


Livrables
Tests unitaires et d'intégration validés
Bugs corrigés
Fichiers packagés pour Windows, Linux et Android
Repository GitHub avec première release publiée
Site web de distribution en ligne
README et guide de démarrage rapide
Système de traduction testé et validé (anglais + français)
Vérification que tous les prompts contiennent {language}


Points de vigilance
Tester avec plusieurs clés API réelles avant la release
Vérifier l'affichage du code Python (police monospace) sur toutes les plateformes
S'assurer que la clé API est bien chiffrée en local
Vérifier que le bouton "Un autre exercice" ne génère jamais le même exercice deux fois de suite
README clair pour faciliter les contributions open source
Vérifier que settings.json est bien absent du repository GitHub
Vérifier que settings.example.json est bien présent et documenté
Tester le changement de langue en cours de session





Phase 5 — Design & Expérience utilisateur

Objectif : Implémenter une interface visuelle soignée, cohérente et agréable sur tous les écrans, avec support dark/light mode. Le dark mode est activé par défaut au lancement.
Tâches concrètes
Implémenter le thème global dark mode par défaut
Implémenter le thème light mode
Implémenter le toggle dark/light mode dans les Paramètres
Sauvegarder le choix du mode dans settings.json
Redesigner l'écran d'accueil
Redesigner l'écran des niveaux
Redesigner l'écran des sous-niveaux
Redesigner l'écran d'exercice avec bloc de code style VS Code
Redesigner l'écran Paramètres
Vérifier le responsive PC et mobile


Palettes de couleurs
Dark mode (défaut) :
Fond principal     → #1a1a2e
Fond cards         → #22223a
Fond code          → #1e1e1e
Accent bleu        → #4a9eff
Texte principal    → #ffffff
Texte code         → #d4d4d4
Bordures           → #2a2a4a
Séparateurs        → #4a9eff
Boutons principaux → fond #ffffff, texte #1a1a2e


Light mode :

Fond principal     → #f5f7fa
Fond cards         → #ffffff
Fond code          → #1e1e1e
Accent bleu        → #1a6ecc
Texte principal    → #1a1a2e
Texte code         → #d4d4d4
Bordures           → #e0e4ec
Séparateurs        → #1a6ecc
Boutons principaux → fond #1a1a2e, texte #ffffff


Bloc de code (identique dans les deux modes) :


Fond               → #1e1e1e
Texte              → #d4d4d4
Keywords           → #569cd6 (bleu)
Fonctions          → #dcdcaa (jaune)
Strings            → #ce9178 (orange)
Commentaires       → #6a9955 (vert)



Composants par écran
Écran d'accueil (home_screen.py) :

AppBar :
├── Titre FORPY centré (blanc dark / foncé light)
└── Icône ⚙️ à droite (accent bleu)

Hero :
├── Icône logo 🐍 (72x72px, fond accent22,
│   bordure accent66, border-radius 20px)
├── Texte FORPY (28px, bold)
└── Sous-titre "For Python — Learn by doing"
    (12px, couleur texte principal)

Boutons :
├── Python → bouton principal
├── Python ML — coming soon → opacity 0.4
└── Python IA — coming soon → opacity 0.4


Écran niveaux (level_screen.py) :


AppBar :
├── Bouton retour ← (accent bleu)
└── Titre "Python"

Contenu :
├── Label "Choisissez votre niveau"
└── Pour chaque niveau :
    ├── Bouton niveau (taille adaptée au texte)
    ├── Badge "X niveaux" (accent bleu, 11px)
    └── Séparateur (1px, accent bleu)



Écran sous-niveaux (sublevel_screen.py) :


→ Même style que l'écran niveaux



Écran exercice (exercise_screen.py) :


4 cards :
├── 📝 Énoncé   → titre accent bleu + texte principal
├── ✅ Correction → titre accent bleu + bloc code VS Code
├── 💡 Explication → titre accent bleu + texte principal
└── 🎙️ Déroulement → titre accent bleu + texte principal

Bouton "Un autre exercice" → bouton principal pleine largeur


Écran Paramètres (settings_screen.py) :

├── Fournisseurs IA → 3 boutons
│   ├── Actif  → bouton principal
│   └── Inactif → bouton principal opacity 0.4
├── Clé API → champ masqué
└── Préférences (card) :
    ├── Toggle Dark mode ← sauvegardé dans settings.json
    ├── Langue interface → dropdown accent bleu
    └── Langue exercices → dropdown accent bleu

Bouton "Sauvegarder" → bouton principal pleine largeur



Implémentation du toggle dark/light


# Dans settings.json
{
    "api_key": "...",
    "provider": "anthropic",
    "interface_language": "english",
    "exercise_language": "english",
    "theme": "dark"    # ← "dark" par défaut
}

# Dans main.py
def apply_theme(page, theme):
    if theme == "dark":
        page.bgcolor = "#1a1a2e"
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.bgcolor = "#f5f7fa"
        page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

# Au lancement → dark mode par défaut
theme = session.settings.get("theme", "dark")
apply_theme(page, theme)




Livrables
Tous les écrans redesignés en dark mode et light mode
Dark mode activé par défaut au lancement
Toggle dark/light fonctionnel dans les Paramètres
Choix du mode sauvegardé dans settings.json
Bloc de code style VS Code identique dans les deux modes
Interface responsive PC et mobile
Cohérence visuelle sur toutes les plateformes


Points de vigilance
Dark mode par défaut au premier lancement
Tous les textes lisibles dans les deux modes
Boutons principaux inversés selon le mode :
Dark → fond blanc, texte foncé
Light → fond foncé, texte blanc
Séparateurs et badges en accent bleu dans les deux modes
Bloc de code toujours en fond sombre #1e1e1e même en light mode
Toggle sauvegarde immédiatement dans settings.json
Changement de thème appliqué en temps réel sans redémarrage










Synthèse globale — FORPY
For Python (FORPY) est une application open source et gratuite pour apprendre Python. Plutôt que se concentrer sur un exercice long et laborieux, FORPY est conçu pour apprendre Python grâce à des mini-exercices générés par l'intelligence artificielle ; mais de manière industrielle (en volume et à grande vitesse). 
Là où certaines personnes se focalisent sur 10 exercices spécifiques et laborieux, vous en aurez certainement vu dans le même temps peut-être 80 mini-exercices différents avec cette app. C'est colossal. 
C'est ultra rapide pour comprendre l'architecture, pour être autonome pour du vibe coding dans un premier temps. Puis la répétition (et l’application) en volume des exercices sur plusieurs mois vous permettra d'être un dev chevronné dans le langage Python. 
Elle s'adresse à tous les profils, du grand débutant jusqu'au développeur confirmé qui souhaite affiner son code.
L'idée centrale est simple : l'utilisateur installe l'application sur son PC ou son mobile, renseigne sa propre clé API IA dans les paramètres, choisit son niveau et reçoit instantanément un exercice personnalisé avec sa correction détaillée. Il n'y a aucun serveur, aucun abonnement, aucune donnée envoyée ailleurs que vers le fournisseur IA de l'utilisateur lui-même. Tout fonctionne en local.
Le parcours pédagogique est structuré en six niveaux progressifs — de Noob à Expert Architecture — chacun découpé en sous-niveaux spécialisés. On y retrouve des exercices classiques, des sessions de debugging sur du code réaliste, des exercices orientés code pythonique, et des exercices ciblés sur des patterns spécifiques. Chaque sous-niveau possède son propre prompt, soigneusement rédigé pour garantir des exercices cohérents, variés et adaptés. À chaque fois que l'utilisateur demande un nouvel exercice, l'app s'assure de ne pas répéter le sujet précédent.
Côté technique, l'application est entièrement codée en Python avec le framework Flet, ce qui permet de livrer une seule application pour Windows, Linux et Android. Les exercices sont générés au format JSON et affichent quatre éléments : Un énoncé clair et simple, une correction de l'exercice avec du code Python, l'explication ligne par ligne et une description du déroulement. L'utilisateur lit l'exercice dans l'app et code sa réponse dans son éditeur habituel — VS Code ou autre. L'app n'est pas un IDE, c'est un générateur de contenu pédagogique.
Le projet est pensé dès le départ pour être évolutif. La structure permet d'ajouter facilement de nouveaux domaines comme Python pour le Machine Learning ou Python pour l'IA, sans réécrire le code existant. C'est aussi un projet communautaire — le code source complet est disponible sur GitHub, et n'importe qui peut contribuer en ajoutant de nouveaux prompts ou de nouveaux niveaux.
La distribution est volontairement simple : un site web propose le téléchargement direct de l'application selon la plateforme, et redirige vers GitHub pour ceux qui souhaitent accéder au code source. Aucun hébergement coûteux, aucune infrastructure à maintenir.

Stack technique : Python + Flet Plateformes MVP : Windows, Linux, Android Fournisseurs IA supportés : Anthropic (Claude), OpenAI, Google (Gemini), toute API compatible OpenAI Langues : Anglais par défaut — extensible via translations.json Distribution : GitHub Releases + site web dédié Modèle : Open source, gratuit, clé API utilisateur


"






