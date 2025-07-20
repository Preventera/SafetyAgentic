"""Collecteur Agent (A1) - Collecte des autoévaluations et données"""

from typing import Dict, Any, List
from datetime import datetime
import random
from ...core.state import SafetyState
from ...core.config import config

# Questionnaire de base par secteur SCIAN
SECTORIAL_QUESTIONNAIRES = {
    "236": {  # Construction
        "name": "Évaluation Sécurité Construction",
        "questions": [
            {"id": "Q1", "text": "Je porte systématiquement mon casque sur le chantier", "type": "likert"},
            {"id": "Q2", "text": "Je vérifie l'état de mes EPI chaque matin", "type": "likert"},
            {"id": "Q3", "text": "Je signale immédiatement les situations dangereuses", "type": "likert"},
            {"id": "Q4", "text": "Je respecte les zones de sécurité balisées", "type": "likert"},
            {"id": "Q5", "text": "Je me sens confiant dans ma capacité à travailler en sécurité", "type": "likert"}
        ]
    },
    "484": {  # Transport
        "name": "Évaluation Sécurité Transport",
        "questions": [
            {"id": "Q1", "text": "Je respecte systématiquement les temps de repos", "type": "likert"},
            {"id": "Q2", "text": "Je signale immédiatement la fatigue excessive", "type": "likert"},
            {"id": "Q3", "text": "Je vérifie mon véhicule avant chaque trajet", "type": "likert"},
            {"id": "Q4", "text": "Je respecte les limitations de vitesse", "type": "likert"},
            {"id": "Q5", "text": "Je me sens vigilant pendant la conduite", "type": "likert"}
        ]
    },
    "622": {  # Santé
        "name": "Évaluation Sécurité Soins",
        "questions": [
            {"id": "Q1", "text": "Je respecte les protocoles d'hygiène des mains", "type": "likert"},
            {"id": "Q2", "text": "Je double-vérifie les identités patients", "type": "likert"},
            {"id": "Q3", "text": "Je signale les erreurs potentielles", "type": "likert"},
            {"id": "Q4", "text": "Je gère bien le stress des situations d'urgence", "type": "likert"},
            {"id": "Q5", "text": "Je me sens soutenu par mon équipe", "type": "likert"}
        ]
    }
}

def collecteur_agent(state: SafetyState) -> Dict[str, Any]:
    """
    Agent Collecteur (A1) - Collecte autoévaluations et données comportementales
    
    Args:
        state: État SafeGraph actuel
        
    Returns:
        Dict avec données collectées et questionnaires
    """
    
    # Ajouter trace
    state["agent_trace"].append("collecteur_agent")
    
    try:
        scian_sector = state.get("scian_sector")
        user_profile = state.get("user_profile", {})
        context = state.get("context", {})
        
        # Sélectionner questionnaire approprié
        questionnaire = _select_questionnaire(scian_sector)
        
        # Simuler la collecte de données (pour la démo)
        collected_data = _simulate_data_collection(questionnaire, user_profile)
        
        # Analyser les réponses collectées
        analysis_summary = _analyze_responses(collected_data)
        
        # Préparer les données pour l'analyse
        collection_result = {
            "questionnaire_id": questionnaire["name"],
            "sector": scian_sector,
            "responses": collected_data["responses"],
            "metadata": collected_data["metadata"],
            "preliminary_scores": analysis_summary["scores"],
            "completion_rate": analysis_summary["completion_rate"],
            "collection_timestamp": datetime.now().isoformat()
        }
        
        return {
            "collection_results": [collection_result],
            "questionnaire_data": {
                "selected_questionnaire": questionnaire,
                "total_questions": len(questionnaire["questions"]),
                "mandatory_completed": analysis_summary["completion_rate"] > 0.8
            }
        }
        
    except Exception as e:
        return {
            "errors": [f"Erreur Collecteur Agent: {str(e)}"],
            "collection_results": [],
            "questionnaire_data": {}
        }

def _select_questionnaire(scian_sector: str) -> Dict[str, Any]:
    """Sélectionne le questionnaire approprié selon le secteur"""
    
    if scian_sector in SECTORIAL_QUESTIONNAIRES:
        return SECTORIAL_QUESTIONNAIRES[scian_sector]
    
    # Questionnaire générique si secteur non supporté
    return {
        "name": "Évaluation Sécurité Générale",
        "questions": [
            {"id": "Q1", "text": "Je respecte les consignes de sécurité", "type": "likert"},
            {"id": "Q2", "text": "Je signale les situations dangereuses", "type": "likert"},
            {"id": "Q3", "text": "Je me sens formé pour mon poste", "type": "likert"},
            {"id": "Q4", "text": "Je fais confiance à mes collègues", "type": "likert"},
            {"id": "Q5", "text": "Je connais les procédures d'urgence", "type": "likert"}
        ]
    }

def _simulate_data_collection(questionnaire: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Simule la collecte de données pour la démo"""
    
    # Pour la démo, on simule des réponses réalistes
    responses = {}
    
    for question in questionnaire["questions"]:
        if question["type"] == "likert":
            # Échelle Likert 1-5 avec biais réaliste
            score = random.choices(
                [1, 2, 3, 4, 5],
                weights=[5, 10, 20, 40, 25]  # Biais vers réponses positives
            )[0]
            responses[question["id"]] = {
                "value": score,
                "text": question["text"],
                "response_time": random.randint(3, 15)  # secondes
            }
    
    metadata = {
        "user_id": user_profile.get("user_id", f"user_{random.randint(1000, 9999)}"),
        "completion_time": sum(r["response_time"] for r in responses.values()),
        "device": "web",
        "session_quality": "good",
        "interruptions": random.randint(0, 2)
    }
    
    return {
        "responses": responses,
        "metadata": metadata
    }

def _analyze_responses(collected_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyse préliminaire des réponses collectées"""
    
    responses = collected_data["responses"]
    
    if not responses:
        return {
            "scores": {},
            "completion_rate": 0.0,
            "quality_indicators": {}
        }
    
    # Calcul scores préliminaires
    scores = {}
    total_score = 0
    
    for question_id, response in responses.items():
        score = response["value"]
        scores[question_id] = {
            "raw_score": score,
            "normalized": (score - 1) / 4,  # Normalisation 0-1
            "percentile": score * 20  # Conversion approximative en percentile
        }
        total_score += score
    
    # Score global
    avg_score = total_score / len(responses) if responses else 0
    scores["global"] = {
        "raw_score": avg_score,
        "normalized": (avg_score - 1) / 4,
        "percentile": avg_score * 20
    }
    
    # Indicateurs de qualité
    response_times = [r["response_time"] for r in responses.values()]
    quality_indicators = {
        "avg_response_time": sum(response_times) / len(response_times),
        "consistency_score": _calculate_consistency(list(responses.values())),
        "engagement_level": "high" if all(r["response_time"] > 2 for r in responses.values()) else "medium"
    }
    
    return {
        "scores": scores,
        "completion_rate": len(responses) / 5,  # Supposant 5 questions standard
        "quality_indicators": quality_indicators
    }

def _calculate_consistency(responses: List[Dict[str, Any]]) -> float:
    """Calcule un score de cohérence des réponses"""
    
    if len(responses) < 2:
        return 1.0
    
    values = [r["value"] for r in responses]
    
    # Écart-type comme indicateur de cohérence (inversé)
    import statistics
    
    try:
        std_dev = statistics.stdev(values)
        # Cohérence élevée = faible écart-type
        consistency = max(0, 1 - (std_dev / 2))  # Normalisation approximative
        return round(consistency, 2)
    except:
        return 0.5  # Valeur par défaut