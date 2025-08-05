"""
Bridge pour connecter avec SafetyAgentic et ses 100 agents
"""
import os
import httpx
from typing import Dict, Any

class SafetyAgenticBridge:
    """Connecteur pour utiliser les agents SafetyAgentic"""
    
    def __init__(self):
        self.base_url = os.getenv("SAFETYAGENTIC_URL", "http://localhost:8000")
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def invoke_agent(self, agent_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoque un agent SafetyAgentic (A1-A50, SC1-SC50)
        
        Args:
            agent_id: Identifiant de l'agent (ex: "A1", "SC1")
            data: Données à traiter
            
        Returns:
            Résultat de l'agent
        """
        endpoint = f"{self.base_url}/agents/{agent_id}/invoke"
        
        try:
            response = await self.client.post(endpoint, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "agent_id": agent_id}
    
    async def get_safety_graph(self, query: str) -> Dict[str, Any]:
        """Récupère les données du Safety Graph Neo4j"""
        endpoint = f"{self.base_url}/graph/query"
        
        try:
            response = await self.client.post(
                endpoint,
                json={"cypher": query}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
