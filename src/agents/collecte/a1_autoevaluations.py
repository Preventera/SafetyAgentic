# SafetyAgentic - Agent A1 : Collecteur Autoévaluations (Version Corrigée)
# ========================================================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from datetime import datetime
from typing import Dict, List, Any
import json
import pandas as pd
from pathlib import Path

# Import des classes de base
try:
    from agents.base_agent import BaseAgent, AgentConfig, SafetyAgenticState
except ImportError:
    # Définition locale si import échoue
    from abc import ABC, abstractmethod
    import logging
    
    logging.basicConfig(level=logging.INFO)
    
    class SafetyAgenticState:
        def __init__(self):
            self.incident_data = {}
            self.analysis_results = {}
            self.culture_variables = []
            self.recommendations = []
            self.current_agent = ""
            self.workflow_stage = ""
            self.confidence_score = 0.0
            self.processing_metadata = {}
            self.errors = []
    
    class AgentConfig:
        def __init__(self, agent_id, name, description):
            self.agent_id = agent_id
            self.name = name
            self.description = description
    
    class BaseAgent(ABC):
        def __init__(self, config):
            self.config = config
            self.logger = logging.getLogger(f"SafetyAgentic.{config.agent_id}")
        
        async def validate_input(self, state):
            return True
        
        async def log_performance(self, start_time, result):
            pass

class A1CollecteurAutoevaluations(BaseAgent):
    """
    Agent A1 - Collecteur et Analyste des Autoévaluations de Culture Sécurité
    """
    
    def __init__(self):
        config = AgentConfig(
            agent_id="A1",
            name="Collecteur Autoévaluations",
            description="Collecte et analyse autoévaluations culture sécurité"
        )
        super().__init__(config)
        
        self.logger.info("🤖 Agent A1 initialisé - Collecteur Autoévaluations")
        
        # Variables culture SST de base
        self.variable_names = {
            7: "Leadership visible SST",
            11: "Perception risque",
            15: "Communication RPS",
            21: "Support management",
            23: "Usage EPI",
            28: "Formation initiale",
            29: "Reconnaissance performance",
            33: "Confiance équipe",
            34: "Respect procédures",
            35: "Mentorat jeunes",
            42: "Awareness sécurité",
            45: "Organisation travail",
            56: "Vigilance partagée",
            63: "Compétences techniques",
            67: "EPC équipements",
            78: "Cohésion équipe",
            89: "Maintenance préventive"
        }
        
        # Mapping TMS et autres conditions
        self.culture_mapping = {
            "TMS": [
                {"variable_id": 23, "name": "Usage EPI", "weight": 0.9},
                {"variable_id": 45, "name": "Organisation travail", "weight": 0.8},
                {"variable_id": 67, "name": "EPC équipements", "weight": 0.9}
            ],
            "EFFORT_EXCESSIF": [
                {"variable_id": 23, "name": "Usage EPI", "weight": 0.8},
                {"variable_id": 45, "name": "Organisation travail", "weight": 0.9},
                {"variable_id": 11, "name": "Perception risque", "weight": 0.7}
            ]
        }
    
    async def process(self, state: SafetyAgenticState) -> SafetyAgenticState:
        """Traite les données d'autoévaluation et met à jour l'état"""
        
        start_time = datetime.now()
        
        try:
            self.logger.info("🔄 Démarrage traitement Agent A1")
            
            # Validation des données d'entrée
            if not await self.validate_input(state):
                state.errors.append("A1: Données d'entrée invalides")
                return state
            
            # Extraction des données
            evaluation_data = state.incident_data.get("evaluation_data", {})
            incident_data = state.incident_data.get("incident_cnesst", {})
            
            # Analyse principale
            analysis_result = await self.analyze_autoevaluation(evaluation_data, incident_data)
            
            # Mise à jour de l'état
            state.analysis_results["A1"] = analysis_result
            state.culture_variables.extend(analysis_result.get("culture_variables", []))
            state.current_agent = "A1"
            state.confidence_score = analysis_result.get("reliability_score", 0.0)
            state.workflow_stage = "collecte_completed"
            
            # Log de performance
            await self.log_performance(start_time, analysis_result)
            
            self.logger.info(f"✅ Agent A1 terminé - Score fiabilité: {analysis_result.get('reliability_score', 0):.2f}")
            
        except Exception as e:
            error_msg = f"A1 Error: {str(e)}"
            state.errors.append(error_msg)
            self.logger.error(f"❌ {error_msg}")
        
        return state
    
    async def analyze_autoevaluation(self, evaluation_data: Dict, incident_data: Dict) -> Dict:
        """Analyse complète d'autoévaluation"""
        
        self.logger.info("🔍 Analyse autoévaluation en cours...")
        
        # 1. Analyse psychométrique des réponses
        psychometric_analysis = self.analyze_response_patterns(evaluation_data)
        
        # 2. Détection des biais cognitifs
        bias_detection = self.detect_cognitive_biases(evaluation_data)
        
        # 3. Mapping vers variables culture SST
        culture_variables = self.map_to_culture_variables(evaluation_data, incident_data)
        
        # 4. Calcul score de fiabilité
        reliability_score = self.calculate_reliability_score(
            psychometric_analysis, bias_detection
        )
        
        # 5. Identification des patterns comportementaux
        behavioral_patterns = self.identify_behavioral_patterns(evaluation_data)
        
        # 6. Génération de recommandations
        recommendations = self.generate_recommendations(
            culture_variables, reliability_score, behavioral_patterns
        )
        
        return {
            "agent_id": "A1",
            "analysis_type": "autoevaluation",
            "reliability_score": reliability_score,
            "culture_variables": culture_variables,
            "psychometric_analysis": psychometric_analysis,
            "bias_detection": bias_detection,
            "behavioral_patterns": behavioral_patterns,
            "recommendations": recommendations,
            "confidence_score": reliability_score,
            "next_agent": "N1",
            "processing_timestamp": datetime.now().isoformat()
        }
    
    def analyze_response_patterns(self, evaluation_data: Dict) -> Dict:
        """Analyse psychométrique des patterns de réponses"""
        
        responses = evaluation_data.get("responses", {})
        
        if not responses:
            return {"pattern_type": "insufficient_data", "coherence_score": 0.0}
        
        # Calcul cohérence des réponses
        response_values = [v for v in responses.values() if isinstance(v, (int, float))]
        
        if len(response_values) < 3:
            return {"pattern_type": "insufficient_responses", "coherence_score": 0.0}
        
        # Variance des réponses (cohérence)
        mean_response = sum(response_values) / len(response_values)
        variance = sum((x - mean_response) ** 2 for x in response_values) / len(response_values)
        
        # Score de cohérence (inverse de la variance normalisée)
        coherence_score = max(0, 1 - (variance / 25))
        
        # Détection de patterns
        if variance < 1:
            pattern_type = "uniform_high" if mean_response > 7 else "uniform_low"
        elif variance > 9:
            pattern_type = "highly_variable"
        else:
            pattern_type = "normal_distribution"
        
        return {
            "pattern_type": pattern_type,
            "coherence_score": round(coherence_score, 3),
            "mean_response": round(mean_response, 2),
            "variance": round(variance, 2),
            "response_count": len(response_values)
        }
    
    def detect_cognitive_biases(self, evaluation_data: Dict) -> Dict:
        """Détection des biais cognitifs dans les réponses"""
        
        responses = evaluation_data.get("responses", {})
        employee_profile = evaluation_data.get("employee_profile", {})
        
        biases_detected = []
        bias_confidence = 0.0
        
        if not responses:
            return {"biases_detected": [], "bias_confidence": 0.0}
        
        response_values = [v for v in responses.values() if isinstance(v, (int, float))]
        
        if len(response_values) < 3:
            return {"biases_detected": [], "bias_confidence": 0.0}
        
        mean_response = sum(response_values) / len(response_values)
        
        # Biais de surconfiance
        if mean_response > 8.5 and len([x for x in response_values if x >= 9]) > len(response_values) * 0.7:
            biases_detected.append({
                "type": "surconfiance",
                "description": "Tendance à surévaluer ses compétences sécurité",
                "confidence": 0.8
            })
            bias_confidence += 0.3
        
        # Biais de désirabilité sociale
        if len(set(response_values)) <= 2 and mean_response > 8:
            biases_detected.append({
                "type": "desirabilite_sociale", 
                "description": "Réponses influencées par ce qui est socialement attendu",
                "confidence": 0.7
            })
            bias_confidence += 0.25
        
        return {
            "biases_detected": biases_detected,
            "bias_confidence": min(bias_confidence, 1.0),
            "bias_count": len(biases_detected)
        }
    
    def map_to_culture_variables(self, evaluation_data: Dict, incident_data: Dict) -> List[Dict]:
        """Mapping vers les variables culture SST"""
        
        responses = evaluation_data.get("responses", {})
        mapped_variables = []
        
        # Mapping basé sur l'incident CNESST si disponible
        if incident_data:
            genre = str(incident_data.get("GENRE", "")).upper()
            ind_tms = incident_data.get("IND_LESION_TMS", "")
            
            # TMS détecté
            if ind_tms == "OUI" or "TMS" in str(incident_data.get("NATURE_LESION", "")).upper():
                for var_data in self.culture_mapping["TMS"]:
                    mapped_variables.append({
                        "variable_id": var_data["variable_id"],
                        "variable_name": var_data["name"],
                        "score": 7.0,  # Score par défaut
                        "confidence": var_data["weight"],
                        "source": "incident_cnesst",
                        "category": "TMS"
                    })
            
            # Effort excessif
            if "EFFORT EXCESSIF" in genre:
                for var_data in self.culture_mapping["EFFORT_EXCESSIF"]:
                    mapped_variables.append({
                        "variable_id": var_data["variable_id"],
                        "variable_name": var_data["name"],
                        "score": 6.5,  # Score par défaut
                        "confidence": var_data["weight"],
                        "source": "incident_cnesst",
                        "category": "EFFORT_EXCESSIF"
                    })
        
        # Mapping basé sur les réponses d'autoévaluation
        if responses:
            all_scores = [v for v in responses.values() if isinstance(v, (int, float))]
            avg_score = sum(all_scores) / len(all_scores) if all_scores else 5.0
            
            # Variables générales d'autoévaluation
            autoevaluation_vars = [
                {"variable_id": 11, "name": "Perception risque"},
                {"variable_id": 23, "name": "Usage EPI"},
                {"variable_id": 33, "name": "Confiance équipe"},
                {"variable_id": 45, "name": "Organisation travail"}
            ]
            
            for var_data in autoevaluation_vars:
                mapped_variables.append({
                    "variable_id": var_data["variable_id"],
                    "variable_name": var_data["name"],
                    "score": avg_score,
                    "confidence": min(avg_score / 10.0, 1.0),
                    "source": "autoevaluation",
                    "category": "general"
                })
        
        return mapped_variables
    
    def calculate_reliability_score(self, psychometric: Dict, bias_detection: Dict) -> float:
        """Calcule un score de fiabilité des données d'autoévaluation"""
        
        base_reliability = 0.7
        
        # Ajustement basé sur la cohérence
        coherence_score = psychometric.get("coherence_score", 0.5)
        reliability = base_reliability * (0.5 + 0.5 * coherence_score)
        
        # Pénalité pour les biais
        bias_penalty = bias_detection.get("bias_confidence", 0.0) * 0.3
        reliability = max(0.1, reliability - bias_penalty)
        
        # Bonus pour données suffisantes
        response_count = psychometric.get("response_count", 0)
        if response_count >= 5:
            reliability += 0.1
        
        return round(min(reliability, 1.0), 3)
    
    def identify_behavioral_patterns(self, evaluation_data: Dict) -> List[str]:
        """Identifie les patterns comportementaux"""
        
        patterns = []
        responses = evaluation_data.get("responses", {})
        
        if not responses:
            return ["insufficient_data"]
        
        response_values = [v for v in responses.values() if isinstance(v, (int, float))]
        
        if len(response_values) < 3:
            return ["insufficient_responses"]
        
        mean_response = sum(response_values) / len(response_values)
        
        # Classification des patterns
        if mean_response >= 8.5:
            patterns.append("high_safety_confidence")
        elif mean_response <= 4:
            patterns.append("low_safety_confidence")
        else:
            patterns.append("moderate_safety_awareness")
        
        # Variabilité
        variance = sum((x - mean_response) ** 2 for x in response_values) / len(response_values)
        
        if variance < 1:
            patterns.append("consistent_responder")
        elif variance > 6:
            patterns.append("variable_responder")
        
        return patterns
    
    def generate_recommendations(self, culture_variables: List[Dict], 
                               reliability_score: float, patterns: List[str]) -> List[str]:
        """Génère des recommandations basées sur l'analyse"""
        
        recommendations = []
        
        # Recommandations basées sur la fiabilité
        if reliability_score < 0.5:
            recommendations.append(
                "Fiabilité faible détectée - Recommander collecte de données complémentaire"
            )
            recommendations.append(
                "Envisager observations terrain pour valider les autoévaluations"
            )
        
        # Recommandations basées sur les patterns
        if "high_safety_confidence" in patterns:
            recommendations.append(
                "Surconfiance détectée - Sensibiliser aux risques de complaisance"
            )
        
        if "low_safety_confidence" in patterns:
            recommendations.append(
                "Faible confiance sécurité - Renforcer formation et accompagnement"
            )
        
        if "variable_responder" in patterns:
            recommendations.append(
                "Réponses variables - Clarifier les questions ou approfondir par entretien"
            )
        
        # Recommandations basées sur les variables culture
        low_score_variables = [v for v in culture_variables if v.get("score", 5) < 6]
        
        if low_score_variables:
            for var in low_score_variables[:3]:
                recommendations.append(
                    f"Améliorer {var['variable_name']} (score: {var['score']:.1f}/10)"
                )
        
        return recommendations

# Fonction de test pour l'agent A1
async def test_agent_a1():
    """Test de l'agent A1 avec des données d'exemple"""
    
    print("🧪 TEST AGENT A1 - COLLECTEUR AUTOÉVALUATIONS")
    print("==============================================")
    
    # Création de l'agent
    agent_a1 = A1CollecteurAutoevaluations()
    
    # État de test avec données d'exemple
    test_state = SafetyAgenticState()
    test_state.incident_data = {
        "evaluation_data": {
            "employee_id": "TEST_001",
            "responses": {
                "safety_awareness": 8,
                "risk_perception": 7,
                "epi_usage": 9,
                "procedure_compliance": 6,
                "team_communication": 8
            },
            "employee_profile": {
                "experience_years": 5,
                "role": "operator",
                "department": "production"
            }
        },
        "incident_cnesst": {
            "NATURE_LESION": "BLES. TRAUMA. MUSCLES,TENDONS,ETC.",
            "SIEGE_LESION": "DOS,COLONNE VERTEBRALE",
            "GENRE": "EFFORT EXCESSIF",
            "SECTEUR_SCIAN": "FABRICATION DE BIENS DURABLES",
            "IND_LESION_TMS": "OUI"
        }
    }
    
    # Traitement par l'agent
    result_state = await agent_a1.process(test_state)
    
    # Affichage des résultats
    print("\n📊 RÉSULTATS AGENT A1:")
    print("======================")
    
    if "A1" in result_state.analysis_results:
        a1_result = result_state.analysis_results["A1"]
        
        print(f"✅ Score fiabilité: {a1_result.get('reliability_score', 0):.3f}")
        print(f"📊 Variables culture identifiées: {len(a1_result.get('culture_variables', []))}")
        print(f"🧠 Biais détectés: {a1_result.get('bias_detection', {}).get('bias_count', 0)}")
        print(f"📋 Recommandations: {len(a1_result.get('recommendations', []))}")
        
        print("\n🎯 VARIABLES CULTURE SST:")
        for var in a1_result.get('culture_variables', [])[:5]:
            print(f"  - {var['variable_name']}: {var['score']:.1f}/10 (conf: {var['confidence']:.2f})")
        
        print("\n💡 RECOMMANDATIONS:")
        for rec in a1_result.get('recommendations', [])[:3]:
            print(f"  - {rec}")
        
        print("\n🔍 ANALYSE PSYCHOMÉTRIQUE:")
        psycho = a1_result.get('psychometric_analysis', {})
        print(f"  - Pattern: {psycho.get('pattern_type', 'N/A')}")
        print(f"  - Cohérence: {psycho.get('coherence_score', 0):.3f}")
        print(f"  - Moyenne réponses: {psycho.get('mean_response', 0):.1f}")
    
    print(f"\n❌ Erreurs: {len(result_state.errors)}")
    if result_state.errors:
        for error in result_state.errors:
            print(f"  - {error}")
    
    print("\n✅ Test Agent A1 terminé avec succès!")
    return result_state

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agent_a1())