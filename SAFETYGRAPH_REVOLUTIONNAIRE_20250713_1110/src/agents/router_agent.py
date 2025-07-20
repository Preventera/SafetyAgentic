"""Router Agent - Classification des intentions utilisateur (Version Claude)"""

import re
from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from ..core.state import SafetyState, IntentType
from ..core.config import config
from ..utils.llm_factory import get_preferred_llm

# Template de prompt pour classification d'intention
INTENT_CLASSIFICATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Tu es un expert en classification d'intentions pour SafeGraph, 
    système d'analyse de culture sécurité.
    
    Analyse la requête utilisateur et détermine l'intention principale parmi :
    - EVALUATION : Collecte de données, autoévaluations, questionnaires
    - ANALYSIS : Analyse de risques, détection d'écarts, prédictions
    - RECOMMENDATION : Génération de plans d'action, recommandations
    - MONITORING : Suivi des progrès, évaluation des résultats
    - RESEARCH : Recherche documentaire, benchmarks sectoriels
    - UNKNOWN : Intention non claire ou hors scope
    
    Secteurs SCIAN supportés : Construction (236), Transport (484), Santé (622), 
    Maintenance (811), Sécurité privée (561)
    
    Réponds uniquement avec le nom de l'intention en majuscules."""),
    ("human", "Requête utilisateur : {user_input}")
])

def router_agent(state: SafetyState) -> Dict[str, Any]:
    """
    Agent Router - Détermine l'intention de la requête utilisateur
    
    Args:
        state: État SafeGraph actuel
        
    Returns:
        Dict avec l'intention classifiée et contexte initial
    """
    
    # Ajouter trace
    state["agent_trace"].append("router_agent")
    
    user_input = state.get("user_input", "")
    
    if not user_input:
        return {
            "intent": IntentType.UNKNOWN,
            "errors": ["Aucune entrée utilisateur fournie"]
        }
    
    try:
        # Détection par mots-clés (fallback si pas d'API)
        intent = _detect_intent_by_keywords(user_input)
        confidence = 0.7
        
        # Classification par LLM si API disponible
        if config.preferred_llm != "none":
            try:
                llm = get_preferred_llm(temperature=0.1)
                chain = INTENT_CLASSIFICATION_PROMPT | llm
                response = chain.invoke({"user_input": user_input})
                intent_str = response.content.strip().upper()
                
                # Conversion en IntentType
                intent_mapping = {
                    "EVALUATION": IntentType.EVALUATION,
                    "ANALYSIS": IntentType.ANALYSIS,
                    "RECOMMENDATION": IntentType.RECOMMENDATION,
                    "MONITORING": IntentType.MONITORING,
                    "RESEARCH": IntentType.RESEARCH,
                    "UNKNOWN": IntentType.UNKNOWN
                }
                
                llm_intent = intent_mapping.get(intent_str, IntentType.UNKNOWN)
                if llm_intent != IntentType.UNKNOWN:
                    intent = llm_intent
                    confidence = 0.9
                    
            except Exception as e:
                # Fallback vers détection mots-clés
                print(f"Fallback classification: {e}")
        
        # Détection de secteur SCIAN
        detected_sector = _detect_sector(user_input)
        
        # Contexte initial
        initial_context = {
            "original_query": user_input,
            "detected_keywords": _extract_keywords(user_input),
            "confidence_score": confidence,
            "routing_timestamp": state["timestamp"],
            "llm_used": config.preferred_llm
        }
        
        return {
            "intent": intent,
            "context": initial_context,
            "scian_sector": detected_sector
        }
        
    except Exception as e:
        return {
            "intent": IntentType.UNKNOWN,
            "errors": [f"Erreur Router Agent: {str(e)}"],
            "context": {"error_details": str(e)}
        }

def _detect_intent_by_keywords(user_input: str) -> IntentType:
    """Détection d'intention par mots-clés (fallback)"""
    
    user_lower = user_input.lower()
    
    # Mots-clés par intention
    evaluation_keywords = ["évaluation", "évaluer", "questionnaire", "autoévaluation", "collecte"]
    analysis_keywords = ["analyse", "analyser", "risque", "écart", "prédiction", "détection"]
    recommendation_keywords = ["recommandation", "plan", "action", "amélioration", "conseil"]
    monitoring_keywords = ["suivi", "monitoring", "progrès", "évolution", "surveillance"]
    research_keywords = ["recherche", "benchmark", "étude", "documentation", "référence"]
    
    # Scoring par intention
    scores = {
        IntentType.EVALUATION: sum(1 for kw in evaluation_keywords if kw in user_lower),
        IntentType.ANALYSIS: sum(1 for kw in analysis_keywords if kw in user_lower),
        IntentType.RECOMMENDATION: sum(1 for kw in recommendation_keywords if kw in user_lower),
        IntentType.MONITORING: sum(1 for kw in monitoring_keywords if kw in user_lower),
        IntentType.RESEARCH: sum(1 for kw in research_keywords if kw in user_lower)
    }
    
    # Intention avec le score le plus élevé
    max_intent = max(scores.items(), key=lambda x: x[1])
    
    return max_intent[0] if max_intent[1] > 0 else IntentType.UNKNOWN

def _detect_sector(user_input: str) -> str:
    """Détection de secteur SCIAN par mots-clés"""
    
    sector_keywords = {
        "236": ["construction", "chantier", "btp", "bâtiment", "travaux"],
        "484": ["transport", "conduite", "chauffeur", "camion", "livraison"],
        "622": ["hôpital", "santé", "soins", "médical", "infirmier"],
        "811": ["maintenance", "réparation", "technique", "entretien"],
        "561": ["sécurité", "surveillance", "gardien", "protection"]
    }
    
    user_lower = user_input.lower()
    
    for sector, keywords in sector_keywords.items():
        if any(keyword in user_lower for keyword in keywords):
            return sector
    
    return None

def _extract_keywords(user_input: str) -> list:
    """Extrait les mots-clés pertinents"""
    
    sst_keywords = [
        "sécurité", "risque", "danger", "accident", "incident",
        "formation", "prévention", "EPI", "procédure", "audit"
    ]
    
    user_lower = user_input.lower()
    found_keywords = [kw for kw in sst_keywords if kw in user_lower]
    
    return found_keywords