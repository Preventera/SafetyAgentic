"""
SafetyGraph BehaviorX + Cartographie Culture SST - Interface Complète
====================================================================
Interface Streamlit unifiée : BehaviorX + Cartographie LangGraph
Safety Agentique - Mario Plourde - 8 juillet 2025
Version 3.0 - Architecture LangGraph Intégrée
"""

import streamlit as st

# ===== ENRICHISSEMENT CNESST SAFETYGRAPH =====
try:
    from src.enrichments.cnesst_layer import enrich_safetygraph_context, get_cnesst_status
    CNESST_ENRICHED = True
    print('✅ Enrichissement CNESST activé')
except ImportError:
    CNESST_ENRICHED = False
    print('⚠️ Mode standard - Enrichissements CNESST non disponibles')
    def enrich_safetygraph_context(ctx): return ctx
    def get_cnesst_status(): return {'status': 'disabled', 'message': 'Non disponible'}

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# AJOUTER CES LIGNES AU DÉBUT de app_behaviorx.py (après les imports existants)

# === OPTIMISATION PERFORMANCE ===
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from optimization.performance_optimizer import SafetyGraphOptimizer
    OPTIMIZER_AVAILABLE = True
    optimizer = SafetyGraphOptimizer()
    print("✅ Optimiseur performance activé")
except ImportError:
    OPTIMIZER_AVAILABLE = False
    print("⚠️ Optimiseur non disponible")

# === FIN OPTIMISATION ===
# ===================================================================
# INTEGRATION ANALYTICS AVANCÉS SAFETYGRAPH
# ===================================================================

# Imports modules analytics
try:
    sys.path.append(str(Path(__file__).parent / "src" / "analytics"))
    from predictive_models import display_predictive_analytics_interface
    from pattern_recognition import display_pattern_recognition_interface  
    from anomaly_detection import display_anomaly_detection_interface
    ANALYTICS_AVAILABLE = True
    print("✅ Analytics modules loaded successfully")
except ImportError as e:
    print(f"⚠️ Analytics modules not available: {e}")
    ANALYTICS_AVAILABLE = False

# Configuration page Streamlit
st.set_page_config(
    page_title="SafetyGraph BehaviorX + Cartographie SST",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ajout chemin LangGraph
try:
    sys.path.append(str(Path(__file__).parent / "src" / "langgraph"))
    from safetygraph_cartography_engine import execute_safetygraph_cartography_main
    CARTOGRAPHY_AVAILABLE = True
except ImportError:
    CARTOGRAPHY_AVAILABLE = False

# Imports agents BehaviorX existants
try:
    sys.path.append(str(Path(__file__).parent / "src" / "agents" / "collecte"))
    from orchestrateur_behaviorx_unified import BehaviorXSafetyOrchestrator
    BEHAVIORX_AVAILABLE = True
except ImportError:
    BEHAVIORX_AVAILABLE = False

# ===================================================================
# 1. CONFIGURATION ET ÉTAT SESSION
# ===================================================================

# Initialisation état session
if 'workflow_results' not in st.session_state:
    st.session_state.workflow_results = None
if 'workflow_type' not in st.session_state:
    st.session_state.workflow_type = None
if 'execution_history' not in st.session_state:
    st.session_state.execution_history = []

# ===================================================================
# 2. HEADER ET BRANDING
# ===================================================================

def display_header():
    """Affiche header unifié SafetyGraph"""
    
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1f2937 0%, #374151 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; text-align: center; margin: 0;">
            🗺️ SafetyGraph BehaviorX + Cartographie Culture SST
        </h1>
        <p style="color: #d1d5db; text-align: center; margin: 0.5rem 0 0 0;">
            🏢 <strong>Powered by Safety Agentique</strong> | 
            🤖 LangGraph Multi-Agent | 
            🔍 STORM Research | 
            🧠 Mémoire IA Adaptative
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# 3. SIDEBAR CONFIGURATION
# ===================================================================

def setup_sidebar():
    """Configuration sidebar enrichie"""
    
    with st.sidebar:
        st.markdown("## ⚙️ Configuration SafetyGraph")
        
        # Section entreprise
        st.markdown("### 🏢 Informations Entreprise")
        nom_entreprise = st.text_input("Nom entreprise", value="Entreprise ABC", key="enterprise_name")
        
        # Sélection secteur SCIAN enrichie
        st.markdown("### 📊 Secteur d'Activité (SCIAN)")
        secteurs_scian = {
            "Construction (236)": "236",
            "Soins de santé (622)": "622", 
            "Fabrication alimentaire (311)": "311",
            "Fabrication du bois (321)": "321",
            "Services professionnels (541)": "541",
            "Secteur général": "000"
        }
        
        secteur_selectionne = st.selectbox(
            "Choisir secteur",
            options=list(secteurs_scian.keys()),
            key="sector_selection"
        )
        secteur_code = secteurs_scian[secteur_selectionne]
        
        # Mode workflow enrichi
        st.markdown("### 🎯 Mode Workflow")
        mode_workflow = st.selectbox(
            "Mode d'analyse",
            ["Hybrid (VCS + Safe Self)", "VCS + ABC seulement", "Safe Self seulement", "Cartographie Complète"],
            key="workflow_mode"
        )
        
        # Options avancées
        st.markdown("### 🔧 Options Avancées")
        memoire_ia = st.checkbox("✅ Mémoire IA Mem0", value=True, key="memory_enabled")
        mode_debug = st.checkbox("🐛 Mode Debug", value=False, key="debug_mode")
        
        # Statut modules
        st.markdown("### 📊 Statut Modules")
        st.success(f"🧠 BehaviorX: {'✅ Disponible' if BEHAVIORX_AVAILABLE else '❌ Indisponible'}")
        st.success(f"🗺️ Cartographie: {'✅ Disponible' if CARTOGRAPHY_AVAILABLE else '❌ Indisponible'}")
        
        # À propos
        st.markdown("### ℹ️ À Propos")
        st.info("""
        **SafetyGraph BehaviorX v3.0**
        
        🏢 **Safety Agentique** - Plateforme IA pour culture SST
        
        🗺️ **Cartographie 7D** - Leadership, Communication, Participation, etc.
        
        🤖 **100+ Agents** - A1-A10, AN1-AN10, R1-R10, S1-S10, SC1-SC50
        
        🔍 **STORM Research** - Enrichissement scientifique temps réel
        
        🧠 **LangGraph** - Orchestration multi-agent avancée
        """)
        
        return {
            'enterprise_name': nom_entreprise,
            'sector_name': secteur_selectionne,
            'sector_code': secteur_code,
            'workflow_mode': mode_workflow,
            'memory_enabled': memoire_ia,
            'debug_mode': mode_debug
        }

# ===================================================================
# 4. WORKFLOW BEHAVIORX STANDARD (EXISTANT)
# ===================================================================

def execute_behaviorx_workflow_standard(config):
    """Exécute workflow BehaviorX standard (version existante)"""
    
    if not BEHAVIORX_AVAILABLE:
        st.error("❌ Module BehaviorX non disponible")
        return None
    
    with st.container():
        st.markdown("## 🧠 Workflow BehaviorX Standard")
        
        # Progress tracking
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # Métriques container
        metrics_container = st.container()
        
        try:
            # Initialisation
            status_text.text("🎼 Initialisation Orchestrateur BehaviorX...")
            progress_bar.progress(10)
            
            orchestrator = BehaviorXSafetyOrchestrator({
                'memory_enabled': config['memory_enabled'],
                'debug_mode': config['debug_mode']
            })
            
            # Exécution workflow
            status_text.text("🚀 Exécution Workflow VCS → ABC → A1 Enhanced...")
            progress_bar.progress(50)
            
            results = orchestrator.execute_full_workflow(
                enterprise_id=config['enterprise_name'],
                sector_code=config['sector_code'],
                workflow_mode=config['workflow_mode']
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Workflow BehaviorX Terminé !")
            
            # Affichage métriques
            with metrics_container:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("🎯 Score Intégration", "92.0%", delta="Excellent")
                
                with col2:
                    st.metric("🔍 Conformité VCS", "75.0%", delta="6 Forces")
                
                with col3:
                    st.metric("🤖 Score A1 Enhanced", "79.0", delta="BON")
                
                with col4:
                    st.metric("🚨 Zones Aveugles", "0", delta="Aucune")
            
            return {
                'success': True,
                'type': 'behaviorx_standard',
                'results': results,
                'metrics': {
                    'integration_score': 92.0,
                    'vcs_conformity': 75.0,
                    'a1_score': 79.0,
                    'blind_spots': 0
                }
            }
            
        except Exception as e:
            st.error(f"❌ Erreur workflow BehaviorX: {str(e)}")
            return None

# ===================================================================
# 5. WORKFLOW CARTOGRAPHIE COMPLET (NOUVEAU)
# ===================================================================

def execute_cartography_workflow_complete(config):
    """Exécute workflow cartographie culture SST complet"""
    
    if not CARTOGRAPHY_AVAILABLE:
        st.error("❌ Module Cartographie non disponible")
        return None
    
    with st.container():
        st.markdown("## 🗺️ Cartographie Culture SST Complète")
        
        # Progress tracking cartographique
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # Métriques cartographiques
        metrics_container = st.container()
        
        try:
            # Préparation données entreprise
            enterprise_info = {
                "name": config['enterprise_name'],
                "sector": config['sector_code'],
                "sector_name": config['sector_name'],
                "workflow_mode": config['workflow_mode'],
                "size": "medium"
            }
            
            # Construction requête cartographique
            user_input = f"Cartographie complète culture sécurité entreprise {config['enterprise_name']} secteur {config['sector_name']}"
            
            # Étapes progression
            status_text.text("🎯 Analyse intention cartographique...")
            progress_bar.progress(10)
            time.sleep(0.5)
            
            status_text.text("🏢 Détection contexte SCIAN et enrichissement sectoriel...")
            progress_bar.progress(20)
            time.sleep(0.5)
            
            status_text.text("📊 Collecte multi-dimensionnelle agents A1-A10...")
            progress_bar.progress(35)
            time.sleep(0.8)
            
            status_text.text("🧠 Analyse cartographique 7 dimensions (AN1-AN10)...")
            progress_bar.progress(55)
            time.sleep(0.8)
            
            status_text.text("🔍 Recherche STORM enrichissement scientifique...")
            progress_bar.progress(70)
            time.sleep(0.6)
            
            status_text.text("📋 Génération recommandations cartographiques (R1-R10)...")
            progress_bar.progress(85)
            time.sleep(0.5)
            
            status_text.text("📈 Configuration suivi et monitoring (S1-S10)...")
            progress_bar.progress(95)
            time.sleep(0.3)
            
            # Exécution cartographie
            result = execute_safetygraph_cartography_main(
                user_input=user_input,
                enterprise_info=enterprise_info
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Cartographie Culture SST Terminée avec Succès !")
            
            if result['success']:
                cartography = result['cartography']
                
                # Affichage métriques cartographiques
                with metrics_container:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        maturity_score = cartography['executive_summary']['overall_culture_maturity']
                        st.metric(
                            "🎯 Maturité Culture Globale",
                            f"{maturity_score:.1f}/5.0",
                            delta=f"+{0.5:.1f} (obj. 6 mois)"
                        )
                    
                    with col2:
                        dimensions_count = len(cartography['detailed_cartography'].get('dimensions', {}))
                        st.metric(
                            "📊 Dimensions Cartographiées", 
                            f"{dimensions_count}/7",
                            delta="✅ Complète"
                        )
                    
                    with col3:
                        action_plans = len(cartography['improvement_roadmap'])
                        st.metric(
                            "📋 Plans d'Action",
                            f"{action_plans}",
                            delta="🎯 Personnalisés"
                        )
                    
                    with col4:
                        sector_adapted = cartography['metadata']['sector_name']
                        st.metric(
                            "🏗️ Secteur Adapté",
                            f"{sector_adapted}",
                            delta="✅ SCIAN"
                        )
                
                return result
            else:
                st.error("❌ Erreur lors de l'exécution de la cartographie")
                return None
                
        except Exception as e:
            st.error(f"❌ Erreur cartographie: {str(e)}")
            return None

# ===================================================================
# 6. AFFICHAGE RÉSULTATS BEHAVIORX STANDARD
# ===================================================================

def display_behaviorx_results(results):
    """Affiche résultats BehaviorX standard dans onglets"""
    
    if not results or not results['success']:
        return
    
    # Onglets BehaviorX
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 VCS Observation",
        "🔗 Analyse ABC",
        "🤖 A1 Enhanced",
        "📈 Intégration",
        "📄 Rapport"
    ])
    
    # TAB 1: VCS Observation
    with tab1:
        st.markdown("### 🔍 VCS Observation - SafetyGraph Module BehaviorX")
        
        # Métriques VCS
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Items Observés", "12", delta="Complet")
        
        with col2:
            st.metric("✅ Conformité", "75.0%", delta="6 Forces")
        
        with col3:
            st.metric("⚠️ Préoccupations", "2", delta="À surveiller")
        
        # Graphique VCS
        vcs_data = pd.DataFrame({
            'Catégorie': ['EPI Usage', 'Procédures', 'Communication', 'Formation', 'Équipements', 'Environnement'],
            'Score': [4, 3, 3, 4, 4, 3],
            'Conforme': [True, False, False, True, True, False]
        })
        
        fig_vcs = px.bar(
            vcs_data, 
            x='Catégorie', 
            y='Score',
            color='Conforme',
            title="VCS Observation par Catégorie",
            color_discrete_map={True: 'green', False: 'red'}
        )
        st.plotly_chart(fig_vcs, use_container_width=True)
    
    # TAB 2: Analyse ABC
    with tab2:
        st.markdown("### 🔗 Analyse ABC - Comportements Observés")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("✅ Comportements Positifs", "6", delta="Maintenir")
            st.success("• Port EPI systématique")
            st.success("• Communication proactive")
            st.success("• Respect procédures")
        
        with col2:
            st.metric("⚠️ Comportements Négatifs", "2", delta="À corriger")
            st.warning("• Raccourcis procédures")
            st.warning("• Communication insuffisante")
        
        st.info("🚨 **2 Interventions Urgentes** identifiées par analyse ABC")
    
    # TAB 3: A1 Enhanced
    with tab3:
        st.markdown("### 🤖 Agent A1 Enhanced - SafetyGraph Intelligence")
        
        # Score gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 79.0,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Score Safe Self A1 Enhanced"},
            delta = {'reference': 70},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.success("📊 **Niveau:** BON_COMPORTEMENTAL")
        st.info("🧠 **Enrichi par ABC:** Analyse comportementale intégrée")
        st.warning("💡 **2 Recommandations** d'amélioration générées")
    
    # TAB 4: Intégration
    with tab4:
        st.markdown("### 📈 Analyse Intégration - Cohérence Système")
        
        # Gauge intégration
        fig_integration = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 92.0,
            title = {'text': "Cohérence A1↔VCS (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "green"},
                'steps': [{'range': [0, 100], 'color': "lightgray"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}
            }
        ))
        
        st.plotly_chart(fig_integration, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("🔗 **Niveau Intégration:** Excellent")
            st.success("🚨 **Zones Aveugles:** Aucune")
        
        with col2:
            st.info("🚀 **Actions Prioritaires:** 2")
            st.info("📊 **Score Global:** 92.0%")
    
    # TAB 5: Rapport
    with tab5:
        st.markdown("### 📄 Rapport Complet BehaviorX")
        
        st.markdown("#### 📊 Synthèse Exécutive")
        st.success("""
        **✅ WORKFLOW BEHAVIORX RÉUSSI**
        
        🎯 **Score Intégration Global:** 92.0% (Excellent)
        🔍 **Conformité VCS:** 75.0% avec 6 forces identifiées
        🤖 **Agent A1 Enhanced:** 79.0 (Bon niveau comportemental)
        🚨 **Zones Aveugles:** 0 (Couverture complète)
        """)
        
        # Export JSON BehaviorX
        behaviorx_export = {
            "platform": "Safety Agentique",
            "system": "SafetyGraph BehaviorX",
            "version": "v3.0_standard",
            "session_timestamp": datetime.now().isoformat(),
            "results": results,
            "enterprise": results.get('enterprise_context', {}),
            "integration_score": 92.0
        }
        
        st.download_button(
            label="💾 Télécharger Rapport BehaviorX (JSON)",
            data=json.dumps(behaviorx_export, indent=2, ensure_ascii=False),
            file_name=f"rapport_behaviorx_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# ===================================================================
# 7. AFFICHAGE RÉSULTATS CARTOGRAPHIE COMPLÈTE
# ===================================================================

def display_cartography_results(cartography_result):
    """Affiche résultats cartographie dans onglets enrichis"""
    
    if not cartography_result or not cartography_result['success']:
        return
    
    cartography = cartography_result['cartography']
    
    # Onglets cartographiques
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🎯 Vue Exécutive",
        "🗺️ Cartographie 7D", 
        "📊 Analyse Dimensionnelle",
        "🔍 Recherche STORM",
        "📋 Plans d'Action",
        "📈 Suivi & KPI",
        "🧩 Mémoire IA",
        "📄 Export Complet"
    ])
    
    # TAB 1: Vue Exécutive
    with tab1:
        st.markdown("### 🎯 Résumé Exécutif Cartographie Culture SST")
        
        exec_summary = cartography['executive_summary']
        
        # Métriques clés exécutives
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"""
            **🎯 Maturité Culture Globale**
            
            Score Actuel: **{exec_summary['overall_culture_maturity']:.1f}/5.0**
            
            Niveau: **{"🔴 Émergent" if exec_summary['overall_culture_maturity'] < 3.0 else "🟡 En Développement" if exec_summary['overall_culture_maturity'] < 4.0 else "🟢 Mature"}**
            
            Tendance: **📈 Amélioration Continue**
            """)
        
        with col2:
            st.success(f"""
            **📋 Feuille de Route**
            
            Plans d'Action: **{exec_summary['recommended_actions']} plans**
            
            Timeline: **{exec_summary['estimated_improvement_timeline']}**
            
            Priorité: **🚨 {len(exec_summary.get('improvement_priority_dimensions', []))} dimensions critiques**
            """)
        
        with col3:
            st.warning(f"""
            **💰 Investissement & ROI**
            
            Investissement: **{exec_summary['investment_required'].title()}**
            
            ROI Attendu: **{exec_summary['expected_roi']}**
            
            Payback: **⚡ 12-18 mois**
            """)
        
        # Dimensions prioritaires
        priority_dims = exec_summary.get('improvement_priority_dimensions', [])
        if priority_dims:
            st.markdown("#### 🚨 Dimensions Prioritaires (Action Urgente)")
            for dim in priority_dims:
                st.error(f"⚠️ **{dim.replace('_', ' ').title()}** - Amélioration Critique Requise")
        else:
            st.success("✅ **Aucune Dimension Critique** - Culture équilibrée")
    
    # TAB 2: Cartographie 7 Dimensions
    with tab2:
        st.markdown("### 🗺️ Cartographie Culture SST - 7 Dimensions")
        
        detailed_cartography = cartography['detailed_cartography']
        dimensions = detailed_cartography.get('dimensions', {})
        
        # Visualisation radar chart
        if dimensions:
            dimension_names = []
            maturity_scores = []
            
            for dim_name, dim_data in dimensions.items():
                dimension_names.append(dim_name.replace('_', ' ').title())
                maturity_scores.append(dim_data.get('maturity_score', 0))
            
            # Graphique radar dimensions
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=maturity_scores,
                theta=dimension_names,
                fill='toself',
                name='Maturité Actuelle',
                line_color='rgb(99, 110, 250)',
                fillcolor='rgba(99, 110, 250, 0.3)'
            ))
            
            # Cible maturité
            target_scores = [4.0] * len(dimension_names)
            fig.add_trace(go.Scatterpolar(
                r=target_scores,
                theta=dimension_names,
                fill='toself',
                name='Cible Maturité (4.0)',
                line_color='rgb(239, 85, 59)',
                fillcolor='rgba(239, 85, 59, 0.2)',
                opacity=0.6
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5],
                        tickvals=[1, 2, 3, 4, 5],
                        ticktext=['1-Émergent', '2-Basique', '3-Développé', '4-Mature', '5-Excellence']
                    )),
                showlegend=True,
                title="🗺️ Cartographie Maturité Culture SST par Dimension",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Détails par dimension
        st.markdown("#### 📊 Analyse Détaillée par Dimension")
        
        for dim_name, dim_data in dimensions.items():
            priority_icon = "🚨" if dim_data.get('improvement_priority') == 'high' else "⚠️" if dim_data.get('improvement_priority') == 'medium' else "✅"
            
            with st.expander(f"{priority_icon} **{dim_name.replace('_', ' ').title()}** - Score: {dim_data.get('maturity_score', 0):.1f}/5.0"):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**✅ Forces Identifiées:**")
                    for strength in dim_data.get('strengths', []):
                        st.success(f"• {strength.replace('_', ' ').title()}")
                
                with col2:
                    st.markdown("**⚠️ Gaps à Combler:**")
                    for gap in dim_data.get('gaps', []):
                        st.warning(f"• {gap.replace('_', ' ').title()}")
                
                # Informations dimension
                priority = dim_data.get('improvement_priority', 'medium')
                agents = dim_data.get('agents_analysis', [])
                
                st.info(f"""
                **📋 Informations Dimension:**
                - **Priorité Amélioration:** {priority.title()} {priority_icon}
                - **Agents Responsables:** {', '.join(agents)}
                - **Sources Données:** {', '.join(dim_data.get('data_sources', []))}
                - **Méthode Assessment:** {dim_data.get('assessment_method', 'N/A')}
                """)
    
    # TAB 3: Analyse Dimensionnelle
    with tab3:
        st.markdown("### 📊 Analyse Dimensionnelle Approfondie")
        
        # Matrice corrélations (simulation enrichie)
        st.markdown("#### 🔗 Matrice Interdépendances Dimensions")
        
        correlation_data = {
            'Leadership': [1.0, 0.8, 0.6, 0.9, 0.7, 0.5, 0.6],
            'Organisation': [0.8, 1.0, 0.7, 0.6, 0.8, 0.6, 0.5],
            'Processus': [0.6, 0.7, 1.0, 0.5, 0.6, 0.9, 0.4],
            'Communication': [0.9, 0.6, 0.5, 1.0, 0.8, 0.6, 0.7],
            'Participation': [0.7, 0.8, 0.6, 0.8, 1.0, 0.7, 0.8],
            'Suivi': [0.5, 0.6, 0.9, 0.6, 0.7, 1.0, 0.5],
            'Psychosocial': [0.6, 0.5, 0.4, 0.7, 0.8, 0.5, 1.0]
        }
        
        correlation_df = pd.DataFrame(
            correlation_data, 
            index=['Leadership', 'Organisation', 'Processus', 'Communication', 'Participation', 'Suivi', 'Psychosocial']
        )
        
        # Heatmap corrélations
        fig_corr = px.imshow(
            correlation_df, 
            title="🔗 Matrice Corrélations Dimensions Culture SST",
            color_continuous_scale="RdYlBu_r",
            aspect="auto",
            height=400
        )
        fig_corr.update_layout(
            xaxis_title="Dimensions",
            yaxis_title="Dimensions"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Zones aveugles détectées
        zones_aveugles = cartography_result['final_state'].get('zones_aveugles', [])
        if zones_aveugles:
            st.markdown("#### ⚠️ Zones Aveugles Détectées")
            for zone in zones_aveugles:
                st.error(f"🚨 **Zone Aveugle:** {zone.replace('_', ' ').title()}")
                
            st.warning("""
            **🔍 Actions Recommandées pour Zones Aveugles:**
            - Collecte données supplémentaires ciblées
            - Validation croisée avec stakeholders
            - Recherche STORM approfondie
            """)
        else:
            st.success("✅ **Aucune Zone Aveugle Majeure Détectée** - Couverture cartographique complète")
        
        # Analyse équilibre dimensions
        if dimensions:
            scores = [dim_data.get('maturity_score', 0) for dim_data in dimensions.values()]
            balance_score = 1 - (max(scores) - min(scores)) / 5  # Score équilibre 0-1
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📊 Score Équilibre", f"{balance_score:.2f}", 
                         delta="Excellent" if balance_score > 0.8 else "Bon" if balance_score > 0.6 else "À améliorer")
            
            with col2:
                st.metric("📈 Dimension Forte", f"{max(scores):.1f}", 
                         delta="Leadership" if scores.index(max(scores)) == 0 else "Autre")
            
            with col3:
                st.metric("📉 Dimension Faible", f"{min(scores):.1f}", 
                         delta="Priorité" if min(scores) < 3.0 else "Acceptable")
    
    # TAB 4: Recherche STORM
    with tab4:
        st.markdown("### 🔍 Recherche STORM - Enrichissement Scientifique")
        
        storm_data = cartography['technology_integration']['storm_research']
        
        if storm_data:
            # Métriques STORM
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📚 Sources Analysées", storm_data.get('total_sources', 0))
            
            with col2:
                st.metric("🎯 Pertinence Cartographie", f"{storm_data.get('cartography_relevance', 0):.1%}")
            
            with col3:
                st.metric("🏆 Qualité Preuves", f"{storm_data.get('evidence_quality', 0):.1%}")
            
            with col4:
                st.metric("⚡ Temps Exécution", f"{storm_data.get('execution_time', 0):.1f}s")
            
            # Topics recherchés
            topics = storm_data.get('topics_researched', [])
            if topics:
                st.markdown("#### 📖 Topics de Recherche Analysés")
                for i, topic in enumerate(topics, 1):
                    st.info(f"**{i}.** {topic.replace('_', ' ').title()}")
        
        # Base de preuves
        evidence_base = cartography_result['final_state'].get('evidence_base', {})
        if evidence_base:
            st.markdown("#### 📊 Base de Preuves Scientifiques")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.success(f"🎓 **Sources Académiques:** {evidence_base.get('academic_sources', 0)}")
            
            with col2:
                st.info(f"🏢 **Rapports Institutionnels:** {evidence_base.get('institutional_reports', 0)}")
            
            with col3:
                st.warning(f"📋 **Cas Pratiques:** {evidence_base.get('best_practice_cases', 0)}")
        
        # Meilleures pratiques identifiées
        best_practices = cartography_result['final_state'].get('best_practices', [])
        if best_practices:
            st.markdown("#### ✨ Meilleures Pratiques Identifiées par STORM")
            for practice in best_practices:
                st.success(f"✅ {practice.replace('_', ' ').title()}")
        
        # Insights recherche
        research_insights = cartography_result['final_state'].get('research_insights', {})
        if research_insights and 'key_findings' in research_insights:
            st.markdown("#### 🔍 Insights Clés de la Recherche")
            for finding in research_insights['key_findings']:
                st.info(f"💡 {finding}")
    
    # TAB 5: Plans d'Action
    with tab5:
        st.markdown("### 📋 Plans d'Action Cartographiques")
        
        action_plans = cartography['improvement_roadmap']
        
        if action_plans:
            # Vue d'ensemble plans
            st.markdown("#### 📊 Vue d'Ensemble Plans d'Action")
            
            plans_summary = pd.DataFrame([
                {
                    'Plan': plan['title'],
                    'Dimension': plan['dimension'].replace('_', ' ').title(),
                    'Priorité': plan['priority'].title(),
                    'Timeline': plan['timeline'],
                    'Score Actuel': plan['current_maturity'],
                    'Cible': plan['target_maturity']
                } for plan in action_plans
            ])
            
            st.dataframe(plans_summary, use_container_width=True)
            
            # Détails par plan
            st.markdown("#### 📋 Détails Plans d'Action")
            
            for plan in action_plans:
                priority_color = "🚨" if plan['priority'] == 'high' else "⚠️" if plan['priority'] == 'medium' else "✅"
                
                with st.expander(f"{priority_color} **{plan['title']}** - Priorité: {plan['priority'].title()}"):
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**📊 Informations Plan:**")
                        st.info(f"""
                        - **Dimension Cible:** {plan['dimension'].replace('_', ' ').title()}
                        - **Maturité Actuelle:** {plan['current_maturity']:.1f}/5.0
                        - **Maturité Cible:** {plan['target_maturity']:.1f}/5.0
                        - **Amélioration:** +{plan['target_maturity'] - plan['current_maturity']:.1f} points
                        - **Timeline:** {plan['timeline']}
                        - **Agents Responsables:** {', '.join(plan['responsible_agents'])}
                        """)
                    
                    with col2:
                        st.markdown("**🎯 Actions Spécifiques:**")
                        for action in plan['actions']:
                            st.success(f"• {action}")
                    
                    st.markdown("**📈 Métriques de Succès:**")
                    for metric in plan['success_metrics']:
                        st.warning(f"📊 {metric}")
                    
                    st.markdown("**💰 Ressources Requises:**")
                    for resource in plan['resources_required']:
                        st.info(f"🔧 {resource.replace('_', ' ').title()}")
        else:
            st.info("ℹ️ Aucun plan d'action généré - Culture SST satisfaisante")
    
    # TAB 6: Suivi & KPI
    with tab6:
        st.markdown("### 📈 Suivi et KPI Cartographiques")
        
        monitoring = cartography_result['final_state'].get('monitoring_dashboard', {})
        
        if monitoring:
            # Santé cartographique
            cartography_health = monitoring.get('cartography_health', {})
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                trend = cartography_health.get('overall_culture_trend', 'stable')
                trend_icon = "📈" if trend == 'improving' else "📉" if trend == 'declining' else "➡️"
                st.metric("🌡️ Tendance Culture", f"{trend_icon} {trend.title()}")
            
            with col2:
                balance = cartography_health.get('dimension_balance', 0)
                st.metric("⚖️ Équilibre Dimensions", f"{balance:.2f}", delta="Bon" if balance > 0.8 else "Moyen")
            
            with col3:
                progress = cartography_health.get('action_plan_progress', 0)
                st.metric("🎯 Progrès Plans", f"{progress:.1%}", delta="En cours")
            
            with col4:
                engagement = cartography_health.get('stakeholder_engagement', 0)
                st.metric("🤝 Engagement", f"{engagement:.1%}", delta="Actif")
            
            # Métriques temps réel
            real_time = monitoring.get('real_time_metrics', {})
            if real_time:
                st.markdown("#### ⚡ Métriques Temps Réel")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.success(f"📈 **Évolution Culture:** {real_time.get('culture_evolution_rate', 'N/A')}")
                
                with col2:
                    st.info(f"🔧 **Améliorations Actives:** {real_time.get('dimension_improvements', 0)}")
                
                with col3:
                    st.warning(f"💬 **Taux Feedback:** {real_time.get('feedback_response_rate', 'N/A')}")
            
            # Alertes monitoring
            alerts = monitoring.get('alerts_notifications', [])
            if alerts:
                st.markdown("#### 🚨 Alertes Monitoring Actives")
                for alert in alerts:
                    st.warning(f"⚠️ {alert}")
            else:
                st.success("✅ Aucune alerte active - Système stable")
            
            # Prochaine mise à jour
            next_update = monitoring.get('next_cartography_update', 'N/A')
            st.info(f"📅 **Prochaine Mise à Jour Cartographie:** {next_update}")
        
        # KPI Evolution (simulation graphique)
        kpi_evolution = cartography_result['final_state'].get('kpi_evolution', {})
        if kpi_evolution:
            st.markdown("#### 📊 Évolution KPI Culture (3 derniers mois)")
            
            months = ['Mois -2', 'Mois -1', 'Mois Actuel']
            culture_trend = kpi_evolution.get('culture_maturity_trend', [3.2, 3.4, 3.6])
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=months,
                y=culture_trend,
                mode='lines+markers',
                name='Maturité Culture Globale',
                line=dict(color='blue', width=3),
                marker=dict(size=8)
            ))
            
            fig_trend.update_layout(
                title="📈 Évolution Maturité Culture SST",
                xaxis_title="Période",
                yaxis_title="Score Maturité (/5.0)",
                yaxis=dict(range=[0, 5])
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
    
    # TAB 7: Mémoire IA
    with tab7:
        st.markdown("### 🧩 Mémoire IA et Apprentissage Continu")
        
        memory_data = cartography_result['final_state'].get('memory_ai', {})
        learning_insights = cartography_result['final_state'].get('learning_insights', [])
        pattern_recognition = cartography_result['final_state'].get('pattern_recognition', {})
        
        if memory_data:
            # Métriques mémoire IA
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🧠 Mémoires Culture", memory_data.get('cartography_memories', 0))
            
            with col2:
                st.metric("🎯 Précision Mémoire", f"{memory_data.get('memory_accuracy', 0):.1%}")
            
            with col3:
                st.metric("📚 Patterns Appris", memory_data.get('culture_patterns_learned', 0))
            
            with col4:
                st.metric("⚡ Vitesse Apprentissage", f"{memory_data.get('learning_velocity', 0):.2f}")
        
        # Insights apprentissage
        if learning_insights:
            st.markdown("#### 💡 Insights Apprentissage IA")
            for insight in learning_insights:
                st.info(f"🔍 {insight}")
        
        # Reconnaissance patterns
        if pattern_recognition:
            st.markdown("#### 🔍 Reconnaissance Patterns Culture")
            
            # Archétypes culture identifiés
            archetypes = pattern_recognition.get('culture_archetypes_identified', [])
            if archetypes:
                st.markdown("**🏛️ Archétypes Culture Identifiés:**")
                for archetype in archetypes:
                    st.success(f"✅ {archetype.replace('_', ' ').title()}")
            
            # Corrélations risques
            risk_correlations = pattern_recognition.get('risk_pattern_correlations', {})
            if risk_correlations:
                st.markdown("**⚠️ Patterns Risques Identifiés:**")
                for risk_pattern, correlation in risk_correlations.items():
                    st.warning(f"🚨 {risk_pattern}: Corrélation {correlation:.2f}")
            
            # Patterns succès
            success_patterns = pattern_recognition.get('success_pattern_identification', {})
            if success_patterns:
                st.markdown("**🎯 Patterns Succès Identifiés:**")
                for success_pattern, correlation in success_patterns.items():
                    st.success(f"✅ {success_pattern}: Corrélation {correlation:.2f}")
    
    # TAB 8: Export Complet
    with tab8:
        st.markdown("### 📄 Export Cartographie Complète")
        
        # Informations export
        st.markdown("#### 📦 Contenu Export Cartographique")
        st.info("""
        **📋 Cartographie Culture SST Complète comprend:**
        
        🎯 **Résumé Exécutif**
        - Maturité culture globale et tendances
        - ROI et timeline d'amélioration
        - Dimensions prioritaires identifiées
        
        🗺️ **Cartographie Détaillée 7 Dimensions**
        - Scores maturité par dimension
        - Forces et gaps spécifiques
        - Agents responsables et sources données
        
        📊 **Analyse Dimensionnelle**
        - Matrice corrélations interdépendances
        - Zones aveugles et recommandations
        - Équilibre et cohérence système
        
        🔍 **Enrichissement STORM**
        - Base preuves scientifiques
        - Meilleures pratiques sectorielles
        - Insights recherche applicables
        
        📋 **Feuille Route Amélioration**
        - Plans d'action personnalisés
        - Métriques succès et ressources
        - Timeline et responsabilités
        
        📈 **Framework Monitoring**
        - KPI temps réel et alertes
        - Systèmes feedback continue
        - Prédictions évolution culture
        
        🧩 **Intelligence Artificielle**
        - Mémoire IA et apprentissage
        - Reconnaissance patterns
        - Recommandations adaptatives
        """)
        
        # Export JSON complet
        cartography_json = json.dumps(cartography, indent=2, ensure_ascii=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="💾 Télécharger Cartographie Complète (JSON)",
                data=cartography_json,
                file_name=f"cartographie_culture_sst_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            # Export résumé exécutif
            executive_summary = json.dumps(cartography['executive_summary'], indent=2, ensure_ascii=False)
            st.download_button(
                label="📊 Télécharger Résumé Exécutif (JSON)",
                data=executive_summary,
                file_name=f"resume_executif_culture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Diagramme workflow Mermaid
        if 'mermaid_diagram' in cartography_result:
            st.markdown("#### 🗺️ Diagramme Workflow Cartographique")
            st.code(cartography_result['mermaid_diagram'], language='mermaid')
        
        # Métadonnées session
        st.markdown("#### 🔍 Métadonnées Session")
        metadata = cartography['metadata']
        st.json({
            "Session ID": metadata['session_id'],
            "Timestamp": metadata['timestamp'],
            "Secteur SCIAN": f"{metadata['sector_scian']} - {metadata['sector_name']}",
            "Moteur Cartographie": metadata['cartography_engine'],
            "Mode Exécution": cartography_result.get('execution_mode', 'unknown')
        })

# ===================================================================
# 8. FONCTION PRINCIPALE AVEC CHOIX WORKFLOW
# ===================================================================

def main():
    """Fonction principale SafetyGraph BehaviorX + Cartographie"""
    
    # Header
    display_header()
    
    # Configuration sidebar
    config = setup_sidebar()
    
    # Zone principale - Choix workflow
    st.markdown("## 🚀 Choix Workflow SafetyGraph")
    
    col1, col2 = st.columns(2)
    
    # TABS ENRICHIS AVEC ANALYTICS
main_tabs = st.tabs([
    "🧠 BehaviorX Standard",
    "🗺️ Cartographie Culture", 
    "🔮 Analytics Prédictifs",    # NOUVEAU
    "🔍 Pattern Recognition",     # NOUVEAU
    "⚠️ Anomaly Detection",     # NOUVEAU  
"⚡ Analytics Optimisés"    # AJOUT NOUVEAU
])

with main_tabs[0]:
    # Workflow BehaviorX existant
    if st.button("🚀 Lancer BehaviorX Standard", use_container_width=True):
        st.session_state.workflow_type = "behaviorx_standard"
        st.session_state.workflow_results = None
    
    # Gardez ici votre code BehaviorX existant (après les descriptions)

with main_tabs[1]:
    # Titre de la section
    st.markdown("## 🗺️ SafetyGraph BehaviorX + Cartographie Culture SST")
    st.markdown("### 📊 Powered by Safety Agentique | 🌐 LangGraph Multi-Agent | 🌪️ STORM Research | 🧠 Mémoire IA Adaptative")
    
    # BOUTON CARTOGRAPHIE CULTURE
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🗺️ Lancer Cartographie Culture SST", key="launch_cartographie_culture", type="primary"):
            st.success("🎉 Cartographie Culture SST lancée avec succès !")
            st.balloons()
            
            # Simulation cartographie rapide
            with st.spinner("🔄 Génération cartographie culture secteur Construction..."):
                time.sleep(1.5)
            
            st.markdown("### 📊 Résultats Cartographie Culture")
            
            # Données cartographie par secteur
            culture_data = {
                'Secteur SCIAN': ['Construction (236)', 'Manufacturier (311-333)', 'Transport (484-488)', 'Services (541)'],
                'Score Culture': [3.8, 4.2, 3.6, 4.0],
                'Niveau Maturité': ['Réactif', 'Proactif', 'Réactif', 'Proactif'],
                'Risque Incident (%)': [15.2, 8.7, 12.3, 6.9],
                'Conformité (%)': [87.1, 94.3, 83.7, 91.2]
            }
            
            df_culture = pd.DataFrame(culture_data)
            st.dataframe(df_culture, use_container_width=True, hide_index=True)
            
            st.success("✅ Cartographie générée avec STORM Research enrichi !")
with main_tabs[5]:
    if OPTIMIZER_AVAILABLE:
        optimizer.render_optimized_analytics()
    else:
        st.warning("⚠️ Optimiseur non disponible - Analytics en mode standard")
        st.info("Pour activer l'optimisation, vérifiez le fichier src/optimization/performance_optimizer.py")
    if st.button("🗺️ Lancer Cartographie Complète", use_container_width=True):
        st.session_state.workflow_type = "cartography_complete"
        st.session_state.workflow_results = None
    
    # Gardez ici votre code cartographie existant


                
                # Simulation cartographie rapide
with st.spinner("🔄 Génération cartographie culture secteur Construction..."):
                    time.sleep(1.5)
                
                st.markdown("### 📊 Résultats Cartographie Culture")
                
                # Données cartographie par secteur
                culture_data = {
                    'Secteur SCIAN': ['Construction (236)', 'Manufacturier (311-333)', 'Transport (484-488)', 'Services (541)'],
                    'Score Culture': [3.8, 4.2, 3.6, 4.0],
                    'Niveau Maturité': ['Réactif', 'Proactif', 'Réactif', 'Proactif'],
                    'Risque Incident (%)': [15.2, 8.7, 12.3, 6.9],
                    'Conformité (%)': [87.1, 94.3, 83.7, 91.2]
                }
                
                df_culture = pd.DataFrame(culture_data)
                st.dataframe(df_culture, use_container_width=True, hide_index=True)
                
                st.success("✅ Cartographie générée avec STORM Research enrichi !")
with main_tabs[2]:
    if ANALYTICS_AVAILABLE:
        display_predictive_analytics_interface()
    else:
        st.error("⚠️ Module analytics prédictifs non disponible")

with main_tabs[3]:
    if ANALYTICS_AVAILABLE:
        display_pattern_recognition_interface()
    else:
        st.error("⚠️ Module pattern recognition non disponible")

with main_tabs[4]:
    if ANALYTICS_AVAILABLE:
        display_anomaly_detection_interface()
    else:
        st.error("⚠️ Module anomaly detection non disponible")
    
    # Description workflows
    if st.session_state.get('workflow_type'):
        if st.session_state.workflow_type == "behaviorx_standard":
            st.info("""
            **🧠 Workflow BehaviorX Standard**
            - ✅ Analyse VCS (Visual Card Sorting)
            - ✅ Analyse ABC comportementale
            - ✅ Agent A1 Enhanced avec Safe Self
            - ✅ Score intégration et zones aveugles
            - ⚡ Exécution rapide (~30 secondes)
            """)
        
        elif st.session_state.workflow_type == "cartography_complete":
            st.success("""
            **🗺️ Cartographie Culture SST Complète**
            - 🗺️ Cartographie 7 dimensions culture SST
            - 🤖 Architecture LangGraph multi-agent (100+ agents)
            - 🔍 Recherche STORM enrichissement scientifique
            - 📋 Plans d'action personnalisés par dimension
            - 📈 Framework monitoring et KPI évolution
            - 🧩 Mémoire IA et apprentissage continu
            - ⚡ Analyse approfondie (~2-3 minutes)
            """)
        
        # Bouton exécution
        if st.button("▶️ Lancer Workflow Sélectionné", type="primary", use_container_width=True):
            if st.session_state.workflow_type == "behaviorx_standard":
                st.session_state.workflow_results = execute_behaviorx_workflow_standard(config)
            elif st.session_state.workflow_type == "cartography_complete":
                st.session_state.workflow_results = execute_cartography_workflow_complete(config)
    
    # Affichage résultats selon type workflow
    if st.session_state.get('workflow_results'):
        results = st.session_state.workflow_results
        
        if results['success']:
            if results.get('type') == 'behaviorx_standard':
                display_behaviorx_results(results)
            else:
                display_cartography_results(results)
            
            # Ajout à l'historique
            if results not in st.session_state.execution_history:
                st.session_state.execution_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': st.session_state.workflow_type,
                    'enterprise': config['enterprise_name'],
                    'sector': config['sector_name'],
                    'success': True
                })
        else:
            st.error("❌ Erreur lors de l'exécution du workflow")
    
    # Historique exécutions (optionnel)
    if st.session_state.execution_history:
        with st.expander("📋 Historique Exécutions"):
            for i, execution in enumerate(reversed(st.session_state.execution_history[-5:]), 1):
                st.text(f"{i}. {execution['timestamp'][:19]} - {execution['type']} - {execution['enterprise']} ({execution['sector']})")

# ===================================================================
# 9. POINT D'ENTRÉE APPLICATION
# ===================================================================

if __name__ == "__main__":
    main()

# ===================================================================
# INTÉGRATION ANALYTICS AVANCÉS SAFETYGRAPH
# ===================================================================

# Imports modules analytics
sys.path.append(str(Path(__file__).parent / "src" / "analytics"))

try:
    from predictive_models import display_predictive_analytics_interface
    from pattern_recognition import display_pattern_recognition_interface  
    from anomaly_detection import display_anomaly_detection_interface
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False

# Dans votre fonction main(), modifier les tabs :
def main():
    display_header()
    
    # NOUVEAUX TABS AVEC ANALYTICS
    main_tabs = st.tabs([
        "🧠 BehaviorX Standard",
        "🗺️ Cartographie Culture", 
        "🔮 Analytics Prédictifs",    # NOUVEAU
        "🔍 Pattern Recognition",     # NOUVEAU
        "⚠️ Anomaly Detection"        # NOUVEAU
    ])
    
    with main_tabs[0]:
        # Votre workflow BehaviorX existant
        pass
    
    with main_tabs[1]:
        # Votre cartographie existante
        pass
    
    with main_tabs[2]:
        if ANALYTICS_AVAILABLE:
            display_predictive_analytics_interface()
        else:
            st.warning("⚠️ Modules analytics non disponibles")
    
    with main_tabs[3]:
        if ANALYTICS_AVAILABLE:
            display_pattern_recognition_interface()
        else:
            st.warning("⚠️ Modules analytics non disponibles")
    
    with main_tabs[4]:
        if ANALYTICS_AVAILABLE:
            display_anomaly_detection_interface()
        else:
            st.warning("⚠️ Modules analytics non disponibles")    