# Script Vérification Environnement SafetyAgentic
# ===============================================
# Vérification complète avant connexion réelle aux données

import os
import sys
from pathlib import Path
import importlib.util
import pandas as pd

class VerificationSafetyAgentic:
    def __init__(self):
        self.score_total = 0
        self.score_max = 100
        self.resultats = {}
        
    def afficher_header(self):
        print("=" * 60)
        print("🔍 VÉRIFICATION ENVIRONNEMENT SAFETYAGENTIC")
        print("=" * 60)
        print(f"📁 Répertoire actuel: {os.getcwd()}")
        print(f"🐍 Version Python: {sys.version}")
        print("-" * 60)
    
    def verifier_structure_dossiers(self):
        print("\n📂 VÉRIFICATION STRUCTURE DOSSIERS")
        print("-" * 40)
        
        dossiers_requis = [
            "src",
            "src/agents", 
            "src/agents/collecte",
            "src/agents/analyse",
            "src/agents/recommendation",
            "data",
            "tests"
        ]
        
        score_dossiers = 0
        for dossier in dossiers_requis:
            if os.path.exists(dossier):
                print(f"  ✅ {dossier}")
                score_dossiers += 10
            else:
                print(f"  ❌ {dossier} - MANQUANT")
        
        self.resultats['dossiers'] = score_dossiers
        self.score_total += min(score_dossiers, 20)  # Max 20 points
        
    def verifier_agents_existants(self):
        print("\n🤖 VÉRIFICATION AGENTS SAFETYAGENTIC")
        print("-" * 40)
        
        agents_requis = {
            "A1": "src/agents/collecte/a1_autoevaluations.py",
            "A2": "src/agents/collecte/a2_observations.py", 
            "AN1": "src/agents/analyse/analyste_agent.py",
            "R1": "src/agents/recommendation/r1_generateur_recommandations.py"
        }
        
        score_agents = 0
        for nom_agent, chemin in agents_requis.items():
            if os.path.exists(chemin):
                print(f"  ✅ Agent {nom_agent}: {chemin}")
                score_agents += 15
            else:
                # Vérifier variantes de noms
                dossier = os.path.dirname(chemin)
                if os.path.exists(dossier):
                    fichiers = [f for f in os.listdir(dossier) if f.endswith('.py')]
                    print(f"  🔍 Agent {nom_agent}: Recherche dans {dossier}")
                    print(f"      Fichiers trouvés: {fichiers}")
                    if fichiers:
                        score_agents += 10  # Points partiels
                else:
                    print(f"  ❌ Agent {nom_agent}: {chemin} - MANQUANT")
        
        self.resultats['agents'] = score_agents
        self.score_total += min(score_agents, 30)  # Max 30 points
        
    def verifier_donnees_cnesst(self):
        print("\n📊 VÉRIFICATION DONNÉES CNESST")
        print("-" * 40)
        
        fichiers_cnesst = [
            "data/lesions-2017 (1).csv",
            "data/lesions-2018 (1).csv", 
            "data/lesions-2019.csv",
            "data/lesions-2020 (1).csv",
            "data/lesions-2021 (1).csv",
            "data/lesions-2022 (1).csv",
            "data/lesions-2023 (1).csv"
        ]
        
        score_donnees = 0
        total_lignes = 0
        
        for fichier in fichiers_cnesst:
            if os.path.exists(fichier):
                try:
                    df = pd.read_csv(fichier)
                    lignes = len(df)
                    total_lignes += lignes
                    print(f"  ✅ {fichier}: {lignes:,} lignes")
                    score_donnees += 10
                except Exception as e:
                    print(f"  ⚠️ {fichier}: Erreur lecture - {e}")
                    score_donnees += 5
            else:
                print(f"  ❌ {fichier}: MANQUANT")
        
        print(f"\n📈 Total incidents CNESST: {total_lignes:,}")
        
        self.resultats['donnees'] = score_donnees
        self.resultats['total_incidents'] = total_lignes
        self.score_total += min(score_donnees, 25)  # Max 25 points
        
    def verifier_dependances(self):
        print("\n📦 VÉRIFICATION DÉPENDANCES PYTHON")
        print("-" * 40)
        
        dependances_requises = [
            'pandas',
            'numpy', 
            'scikit-learn',
            'matplotlib',
            'seaborn',
            'asyncio',
            'json',
            'datetime'
        ]
        
        score_deps = 0
        for dep in dependances_requises:
            try:
                if dep in ['asyncio', 'json', 'datetime']:
                    # Modules built-in
                    __import__(dep)
                    print(f"  ✅ {dep} (built-in)")
                else:
                    __import__(dep)
                    print(f"  ✅ {dep}")
                score_deps += 5
            except ImportError:
                print(f"  ❌ {dep} - NON INSTALLÉ")
        
        self.resultats['dependances'] = score_deps
        self.score_total += min(score_deps, 15)  # Max 15 points
        
    def verifier_orchestrateur(self):
        print("\n🎛️ VÉRIFICATION ORCHESTRATEUR")
        print("-" * 40)
        
        fichiers_orchestrateur = [
            "tests/orchestrateur_safetyagentic.py",
            "src/orchestrateur_safetyagentic.py",
            "orchestrateur_safetyagentic.py"
        ]
        
        score_orch = 0
        for fichier in fichiers_orchestrateur:
            if os.path.exists(fichier):
                print(f"  ✅ Orchestrateur trouvé: {fichier}")
                score_orch = 10
                break
        
        if score_orch == 0:
            print("  ❌ Orchestrateur principal non trouvé")
        
        self.resultats['orchestrateur'] = score_orch
        self.score_total += score_orch  # Max 10 points
        
    def generer_rapport_final(self):
        print("\n" + "=" * 60)
        print("📋 RAPPORT DE VÉRIFICATION FINAL")
        print("=" * 60)
        
        print(f"\n📊 SCORE GLOBAL: {self.score_total}/{self.score_max}")
        
        # Détail des scores
        print("\n🔍 DÉTAIL PAR COMPOSANT:")
        print(f"  📂 Structure dossiers: {min(self.resultats.get('dossiers', 0), 20)}/20")
        print(f"  🤖 Agents SafetyAgentic: {min(self.resultats.get('agents', 0), 30)}/30") 
        print(f"  📊 Données CNESST: {min(self.resultats.get('donnees', 0), 25)}/25")
        print(f"  📦 Dépendances Python: {min(self.resultats.get('dependances', 0), 15)}/15")
        print(f"  🎛️ Orchestrateur: {self.resultats.get('orchestrateur', 0)}/10")
        
        # Recommandations
        print("\n🎯 STATUT:")
        if self.score_total >= 80:
            print("  ✅ EXCELLENT - Prêt pour connexion réelle!")
        elif self.score_total >= 60:
            print("  ⚠️ ACCEPTABLE - Quelques ajustements recommandés")
        else:
            print("  ❌ CRITIQUE - Corrections nécessaires avant de continuer")
            
        # Actions recommandées
        print("\n📋 ACTIONS RECOMMANDÉES:")
        if self.resultats.get('dossiers', 0) < 60:
            print("  🔧 Créer la structure de dossiers manquante")
        if self.resultats.get('agents', 0) < 40:
            print("  🤖 Vérifier/installer les agents SafetyAgentic")
        if self.resultats.get('donnees', 0) < 50:
            print("  📊 Vérifier l'accès aux données CNESST")
        if self.resultats.get('dependances', 0) < 30:
            print("  📦 Installer les dépendances manquantes: pip install pandas numpy scikit-learn matplotlib seaborn")
            
        return self.score_total >= 60
    
    def executer_verification_complete(self):
        self.afficher_header()
        self.verifier_structure_dossiers()
        self.verifier_agents_existants()
        self.verifier_donnees_cnesst()
        self.verifier_dependances()
        self.verifier_orchestrateur()
        return self.generer_rapport_final()

if __name__ == "__main__":
    print("🔍 Démarrage vérification environnement SafetyAgentic...")
    
    verificateur = VerificationSafetyAgentic()
    succes = verificateur.executer_verification_complete()
    
    if succes:
        print("\n🎉 Environnement validé ! Prêt pour l'étape suivante.")
        exit(0)
    else:
        print("\n⚠️ Corrections nécessaires avant de continuer.")
        exit(1)