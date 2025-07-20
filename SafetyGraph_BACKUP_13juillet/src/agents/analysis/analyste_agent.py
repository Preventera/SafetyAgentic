"""Analyste Agent (AN1) - Analyse des écarts et risques"""

from typing import Dict, Any, List
from datetime import datetime
import statistics
from ...core.state import SafetyState
from ...core.config import config

# Benchmarks sectoriels (données simulées)
SECTORIAL_BENCHMARKS = {
    "236": {  # Construction
        "industry_averages": {
            "Q1": 4.2,  # Port du casque
            "Q2": 3.8,  # Vérification EPI
            "Q3": 3.9,  # Signalement dangers
            "Q4": 4.1,  # Respect zones sécurité
            "Q5": 3.7,  # Confiance sécurité
            "global": 3.94
        },
        "thresholds": {
            "critical": 2.0,
            "at_risk": 3.0,
            "safe": 4.0
        }
    },
    "484": {  # Transport
        "industry_averages": {
            "Q1": 4.0,  # Respect temps repos
            "Q2": 3.5,  # Signalement fatigue
            "Q3": 4.3,  # Vérification véhicule
            "Q4": 4.1,  # Respect vitesse
            "Q5": 3.8,  # Vigilance conduite
            "global": 3.94
        },
        "thresholds": {
            "critical": 2.0,
            "at_risk": 3.0,
            "safe": 4.0
        }
    },
    "622": {  # Santé
        "industry_averages": {
            "Q1": 4.5,  # Hygiène mains
            "Q2": 4.2,  # Vérification patients
            "Q3": 3.6,  # Signalement erreurs
            "Q4": 3.4,  # Gestion stress
            "Q5": 3.8,  # Soutien équipe
            "global": 3.9
        },
        "thresholds": {
            "critical": 2.0,
            "at_risk": 3.0,
            "safe": 4.0
        }
    }
}

def analyste_agent(state: SafetyState) -> Dict[str, Any]:
    """
    Agent Analyste (AN1) - Analyse écarts et évaluation des risques
    
    Args:
        state: État SafeGraph actuel
        
    Returns:
        Dict avec analyse des écarts et scores de risque
    """
    
    # Ajouter trace
    state["agent_trace"].append("analyste_agent")
    
    try:
        collection_results = state.get("collection_results", [])
        scian_sector = state.get("scian_sector")
        
        if not collection_results:
            return {
                "errors": ["Aucune donnée collectée à analyser"],
                "analysis": {},
                "risk_scores": {}
            }
        
        # Analyse principale sur les dernières données collectées
        latest_data = collection_results[-1]
        
        # Analyse des écarts par rapport aux benchmarks
        gap_analysis = _analyze_gaps(latest_data, scian_sector)
        
        # Calcul des scores de risque
        risk_assessment = _assess_risks(latest_data, gap_analysis)
        
        # Détection de patterns comportementaux
        behavioral_patterns = _detect_behavioral_patterns(latest_data)
        
        # Prédictions de risque
        risk_predictions = _predict_risk_trends(latest_data, scian_sector)
        
        # Analyse consolidée
        analysis_result = {
            "gap_analysis": gap_analysis,
            "behavioral_patterns": behavioral_patterns,
            "risk_classification": risk_assessment["classification"],
            "key_findings": _extract_key_findings(gap_analysis, risk_assessment),
            "analysis_timestamp": datetime.now().isoformat(),
            "data_quality": latest_data.get("completion_rate", 0.0)
        }
        
        return {
            "analysis": analysis_result,
            "risk_scores": risk_assessment["scores"],
            "predictions": risk_predictions
        }
        
    except Exception as e:
        return {
            "errors": [f"Erreur Analyste Agent: {str(e)}"],
            "analysis": {},
            "risk_scores": {}
        }

def _analyze_gaps(data: Dict[str, Any], scian_sector: str) -> Dict[str, Any]:
    """Analyse les écarts par rapport aux benchmarks sectoriels"""
    
    sector_benchmarks = SECTORIAL_BENCHMARKS.get(scian_sector, {})
    industry_averages = sector_benchmarks.get("industry_averages", {})
    
    if not industry_averages:
        return {"error": "Benchmarks non disponibles pour ce secteur"}
    
    responses = data.get("responses", {})
    gaps = {}
    
    for question_id, response in responses.items():
        user_score = response["value"]
        industry_avg = industry_averages.get(question_id, 3.0)
        
        gap = user_score - industry_avg
        gap_percentage = (gap / industry_avg) * 100
        
        gaps[question_id] = {
            "user_score": user_score,
            "industry_average": industry_avg,
            "absolute_gap": round(gap, 2),
            "percentage_gap": round(gap_percentage, 1),
            "performance": "above" if gap > 0 else "below" if gap < 0 else "equal"
        }
    
    # Gap global
    user_global = statistics.mean([r["value"] for r in responses.values()])
    industry_global = industry_averages.get("global", 3.0)
    global_gap = user_global - industry_global
    
    gaps["global"] = {
        "user_score": round(user_global, 2),
        "industry_average": industry_global,
        "absolute_gap": round(global_gap, 2),
        "percentage_gap": round((global_gap / industry_global) * 100, 1),
        "performance": "above" if global_gap > 0 else "below" if global_gap < 0 else "equal"
    }
    
    return gaps

def _assess_risks(data: Dict[str, Any], gap_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Évalue les niveaux de risque"""
    
    responses = data.get("responses", {})
    risk_scores = {}
    
    # Scores de risque par question (inversé: score bas = risque élevé)
    for question_id, response in responses.items():
        score = response["value"]
        
        # Conversion score en niveau de risque (1-5 → 5-1)
        risk_level = 6 - score
        
        # Classification du risque
        if risk_level <= 2:
            risk_category = "Low"
        elif risk_level <= 3:
            risk_category = "Medium" 
        else:
            risk_category = "High"
        
        risk_scores[question_id] = {
            "risk_level": risk_level,
            "risk_category": risk_category,
            "confidence": 0.8,  # Confiance dans l'évaluation
            "contributing_factors": _identify_risk_factors(question_id, score)
        }
    
    # Risque global
    avg_risk = statistics.mean([rs["risk_level"] for rs in risk_scores.values()])
    
    if avg_risk <= 2:
        global_classification = "Safe"
    elif avg_risk <= 3:
        global_classification = "At-Risk"
    else:
        global_classification = "High-Risk"
    
    risk_scores["global"] = {
        "risk_level": round(avg_risk, 2),
        "risk_category": global_classification,
        "confidence": 0.85
    }
    
    return {
        "scores": risk_scores,
        "classification": global_classification
    }

def _detect_behavioral_patterns(data: Dict[str, Any]) -> Dict[str, Any]:
    """Détecte des patterns comportementaux"""
    
    responses = data.get("responses", {})
    metadata = data.get("metadata", {})
    
    if not responses:
        return {}
    
    scores = [r["value"] for r in responses.values()]
    response_times = [r["response_time"] for r in responses.values()]
    
    patterns = {
        "consistency": {
            "score": 1 - (statistics.stdev(scores) / 4),  # Cohérence des réponses
            "interpretation": "consistent" if statistics.stdev(scores) < 1 else "variable"
        },
        "engagement": {
            "avg_response_time": statistics.mean(response_times),
            "interpretation": "high" if statistics.mean(response_times) > 5 else "medium"
        },
        "bias_tendency": {
            "central_tendency": statistics.mean(scores),
            "interpretation": "positive_bias" if statistics.mean(scores) > 3.5 else "realistic"
        },
        "completion_quality": {
            "interruptions": metadata.get("interruptions", 0),
            "session_quality": metadata.get("session_quality", "unknown")
        }
    }
    
    return patterns

def _predict_risk_trends(data: Dict[str, Any], scian_sector: str) -> Dict[str, Any]:
    """Prédit les tendances de risque"""
    
    responses = data.get("responses", {})
    
    if not responses:
        return {}
    
    avg_score = statistics.mean([r["value"] for r in responses.values()])
    
    # Prédiction basique basée sur le score moyen
    if avg_score >= 4.0:
        trend = "improving"
        risk_probability = 0.2
    elif avg_score >= 3.0:
        trend = "stable"
        risk_probability = 0.4
    else:
        trend = "declining"
        risk_probability = 0.7
    
    return {
        "6_month_trend": trend,
        "incident_probability": risk_probability,
        "recommended_monitoring": "monthly" if risk_probability > 0.5 else "quarterly",
        "prediction_confidence": 0.7
    }

def _identify_risk_factors(question_id: str, score: int) -> List[str]:
    """Identifie les facteurs de risque pour une question donnée"""
    
    # Facteurs de risque par type de question
    risk_factors_map = {
        "Q1": ["non_compliance", "equipment_issues", "training_gaps"],
        "Q2": ["awareness_low", "process_issues", "resource_constraints"],
        "Q3": ["communication_barriers", "fear_reporting", "culture_issues"],
        "Q4": ["supervision_gaps", "peer_pressure", "time_pressure"],
        "Q5": ["confidence_low", "support_lacking", "stress_high"]
    }
    
    base_factors = risk_factors_map.get(question_id, ["general_risk"])
    
    # Ajouter facteurs basés sur le score
    if score <= 2:
        base_factors.extend(["critical_gap", "immediate_attention"])
    elif score <= 3:
        base_factors.append("moderate_concern")
    
    return base_factors

def _extract_key_findings(gap_analysis: Dict[str, Any], risk_assessment: Dict[str, Any]) -> List[str]:
    """Extrait les conclusions clés de l'analyse"""
    
    findings = []
    
    # Analyse des gaps
    global_gap = gap_analysis.get("global", {})
    if global_gap.get("absolute_gap", 0) < -0.5:
        findings.append("Performance significativement en dessous de la moyenne sectorielle")
    elif global_gap.get("absolute_gap", 0) > 0.5:
        findings.append("Performance supérieure à la moyenne sectorielle")
    
    # Classification de risque
    risk_classification = risk_assessment.get("classification", "Unknown")
    if risk_classification == "High-Risk":
        findings.append("Profil de risque élevé nécessitant une attention immédiate")
    elif risk_classification == "At-Risk":
        findings.append("Profil de risque modéré nécessitant un suivi renforcé")
    
    # Identification des points faibles
    gaps = {k: v for k, v in gap_analysis.items() if k != "global"}
    weak_areas = [k for k, v in gaps.items() if v.get("absolute_gap", 0) < -0.3]
    
    if weak_areas:
        findings.append(f"Domaines nécessitant amélioration: {', '.join(weak_areas)}")
    
    return findings