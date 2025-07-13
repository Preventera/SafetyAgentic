# 🚀 **GUIDE DÉPLOIEMENT SAFETYGRAPH - INTÉGRATION CNESST**
## Implémentation Code Fonctionnel Complète

**Nom de Code:** IMPLEMENTATION ✅ **TERMINÉE**  
**Date:** 11 juillet 2025  
**Auteur:** Mario Genest - GenAISafety  

---

## **📁 1. FICHIERS GÉNÉRÉS**

### **🎯 Modules Principaux**

| **Fichier** | **Description** | **Taille Est.** | **Statut** |
|-------------|-----------------|-----------------|------------|
| `app_cnesst_dashboard.py` | Module expert administration 104 agents | ~15 KB | ✅ Généré |
| `behaviorx_enrichments.py` | Enrichissements workflow VCS→ABC | ~12 KB | ✅ Généré |
| `cnesst_config.json` | Configuration système complète | ~3 KB | ✅ Généré |
| `guide_deploiement_final.md` | Instructions déploiement | ~8 KB | ✅ Généré |

### **📂 Structure Fichiers Recommandée**

```
SafeGraph/
├── app_behaviorx.py (EXISTANT - À modifier)
├── app_cnesst_dashboard.py (NOUVEAU)
├── data/
│   ├── lesions-2017.csv à lesions-2023.csv (EXISTANT)
│   ├── safetyagentic_behaviorx.db (EXISTANT - 20 KB)
│   ├── cnesst_cache.db (À créer automatiquement)
│   └── cnesst_config.json (NOUVEAU)
├── src/
│   ├── enrichments/
│   │   └── behaviorx_enrichments.py (NOUVEAU)
│   ├── agents/ (EXISTANT)
│   ├── analytics/ (EXISTANT)
│   └── langgraph/ (EXISTANT)
└── logs/ (Auto-créé)
```

---

## **⚡ 2. DÉPLOIEMENT IMMÉDIAT (30 MINUTES)**

### **🔧 ÉTAPE 2.1: Préparation Fichiers (5 minutes)**

```bash
# 1. Navigation vers projet
cd "C:\Users\Mario\Documents\PROJECTS_NEW\SafeGraph"

# 2. Backup sécurité app_behaviorx.py existant
copy app_behaviorx.py app_behaviorx_BACKUP_$(Get-Date -Format "yyyyMMdd_HHmm").py

# 3. Création structure enrichments
mkdir src\enrichments 2>$null

# 4. Création fichier configuration
# Copier le contenu de cnesst_config.json dans: data\cnesst_config.json
```

### **🔧 ÉTAPE 2.2: Installation Modules (10 minutes)**

```bash
# 1. Copier app_cnesst_dashboard.py à la racine du projet
# Copier le code généré dans: app_cnesst_dashboard.py

# 2. Copier behaviorx_enrichments.py 
# Copier le code généré dans: src\enrichments\behaviorx_enrichments.py

# 3. Vérification imports requis
pip install streamlit pandas plotly sqlite3 json datetime typing logging pathlib
```

### **🔧 ÉTAPE 2.3: Modification app_behaviorx.py (10 minutes)**

**Modifications minimales à apporter à votre app_behaviorx.py existant :**

```python
# =====