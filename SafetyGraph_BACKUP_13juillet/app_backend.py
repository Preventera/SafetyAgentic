"""
SafeGraph - Interface avec Backend Réel Intégré
Système multi-agent d'analyse de culture sécurité
Version Backend Complète
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from typing import Dict, Any, Optional

# Configuration page
st.set_page_config(
    page_title="SafeGraph - Culture Sécurité",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import des modules SafeGraph RÉELS
SAFEGRAPH_AVAILABLE = False
try:
    from src.core.state import create_initial_state, IntentType, SafetyState
    from src.core.graph import create_safety_graph
    from src.core.config import config
    from src.utils.llm_factory import get_preferred_llm
    SAFEGRAPH_AVAILABLE = True
    st.success("🔗 Backend SafeGraph connecté !")
except ImportError as e:
    st.warning(f"⚠️ Backend SafeGraph non disponible: {e}")
    # Configuration simulée pour développement
    class MockConfig:
        preferred_llm = "claude"
        scian_sectors = {
            "236": "Construction", 
            "484": "Transport", 
            "622": "Santé", 
            "811": "Maintenance", 
            "561": "Sécurité"
        }
        has_claude_api = True
        has_openai_api = False
        debug_mode = True
    config = MockConfig()

# Fonctions d'intégration backend RÉELLES
def run_real_safegraph_analysis(query: str, sector: str, debug: bool = False) -> Dict[str, Any]:
    """
    Exécution RÉELLE du système SafeGraph multi-agent
    """
    try:
        if debug:
            st.info("🔄 Initialisation du système SafeGraph...")
        
        # 1. Créer l'état initial SafeGraph
        initial_state = create_initial_state(query)
        
        # 2. Enrichir avec le secteur sélectionné
        sector_code = sector.split(' - ')[0]
        initial_state['context']['selected_sector'] = sector_code
        initial_state['context']['sector_name'] = config.scian_sectors.get(sector_code, "Inconnu")
        
        if debug:
            st.info(f"📊 État initial créé - Secteur: {sector_code}")
        
        # 3. Créer et exécuter le graphe SafeGraph
        safety_graph = create_safety_graph()
        
        if debug:
            st.info("🤖 Exécution du workflow multi-agent...")
        
        # 4. Exécution du workflow complet
        final_state = safety_graph.invoke(initial_state)
        
        if debug:
            st.success("✅ Workflow SafeGraph terminé !")
        
        # 5. Formater les résultats pour l'interface
        return format_safegraph_results(final_state, debug)
        
    except Exception as e:
        st.error(f"❌ Erreur backend SafeGraph: {str(e)}")
        if debug:
            st.exception(e)
        # Fallback vers simulation
        return run_simulation_fallback(query, sector)

def format_safegraph_results(state: SafetyState, debug: bool = False) -> Dict[str, Any]:
    """
    Convertit les résultats SafeGraph en format interface
    """
    try:
        # Extraire les données du state SafeGraph
        intent = state.get('intent', IntentType.UNKNOWN)
        analysis = state.get('analysis', {})
        recommendations = state.get('recommendations', [])
        risk_scores = state.get('risk_scores', {})
        context = state.get('context', {})
        
        # Classification basée sur l'analyse
        classification = determine_risk_classification(analysis, risk_scores)
        
        # Score global basé sur les métriques
        global_score = calculate_global_score(analysis, risk_scores)
        
        # Formater les recommandations
        formatted_recommendations = format_recommendations(recommendations)
        
        if debug:
            st.info(f"📈 Classification: {classification}, Score: {global_score}")
            st.info(f"💡 {len(formatted_recommendations)} recommandations générées")
        
        return {
            'classification': classification,
            'score': global_score,
            'nb_recommendations': len(formatted_recommendations),
            'confidence': analysis.get('confidence', 0.85),
            'sector': context.get('selected_sector', '236'),
            'intent': intent.value if intent else 'unknown',
            'recommendations': formatted_recommendations,
            'analysis_details': analysis,
            'risk_breakdown': risk_scores,
            'agent_trace': state.get('agent_trace', []),
            'timestamp': state.get('timestamp', datetime.now().isoformat())
        }
        
    except Exception as e:
        st.error(f"❌ Erreur formatage résultats: {str(e)}")
        return run_simulation_fallback("", "")

def determine_risk_classification(analysis: Dict, risk_scores: Dict) -> str:
    """
    Détermine la classification de risque basée sur l'analyse SafeGraph
    """
    if not analysis and not risk_scores:
        return "At-Risk"
    
    # Logique de classification basée sur les scores de risque
    avg_risk = sum(risk_scores.values()) / len(risk_scores) if risk_scores else 0.7
    
    if avg_risk >= 0.8:
        return "High-Risk"
    elif avg_risk >= 0.5:
        return "At-Risk"
    elif avg_risk >= 0.3:
        return "Moderate"
    else:
        return "Low-Risk"

def calculate_global_score(analysis: Dict, risk_scores: Dict) -> float:
    """
    Calcule le score global basé sur l'analyse SafeGraph
    """
    if not analysis and not risk_scores:
        return 7.2
    
    # Score basé sur l'inverse du risque moyen
    avg_risk = sum(risk_scores.values()) / len(risk_scores) if risk_scores else 0.3
    score = (1 - avg_risk) * 10
    return round(score, 1)

def format_recommendations(recommendations: list) -> list:
    """
    Formate les recommandations SafeGraph pour l'interface
    """
    if not recommendations:
        # Recommandations par défaut si aucune générée
        return [
            {
                'description': 'Formation sécurité adaptée au secteur',
                'priority': 'High',
                'effort_days': 3,
                'source': 'sectorial',
                'impact': 'Élevé'
            },
            {
                'description': 'Audit sécurité complet',
                'priority': 'High',
                'effort_days': 2,
                'source': 'regulatory',
                'impact': 'Élevé'
            }
        ]
    
    formatted = []
    for rec in recommendations:
        if isinstance(rec, dict):
            formatted.append({
                'description': rec.get('description', rec.get('action', 'Action recommandée')),
                'priority': rec.get('priority', 'Medium'),
                'effort_days': rec.get('effort_days', rec.get('duration', 2)),
                'source': rec.get('source', rec.get('category', 'safegraph')),
                'impact': rec.get('impact', 'Moyen')
            })
        else:
            # Si la recommandation est une string
            formatted.append({
                'description': str(rec),
                'priority': 'Medium',
                'effort_days': 2,
                'source': 'safegraph',
                'impact': 'Moyen'
            })
    
    return formatted

def run_simulation_fallback(query: str, sector: str) -> Dict[str, Any]:
    """
    Fallback vers simulation si le backend échoue
    """
    return {
        'classification': 'At-Risk',
        'score': 6.8,
        'nb_recommendations': 5,
        'confidence': 0.75,
        'sector': sector.split(' - ')[0] if ' - ' in sector else '236',
        'intent': 'evaluation',
        'recommendations': [
            {
                'description': 'Formation EPI obligatoire (Fallback)',
                'priority': 'High',
                'effort_days': 3,
                'source': 'simulation',
                'impact': 'Élevé'
            },
            {
                'description': 'Audit sécurité chantier (Fallback)',
                'priority': 'High',
                'effort_days': 2,
                'source': 'simulation',
                'impact': 'Élevé'
            }
        ],
        'analysis_details': {'fallback': True},
        'risk_breakdown': {'general': 0.6},
        'agent_trace': ['simulation_mode'],
        'timestamp': datetime.now().isoformat()
    }

# Fonction principale d'analyse
@st.cache_data(ttl=300)  # Cache 5 minutes
def run_safegraph_analysis(query: str, sector: str, debug: bool = False):
    """
    Point d'entrée principal pour l'analyse SafeGraph
    """
    if SAFEGRAPH_AVAILABLE:
        return run_real_safegraph_analysis(query, sector, debug)
    else:
        st.warning("🔄 Mode simulation - Backend SafeGraph non disponible")
        return run_simulation_fallback(query, sector)

# Interface utilisateur enrichie avec backend
def display_backend_status():
    """
    Affiche le status détaillé du backend dans la sidebar
    """
    st.subheader("🔗 Backend SafeGraph")
    
    if SAFEGRAPH_AVAILABLE:
        st.success("✅ Système connecté")
        
        # Status des composants
        try:
            # Test de la configuration
            if hasattr(config, 'preferred_llm'):
                st.info(f"🤖 LLM: {config.preferred_llm.upper()}")
            
            # Test des secteurs
            if hasattr(config, 'scian_sectors'):
                st.info(f"🏭 Secteurs: {len(config.scian_sectors)}")
            
            # Test des APIs
            if hasattr(config, 'has_claude_api') and config.has_claude_api:
                st.success("🧠 Claude API: Actif")
            if hasattr(config, 'has_openai_api') and config.has_openai_api:
                st.info("🔄 OpenAI API: Disponible")
                
        except Exception as e:
            st.warning(f"⚠️ Configuration partielle: {e}")
    else:
        st.error("❌ Système déconnecté")
        st.info("🔄 Mode simulation actif")

def display_real_agent_execution(result: Dict[str, Any]):
    """
    Affiche l'exécution réelle des agents SafeGraph
    """
    st.subheader("🤖 Exécution Agents SafeGraph")
    
    # Trace des agents réels
    agent_trace = result.get('agent_trace', [])
    
    if agent_trace:
        st.success(f"✅ {len(agent_trace)} agents exécutés")
        
        # Affichage de la trace
        for i, agent in enumerate(agent_trace, 1):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{i}. {agent}**")
            with col2:
                st.write("✅")
        
        # Détails de l'analyse
        analysis_details = result.get('analysis_details', {})
        if analysis_details and not analysis_details.get('fallback'):
            with st.expander("🔍 Détails de l'Analyse"):
                st.json(analysis_details)
    else:
        st.info("ℹ️ Aucune trace d'agent disponible")

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .agent-status {
        display: flex;
        align-items: center;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 5px;
        background: #f0f2f6;
    }
    .success { 
        background: #d4edda; 
        border-left: 4px solid #28a745; 
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .warning { 
        background: #fff3cd; 
        border-left: 4px solid #ffc107; 
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .danger { 
        background: #f8d7da; 
        border-left: 4px solid #dc3545; 
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .info {
        background: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('<h1 class="main-header">🛡️ SafeGraph</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Système Multi-Agent d\'Analyse de Culture Sécurité</p>', unsafe_allow_html=True)

# Sidebar avec status backend amélioré
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Status système avec backend détaillé
    display_backend_status()
    
    # Sélection mode
    mode = st.selectbox(
        "Mode d'Analyse",
        ["🔍 Évaluation", "📊 Analyse", "💡 Recommandations", "📈 Monitoring"],
        index=0
    )
    
    # Secteur SCIAN
    secteur = st.selectbox(
        "Secteur d'Activité",
        [
            "236 - Construction",
            "484 - Transport",
            "622 - Santé", 
            "811 - Maintenance",
            "561 - Sécurité"
        ]
    )
    
    # Paramètres avancés
    with st.expander("🔧 Paramètres Avancés"):
        debug_mode = st.checkbox("Mode Debug", value=SAFEGRAPH_AVAILABLE)
        max_recommendations = st.slider("Nombre max recommandations", 3, 15, 7)
        confidence_threshold = st.slider("Seuil de confiance", 0.5, 1.0, 0.8)
        
        if SAFEGRAPH_AVAILABLE:
            st.info("🔗 Backend réel connecté")
        else:
            st.warning("🔄 Mode simulation")

# Interface principale avec onglets
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Analyse", "📊 Dashboard", "🤖 Agents", "📈 Résultats"])

with tab1:
    st.header("🔍 Analyse de Culture Sécurité")
    
    # Zone de saisie utilisateur
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_query = st.text_area(
            "Décrivez votre situation sécurité :",
            placeholder="Ex: Je travaille en construction et j'aimerais évaluer ma culture sécurité sur le chantier...",
            height=120,
            key="user_input"
        )
        
        # Boutons d'action avec backend réel
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🚀 Lancer l'Analyse", type="primary", use_container_width=True):
                if user_query:
                    with st.spinner("🔄 Analyse SafeGraph en cours..."):
                        # Barre de progression
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Étapes du workflow SafeGraph
                        if SAFEGRAPH_AVAILABLE:
                            steps = [
                                "🔍 Initialisation SafeGraph...",
                                "🤖 Router Agent - Classification intention...",
                                "🏭 Context Agent - Enrichissement SCIAN...",
                                "📋 Collecteur Agent - Collecte données...",
                                "🔍 Analyste Agent - Analyse écarts...",
                                "💡 Recommandation Agent - Génération actions..."
                            ]
                        else:
                            steps = [
                                "🔄 Mode simulation...",
                                "📊 Génération données test...",
                                "💡 Recommandations simulées..."
                            ]
                        
                        for i, step in enumerate(steps):
                            status_text.text(step)
                            progress_bar.progress((i + 1) / len(steps))
                            time.sleep(0.5 if SAFEGRAPH_AVAILABLE else 0.3)
                        
                        # Exécution de l'analyse RÉELLE
                        result = run_safegraph_analysis(user_query, secteur, debug_mode)
                        st.session_state['analysis_result'] = result
                        st.session_state['analysis_timestamp'] = datetime.now()
                        
                        progress_bar.progress(1.0)
                        status_text.text("✅ Analyse SafeGraph terminée !")
                        
                        if SAFEGRAPH_AVAILABLE:
                            st.success("🎉 Analyse backend SafeGraph complétée !")
                        else:
                            st.info("🔄 Analyse simulation complétée !")
                        
                        st.rerun()
                else:
                    st.warning("⚠️ Veuillez saisir une description de votre situation.")
        
        with col_btn2:
            if st.button("🔄 Réinitialiser", use_container_width=True):
                if 'analysis_result' in st.session_state:
                    del st.session_state['analysis_result']
                if 'analysis_timestamp' in st.session_state:
                    del st.session_state['analysis_timestamp']
                st.rerun()
    
    with col2:
        st.subheader("🎯 Exemples")
        examples = [
            "Évaluation construction",
            "Analyse transport routier", 
            "Recommandations maintenance",
            "Monitoring sécurité"
        ]
        
        for ex in examples:
            if st.button(ex, use_container_width=True, key=f"example_{ex}"):
                st.session_state['user_input'] = f"Je souhaite une {ex.lower()} pour mon équipe dans le secteur {secteur.split(' - ')[1].lower()}."
                st.rerun()
        
        # Historique avec détails backend
        st.subheader("📚 Historique")
        if 'analysis_timestamp' in st.session_state:
            result = st.session_state.get('analysis_result', {})
            backend_type = "🔗 Backend" if SAFEGRAPH_AVAILABLE else "🔄 Simulation"
            st.info(f"🕒 {st.session_state['analysis_timestamp'].strftime('%H:%M:%S')}")
            st.info(f"{backend_type}")
            if 'intent' in result:
                st.info(f"🎯 Intent: {result['intent']}")
        else:
            st.info("Aucune analyse récente")

with tab2:
    st.header("📊 Dashboard Sécurité")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Score Global", "7.2/10", "↗️ +0.5")
    with col2:
        st.metric("Risques Détectés", "3", "↘️ -2")
    with col3:
        st.metric("Actions Complétées", "85%", "↗️ +15%")
    with col4:
        st.metric("Conformité", "92%", "↗️ +3%")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        # Score par domaine - Radar chart
        domains = ['Formation', 'EPI', 'Procédures', 'Communication', 'Leadership']
        scores = [8.2, 6.8, 7.5, 7.1, 8.0]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=scores,
            theta=domains,
            fill='toself',
            name='Score Actuel',
            fillcolor='rgba(31, 119, 180, 0.3)',
            line_color='#1f77b4'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, 10],
                    tickfont=dict(size=10)
                )
            ),
            title="Scores par Domaine Sécurité",
            title_x=0.5,
            height=400
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        # Évolution temporelle - CORRIGÉ
        safety_scores = [6.2, 6.5, 6.8, 7.0, 7.1, 7.2]
        dates = pd.date_range(start='2024-01-01', periods=len(safety_scores), freq='M')
        
        df_evolution = pd.DataFrame({
            'Date': dates,
            'Score': safety_scores
        })
        
        fig_line = px.line(
            df_evolution,
            x='Date', 
            y='Score',
            title="Évolution Score Sécurité",
            markers=True
        )
        fig_line.update_traces(
            line_color='#1f77b4', 
            line_width=3,
            marker_size=8
        )
        fig_line.update_layout(
            height=400,
            title_x=0.5
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Graphiques supplémentaires
    st.subheader("📈 Analyses Détaillées")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des risques par secteur
        sectors = ['Construction', 'Transport', 'Santé', 'Maintenance', 'Sécurité']
        risk_counts = [12, 8, 5, 10, 6]
        
        fig_bar = px.bar(
            x=sectors,
            y=risk_counts,
            title="Risques par Secteur SCIAN",
            color=risk_counts,
            color_continuous_scale='Reds'
        )
        fig_bar.update_layout(height=300, title_x=0.5)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Statut des recommandations
        statuts = ['Complétées', 'En cours', 'Planifiées', 'En retard']
        counts = [25, 15, 8, 3]
        colors = ['#28a745', '#ffc107', '#17a2b8', '#dc3545']
        
        fig_pie = px.pie(
            values=counts,
            names=statuts,
            title="Statut des Recommandations",
            color_discrete_sequence=colors
        )
        fig_pie.update_layout(height=300, title_x=0.5)
        st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    st.header("🤖 Status des Agents")
    
    # Affichage de l'exécution réelle si disponible
    if 'analysis_result' in st.session_state:
        display_real_agent_execution(st.session_state['analysis_result'])
    else:
        # Simulation du workflow d'agents
        agents_status = [
            {"name": "Router Agent", "status": "✅", "time": "0.2s", "result": "Intent: EVALUATION", "confidence": 0.95},
            {"name": "Context Agent", "status": "✅", "time": "0.5s", "result": "Secteur: Construction", "confidence": 0.92},
            {"name": "Collecteur Agent", "status": "✅", "time": "1.2s", "result": "Données: 100%", "confidence": 1.0},
            {"name": "Analyste Agent", "status": "✅", "time": "2.1s", "result": "Risque: Modéré", "confidence": 0.88},
            {"name": "Recommandation Agent", "status": "✅", "time": "1.8s", "result": "7 actions", "confidence": 0.91}
        ]
        
        # Table des agents avec métriques
        st.subheader("📋 Exécution des Agents")
        
        for i, agent in enumerate(agents_status):
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 3, 1])
                with col1:
                    st.write(f"**{agent['name']}**")
                with col2:
                    st.write(agent['status'])
                with col3:
                    st.write(agent['time'])
                with col4:
                    st.write(agent['result'])
                with col5:
                    st.write(f"{agent['confidence']:.0%}")
                
                # Barre de progression pour la confiance
                st.progress(agent['confidence'])
        
        st.info("🔍 Lancez une analyse pour voir l'exécution réelle des agents")

with tab4:
    st.header("📈 Résultats d'Analyse")
    
    # Affichage des résultats si disponibles
    if 'analysis_result' in st.session_state:
        result = st.session_state['analysis_result']
        
        # Résumé exécutif avec alertes
        st.subheader("📋 Résumé Exécutif")
        
        classification = result.get('classification', 'N/A')
        if classification == 'At-Risk':
            st.error("⚠️ **Situation À Risque Détectée** - Actions immédiates requises")
        elif classification == 'Moderate':
            st.warning("⚡ **Risque Modéré** - Surveillance renforcée recommandée")
        else:
            st.success("✅ **Situation Satisfaisante** - Maintenir les bonnes pratiques")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Classification</h3>
                <h2>{result.get('classification', 'N/A')}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Score Global</h3>
                <h2>{result.get('score', 'N/A')}/10</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Recommandations</h3>
                <h2>{result.get('nb_recommendations', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommandations détaillées avec priorisation
        st.subheader("💡 Recommandations Prioritaires")
        
        recommendations = result.get('recommendations', [])
        
        # Grouper par priorité
        high_priority = [r for r in recommendations if r.get('priority') == 'High']
        medium_priority = [r for r in recommendations if r.get('priority') == 'Medium']
        low_priority = [r for r in recommendations if r.get('priority') == 'Low']
        
        # Actions prioritaires
        if high_priority:
            st.markdown("### 🚨 **Actions Prioritaires (Haute)**")
            for i, rec in enumerate(high_priority, 1):
                st.markdown(f"""
                <div class="danger">
                    <strong>{i}. {rec.get('description', 'N/A')}</strong><br>
                    📅 Effort: {rec.get('effort_days', 'N/A')} jours | 
                    🎯 Impact: {rec.get('impact', 'Moyen')} | 
                    📋 Source: {rec.get('source', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
        
        # Actions moyennes
        if medium_priority:
            st.markdown("### ⚡ **Actions Recommandées (Moyenne)**")
            for i, rec in enumerate(medium_priority, 1):
                st.markdown(f"""
                <div class="warning">
                    <strong>{i}. {rec.get('description', 'N/A')}</strong><br>
                    📅 Effort: {rec.get('effort_days', 'N/A')} jours | 
                    🎯 Impact: {rec.get('impact', 'Moyen')} | 
                    📋 Source: {rec.get('source', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
        
        # Actions de maintenance
        if low_priority:
            with st.expander("🔧 Actions de Maintenance (Faible Priorité)"):
                for i, rec in enumerate(low_priority, 1):
                    st.markdown(f"""
                    <div class="info">
                        <strong>{i}. {rec.get('description', 'N/A')}</strong><br>
                        📅 Effort: {rec.get('effort_days', 'N/A')} jours
                    </div>
                    """, unsafe_allow_html=True)
        
        # Plan d'action avec timeline
        st.subheader("📅 Plan d'Action Détaillé")
        
        # Créer une timeline
        all_recs = high_priority + medium_priority + low_priority[:2]  # Top 5
        
        if all_recs:
            timeline_data = []
            current_date = datetime.now()
            
            for i, rec in enumerate(all_recs):
                start_date = current_date + timedelta(days=sum([r.get('effort_days', 2) for r in all_recs[:i]]))
                end_date = start_date + timedelta(days=rec.get('effort_days', 2))
                
                timeline_data.append({
                    'Action': rec.get('description', f'Action {i+1}')[:30] + '...',
                    'Début': start_date.strftime('%Y-%m-%d'),
                    'Fin': end_date.strftime('%Y-%m-%d'),
                    'Durée': rec.get('effort_days', 2),
                    'Priorité': rec.get('priority', 'Medium')
                })
            
            df_timeline = pd.DataFrame(timeline_data)
            st.dataframe(df_timeline, use_container_width=True)
            
            # Graphique Gantt simplifié
            fig_gantt = px.bar(
                df_timeline,
                x='Durée',
                y='Action',
                color='Priorité',
                title="Timeline du Plan d'Action",
                color_discrete_map={
                    'High': '#dc3545',
                    'Medium': '#ffc107',
                    'Low': '#28a745'
                },
                orientation='h'
            )
            fig_gantt.update_layout(height=300, title_x=0.5)
            st.plotly_chart(fig_gantt, use_container_width=True)
        
        # Exports et actions
        st.subheader("📤 Export et Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export PDF", use_container_width=True):
                st.info("🔄 Génération du rapport PDF en cours...")
        
        with col2:
            if st.button("📊 Export Excel", use_container_width=True):
                st.info("🔄 Export Excel en cours...")
        
        with col3:
            if st.button("📧 Envoyer Rapport", use_container_width=True):
                st.info("📧 Envoi du rapport par email...")
        
        # Informations backend si disponible
        if SAFEGRAPH_AVAILABLE and debug_mode:
            st.subheader("🔍 Détails Backend")
            
            with st.expander("Voir les détails techniques"):
                st.json({
                    'backend_type': 'SafeGraph Real',
                    'timestamp': result.get('timestamp'),
                    'confidence': result.get('confidence'),
                    'agent_trace': result.get('agent_trace', []),
                    'analysis_details': result.get('analysis_details', {}),
                    'risk_breakdown': result.get('risk_breakdown', {})
                })
    
    else:
        st.info("🔍 Lancez une analyse dans l'onglet 'Analyse' pour voir les résultats ici.")
        
        # Exemple de résultats
        st.subheader("📊 Exemple de Résultats")
        st.markdown("""
        Après analyse SafeGraph, vous verrez ici :
        - **Classification du risque** basée sur l'analyse réelle
        - **Score global** calculé par les agents SafeGraph
        - **Recommandations authentiques** du système multi-agent
        - **Plan d'action détaillé** avec timeline réaliste
        - **Trace complète** des agents exécutés
        - **Options d'export** (PDF, Excel, Email)
        """)

# Footer avec status backend
st.markdown("---")
backend_status = "Backend Connecté" if SAFEGRAPH_AVAILABLE else "Mode Simulation"
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>🛡️ SafeGraph v1.0</strong> | Développé avec ❤️ par <strong>Preventera</strong></p>
    <p>Powered by <strong>Claude 4 Sonnet</strong> & <strong>LangGraph</strong> | 
    🔗 {backend_status} | 🏭 {len(config.scian_sectors)} secteurs SCIAN | 🤖 5 agents spécialisés</p>
</div>
""", unsafe_allow_html=True)