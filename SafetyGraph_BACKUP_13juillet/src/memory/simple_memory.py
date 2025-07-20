import chromadb
import os
import json
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SafetyAgenticMemorySimple:
    def __init__(self):
        self.db_path = "data/memory_vectorstore"
        os.makedirs(self.db_path, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        try:
            self.collection = self.client.get_or_create_collection(
                name="safetyagentic_memory",
                metadata={"description": "SafetyAgentic Agent Memories"}
            )
            print("SafetyAgentic Memory Simple initialise")
        except Exception as e:
            print(f"Erreur initialisation ChromaDB: {e}")
            raise
    
    def add_agent_memory(self, agent_id: str, user_id: str, content: str, metadata: Optional[Dict] = None) -> Dict:
        try:
            memory_id = f"{agent_id}_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            enhanced_metadata = {
                "agent_id": agent_id,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "source": "safetyagentic",
                **(metadata or {})
            }
            
            self.collection.add(
                documents=[content],
                metadatas=[enhanced_metadata],
                ids=[memory_id]
            )
            
            print(f"Memoire ajoutee: {memory_id}")
            return {"success": True, "memory_id": memory_id}
            
        except Exception as e:
            print(f"Erreur ajout memoire: {e}")
            return {"success": False, "error": str(e)}
    
    def search_agent_memories(self, agent_id: str, user_id: str, query: str, limit: int = 5) -> List[Dict]:
        try:
            # CORRECTION: Syntaxe ChromaDB correcte pour filtres
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where={"$and": [
                    {"agent_id": {"$eq": agent_id}},
                    {"user_id": {"$eq": user_id}}
                ]}
            )
            
            memories = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    memory = {
                        "id": results['ids'][0][i],
                        "content": doc,
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if 'distances' in results else None
                    }
                    memories.append(memory)
            
            print(f"{len(memories)} memoires trouvees pour {agent_id}")
            return memories
            
        except Exception as e:
            print(f"Erreur recherche: {e}")
            # Fallback: récupérer toutes les mémoires de cet agent/user
            try:
                all_results = self.collection.get(
                    where={"$and": [
                        {"agent_id": {"$eq": agent_id}},
                        {"user_id": {"$eq": user_id}}
                    ]}
                )
                memories = []
                if all_results['documents']:
                    for i, doc in enumerate(all_results['documents']):
                        memory = {
                            "id": all_results['ids'][i],
                            "content": doc,
                            "metadata": all_results['metadatas'][i]
                        }
                        memories.append(memory)
                print(f"Fallback: {len(memories)} memoires recuperees pour {agent_id}")
                return memories
            except:
                return []
    
    def get_memory_stats(self) -> Dict:
        try:
            count = self.collection.count()
            return {
                "total_memories": count,
                "collection_name": "safetyagentic_memory",
                "status": "operational",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

def test_simple_memory():
    try:
        print("Test SafetyAgentic Memory Simple")
        print("=" * 40)
        
        memory = SafetyAgenticMemorySimple()
        
        result = memory.add_agent_memory(
            "A1", 
            "test_user",
            "Incident chute hauteur - EPI manquant, formation insuffisante",
            {"secteur": "construction", "gravite": "majeur"}
        )
        print("Test ajout:", result)
        
        memories = memory.search_agent_memories("A1", "test_user", "incident construction", limit=3)
        print(f"Test recherche: {len(memories)} memoires trouvees")
        
        stats = memory.get_memory_stats()
        print("Test stats:", stats)
        
        return True
        
    except Exception as e:
        print(f"Test echoue: {e}")
        return False

if __name__ == "__main__":
    test_simple_memory()
