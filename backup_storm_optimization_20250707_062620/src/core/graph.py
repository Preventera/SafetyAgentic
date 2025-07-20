"""GraphQL principal SafeGraph avec orchestration LangGraph"""

from langgraph.graph import StateGraph, START, END
from typing import Literal
from .state import SafetyState, IntentType

def create_safety_graph() -> StateGraph:
    """Crée le graphe principal SafeGraph"""
    
    # Import dynamique des agents pour éviter les imports circulaires
    from ..agents.router_agent import router_agent
    from ..agents.context_agent import context_agent
    from ..agents.evaluation.collecteur_agent import collecteur_agent
    from ..agents.analysis.analyste_agent import analyste_agent
    from ..agents.recommendation.recommandation_agent import recommandation_agent
    
    # Initialiser le StateGraph
    workflow = StateGraph(SafetyState)
    
    # Ajouter les nœuds (agents)
    workflow.add_node("router", router_agent)
    workflow.add_node("context_enricher", context_agent)
    workflow.add_node("collecteur", collecteur_agent)
    workflow.add_node("analyste", analyste_agent)
    workflow.add_node("recommandation", recommandation_agent)
    
    # Point d'entrée
    workflow.add_edge(START, "router")
    
    # Transitions conditionnelles basées sur l'intention
    workflow.add_conditional_edges(
        "router",
        route_by_intent,
        {
            "evaluation": "context_enricher",
            "analysis": "context_enricher", 
            "recommendation": "context_enricher",
            "monitoring": "context_enricher",
            "research": "context_enricher",
            "end": END
        }
    )
    
    # Flux principal après enrichissement contexte
    workflow.add_edge("context_enricher", "collecteur")
    workflow.add_edge("collecteur", "analyste") 
    workflow.add_edge("analyste", "recommandation")
    workflow.add_edge("recommandation", END)
    
    return workflow.compile()

def route_by_intent(state: SafetyState) -> Literal["evaluation", "analysis", "recommendation", "monitoring", "research", "end"]:
    """Détermine la route basée sur l'intention détectée"""
    
    # Ajouter trace de l'agent
    state["agent_trace"].append("route_by_intent")
    
    if not state.get("intent"):
        return "end"
    
    intent = state["intent"]
    
    # Mapper les intentions vers les routes
    intent_routes = {
        IntentType.EVALUATION: "evaluation",
        IntentType.ANALYSIS: "analysis", 
        IntentType.RECOMMENDATION: "recommendation",
        IntentType.MONITORING: "monitoring",
        IntentType.RESEARCH: "research"
    }
    
    return intent_routes.get(intent, "end")