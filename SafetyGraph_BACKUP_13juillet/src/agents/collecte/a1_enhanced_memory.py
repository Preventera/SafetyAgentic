"""
Agent A1 Enhanced avec Mem0 - Version Production
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from memory.wrapper import add_agent_interaction, get_agent_context
from agents.collecte.a1_autoevaluations_behaviorx import AgentA1AutoevaluationsBehaviorX
import json

class AgentA1Enhanced(AgentA1AutoevaluationsBehaviorX):
    """Agent A1 avec mémoire persistante Mem0"""
    
    def __init__(self):
        super().__init__()
        self.agent_id = "A1"
    
    def process_with_memory(self, data: dict, user_id: str = "default", secteur_scian: str = "236"):
        """
        Traite autoévaluation avec mémoire persistante
        
        Args:
            data: Données autoévaluation
            user_id: ID utilisateur/entreprise
            secteur_scian: Code secteur
            
        Returns:
            Résultat enrichi avec contexte mémoire
        """
        try:
            # 1. Récupérer contexte mémoire
            memories = get_agent_context(self.agent_id, user_id, f"autoevaluation {secteur_scian}")
            
            # 2. Traitement standard
            result = self.process_autoevaluation(data, secteur_scian)
            
            # 3. Enrichir avec insights mémoire
            if memories:
                result["memory_insights"] = {
                    "historical_evaluations": len(memories),
                    "previous_scores": [m.get("metadata", {}).get("score", 0) for m in memories],
                    "improvement_trend": self._calculate_trend(memories),
                    "recommendations_based_on_history": self._get_historical_recommendations(memories)
                }
            else:
                result["memory_insights"] = {
                    "historical_evaluations": 0,
                    "status": "première_évaluation",
                    "recommendations": ["Première évaluation enregistrée pour apprentissage futur"]
                }
            
            # 4. Mémoriser cette interaction
            add_agent_interaction(self.agent_id, user_id, data, result)
            
            return result
            
        except Exception as e:
            print(f"Erreur A1 Enhanced: {e}")
            # Fallback vers traitement standard
            return self.process_autoevaluation(data, secteur_scian)
    
    def _calculate_trend(self, memories):
        """Calcule tendance amélioration"""
        scores = [m.get("metadata", {}).get("score", 0) for m in memories[-3:]]
        if len(scores) >= 2:
            return "improving" if scores[-1] > scores[0] else "stable"
        return "insufficient_data"
    
    def _get_historical_recommendations(self, memories):
        """Recommandations basées sur historique"""
        return [
            "Continuez vos efforts basés sur l'historique positif",
            f"Vous avez {len(memories)} évaluations précédentes comme référence",
            "L'IA apprend de vos patterns pour de meilleures recommandations"
        ]

# Test rapide
if __name__ == "__main__":
    agent = AgentA1Enhanced()
    test_data = {
        "questions": [{"question": "Formation sécurité", "reponse": "Oui"}],
        "domaine": "construction"
    }
    result = agent.process_with_memory(test_data, "entreprise_test", "236")
    print("Test A1 Enhanced:", result.get("memory_insights", {}))
