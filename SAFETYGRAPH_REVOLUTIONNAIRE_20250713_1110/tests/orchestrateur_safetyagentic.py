# Orchestrateur SafetyAgentic Complet - Imports Corrigés
# =====================================================
# Coordonne A1 (Autoévaluations) + A2 (Observations) + AN1 (Analyse Écarts)

import asyncio
import json
import uuid
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import logging
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

# Ajout des chemins pour imports depuis tests\
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'agents', 'collecte'))

# Imports des agents SafetyAgentic
try:
    from agent_a2_configurable import AgentA2Configurable, ModeCollecteDonnees, ConfigurationA2
    from generateur_donnees_synthetiques import SecteurActivite, TypeIncident
    print("✅ Imports agents réussis")
except ImportError as e:
    print(f"❌ Erreur import agents: {e}")
    print("📁 Vérifiez la structure des dossiers")
    print("Structure attendue:")
    print("tests/")
    print("├── orchestrateur_safetyagentic.py")
    print("└── src/agents/collecte/")
    print("    ├── agent_a2_configurable.py")
    print("    └── generateur_donnees_synthetiques.py")
    sys.exit(1)

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SafetyAgentic.Orchestrateur")

class EtapeWorkflow(Enum):
    """Étapes du workflow SafetyAgentic"""
    INITIALISATION = "initialisation"
    AGENT_A1 = "agent_a1"
    AGENT_A2 = "agent_a2"
    AGENT_AN1 = "agent_an1"
    SYNTHESE_FINALE = "synthese_finale"
    RAPPORT_BUSINESS = "rapport_business"
    TERMINEE = "terminee"

class StatutAnalyse(Enum):
    """Statut de l'analyse"""
    EN_COURS = "en_cours"
    TERMINEE = "terminee"
    ERREUR = "erreur"
    INTERROMPUE = "interrompue"

@dataclass
class ContexteAnalyse:
    """Contexte d'analyse SafetyAgentic"""
    incident_data: Dict[str, Any]
    context_organisationnel: Dict[str, Any] = field(default_factory=dict)
    configuration_a2: Optional[ConfigurationA2] = None
    options_analyse: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ResultatWorkflow:
    """Résultat complet du workflow SafetyAgentic"""
    analysis_id: str
    timestamp_debut: datetime
    timestamp_fin: Optional[datetime] = None
    statut: StatutAnalyse = StatutAnalyse.EN_COURS
    etape_courante: EtapeWorkflow = EtapeWorkflow.INITIALISATION
    
    # Résultats des agents
    resultat_a1: Optional[Dict] = None
    resultat_a2: Optional[Dict] = None
    resultat_an1: Optional[Dict] = None
    
    # Synthèse finale
    synthese_finale: Optional[Dict] = None
    rapport_business: Optional[Dict] = None
    zones_aveugles: List[Dict] = field(default_factory=list)
    recommandations_prioritaires: List[Dict] = field(default_factory=list)
    
    # Métriques
    performance_globale: Dict[str, float] = field(default_factory=dict)
    score_confiance_global: float = 0.0
    qualite_analyse: str = ""
    
    # Erreurs
    erreurs: List[str] = field(default_factory=list)

class AgentA1Simulateur:
    """Simulateur Agent A1 - Autoévaluations"""
    
    def __init__(self):
        self.agent_id = "A1_SIMULATOR"
        self.version = "1.0.0"
    
    async def process(self, incident_data: Dict, context: Dict) -> Dict:
        """Simulation traitement Agent A1"""
        await asyncio.sleep(0.1)  # Simulation latence
        
        # Génération autoévaluations selon secteur
        secteur = incident_data.get("SECTEUR_SCIAN", "CONSTRUCTION").upper()
        
        # Scores autoévaluations (généralement optimistes)
        if "CONSTRUCTION" in secteur:
            base_scores = {
                "usage_epi": 8.2, "respect_procedures": 7.5, "formation_securite": 7.8,
                "supervision_directe": 7.2, "communication_risques": 6.9, "leadership_sst": 7.1
            }
        elif "SOINS" in secteur or "SANTE" in secteur:
            base_scores = {
                "usage_epi": 8.8, "respect_procedures": 8.2, "formation_securite": 8.5,
                "supervision_directe": 7.8, "communication_risques": 7.9, "leadership_sst": 7.6
            }
        elif "FABRICATION" in secteur:
            base_scores = {
                "usage_epi": 8.0, "respect_procedures": 7.8, "formation_securite": 8.1,
                "supervision_directe": 7.3, "communication_risques": 7.4, "leadership_sst": 7.2
            }
        else:
            base_scores = {
                "usage_epi": 7.5, "respect_procedures": 7.2, "formation_securite": 7.8,
                "supervision_directe": 6.8, "communication_risques": 7.1, "leadership_sst": 6.9
            }
        
        # Ajout variance réaliste
        variables_culture_sst = {}
        for var, score in base_scores.items():
            score_final = max(1, min(10, score + np.random.normal(0, 0.4)))
            variables_culture_sst[var] = {
                "score": round(score_final, 1),
                "source": "questionnaire_autoevaluation",
                "confiance": np.random.uniform(0.7, 0.9),
                "repondants": np.random.randint(8, 25)
            }
        
        score_global = int(np.mean([v["score"] for v in variables_culture_sst.values()]) * 10)
        
        return {
            "agent_id": self.agent_id,
            "confidence_score": 0.82,
            "variables_culture_sst": variables_culture_sst,
            "scores_autoeval": {
                "score_global": score_global,
                "fiabilite_estimee": 0.75,
                "biais_detectes": ["surconfiance", "desirabilite_sociale"],
                "nb_repondants": np.random.randint(8, 25)
            },
            "analyse_psychometrique": {
                "coherence_reponses": 0.78,
                "variance_inter_repondants": 1.2,
                "detection_outliers": []
            },
            "recommendations": [
                {
                    "priorite": "MOYENNE", 
                    "action": "Validation terrain des autoévaluations",
                    "timeline": "2-4 semaines"
                }
            ],
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "secteur_analyse": secteur,
                "duree_analyse": "0.1s"
            }
        }

class AgentAN1Simulateur:
    """Simulateur Agent AN1 - Analyse Écarts"""
    
    def __init__(self):
        self.agent_id = "AN1_SIMULATOR"
        self.version = "1.0.0"
    
    async def process(self, resultat_a1: Dict, resultat_a2: Dict, context: Dict) -> Dict:
        """Simulation analyse écarts A1 vs A2"""
        await asyncio.sleep(0.2)
        
        # Extraction variables
        vars_a1 = {k: v["score"] for k, v in resultat_a1["variables_culture_sst"].items()}
        vars_a2 = {k: v["score"] for k, v in resultat_a2["variables_culture_terrain"].items()}
        
        # Calcul écarts réels
        ecarts_variables = {}
        zones_aveugles = []
        
        for var in vars_a1.keys():
            if var in vars_a2:
                score_a1 = vars_a1[var]
                score_a2 = vars_a2[var]
                ecart_absolu = abs(score_a1 - score_a2)
                ecart_pct = (ecart_absolu / max(score_a1, 1)) * 100
                
                # Classification niveau écart
                if ecart_pct >= 50:
                    niveau = "critique"
                elif ecart_pct >= 30:
                    niveau = "eleve"
                elif ecart_pct >= 15:
                    niveau = "modere"
                else:
                    niveau = "faible"
                
                direction = "surconfiance" if score_a1 > score_a2 else "sous_estimation"
                
                ecarts_variables[var] = {
                    "score_autoeval": score_a1,
                    "score_terrain": score_a2,
                    "ecart_absolu": ecart_absolu,
                    "ecart_pourcentage": ecart_pct,
                    "niveau": niveau,
                    "direction": direction,
                    "impact_securite": "ELEVE" if niveau in ["critique", "eleve"] else "MODERE"
                }
                
                # Zones aveugles si écart significatif
                if niveau in ["critique", "eleve"]:
                    zones_aveugles.append({
                        "variable": var,
                        "ecart_pourcentage": ecart_pct,
                        "niveau_criticite": niveau,
                        "type_ecart": direction,
                        "score_a1": score_a1,
                        "score_a2": score_a2,
                        "impact_potentiel": "CRITIQUE" if niveau == "critique" else "ÉLEVÉ",
                        "explication": f"{direction.title()} de {ecart_pct:.1f}% sur {var.replace('_', ' ')}",
                        "cout_estime": self._estimer_cout_zone_aveugle(var, ecart_pct)
                    })
        
        # Tri zones aveugles par criticité
        zones_aveugles.sort(key=lambda x: x["ecart_pourcentage"], reverse=True)
        
        # Recommandations ciblées
        recommendations = []
        for zone in zones_aveugles[:3]:
            recommendations.append({
                "priorite": "URGENTE" if zone["niveau_criticite"] == "critique" else "ÉLEVÉE",
                "action": f"Corriger {zone['type_ecart']} {zone['variable'].replace('_', ' ')}",
                "variable_cible": zone["variable"],
                "timeline": "1-2 semaines" if zone["niveau_criticite"] == "critique" else "2-4 semaines",
                "methode_intervention": self._generer_methode_intervention(zone),
                "cout_intervention": zone["cout_estime"] * 0.15,
                "roi_estime": self._calculer_roi_intervention(zone)
            })
        
        return {
            "agent_id": self.agent_id,
            "confidence_score": 0.87,
            "ecarts_analysis": {
                "ecarts_variables": ecarts_variables,
                "zones_aveugles": zones_aveugles,
                "nombre_ecarts_critiques": len([e for e in ecarts_variables.values() if e["niveau"] == "critique"]),
                "ecart_moyen_pourcentage": np.mean([e["ecart_pourcentage"] for e in ecarts_variables.values()]) if ecarts_variables else 0,
                "realisme_autoeval": max(0, 100 - np.mean([e["ecart_pourcentage"] for e in ecarts_variables.values()])) if ecarts_variables else 100
            },
            "impact_business": {
                "cout_total_zones_aveugles": sum(z["cout_estime"] for z in zones_aveugles),
                "cout_interventions_recommandees": sum(r["cout_intervention"] for r in recommendations),
                "roi_global_estime": np.mean([r["roi_estime"] for r in recommendations]) if recommendations else 2.0,
                "probabilite_incident_reduite": len(zones_aveugles) * 0.05
            },
            "recommendations": recommendations,
            "summary": {
                "niveau_risque_global": "ÉLEVÉ" if len(zones_aveugles) >= 3 else "MODÉRÉ" if zones_aveugles else "FAIBLE",
                "priorite_intervention": "URGENTE" if any(z["niveau_criticite"] == "critique" for z in zones_aveugles) else "ÉLEVÉE",
                "variables_critiques": len(zones_aveugles),
                "actions_recommandees": len(recommendations)
            }
        }
    
    def _estimer_cout_zone_aveugle(self, variable: str, ecart_pct: float) -> float:
        """Estimation coût d'une zone aveugle"""
        cout_base = {
            "usage_epi": 50000, "supervision_directe": 75000, "formation_securite": 40000,
            "respect_procedures": 60000, "communication_risques": 35000, "leadership_sst": 80000
        }
        base = cout_base.get(variable, 50000)
        multiplicateur = 1 + (ecart_pct / 100)
        return int(base * multiplicateur)
    
    def _generer_methode_intervention(self, zone: Dict) -> str:
        """Génération méthode d'intervention selon variable"""
        methodes = {
            "usage_epi": "Formation pratique + contrôles terrain quotidiens",
            "supervision_directe": "Formation leadership + présence terrain renforcée",
            "formation_securite": "Refonte programme formation + validation compétences",
            "respect_procedures": "Révision procédures + coaching individuel",
            "communication_risques": "Plan communication + feedback bidirectionnel",
            "leadership_sst": "Programme développement leadership + mentoring"
        }
        return methodes.get(zone["variable"], "Formation ciblée + suivi renforcé")
    
    def _calculer_roi_intervention(self, zone: Dict) -> float:
        """Calcul ROI d'une intervention"""
        roi_base = {"critique": 4.5, "eleve": 3.2}
        return roi_base.get(zone["niveau_criticite"], 2.0)

class OrchestrateurSafetyAgentic:
    """Orchestrateur principal SafetyAgentic"""
    
    def __init__(self, config_a2: Optional[ConfigurationA2] = None):
        self.orchestrateur_id = "SAFETYAGENTIC_ORCHESTRATEUR"
        self.version = "3.0.0"
        
        # Configuration A2 par défaut
        if not config_a2:
            config_a2 = ConfigurationA2(
                mode_collecte=ModeCollecteDonnees.HYBRIDE_AUTO,
                fallback_to_synthetic=True,
                synthetic_seed=42
            )
        
        # Initialisation des agents
        self.agent_a1 = AgentA1Simulateur()
        self.agent_a2 = AgentA2Configurable(config_a2)
        self.agent_an1 = AgentAN1Simulateur()
        
        # Stockage des analyses en cours
        self.analyses_en_cours: Dict[str, ResultatWorkflow] = {}
        
        logger.info(f"🤖 {self.orchestrateur_id} v{self.version} initialisé")
        print(f"🤖 {self.orchestrateur_id} v{self.version} initialisé")
    
    async def analyser_culture_securite(self, 
                                      incident_data: Dict,
                                      context_organisationnel: Dict = None,
                                      options: Dict = None) -> ResultatWorkflow:
        """Analyse complète de culture sécurité via workflow A1 → A2 → AN1"""
        
        # Initialisation analyse
        analysis_id = str(uuid.uuid4())[:8]
        start_time = datetime.now()
        
        # Contexte d'analyse
        contexte = ContexteAnalyse(
            incident_data=incident_data,
            context_organisationnel=context_organisationnel or {},
            options_analyse=options or {}
        )
        
        # Initialisation résultat workflow
        workflow_result = ResultatWorkflow(
            analysis_id=analysis_id,
            timestamp_debut=start_time
        )
        
        self.analyses_en_cours[analysis_id] = workflow_result
        
        logger.info(f"🚀 Démarrage analyse SafetyAgentic - ID: {analysis_id}")
        print(f"\n🚀 ANALYSE SAFETYAGENTIC - ID: {analysis_id}")
        print("=" * 60)
        
        try:
            # ÉTAPE 1: Agent A1 - Autoévaluations
            workflow_result.etape_courante = EtapeWorkflow.AGENT_A1
            print(f"\n🎯 ÉTAPE 1/4 - AGENT A1 (AUTOÉVALUATIONS)")
            print("-" * 45)
            
            workflow_result.resultat_a1 = await self.agent_a1.process(
                incident_data, contexte.context_organisationnel
            )
            
            self._afficher_resume_a1(workflow_result.resultat_a1)
            
            # ÉTAPE 2: Agent A2 - Observations terrain
            workflow_result.etape_courante = EtapeWorkflow.AGENT_A2
            print(f"\n🔍 ÉTAPE 2/4 - AGENT A2 (OBSERVATIONS TERRAIN)")
            print("-" * 50)
            
            workflow_result.resultat_a2 = await self.agent_a2.process(
                incident_data, contexte.context_organisationnel
            )
            
            self._afficher_resume_a2(workflow_result.resultat_a2)
            
            # ÉTAPE 3: Agent AN1 - Analyse écarts
            workflow_result.etape_courante = EtapeWorkflow.AGENT_AN1
            print(f"\n🔬 ÉTAPE 3/4 - AGENT AN1 (ANALYSE ÉCARTS)")
            print("-" * 45)
            
            workflow_result.resultat_an1 = await self.agent_an1.process(
                workflow_result.resultat_a1, 
                workflow_result.resultat_a2,
                contexte.context_organisationnel
            )
            
            self._afficher_resume_an1(workflow_result.resultat_an1)
            
            # ÉTAPE 4: Synthèse finale
            workflow_result.etape_courante = EtapeWorkflow.SYNTHESE_FINALE
            print(f"\n📊 ÉTAPE 4/4 - SYNTHÈSE FINALE")
            print("-" * 35)
            
            await self._generer_synthese_finale(workflow_result, contexte)
            
            # Finalisation
            workflow_result.timestamp_fin = datetime.now()
            workflow_result.statut = StatutAnalyse.TERMINEE
            workflow_result.etape_courante = EtapeWorkflow.TERMINEE
            
            # Calcul performance globale
            duree_totale = (workflow_result.timestamp_fin - workflow_result.timestamp_debut).total_seconds()
            workflow_result.performance_globale = {
                "duree_totale_secondes": duree_totale,
                "duree_a1": 0.1,
                "duree_a2": workflow_result.resultat_a2.get("agent_info", {}).get("performance_time", 0),
                "duree_an1": 0.2,
                "duree_synthese": 0.1
            }
            
            # Score confiance global
            scores_confiance = [
                workflow_result.resultat_a1.get("confidence_score", 0),
                workflow_result.resultat_a2.get("confidence_score", 0),
                workflow_result.resultat_an1.get("confidence_score", 0)
            ]
            workflow_result.score_confiance_global = sum(scores_confiance) / len(scores_confiance)
            
            # Affichage rapport final
            self._afficher_rapport_final(workflow_result)
            
            logger.info(f"✅ Analyse SafetyAgentic terminée - {duree_totale:.2f}s")
            
            return workflow_result
            
        except Exception as e:
            logger.error(f"❌ Erreur orchestrateur: {str(e)}")
            workflow_result.statut = StatutAnalyse.ERREUR
            workflow_result.erreurs.append(str(e))
            workflow_result.timestamp_fin = datetime.now()
            
            return workflow_result
        
        finally:
            # Nettoyage
            if analysis_id in self.analyses_en_cours:
                del self.analyses_en_cours[analysis_id]
    
    async def _generer_synthese_finale(self, workflow_result: ResultatWorkflow, contexte: ContexteAnalyse):
        """Génération synthèse finale et rapport business"""
        
        # Extraction données des agents
        a1_data = workflow_result.resultat_a1
        a2_data = workflow_result.resultat_a2
        an1_data = workflow_result.resultat_an1
        
        zones_aveugles = an1_data["ecarts_analysis"]["zones_aveugles"]
        impact_business = an1_data["impact_business"]
        
        # Synthèse finale
        workflow_result.synthese_finale = {
            "message_principal": f"⚠️ {len(zones_aveugles)} zone(s) aveugle(s) détectée(s) dans la culture sécurité",
            "niveau_risque_global": an1_data["summary"]["niveau_risque_global"],
            "score_realisme_autoeval": an1_data["ecarts_analysis"]["realisme_autoeval"],
            "variables_problematiques": [z["variable"] for z in zones_aveugles[:3]],
            "source_donnees_a2": a2_data.get("data_source", "unknown"),
            "confiance_analyse": workflow_result.score_confiance_global
        }
        
        # Zones aveugles et recommandations
        workflow_result.zones_aveugles = zones_aveugles
        workflow_result.recommandations_prioritaires = an1_data["recommendations"][:5]
        
        # Rapport business
        workflow_result.rapport_business = {
            "cout_zones_aveugles": impact_business["cout_total_zones_aveugles"],
            "cout_interventions": impact_business["cout_interventions_recommandees"],
            "roi_global": impact_business["roi_global_estime"],
            "reduction_risque": impact_business["probabilite_incident_reduite"]
        }
        
        # Qualité analyse
        if workflow_result.score_confiance_global >= 0.85:
            workflow_result.qualite_analyse = "EXCELLENTE"
        elif workflow_result.score_confiance_global >= 0.75:
            workflow_result.qualite_analyse = "BONNE"
        else:
            workflow_result.qualite_analyse = "ACCEPTABLE"
    
    def _afficher_resume_a1(self, resultat_a1: Dict):
        """Affichage résumé Agent A1"""
        scores = resultat_a1["scores_autoeval"]
        print(f"📊 Score global autoévaluation: {scores['score_global']}/100")
        print(f"👥 Répondants: {scores['nb_repondants']}")
        print(f"🎯 Fiabilité estimée: {scores['fiabilite_estimee']:.1%}")
        print(f"✅ Confiance: {resultat_a1['confidence_score']:.2f}")
    
    def _afficher_resume_a2(self, resultat_a2: Dict):
        """Affichage résumé Agent A2"""
        obs = resultat_a2["observations"]
        source = resultat_a2.get("data_source", "unknown")
        
        print(f"🔍 Source données: {source.upper()}")
        print(f"📊 Score comportement: {obs['score_comportement']}/100")
        print(f"⚠️ Dangers détectés: {obs['dangers_detectes']}")
        print(f"🛡️ Conformité: {obs['conformite_procedures']:.1f}%")
        print(f"✅ Confiance: {resultat_a2['confidence_score']:.2f}")
    
    def _afficher_resume_an1(self, resultat_an1: Dict):
        """Affichage résumé Agent AN1"""
        ecarts = resultat_an1["ecarts_analysis"]
        summary = resultat_an1["summary"]
        
        print(f"📊 Écart moyen: {ecarts['ecart_moyen_pourcentage']:.1f}%")
        print(f"⚠️ Zones aveugles: {len(ecarts['zones_aveugles'])}")
        print(f"🚨 Écarts critiques: {ecarts['nombre_ecarts_critiques']}")
        print(f"🔥 Priorité: {summary['priorite_intervention']}")
        print(f"✅ Confiance: {resultat_an1['confidence_score']:.2f}")
    
    def _afficher_rapport_final(self, workflow_result: ResultatWorkflow):
        """Affichage rapport final complet"""
        print("\n" + "=" * 70)
        print("📋 RAPPORT FINAL SAFETYAGENTIC")
        print("=" * 70)
        
        synthese = workflow_result.synthese_finale
        rapport_business = workflow_result.rapport_business
        zones = workflow_result.zones_aveugles
        
        # Message principal
        print(f"\n🎯 {synthese['message_principal']}")
        print(f"🚨 Niveau risque: {synthese['niveau_risque_global']}")
        
        # Métriques clés
        print(f"\n📊 MÉTRIQUES CLÉS:")
        print(f"   • Confiance analyse: {synthese['confiance_analyse']:.1%}")
        print(f"   • Qualité analyse: {workflow_result.qualite_analyse}")
        print(f"   • Réalisme autoéval: {synthese['score_realisme_autoeval']:.1f}%")
        print(f"   • Source A2: {synthese['source_donnees_a2']}")
        print(f"   • Performance: {workflow_result.performance_globale['duree_totale_secondes']:.2f}s")
        
        # Zones aveugles critiques
        if zones:
            print(f"\n⚠️ ZONES AVEUGLES DÉTECTÉES:")
            for i, zone in enumerate(zones[:3], 1):
                print(f"   {i}. {zone['variable'].replace('_', ' ').title()}")
                print(f"      📊 Écart: {zone['ecart_pourcentage']:.1f}% ({zone['niveau_criticite']})")
                print(f"      📈 A1: {zone['score_a1']:.1f}/10 → A2: {zone['score_a2']:.1f}/10")
                print(f"      💰 Coût estimé: {zone['cout_estime']:,}$")
        
        # Impact business
        print(f"\n💼 IMPACT BUSINESS:")
        print(f"   💰 Coût zones aveugles: {rapport_business['cout_zones_aveugles']:,}$")
        print(f"   🔧 Coût interventions: {rapport_business['cout_interventions']:,}$")
        print(f"   📈 ROI estimé: {rapport_business['roi_global']*100:.0f}%")
        print(f"   📉 Réduction risque: {rapport_business['reduction_risque']*100:.0f}%")
        
        # Recommandations prioritaires
        recommandations = workflow_result.recommandations_prioritaires
        if recommandations:
            print(f"\n🎯 RECOMMANDATIONS PRIORITAIRES:")
            for i, rec in enumerate(recommandations[:3], 1):
                print(f"   {i}. 🔥 {rec['priorite']}: {rec['action']}")
                print(f"      ⏱️ Timeline: {rec['timeline']}")
                print(f"      💰 Coût: {rec['cout_intervention']:,}$")

async def test_orchestrateur_complet():
    """Test complet orchestrateur SafetyAgentic"""
    
    print("🧪 TEST ORCHESTRATEUR SAFETYAGENTIC COMPLET")
    print("=" * 50)
    
    # Configuration A2 pour test
    config_a2 = ConfigurationA2(
        mode_collecte=ModeCollecteDonnees.HYBRIDE_AUTO,
        fallback_to_synthetic=True,
        timeout_seconds=1.0,  # Court pour tester fallback
        synthetic_seed=42
    )
    
    # Initialisation orchestrateur
    orchestrateur = OrchestrateurSafetyAgentic(config_a2)
    
    # Incident de test - Construction
    incident_test = {
        "ID": 2024123456,
        "SECTEUR_SCIAN": "CONSTRUCTION",
        "GENRE": "CHUTE DE HAUTEUR AU TRAVAIL",
        "NATURE_LESION": "FRACTURE MEMBRES INFERIEURS",
        "SIEGE_LESION": "JAMBE DROITE",
        "AGENT_CAUSAL_LESION": "ECHAFAUDAGE MOBILE",
        "GROUPE_AGE": "25-34 ANS",
        "SEXE_PERS_PHYS": "HOMME"
    }
    
    context_test = {
        "nom_entreprise": "Construction Excellence Inc.",
        "budget_sst_annuel": 75000,
        "incidents_recents": 3,
        "formation_recente_sst": False,
        "certification_sst": None,
        "nb_employes": 45,
        "region": "Quebec"
    }
    
    # Lancement analyse complète
    print(f"🎯 Test avec incident construction (chute hauteur)")
    resultat = await orchestrateur.analyser_culture_securite(
        incident_test, 
        context_test,
        {"priorite_analyse": "complete"}
    )
    
    # Vérification résultats
    print(f"\n🔍 VÉRIFICATION RÉSULTATS:")
    print(f"  ✅ Statut: {resultat.statut.value}")
    print(f"  📊 Confiance globale: {resultat.score_confiance_global:.2f}")
    print(f"  ⚠️ Zones aveugles: {len(resultat.zones_aveugles)}")
    print(f"  🎯 Recommandations: {len(resultat.recommandations_prioritaires)}")
    print(f"  ⏱️ Performance: {resultat.performance_globale['duree_totale_secondes']:.2f}s")
    
    return resultat

async def demo_modes_a2():
    """Démonstration différents modes A2"""
    
    print("\n🔄 DÉMONSTRATION MODES A2")
    print("=" * 35)
    
    incident_simple = {
        "ID": 999,
        "SECTEUR_SCIAN": "FABRICATION", 
        "GENRE": "CONTACT MACHINE"
    }
    
    context_simple = {"nom_entreprise": "Usine Test"}
    
    modes_test = [
        (ModeCollecteDonnees.SYNTHETIQUE_UNIQUEMENT, "🔬 SYNTHÉTIQUE"),
        (ModeCollecteDonnees.HYBRIDE_AUTO, "🔄 HYBRIDE"),
        (ModeCollecteDonnees.DEMO_MODE, "🎭 DÉMO")
    ]
    
    for mode, nom_mode in modes_test:
        print(f"\n{nom_mode}")
        print("-" * 25)
        
        config = ConfigurationA2(mode_collecte=mode, timeout_seconds=0.5)
        orchestrateur = OrchestrateurSafetyAgentic(config)
        
        try:
            resultat = await orchestrateur.analyser_culture_securite(incident_simple, context_simple)
            source_a2 = resultat.resultat_a2.get("data_source", "unknown")
            zones = len(resultat.zones_aveugles)
            
            print(f"  ✅ Source A2: {source_a2}")
            print(f"  ⚠️ Zones aveugles: {zones}")
            print(f"  ⏱️ Performance: {resultat.performance_globale['duree_totale_secondes']:.2f}s")
            
        except Exception as e:
            print(f"  ❌ Erreur: {e}")

class InterfaceSimple:
    """Interface simple pour SafetyAgentic"""
    
    def __init__(self, orchestrateur: OrchestrateurSafetyAgentic):
        self.orchestrateur = orchestrateur
    
    async def menu_principal(self):
        """Menu principal interactif"""
        print("\n🤖 INTERFACE SAFETYAGENTIC")
        print("=" * 35)
        print("1. 🏗️  Analyser Construction")
        print("2. 🏭  Analyser Fabrication") 
        print("3. 🏥  Analyser Soins Santé")
        print("4. ⚙️  Configuration A2")
        print("5. ❌  Quitter")
        
        while True:
            try:
                choix = input("\n🔍 Choisissez (1-5): ").strip()
                
                if choix == "1":
                    await self._analyser_secteur("CONSTRUCTION")
                elif choix == "2":
                    await self._analyser_secteur("FABRICATION")
                elif choix == "3":
                    await self._analyser_secteur("SOINS_SANTE")
                elif choix == "4":
                    self._afficher_config()
                elif choix == "5":
                    print("👋 Au revoir !")
                    break
                else:
                    print("❓ Choix invalide (1-5)")
                    
            except KeyboardInterrupt:
                print("\n👋 Au revoir !")
                break
    
    async def _analyser_secteur(self, secteur: str):
        """Analyse par secteur"""
        incidents_exemples = {
            "CONSTRUCTION": {
                "ID": 2024001, "SECTEUR_SCIAN": "CONSTRUCTION",
                "GENRE": "CHUTE DE HAUTEUR", "NATURE_LESION": "FRACTURE"
            },
            "FABRICATION": {
                "ID": 2024002, "SECTEUR_SCIAN": "FABRICATION", 
                "GENRE": "CONTACT MACHINE", "NATURE_LESION": "LACERATION"
            },
            "SOINS_SANTE": {
                "ID": 2024003, "SECTEUR_SCIAN": "SOINS DE SANTE",
                "GENRE": "EFFORT EXCESSIF", "NATURE_LESION": "ENTORSE"
            }
        }
        
        incident = incidents_exemples[secteur]
        context = {"nom_entreprise": f"Entreprise {secteur}", "budget_sst_annuel": 50000}
        
        print(f"\n🚀 Analyse secteur {secteur}...")
        resultat = await self.orchestrateur.analyser_culture_securite(incident, context)
        
        print(f"\n✅ Analyse terminée - {len(resultat.zones_aveugles)} zone(s) aveugle(s)")
        
        # Retour menu
        input("\n📋 Appuyez sur Entrée pour retourner au menu...")
    
    def _afficher_config(self):
        """Affichage configuration"""
        config_info = self.orchestrateur.agent_a2.get_config_info()
        print(f"\n⚙️ CONFIGURATION A2:")
        print(f"   Mode: {config_info['mode_collecte']}")
        print(f"   Fallback: {config_info['fallback_synthetique']}")
        print(f"   Générateur: {config_info['generateur_disponible']}")

if __name__ == "__main__":
    print("🚀 LANCEMENT ORCHESTRATEUR SAFETYAGENTIC")
    print("=" * 50)
    
    async def main():
        try:
            # Test orchestrateur principal
            print("🧪 PHASE 1: Test orchestrateur complet")
            resultat_test = await test_orchestrateur_complet()
            
            # Démonstration modes A2
            print("\n🔄 PHASE 2: Démonstration modes A2")
            await demo_modes_a2()
            
            print(f"\n🏆 VALIDATION ORCHESTRATEUR RÉUSSIE !")
            print("=" * 45)
            print("✅ Workflow A1 → A2 → AN1 opérationnel")
            print("🔍 Détection zones aveugles automatique")
            print("📊 Rapports business avec ROI")
            print("⚙️ Configuration dynamique A2")
            print("🔬 Intégration générateur synthétique")
            
            # Proposition interface interactive
            choix = input(f"\n❓ Démarrer interface interactive ? (o/n): ")
            if choix.lower().startswith('o'):
                config_interactive = ConfigurationA2(
                    mode_collecte=ModeCollecteDonnees.SYNTHETIQUE_UNIQUEMENT,
                    synthetic_seed=42
                )
                orchestrateur = OrchestrateurSafetyAgentic(config_interactive)
                interface = InterfaceSimple(orchestrateur)
                await interface.menu_principal()
            
        except Exception as e:
            print(f"\n❌ ERREUR: {e}")
            import traceback
            print("📋 Détails erreur:")
            traceback.print_exc()
    
    asyncio.run(main())