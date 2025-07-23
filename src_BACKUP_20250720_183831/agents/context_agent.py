"""Context Agent - Enrichissement du contexte métier"""

from typing import Dict, Any, List
from ..core.state import SafetyState, SectorType, IntentType
from ..core.config import config

def context_agent(state: SafetyState) -> Dict[str, Any]:
    """
    Agent Context - Enrichit le contexte avec données sectorielles et métier
    
    Args:
        state: État SafeGraph actuel
        
    Returns:
        Dict avec contexte enrichi
    """
    
    # Ajouter trace
    state["agent_trace"].append("context_agent")
    
    try:
        current_context = state.get("context", {})
        intent = state.get("intent")
        scian_sector = state.get("scian_sector")
        user_input = state.get("user_input", "")
        
        # Enrichissement par secteur SCIAN
        sector_context = _get_sector_context(scian_sector)
        
        # Enrichissement par intention
        intent_context = _get_intent_context(intent)
        
        # Extraction d'entités métier
        business_entities = _extract_business_entities(user_input)
        
        # Contexte de risques par secteur
        risk_context = _get_risk_context(scian_sector)
        
        # Fusion des contextes
        enriched_context = {
            **current_context,
            "sector_info": sector_context,
            "intent_info": intent_context,
            "business_entities": business_entities,
            "risk_factors": risk_context,
            "enrichment_timestamp": state["timestamp"]
        }
        
        # Profil utilisateur basique
        user_profile = {
            "sector": scian_sector,
            "query_complexity": _assess_query_complexity(user_input),
            "expected_output": _determine_expected_output(intent),
            "language": "fr"  # Détection basique
        }
        
        return {
            "context": enriched_context,
            "user_profile": user_profile
        }
        
    except Exception as e:
        return {
            "errors": [f"Erreur Context Agent: {str(e)}"],
            "context": {"error_details": str(e)}
        }

def _get_sector_context(scian_sector: str) -> Dict[str, Any]:
    """Obtient le contexte spécifique au secteur SCIAN"""
    
    sector_info = {
        "236": {
            "name": "Construction",
            "key_risks": ["chutes", "équipements", "espaces_confinés"],
            "regulations": ["CNESST", "codes_bâtiment"],
            "typical_roles": ["ouvrier", "chef_chantier", "superviseur"],
            "priority_metrics": ["taux_incidents", "conformité_EPI", "formation"]
        },
        "484": {
            "name": "Transport routier", 
            "key_risks": ["fatigue", "accidents_route", "manutention"],
            "regulations": ["Transport_Canada", "temps_conduite"],
            "typical_roles": ["conducteur", "dispatcher", "mécanicien"],
            "priority_metrics": ["heures_conduite", "incidents_route", "maintenance"]
        },
        "622": {
            "name": "Santé",
            "key_risks": ["infections", "ergonomie", "stress"],
            "regulations": ["santé_publique", "CNESST_santé"],
            "typical_roles": ["infirmier", "médecin", "préposé"],
            "priority_metrics": ["infections_nosocomial", "burnout", "erreurs_médication"]
        },
        "811": {
            "name": "Maintenance industrielle",
            "key_risks": ["machines", "électricité", "produits_chimiques"],
            "regulations": ["CNESST_industrie", "codes_électriques"],
            "typical_roles": ["technicien", "électricien", "mécanicien"],
            "priority_metrics": ["arrêts_machines", "incidents_électriques", "exposition_chimique"]
        },
        "561": {
            "name": "Sécurité privée",
            "key_risks": ["violence", "stress", "surveillance_prolongée"],
            "regulations": ["BSP", "formation_agents"],
            "typical_roles": ["agent_sécurité", "superviseur", "gardien"],
            "priority_metrics": ["incidents_violence", "vigilance", "conformité_formation"]
        }
    }
    
    return sector_info.get(scian_sector, {"name": "Non spécifié", "key_risks": [], "regulations": []})

def _get_intent_context(intent: IntentType) -> Dict[str, Any]:
    """Obtient le contexte spécifique à l'intention"""
    
    intent_info = {
        IntentType.EVALUATION: {
            "description": "Collecte et évaluation des données sécurité",
            "expected_inputs": ["questionnaires", "observations", "entretiens"],
            "expected_outputs": ["scores", "profils_risque", "rapports"],
            "next_steps": ["normalisation", "analyse"]
        },
        IntentType.ANALYSIS: {
            "description": "Analyse des risques et détection d'écarts",
            "expected_inputs": ["données_normalisées", "historiques", "benchmarks"],
            "expected_outputs": ["écarts", "prédictions", "corrélations"],
            "next_steps": ["recommandations", "plans_action"]
        },
        IntentType.RECOMMENDATION: {
            "description": "Génération de recommandations et plans d'action",
            "expected_inputs": ["analyses", "profils_risque", "contraintes"],
            "expected_outputs": ["plans_action", "formations", "mesures_correctives"],
            "next_steps": ["mise_en_œuvre", "suivi"]
        },
        IntentType.MONITORING: {
            "description": "Suivi des progrès et évaluation des résultats",
            "expected_inputs": ["données_suivi", "indicateurs", "feedback"],
            "expected_outputs": ["rapports_progrès", "alertes", "ajustements"],
            "next_steps": ["amélioration_continue"]
        },
        IntentType.RESEARCH: {
            "description": "Recherche documentaire et benchmarking",
            "expected_inputs": ["requêtes", "domaines", "critères"],
            "expected_outputs": ["études", "références", "bonnes_pratiques"],
            "next_steps": ["application", "adaptation"]
        }
    }
    
    return intent_info.get(intent, {"description": "Intention non définie"})

def _extract_business_entities(text: str) -> List[str]:
    """Extrait les entités métier du texte"""
    
    # Entités SST courantes
    sst_entities = [
        "EPI", "casque", "gants", "chaussures_sécurité",
        "formation", "sensibilisation", "audit",
        "incident", "accident", "quasi_accident",
        "risque", "danger", "exposition",
        "procédure", "protocole", "consigne",
        "surveillance", "inspection", "contrôle"
    ]
    
    text_lower = text.lower()
    found_entities = [entity for entity in sst_entities if entity.lower() in text_lower]
    
    return found_entities

def _get_risk_context(scian_sector: str) -> Dict[str, Any]:
    """Obtient le contexte des risques par secteur"""
    
    risk_matrices = {
        "236": {"high": ["chutes_hauteur"], "medium": ["coupures", "contusions"], "low": ["fatigue"]},
        "484": {"high": ["accidents_mortels"], "medium": ["fatigue_conduite"], "low": ["inconfort"]},
        "622": {"high": ["infections_graves"], "medium": ["TMS"], "low": ["stress_léger"]},
        "811": {"high": ["électrocution"], "medium": ["coupures"], "low": ["bruit"]},
        "561": {"high": ["violence"], "medium": ["stress"], "low": ["fatigue"]}
    }
    
    return risk_matrices.get(scian_sector, {"high": [], "medium": [], "low": []})

def _assess_query_complexity(text: str) -> str:
    """Évalue la complexité de la requête"""
    
    word_count = len(text.split())
    technical_terms = ["analyse", "prédiction", "corrélation", "benchmark", "matrice"]
    
    if word_count > 20 or any(term in text.lower() for term in technical_terms):
        return "complex"
    elif word_count > 10:
        return "medium"
    else:
        return "simple"

def _determine_expected_output(intent: IntentType) -> str:
    """Détermine le type de sortie attendu"""
    
    output_mapping = {
        IntentType.EVALUATION: "rapport_evaluation",
        IntentType.ANALYSIS: "analyse_risques",
        IntentType.RECOMMENDATION: "plan_action",
        IntentType.MONITORING: "rapport_suivi",
        IntentType.RESEARCH: "synthese_recherche"
    }
    
    return output_mapping.get(intent, "rapport_general")