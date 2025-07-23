"""
SafeGraph Core Module
Architecture multi-agent pour l'analyse de culture sécurité
"""

from .state import SafetyState, IntentType, SectorType
from .graph import create_safety_graph
from .config import SafeGraphConfig

__version__ = "0.1.0"
__all__ = ["SafetyState", "IntentType", "SectorType", "create_safety_graph", "SafeGraphConfig"]