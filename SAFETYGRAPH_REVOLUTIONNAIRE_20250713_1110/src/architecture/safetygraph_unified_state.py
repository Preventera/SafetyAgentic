"""
SafetyGraph Unified State Architecture
====================================
État global unifié pour orchestration 100+ agents SafetyGraph
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SafetyGraphUnifiedState:
    """État global unifié SafetyGraph - Hub central données"""
    
    # === CONTEXTE UTILISATEUR ===
    user_input: str = ""
    user_profile: Dict[str, Any] = None
    session_context: Dict[str, Any] = None
    
    # === ROUTAGE & ORCHESTRATION ===
    intent: str = ""
    workflow_path: List[str] = None
    active_agents: List[str] = None
    
    # === DONNÉES COLLECTÉES ===
    observations_vcs: Dict[str, Any] = None
    questionnaires_culture: Dict[str, Any] = None
    feedback_terrain: Dict[str, Any] = None
    
    # === ANALYSES & ML ===
    culture_scores: Dict[str, float] = None
    predictions_ml: Dict[str, Any] = None
    anomalies_detected: List[Dict] = None
    
    # === RECHERCHE STORM ===
    storm_results: Dict[str, Any] = None
    scientific_citations: List[str] = None
    
    # === RECOMMANDATIONS ===
    action_plans: List[Dict] = None
    priorities: List[str] = None
    
    # === MONITORING & SUIVI ===
    kpi_realtime: Dict[str, float] = None
    alerts_active: List[Dict] = None
    
    # === CONTEXTE SECTORIEL ===
    sector_scian: str = ""
    sector_variables: List[int] = None
    
    # === MÉTA-DONNÉES ===
    timestamp: datetime = None
    version: str = "1.0"
    
    def __post_init__(self):
        """Initialisation automatique des champs par défaut"""
        if self.user_profile is None:
            self.user_profile = {}
        if self.session_context is None:
            self.session_context = {}
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Conversion en dictionnaire pour sérialisation"""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

def create_behaviorx_state(user_input: str) -> SafetyGraphUnifiedState:
    """Création état pour workflow BehaviorX"""
    state = SafetyGraphUnifiedState()
    state.user_input = user_input
    state.intent = "behaviorx_analysis"
    state.workflow_path = ["Router", "Context", "A1", "A2", "AN1", "R1"]
    state.active_agents = ["A1", "A2"]
    return state

if __name__ == "__main__":
    # Test création état
    test_state = create_behaviorx_state("Analyser culture construction")
    print("✅ SafetyGraphUnifiedState créé avec succès")
    print(f"Intent: {test_state.intent}")
    print(f"Workflow: {test_state.workflow_path}")
    print(f"Timestamp: {test_state.timestamp}")
    
    # Test sérialisation
    import json
    state_dict = test_state.to_dict()
    print(json.dumps(state_dict, indent=2, default=str))
