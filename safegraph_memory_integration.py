"""
Intégration Mémoire IA dans SafeGraph Streamlit
==============================================

Module pour ajouter capacités mémoire Mem0 à l'interface SafeGraph existante
"""

import sys
import os
sys.path.append('src')

# Import de l'Agent A1 Enhanced avec mémoire
try:
    from agents.collecte.a1_enhanced_standalone import AgentA1EnhancedStandalone
    from memory.wrapper import get_memory, get_agent_context
    MEMORY_AVAILABLE = True
    print("✅ Mémoire IA Mem0 chargée")
except ImportError as e:
    MEMORY_AVAILABLE = False
    print(f"⚠️ Mémoire IA non disponible: {e}")

import streamlit as st
import json
from datetime import datetime

def render_memory_section():
    """Section mémoire IA dans la sidebar"""
    if MEMORY_AVAILABLE:
        st.sidebar.markdown("---")
        st.sidebar.subheader("🧠 Mémoire IA")
        
        try:
            memory = get_memory()
            stats = memory.get_memory_stats()
            total_memories = stats.get('total_memories', 0)
            
            if total_memories > 0:
                st.sidebar.success(f"✅ {total_memories} mémoires actives")
                
                if st.sidebar.button("📊 Détails Mémoire"):
                    st.sidebar.json(stats)
            else:
                st.sidebar.info("🆕 Première utilisation")
                
        except Exception as e:
            st.sidebar.error(f"❌ Erreur mémoire: {e}")
    else:
        st.sidebar.warning("⚠️ Mémoire IA désactivée")

def enhance_analysis_with_memory(analysis_text, user_company, secteur="236"):
    """
    Fonction pour enrichir une analyse avec la mémoire IA
    
    Args:
        analysis_text: Texte d'analyse de l'utilisateur
        user_company: Nom de l'entreprise
        secteur: Code secteur SCIAN
        
    Returns:
        dict: Résultats enrichis avec mémoire
    """
    if not MEMORY_AVAILABLE:
        return {"error": "Mémoire IA non disponible", "standard_mode": True}
    
    try:
        # Préparer données pour Agent A1 Enhanced
        analysis_data = {
            "questions": [
                {"question": "Analyse demandée", "reponse": "Oui"},
                {"question": "Contexte fourni", "reponse": "Oui" if analysis_text else "Non"}
            ],
            "domaine": "analyse_culture_securite",
            "secteur_scian": secteur,
            "situation_text": analysis_text,
            "metadata": {
                "interface": "safegraph_streamlit",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Utiliser Agent A1 Enhanced
        agent = AgentA1EnhancedStandalone()
        result = agent.process_with_memory(
            analysis_data,
            user_company or "utilisateur_anonyme", 
            secteur
        )
        
        # Enrichir avec contexte mémoire
        result["memory_context"] = True
        result["source"] = "A1_Enhanced_Mem0"
        
        return result
        
    except Exception as e:
        return {
            "error": f"Erreur analyse mémoire: {e}",
            "fallback": True,
            "standard_mode": True
        }

def render_memory_enhanced_results(result):
    """
    Affiche les résultats enrichis par la mémoire IA
    
    Args:
        result: Résultats de l'analyse avec mémoire
    """
    # Header avec indicateur mémoire
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.subheader("📊 Résultats Analyse IA Enhanced")
    
    with col2:
        if result.get("enhanced_by_memory"):
            st.success("🧠 IA Mémoire")
        else:
            st.info("🆕 Première fois")
    
    # Métriques principales
    if "score_final" in result:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            score = result.get("score_final", 0)
            st.metric("Score Sécurité", f"{score}/100")
        
        with col2:
            niveau = result.get("niveau_securite", "N/A")
            st.metric("Niveau", niveau)
        
        with col3:
            questions = result.get("total_questions", 0)
            st.metric("Points Analysés", questions)
    
    # Recommandations avec style
    if "recommandations" in result:
        st.subheader("🎯 Recommandations")
        
        for rec in result["recommandations"]:
            if "🎉" in rec or "✅" in rec:
                st.success(rec)
            elif "⚠️" in rec or "🚨" in rec:
                st.warning(rec)
            elif "📈" in rec or "🎯" in rec:
                st.info(rec)
            else:
                st.write(f"• {rec}")
    
    # Insights mémoire (si disponibles)
    if "memory_insights" in result:
        render_memory_insights_compact(result["memory_insights"])

def render_memory_insights_compact(insights):
    """Affichage compact des insights mémoire"""
    
    historical_count = insights.get("historical_evaluations", 0)
    
    if historical_count > 0:
        st.markdown("---")
        st.subheader("🧠 Insights Mémoire IA")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Analyses Historiques", historical_count)
            
            # Tendance
            trend_analysis = insights.get("trend_analysis", {})
            trend_message = trend_analysis.get("message", "N/A")
            trend_type = trend_analysis.get("trend", "")
            
            if "improvement" in trend_type:
                st.success(f"📈 {trend_message}")
            elif "decline" in trend_type:
                st.error(f"📉 {trend_message}")
            else:
                st.info(f"📊 {trend_message}")
        
        with col2:
            # Potentiel d'amélioration
            potential = insights.get("improvement_potential", "")
            if potential:
                st.info(f"🎯 {potential}")
            
            # Scores précédents
            prev_scores = insights.get("previous_scores", [])
            if prev_scores:
                st.write("**Scores récents:**")
                for i, score in enumerate(prev_scores[-3:]):
                    st.write(f"#{i+1}: {score}/100")
        
        # Recommandations personnalisées
        personalized_recs = insights.get("personalized_recommendations", [])
        if personalized_recs:
            st.markdown("**🎯 Recommandations Personnalisées:**")
            for rec in personalized_recs[:3]:  # Top 3
                st.write(f"• {rec}")

def add_memory_controls_to_sidebar():
    """Ajoute contrôles mémoire à la sidebar existante"""
    
    if not MEMORY_AVAILABLE:
        return False
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧠 Contrôles Mémoire IA")
    
    # Input entreprise
    user_company = st.sidebar.text_input(
        "🏢 Nom Entreprise",
        placeholder="Ex: Construction ABC",
        help="Pour historique personnalisé"
    )
    
    # Toggle mémoire
    use_memory = st.sidebar.checkbox(
        "✅ Activer Mémoire IA",
        value=True,
        help="Analyse avec apprentissage"
    )
    
    # Bouton historique
    if user_company and st.sidebar.button("📚 Voir Historique"):
        show_user_history_sidebar(user_company)
    
    return {
        "user_company": user_company,
        "use_memory": use_memory,
        "memory_available": True
    }

def show_user_history_sidebar(user_company):
    """Affiche historique dans sidebar"""
    try:
        memories = get_agent_context("A1", user_company, "analyse", limit=5)
        
        if memories:
            st.sidebar.success(f"📚 {len(memories)} analyses trouvées")
            
            for i, memory in enumerate(memories[:3]):
                metadata = memory.get("metadata", {})
                score = metadata.get("score", 0)
                date = metadata.get("timestamp", "")[:10]
                
                st.sidebar.write(f"**#{i+1}** - {date}")
                st.sidebar.write(f"Score: {score}/100")
                st.sidebar.markdown("---")
        else:
            st.sidebar.info("📭 Aucun historique")
            
    except Exception as e:
        st.sidebar.error(f"❌ Erreur: {e}")

# Fonction principale d'intégration
def integrate_memory_into_safegraph():
    """
    Fonction principale pour intégrer la mémoire IA dans SafeGraph
    
    À appeler dans votre app.py :
    
    from safegraph_memory_integration import integrate_memory_into_safegraph
    
    # Dans votre interface principale :
    memory_config = integrate_memory_into_safegraph()
    """
    
    # Ajouter section mémoire à la sidebar
    render_memory_section()
    
    # Ajouter contrôles
    memory_config = add_memory_controls_to_sidebar()
    
    return memory_config

# Export des fonctions principales
__all__ = [
    "integrate_memory_into_safegraph",
    "enhance_analysis_with_memory", 
    "render_memory_enhanced_results",
    "MEMORY_AVAILABLE"
]
