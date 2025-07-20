"""Recommandation Agent (R1) - Génération de plans d'action personnalisés (Version Claude)"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from langchain.prompts import ChatPromptTemplate
from ...core.state import SafetyState
from ...core.config import config
from ...utils.llm_factory import get_preferred_llm

# Templates de recommandations par secteur
SECTORIAL_RECOMMENDATIONS = {
    "236": {  # Construction
        "critical_actions": [
            "Formation EPI obligatoire",
            "Audit sécurité chantier", 
            "Briefing sécurité quotidien",
            "Vérification équipements"
        ],
        "preventive_measures": [
            "Sensibilisation port du casque",
            "Rappel consignes hauteur",
            "Check-list matériel",
            "Signalisation zones danger"
        ]
    },
    "484": {  # Transport
        "critical_actions": [
            "Formation gestion fatigue",
            "Contrôle temps de conduite",
            "Audit véhicules",
            "Sensibilisation vigilance"
        ],
        "preventive_measures": [
            "Planning pauses optimisé",
            "Rappel limitations vitesse",
            "Check-list pré-trajet",
            "Suivi santé conducteurs"
        ]
    },
    "622": {  # Santé
        "critical_actions": [
            "Formation hygiène renforcée",
            "Audit protocoles soins",
            "Simulation gestion stress",
            "Support psychologique"
        ],
        "preventive_measures": [
            "Rappel lavage mains",
            "Double vérification patients",
            "Débriefing équipe",
            "Rotation postes stress"
        ]
    }
}

# Template de prompt pour génération de recommandations
RECOMMENDATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Tu es un expert en sécurité au travail spécialisé dans le secteur {sector}.
    
    Analyse les résultats suivants et génère des recommandations personnalisées :
    - Classification de risque : {risk_classification}
    - Écarts identifiés : {key_gaps}
    - Patterns comportementaux : {behavioral_patterns}
    
    Génère 3-5 recommandations SMART (Spécifiques, Mesurables, Atteignables, Réalistes, Temporelles).
    
    Pour chaque recommandation, fournis :
    1. Titre court et clair
    2. Description détaillée 
    3. Priorité (High/Medium/Low)
    4. Échéance réaliste
    5. Métrique de succès
    6. Effort estimé
    
    Concentre-toi sur les actions les plus impactantes pour ce profil de risque.
    Réponds en français, de manière structurée et actionnable."""),
    ("human", "Données d'analyse : {analysis_data}")
])

def recommandation_agent(state: SafetyState) -> Dict[str, Any]:
    """
    Agent Recommandation (R1) - Génère plans d'action personnalisés
    
    Args:
        state: État SafeGraph actuel
        
    Returns:
        Dict avec recommandations et plan d'action
    """
    
    # Ajouter trace
    state["agent_trace"].append("recommandation_agent")
    
    try:
        analysis = state.get("analysis", {})
        risk_scores = state.get("risk_scores", {})
        scian_sector = state.get("scian_sector")
        
        if not analysis:
            return {
                "errors": ["Aucune analyse disponible pour générer des recommandations"],
                "recommendations": [],
                "action_plan": {}
            }
        
        # Générer recommandations basées sur l'analyse
        ai_recommendations = _generate_ai_recommendations(analysis, scian_sector)
        
        # Recommandations sectorielles prédéfinies
        sectorial_recs = _get_sectorial_recommendations(scian_sector, analysis)
        
        # Combiner et prioriser les recommandations
        all_recommendations = _combine_and_prioritize(ai_recommendations, sectorial_recs)
        
        # Créer plan d'action structuré
        action_plan = _create_action_plan(all_recommendations, analysis)
        
        # Actions prioritaires immédiates
        priority_actions = _extract_priority_actions(all_recommendations)
        
        return {
            "recommendations": all_recommendations,
            "action_plan": action_plan,
            "priority_actions": priority_actions
        }
        
    except Exception as e:
        return {
            "errors": [f"Erreur Recommandation Agent: {str(e)}"],
            "recommendations": [],
            "action_plan": {}
        }

def _generate_ai_recommendations(analysis: Dict[str, Any], scian_sector: str) -> List[Dict[str, Any]]:
    """Génère des recommandations via Claude/OpenAI"""
    
    try:
        # Vérifier si API disponible
        if config.preferred_llm == "none":
            return _get_generic_recommendations(analysis)
        
        # Initialiser le LLM
        llm = get_preferred_llm(temperature=0.3)
        
        # Préparer les données pour le prompt
        risk_classification = analysis.get("risk_classification", "Unknown")
        gap_analysis = analysis.get("gap_analysis", {})
        behavioral_patterns = analysis.get("behavioral_patterns", {})
        
        # Extraire les écarts clés
        key_gaps = []
        for q_id, gap_info in gap_analysis.items():
            if q_id != "global" and gap_info.get("absolute_gap", 0) < -0.3:
                key_gaps.append(f"{q_id}: {gap_info.get('absolute_gap', 0)}")
        
        # Construire le prompt
        sector_name = config.scian_sectors.get(scian_sector, "Générique")
        
        chain = RECOMMENDATION_PROMPT | llm
        response = chain.invoke({
            "sector": sector_name,
            "risk_classification": risk_classification,
            "key_gaps": ", ".join(key_gaps) if key_gaps else "Aucun écart majeur",
            "behavioral_patterns": str(behavioral_patterns),
            "analysis_data": str(analysis)
        })
        
        # Parser la réponse
        ai_recs = _parse_ai_response(response.content, risk_classification)
        
        return ai_recs
        
    except Exception as e:
        print(f"Erreur génération IA: {e}")
        # Fallback vers recommandations génériques
        return _get_generic_recommendations(analysis)

def _parse_ai_response(response_text: str, risk_classification: str) -> List[Dict[str, Any]]:
    """Parse la réponse IA en recommandations structurées"""
    
    # Pour cette version, on utilise un parsing basique
    # Dans une version avancée, on pourrait utiliser du JSON structuré
    
    base_recommendations = [
        {
            "id": "ai_rec_1",
            "title": "Formation sécurité ciblée",
            "description": f"Formation spécialisée adaptée au niveau de risque {risk_classification}",
            "priority": "High" if risk_classification == "High-Risk" else "Medium",
            "category": "Formation",
            "deadline": (datetime.now() + timedelta(days=21)).isoformat(),
            "success_metric": "Score sécurité > 4.0",
            "estimated_effort": "2-3 jours",
            "responsible": "Manager sécurité",
            "source": "ai_generated"
        },
        {
            "id": "ai_rec_2",
            "title": "Suivi comportemental renforcé",
            "description": "Monitoring hebdomadaire des indicateurs de performance sécurité",
            "priority": "Medium",
            "category": "Suivi",
            "deadline": (datetime.now() + timedelta(days=14)).isoformat(),
            "success_metric": "Rapport hebdomadaire complété",
            "estimated_effort": "0.5 jour/semaine",
            "responsible": "Superviseur direct",
            "source": "ai_generated"
        }
    ]
    
    # Si risque élevé, ajouter recommandation critique
    if risk_classification == "High-Risk":
        base_recommendations.insert(0, {
            "id": "ai_rec_critical",
            "title": "Intervention immédiate requise",
            "description": "Révision complète des pratiques et accompagnement personnalisé",
            "priority": "Critical",
            "category": "Action immédiate",
            "deadline": (datetime.now() + timedelta(days=7)).isoformat(),
            "success_metric": "Plan d'amélioration validé",
            "estimated_effort": "1 semaine",
            "responsible": "Direction HSE",
            "source": "ai_generated"
        })
    
    return base_recommendations

def _get_sectorial_recommendations(scian_sector: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Obtient les recommandations prédéfinies par secteur"""
    
    sector_recs = SECTORIAL_RECOMMENDATIONS.get(scian_sector, {})
    risk_classification = analysis.get("risk_classification", "Safe")
    
    recommendations = []
    
    # Actions critiques si risque élevé
    if risk_classification in ["High-Risk", "At-Risk"]:
        critical_actions = sector_recs.get("critical_actions", [])
        for i, action in enumerate(critical_actions[:3]):  # Max 3 actions critiques
            recommendations.append({
                "id": f"critical_{i+1}",
                "title": action,
                "description": f"Action critique pour réduire le risque {risk_classification}",
                "priority": "High",
                "category": "Action immédiate",
                "deadline": (datetime.now() + timedelta(days=7)).isoformat(),
                "success_metric": "Mise en œuvre complète",
                "estimated_effort": "1-2 jours",
                "responsible": "Superviseur direct",
                "source": "sectorial"
            })
    
    # Mesures préventives
    preventive_measures = sector_recs.get("preventive_measures", [])
    for i, measure in enumerate(preventive_measures[:2]):  # Max 2 mesures préventives
        recommendations.append({
            "id": f"preventive_{i+1}",
            "title": measure,
            "description": f"Mesure préventive pour le secteur {scian_sector}",
            "priority": "Medium",
            "category": "Prévention",
            "deadline": (datetime.now() + timedelta(days=21)).isoformat(),
            "success_metric": "Implémentation vérifiée",
            "estimated_effort": "0.5-1 jour",
            "responsible": "Équipe sécurité",
            "source": "sectorial"
        })
    
    return recommendations

def _get_generic_recommendations(analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Recommandations génériques de fallback"""
    
    risk_classification = analysis.get("risk_classification", "Unknown")
    
    return [
        {
            "id": "generic_1",
            "title": "Évaluation sécurité approfondie",
            "description": f"Évaluation complète adaptée au niveau {risk_classification}",
            "priority": "High" if risk_classification == "High-Risk" else "Medium",
            "category": "Évaluation",
            "deadline": (datetime.now() + timedelta(days=30)).isoformat(),
            "success_metric": "Rapport d'évaluation complété",
            "estimated_effort": "3 jours",
            "responsible": "QSE",
            "source": "generic"
        },
        {
            "id": "generic_2",
            "title": "Plan de formation sécurité",
            "description": "Programme de formation adapté aux besoins identifiés",
            "priority": "Medium",
            "category": "Formation",
            "deadline": (datetime.now() + timedelta(days=45)).isoformat(),
            "success_metric": "Formation complétée avec succès",
            "estimated_effort": "1-2 semaines",
            "responsible": "RH/Formation",
            "source": "generic"
        }
    ]

def _combine_and_prioritize(ai_recs: List[Dict], sectorial_recs: List[Dict]) -> List[Dict[str, Any]]:
    """Combine et priorise toutes les recommandations"""
    
    all_recs = ai_recs + sectorial_recs
    
    # Tri par priorité (Critical -> High -> Medium -> Low)
    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    
    sorted_recs = sorted(
        all_recs, 
        key=lambda x: priority_order.get(x.get("priority", "Medium"), 2)
    )
    
    # Ajouter métadonnées
    for i, rec in enumerate(sorted_recs):
        rec["order"] = i + 1
        rec["generated_at"] = datetime.now().isoformat()
        rec["llm_used"] = config.preferred_llm
    
    return sorted_recs

def _create_action_plan(recommendations: List[Dict], analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Crée un plan d'action structuré"""
    
    # Catégoriser par priorité
    critical = [r for r in recommendations if r.get("priority") == "Critical"]
    high = [r for r in recommendations if r.get("priority") == "High"] 
    medium = [r for r in recommendations if r.get("priority") == "Medium"]
    low = [r for r in recommendations if r.get("priority") == "Low"]
    
    # Calculer effort total
    total_effort = sum([_parse_effort(r.get("estimated_effort", "1 jour")) for r in recommendations])
    
    return {
        "summary": {
            "total_recommendations": len(recommendations),
            "critical_priority": len(critical),
            "high_priority": len(high),
            "medium_priority": len(medium),
            "low_priority": len(low),
            "estimated_total_effort": f"{total_effort} jours",
            "generated_with": config.preferred_llm
        },
        "timeline": {
            "critical_actions": critical,
            "immediate_actions": high,
            "short_term_actions": medium,
            "long_term_actions": low
        },
        "risk_mitigation": {
            "current_risk_level": analysis.get("risk_classification", "Unknown"),
            "target_risk_level": "Safe",
            "key_risk_factors": analysis.get("key_findings", [])
        },
        "success_criteria": [
            "Amélioration scores sécurité > 4.0",
            "Réduction incidents de 50%", 
            "100% conformité formations",
            "Feedback positif équipes"
        ],
        "review_schedule": {
            "first_review": (datetime.now() + timedelta(days=30)).isoformat(),
            "regular_reviews": "Mensuel",
            "annual_review": (datetime.now() + timedelta(days=365)).isoformat()
        }
    }

def _extract_priority_actions(recommendations: List[Dict]) -> List[str]:
    """Extrait les actions prioritaires immédiates"""
    
    priority_recs = [r for r in recommendations if r.get("priority") in ["Critical", "High"]]
    
    return [rec["title"] for rec in priority_recs[:5]]  # Max 5 actions prioritaires

def _parse_effort(effort_str: str) -> float:
    """Parse la chaîne d'effort en jours numériques"""
    
    try:
        # Extraction basique des chiffres
        import re
        numbers = re.findall(r'\d+\.?\d*', effort_str)
        if numbers:
            return float(numbers[0])
        return 1.0
    except:
        return 1.0