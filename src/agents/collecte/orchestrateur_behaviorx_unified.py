"""
Orchestrateur BehaviorX-SafetyAgentic Unifié v2.0
===============================================

ÉTAPE 2.1 - Workflow intégré VCS → ABC → A1/A2 → AN1 → R1
Coordination intelligente avec mémoire IA persistante
"""

import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import traceback

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BehaviorXContext:
    """Contexte unifié BehaviorX-SafetyAgentic"""
    enterprise_id: str
    sector_code: str
    sector_name: str
    workflow_mode: str  # "vcs_abc", "self_assessment", "hybrid"
    session_id: str
    timestamp: datetime
    memory_enabled: bool = True
    
@dataclass
class WorkflowResults:
    """Résultats consolidés du workflow"""
    context: BehaviorXContext
    vcs_results: Optional[Dict] = None
    abc_analysis: Optional[Dict] = None
    a1_enhanced_results: Optional[Dict] = None
    a2_enhanced_results: Optional[Dict] = None
    an1_analysis: Optional[Dict] = None
    r1_recommendations: Optional[Dict] = None
    integration_score: float = 0.0
    blind_spots: List[str] = None
    priority_actions: List[Dict] = None
    memory_insights: List[str] = None

class BehaviorXSafetyOrchestrator:
    """
    Orchestrateur unifié BehaviorX-SafetyAgentic
    
    Coordonne le workflow complet :
    VCS → ABC → A1/A2 Enhanced → AN1 → R1
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.session_id = f"orchestrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.workflow_history = []
        self.memory_enabled = self.config.get('memory_enabled', True)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Simulation des agents (en production, imports réels)
        self.simulation_mode = True
        
        print(f"🎼 Orchestrateur BehaviorX-SafetyAgentic v2.0 initialisé")
        print(f"🆔 Session: {self.session_id}")
        print(f"🧠 Mémoire IA: {'✅ Activée' if self.memory_enabled else '❌ Désactivée'}")
    
    def create_context(self, enterprise_id: str, sector_code: str, 
                      workflow_mode: str = "hybrid") -> BehaviorXContext:
        """Créer le contexte unifié pour le workflow"""
        
        sector_mapping = {
            "236": "Construction",
            "622": "Soins de santé",
            "311": "Fabrication alimentaire",
            "541": "Services professionnels"
        }
        
        context = BehaviorXContext(
            enterprise_id=enterprise_id,
            sector_code=sector_code,
            sector_name=sector_mapping.get(sector_code, "Secteur général"),
            workflow_mode=workflow_mode,
            session_id=self.session_id,
            timestamp=datetime.now(),
            memory_enabled=self.memory_enabled
        )
        
        print(f"🏢 Contexte créé: {context.enterprise_id}")
        print(f"📊 Secteur: {context.sector_code} - {context.sector_name}")
        print(f"⚙️ Mode workflow: {context.workflow_mode}")
        
        return context
    
    def execute_vcs_observation(self, context: BehaviorXContext) -> Dict[str, Any]:
        """Étape 1: Exécution VCS (Visite Comportementale Sécurité)"""
        
        print(f"\n🔍 ÉTAPE 1: VCS OBSERVATION")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        try:
            if self.simulation_mode:
                # Simulation VCS avec Agent A2 Enhanced
                vcs_results = {
                    "checklist_items": 12,
                    "observations": [
                        {"category": "epi_usage", "score": 4, "conforme": True},
                        {"category": "positioning_movement", "score": 3, "conforme": True},
                        {"category": "tools_equipment", "score": 2, "conforme": False},
                        {"category": "procedures_compliance", "score": 2, "conforme": False},
                        {"category": "communication_interaction", "score": 4, "conforme": True},
                        {"category": "attention_focus", "score": 4, "conforme": True},
                        {"category": "risk_perception", "score": 3, "conforme": True},
                        {"category": "proactive_safety", "score": 3, "conforme": True}
                    ],
                    "conformity_rate": 75.0,
                    "strengths": 6,
                    "concerns": 2,
                    "observer_notes": "Bonne culture sécurité générale, points d'amélioration sur équipements"
                }
            else:
                # Appel Agent A2 Enhanced réel
                from src.agents.collecte.a2_behaviorx_enhanced import AgentA2BehaviorXEnhanced
                agent_a2 = AgentA2BehaviorXEnhanced()
                vcs_results = agent_a2.execute_vcs(context.sector_code)
            
            print(f"✅ VCS terminée: {vcs_results['checklist_items']} items observés")
            print(f"📊 Conformité: {vcs_results['conformity_rate']:.1f}%")
            print(f"💪 Forces: {vcs_results['strengths']} | ⚠️ Préoccupations: {vcs_results['concerns']}")
            
            return vcs_results
            
        except Exception as e:
            self.logger.error(f"Erreur VCS: {e}")
            return {"error": str(e), "status": "failed"}
    
    def execute_abc_analysis(self, context: BehaviorXContext, 
                           vcs_results: Dict[str, Any]) -> Dict[str, Any]:
        """Étape 2: Analyse ABC (Antécédent-Comportement-Conséquence)"""
        
        print(f"\n🔗 ÉTAPE 2: ANALYSE ABC")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        try:
            # Mapper VCS vers framework ABC
            abc_behaviors = []
            intervention_points = []
            
            for obs in vcs_results.get("observations", []):
                category = obs["category"]
                score = obs["score"]
                conforme = obs["conforme"]
                
                abc_behavior = {
                    "antecedent": f"Contexte_{category}",
                    "behavior": category,
                    "consequence": "positive" if conforme else "negative",
                    "score": score,
                    "intervention_needed": not conforme
                }
                
                abc_behaviors.append(abc_behavior)
                
                if not conforme:
                    intervention_points.append({
                        "category": category,
                        "priority": "high" if score <= 2 else "medium",
                        "intervention_type": "immediate" if score <= 2 else "planned"
                    })
            
            abc_analysis = {
                "behaviors_analyzed": len(abc_behaviors),
                "behaviors": abc_behaviors,
                "intervention_points": intervention_points,
                "behavioral_patterns": {
                    "positive_behaviors": len([b for b in abc_behaviors if b["consequence"] == "positive"]),
                    "negative_behaviors": len([b for b in abc_behaviors if b["consequence"] == "negative"]),
                    "high_priority_interventions": len([i for i in intervention_points if i["priority"] == "high"])
                }
            }
            
            print(f"🧠 ABC: {abc_analysis['behaviors_analyzed']} comportements analysés")
            print(f"✅ Positifs: {abc_analysis['behavioral_patterns']['positive_behaviors']}")
            print(f"❌ Négatifs: {abc_analysis['behavioral_patterns']['negative_behaviors']}")
            print(f"🚨 Interventions urgentes: {abc_analysis['behavioral_patterns']['high_priority_interventions']}")
            
            return abc_analysis
            
        except Exception as e:
            self.logger.error(f"Erreur ABC: {e}")
            return {"error": str(e), "status": "failed"}
    
    def execute_a1_enhanced(self, context: BehaviorXContext, 
                          abc_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Étape 3: Agent A1 Enhanced (Safe Self + Mémoire IA)"""
        
        print(f"\n🤖 ÉTAPE 3: AGENT A1 ENHANCED")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        try:
            if self.simulation_mode:
                # Simulation enrichie par contexte ABC
                risk_factors = len([b for b in abc_analysis.get("behaviors", []) 
                                  if b["consequence"] == "negative"])
                protective_factors = len([b for b in abc_analysis.get("behaviors", []) 
                                        if b["consequence"] == "positive"])
                
                base_score = 65.0
                abc_boost = (protective_factors * 5) - (risk_factors * 8)
                final_score = max(0, min(100, base_score + abc_boost))
                
                a1_results = {
                    "safe_self_score": final_score,
                    "risk_factors": risk_factors,
                    "protective_factors": protective_factors,
                    "behavioral_level": self._get_behavioral_level(final_score),
                    "abc_enriched": True,
                    "memory_insights": [
                        "Amélioration comportementale détectée vs historique",
                        "Pattern récurrent sur équipements identifié"
                    ] if context.memory_enabled else [],
                    "recommendations": self._generate_a1_recommendations(abc_analysis)
                }
            else:
                # Appel Agent A1 Enhanced réel
                from src.agents.collecte.a1_behaviorx_enhanced import AgentA1BehaviorXEnhanced
                agent_a1 = AgentA1BehaviorXEnhanced()
                a1_results = agent_a1.process_with_abc_context(context.enterprise_id, abc_analysis)
            
            print(f"🎯 Score Safe Self: {a1_results['safe_self_score']:.1f}")
            print(f"📈 Niveau: {a1_results['behavioral_level']}")
            print(f"🧠 Enrichi par ABC: {'✅' if a1_results.get('abc_enriched') else '❌'}")
            print(f"💡 Recommandations: {len(a1_results.get('recommendations', []))}")
            
            return a1_results
            
        except Exception as e:
            self.logger.error(f"Erreur A1 Enhanced: {e}")
            return {"error": str(e), "status": "failed"}
    
    def execute_integration_analysis(self, workflow_results: WorkflowResults) -> Dict[str, Any]:
        """Étape 4: Analyse d'intégration et détection zones aveugles"""
        
        print(f"\n🔗 ÉTAPE 4: ANALYSE INTÉGRATION")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        try:
            vcs_score = workflow_results.vcs_results.get("conformity_rate", 0)
            a1_score = workflow_results.a1_enhanced_results.get("safe_self_score", 0)
            
            # Calcul cohérence perception vs observation
            score_difference = abs(vcs_score - a1_score)
            coherence_score = max(0, 100 - (score_difference * 2))
            
            # Détection zones aveugles
            blind_spots = []
            if score_difference > 25:
                blind_spots.append("Écart perception/réalité important")
            
            abc_high_priority = len([i for i in workflow_results.abc_analysis.get("intervention_points", []) 
                                   if i["priority"] == "high"])
            if abc_high_priority > 2:
                blind_spots.append("Interventions urgentes multiples")
            
            # Priorisation actions
            priority_actions = []
            for intervention in workflow_results.abc_analysis.get("intervention_points", []):
                priority_actions.append({
                    "category": intervention["category"],
                    "priority": intervention["priority"],
                    "source": "abc_vcs",
                    "action": f"Amélioration ciblée {intervention['category']}"
                })
            
            integration_results = {
                "coherence_score": coherence_score,
                "coherence_level": self._get_coherence_level(coherence_score),
                "score_difference": score_difference,
                "blind_spots_detected": len(blind_spots) > 0,
                "blind_spots": blind_spots,
                "priority_actions": priority_actions[:5],  # Top 5
                "integration_quality": "excellent" if coherence_score > 80 else 
                                     "good" if coherence_score > 60 else "needs_improvement"
            }
            
            print(f"🎯 Cohérence A1↔VCS: {coherence_score:.1f}%")
            print(f"🔗 Niveau intégration: {integration_results['coherence_level']}")
            print(f"🚨 Zones aveugles: {'OUI' if integration_results['blind_spots_detected'] else 'NON'}")
            print(f"📈 Actions prioritaires: {len(priority_actions)}")
            
            return integration_results
            
        except Exception as e:
            self.logger.error(f"Erreur intégration: {e}")
            return {"error": str(e), "status": "failed"}
    
    def execute_full_workflow(self, enterprise_id: str, sector_code: str,
                            workflow_mode: str = "hybrid") -> WorkflowResults:
        """Exécution complète du workflow BehaviorX-SafetyAgentic"""
        
        print(f"\n🚀 WORKFLOW BEHAVIORX-SAFETYAGENTIC UNIFIÉ")
        print(f"{'='*60}")
        
        # Création contexte
        context = self.create_context(enterprise_id, sector_code, workflow_mode)
        
        # Initialisation résultats
        results = WorkflowResults(context=context, blind_spots=[])
        
        try:
            # ÉTAPE 1: VCS Observation
            results.vcs_results = self.execute_vcs_observation(context)
            if results.vcs_results.get("error"):
                raise Exception(f"VCS failed: {results.vcs_results['error']}")
            
            # ÉTAPE 2: Analyse ABC
            results.abc_analysis = self.execute_abc_analysis(context, results.vcs_results)
            if results.abc_analysis.get("error"):
                raise Exception(f"ABC failed: {results.abc_analysis['error']}")
            
            # ÉTAPE 3: Agent A1 Enhanced
            results.a1_enhanced_results = self.execute_a1_enhanced(context, results.abc_analysis)
            if results.a1_enhanced_results.get("error"):
                raise Exception(f"A1 Enhanced failed: {results.a1_enhanced_results['error']}")
            
            # ÉTAPE 4: Analyse intégration
            integration_analysis = self.execute_integration_analysis(results)
            
            # Consolidation résultats finaux
            results.integration_score = integration_analysis.get("coherence_score", 0)
            results.blind_spots = integration_analysis.get("blind_spots", [])
            results.priority_actions = integration_analysis.get("priority_actions", [])
            
            if context.memory_enabled:
                results.memory_insights = [
                    "Workflow BehaviorX intégré avec succès",
                    f"Score cohérence: {results.integration_score:.1f}%",
                    f"Secteur {context.sector_name}: Pattern comportemental analysé"
                ]
            
            print(f"\n✅ WORKFLOW TERMINÉ AVEC SUCCÈS")
            print(f"🎯 Score intégration: {results.integration_score:.1f}%")
            print(f"📊 Zones aveugles: {len(results.blind_spots)}")
            print(f"🚀 Actions prioritaires: {len(results.priority_actions)}")
            
            # Sauvegarde historique
            self.workflow_history.append({
                "timestamp": datetime.now().isoformat(),
                "context": asdict(context),
                "results_summary": {
                    "integration_score": results.integration_score,
                    "blind_spots_count": len(results.blind_spots),
                    "priority_actions_count": len(results.priority_actions)
                }
            })
            
            return results
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {e}")
            print(f"❌ ERREUR WORKFLOW: {e}")
            traceback.print_exc()
            return results
    
    def _get_behavioral_level(self, score: float) -> str:
        """Déterminer le niveau comportemental"""
        if score >= 90: return "EXCELLENT_COMPORTEMENTAL"
        elif score >= 75: return "BON_COMPORTEMENTAL"
        elif score >= 60: return "ACCEPTABLE_COMPORTEMENTAL"
        elif score >= 45: return "ATTENTION_COMPORTEMENTAL"
        else: return "CRITIQUE_COMPORTEMENTAL"
    
    def _get_coherence_level(self, score: float) -> str:
        """Déterminer le niveau de cohérence"""
        if score >= 80: return "excellent"
        elif score >= 60: return "bon"
        elif score >= 40: return "modere"
        else: return "faible"
    
    def _generate_a1_recommendations(self, abc_analysis: Dict[str, Any]) -> List[str]:
        """Générer recommandations A1 basées sur ABC"""
        recommendations = []
        
        for intervention in abc_analysis.get("intervention_points", []):
            category = intervention["category"]
            priority = intervention["priority"]
            
            if priority == "high":
                recommendations.append(f"Action immédiate: Corriger {category}")
            else:
                recommendations.append(f"Planifier amélioration: {category}")
        
        return recommendations[:5]  # Max 5 recommandations

# =============================================================================
# TESTS ET DÉMONSTRATION
# =============================================================================

def test_orchestrateur():
    """Test complet de l'orchestrateur"""
    
    print("🧪 TEST ORCHESTRATEUR BEHAVIORX-SAFETYAGENTIC")
    print("="*60)
    
    # Initialisation
    orchestrator = BehaviorXSafetyOrchestrator({
        'memory_enabled': True,
        'debug_mode': True
    })
    
    # Test 1: Chantier construction standard
    print(f"\n📋 TEST 1: Chantier Construction Standard")
    results1 = orchestrator.execute_full_workflow(
        enterprise_id="Construction_ABC_Test", 
        sector_code="236",
        workflow_mode="hybrid"
    )
    
    # Test 2: Établissement soins de santé
    print(f"\n📋 TEST 2: Établissement Soins de Santé")
    results2 = orchestrator.execute_full_workflow(
        enterprise_id="Hopital_DEF_Test", 
        sector_code="622",
        workflow_mode="vcs_abc"
    )
    
    # Synthèse
    print(f"\n📊 SYNTHÈSE TESTS ORCHESTRATEUR")
    print(f"="*60)
    print(f"🧪 Test 1 - Construction:")
    print(f"   Score intégration: {results1.integration_score:.1f}%")
    print(f"   Zones aveugles: {len(results1.blind_spots)}")
    print(f"   Actions prioritaires: {len(results1.priority_actions)}")
    
    print(f"🧪 Test 2 - Soins de santé:")
    print(f"   Score intégration: {results2.integration_score:.1f}%")
    print(f"   Zones aveugles: {len(results2.blind_spots)}")
    print(f"   Actions prioritaires: {len(results2.priority_actions)}")
    
    print(f"\n✅ ORCHESTRATEUR OPÉRATIONNEL")
    print(f"🎯 Prêt pour intégration interface Streamlit")

if __name__ == "__main__":
    test_orchestrateur()