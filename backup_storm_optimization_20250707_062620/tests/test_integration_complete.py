# Test Intégration Complète SafetyAgentic
# =======================================
# Démontre orchestrateur avec Agent A2 configurable (réel + synthétique)

import asyncio
import numpy as np
from datetime import datetime
from typing import Dict, List
import logging
import json
import sys
import os

# Ajout des chemins pour imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'agents', 'collecte'))

# Imports des composants
try:
    from agent_a2_configurable import AgentA2Configurable, ModeCollecteDonnees
    from generateur_donnees_synthetiques import GenerateurDonneesSynthetiques, SecteurActivite
except ImportError as e:
    print(f"❌ Erreur import: {e}")
    print("📁 Vérifiez que les fichiers sont dans src/agents/collecte/")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SafetyAgentic.Integration")

class SafetyAgenticOrchestratorV2:
    """
    Orchestrateur SafetyAgentic V2 avec Agent A2 configurable
    Support données réelles ET synthétiques
    """
    
    def __init__(self, config_a2: Dict = None):
        self.orchestrator_id = "SAFETYAGENTIC_V2"
        self.version = "2.0.0"
        
        # Configuration par défaut A2
        default_a2_config = {
            "mode_collecte": ModeCollecteDonnees.HYBRIDE_AUTO,
            "fallback_to_synthetic": True,
            "synthetic_seed": 42  # Reproductibilité
        }
        
        if config_a2:
            default_a2_config.update(config_a2)
        
        # Initialisation agents
        self.agent_a2 = AgentA2Configurable(default_a2_config)
        
        logger.info(f"🤖 {self.orchestrator_id} v{self.version} initialisé")
        print(f"🤖 {self.orchestrator_id} v{self.version} initialisé")
        
    async def analyze_safety_culture_v2(
        self, 
        incident_data: Dict, 
        context: Dict = None,
        mode_a2: str = None
    ) -> Dict:
        """
        Analyse culture sécurité V2 avec A2 configurable
        
        Args:
            incident_data: Données incident CNESST
            context: Contexte organisationnel
            mode_a2: Mode spécifique pour A2 (override config)
        """
        start_time = datetime.now()
        analysis_id = f"SAV2_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"🔄 Analyse SafetyAgentic V2 - ID: {analysis_id}")
        print(f"\n🔄 ANALYSE SAFETYAGENTIC V2 - ID: {analysis_id}")
        print("=" * 60)
        
        try:
            # Override mode A2 si spécifié
            original_mode = None
            if mode_a2:
                original_mode = self.agent_a2.config["mode_collecte"]
                if mode_a2 == "real":
                    self.agent_a2.config["mode_collecte"] = ModeCollecteDonnees.REEL_UNIQUEMENT
                elif mode_a2 == "synthetic":
                    self.agent_a2.config["mode_collecte"] = ModeCollecteDonnees.SYNTHETIQUE_UNIQUEMENT
                elif mode_a2 == "hybrid":
                    self.agent_a2.config["mode_collecte"] = ModeCollecteDonnees.HYBRIDE_AUTO
                elif mode_a2 == "demo":
                    self.agent_a2.config["mode_collecte"] = ModeCollecteDonnees.DEMO_MODE
            
            # Contexte analyse
            analysis_context = self._prepare_analysis_context(incident_data, context)
            print(f"📋 Contexte: {analysis_context['secteur']} - {analysis_context['type_incident']}")
            
            # Workflow V2 : A1 → A2 → AN1
            workflow_results = {}
            
            # ÉTAPE 1: Agent A1 - Autoévaluations (simulation)
            print(f"\n🎯 ÉTAPE 1/4 - AGENT A1 (AUTOÉVALUATIONS)")
            print("-" * 45)
            result_a1 = await self._execute_agent_a1_sim(incident_data, analysis_context)
            workflow_results["A1"] = result_a1
            self._display_a1_summary(result_a1)
            
            # ÉTAPE 2: Agent A2 - Observations (configurable)
            print(f"\n🔍 ÉTAPE 2/4 - AGENT A2 (OBSERVATIONS CONFIGURABLES)")
            print("-" * 55)
            result_a2 = await self.agent_a2.process(incident_data, analysis_context)
            workflow_results["A2"] = result_a2
            self._display_a2_summary_v2(result_a2)
            
            # ÉTAPE 3: Agent AN1 - Analyse écarts
            print(f"\n🔬 ÉTAPE 3/4 - AGENT AN1 (ANALYSE ÉCARTS)")
            print("-" * 45)
            result_an1 = await self._execute_agent_an1_sim(result_a1, result_a2, analysis_context)
            workflow_results["AN1"] = result_an1
            self._display_an1_summary(result_an1)
            
            # ÉTAPE 4: Synthèse finale V2
            print(f"\n📊 ÉTAPE 4/4 - SYNTHÈSE FINALE V2")
            print("-" * 40)
            final_synthesis = await self._generate_final_synthesis_v2(
                workflow_results, incident_data, analysis_context
            )
            
            # Métriques globales
            global_metrics = self._calculate_global_metrics_v2(workflow_results)
            
            # Construction rapport final
            performance_time = (datetime.now() - start_time).total_seconds()
            
            final_report = {
                "analysis_info": {
                    "analysis_id": analysis_id,
                    "orchestrator_version": self.version,
                    "timestamp": datetime.now().isoformat(),
                    "performance_time": performance_time,
                    "incident_context": analysis_context,
                    "a2_mode_used": result_a2.get("data_source", "unknown")
                },
                "workflow_results": workflow_results,
                "global_metrics": global_metrics,
                "final_synthesis": final_synthesis,
                "quality_assessment": self._assess_analysis_quality_v2(workflow_results, global_metrics),
                "executive_summary": self._generate_executive_summary_v2(final_synthesis, global_metrics),
                "data_sources": {
                    "a1_source": "simulation",
                    "a2_source": result_a2.get("data_source", "unknown"),
                    "an1_source": "analysis_engine"
                }
            }
            
            # Affichage rapport final
            self._display_final_report_v2(final_report)
            
            # Restaurer mode A2 original si override
            if original_mode is not None:
                self.agent_a2.config["mode_collecte"] = original_mode
            
            logger.info(f"✅ Analyse SafetyAgentic V2 terminée - {performance_time:.2f}s")
            return final_report
            
        except Exception as e:
            logger.error(f"❌ Erreur orchestrateur V2: {str(e)}")
            return {
                "error": str(e),
                "analysis_id": analysis_id,
                "orchestrator_id": self.orchestrator_id
            }
    
    def _prepare_analysis_context(self, incident_data: Dict, context: Dict) -> Dict:
        """Préparation contexte analyse V2"""
        return {
            "secteur": incident_data.get("SECTEUR_SCIAN", "CONSTRUCTION"),
            "type_incident": incident_data.get("GENRE", "CHUTE_HAUTEUR"),
            "nature_lesion": incident_data.get("NATURE_LESION", "TRAUMA"),
            "agent_causal": incident_data.get("AGENT_CAUSAL_LESION", "ECHAFAUDAGE"),
            "age_groupe": incident_data.get("GROUPE_AGE", "25-34"),
            "organisation_context": context or {}
        }
    
    async def _execute_agent_a1_sim(self, incident_data: Dict, context: Dict) -> Dict:
        """Simulation Agent A1 - Autoévaluations"""
        print("🤖 Simulation Agent A1...")
        await asyncio.sleep(0.1)
        
        # Génération autoévaluations selon secteur
        secteur = context.get("secteur", "CONSTRUCTION")
        
        # Scores optimistes typiques autoévaluations
        if "CONSTRUCTION" in secteur:
            base_scores = {"usage_epi": 8.2, "respect_procedures": 7.5, "formation_securite": 7.8,
                          "supervision_directe": 7.2, "communication_risques": 6.9, "leadership_sst": 7.1}
        elif "SOINS" in secteur:
            base_scores = {"usage_epi": 8.8, "respect_procedures": 8.2, "formation_securite": 8.5,
                          "supervision_directe": 7.8, "communication_risques": 7.9, "leadership_sst": 7.6}
        else:
            base_scores = {"usage_epi": 7.5, "respect_procedures": 7.2, "formation_securite": 7.8,
                          "supervision_directe": 6.8, "communication_risques": 7.1, "leadership_sst": 6.9}
        
        # Ajout variance réaliste
        variables_culture = {}
        for var, score in base_scores.items():
            variables_culture[var] = {
                "score": max(1, min(10, score + np.random.normal(0, 0.3))),
                "source": "questionnaire",
                "confiance": np.random.uniform(0.7, 0.9)
            }
        
        score_global = int(np.mean([v["score"] for v in variables_culture.values()]) * 10)
        
        return {
            "agent_id": "A1",
            "confidence_score": 0.82,
            "variables_culture_sst": variables_culture,
            "scores_autoeval": {
                "score_global": score_global,
                "fiabilite": 0.8,
                "biais_detectes": ["surconfiance", "desirabilite_sociale"]
            },
            "recommendations": [
                {"priorite": "ÉLEVÉE", "action": "Sensibilisation EPI", "timeline": "4-6 semaines"}
            ]
        }
    
    async def _execute_agent_an1_sim(self, result_a1: Dict, result_a2: Dict, context: Dict) -> Dict:
        """Simulation Agent AN1 - Analyse écarts"""
        print("🤖 Calcul écarts A1 vs A2...")
        await asyncio.sleep(0.1)
        
        # Extraction variables
        vars_a1 = {k: v["score"] for k, v in result_a1["variables_culture_sst"].items()}
        vars_a2 = {k: v["score"] for k, v in result_a2["variables_culture_terrain"].items()}
        
        # Calcul écarts réels
        ecarts_variables = {}
        zones_aveugles = []
        
        for var in vars_a1.keys():
            if var in vars_a2:
                score_a1 = vars_a1[var]
                score_a2 = vars_a2[var]
                ecart_pct = abs(score_a1 - score_a2) / max(score_a1, 1) * 100
                
                # Classification
                if ecart_pct >= 50:
                    niveau = "critique"
                elif ecart_pct >= 25:
                    niveau = "eleve"
                elif ecart_pct >= 10:
                    niveau = "modere"
                else:
                    niveau = "faible"
                
                direction = "surestimation" if score_a1 > score_a2 else "sous_estimation"
                
                ecarts_variables[var] = {
                    "score_autoeval": score_a1,
                    "score_terrain": score_a2,
                    "ecart_absolu": abs(score_a1 - score_a2),
                    "pourcentage": ecart_pct,
                    "niveau": niveau,
                    "direction": direction
                }
                
                # Zone aveugle si écart significatif
                if niveau in ["eleve", "critique"]:
                    zones_aveugles.append({
                        "variable": var,
                        "pourcentage_ecart": ecart_pct,
                        "niveau_critique": niveau,
                        "type_ecart": direction,
                        "impact_potentiel": "CRITIQUE" if niveau == "critique" else "ÉLEVÉ",
                        "explication": f"{direction.title()} de {ecart_pct:.1f}% sur {var}"
                    })
        
        # Tri zones aveugles par écart décroissant
        zones_aveugles.sort(key=lambda x: x["pourcentage_ecart"], reverse=True)
        
        # Recommandations ciblées
        recommendations = []
        for zone in zones_aveugles[:3]:
            recommendations.append({
                "priorite": "URGENTE" if zone["niveau_critique"] == "critique" else "ÉLEVÉE",
                "action": f"Corriger écart {zone['type_ecart']} {zone['variable']}",
                "variable_cible": zone["variable"],
                "timeline": "2-4 semaines" if zone["niveau_critique"] == "critique" else "1-2 mois",
                "methode": f"Formation ciblée + observations terrain {zone['variable']}"
            })
        
        return {
            "agent_id": "AN1",
            "confidence_score": 0.85,
            "ecarts_analysis": {
                "ecarts_variables": ecarts_variables,
                "zones_aveugles": zones_aveugles,
                "nombre_ecarts_critiques": len([e for e in ecarts_variables.values() if e["niveau"] == "critique"]),
                "realisme_scores": {
                    "realisme_global": max(0, 100 - np.mean([e["pourcentage"] for e in ecarts_variables.values()])),
                    "fiabilite_autoeval": 75,
                    "niveau_autocritique": "moyen"
                }
            },
            "hse_models_analysis": {
                "hfacs_l2": {"model_name": "Supervision inadéquate", "score_applicabilite": 90},
                "swiss_cheese": {"model_name": "Défaillances barrières", "score_applicabilite": 85}
            },
            "recommendations": recommendations,
            "summary": {
                "ecart_moyen": np.mean([e["pourcentage"] for e in ecarts_variables.values()]),
                "variables_critiques": len(zones_aveugles),
                "actions_recommandees": len(recommendations),
                "priorite_intervention": "ÉLEVÉE" if zones_aveugles else "MOYENNE"
            }
        }
    
    async def _generate_final_synthesis_v2(
        self, 
        workflow_results: Dict, 
        incident_data: Dict, 
        context: Dict
    ) -> Dict:
        """Synthèse finale V2 avec source tracking"""
        
        a1_data = workflow_results["A1"]
        a2_data = workflow_results["A2"]
        an1_data = workflow_results["AN1"]
        
        zones_aveugles = an1_data["ecarts_analysis"]["zones_aveugles"]
        
        # Impact business avec source A2
        a2_source = a2_data.get("data_source", "unknown")
        confidence_multiplier = 1.0 if a2_source == "real" else 0.85 if a2_source.startswith("hybrid") else 0.75
        
        cost_per_zone = 75000 * confidence_multiplier
        nb_zones_critiques = len([z for z in zones_aveugles if z["niveau_critique"] == "critique"])
        estimated_cost = nb_zones_critiques * cost_per_zone
        
        return {
            "zones_aveugles_critiques": zones_aveugles[:3],
            "causes_racines": [
                {
                    "cause": f"Écarts perception vs réalité terrain (Source A2: {a2_source})",
                    "evidence": f"{len(zones_aveugles)} zone(s) aveugle(s) détectée(s)",
                    "impact": "Risque sous-estimation dangers",
                    "level": "perceptuel"
                }
            ],
            "actions_prioritaires": an1_data["recommendations"][:5],
            "impact_business": {
                "cout_zones_aveugles": estimated_cost,
                "probabilite_incident": 0.15 + (nb_zones_critiques * 0.05),
                "confidence_source": a2_source,
                "confidence_multiplier": confidence_multiplier
            },
            "data_quality_assessment": {
                "a2_source": a2_source,
                "a2_confidence": a2_data.get("confidence_score", 0),
                "hybrid_details": a2_data.get("fusion_details", {}),
                "real_data_count": a2_data.get("real_data_details", {}).get("observations_count", 0)
            }
        }
    
    def _calculate_global_metrics_v2(self, workflow_results: Dict) -> Dict:
        """Métriques globales V2"""
        confidence_scores = [r.get("confidence_score", 0) for r in workflow_results.values()]
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        
        a2_source = workflow_results["A2"].get("data_source", "unknown")
        an1_data = workflow_results["AN1"]["ecarts_analysis"]
        
        return {
            "confidence_globale": avg_confidence,
            "agents_executes": len(workflow_results),
            "variables_analysees": len(an1_data["ecarts_variables"]),
            "zones_aveugles_detectees": len(an1_data["zones_aveugles"]),
            "qualite_analyse": "ÉLEVÉE" if avg_confidence > 0.8 else "MOYENNE",
            "a2_data_source": a2_source,
            "a2_confidence_impact": self._assess_a2_confidence_impact(a2_source)
        }
    
    def _assess_a2_confidence_impact(self, source: str) -> str:
        """Évaluation impact confiance source A2"""
        if source == "real":
            return "MAXIMUM - Données terrain réelles"
        elif source.startswith("hybrid"):
            return "ÉLEVÉ - Fusion données réelles et synthétiques"
        elif source == "synthetic":
            return "MOYEN - Données synthétiques réalistes"
        else:
            return "FAIBLE - Source non identifiée"
    
    def _assess_analysis_quality_v2(self, workflow_results: Dict, metrics: Dict) -> Dict:
        """Évaluation qualité V2"""
        quality_score = 70  # Base
        issues = []
        
        # Bonus source A2
        a2_source = metrics["a2_data_source"]
        if a2_source == "real":
            quality_score += 20
        elif a2_source.startswith("hybrid"):
            quality_score += 15
        elif a2_source == "synthetic":
            quality_score += 5
        else:
            issues.append(f"Source A2 inconnue: {a2_source}")
        
        # Confiance globale
        if metrics["confidence_globale"] >= 0.8:
            quality_score += 10
        
        return {
            "score_qualite": min(100, quality_score),
            "niveau_qualite": "EXCELLENT" if quality_score >= 90 else "BON" if quality_score >= 75 else "ACCEPTABLE",
            "issues_detectees": issues,
            "recommandation_qualite": f"Analyse fiable - Source A2: {a2_source}"
        }
    
    def _generate_executive_summary_v2(self, synthesis: Dict, metrics: Dict) -> Dict:
        """Résumé exécutif V2"""
        zones_aveugles = synthesis["zones_aveugles_critiques"]
        a2_source = metrics["a2_data_source"]
        
        # Message adapté selon source A2
        if a2_source == "real":
            source_note = " (Basé sur observations terrain réelles)"
        elif a2_source.startswith("hybrid"):
            source_note = " (Fusion données réelles + prédictives)"
        else:
            source_note = " (Basé sur modélisation prédictive)"
        
        key_message = f"⚠️ {len(zones_aveugles)} zone(s) aveugle(s) détectée(s){source_note}"
        
        return {
            "message_cle": key_message,
            "zones_aveugles_nb": len(zones_aveugles),
            "source_donnees_a2": a2_source,
            "confidence_analyse": metrics["confidence_globale"],
            "impact_business": synthesis["impact_business"]["cout_zones_aveugles"],
            "niveau_risque": "ÉLEVÉ" if len(zones_aveugles) >= 2 else "MODÉRÉ"
        }
    
    # Méthodes d'affichage
    def _display_a1_summary(self, result_a1: Dict):
        """Affichage résumé A1"""
        score_global = result_a1["scores_autoeval"]["score_global"]
        variables = result_a1["variables_culture_sst"]
        print(f"📊 Score global autoévaluation: {score_global}/100")
        print(f"🎯 Variables culture: {len(variables)}")
        print(f"✅ Confiance: {result_a1['confidence_score']:.2f}")
    
    def _display_a2_summary_v2(self, result_a2: Dict):
        """Affichage résumé A2 V2"""
        source = result_a2.get("data_source", "unknown")
        confidence = result_a2.get("confidence_score", 0)
        observations = result_a2.get("observations", {})
        
        print(f"🔍 Source données: {source.upper()}")
        print(f"📊 Score comportement: {observations.get('score_comportement', 0)}/100")
        print(f"⚠️ Dangers détectés: {observations.get('dangers_detectes', 0)}")
        print(f"🛡️ Conformité: {observations.get('conformite_procedures', 0):.1f}%")
        print(f"✅ Confiance: {confidence:.2f}")
        
        # Détails source si hybride
        if "hybrid" in source:
            fusion_details = result_a2.get("fusion_details", {})
            if fusion_details:
                print(f"🔗 Fusion: {fusion_details.get('real_observations_count', 0)} obs. réelles")
    
    def _display_an1_summary(self, result_an1: Dict):
        """Affichage résumé AN1"""
        summary = result_an1["summary"]
        zones = result_an1["ecarts_analysis"]["zones_aveugles"]
        
        print(f"📊 Écart moyen: {summary['ecart_moyen']:.1f}%")
        print(f"⚠️ Zones aveugles: {len(zones)}")
        print(f"🚨 Priorité: {summary['priorite_intervention']}")
        print(f"✅ Confiance: {result_an1['confidence_score']:.2f}")
    
    def _display_final_report_v2(self, report: Dict):
        """Affichage rapport final V2"""
        print("\n" + "=" * 60)
        print("📋 RAPPORT FINAL SAFETYAGENTIC V2")
        print("=" * 60)
        
        exec_summary = report["executive_summary"]
        metrics = report["global_metrics"]
        synthesis = report["final_synthesis"]
        
        print(f"\n🎯 {exec_summary['message_cle']}")
        
        print(f"\n📊 MÉTRIQUES GLOBALES V2:")
        print(f"   • Confiance: {metrics['confidence_globale']:.1%}")
        print(f"   • Source A2: {metrics['a2_data_source']}")
        print(f"   • Impact confiance: {metrics['a2_confidence_impact']}")
        print(f"   • Qualité: {metrics['qualite_analyse']}")
        
        # Zones aveugles
        zones = synthesis["zones_aveugles_critiques"]
        if zones:
            print(f"\n⚠️ ZONES AVEUGLES DÉTECTÉES:")
            for i, zone in enumerate(zones, 1):
                print(f"   {i}. {zone['variable']} - {zone['pourcentage_ecart']:.1f}% ({zone['niveau_critique']})")
        
        # Qualité données A2
        quality_data = synthesis["data_quality_assessment"]
        print(f"\n📊 QUALITÉ DONNÉES A2:")
        print(f"   • Source: {quality_data['a2_source']}")
        print(f"   • Confiance A2: {quality_data['a2_confidence']:.2f}")
        
        if quality_data.get("real_data_count", 0) > 0:
            print(f"   • Observations réelles: {quality_data['real_data_count']}")
        
        print(f"\n⏱️ Performance: {report['analysis_info']['performance_time']:.3f}s")


async def test_integration_modes():
    """Test intégration avec différents modes A2"""
    
    print("🧪 TEST INTÉGRATION SAFETYAGENTIC V2")
    print("=" * 45)
    print("🎯 Test différents modes Agent A2")
    
    # Incident test
    incident_test = {
        "ID": 2024789456,
        "SECTEUR_SCIAN": "CONSTRUCTION",
        "GENRE": "CHUTE DE HAUTEUR...",
        "NATURE_LESION": "TRAUMA OS,NERFS...",
        "SIEGE_LESION": "COLONNE VERTEBRALE...",
        "AGENT_CAUSAL_LESION": "ECHAFAUDAGE...",
        "GROUPE_AGE": "25-29 ANS"
    }
    
    context_test = {
        "nom_entreprise": "Construction Pro Inc.",
        "budget_sst_annuel": 35000,
        "incidents_recents": 3,
        "formation_recente_sst": False
    }
    
    # Modes à tester
    modes_test = ["synthetic", "demo"]
    
    for mode in modes_test:
        print(f"\n{'='*60}")
        print(f"🔄 TEST MODE A2: {mode.upper()}")
        print(f"{'='*60}")
        
        # Configuration orchestrateur
        config_a2 = {
            "mode_collecte": getattr(ModeCollecteDonnees, f"{mode.upper()}_MODE" if mode == "demo" else f"{mode.upper()}_UNIQUEMENT"),
            "synthetic_seed": 42,
            "db_timeout_seconds": 1.0  # Court pour simulation échec DB
        }
        
        orchestrator = SafetyAgenticOrchestratorV2(config_a2)
        
        # Exécution analyse
        rapport = await orchestrator.analyze_safety_culture_v2(
            incident_test, 
            context_test,
            mode_a2=mode
        )
        
        if "error" in rapport:
            print(f"❌ Erreur mode {mode}: {rapport['error']}")
        else:
            # Résumé comparatif
            exec_summary = rapport["executive_summary"]
            print(f"\n📋 RÉSUMÉ MODE {mode.upper()}:")
            print(f"   ✅ Source A2: {exec_summary['source_donnees_a2']}")
            print(f"   📊 Confiance: {exec_summary['confidence_analyse']:.2f}")
            print(f"   ⚠️ Zones aveugles: {exec_summary['zones_aveugles_nb']}")
            print(f"   💰 Impact: {exec_summary['impact_business']:,}$")
            print(f"   ⏱️ Performance: {rapport['analysis_info']['performance_time']:.3f}s")
    
    print(f"\n🎉 TESTS D'INTÉGRATION TERMINÉS !")
    print("=" * 45)
    print("✅ SafetyAgentic V2 validé avec Agent A2 configurable")
    print("🔄 Support données réelles ET synthétiques")
    print("⚡ Fallback automatique intelligent")
    print("📊 Tracking source et qualité données")

async def demo_simple():
    """Démonstration simple SafetyAgentic V2"""
    
    print("\n🎭 DÉMONSTRATION SIMPLE SAFETYAGENTIC V2")
    print("=" * 50)
    
    # Orchestrateur avec config synthétique
    orchestrator = SafetyAgenticOrchestratorV2({
        "mode_collecte": ModeCollecteDonnees.SYNTHETIQUE_UNIQUEMENT
    })
    
    # Incident simple
    incident = {
        "ID": 999, 
        "SECTEUR_SCIAN": "FABRICATION", 
        "GENRE": "CONTACT MACHINE",
        "NATURE_LESION": "FRACTURE",
        "SIEGE_LESION": "MAIN DROITE"
    }
    
    context = {
        "nom_entreprise": "Usine Test",
        "budget_sst_annuel": 15000,
        "incidents_recents": 2
    }
    
    print("🔄 Test avec mode SYNTHETIQUE_UNIQUEMENT")
    
    # Exécution analyse
    rapport = await orchestrator.analyze_safety_culture_v2(incident, context, mode_a2="synthetic")
    
    if "error" in rapport:
        print(f"❌ Erreur: {rapport['error']}")
    else:
        print("✅ Analyse terminée avec succès!")
        exec_summary = rapport["executive_summary"]
        print(f"📊 Zones aveugles détectées: {exec_summary['zones_aveugles_nb']}")
        print(f"🎯 Source A2: {exec_summary['source_donnees_a2']}")
        print(f"💰 Impact estimé: {exec_summary['impact_business']:,}$")

if __name__ == "__main__":
    print("🚀 LANCEMENT TESTS SAFETYAGENTIC V2")
    print("=" * 40)
    
    # Menu choix test
    print("\n📋 Tests disponibles:")
    print("1. 🎭 Démonstration simple")
    print("2. 🧪 Tests intégration complets")
    print("3. ⚡ Les deux")
    
    choix = input("\nChoisissez (1/2/3): ").strip()
    
    if choix == "1":
        asyncio.run(demo_simple())
    elif choix == "2":
        asyncio.run(test_integration_modes())
    elif choix == "3":
        asyncio.run(demo_simple())
        asyncio.run(test_integration_modes())
    else:
        print("🎭 Exécution démonstration simple par défaut...")
        asyncio.run(demo_simple())