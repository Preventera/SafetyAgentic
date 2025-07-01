# SafetyAgentic
> **Multi-Agent Safety Intelligence Platform**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-green.svg)](https://github.com/langchain-ai/langgraph)
[![Claude 4](https://img.shields.io/badge/Claude%204-Sonnet-purple.svg)](https://www.anthropic.com/)

## 🎯 Vision

SafetyAgentic révolutionne l'analyse de culture sécurité en combinant **100 agents spécialisés** avec l'intelligence artificielle de pointe. Notre plateforme transforme des données complexes de sécurité en recommandations actionnables et personnalisées.

## 🧠 Intelligence Agentique

### Architecture Multi-Agent
- **100 agents spécialisés** organisés en 5 phases critiques
- **Orchestration LangGraph** pour coordination intelligente
- **Claude 4 Sonnet** comme moteur d'intelligence principal
- **Analyse prédictive** basée sur 793K+ incidents réels

### Phases d'Analyse
```
Collecte → Normalisation → Analyse → Recommandation → Suivi
   ↓           ↓            ↓           ↓            ↓
A1-A10     N1-N10      AN1-AN10     R1-R10      S1-S10
   ↓           ↓            ↓           ↓            ↓
        Agents Sectoriels SC1-SC50 (spécialisés SCIAN)
```

## 🏗️ Fonctionnalités Clés

### 🔍 Analyse Conversationnelle
- **Interface en langage naturel** pour interroger vos données SST
- **Compréhension contextuelle** des enjeux sectoriels
- **Visualisations dynamiques** des risques et tendances

### 🤖 Agents Spécialisés
- **Collecteur d'Auto-évaluations** (A1) : Questionnaires comportementaux
- **Analyste Prédictif** (AN2) : Modélisation probabilité incidents
- **Générateur de Recommandations** (R1) : Plans d'action personnalisés
- **Coach Sécurité** (R3) : Accompagnement terrain et formation
- **Détecteur de Signaux Faibles** (AN3) : Identification tendances émergentes

### 📊 Safe Graph Relationnel
- **Graphe causale** liant incidents → variables culture → actions
- **Modèles d'analyse** : Reason, INRS, STEP
- **Variables culture SST** : 100 déterminants clés trackés
- **Recommandations ciblées** par secteur SCIAN

## 🏭 Secteurs Supportés

| Secteur SCIAN | Description | Agents Spécialisés |
|---------------|-------------|-------------------|
| **236** | Construction | Analyse chutes, EPI, échafaudages |
| **484** | Transport routier | Fatigue, conduite, maintenance |
| **622** | Santé | Ergonomie, infections, stress |
| **811** | Maintenance industrielle | Machines, lockout, espaces confinés |
| **561** | Sécurité privée | Surveillance, agressions, patrouilles |

## 🚀 Installation Rapide

### Prérequis
```bash
Python 3.9+
Git
Docker (optionnel)
```

### Setup
```bash
# Cloner le repository
git clone https://github.com/Preventera/SafetyAgentic.git
cd SafetyAgentic

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.template .env
# Éditer .env avec vos clés API
```

### Configuration API
```bash
# Dans .env
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_fallback_key
LANGCHAIN_TRACING_V2=true
SAFETYAGENTIC_DEBUG=true
```

## 🎮 Utilisation

### Démarrage Rapide
```bash
# Lancer l'interface principal
python main.py

# Ou démarrer en mode développement
python app.py --debug

# Tests du prototype
python test_prototype.py
```

### Exemple d'Interaction
```python
from src.core.graph import create_safety_graph
from src.core.state import create_initial_state

# Créer une session d'analyse
graph = create_safety_graph()
state = create_initial_state(
    user_input="Analyse les chutes d'échafaudage dans la construction",
    sector="236"  # Construction
)

# Exécuter l'analyse multi-agent
result = graph.invoke(state)
print(result['recommendations'])
```

## 📈 Données et Performance

### Volume de Données
- **793 737 lésions** analysées (2017-2023)
- **100 scénarios** de référence par secteur
- **100 variables** culture SST trackées
- **10 modèles** prédictifs sectoriels

### Métriques de Performance
- ⚡ **< 30 secondes** par analyse complète
- 🎯 **> 85%** précision des recommandations
- 📊 **> 100 analyses/heure** en mode batch
- 🔄 **99%** disponibilité système

## 🔬 Méthodologie Scientifique

### Modèles d'Analyse Intégrés
- **Modèle de Reason** : Défaillances actives vs latentes
- **Arbre des causes INRS** : Événements déclencheurs à organisationnels
- **Modèle STEP** : Séquences temporelles d'événements

### Module STORM
- **Recherche automatisée** de littérature scientifique
- **Validation croisée** avec bases de données HSE
- **Citations et références** pour chaque recommandation

## 🛠️ Architecture Technique

### Stack Principal
```
Frontend: Streamlit / React
Backend: FastAPI + LangGraph
LLM: Claude 4 Sonnet (Anthropic)
Base de données: PostgreSQL + Neo4j
Cache: Redis
Infrastructure: Docker + AWS/Azure
```

### Structure du Projet
```
SafetyAgentic/
├── src/
│   ├── agents/           # 100 agents spécialisés
│   │   ├── evaluation/   # A1-A10 (Collecte)
│   │   ├── analysis/     # AN1-AN10 (Analyse)
│   │   ├── recommendation/ # R1-R10 (Recommandations)
│   │   └── sectorial/    # SC1-SC50 (Spécialisés SCIAN)
│   ├── core/            # LangGraph orchestration
│   ├── utils/           # Utilitaires système
│   └── storm_research/  # Module recherche STORM
├── training_data/       # Datasets d'entraînement
├── tests/              # Tests unitaires
└── docs/               # Documentation
```

## 📚 Cas d'Usage

### 1. Analyse d'Incident
```
Input: "Charpentier chute échafaudage - fracture bras"
↓
Agents activés: A1→AN4→R1→SC1 (Construction)
↓
Output: 5 causes identifiées + 8 actions correctives SMART
```

### 2. Prédiction Risques
```
Input: "Équipe transport - fatigue augmentée"
↓
Agents activés: AN2→AN3→R1→SC2 (Transport)
↓
Output: Probabilité incident +15% + plan préventif 30 jours
```

### 3. Amélioration Continue
```
Input: Données TMS secteur santé
↓
Agents activés: AN5→R2→R6→SC3 (Santé)
↓
Output: Programme ergonomie personnalisé + formation ciblée
```

## 🎓 Formation et Support

### Documentation
- [Guide Utilisateur](docs/user-guide.md)
- [API Reference](docs/api-reference.md)
- [Architecture Technique](docs/architecture.md)
- [Cas d'Usage Sectoriels](docs/use-cases.md)

### Support Communauté
- 💬 [Discussions GitHub](https://github.com/Preventera/SafetyAgentic/discussions)
- 📧 Support: contact@preventera.ai
- 🎓 Formation: training@preventera.ai

## 🗺️ Roadmap

### Version 1.0 (Q2 2025)
- [x] Architecture multi-agent complète
- [x] 100 agents spécialisés opérationnels
- [ ] Interface conversationnelle avancée
- [ ] Module STORM intégré
- [ ] 5 secteurs SCIAN supportés

### Version 2.0 (Q4 2025)
- [ ] 20 secteurs SCIAN supportés
- [ ] API publique disponible
- [ ] Intégrations ERP (SAP, Oracle)
- [ ] Mobile app iOS/Android
- [ ] Analyses temps réel IoT

### Vision 2026+
- [ ] Réseau agentique distribué
- [ ] IA prédictive avancée
- [ ] Réalité augmentée terrain
- [ ] Standard international SafetyAgentic

## 👥 Équipe

**Développé par Preventera & GenAISafety**
- Intelligence Artificielle appliquée à la HSE
- 25+ années d'expertise en prévention
- Standards éthiques C-25
- Recherche & développement continu

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez notre [Guide de Contribution](CONTRIBUTING.md) pour commencer.

### Processus de Contribution
1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 🔗 Liens Utiles

- **Website**: [www.preventera.ai](https://www.preventera.ai)
- **Documentation**: [docs.safetyagentic.ai](https://docs.safetyagentic.ai)
- **Demo Live**: [demo.safetyagentic.ai](https://demo.safetyagentic.ai)
- **Blog Technique**: [blog.preventera.ai](https://blog.preventera.ai)

---

<div align="center">

**SafetyAgentic** - Où l'Intelligence Artificielle Rencontre l'Excellence en Sécurité

*Développé avec ❤️ par l'équipe Preventera*

</div>