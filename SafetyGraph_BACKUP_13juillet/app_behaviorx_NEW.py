"""
SafetyGraph BehaviorX + Cartographie Culture SST - Interface Complète
====================================================================
Interface Streamlit unifiée : BehaviorX + Cartographie LangGraph
Safety Agentique - Mario Plourde - 13 juillet 2025
Version 4.0 - Architecture LangGraph Optimisée
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import json
from datetime import datetime, timedelta
import hashlib
import uuid
from typing import Dict, List, Any, Optional, Tuple
import random
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════
# 🔧 CONFIGURATION SAFETYGRAPH
# ═══════════════════════════════════════════════════════════════

# Configuration des modules
try:
    from src.revolution_culture_sst.culture_sst_engine import MoteurCultureSST
    REVOLUTION_CULTURE_SST_AVAILABLE = True
except ImportError:
    REVOLUTION_CULTURE_SST_AVAILABLE = False

try:
    from src.analytics.predictive_models import PredictiveAnalytics
    from src.analytics.pattern_recognition import PatternRecognition  
    from src.analytics.anomaly_detection import AnomalyDetector
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False

try:
    from src.performance.optimizer import PerformanceOptimizer
    OPTIMIZER_AVAILABLE = True
except ImportError:
    OPTIMIZER_AVAILABLE = False

# Configuration générale
st.set_page_config(
    page_title="SafetyGraph BehaviorX",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
    }
    .status-success { color: #28a745; }
    .status-warning { color: #ffc107; }
    .status-error { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# Variables globales
if 'behaviorx_memory' not in st.session_state:
    st.session_state.behaviorx_memory = {}
if 'workflow_results' not in st.session_state:
    st.session_state.workflow_results = {}
if 'analytics_cache' not in st.session_state:
    st.session_state.analytics_cache = {}

# ═══════════════════════════════════════════════════════════════
# 🎨 FONCTIONS D'INTERFACE
# ═══════════════════════════════════════════════════════════════

def display_header():
    """Affichage du header principal"""
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ SafetyGraph BehaviorX</h1>
        <p>Interface Agentique Complète - Culture SST & Analytics Prédictifs</p>
        <p><strong>v4.0</strong> • LangGraph • Mario Plourde • {}</p>
    </div>
    """.format(datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)

def display_sidebar():
    """Configuration de la sidebar"""
    st.sidebar.markdown("### 🛠️ Configuration SafetyGraph")
    
    # Statut des modules
    st.sidebar.markdown("#### 📊 Statut Modules")
    
    modules_status = [
        ("🌪️ Révolution Culture SST", REVOLUTION_CULTURE_SST_AVAILABLE),
        ("📈 Analytics Prédictifs", ANALYTICS_AVAILABLE),
        ("⚡ Performance Optimizer", OPTIMIZER_AVAILABLE)
    ]
    
    for module_name, is_available in modules_status:
        status_class = "status-success" if is_available else "status-error"
        status_text = "✅ Actif" if is_available else "❌ Indisponible"
        st.sidebar.markdown(f'<p class="{status_class}">{module_name}: {status_text}</p>', 
                          unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Informations Enterprise
    st.sidebar.markdown("#### 📋 Informations Enterprise")
    nom_entreprise = st.sidebar.text_input("Nom entreprise", value="Enterprise ABC", key="nom_entreprise")
    
    # Secteur d'activité
    st.sidebar.markdown("#### 🏭 Secteur d'Activité (SCIAN)")
    secteur = st.sidebar.selectbox(
        "Choisir secteur",
        options=[
            "Construction (236)",
            "Fabrication (31-33)", 
            "Transport (48-49)",
            "Services (54)",
            "Autre"
        ],
        key="secteur_activite"
    )
    
    # Mode Workflow
    st.sidebar.markdown("#### 🔄 Mode Workflow")
    mode_workflow = st.sidebar.selectbox(
        "Mode d'analyse", 
        options=[
            "VCS + ABC structuré",
            "SCIAN secteur spécifique",
            "Analytics prédictifs",
            "Cartographie complète"
        ],
        key="mode_workflow"
    )
    
    return nom_entreprise, secteur, mode_workflow

def display_actions_rapides():
    """Interface des actions rapides"""
    st.markdown("### ⚡ Actions Rapides")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Lancer BehaviorX Standard", 
                    help="Lance le workflow BehaviorX standard avec mémoire adaptative",
                    key="btn_behaviorx_standard"):
            secteur = st.session_state.get('secteur_activite', 'Construction (236)')
            mode = st.session_state.get('mode_workflow', 'VCS + ABC structuré')
            lancer_behaviorx_standard(secteur, mode, st.session_state.behaviorx_memory)
    
    with col2:
        if st.button("🗺️ Lancer Cartographie Culture SST",
                    help="Génère une cartographie complète de la culture SST",
                    key="btn_cartographie_culture"):
            if REVOLUTION_CULTURE_SST_AVAILABLE:
                lancer_cartographie_culture_sst()
            else:
                st.error("❌ Module Révolution Culture SST non disponible")
                st.info("📋 Installez le module revolution_culture_sst")

def display_metriques_culture_sst():
    """Affichage des métriques Culture SST en temps réel"""
    if not REVOLUTION_CULTURE_SST_AVAILABLE:
        return
    
    st.markdown("#### 📊 Métriques Culture SST Temps Réel")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Simulation de métriques (remplacez par vraies données)
    metriques = {
        "Niveau Culture": 8.5,
        "Engagement": 92,
        "Conformité": 87,
        "Proactivité": 78
    }
    
    colors = ["#28a745", "#17a2b8", "#ffc107", "#6f42c1"]
    
    for idx, (col, (metric, value)) in enumerate(zip([col1, col2, col3, col4], metriques.items())):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: {colors[idx]}">
                <h4 style="margin: 0; color: {colors[idx]}">{metric}</h4>
                <h2 style="margin: 0; color: #333">{value}{'%' if idx > 0 else '/10'}</h2>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 🧠 FONCTIONS WORKFLOW BEHAVIORX
# ═══════════════════════════════════════════════════════════════

def lancer_behaviorx_standard(secteur: str, mode: str, memoire: Dict):
    """Lance le workflow BehaviorX Standard"""
    
    with st.spinner("🚀 Lancement BehaviorX Standard..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulation workflow multi-agent
        workflow_steps = [
            ("🔄 Initialisation VCS (Validation Context Sharing)", 0.2),
            ("🧠 Agent A1 - Analyse Contextuelle", 0.4),
            ("🎯 Agent A2 - Recommandations Ciblées", 0.6),
            ("🔍 Agent AN1 - Analyse Comportementale", 0.8),
            ("📊 Agent R1 - Rapport Final", 1.0)
        ]
        
        results = {}
        
        for step_name, progress in workflow_steps:
            status_text.text(step_name)
            progress_bar.progress(progress)
            
            # Simulation de traitement
            time.sleep(1)
            
            # Génération de résultats simulés par étape
            if "A1" in step_name:
                results['analyse_contextuelle'] = generer_analyse_contextuelle(secteur)
            elif "A2" in step_name:
                results['recommandations'] = generer_recommandations_ciblees(secteur, mode)
            elif "AN1" in step_name:
                results['analyse_comportementale'] = generer_analyse_comportementale(memoire)
            elif "R1" in step_name:
                results['rapport_final'] = generer_rapport_final(results)
        
        status_text.text("✅ Workflow terminé avec succès!")
        progress_bar.progress(1.0)
        
        # Mise à jour mémoire
        memoire[f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"] = results
        
        # Stockage des résultats pour affichage ultérieur
        st.session_state.workflow_results = results
        
        # Affichage des résultats
        afficher_resultats_behaviorx(results)

def lancer_cartographie_culture_sst():
    """Lance la cartographie Culture SST"""
    
    if not REVOLUTION_CULTURE_SST_AVAILABLE:
        st.error("❌ Module Culture SST non disponible")
        return
    
    with st.spinner("🗺️ Génération cartographie Culture SST..."):
        progress_bar = st.progress(0)
        
        etapes_cartographie = [
            ("📋 Collecte données organisationnelles", 0.25),
            ("🔍 Analyse granulaire par département", 0.5),
            ("🎨 Génération visualisations", 0.75),
            ("📊 Synthèse et recommandations", 1.0)
        ]
        
        for etape, progress in etapes_cartographie:
            st.text(etape)
            progress_bar.progress(progress)
            time.sleep(1.5)
        
        # Génération cartographie
        cartographie_data = generer_cartographie_data()
        afficher_cartographie_culture_sst(cartographie_data)

def generer_analyse_contextuelle(secteur: str) -> Dict:
    """Génère l'analyse contextuelle selon le secteur"""
    
    secteur_clean = secteur.split("(")[0].strip()
    
    analyses_par_secteur = {
        "Construction": {
            "risques_principaux": ["Chutes de hauteur", "Équipements lourds", "Espaces confinés"],
            "comportements_cles": ["Port EPI", "Signalisation", "Communication sécurité"],
            "facteurs_contextuels": ["Météo", "Échéanciers", "Coordination équipes"]
        },
        "Fabrication": {
            "risques_principaux": ["Machines industrielles", "Substances chimiques", "Ergonomie"],
            "comportements_cles": ["Lockout/Tagout", "Inspection équipements", "Procédures sécurité"],
            "facteurs_contextuels": ["Cadence production", "Formation", "Maintenance"]
        },
        "Transport": {
            "risques_principaux": ["Accidents routiers", "Manutention", "Fatigue"],
            "comportements_cles": ["Conduite défensive", "Vérifications véhicules", "Gestion temps"],
            "facteurs_contextuels": ["Conditions routières", "Horaires", "Stress"]
        }
    }
    
    return analyses_par_secteur.get(secteur_clean, analyses_par_secteur["Construction"])

def generer_recommandations_ciblees(secteur: str, mode: str) -> List[Dict]:
    """Génère des recommandations ciblées"""
    
    base_recommendations = [
        {
            "priorite": "Élevée",
            "domaine": "Formation",
            "action": "Renforcer la formation sur les comportements sécuritaires",
            "impact_estime": "85%",
            "delai": "30 jours"
        },
        {
            "priorite": "Moyenne", 
            "domaine": "Communication",
            "action": "Améliorer la communication des near-miss",
            "impact_estime": "70%",
            "delai": "45 jours"
        },
        {
            "priorite": "Élevée",
            "domaine": "Leadership",
            "action": "Former les superviseurs au coaching sécurité",
            "impact_estime": "90%",
            "delai": "60 jours"
        }
    ]
    
    # Personnalisation selon secteur et mode
    if "Construction" in secteur:
        base_recommendations.append({
            "priorite": "Critique",
            "domaine": "EPI",
            "action": "Audit quotidien du port des EPI",
            "impact_estime": "95%",
            "delai": "Immédiat"
        })
    
    return base_recommendations

def generer_analyse_comportementale(memoire: Dict) -> Dict:
    """Génère l'analyse comportementale avec mémoire"""
    
    # Analyse des patterns historiques
    sessions_precedentes = len(memoire)
    
    analyse = {
        "patterns_identifies": [
            "Amélioration continue observée",
            "Engagement équipes en hausse", 
            "Conformité procédures stable"
        ],
        "tendances": {
            "securite": "↗️ Amélioration (+12%)",
            "engagement": "↗️ Croissance (+8%)",
            "conformite": "→ Stable (87%)"
        },
        "sessions_analysees": sessions_precedentes,
        "recommandations_adaptatives": [
            "Maintenir l'effort sur la formation",
            "Intensifier le coaching terrain",
            "Mesurer impact des interventions"
        ]
    }
    
    return analyse

def generer_rapport_final(results: Dict) -> Dict:
    """Génère le rapport final consolidé"""
    
    rapport = {
        "resume_executif": {
            "score_global": random.randint(75, 95),
            "domaines_forts": ["Leadership", "Formation"],
            "axes_amelioration": ["Communication", "Suivi"],
            "priorites_immediates": 3
        },
        "indicateurs_cles": {
            "taux_conformite": f"{random.randint(80, 95)}%",
            "engagement_equipes": f"{random.randint(75, 90)}%", 
            "reduction_incidents": f"{random.randint(15, 35)}%"
        },
        "plan_action": {
            "actions_immediates": 2,
            "actions_court_terme": 4,
            "actions_long_terme": 3
        },
        "timestamp": datetime.now().isoformat()
    }
    
    return rapport

# ═══════════════════════════════════════════════════════════════
# 📊 FONCTIONS ANALYTICS ET AFFICHAGE
# ═══════════════════════════════════════════════════════════════

def afficher_resultats_behaviorx(results: Dict):
    """Affiche les résultats du workflow BehaviorX"""
    
    st.markdown("## 📊 Résultats BehaviorX Standard")
    
    # Onglets pour organiser les résultats
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧠 Analyse Contextuelle", 
        "🎯 Recommandations", 
        "🔍 Analyse Comportementale", 
        "📋 Rapport Final"
    ])
    
    with tab1:
        if 'analyse_contextuelle' in results:
            analyse = results['analyse_contextuelle']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🚨 Risques Principaux")
                for risque in analyse['risques_principaux']:
                    st.markdown(f"• {risque}")
                
                st.markdown("#### 🎯 Comportements Clés")
                for comportement in analyse['comportements_cles']:
                    st.markdown(f"• {comportement}")
            
            with col2:
                st.markdown("#### 🌍 Facteurs Contextuels")
                for facteur in analyse['facteurs_contextuels']:
                    st.markdown(f"• {facteur}")
    
    with tab2:
        if 'recommandations' in results:
            st.markdown("#### 🎯 Plan d'Action Recommandé")
            
            for idx, rec in enumerate(results['recommandations']):
                priority_color = {
                    "Critique": "#dc3545",
                    "Élevée": "#fd7e14", 
                    "Moyenne": "#ffc107",
                    "Faible": "#28a745"
                }.get(rec['priorite'], "#6c757d")
                
                st.markdown(f"""
                <div style="border-left: 4px solid {priority_color}; padding: 1rem; margin: 1rem 0; background: #f8f9fa;">
                    <h5 style="margin: 0; color: {priority_color};">Priorité {rec['priorite']} - {rec['domaine']}</h5>
                    <p style="margin: 0.5rem 0;"><strong>Action:</strong> {rec['action']}</p>
                    <p style="margin: 0;"><strong>Impact estimé:</strong> {rec['impact_estime']} | <strong>Délai:</strong> {rec['delai']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        if 'analyse_comportementale' in results:
            analyse_comp = results['analyse_comportementale']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔍 Patterns Identifiés")
                for pattern in analyse_comp['patterns_identifies']:
                    st.markdown(f"✅ {pattern}")
                
                st.markdown("#### 📈 Tendances")
                for domaine, tendance in analyse_comp['tendances'].items():
                    st.markdown(f"**{domaine.capitalize()}:** {tendance}")
            
            with col2:
                st.markdown("#### 🧠 Recommandations Adaptatives")
                for rec in analyse_comp['recommandations_adaptatives']:
                    st.markdown(f"• {rec}")
                
                st.info(f"📊 Basé sur {analyse_comp['sessions_analysees']} sessions précédentes")
    
    with tab4:
        if 'rapport_final' in results:
            rapport = results['rapport_final']
            
            # Score global avec gauge
            score = rapport['resume_executif']['score_global']
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Score Global de Sécurité"},
                delta = {'reference': 80},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Indicateurs clés
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Taux de Conformité", 
                    rapport['indicateurs_cles']['taux_conformite'],
                    delta="5%"
                )
            
            with col2:
                st.metric(
                    "Engagement Équipes",
                    rapport['indicateurs_cles']['engagement_equipes'], 
                    delta="8%"
                )
            
            with col3:
                st.metric(
                    "Réduction Incidents",
                    rapport['indicateurs_cles']['reduction_incidents'],
                    delta="12%"
                )

def generer_cartographie_data():
    """Génère les données pour la cartographie Culture SST"""
    
    departements = [
        "Production", "Maintenance", "Logistique", "Qualité", 
        "Administration", "RH", "IT", "Sécurité"
    ]
    
    data = []
    for dept in departements:
        data.append({
            'departement': dept,
            'score_culture': random.randint(65, 95),
            'engagement': random.randint(70, 90),
            'conformite': random.randint(75, 95),
            'formation': random.randint(60, 90),
            'communication': random.randint(65, 85),
            'leadership': random.randint(70, 95)
        })
    
    return pd.DataFrame(data)

def afficher_cartographie_culture_sst(data: pd.DataFrame):
    """Affiche la cartographie Culture SST"""
    
    st.markdown("## 🗺️ Cartographie Culture SST")
    
    # Heatmap des scores par département
    fig_heatmap = px.imshow(
        data.set_index('departement')[['score_culture', 'engagement', 'conformite', 'formation', 'communication', 'leadership']].T,
        title="Matrice Culture SST par Département",
        color_continuous_scale="RdYlGn",
        aspect="auto"
    )
    
    fig_heatmap.update_layout(height=400)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Radar chart pour comparaison
    categories = ['Score Culture', 'Engagement', 'Conformité', 'Formation', 'Communication', 'Leadership']
    
    fig_radar = go.Figure()
    
    for idx, row in data.iterrows():
        if idx < 4:  # Limiter à 4 départements pour lisibilité
            values = [row['score_culture'], row['engagement'], row['conformite'], 
                     row['formation'], row['communication'], row['leadership']]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=row['departement']
            ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Profil Culture SST - Top 4 Départements",
        height=500
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Tableau détaillé
    st.markdown("#### 📊 Données Détaillées")
    st.dataframe(data.style.background_gradient(subset=['score_culture', 'engagement', 'conformite'], cmap='RdYlGn'))

def display_predictive_analytics_interface():
    """Interface Analytics Prédictifs"""
    
    st.markdown("## 🔮 Analytics Prédictifs SafetyGraph")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Métriques principales
    with col1:
        st.metric("🎯 Précision Modèle", "89.4%", delta="2.1%")
    
    with col2:
        st.metric("📊 Prédictions Actives", "1,247", delta="89")
    
    with col3:
        st.metric("⚠️ Alertes Risque", "23", delta="-5")
    
    with col4:
        st.metric("🕒 Dernière MAJ", "2min", delta=None)
    
    # Configuration prédictions
    st.markdown("### ⚙️ Configuration Prédictions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        horizon = st.selectbox(
            "🕐 Horizon Prédiction",
            ["12 mois", "6 mois", "3 mois", "1 mois"],
            index=0
        )
    
    with col2:
        secteur = st.selectbox(
            "🏭 Secteur SCIAN",
            ["Construction (236)", "Fabrication (31-33)", "Transport (48-49)"],
            index=0
        )
    
    # Graphiques prédictifs
    display_prediction_charts()

def display_prediction_charts():
    """Affiche les graphiques prédictifs"""
    
    # Données simulées pour prédictions
    dates = pd.date_range(start='2025-01-01', end='2025-12-31', freq='M')
    
    # Prédiction incidents
    incidents_pred = np.random.poisson(3, len(dates))
    incidents_conf_low = incidents_pred - np.random.poisson(1, len(dates))
    incidents_conf_high = incidents_pred + np.random.poisson(1, len(dates))
    
    fig_pred = go.Figure()
    
    # Ligne principale
    fig_pred.add_trace(go.Scatter(
        x=dates,
        y=incidents_pred,
        mode='lines+markers',
        name='Prédiction Incidents',
        line=dict(color='blue', width=3)
    ))
    
    # Intervalle de confiance
    fig_pred.add_trace(go.Scatter(
        x=dates.tolist() + dates.tolist()[::-1],
        y=incidents_conf_high.tolist() + incidents_conf_low.tolist()[::-1],
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Intervalle de confiance'
    ))
    
    fig_pred.update_layout(
        title="🔮 Prédiction Incidents - 12 mois",
        xaxis_title="Période",
        yaxis_title="Nombre d'incidents prédits",
        height=400
    )
    
    st.plotly_chart(fig_pred, use_container_width=True)
    
    # Heatmap risques par zone
    zones = ['Zone A', 'Zone B', 'Zone C', 'Zone D', 'Zone E']
    mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun']
    
    risques_matrix = np.random.rand(len(zones), len(mois)) * 100
    
    fig_heatmap = px.imshow(
        risques_matrix,
        x=mois,
        y=zones,
        title="🗺️ Cartographie Risques Prédictifs",
        color_continuous_scale="Reds",
        aspect="auto"
    )
    
    fig_heatmap.update_layout(height=300)
    st.plotly_chart(fig_heatmap, use_container_width=True)

def display_pattern_recognition_interface():
    """Interface Pattern Recognition"""
    
    st.markdown("## 🧩 Pattern Recognition SafetyGraph")
    
    # Métriques pattern
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔍 Patterns Détectés", "156", delta="12")
    
    with col2:
        st.metric("⚡ Patterns Critiques", "8", delta="-2")
    
    with col3:
        st.metric("📈 Tendances Identifiées", "23", delta="5")
    
    with col4:
        st.metric("🎯 Précision", "94.2%", delta="1.8%")
    
    # Visualisation patterns
    patterns_data = {
        'Pattern': ['Fatigue End-of-Shift', 'Equipment Bypass', 'Communication Gap', 'Training Deficiency'],
        'Fréquence': [45, 32, 28, 19],
        'Criticité': [8.5, 9.2, 6.8, 7.1],
        'Tendance': ['↗️', '↘️', '→', '↗️']
    }
    
    df_patterns = pd.DataFrame(patterns_data)
    
    # Graphique en barres
    fig_patterns = px.bar(
        df_patterns,
        x='Pattern',
        y='Fréquence',
        color='Criticité',
        title="🧩 Patterns Comportementaux Détectés",
        color_continuous_scale="Reds"
    )
    
    st.plotly_chart(fig_patterns, use_container_width=True)
    
    # Tableau détaillé
    st.markdown("#### 📊 Analyse Détaillée des Patterns")
    st.dataframe(df_patterns)

def display_anomaly_detection_interface():
    """Interface Anomaly Detection"""
    
    st.markdown("## 🚨 Anomaly Detection SafetyGraph")
    
    # Métriques anomalies
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🚨 Anomalies Détectées", "12", delta="3")
    
    with col2:
        st.metric("⚠️ Seuil Critique", "5", delta="0")
    
    with col3:
        st.metric("🔍 Taux Détection", "97.8%", delta="0.5%")
    
    with col4:
        st.metric("⚡ Temps Réponse", "1.2s", delta="-0.3s")
    
    # Timeline des anomalies
    dates_anomalies = pd.date_range(start='2025-07-01', end='2025-07-13', freq='D')
    scores_anomalies = np.random.exponential(2, len(dates_anomalies))
    
    fig_anomalies = go.Figure()
    
    fig_anomalies.add_trace(go.Scatter(
        x=dates_anomalies,
        y=scores_anomalies,
        mode='lines+markers',
        name='Score Anomalie',
        line=dict(color='red', width=2),
        marker=dict(size=8)
    ))
    
    # Seuil critique
    fig_anomalies.add_hline(
        y=5.0,
        line_dash="dash",
        line_color="orange",
        annotation_text="Seuil Critique"
    )
    
    fig_anomalies.update_layout(
        title="🚨 Timeline des Anomalies Détectées",
        xaxis_title="Date",
        yaxis_title="Score d'Anomalie",
        height=400
    )
    
    st.plotly_chart(fig_anomalies, use_container_width=True)

def performance_optimizer_interface():
    """Interface Performance Optimizer"""
    
    st.markdown("## ⚡ Analytics Optimisés SafetyGraph")
    
    # Métriques performance
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💾 Cache Hit Rate", "0.0%", delta="↗ Cible: 80%+", delta_color="inverse")
    
    with col2:
        st.metric("⚡ Temps Moyen", "0.00s", delta="↗ Cible: <1.5s", delta_color="normal")
    
    with col3:
        st.metric("💚 Temps Économisé", "0.0s", delta="+0 hits", delta_color="normal")
    
    with col4:
        st.metric("🕐 Uptime Session", "0.0min", delta="✅ Stable", delta_color="normal")
    
    # Analytics Cache
    st.markdown("### 🧠 Analytics Cache")
    
    with st.expander("📊 Statistiques Cache", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**• Hits:** 0")
            st.markdown("**• Misses:** 0")
        
        with col2:
            st.markdown("**• Éléments en cache:** 0")
            st.markdown("**• Temps total économisé:** 0.0s")
    
    # Recommandations Performance
    st.markdown("### 🚀 Recommandations Performance")
    
    recommendations = [
        "🔄 Optimiser les requêtes fréquentes",
        "💾 Implémenter mise en cache intelligente",
        "⚡ Réduire la latence des calculs",
        "📊 Paralléliser les analytics lourds"
    ]
    
    for rec in recommendations:
        st.markdown(f"• {rec}")

# ═══════════════════════════════════════════════════════════════
# 📋 INTERFACE NORMES & CONFORMITÉ
# ═══════════════════════════════════════════════════════════════

def display_normes_conformite_interface():
    """Interface Normes & Conformité"""
    
    st.markdown("## 📋 Normes & Conformité SafetyGraph")
    
    # Statut conformité
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Conformité Globale", "87%", delta="3%")
    
    with col2:
        st.metric("📝 Normes Couvertes", "55/78", delta="5")
    
    with col3:
        st.metric("🔍 Audits Réalisés", "12", delta="2")
    
    with col4:
        st.metric("⚠️ Non-Conformités", "8", delta="-3")
    
    # Répartition par famille de normes
    normes_data = {
        'Famille': ['ISO 45001', 'OHSAS 18001', 'CSA Z1000', 'SCIAN Spécifiques', 'Autres'],
        'Conformité': [92, 85, 78, 83, 90],
        'Critiques': [2, 4, 6, 3, 1]
    }
    
    df_normes = pd.DataFrame(normes_data)
    
    fig_conformite = px.bar(
        df_normes,
        x='Famille',
        y='Conformité',
        title="📊 Taux de Conformité par Famille de Normes",
        color='Conformité',
        color_continuous_scale="RdYlGn"
    )
    
    st.plotly_chart(fig_conformite, use_container_width=True)
    
    # Plan d'action conformité
    st.markdown("### 📋 Plan d'Action Conformité")
    
    actions_conformite = [
        {"Action": "Mise à jour procédures ISO 45001", "Priorité": "Élevée", "Échéance": "15/08/2025"},
        {"Action": "Formation équipe CSA Z1000", "Priorité": "Moyenne", "Échéance": "30/08/2025"},
        {"Action": "Audit interne OHSAS", "Priorité": "Élevée", "Échéance": "10/08/2025"}
    ]
    
    df_actions = pd.DataFrame(actions_conformite)
    st.dataframe(df_actions)

# ═══════════════════════════════════════════════════════════════
# 🎛️ INTERFACE PRINCIPALE
# ═══════════════════════════════════════════════════════════════

def main_interface():
    """Interface principale SafetyGraph"""
    
    # Header
    display_header()
    
    # Sidebar
    nom_entreprise, secteur, mode_workflow = display_sidebar()
    
    # Actions rapides et métriques
    display_actions_rapides()
    
    # Métriques Culture SST en temps réel
    display_metriques_culture_sst()
    
    st.markdown("---")
    
    # Onglets principaux
    main_tabs = st.tabs([
        "🌀 BehaviorX Standard",
        "🗺️ Cartographie Culture", 
        "🔮 Analytics Prédictifs",
        "🧩 Pattern Recognition",
        "🚨 Anomaly Detection",
        "⚡ Analytics Optimisés",
        "📋 Normes & Conformité"
    ])
    
    # ═══════════════════════════════════════════════════════════════
    # ONGLET 1: BEHAVIORX STANDARD
    # ═══════════════════════════════════════════════════════════════
    with main_tabs[0]:
        st.markdown("### 🌀 BehaviorX Standard - Workflow Multi-Agent")
        
        if st.session_state.get('workflow_results'):
            st.success("✅ Dernière analyse terminée avec succès")
            
            if st.button("📊 Voir les résultats", key="voir_resultats_behaviorx"):
                afficher_resultats_behaviorx(st.session_state.workflow_results)
            
            if st.button("🔄 Nouvelle analyse", key="nouvelle_analyse_behaviorx"):
                st.session_state.workflow_results = {}
                st.rerun()
        else:
            st.info("👆 Cliquez sur 'Lancer BehaviorX Standard' pour commencer l'analyse")
            
            # Aperçu des capacités
            st.markdown("#### 🎯 Capacités BehaviorX Standard")
            
            capacites = [
                "🧠 **Agent A1** - Analyse contextuelle SCIAN",
                "🎯 **Agent A2** - Recommandations ciblées par secteur", 
                "🔍 **Agent AN1** - Analyse comportementale ABC",
                "📊 **Agent R1** - Rapport consolidé avec métriques",
                "🧠 **Mémoire Adaptative** - Apprentissage continu"
            ]
            
            for capacite in capacites:
                st.markdown(capacite)
    
    # ═══════════════════════════════════════════════════════════════
    # ONGLET 2: CARTOGRAPHIE CULTURE
    # ═══════════════════════════════════════════════════════════════
    with main_tabs[1]:
        if REVOLUTION_CULTURE_SST_AVAILABLE:
            st.markdown("### 🗺️ Cartographie Culture SST")
            
            if st.button("🚀 Générer Cartographie Complète", key="generer_cartographie"):
                lancer_cartographie_culture_sst()
            
            # Paramètres de cartographie
            with st.expander("⚙️ Paramètres Cartographie", expanded=False):
                granularite = st.selectbox(
                    "Niveau de granularité",
                    ["Département", "Équipe", "Individuel"],
                    key="granularite_carto"
                )
                
                dimensions = st.multiselect(
                    "Dimensions à analyser",
                    ["Culture Sécurité", "Engagement", "Conformité", "Formation", "Communication", "Leadership"],
                    default=["Culture Sécurité", "Engagement", "Conformité"],
                    key="dimensions_carto"
                )
        else:
            st.warning("⚠️ Module Révolution Culture SST non disponible")
            st.info("📋 Créez le fichier src/revolution_culture_sst/culture_sst_engine.py")
    
    # ═══════════════════════════════════════════════════════════════
    # ONGLET 3: ANALYTICS PRÉDICTIFS
    # ═══════════════════════════════════════════════════════════════
    with main_tabs[2]:
        if ANALYTICS_AVAILABLE:
            display_predictive_analytics_interface()
        else:
            st.warning("⚠️ Module Analytics Prédictifs non disponible")
            st.info("📋 Créez le fichier src/analytics/predictive_models.py")
    
    # ═══════════════════════════════════════════════════════════════
    # ONGLET 4: PATTERN RECOGNITION
    # ═══════════════════════════════════════════════════════════════
    with main_tabs[3]:
        if ANALYTICS_AVAILABLE:
            display_pattern_recognition_interface()
        else:
            st.warning("⚠️ Module Pattern Recognition non disponible")
            st.info("📋 Créez le fichier src/analytics/pattern_recognition.py")
    
    # ═══════════════════════════════════════════════════════════════
    # ONGLET 5: ANOMALY DETECTION
    # ═══════════════════════════════════════════════════════════════
    with main_tabs[4]:
        if ANALYTICS_AVAILABLE:
            display_anomaly_detection_interface()
        else:
            st.warning("⚠️ Module Anomaly Detection non disponible")
            st.info("📋 Créez le fichier src/analytics/anomaly_detection.py")
    
    # ═══════════════════════════════════════════════════════════════
    # ONGLET 6: ANALYTICS OPTIMISÉS
    # ═══════════════════════════════════════════════════════════════
    with main_tabs[5]:
        if OPTIMIZER_AVAILABLE:
            performance_optimizer_interface()
        else:
            st.warning("⚠️ Module Performance Optimizer non disponible")
            st.info("📋 Créez le fichier src/performance/optimizer.py")
    
    # ═══════════════════════════════════════════════════════════════
    # ONGLET 7: NORMES & CONFORMITÉ
    # ═══════════════════════════════════════════════════════════════
    with main_tabs[6]:
        display_normes_conformite_interface()

# ═══════════════════════════════════════════════════════════════
# 🚀 POINT D'ENTRÉE PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def main():
    """Point d'entrée principal de l'application SafetyGraph"""
    
    try:
        # Initialisation de l'interface
        main_interface()
        
    except Exception as e:
        st.error(f"❌ Erreur dans l'application SafetyGraph: {str(e)}")
        st.exception(e)
        
        # Informations de debug
        with st.expander("🔍 Informations de Debug", expanded=False):
            st.write("**Type d'erreur:**", type(e).__name__)
            st.write("**Message:**", str(e))
            st.write("**Session State Keys:**", list(st.session_state.keys()))

# ═══════════════════════════════════════════════════════════════
# 🎯 EXÉCUTION CONDITIONNELLE
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()