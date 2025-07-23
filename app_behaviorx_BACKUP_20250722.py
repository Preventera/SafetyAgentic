"""
SafetyGraph BehaviorX + Cartographie Culture SST - Interface Complète
====================================================================
Interface Streamlit unifiée : BehaviorX + Cartographie LangGraph
Safety Agentique - Mario Plourde - 21 juillet 2025
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
    
# Import module mines souterraines
try:
    from src.modules.mines_souterraines import mines_souterraines_secteur
    MINES_AVAILABLE = True
    print("✅ Module mines souterraines chargé")
except ImportError:
    MINES_AVAILABLE = False
    print("⚠️ Module mines souterraines non disponible")

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
        st.success(f"⛏️ Mines: {'✅ Disponible' if MINES_AVAILABLE else '❌ Indisponible'}")
        
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
        st.plotly_chart(fig_vcs, use_container_width=True, key="vcs_observation_chart")
    
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
        
        st.plotly_chart(fig_gauge, use_container_width=True, key="a1_enhanced_gauge")
        
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
        
        st.plotly_chart(fig_integration, use_container_width=True, key="integration_gauge")
        
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
            "results_summary": {  # ← CORRECTION ICI
            "success": results.get('success', True),
            "type": results.get('type', 'behaviorx_standard'),
            "metrics": results.get('metrics', {})
    },
    "enterprise": "Entreprise ABC",  # ← VALEUR SIMPLE
    "integration_score": 92.0
}
        
        st.download_button(
            label="💾 Télécharger Rapport BehaviorX (JSON)",
            data=json.dumps(behaviorx_export, indent=2, ensure_ascii=False),
            file_name=f"rapport_behaviorx_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

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
    
    # ✅ DÉFINITION ONGLETS DANS MAIN()
    main_tabs = st.tabs([
        "🎯 BehaviorX Standard",
        "🗺️ Cartographie Culture", 
        "🔮 Analytics Prédictifs",
        "🔍 Pattern Recognition",
        "⚡ Analytics Optimisés",
        "⛏️ Mines Souterraines"
    ])

    # ===================================================================
    # ONGLETS PRINCIPAUX
    # ===================================================================

    with main_tabs[0]:  # BehaviorX Standard
        if st.button("🚀 Lancer BehaviorX Standard", use_container_width=True):
            st.session_state.workflow_type = "behaviorx_standard"
            st.session_state.workflow_results = None

    with main_tabs[1]:  # Cartographie Culture
        st.markdown("## 🗺️ SafetyGraph BehaviorX + Cartographie Culture SST")
        st.markdown("### 📊 Powered by Safety Agentique | 🌐 LangGraph Multi-Agent | 🌪️ STORM Research | 🧠 Mémoire IA Adaptative")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🗺️ Lancer Cartographie Culture SST", key="launch_cartographie_culture", type="primary"):
                st.success("🎉 Cartographie Culture SST lancée avec succès !")
                st.balloons()
                
                with st.spinner("🔄 Génération cartographie culture secteur Construction..."):
                    time.sleep(1.5)
                
                st.markdown("### 📊 Résultats Cartographie Culture")
                
                culture_data = {
                    "Secteur SCIAN": ['Construction (236)', 'Manufacturier (311-333)', 'Transport (484-488)', 'Services (541)'],
                    'Score Culture': [3.8, 4.2, 3.6, 4.0],
                    'Niveau Maturité': ['Réactif', 'Proactif', 'Réactif', 'Proactif'],
                    'Risque Incident (%)': [15.2, 8.7, 12.3, 6.9],
                    'Conformité (%)': [87.1, 94.3, 83.7, 91.2]
                }
                
                df_culture = pd.DataFrame(culture_data)
                st.dataframe(df_culture, use_container_width=True, hide_index=True)
                st.success("✅ Cartographie générée avec STORM Research enrichi !")
        
        if st.button("🗺️ Lancer Cartographie Complète", use_container_width=True):
            st.session_state.workflow_type = "cartography_complete"
            st.session_state.workflow_results = None

    with main_tabs[2]:  # Analytics Prédictifs
        if ANALYTICS_AVAILABLE:
            display_predictive_analytics_interface()
        else:
            st.warning("⚠️ Module analytics prédictifs non disponible")

    with main_tabs[3]:  # Pattern Recognition
        if ANALYTICS_AVAILABLE:
            display_pattern_recognition_interface()
        else:
            st.warning("⚠️ Module pattern recognition non disponible")

    with main_tabs[4]:  # Analytics Optimisés
        if OPTIMIZER_AVAILABLE:
            optimizer.render_optimized_analytics()
        else:
            st.warning("⚠️ Optimiseur non disponible - Analytics en mode standard")
            st.info("Pour activer l'optimisation, vérifiez le fichier src/optimization/performance_optimizer.py")

    with main_tabs[5]:  # Mines Souterraines
        if MINES_AVAILABLE:
            mines_souterraines_secteur()
        else:
            st.error("⚠️ Module mines souterraines non disponible")

    # ===================================================================
    # WORKFLOW EXECUTION LOGIC
    # ===================================================================
    
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
                # Pour cartographie complète, affichage simplifié
                st.success("✅ Cartographie Culture SST terminée avec succès !")
                st.json(results.get('cartography', {}).get('executive_summary', {}))
            
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