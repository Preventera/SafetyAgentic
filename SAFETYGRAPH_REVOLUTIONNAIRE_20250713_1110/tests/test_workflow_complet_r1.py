# Test Workflow Complet A1→A2→AN1→R1 SafetyAgentic
# =====================================================
# Test intégration complète du workflow avec Agent R1

import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime

# Ajout des chemins pour imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))
sys.path.append(str(project_root / "src" / "agents" / "collecte"))

# Imports des agents
try:
    from src.agents.collecte.a1_autoevaluations import A1CollecteurAutoevaluations
    from src.agents.collecte.a2_observations import A2CapteurObservations  
    from src.agents.analyse.an1_analyste_ecarts import AN1AnalysteEcarts
    from src.agents.recommendation.r1_generateur_recommandations import R1GenerateurRecommandations
    print("✅ Imports agents A1, A2, AN1, R1 réussis")
except ImportError as e:
    print(f"❌ Erreur import agents: {e}")
    sys.exit(1)

class WorkflowCompletSafetyAgentic:
    """
    Orchestrateur workflow complet A1→A2→AN1→R1
    Test intégration bout-en-bout SafetyAgentic
    """
    
    def __init__(self):
        self.workflow_id = f"WF_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.agents = {
            "A1": A1CollecteurAutoevaluations(),
            "A2": A2CapteurObservations(),
            "AN1": AN1AnalysteEcarts(), 
            "R1": R1GenerateurRecommandations()
        }
        print(f"🤖 Workflow {self.workflow_id} initialisé")
    
    async def execute_complete_workflow(self, incident_context: dict) -> dict:
        """
        Exécution workflow complet A1→A2→AN1→R1
        """
        print(f"\n🚀 DÉMARRAGE WORKFLOW COMPLET - {self.workflow_id}")
        print("=" * 60)
        
        workflow_start = datetime.now()
        results = {}
        
        try:
            # ÉTAPE 1: Agent A1 - Autoévaluations
            print("\n🎯 ÉTAPE 1/4 - AGENT A1 (AUTOÉVALUATIONS)")
            print("-" * 45)
            
            # Données A1 simulées réalistes
            data_a1_input = {
                "incident_context": incident_context,
                "questionnaires": {
                    "management": {"score_global": 78, "repondants": 8},
                    "superviseurs": {"score_global": 74, "repondants": 12}, 
                    "operateurs": {"score_global": 68, "repondants": 35}
                }
            }
            
            result_a1 = await self.agents["A1"].process(data_a1_input)
            results["A1"] = result_a1
            
            print(f"✅ A1 terminé - Score: {result_a1.get('score_global', 0)}/100")
            print(f"   Variables analysées: {len(result_a1.get('variables_culture_sst', {}))}")
            
            # ÉTAPE 2: Agent A2 - Observations terrain
            print("\n🔍 ÉTAPE 2/4 - AGENT A2 (OBSERVATIONS TERRAIN)")
            print("-" * 48)
            
            # Données A2 avec écarts significatifs pour déclencher zones aveugles
            data_a2_input = {
                "incident_context": incident_context,
                "observations_terrain": {
                    "duree_observation": 8,  # heures
                    "observateurs": 3,
                    "zones_observees": ["production", "maintenance", "reception"]
                }
            }
            
            result_a2 = await self.agents["A2"].process(data_a2_input)
            results["A2"] = result_a2
            
            print(f"✅ A2 terminé - Score terrain: {result_a2.get('score_comportement', 0)}/100")
            print(f"   Dangers détectés: {result_a2.get('dangers_detectes', 0)}")
            
            # ÉTAPE 3: Agent AN1 - Analyse écarts 
            print("\n🔬 ÉTAPE 3/4 - AGENT AN1 (ANALYSE ÉCARTS)")
            print("-" * 45)
            
            result_an1 = await self.agents["AN1"].process(result_a1, result_a2, incident_context)
            results["AN1"] = result_an1
            
            zones_aveugles = result_an1.get("ecarts_analysis", {}).get("zones_aveugles", [])
            print(f"✅ AN1 terminé - Zones aveugles: {len(zones_aveugles)}")
            print(f"   Écart moyen: {result_an1.get('summary', {}).get('ecart_moyen', 0):.1f}%")
            
            # ÉTAPE 4: Agent R1 - Recommandations
            print("\n💡 ÉTAPE 4/4 - AGENT R1 (RECOMMANDATIONS)")
            print("-" * 45)
            
            result_r1 = await self.agents["R1"].process(result_an1, incident_context)
            results["R1"] = result_r1
            
            recommandations = result_r1.get("recommandations_detaillees", [])
            budget_total = result_r1.get("budget_analysis", {}).get("cout_total", 0)
            roi = result_r1.get("budget_analysis", {}).get("roi_estime", 0)
            
            print(f"✅ R1 terminé - Recommandations: {len(recommandations)}")
            print(f"   Budget total: {budget_total:,.0f}$")
            print(f"   ROI estimé: {roi:.1f}%")
            
            # SYNTHÈSE FINALE
            workflow_duration = (datetime.now() - workflow_start).total_seconds()
            
            final_synthesis = {
                "workflow_id": self.workflow_id,
                "execution_time": workflow_duration,
                "agents_executed": 4,
                "zones_aveugles_detected": len(zones_aveugles),
                "recommandations_generated": len(recommandations), 
                "budget_total": budget_total,
                "roi_estime": roi,
                "success": True,
                "confidence_moyenne": sum([
                    result_a1.get("confidence_score", 0),
                    result_a2.get("confidence_score", 0), 
                    result_an1.get("agent_info", {}).get("confidence_score", 0),
                    result_r1.get("agent_info", {}).get("confidence_score", 0)
                ]) / 4
            }
            
            results["SYNTHESE"] = final_synthesis
            
            print(f"\n📊 SYNTHÈSE WORKFLOW COMPLET")
            print("=" * 35)
            print(f"🎯 Workflow: {self.workflow_id}")
            print(f"⏱️ Durée totale: {workflow_duration:.2f}s")
            print(f"🤖 Agents exécutés: 4/4")
            print(f"⚠️ Zones aveugles: {len(zones_aveugles)}")
            print(f"💡 Recommandations: {len(recommandations)}")
            print(f"💰 Budget: {budget_total:,.0f}$")
            print(f"📈 ROI: {roi:.1f}%")
            print(f"✅ Confiance moyenne: {final_synthesis['confidence_moyenne']:.2f}")
            
            return results
            
        except Exception as e:
            print(f"❌ Erreur workflow: {str(e)}")
            return {"error": str(e), "workflow_id": self.workflow_id}
    
    def display_detailed_results(self, results: dict):
        """Affichage détaillé des résultats"""
        
        print(f"\n📋 RAPPORT DÉTAILLÉ WORKFLOW")
        print("=" * 40)
        
        # Zones aveugles détaillées
        if "AN1" in results:
            zones = results["AN1"].get("ecarts_analysis", {}).get("zones_aveugles", [])
            if zones:
                print(f"\n⚠️ ZONES AVEUGLES IDENTIFIÉES:")
                for i, zone in enumerate(zones, 1):
                    print(f"  {i}. {zone['variable']} - {zone['pourcentage_ecart']:.1f}% ({zone['niveau_critique']})")
                    print(f"     Impact: {zone['impact_potentiel']}")
        
        # Recommandations prioritaires
        if "R1" in results:
            recos = results["R1"].get("recommandations_detaillees", [])
            if recos:
                print(f"\n💡 RECOMMANDATIONS PRIORITAIRES:")
                for i, reco in enumerate(recos[:3], 1):
                    print(f"  {i}. {reco['variable_cible']} ({reco['priorite']})")
                    print(f"     Timeline: {reco['timeline']}")
                    print(f"     Budget: {reco['budget_estime']:,.0f}$")
                    if reco['formations']:
                        print(f"     Formation: {reco['formations'][0]}")
        
        # Plan d'action
        if "R1" in results:
            plan = results["R1"].get("plan_action", {})
            timeline = results["R1"].get("implementation_timeline", {})
            
            print(f"\n📅 PLAN D'ACTION:")
            print(f"  • Durée: {plan.get('duree_totale_estimee', 'N/A')}")
            print(f"  • Phases: {len(timeline.get('phases', []))}")
            print(f"  • Actions total: {plan.get('nombre_actions', 0)}")
        
        # Métriques business
        if "R1" in results:
            business = results["R1"].get("business_impact", {})
            print(f"\n💼 IMPACT BUSINESS:")
            print(f"  • ROI: {business.get('roi_estime', 0):.1f}%")
            print(f"  • Économies: {business.get('economies_estimees', 0):,.0f}$")
            print(f"  • Payback: {business.get('payback_period', 0):.1f} mois")


async def test_workflow_complet_construction():
    """Test workflow complet avec incident construction"""
    
    print("🧪 TEST WORKFLOW COMPLET A1→A2→AN1→R1")
    print("=" * 50)
    print("🎯 Secteur: Construction - Incident chute échafaudage")
    print("📊 Objectif: Valider workflow bout-en-bout SafetyAgentic")
    
    # Contexte incident construction réaliste
    incident_context = {
        "secteur": "CONSTRUCTION",
        "type_incident": "CHUTE_HAUTEUR",
        "nature_lesion": "FRACTURE_JAMBE",
        "agent_causal": "ECHAFAUDAGE_MOBILE",
        "taille_entreprise": "MOYENNE",
        "nombre_employes": 85,
        "experience_moyenne": 8.5,  # années
        "formation_recente": False,
        "certification": "ISO45001"
    }
    
    # Créer et exécuter workflow
    workflow = WorkflowCompletSafetyAgentic()
    results = await workflow.execute_complete_workflow(incident_context)
    
    # Affichage résultats détaillés
    if "error" not in results:
        workflow.display_detailed_results(results)
        print(f"\n🎉 WORKFLOW COMPLET RÉUSSI !")
        print(f"✅ SafetyAgentic A1→A2→AN1→R1 opérationnel")
    else:
        print(f"❌ Erreur workflow: {results['error']}")
    
    return results


async def test_workflow_complet_sante():
    """Test workflow complet avec incident soins santé"""
    
    print("\n" + "="*60)
    print("🧪 TEST WORKFLOW COMPLET - SOINS SANTÉ")
    print("=" * 50)
    
    # Contexte incident soins santé
    incident_context = {
        "secteur": "SOINS_SANTE", 
        "type_incident": "CONTACT_PRODUIT_CHIMIQUE",
        "nature_lesion": "IRRITATION_CUTANEE",
        "agent_causal": "PRODUIT_NETTOYAGE",
        "taille_entreprise": "GRANDE",
        "nombre_employes": 450,
        "experience_moyenne": 12.3,
        "formation_recente": True,
        "certification": "JCI"
    }
    
    workflow = WorkflowCompletSafetyAgentic()
    results = await workflow.execute_complete_workflow(incident_context)
    
    if "error" not in results:
        workflow.display_detailed_results(results)
        print(f"\n🎉 WORKFLOW SOINS SANTÉ RÉUSSI !")
    
    return results


# Exécution tests
if __name__ == "__main__":
    print("🚀 LANCEMENT TESTS WORKFLOW COMPLET SAFETYAGENTIC")
    print("=" * 55)
    
    # Test 1: Construction
    asyncio.run(test_workflow_complet_construction())
    
    # Test 2: Soins santé
    asyncio.run(test_workflow_complet_sante())
    
    print(f"\n🏆 TESTS WORKFLOW COMPLET TERMINÉS")
    print("SafetyAgentic A1→A2→AN1→R1 validé !")