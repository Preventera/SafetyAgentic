"""
Wrapper simple pour intégrer Mem0 aux agents existants
"""

from memory.mem0_integration import create_safetyagentic_memory
from typing import Dict, Any

# Instance globale mémoire
_memory_instance = None

def get_memory():
    """Récupère instance mémoire globale"""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = create_safetyagentic_memory()
    return _memory_instance

def enhance_agent_with_memory(agent_id: str, user_id: str, 
                             input_data: Dict, result: Dict):
    """
    Ajoute mémoire à n'importe quel agent existant
    
    Usage:
        # Dans votre agent existant
        result = self.process_data(data)
        enhance_agent_with_memory("A1", user_id, data, result)
        return result
    """
    try:
        memory = get_memory()
        
        messages = [
            {"role": "user", "content": str(input_data)[:500]},
            {"role": "assistant", "content": str(result)[:500]}
        ]
        
        metadata = {
            "agent_id": agent_id,
            "timestamp": "2025-07-07",
            "type": "agent_interaction"
        }
        
        memory.add_agent_memory(agent_id, user_id, messages, metadata)
        print(f"✅ Mémoire ajoutée pour {agent_id}")
        
    except Exception as e:
        print(f"⚠️ Erreur mémoire: {e}")

def get_agent_context(agent_id: str, user_id: str, query: str):
    """Récupère contexte mémoire pour un agent"""
    try:
        memory = get_memory()
        return memory.get_agent_context(agent_id, user_id, query)
    except:
        return []