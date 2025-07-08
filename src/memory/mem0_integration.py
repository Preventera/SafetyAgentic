"""
Configuration Mem0 Simplifiée pour SafetyAgentic
================================================

Version qui fonctionne sans API keys externes
"""

import chromadb
import os
import json
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SafetyAgenticMemorySimple:
    """
    Version simplifiée utilisant directement ChromaDB
    sans dépendre des API keys externes
    """
    
    def __init__(self):
        """Initialise la mémoire simple avec ChromaDB uniquement"""
        self.db_path = "data/memory_vectorstore"
        os.makedirs(self.db_path, exist_ok=True)
        
        # Client ChromaDB persistant
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Collection pour SafetyAgentic
        try:
            self.collection = self.client.get_or_create_collection(
                name="safetyagentic_memory",
                metadata={"description": "SafetyAgentic Agent Memories"}
            )
            logger.info("✅ SafetyAgentic Memory Simple initialisé")
        except Exception as e:
            logger.error(f"❌ Erreur initialisation ChromaDB: {e}")
            raise
    
    def add_agent_memory(self, 
                        agent_id: str, 
                        user_id: str, 
                        content: str,
                        metadata: Optional[Dict] = None) -> Dict:
        """
        Ajoute une mémoire pour un agent
        
        Args:
            agent_id: ID de l'agent (A1, A2, etc.)
            user_id: ID utilisateur
            content: Contenu à mémoriser
            metadata: Métadonnées additionnelles
        """
        try:
            # ID unique pour cette mémoire
            memory_id = f"{agent_id}_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Métadonnées enrichies
            enhanced_metadata = {
                "agent_id": agent_id,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "source": "safetyagentic",
                **(metadata or {})
            }
            
            # Ajouter à ChromaDB
            self.collection.add(
                documents=[content],
                metadatas=[enhanced_metadata],
                ids=[memory_id]
            )
            
            logger.info(f"✅ Mémoire ajoutée: {memory_id}")
            return {"success": True, "memory_id": memory_id}
            
        except Exception as e:
            logger.error(f"❌ Erreur ajout mémoire: {e}")
            return {"success": False, "error": str(e)}
    
    def search_agent_memories(self, 
                             agent_id: str,
                             user_id: str, 
                             query: str, 
                             limit: int = 5) -> List[Dict]:
        """
        Recherche des mémoires pertinentes
        
        Args:
            agent_id: ID de l'agent
            user_id: ID utilisateur
            query: Requête de recherche
            limit: Nombre max de résultats
        """
        try:
            # Recherche sémantique
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where={
                    "$and": [
                        {"agent_id": {"$eq": agent_id}},
                        {"user_id": {"$eq": user_id}}
                    ]
                }
            )
            
            # Formater résultats
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
            
            logger.info(f"✅ {len(memories)} mémoires trouvées pour {agent_id}")
            return memories
            
        except Exception as e:
            logger.error(f"❌ Erreur recherche: {e}")
            return []
    
    def get_all_agent_memories(self, agent_id: str, user_id: str) -> List[Dict]:
        """Récupère toutes les mémoires d'un agent"""
        try:
            results = self.collection.get(
                where={
                    "$and": [
                        {"agent_id": {"$eq": agent_id}},
                        {"user_id": {"$eq": user_id}}
                    ]
                }
            )
            
            memories = []
            if results['documents']:
                for i, doc in enumerate(results['documents']):
                    memory = {
                        "id": results['ids'][i],
                        "content": doc,
                        "metadata": results['metadatas'][i]
                    }
                    memories.append(memory)
            
            return memories
            
        except Exception as e:
            logger.error(f"❌ Erreur récupération: {e}")
            return []
    
    def get_memory_stats(self) -> Dict:
        """Statistiques de la mémoire"""
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
    """Test de la mémoire simplifiée"""
    try:
        print("🧠 Test SafetyAgentic Memory Simple")
        print("=" * 40)
        
        # Initialiser
        memory = SafetyAgenticMemorySimple()
        
        # Test ajout
        result = memory.add_agent_memory(
            "A1", 
            "test_user",
            "Incident chute hauteur - EPI manquant, formation insuffisante",
            {"secteur": "construction", "gravite": "majeur"}
        )
        print("✅ Test ajout:", result)
        
        # Test recherche
        memories = memory.search_agent_memories(
            "A1", 
            "test_user", 
            "incident construction",
            limit=3
        )
        print(f"✅ Test recherche: {len(memories)} mémoires trouvées")
        
        # Test stats
        stats = memory.get_memory_stats()
        print("✅ Test stats:", stats)
        
        return True
        
    except Exception as e:
        print(f"❌ Test échoué: {e}")
        return False

if __name__ == "__main__":
    test_simple_memory()