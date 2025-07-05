# SafetyAgentic - Agent de Base
# =============================

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SafetyAgenticState:
    """État partagé entre tous les agents SafetyAgentic"""
    
    def __init__(self):
        self.incident_data: Dict[str, Any] = {}
        self.analysis_results: Dict[str, Any] = {}
        self.culture_variables: List[Dict] = []
        self.recommendations: List[Dict] = []
        self.current_agent: str = ""
        self.workflow_stage: str = ""
        self.confidence_score: float = 0.0
        self.processing_metadata: Dict[str, Any] = {}
        self.errors: List[str] = []
    
    def to_dict(self) -> Dict:
        """Convertit l'état en dictionnaire"""
        return {
            "incident_data": self.incident_data,
            "analysis_results": self.analysis_results,
            "culture_variables": self.culture_variables,
            "recommendations": self.recommendations,
            "current_agent": self.current_agent,
            "workflow_stage": self.workflow_stage,
            "confidence_score": self.confidence_score,
            "processing_metadata": self.processing_metadata,
            "errors": self.errors
        }

class AgentConfig:
    """Configuration d'un agent SafetyAgentic"""
    
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.enabled = True
        self.max_retries = 3
        self.timeout_seconds = 300
        self.specialized_sectors = []
        self.culture_variables_focus = []

class BaseAgent(ABC):
    """Classe de base pour tous les agents SafetyAgentic"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.performance_metrics = {}
        self.logger = logging.getLogger(f"SafetyAgentic.{config.agent_id}")
        
        self.logger.info(f"🤖 Agent {config.agent_id} ({config.name}) initialisé")
    
    @abstractmethod
    async def process(self, state: SafetyAgenticState) -> SafetyAgenticState:
        """Méthode principale de traitement de l'agent"""
        pass
    
    async def validate_input(self, state: SafetyAgenticState) -> bool:
        """Valide les données d'entrée"""
        if not state.incident_data:
            self.logger.warning("❌ Données d'incident manquantes")
            return False
        
        self.logger.info("✅ Validation des données d'entrée réussie")
        return True
    
    async def log_performance(self, start_time: datetime, result: Dict):
        """Log des métriques de performance"""
        processing_time = (datetime.now() - start_time).total_seconds()
        
        self.performance_metrics[datetime.now().isoformat()] = {
            "processing_time": processing_time,
            "confidence": result.get("confidence_score", 0.0),
            "status": "success" if result else "error"
        }
        
        self.logger.info(
            f"📊 Performance {self.config.agent_id}: "
            f"{processing_time:.2f}s, "
            f"confidence: {result.get('confidence_score', 0.0):.2f}"
        )
    
    def get_culture_variables_mapping(self) -> Dict[str, List[Dict]]:
        """Retourne le mapping des variables culture SST"""
        
        return {
            "TMS": [
                {"variable_id": 23, "name": "Usage EPI", "weight": 0.9},
                {"variable_id": 45, "name": "Organisation travail", "weight": 0.8},
                {"variable_id": 67, "name": "Ergonomie postes", "weight": 0.9}
            ],
            "PSYCHOLOGIQUE": [
                {"variable_id": 15, "name": "Communication RPS", "weight": 0.9},
                {"variable_id": 33, "name": "Confiance équipe", "weight": 0.8},
                {"variable_id": 78, "name": "Gestion stress", "weight": 0.9}
            ],
            "EFFORT_EXCESSIF": [
                {"variable_id": 23, "name": "Usage EPI", "weight": 0.8},
                {"variable_id": 45, "name": "Organisation travail", "weight": 0.9},
                {"variable_id": 11, "name": "Perception risque", "weight": 0.7}
            ],
            "CHUTE": [
                {"variable_id": 7, "name": "Leadership visible SST", "weight": 0.8},
                {"variable_id": 23, "name": "Usage EPI", "weight": 0.9},
                {"variable_id": 50, "name": "Signalisation", "weight": 0.7}
            ],
            "MACHINE": [
                {"variable_id": 50, "name": "Signalisation", "weight": 0.8},
                {"variable_id": 67, "name": "EPC équipements", "weight": 0.9},
                {"variable_id": 89, "name": "Maintenance préventive", "weight": 0.8}
            ]
        }
    
    def calculate_severity_score(self, incident_data: Dict) -> float:
        """Calcule un score de gravité basé sur les données d'incident"""
        
        base_score = 1.0
        
        # Facteurs de gravité par nature de lésion
        nature = str(incident_data.get("NATURE_LESION", "")).upper()
        
        if "DECES" in nature:
            base_score *= 10.0
        elif "AMPUTATION" in nature:
            base_score *= 8.0
        elif "FRACTURE" in nature:
            base_score *= 6.0
        elif "TRAUMA" in nature:
            base_score *= 4.0
        elif "TMS" in nature or "MUSCLE" in nature:
            base_score *= 3.0
        elif "CONTUSION" in nature:
            base_score *= 2.0
        
        # Facteurs par siège de lésion
        siege = str(incident_data.get("SIEGE_LESION", "")).upper()
        
        if "TETE" in siege:
            base_score *= 3.0
        elif "COLONNE" in siege or "DOS" in siege:
            base_score *= 2.5
        elif "MULTIPLE" in siege:
            base_score *= 2.0
        
        # Facteurs spéciaux
        if incident_data.get("IND_LESION_PSY") == "OUI":
            base_score *= 2.0
        
        if incident_data.get("IND_LESION_TMS") == "OUI":
            base_score *= 1.5
        
        # Normalisation 1-10
        return min(max(base_score, 1.0), 10.0)
    
    def map_incident_to_culture_variables(self, incident_data: Dict) -> List[Dict]:
        """Map un incident vers les variables culture SST pertinentes"""
        
        mapped_vars = []
        mapping = self.get_culture_variables_mapping()
        
        # Mapping basé sur la nature de lésion
        nature = str(incident_data.get("NATURE_LESION", "")).upper()
        
        if "TMS" in nature or "MUSCLE" in nature:
            mapped_vars.extend(mapping["TMS"])
        
        # Mapping basé sur le genre d'accident
        genre = str(incident_data.get("GENRE", "")).upper()
        
        if "EFFORT EXCESSIF" in genre:
            mapped_vars.extend(mapping["EFFORT_EXCESSIF"])
        elif "CHUTE" in genre:
            mapped_vars.extend(mapping["CHUTE"])
        
        # Mapping basé sur les indicateurs
        if incident_data.get("IND_LESION_PSY") == "OUI":
            mapped_vars.extend(mapping["PSYCHOLOGIQUE"])
        
        if incident_data.get("IND_LESION_MACHINE") == "OUI":
            mapped_vars.extend(mapping["MACHINE"])
        
        # Dédoublonnage par variable_id
        unique_vars = {}
        for var in mapped_vars:
            var_id = var["variable_id"]
            if var_id not in unique_vars or var["weight"] > unique_vars[var_id]["weight"]:
                unique_vars[var_id] = var
        
        return list(unique_vars.values())
    
    def get_sector_specialization(self, secteur_scian: str) -> Dict:
        """Retourne la spécialisation sectorielle"""
        
        secteur_upper = str(secteur_scian).upper()
        
        if "SOINS DE SANTE" in secteur_upper:
            return {
                "agent_id": "A15",
                "specialization": "healthcare",
                "priority": 1,
                "specific_variables": [15, 33, 78, 88]  # RPS, confiance, stress, hygiène
            }
        elif "CONSTRUCTION" in secteur_upper:
            return {
                "agent_id": "A35", 
                "specialization": "construction",
                "priority": 1,
                "specific_variables": [7, 23, 50, 67]  # Leadership, EPI, signalisation, EPC
            }
        elif "FABRICATION" in secteur_upper:
            return {
                "agent_id": "A25",
                "specialization": "manufacturing", 
                "priority": 2,
                "specific_variables": [50, 67, 89]  # Signalisation, EPC, maintenance
            }
        else:
            return {
                "agent_id": "A99",
                "specialization": "general",
                "priority": 3,
                "specific_variables": [7, 11, 23]  # Leadership, perception, EPI
            }