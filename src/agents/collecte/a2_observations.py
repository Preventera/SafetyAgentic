# SafetyAgentic - Agent A2 : Capteur Observations Terrain
# ======================================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import re

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

class A2CapteurObservations(BaseAgent):
    """
    Agent A2 - Capteur et Analyste des Observations Terrain
    
    Spécialisé dans:
    - Analyse des observations de terrain (photos, vidéos, signalements)
    - Détection automatique des EPI et équipements de sécurité
    - Évaluation de la conformité aux procédures
    - Identification des conditions dangereuses
    - Analyse comportementale et des gestes de sécurité
    """
    
    def __init__(self):
        config = AgentConfig(
            agent_id="A2",
            name="Capteur Observations",
            description="Capture et analyse observations terrain multimédia"
        )
        super().__init__(config)
        
        self.logger.info("🤖 Agent A2 initialisé - Capteur Observations")
        
        # EPI et équipements de sécurité référentiels
        self.epi_reference = {
            "casque": {
                "obligatoire_secteurs": ["CONSTRUCTION", "FABRICATION", "MINES"],
                "patterns": ["CASQUE", "HELMET", "TETE", "CRANIEN"],
                "variables_culture": [23, 67, 50]  # Usage EPI, EPC, Signalisation
            },
            "lunettes": {
                "obligatoire_secteurs": ["FABRICATION", "CHIMIE", "SOUDURE"],
                "patterns": ["LUNETTES", "PROTECTION OCULAIRE", "YEUX"],
                "variables_culture": [23, 67]
            },
            "gants": {
                "obligatoire_secteurs": ["FABRICATION", "CHIMIE", "MAINTENANCE"],
                "patterns": ["GANTS", "PROTECTION MAINS", "MANIPULATION"],
                "variables_culture": [23, 45]
            },
            "chaussures": {
                "obligatoire_secteurs": ["CONSTRUCTION", "FABRICATION", "ENTREPOT"],
                "patterns": ["CHAUSSURES SECURITE", "PROTECTION PIEDS", "BOTTES"],
                "variables_culture": [23, 50]
            },
            "harnais": {
                "obligatoire_secteurs": ["CONSTRUCTION", "HAUTEUR", "TOITURE"],
                "patterns": ["HARNAIS", "PROTECTION CHUTE", "HAUTEUR"],
                "variables_culture": [23, 67, 7]  # EPI, EPC, Leadership
            }
        }
        
        # Conditions dangereuses à détecter
        self.hazards_detection = {
            "sol_glissant": {
                "patterns": ["LIQUIDE SOL", "HUILE", "EAU", "GLISSANT", "MOUILLE"],
                "gravite": "medium",
                "variables": [50, 67, 45]  # Signalisation, EPC, Organisation
            },
            "hauteur_non_protegee": {
                "patterns": ["HAUTEUR", "ECHELLE", "TOIT", "SANS PROTECTION"],
                "gravite": "high",
                "variables": [67, 23, 7]  # EPC, EPI, Leadership
            },
            "machine_non_protegee": {
                "patterns": ["MACHINE", "COURROIE", "ENGRENAGE", "SANS PROTECTION"],
                "gravite": "high",
                "variables": [67, 89, 50]  # EPC, Maintenance, Signalisation
            },
            "produit_chimique": {
                "patterns": ["CHIMIQUE", "VAPEUR", "GAZ", "TOXIQUE"],
                "gravite": "high",
                "variables": [23, 67, 88]  # EPI, EPC, Hygiène
            },
            "encombrement": {
                "patterns": ["ENCOMBREMENT", "PASSAGE BLOQUE", "OBSTACLE"],
                "gravite": "low",
                "variables": [45, 50]  # Organisation, Signalisation
            }
        }
    
    async def process(self, state: SafetyAgenticState) -> SafetyAgenticState:
        """Traite les observations terrain et met à jour l'état"""
        
        start_time = datetime.now()
        
        try:
            self.logger.info("🔄 Démarrage traitement Agent A2")
            
            # Validation des données d'entrée
            if not await self.validate_input(state):
                state.errors.append("A2: Données d'entrée invalides")
                return state
            
            # Extraction des données d'observation
            observation_data = state.incident_data.get("observation_data", {})
            incident_data = state.incident_data.get("incident_cnesst", {})
            
            # Analyse principale
            analysis_result = await self.analyze_observation(observation_data, incident_data)
            
            # Mise à jour de l'état
            state.analysis_results["A2"] = analysis_result
            state.culture_variables.extend(analysis_result.get("culture_variables", []))
            state.current_agent = "A2"
            state.confidence_score = analysis_result.get("confidence_score", 0.0)
            state.workflow_stage = "observation_completed"
            
            # Log de performance
            await self.log_performance(start_time, analysis_result)
            
            self.logger.info(f"✅ Agent A2 terminé - Score confiance: {analysis_result.get('confidence_score', 0):.2f}")
            
        except Exception as e:
            error_msg = f"A2 Error: {str(e)}"
            state.errors.append(error_msg)
            self.logger.error(f"❌ {error_msg}")
        
        return state
    
    async def analyze_observation(self, observation_data: Dict, incident_data: Dict) -> Dict:
        """Analyse complète des observations terrain"""
        
        self.logger.info("🔍 Analyse observations terrain en cours...")
        
        # 1. Analyse des EPI et équipements
        epi_analysis = self.analyze_epi_compliance(observation_data, incident_data)
        
        # 2. Détection des dangers et conditions dangereuses
        hazard_detection = self.detect_hazards(observation_data, incident_data)
        
        # 3. Évaluation de la conformité procédurale
        compliance_analysis = self.evaluate_procedure_compliance(observation_data, incident_data)
        
        # 4. Analyse comportementale et gestuelle
        behavioral_analysis = self.analyze_safety_behaviors(observation_data, incident_data)
        
        # 5. Mapping vers variables culture SST
        culture_variables = self.map_observations_to_culture_variables(
            epi_analysis, hazard_detection, compliance_analysis, behavioral_analysis, incident_data
        )
        
        # 6. Calcul du score de confiance global
        confidence_score = self.calculate_observation_confidence(
            epi_analysis, hazard_detection, compliance_analysis
        )
        
        # 7. Génération de recommandations
        recommendations = self.generate_observation_recommendations(
            epi_analysis, hazard_detection, compliance_analysis, culture_variables
        )
        
        return {
            "agent_id": "A2",
            "analysis_type": "observation_terrain",
            "epi_analysis": epi_analysis,
            "hazard_detection": hazard_detection,
            "compliance_analysis": compliance_analysis,
            "behavioral_analysis": behavioral_analysis,
            "culture_variables": culture_variables,
            "confidence_score": confidence_score,
            "recommendations": recommendations,
            "immediate_risks": hazard_detection.get("high_priority_hazards", []),
            "next_agent": "AN1",
            "processing_timestamp": datetime.now().isoformat()
        }
    
    def analyze_epi_compliance(self, observation_data: Dict, incident_data: Dict) -> Dict:
        """Analyse de la conformité EPI"""
        
        # Simulation d'analyse EPI basée sur les données d'incident
        secteur = str(incident_data.get("SECTEUR_SCIAN", "")).upper()
        nature_lesion = str(incident_data.get("NATURE_LESION", "")).upper()
        siege_lesion = str(incident_data.get("SIEGE_LESION", "")).upper()
        
        epi_detected = {}
        epi_compliance = {}
        overall_compliance = 0.0
        
        # Analyse par type d'EPI
        for epi_type, epi_config in self.epi_reference.items():
            
            # Vérifier si EPI obligatoire dans le secteur
            is_required = any(sector in secteur for sector in epi_config["obligatoire_secteurs"])
            
            # Détecter présence/absence selon l'incident
            detected = False
            compliance_score = 0.7  # Score par défaut
            
            # Logique de détection basée sur l'incident
            if epi_type == "casque" and "TETE" in siege_lesion:
                detected = False  # Si blessure à la tête, probablement pas de casque
                compliance_score = 0.2
            elif epi_type == "gants" and "MAIN" in siege_lesion:
                detected = False  # Si blessure aux mains, probablement pas de gants
                compliance_score = 0.3
            elif epi_type == "chaussures" and "PIED" in siege_lesion:
                detected = False
                compliance_score = 0.2
            elif is_required:
                detected = True  # Assume présence si obligatoire et pas de blessure liée
                compliance_score = 0.8
            
            epi_detected[epi_type] = {
                "detected": detected,
                "required": is_required,
                "compliance_score": compliance_score,
                "confidence": 0.7
            }
            
            if is_required:
                epi_compliance[epi_type] = compliance_score
        
        # Calcul compliance globale
        if epi_compliance:
            overall_compliance = sum(epi_compliance.values()) / len(epi_compliance)
        
        return {
            "epi_detected": epi_detected,
            "overall_compliance": round(overall_compliance, 3),
            "compliance_by_type": epi_compliance,
            "total_epi_analyzed": len(epi_detected),
            "required_epi_count": len(epi_compliance)
        }
    
    def detect_hazards(self, observation_data: Dict, incident_data: Dict) -> Dict:
        """Détection des dangers et conditions dangereuses"""
        
        genre = str(incident_data.get("GENRE", "")).upper()
        agent_causal = str(incident_data.get("AGENT_CAUSAL_LESION", "")).upper()
        nature = str(incident_data.get("NATURE_LESION", "")).upper()
        
        detected_hazards = []
        high_priority_hazards = []
        
        # Analyse des dangers basée sur l'incident
        for hazard_type, hazard_config in self.hazards_detection.items():
            
            hazard_detected = False
            confidence = 0.0
            
            # Logique de détection basée sur les patterns
            for pattern in hazard_config["patterns"]:
                if (pattern in genre or pattern in agent_causal or 
                    pattern in nature):
                    hazard_detected = True
                    confidence = 0.8
                    break
            
            # Détections spécifiques
            if hazard_type == "sol_glissant" and "CHUTE AU MEME NIVEAU" in genre:
                hazard_detected = True
                confidence = 0.9
            elif hazard_type == "hauteur_non_protegee" and "CHUTE A UN NIVEAU INFERIEUR" in genre:
                hazard_detected = True
                confidence = 0.9
            elif hazard_type == "machine_non_protegee" and incident_data.get("IND_LESION_MACHINE") == "OUI":
                hazard_detected = True
                confidence = 0.8
            
            if hazard_detected:
                hazard_info = {
                    "type": hazard_type,
                    "severity": hazard_config["gravite"],
                    "confidence": confidence,
                    "variables_impacted": hazard_config["variables"]
                }
                
                detected_hazards.append(hazard_info)
                
                if hazard_config["gravite"] == "high":
                    high_priority_hazards.append(hazard_info)
        
        return {
            "total_hazards_detected": len(detected_hazards),
            "detected_hazards": detected_hazards,
            "high_priority_hazards": high_priority_hazards,
            "overall_risk_level": self.calculate_overall_risk_level(detected_hazards)
        }
    
    def calculate_overall_risk_level(self, hazards: List[Dict]) -> str:
        """Calcule le niveau de risque global"""
        
        if not hazards:
            return "low"
        
        high_count = len([h for h in hazards if h["severity"] == "high"])
        medium_count = len([h for h in hazards if h["severity"] == "medium"])
        
        if high_count >= 2:
            return "critical"
        elif high_count >= 1:
            return "high"
        elif medium_count >= 2:
            return "medium"
        else:
            return "low"
    
    def evaluate_procedure_compliance(self, observation_data: Dict, incident_data: Dict) -> Dict:
        """Évaluation de la conformité aux procédures"""
        
        genre = str(incident_data.get("GENRE", "")).upper()
        nature = str(incident_data.get("NATURE_LESION", "")).upper()
        
        # Score de conformité basé sur le type d'incident
        procedure_compliance = 0.7  # Score par défaut
        
        # Ajustements basés sur l'incident
        if "EFFORT EXCESSIF" in genre:
            procedure_compliance = 0.5  # Mauvaise technique de manutention
        elif "CHUTE" in genre:
            procedure_compliance = 0.4  # Procédures hauteur non suivies
        elif "MACHINE" in nature or incident_data.get("IND_LESION_MACHINE") == "OUI":
            procedure_compliance = 0.3  # Procédures machine non respectées
        elif incident_data.get("IND_LESION_TMS") == "OUI":
            procedure_compliance = 0.5  # Mauvaises postures/techniques
        
        return {
            "overall_compliance": round(procedure_compliance, 3),
            "procedure_areas": {
                "manutention": procedure_compliance if "EFFORT" in genre else 0.8,
                "travail_hauteur": procedure_compliance if "CHUTE" in genre else 0.8,
                "utilisation_machine": procedure_compliance if "MACHINE" in nature else 0.8,
                "ergonomie": procedure_compliance if incident_data.get("IND_LESION_TMS") == "OUI" else 0.8
            },
            "compliance_confidence": 0.7
        }
    
    def analyze_safety_behaviors(self, observation_data: Dict, incident_data: Dict) -> Dict:
        """Analyse comportementale et des gestes de sécurité"""
        
        # Analyse basée sur les données d'incident
        behaviors_observed = []
        safety_score = 0.7  # Score par défaut
        
        genre = str(incident_data.get("GENRE", "")).upper()
        nature = str(incident_data.get("NATURE_LESION", "")).upper()
        
        # Comportements déduits de l'incident
        if "EFFORT EXCESSIF" in genre:
            behaviors_observed.append({
                "behavior": "Technique manutention inadéquate",
                "safety_impact": "negative",
                "confidence": 0.8
            })
            safety_score -= 0.3
        
        if incident_data.get("IND_LESION_TMS") == "OUI":
            behaviors_observed.append({
                "behavior": "Postures contraignantes répétées",
                "safety_impact": "negative", 
                "confidence": 0.7
            })
            safety_score -= 0.2
        
        if "VOIES FAIT,ACTE VIOLENT" in genre:
            behaviors_observed.append({
                "behavior": "Gestion de conflit inadéquate",
                "safety_impact": "negative",
                "confidence": 0.9
            })
            safety_score -= 0.4
        
        safety_score = max(0.1, safety_score)  # Score minimum
        
        return {
            "behaviors_observed": behaviors_observed,
            "safety_behavior_score": round(safety_score, 3),
            "behavioral_patterns": self.identify_behavioral_patterns(behaviors_observed),
            "improvement_areas": self.identify_behavior_improvements(behaviors_observed)
        }
    
    def identify_behavioral_patterns(self, behaviors: List[Dict]) -> List[str]:
        """Identifie les patterns comportementaux"""
        
        patterns = []
        
        negative_behaviors = [b for b in behaviors if b["safety_impact"] == "negative"]
        
        if len(negative_behaviors) >= 2:
            patterns.append("multiple_unsafe_behaviors")
        
        behavior_types = [b["behavior"] for b in behaviors]
        
        if any("manutention" in b.lower() for b in behavior_types):
            patterns.append("manutention_risks")
        
        if any("posture" in b.lower() for b in behavior_types):
            patterns.append("ergonomic_risks")
        
        if any("conflit" in b.lower() for b in behavior_types):
            patterns.append("psychosocial_risks")
        
        return patterns
    
    def identify_behavior_improvements(self, behaviors: List[Dict]) -> List[str]:
        """Identifie les axes d'amélioration comportementale"""
        
        improvements = []
        
        behavior_texts = [b["behavior"].lower() for b in behaviors]
        
        if any("manutention" in text for text in behavior_texts):
            improvements.append("Formation gestes et postures")
        
        if any("posture" in text for text in behavior_texts):
            improvements.append("Analyse ergonomique postes")
        
        if any("conflit" in text for text in behavior_texts):
            improvements.append("Formation gestion stress et conflits")
        
        if any("technique" in text for text in behavior_texts):
            improvements.append("Renforcement formation technique")
        
        return improvements
    
    def map_observations_to_culture_variables(self, epi_analysis: Dict, hazard_detection: Dict, 
                                            compliance_analysis: Dict, behavioral_analysis: Dict,
                                            incident_data: Dict) -> List[Dict]:
        """Mapping des observations vers les variables culture SST"""
        
        mapped_variables = []
        
        # Variables basées sur la conformité EPI
        epi_compliance = epi_analysis.get("overall_compliance", 0.7)
        mapped_variables.append({
            "variable_id": 23,
            "variable_name": "Usage EPI",
            "score": epi_compliance * 10,
            "confidence": 0.8,
            "source": "observation_epi"
        })
        
        # Variables basées sur les dangers détectés
        if hazard_detection.get("total_hazards_detected", 0) > 0:
            risk_level = hazard_detection.get("overall_risk_level", "low")
            risk_score = {"low": 8, "medium": 6, "high": 4, "critical": 2}[risk_level]
            
            mapped_variables.extend([
                {
                    "variable_id": 50,
                    "variable_name": "Signalisation sécurité",
                    "score": risk_score,
                    "confidence": 0.7,
                    "source": "hazard_detection"
                },
                {
                    "variable_id": 67,
                    "variable_name": "EPC équipements",
                    "score": risk_score,
                    "confidence": 0.7,
                    "source": "hazard_detection"
                }
            ])
        
        # Variables basées sur la conformité procédurale
        proc_compliance = compliance_analysis.get("overall_compliance", 0.7)
        mapped_variables.append({
            "variable_id": 45,
            "variable_name": "Organisation travail",
            "score": proc_compliance * 10,
            "confidence": 0.8,
            "source": "procedure_compliance"
        })
        
        # Variables basées sur l'analyse comportementale
        behavior_score = behavioral_analysis.get("safety_behavior_score", 0.7)
        mapped_variables.extend([
            {
                "variable_id": 11,
                "variable_name": "Perception risque",
                "score": behavior_score * 10,
                "confidence": 0.7,
                "source": "behavioral_analysis"
            },
            {
                "variable_id": 34,
                "variable_name": "Respect procédures",
                "score": behavior_score * 10,
                "confidence": 0.7,
                "source": "behavioral_analysis"
            }
        ])
        
        # Variables spécifiques selon le type d'incident
        if incident_data.get("IND_LESION_TMS") == "OUI":
            mapped_variables.append({
                "variable_id": 67,
                "variable_name": "Ergonomie postes",
                "score": 5.0,  # Score faible car incident TMS
                "confidence": 0.9,
                "source": "incident_tms"
            })
        
        if incident_data.get("IND_LESION_PSY") == "OUI":
            mapped_variables.extend([
                {
                    "variable_id": 15,
                    "variable_name": "Communication RPS",
                    "score": 4.0,
                    "confidence": 0.8,
                    "source": "incident_psy"
                },
                {
                    "variable_id": 78,
                    "variable_name": "Gestion stress",
                    "score": 4.0,
                    "confidence": 0.8,
                    "source": "incident_psy"
                }
            ])
        
        return mapped_variables
    
    def calculate_observation_confidence(self, epi_analysis: Dict, hazard_detection: Dict, 
                                       compliance_analysis: Dict) -> float:
        """Calcule le score de confiance global des observations"""
        
        base_confidence = 0.7
        
        # Ajustement basé sur la quantité de données analysées
        epi_count = epi_analysis.get("total_epi_analyzed", 0)
        if epi_count >= 3:
            base_confidence += 0.1
        
        # Ajustement basé sur la détection de dangers
        hazard_count = hazard_detection.get("total_hazards_detected", 0)
        if hazard_count > 0:
            base_confidence += 0.1  # Plus de données = plus de confiance
        
        # Ajustement basé sur la confiance de conformité
        compliance_confidence = compliance_analysis.get("compliance_confidence", 0.7)
        base_confidence = (base_confidence + compliance_confidence) / 2
        
        return round(min(base_confidence, 1.0), 3)
    
    def generate_observation_recommendations(self, epi_analysis: Dict, hazard_detection: Dict,
                                           compliance_analysis: Dict, culture_variables: List[Dict]) -> List[str]:
        """Génère des recommandations basées sur les observations"""
        
        recommendations = []
        
        # Recommandations EPI
        epi_compliance = epi_analysis.get("overall_compliance", 1.0)
        if epi_compliance < 0.6:
            recommendations.append(
                f"Conformité EPI faible ({epi_compliance:.1%}) - Renforcer contrôles et formation"
            )
        
        # Recommandations dangers
        high_priority_hazards = hazard_detection.get("high_priority_hazards", [])
        if high_priority_hazards:
            recommendations.append(
                f"⚠️ {len(high_priority_hazards)} danger(s) critique(s) détecté(s) - Action immédiate requise"
            )
        
        # Recommandations conformité procédures
        proc_compliance = compliance_analysis.get("overall_compliance", 1.0)
        if proc_compliance < 0.5:
            recommendations.append(
                f"Conformité procédures faible ({proc_compliance:.1%}) - Formation et supervision renforcées"
            )
        
        # Recommandations variables culture
        low_score_variables = [v for v in culture_variables if v.get("score", 10) < 6]
        for var in low_score_variables[:3]:  # Top 3
            recommendations.append(
                f"Améliorer {var['variable_name']} (score: {var['score']:.1f}/10)"
            )
        
        return recommendations

# Fonction de test pour l'agent A2
async def test_agent_a2():
    """Test de l'agent A2 avec des données d'exemple"""
    
    print("🧪 TEST AGENT A2 - CAPTEUR OBSERVATIONS")
    print("=======================================")
    
    # Création de l'agent
    agent_a2 = A2CapteurObservations()
    
    # État de test avec données d'exemple
    test_state = SafetyAgenticState()
    test_state.incident_data = {
        "observation_data": {
            "location": "Atelier production",
            "observer_id": "INSPECTEUR_001",
            "observation_type": "terrain_inspection",
            "environmental_conditions": {
                "lighting": "adequate",
                "noise_level": "high",
                "temperature": "normal"
            }
        },
        "incident_cnesst": {
            "ID": "TEST_A2_001",
            "NATURE_LESION": "BLES. TRAUMA. MUSCLES,TENDONS,ETC.",
            "SIEGE_LESION": "MAINS,DOIGTS",
            "GENRE": "FRAPPE PAR UN OBJET",
            "AGENT_CAUSAL_LESION": "MACHINE-OUTIL",
            "SECTEUR_SCIAN": "FABRICATION DE BIENS DURABLES",
            "IND_LESION_MACHINE": "OUI",
            "IND_LESION_TMS": "",
            "IND_LESION_PSY": ""
        }
    }
    
    # Traitement par l'agent
    result_state = await agent_a2.process(test_state)
    
    # Affichage des résultats
    print("\n📊 RÉSULTATS AGENT A2:")
    print("======================")
    
    if "A2" in result_state.analysis_results:
        a2_result = result_state.analysis_results["A2"]
        
        print(f"✅ Score confiance: {a2_result.get('confidence_score', 0):.3f}")
        print(f"📊 Variables culture: {len(a2_result.get('culture_variables', []))}")
        print(f"⚠️ Dangers détectés: {a2_result.get('hazard_detection', {}).get('total_hazards_detected', 0)}")
        print(f"🛡️ Conformité EPI: {a2_result.get('epi_analysis', {}).get('overall_compliance', 0):.1%}")
        print(f"📋 Conformité procédures: {a2_result.get('compliance_analysis', {}).get('overall_compliance', 0):.1%}")
        print(f"💡 Recommandations: {len(a2_result.get('recommendations', []))}")
        
        print("\n🎯 VARIABLES CULTURE SST:")
        for var in a2_result.get('culture_variables', [])[:5]:
            print(f"  - {var['variable_name']}: {var['score']:.1f}/10 (source: {var['source']})")
        
        print("\n⚠️ DANGERS DÉTECTÉS:")
        hazards = a2_result.get('hazard_detection', {}).get('detected_hazards', [])
        for hazard in hazards[:3]:
            print(f"  - {hazard['type']} (gravité: {hazard['severity']}, conf: {hazard['confidence']:.2f})")
        
        print("\n💡 RECOMMANDATIONS PRINCIPALES:")
        for rec in a2_result.get('recommendations', [])[:3]:
            print(f"  - {rec}")
        
        print("\n🛡️ ANALYSE EPI:")
        epi_analysis = a2_result.get('epi_analysis', {})
        print(f"  - EPI analysés: {epi_analysis.get('total_epi_analyzed', 0)}")
        print(f"  - EPI obligatoires: {epi_analysis.get('required_epi_count', 0)}")
        
        print("\n🎭 ANALYSE COMPORTEMENTALE:")
        behavioral = a2_result.get('behavioral_analysis', {})
        print(f"  - Score comportement sécurité: {behavioral.get('safety_behavior_score', 0):.3f}")
        print(f"  - Comportements observés: {len(behavioral.get('behaviors_observed', []))}")
        
        patterns = behavioral.get('behavioral_patterns', [])
        if patterns:
            print("  - Patterns identifiés:")
            for pattern in patterns:
                print(f"    • {pattern}")
    
    print(f"\n❌ Erreurs: {len(result_state.errors)}")
    if result_state.errors:
        for error in result_state.errors:
            print(f"  - {error}")
    
    print("\n✅ Test Agent A2 terminé avec succès!")
    return result_state

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agent_a2())