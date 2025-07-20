"""
SafeGraph - Interface Streamlit Complète
Système multi-agent d'analyse de culture sécurité
Version FINALE CORRIGÉE
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import time
import json

# Configuration page
st.set_page_config(
    page_title="SafeGraph - Culture Sécurité",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonctions utilitaires AVANT l'utilisation
@st.cache_data(ttl=300)  # Cache 5 minutes
def run_safegraph_analysis(query: str, sector: str, debug: bool = False):
    """Execute SafeGraph analysis or simulation"""
    
    try:
        # Simulation d'analyse SafeGraph
        if debug:
            st.info("🔄 Exécution du graphe SafeGraph...")
        
        # Simulation d'exécution réaliste
        time.sleep(1)
        
        return {
            'classification': 'At-Risk',
            'score': 7.2,
            'nb_recommendations': 7,
            'confidence': 0.89,
            'sector': sector.split(' - ')[0],
            'recommendations': [
                {
                    'description': 'Formation EPI obligatoire pour tous les employés',
                    'priority': 'High',
                    'effort_days': 3,
                    'source': 'sectorial',
                    'impact': 'Élevé'
                },
                {
                    'description': 'Audit sécurité chantier hebdomadaire',
                    'priority': 'High',
                    'effort_days': 2,
                    'source': 'regulatory',
                    'impact': 'Élevé'
                },
                {
                    'description': 'Briefing sécurité quotidien obligatoire',
                    'priority': 'High',
                    'effort_days': 1,
                    'source': 'best_practice',
                    'impact': 'Élevé'
                },
                {
                    'description': 'Mise à jour des procédures d\'urgence',
                    'priority': 'Medium',
                    'effort_days': 5,
                    'source': 'internal',
                    'impact': 'Moyen'
                },
                {
                    'description': 'Formation premiers secours équipe',
                    'priority': 'Medium',
                    'effort_days': 2,
                    'source': 'regulatory',
                    'impact': 'Moyen'
                },
                {
                    'description': 'Installation signalétique sécurité',
                    'priority': 'Medium',
                    'effort_days': 1,
                    'source': 'sectorial',
                    'impact': 'Moyen'
                },
                {
                    'description': 'Révision annuelle équipements',
                    'priority': 'Low',
                    'effort_days': 3,
                    'source': 'maintenance',
                    'impact': 'Faible'
                }
            ]
        }
    except Exception as e:
        st.error(f"Erreur SafeGraph: {e}")
        return simulate_analysis_result()

def simulate_analysis_result():
    """Simulation des résultats pour le mode démo"""
    return {
        'classification': 'At-Risk',
        'score': 6.8,
        'nb_recommendations': 5,
        'confidence': 0.85,
        'sector': '236',
        'recommendations': [
            {
                'description': 'Formation EPI obligatoire',
                'priority': 'High',
                'effort_days': 3,
                'source': 'sectorial',
                'impact': 'Élevé'
            },
            {
                'description': 'Audit sécurité chantier',
                'priority': 'High',
                'effort_days': 2,
                'source': 'regulatory',
                'impact': 'Élevé'
            },
            {
                'description': 'Briefing sécurité quotidien',
                'priority': 'Medium',
                'effort_days': 1,
                'source': 'best_practice',
                'impact': 'Moyen'
            },
            {
                'description': 'Mise à jour procédures',
                'priority': 'Medium',
                'effort_days': 4,
                'source': 'internal',
                'impact': 'Moyen'
            },
            {
                'description': 'Formation équipe',
                'priority': 'Low',
                'effort_days': 2,
                'source': 'training',
                'impact': 'Faible'
            }
        ]
    }

# Import des modules SafeGraph
try:
    from src.core.state import create_initial_state, IntentType
    from src.core.graph import create_safety_graph
    from src.core.config import config
    SAFEGRAPH_AVAILABLE = True
except ImportError:
    SAFEGRAPH_AVAILABLE = False
    # Configuration simulée
    class MockConfig:
        preferred_llm = "claude"
        scian_sectors = {"236": "Construction", "484": "Transport", "622": "Santé", "811": "Maintenance", "561": "Sécurité"}
        has_claude_api = True
        has_openai_api = False
    config = MockConfig()

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

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Status système
    st.subheader("📊 Status Système")
    if SAFEGRAPH_AVAILABLE:
        st.success("✅ SafeGraph Connecté")
        st.info(f"🤖 LLM: {config.preferred_llm.upper()}")
        st.info(f"🏭 Secteurs: {len(config.scian_sectors)}")
        
        # Détails API
        if config.has_claude_api:
            st.success("🧠 Claude API: Actif")
        if config.has_openai_api:
            st.info("🔄 OpenAI API: Disponible")
    else:
        st.warning("⚠️ Mode Démo")
        st.info(f"🤖 LLM: {config.preferred_llm.upper()}")
        st.info(f"🏭 Secteurs: {len(config.scian_sectors)}")
    
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
        debug_mode = st.checkbox("Mode Debug", value=False)
        max_recommendations = st.slider("Nombre max recommandations", 3, 15, 7)
        confidence_threshold = st.slider("Seuil de confiance", 0.5, 1.0, 0.8)

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
        
        # Boutons d'action
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🚀 Lancer l'Analyse", type="primary", use_container_width=True):
                if user_query:
                    with st.spinner("🔄 Analyse en cours..."):
                        # Barre de progression
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Simulation du workflow
                        steps = [
                            "🔍 Classification intention...",
                            "🏭 Enrichissement contexte SCIAN...",
                            "📋 Collecte données...",
                            "🔍 Analyse écarts...",
                            "💡 Génération recommandations..."
                        ]
                        
                        for i, step in enumerate(steps):
                            status_text.text(step)
                            progress_bar.progress((i + 1) / len(steps))
                            time.sleep(0.5)
                        
                        # Exécution de l'analyse
                        result = run_safegraph_analysis(user_query, secteur, debug_mode)
                        st.session_state['analysis_result'] = result
                        st.session_state['analysis_timestamp'] = datetime.now()
                        
                        progress_bar.progress(1.0)
                        status_text.text("✅ Analyse terminée !")
                        
                        st.success("🎉 Analyse complétée avec succès !")
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
                st.session_state['user_input'] = f"Je souhaite une {ex.lower()} pour mon équipe."
                st.rerun()
        
        # Historique récent
        st.subheader("📚 Historique")
        if 'analysis_timestamp' in st.session_state:
            st.info(f"🕒 Dernière analyse: {st.session_state['analysis_timestamp'].strftime('%H:%M:%S')}")
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
    
    # Graphe de workflow amélioré
    st.subheader("🔄 Workflow SafeGraph")
    
    workflow_data = pd.DataFrame({
        'Agent': ['START', 'Router', 'Context', 'Collecteur', 'Analyste', 'Recommandation', 'END'],
        'Time': [0, 0.2, 0.7, 1.9, 4.0, 5.8, 6.0],
        'Y_Position': [6, 5, 4, 3, 2, 1, 0],
        'Status': ['⚪', '✅', '✅', '✅', '✅', '✅', '⚪']
    })
    
    fig_workflow = px.line(
        workflow_data,
        x='Time',
        y='Y_Position',
        title="Exécution du Workflow Multi-Agent",
        markers=True
    )
    fig_workflow.update_traces(
        line_color='#28a745', 
        line_width=4, 
        marker_size=12
    )
    fig_workflow.update_layout(
        yaxis=dict(
            tickmode='array',
            tickvals=workflow_data['Y_Position'],
            ticktext=workflow_data['Agent']
        ),
        xaxis_title="Temps (secondes)",
        yaxis_title="Agents",
        height=400,
        title_x=0.5
    )
    st.plotly_chart(fig_workflow, use_container_width=True)
    
    # Logs en temps réel
    if debug_mode:
        st.subheader("🔍 Logs Détaillés")
        with st.expander("Voir les logs"):
            st.code("""
[2024-06-30 17:30:12] INFO - Router Agent: Intention détectée EVALUATION (confiance: 95%)
[2024-06-30 17:30:12] INFO - Context Agent: Secteur SCIAN 236 identifié
[2024-06-30 17:30:13] INFO - Collecteur Agent: 15 questions collectées
[2024-06-30 17:30:15] INFO - Analyste Agent: 3 écarts détectés
[2024-06-30 17:30:17] INFO - Recommandation Agent: 7 recommandations générées
""")

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
                    🎯 Impact: Élevé | 
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
                    🎯 Impact: Moyen | 
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
    
    else:
        st.info("🔍 Lancez une analyse dans l'onglet 'Analyse' pour voir les résultats ici.")
        
        # Exemple de résultats
        st.subheader("📊 Exemple de Résultats")
        st.markdown("""
        Après analyse, vous verrez ici :
        - **Classification du risque** (Faible, Modéré, Élevé)
        - **Score global** sur 10
        - **Recommandations priorisées** par criticité
        - **Plan d'action détaillé** avec timeline
        - **Options d'export** (PDF, Excel, Email)
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>🛡️ SafeGraph v1.0</strong> | Développé avec ❤️ par <strong>Preventera</strong></p>
    <p>Powered by <strong>Claude 4 Sonnet</strong> & <strong>LangGraph</strong> | 
    🏭 {sectors} secteurs SCIAN | 🤖 {agents} agents spécialisés</p>
</div>
""".format(
    sectors=len(config.scian_sectors),
    agents="5"
), unsafe_allow_html=True)