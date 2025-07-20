"""Schéma d'état SafeGraph"""

from typing_extensions import TypedDict
from typing import List, Dict, Optional, Any, Annotated
from enum import Enum
from datetime import datetime
import operator

class IntentType(Enum):
    """Types d'intentions utilisateur"""
    EVALUATION = "evaluation"
    ANALYSIS = "analysis"
    RECOMMENDATION = "recommendation" 
    MONITORING = "monitoring"
    RESEARCH = "research"
    UNKNOWN = "unknown"

class SectorType(Enum):
    """Secteurs SCIAN supportés"""
    CONSTRUCTION = "236"
    TRANSPORT = "484"
    HEALTHCARE = "622"
    MAINTENANCE = "811"
    SECURITY = "561"

class SafetyState(TypedDict):
    """État global partagé entre agents SafeGraph"""
    
    # Entrée utilisateur
    user_input: str
    intent: Optional[IntentType]
    session_id: str
    
    # Contexte enrichi
    context: Dict[str, Any]
    scian_sector: Optional[SectorType]
    user_profile: Dict[str, Any]
    
    # Données collectées - utilise operator.add pour agréger
    collection_results: Annotated[List[Dict[str, Any]], operator.add]
    questionnaire_data: Dict[str, Any]
    
    # Analyses
    analysis: Dict[str, Any]
    risk_scores: Dict[str, float]
    predictions: Dict[str, Any]
    
    # Recommandations
    recommendations: Annotated[List[Dict[str, Any]], operator.add]
    action_plan: Dict[str, Any]
    priority_actions: List[str]
    
    # Suivi et historique
    feedback: str
    history: Annotated[List[Dict[str, Any]], operator.add]
    monitoring_data: Dict[str, Any]
    
    # Recherche STORM
    storm_results: Dict[str, Any]
    research_context: List[str]
    
    # Métadonnées
    timestamp: str
    agent_trace: Annotated[List[str], operator.add]
    errors: Annotated[List[str], operator.add]

def create_initial_state(user_input: str) -> SafetyState:
    """Crée un état initial pour une nouvelle session"""
    return SafetyState(
        user_input=user_input,
        intent=None,
        session_id=f"session_{int(datetime.now().timestamp())}",
        context={},
        scian_sector=None,
        user_profile={},
        collection_results=[],
        questionnaire_data={},
        analysis={},
        risk_scores={},
        predictions={},
        recommendations=[],
        action_plan={},
        priority_actions=[],
        feedback="",
        history=[],
        monitoring_data={},
        storm_results={},
        research_context=[],
        timestamp=datetime.now().isoformat(),
        agent_trace=[],
        errors=[]
    )