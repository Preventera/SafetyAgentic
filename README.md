# SafeGraph - Prototype Culture Sécurité

Système multi-agent d'analyse et d'amélioration de la culture sécurité basé sur LangGraph.

## 🎯 Objectif

Démontrer l'orchestration d'agents spécialisés pour :
- Évaluer les comportements sécurité
- Analyser les risques sectoriels 
- Générer des recommandations personnalisées
- Suivre les progrès

## 🏗️ Architecture

- **Router Agent** : Classification des intentions
- **Context Agent** : Enrichissement contexte SCIAN
- **Collecteur Agent** : Collecte autoévaluations
- **Analyste Agent** : Analyse risques et écarts
- **Recommandation Agent** : Plans d'action personnalisés

## 🚀 Installation

```bash
# Cloner le projet
git clone https://github.com/Preventera/SafeGraph.git
cd SafeGraph

# Installer dépendances
pip install -r requirements.txt

# Configurer environnement
cp .env.template .env
# Éditer .env avec vos clés API