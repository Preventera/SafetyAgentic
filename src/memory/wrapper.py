import sys
import os
sys.path.append(os.path.dirname(__file__))

from simple_memory import SafetyAgenticMemorySimple
from typing import Dict, Any
import json

_memory_instance = None

def get_memory():
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = SafetyAgenticMemorySimple()
    return _memory_instance

def add_agent_interaction(agent_id: str, user_id: str, input_data: Dict, result: Dict):
    try:
        memory = get_memory()
        
        content = f"""
        Agent: {agent_id}
        Input: {json.dumps(input_data, ensure_ascii=False)[:300]}
        Output: {json.dumps(result, ensure_ascii=False)[:300]}
        """
        
        metadata = {
            "type": "agent_interaction",
            "agent_id": agent_id,
            "score": result.get("score_final", 0),
            "timestamp": "2025-07-07"
        }
        
        return memory.add_agent_memory(agent_id, user_id, content, metadata)
        
    except Exception as e:
        print(f"Erreur memoire: {e}")
        return {"success": False}

def get_agent_context(agent_id: str, user_id: str, query: str):
    try:
        memory = get_memory()
        return memory.search_agent_memories(agent_id, user_id, query)
    except:
        return []

if __name__ == "__main__":
    print("Test wrapper simple")
    result = add_agent_interaction("A1", "test", {"question": "securite"}, {"score": 85})
    print("Test:", result)
