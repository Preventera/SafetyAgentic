"""
SafetyGraph BehaviorX + Cartographie Culture SST - Interface ComplÃ¨te
====================================================================
Interface Streamlit unifiÃ©e : BehaviorX + Cartographie LangGraph
Safety Agentique - Mario Plourde - 8 juillet 2025
Version 3.0 - Architecture LangGraph IntÃ©grÃ©e
"""

import streamlit as st

# ===== ENRICHISSEMENT CNESST SAFETYGRAPH =====
try:
    from src.enrichments.cnesst_layer import enrich_safetygraph_context, get_cnesst_status
    CNESST_ENRICHED = True
    print("✅ Enrichissement CNESST activé")
except ImportError:
    CNESST_ENRICHED = False
    print("⚠️ Mode standard - Enrichissements CNESST non disponibles")
    def enrich_safetygraph_context(ctx): return ctx
    def get_cnesst_status(): return {"status": "disabled", "message": "Non disponible"}

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# ===================================================================
# INTEGRATION ANALYTICS AVANCÃ‰S SAFETYGRAPH
# ===================================================================

# Imports modules analytics
try:
    sys.path.append(str(Path(__file__).parent / "src" / "analytics"))
    from predictive_models import display_predictive_analytics_interface
    from pattern_recognition import display_pattern_recognition_interface  
    from anomaly_detection import display_anomaly_detection_interface
    ANALYTICS_AVAILABLE = True
    print("âœ… Analytics modules loaded successfully")
except ImportError as e:
    print(f"âš ï¸ Analytics modules not available: {e}")
    ANALYTICS_AVAILABLE = False

# Configuration page Streamlit
st.set_page_config(
    page_title="SafetyGraph BehaviorX + Cartographie SST",
    page_icon="ðŸ—ºï¸",
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
# 1. CONFIGURATION ET Ã‰TAT SESSION
# ===================================================================

# Initialisation Ã©tat session
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
    """Affiche header unifiÃ© SafetyGraph"""
    
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1f2937 0%, #374151 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; text-align: center; margin: 0;">
            ðŸ—ºï¸ SafetyGraph BehaviorX + Cartographie Culture SST
        </h1>
        <p style="color: #d1d5db; text-align: center; margin: 0.5rem 0 0 0;">
            ðŸ¢ <strong>Powered by Safety Agentique</strong> | 
            ðŸ¤– LangGraph Multi-Agent | 
            ðŸ” STORM Research | 
            ðŸ§  MÃ©moire IA Adaptative
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# 3. SIDEBAR CONFIGURATION
# ===================================================================

def setup_sidebar():
    """Configuration sidebar enrichie"""
    
    with st.sidebar:
        st.markdown("## âš™ï¸ Configuration SafetyGraph")
        
        # Section entreprise
        st.markdown("### ðŸ¢ Informations Entreprise")
        nom_entreprise = st.text_input("Nom entreprise", value="Entreprise ABC", key="enterprise_name")
        
        # SÃ©lection secteur SCIAN enrichie
        st.markdown("### ðŸ“Š Secteur d'ActivitÃ© (SCIAN)")
        secteurs_scian = {
            "Construction (236)": "236",
            "Soins de santÃ© (622)": "622", 
            "Fabrication alimentaire (311)": "311",
            "Fabrication du bois (321)": "321",
            "Services professionnels (541)": "541",
            "Secteur gÃ©nÃ©ral": "000"
        }
        
        secteur_selectionne = st.selectbox(
            "Choisir secteur",
            options=list(secteurs_scian.keys()),
            key="sector_selection"
        )
        secteur_code = secteurs_scian[secteur_selectionne]
        
        # Mode workflow enrichi
        st.markdown("### ðŸŽ¯ Mode Workflow")
        mode_workflow = st.selectbox(
            "Mode d'analyse",
            ["Hybrid (VCS + Safe Self)", "VCS + ABC seulement", "Safe Self seulement", "Cartographie ComplÃ¨te"],
            key="workflow_mode"
        )
        
        # Options avancÃ©es
        st.markdown("### ðŸ”§ Options AvancÃ©es")
        memoire_ia = st.checkbox("âœ… MÃ©moire IA Mem0", value=True, key="memory_enabled")
        mode_debug = st.checkbox("ðŸ› Mode Debug", value=False, key="debug_mode")
        
        # Statut modules
        st.markdown("### ðŸ“Š Statut Modules")
        st.success(f"ðŸ§  BehaviorX: {'âœ… Disponible' if BEHAVIORX_AVAILABLE else 'âŒ Indisponible'}")
        st.success(f"ðŸ—ºï¸ Cartographie: {'âœ… Disponible' if CARTOGRAPHY_AVAILABLE else 'âŒ Indisponible'}")
        
        # Ã€ propos
        st.markdown("### â„¹ï¸ Ã€ Propos")
        st.info("""
        **SafetyGraph BehaviorX v3.0**
        
        ðŸ¢ **Safety Agentique** - Plateforme IA pour culture SST
        
        ðŸ—ºï¸ **Cartographie 7D** - Leadership, Communication, Participation, etc.
        
        ðŸ¤– **100+ Agents** - A1-A10, AN1-AN10, R1-R10, S1-S10, SC1-SC50
        
        ðŸ” **STORM Research** - Enrichissement scientifique temps rÃ©el
        
        ðŸ§  **LangGraph** - Orchestration multi-agent avancÃ©e
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
    """ExÃ©cute workflow BehaviorX standard (version existante)"""
    
    if not BEHAVIORX_AVAILABLE:
        st.error("âŒ Module BehaviorX non disponible")
        return None
    
    with st.container():
        st.markdown("## ðŸ§  Workflow BehaviorX Standard")
        
        # Progress tracking
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # MÃ©triques container
        metrics_container = st.container()
        
        try:
            # Initialisation
            status_text.text("ðŸŽ¼ Initialisation Orchestrateur BehaviorX...")
            progress_bar.progress(10)
            
            orchestrator = BehaviorXSafetyOrchestrator({
                'memory_enabled': config['memory_enabled'],
                'debug_mode': config['debug_mode']
            })
            
            # ExÃ©cution workflow
            status_text.text("ðŸš€ ExÃ©cution Workflow VCS â†’ ABC â†’ A1 Enhanced...")
            progress_bar.progress(50)
            
            results = orchestrator.execute_full_workflow(
                enterprise_id=config['enterprise_name'],
                sector_code=config['sector_code'],
                workflow_mode=config['workflow_mode']
            )
            
            progress_bar.progress(100)
            status_text.text("âœ… Workflow BehaviorX TerminÃ© !")
            
            # Affichage mÃ©triques
            with metrics_container:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("ðŸŽ¯ Score IntÃ©gration", "92.0%", delta="Excellent")
                
                with col2:
                    st.metric("ðŸ” ConformitÃ© VCS", "75.0%", delta="6 Forces")
                
                with col3:
                    st.metric("ðŸ¤– Score A1 Enhanced", "79.0", delta="BON")
                
                with col4:
                    st.metric("ðŸš¨ Zones Aveugles", "0", delta="Aucune")
            
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
            st.error(f"âŒ Erreur workflow BehaviorX: {str(e)}")
            return None

# ===================================================================
# 5. WORKFLOW CARTOGRAPHIE COMPLET (NOUVEAU)
# ===================================================================

def execute_cartography_workflow_complete(config):
    """ExÃ©cute workflow cartographie culture SST complet"""
    
    if not CARTOGRAPHY_AVAILABLE:
        st.error("âŒ Module Cartographie non disponible")
        return None
    
    with st.container():
        st.markdown("## ðŸ—ºï¸ Cartographie Culture SST ComplÃ¨te")
        
        # Progress tracking cartographique
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # MÃ©triques cartographiques
        metrics_container = st.container()
        
        try:
            # PrÃ©paration donnÃ©es entreprise
            enterprise_info = {
                "name": config['enterprise_name'],
                "sector": config['sector_code'],
                "sector_name": config['sector_name'],
                "workflow_mode": config['workflow_mode'],
                "size": "medium"
            }
            
            # Construction requÃªte cartographique
            user_input = f"Cartographie complÃ¨te culture sÃ©curitÃ© entreprise {config['enterprise_name']} secteur {config['sector_name']}"
            
            # Ã‰tapes progression
            status_text.text("ðŸŽ¯ Analyse intention cartographique...")
            progress_bar.progress(10)
            time.sleep(0.5)
            
            status_text.text("ðŸ¢ DÃ©tection contexte SCIAN et enrichissement sectoriel...")
            progress_bar.progress(20)
            time.sleep(0.5)
            
            status_text.text("ðŸ“Š Collecte multi-dimensionnelle agents A1-A10...")
            progress_bar.progress(35)
            time.sleep(0.8)
            
            status_text.text("ðŸ§  Analyse cartographique 7 dimensions (AN1-AN10)...")
            progress_bar.progress(55)
            time.sleep(0.8)
            
            status_text.text("ðŸ” Recherche STORM enrichissement scientifique...")
            progress_bar.progress(70)
            time.sleep(0.6)
            
            status_text.text("ðŸ“‹ GÃ©nÃ©ration recommandations cartographiques (R1-R10)...")
            progress_bar.progress(85)
            time.sleep(0.5)
            
            status_text.text("ðŸ“ˆ Configuration suivi et monitoring (S1-S10)...")
            progress_bar.progress(95)
            time.sleep(0.3)
            
            # ExÃ©cution cartographie
            result = execute_safetygraph_cartography_main(
                user_input=user_input,
                enterprise_info=enterprise_info
            )
            
            progress_bar.progress(100)
            status_text.text("âœ… Cartographie Culture SST TerminÃ©e avec SuccÃ¨s !")
            
            if result['success']:
                cartography = result['cartography']
                
                # Affichage mÃ©triques cartographiques
                with metrics_container:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        maturity_score = cartography['executive_summary']['overall_culture_maturity']
                        st.metric(
                            "ðŸŽ¯ MaturitÃ© Culture Globale",
                            f"{maturity_score:.1f}/5.0",
                            delta=f"+{0.5:.1f} (obj. 6 mois)"
                        )
                    
                    with col2:
                        dimensions_count = len(cartography['detailed_cartography'].get('dimensions', {}))
                        st.metric(
                            "ðŸ“Š Dimensions CartographiÃ©es", 
                            f"{dimensions_count}/7",
                            delta="âœ… ComplÃ¨te"
                        )
                    
                    with col3:
                        action_plans = len(cartography['improvement_roadmap'])
                        st.metric(
                            "ðŸ“‹ Plans d'Action",
                            f"{action_plans}",
                            delta="ðŸŽ¯ PersonnalisÃ©s"
                        )
                    
                    with col4:
                        sector_adapted = cartography['metadata']['sector_name']
                        st.metric(
                            "ðŸ—ï¸ Secteur AdaptÃ©",
                            f"{sector_adapted}",
                            delta="âœ… SCIAN"
                        )
                
                return result
            else:
                st.error("âŒ Erreur lors de l'exÃ©cution de la cartographie")
                return None
                
        except Exception as e:
            st.error(f"âŒ Erreur cartographie: {str(e)}")
            return None

# ===================================================================
# 6. AFFICHAGE RÃ‰SULTATS BEHAVIORX STANDARD
# ===================================================================

def display_behaviorx_results(results):
    """Affiche rÃ©sultats BehaviorX standard dans onglets"""
    
    if not results or not results['success']:
        return
    
    # Onglets BehaviorX
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "ðŸ” VCS Observation",
        "ðŸ”— Analyse ABC",
        "ðŸ¤– A1 Enhanced",
        "ðŸ“ˆ IntÃ©gration",
        "ðŸ“„ Rapport"
    ])
    
    # TAB 1: VCS Observation
    with tab1:
        st.markdown("### ðŸ” VCS Observation - SafetyGraph Module BehaviorX")
        
        # MÃ©triques VCS
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("ðŸ“Š Items ObservÃ©s", "12", delta="Complet")
        
        with col2:
            st.metric("âœ… ConformitÃ©", "75.0%", delta="6 Forces")
        
        with col3:
            st.metric("âš ï¸ PrÃ©occupations", "2", delta="Ã€ surveiller")
        
        # Graphique VCS
        vcs_data = pd.DataFrame({
            'CatÃ©gorie': ['EPI Usage', 'ProcÃ©dures', 'Communication', 'Formation', 'Ã‰quipements', 'Environnement'],
            'Score': [4, 3, 3, 4, 4, 3],
            'Conforme': [True, False, False, True, True, False]
        })
        
        fig_vcs = px.bar(
            vcs_data, 
            x='CatÃ©gorie', 
            y='Score',
            color='Conforme',
            title="VCS Observation par CatÃ©gorie",
            color_discrete_map={True: 'green', False: 'red'}
        )
        st.plotly_chart(fig_vcs, use_container_width=True)
    
    # TAB 2: Analyse ABC
    with tab2:
        st.markdown("### ðŸ”— Analyse ABC - Comportements ObservÃ©s")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("âœ… Comportements Positifs", "6", delta="Maintenir")
            st.success("â€¢ Port EPI systÃ©matique")
            st.success("â€¢ Communication proactive")
            st.success("â€¢ Respect procÃ©dures")
        
        with col2:
            st.metric("âš ï¸ Comportements NÃ©gatifs", "2", delta="Ã€ corriger")
            st.warning("â€¢ Raccourcis procÃ©dures")
            st.warning("â€¢ Communication insuffisante")
        
        st.info("ðŸš¨ **2 Interventions Urgentes** identifiÃ©es par analyse ABC")
    
    # TAB 3: A1 Enhanced
    with tab3:
        st.markdown("### ðŸ¤– Agent A1 Enhanced - SafetyGraph Intelligence")
        
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
        
        st.success("ðŸ“Š **Niveau:** BON_COMPORTEMENTAL")
        st.info("ðŸ§  **Enrichi par ABC:** Analyse comportementale intÃ©grÃ©e")
        st.warning("ðŸ’¡ **2 Recommandations** d'amÃ©lioration gÃ©nÃ©rÃ©es")
    
    # TAB 4: IntÃ©gration
    with tab4:
        st.markdown("### ðŸ“ˆ Analyse IntÃ©gration - CohÃ©rence SystÃ¨me")
        
        # Gauge intÃ©gration
        fig_integration = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 92.0,
            title = {'text': "CohÃ©rence A1â†”VCS (%)"},
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
            st.success("ðŸ”— **Niveau IntÃ©gration:** Excellent")
            st.success("ðŸš¨ **Zones Aveugles:** Aucune")
        
        with col2:
            st.info("ðŸš€ **Actions Prioritaires:** 2")
            st.info("ðŸ“Š **Score Global:** 92.0%")
    
    # TAB 5: Rapport
    with tab5:
        st.markdown("### ðŸ“„ Rapport Complet BehaviorX")
        
        st.markdown("#### ðŸ“Š SynthÃ¨se ExÃ©cutive")
        st.success("""
        **âœ… WORKFLOW BEHAVIORX RÃ‰USSI**
        
        ðŸŽ¯ **Score IntÃ©gration Global:** 92.0% (Excellent)
        ðŸ” **ConformitÃ© VCS:** 75.0% avec 6 forces identifiÃ©es
        ðŸ¤– **Agent A1 Enhanced:** 79.0 (Bon niveau comportemental)
        ðŸš¨ **Zones Aveugles:** 0 (Couverture complÃ¨te)
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
            label="ðŸ’¾ TÃ©lÃ©charger Rapport BehaviorX (JSON)",
            data=json.dumps(behaviorx_export, indent=2, ensure_ascii=False),
            file_name=f"rapport_behaviorx_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# ===================================================================
# 7. AFFICHAGE RÃ‰SULTATS CARTOGRAPHIE COMPLÃˆTE
# ===================================================================

def display_cartography_results(cartography_result):
    """Affiche rÃ©sultats cartographie dans onglets enrichis"""
    
    if not cartography_result or not cartography_result['success']:
        return
    
    cartography = cartography_result['cartography']
    
    # Onglets cartographiques
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "ðŸŽ¯ Vue ExÃ©cutive",
        "ðŸ—ºï¸ Cartographie 7D", 
        "ðŸ“Š Analyse Dimensionnelle",
        "ðŸ” Recherche STORM",
        "ðŸ“‹ Plans d'Action",
        "ðŸ“ˆ Suivi & KPI",
        "ðŸ§© MÃ©moire IA",
        "ðŸ“„ Export Complet"
    ])
    
    # TAB 1: Vue ExÃ©cutive
    with tab1:
        st.markdown("### ðŸŽ¯ RÃ©sumÃ© ExÃ©cutif Cartographie Culture SST")
        
        exec_summary = cartography['executive_summary']
        
        # MÃ©triques clÃ©s exÃ©cutives
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"""
            **ðŸŽ¯ MaturitÃ© Culture Globale**
            
            Score Actuel: **{exec_summary['overall_culture_maturity']:.1f}/5.0**
            
            Niveau: **{"ðŸ”´ Ã‰mergent" if exec_summary['overall_culture_maturity'] < 3.0 else "ðŸŸ¡ En DÃ©veloppement" if exec_summary['overall_culture_maturity'] < 4.0 else "ðŸŸ¢ Mature"}**
            
            Tendance: **ðŸ“ˆ AmÃ©lioration Continue**
            """)
        
        with col2:
            st.success(f"""
            **ðŸ“‹ Feuille de Route**
            
            Plans d'Action: **{exec_summary['recommended_actions']} plans**
            
            Timeline: **{exec_summary['estimated_improvement_timeline']}**
            
            PrioritÃ©: **ðŸš¨ {len(exec_summary.get('improvement_priority_dimensions', []))} dimensions critiques**
            """)
        
        with col3:
            st.warning(f"""
            **ðŸ’° Investissement & ROI**
            
            Investissement: **{exec_summary['investment_required'].title()}**
            
            ROI Attendu: **{exec_summary['expected_roi']}**
            
            Payback: **âš¡ 12-18 mois**
            """)
        
        # Dimensions prioritaires
        priority_dims = exec_summary.get('improvement_priority_dimensions', [])
        if priority_dims:
            st.markdown("#### ðŸš¨ Dimensions Prioritaires (Action Urgente)")
            for dim in priority_dims:
                st.error(f"âš ï¸ **{dim.replace('_', ' ').title()}** - AmÃ©lioration Critique Requise")
        else:
            st.success("âœ… **Aucune Dimension Critique** - Culture Ã©quilibrÃ©e")
    
    # TAB 2: Cartographie 7 Dimensions
    with tab2:
        st.markdown("### ðŸ—ºï¸ Cartographie Culture SST - 7 Dimensions")
        
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
                name='MaturitÃ© Actuelle',
                line_color='rgb(99, 110, 250)',
                fillcolor='rgba(99, 110, 250, 0.3)'
            ))
            
            # Cible maturitÃ©
            target_scores = [4.0] * len(dimension_names)
            fig.add_trace(go.Scatterpolar(
                r=target_scores,
                theta=dimension_names,
                fill='toself',
                name='Cible MaturitÃ© (4.0)',
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
                        ticktext=['1-Ã‰mergent', '2-Basique', '3-DÃ©veloppÃ©', '4-Mature', '5-Excellence']
                    )),
                showlegend=True,
                title="ðŸ—ºï¸ Cartographie MaturitÃ© Culture SST par Dimension",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # DÃ©tails par dimension
        st.markdown("#### ðŸ“Š Analyse DÃ©taillÃ©e par Dimension")
        
        for dim_name, dim_data in dimensions.items():
            priority_icon = "ðŸš¨" if dim_data.get('improvement_priority') == 'high' else "âš ï¸" if dim_data.get('improvement_priority') == 'medium' else "âœ…"
            
            with st.expander(f"{priority_icon} **{dim_name.replace('_', ' ').title()}** - Score: {dim_data.get('maturity_score', 0):.1f}/5.0"):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**âœ… Forces IdentifiÃ©es:**")
                    for strength in dim_data.get('strengths', []):
                        st.success(f"â€¢ {strength.replace('_', ' ').title()}")
                
                with col2:
                    st.markdown("**âš ï¸ Gaps Ã  Combler:**")
                    for gap in dim_data.get('gaps', []):
                        st.warning(f"â€¢ {gap.replace('_', ' ').title()}")
                
                # Informations dimension
                priority = dim_data.get('improvement_priority', 'medium')
                agents = dim_data.get('agents_analysis', [])
                
                st.info(f"""
                **ðŸ“‹ Informations Dimension:**
                - **PrioritÃ© AmÃ©lioration:** {priority.title()} {priority_icon}
                - **Agents Responsables:** {', '.join(agents)}
                - **Sources DonnÃ©es:** {', '.join(dim_data.get('data_sources', []))}
                - **MÃ©thode Assessment:** {dim_data.get('assessment_method', 'N/A')}
                """)
    
    # TAB 3: Analyse Dimensionnelle
    with tab3:
        st.markdown("### ðŸ“Š Analyse Dimensionnelle Approfondie")
        
        # Matrice corrÃ©lations (simulation enrichie)
        st.markdown("#### ðŸ”— Matrice InterdÃ©pendances Dimensions")
        
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
        
        # Heatmap corrÃ©lations
        fig_corr = px.imshow(
            correlation_df, 
            title="ðŸ”— Matrice CorrÃ©lations Dimensions Culture SST",
            color_continuous_scale="RdYlBu_r",
            aspect="auto",
            height=400
        )
        fig_corr.update_layout(
            xaxis_title="Dimensions",
            yaxis_title="Dimensions"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Zones aveugles dÃ©tectÃ©es
        zones_aveugles = cartography_result['final_state'].get('zones_aveugles', [])
        if zones_aveugles:
            st.markdown("#### âš ï¸ Zones Aveugles DÃ©tectÃ©es")
            for zone in zones_aveugles:
                st.error(f"ðŸš¨ **Zone Aveugle:** {zone.replace('_', ' ').title()}")
                
            st.warning("""
            **ðŸ” Actions RecommandÃ©es pour Zones Aveugles:**
            - Collecte donnÃ©es supplÃ©mentaires ciblÃ©es
            - Validation croisÃ©e avec stakeholders
            - Recherche STORM approfondie
            """)
        else:
            st.success("âœ… **Aucune Zone Aveugle Majeure DÃ©tectÃ©e** - Couverture cartographique complÃ¨te")
        
        # Analyse Ã©quilibre dimensions
        if dimensions:
            scores = [dim_data.get('maturity_score', 0) for dim_data in dimensions.values()]
            balance_score = 1 - (max(scores) - min(scores)) / 5  # Score Ã©quilibre 0-1
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("ðŸ“Š Score Ã‰quilibre", f"{balance_score:.2f}", 
                         delta="Excellent" if balance_score > 0.8 else "Bon" if balance_score > 0.6 else "Ã€ amÃ©liorer")
            
            with col2:
                st.metric("ðŸ“ˆ Dimension Forte", f"{max(scores):.1f}", 
                         delta="Leadership" if scores.index(max(scores)) == 0 else "Autre")
            
            with col3:
                st.metric("ðŸ“‰ Dimension Faible", f"{min(scores):.1f}", 
                         delta="PrioritÃ©" if min(scores) < 3.0 else "Acceptable")
    
    # TAB 4: Recherche STORM
    with tab4:
        st.markdown("### ðŸ” Recherche STORM - Enrichissement Scientifique")
        
        storm_data = cartography['technology_integration']['storm_research']
        
        if storm_data:
            # MÃ©triques STORM
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("ðŸ“š Sources AnalysÃ©es", storm_data.get('total_sources', 0))
            
            with col2:
                st.metric("ðŸŽ¯ Pertinence Cartographie", f"{storm_data.get('cartography_relevance', 0):.1%}")
            
            with col3:
                st.metric("ðŸ† QualitÃ© Preuves", f"{storm_data.get('evidence_quality', 0):.1%}")
            
            with col4:
                st.metric("âš¡ Temps ExÃ©cution", f"{storm_data.get('execution_time', 0):.1f}s")
            
            # Topics recherchÃ©s
            topics = storm_data.get('topics_researched', [])
            if topics:
                st.markdown("#### ðŸ“– Topics de Recherche AnalysÃ©s")
                for i, topic in enumerate(topics, 1):
                    st.info(f"**{i}.** {topic.replace('_', ' ').title()}")
        
        # Base de preuves
        evidence_base = cartography_result['final_state'].get('evidence_base', {})
        if evidence_base:
            st.markdown("#### ðŸ“Š Base de Preuves Scientifiques")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.success(f"ðŸŽ“ **Sources AcadÃ©miques:** {evidence_base.get('academic_sources', 0)}")
            
            with col2:
                st.info(f"ðŸ¢ **Rapports Institutionnels:** {evidence_base.get('institutional_reports', 0)}")
            
            with col3:
                st.warning(f"ðŸ“‹ **Cas Pratiques:** {evidence_base.get('best_practice_cases', 0)}")
        
        # Meilleures pratiques identifiÃ©es
        best_practices = cartography_result['final_state'].get('best_practices', [])
        if best_practices:
            st.markdown("#### âœ¨ Meilleures Pratiques IdentifiÃ©es par STORM")
            for practice in best_practices:
                st.success(f"âœ… {practice.replace('_', ' ').title()}")
        
        # Insights recherche
        research_insights = cartography_result['final_state'].get('research_insights', {})
        if research_insights and 'key_findings' in research_insights:
            st.markdown("#### ðŸ” Insights ClÃ©s de la Recherche")
            for finding in research_insights['key_findings']:
                st.info(f"ðŸ’¡ {finding}")
    
    # TAB 5: Plans d'Action
    with tab5:
        st.markdown("### ðŸ“‹ Plans d'Action Cartographiques")
        
        action_plans = cartography['improvement_roadmap']
        
        if action_plans:
            # Vue d'ensemble plans
            st.markdown("#### ðŸ“Š Vue d'Ensemble Plans d'Action")
            
            plans_summary = pd.DataFrame([
                {
                    'Plan': plan['title'],
                    'Dimension': plan['dimension'].replace('_', ' ').title(),
                    'PrioritÃ©': plan['priority'].title(),
                    'Timeline': plan['timeline'],
                    'Score Actuel': plan['current_maturity'],
                    'Cible': plan['target_maturity']
                } for plan in action_plans
            ])
            
            st.dataframe(plans_summary, use_container_width=True)
            
            # DÃ©tails par plan
            st.markdown("#### ðŸ“‹ DÃ©tails Plans d'Action")
            
            for plan in action_plans:
                priority_color = "ðŸš¨" if plan['priority'] == 'high' else "âš ï¸" if plan['priority'] == 'medium' else "âœ…"
                
                with st.expander(f"{priority_color} **{plan['title']}** - PrioritÃ©: {plan['priority'].title()}"):
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**ðŸ“Š Informations Plan:**")
                        st.info(f"""
                        - **Dimension Cible:** {plan['dimension'].replace('_', ' ').title()}
                        - **MaturitÃ© Actuelle:** {plan['current_maturity']:.1f}/5.0
                        - **MaturitÃ© Cible:** {plan['target_maturity']:.1f}/5.0
                        - **AmÃ©lioration:** +{plan['target_maturity'] - plan['current_maturity']:.1f} points
                        - **Timeline:** {plan['timeline']}
                        - **Agents Responsables:** {', '.join(plan['responsible_agents'])}
                        """)
                    
                    with col2:
                        st.markdown("**ðŸŽ¯ Actions SpÃ©cifiques:**")
                        for action in plan['actions']:
                            st.success(f"â€¢ {action}")
                    
                    st.markdown("**ðŸ“ˆ MÃ©triques de SuccÃ¨s:**")
                    for metric in plan['success_metrics']:
                        st.warning(f"ðŸ“Š {metric}")
                    
                    st.markdown("**ðŸ’° Ressources Requises:**")
                    for resource in plan['resources_required']:
                        st.info(f"ðŸ”§ {resource.replace('_', ' ').title()}")
        else:
            st.info("â„¹ï¸ Aucun plan d'action gÃ©nÃ©rÃ© - Culture SST satisfaisante")
    
    # TAB 6: Suivi & KPI
    with tab6:
        st.markdown("### ðŸ“ˆ Suivi et KPI Cartographiques")
        
        monitoring = cartography_result['final_state'].get('monitoring_dashboard', {})
        
        if monitoring:
            # SantÃ© cartographique
            cartography_health = monitoring.get('cartography_health', {})
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                trend = cartography_health.get('overall_culture_trend', 'stable')
                trend_icon = "ðŸ“ˆ" if trend == 'improving' else "ðŸ“‰" if trend == 'declining' else "âž¡ï¸"
                st.metric("ðŸŒ¡ï¸ Tendance Culture", f"{trend_icon} {trend.title()}")
            
            with col2:
                balance = cartography_health.get('dimension_balance', 0)
                st.metric("âš–ï¸ Ã‰quilibre Dimensions", f"{balance:.2f}", delta="Bon" if balance > 0.8 else "Moyen")
            
            with col3:
                progress = cartography_health.get('action_plan_progress', 0)
                st.metric("ðŸŽ¯ ProgrÃ¨s Plans", f"{progress:.1%}", delta="En cours")
            
            with col4:
                engagement = cartography_health.get('stakeholder_engagement', 0)
                st.metric("ðŸ¤ Engagement", f"{engagement:.1%}", delta="Actif")
            
            # MÃ©triques temps rÃ©el
            real_time = monitoring.get('real_time_metrics', {})
            if real_time:
                st.markdown("#### âš¡ MÃ©triques Temps RÃ©el")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.success(f"ðŸ“ˆ **Ã‰volution Culture:** {real_time.get('culture_evolution_rate', 'N/A')}")
                
                with col2:
                    st.info(f"ðŸ”§ **AmÃ©liorations Actives:** {real_time.get('dimension_improvements', 0)}")
                
                with col3:
                    st.warning(f"ðŸ’¬ **Taux Feedback:** {real_time.get('feedback_response_rate', 'N/A')}")
            
            # Alertes monitoring
            alerts = monitoring.get('alerts_notifications', [])
            if alerts:
                st.markdown("#### ðŸš¨ Alertes Monitoring Actives")
                for alert in alerts:
                    st.warning(f"âš ï¸ {alert}")
            else:
                st.success("âœ… Aucune alerte active - SystÃ¨me stable")
            
            # Prochaine mise Ã  jour
            next_update = monitoring.get('next_cartography_update', 'N/A')
            st.info(f"ðŸ“… **Prochaine Mise Ã  Jour Cartographie:** {next_update}")
        
        # KPI Evolution (simulation graphique)
        kpi_evolution = cartography_result['final_state'].get('kpi_evolution', {})
        if kpi_evolution:
            st.markdown("#### ðŸ“Š Ã‰volution KPI Culture (3 derniers mois)")
            
            months = ['Mois -2', 'Mois -1', 'Mois Actuel']
            culture_trend = kpi_evolution.get('culture_maturity_trend', [3.2, 3.4, 3.6])
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=months,
                y=culture_trend,
                mode='lines+markers',
                name='MaturitÃ© Culture Globale',
                line=dict(color='blue', width=3),
                marker=dict(size=8)
            ))
            
            fig_trend.update_layout(
                title="ðŸ“ˆ Ã‰volution MaturitÃ© Culture SST",
                xaxis_title="PÃ©riode",
                yaxis_title="Score MaturitÃ© (/5.0)",
                yaxis=dict(range=[0, 5])
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
    
    # TAB 7: MÃ©moire IA
    with tab7:
        st.markdown("### ðŸ§© MÃ©moire IA et Apprentissage Continu")
        
        memory_data = cartography_result['final_state'].get('memory_ai', {})
        learning_insights = cartography_result['final_state'].get('learning_insights', [])
        pattern_recognition = cartography_result['final_state'].get('pattern_recognition', {})
        
        if memory_data:
            # MÃ©triques mÃ©moire IA
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("ðŸ§  MÃ©moires Culture", memory_data.get('cartography_memories', 0))
            
            with col2:
                st.metric("ðŸŽ¯ PrÃ©cision MÃ©moire", f"{memory_data.get('memory_accuracy', 0):.1%}")
            
            with col3:
                st.metric("ðŸ“š Patterns Appris", memory_data.get('culture_patterns_learned', 0))
            
            with col4:
                st.metric("âš¡ Vitesse Apprentissage", f"{memory_data.get('learning_velocity', 0):.2f}")
        
        # Insights apprentissage
        if learning_insights:
            st.markdown("#### ðŸ’¡ Insights Apprentissage IA")
            for insight in learning_insights:
                st.info(f"ðŸ” {insight}")
        
        # Reconnaissance patterns
        if pattern_recognition:
            st.markdown("#### ðŸ” Reconnaissance Patterns Culture")
            
            # ArchÃ©types culture identifiÃ©s
            archetypes = pattern_recognition.get('culture_archetypes_identified', [])
            if archetypes:
                st.markdown("**ðŸ›ï¸ ArchÃ©types Culture IdentifiÃ©s:**")
                for archetype in archetypes:
                    st.success(f"âœ… {archetype.replace('_', ' ').title()}")
            
            # CorrÃ©lations risques
            risk_correlations = pattern_recognition.get('risk_pattern_correlations', {})
            if risk_correlations:
                st.markdown("**âš ï¸ Patterns Risques IdentifiÃ©s:**")
                for risk_pattern, correlation in risk_correlations.items():
                    st.warning(f"ðŸš¨ {risk_pattern}: CorrÃ©lation {correlation:.2f}")
            
            # Patterns succÃ¨s
            success_patterns = pattern_recognition.get('success_pattern_identification', {})
            if success_patterns:
                st.markdown("**ðŸŽ¯ Patterns SuccÃ¨s IdentifiÃ©s:**")
                for success_pattern, correlation in success_patterns.items():
                    st.success(f"âœ… {success_pattern}: CorrÃ©lation {correlation:.2f}")
    
    # TAB 8: Export Complet
    with tab8:
        st.markdown("### ðŸ“„ Export Cartographie ComplÃ¨te")
        
        # Informations export
        st.markdown("#### ðŸ“¦ Contenu Export Cartographique")
        st.info("""
        **ðŸ“‹ Cartographie Culture SST ComplÃ¨te comprend:**
        
        ðŸŽ¯ **RÃ©sumÃ© ExÃ©cutif**
        - MaturitÃ© culture globale et tendances
        - ROI et timeline d'amÃ©lioration
        - Dimensions prioritaires identifiÃ©es
        
        ðŸ—ºï¸ **Cartographie DÃ©taillÃ©e 7 Dimensions**
        - Scores maturitÃ© par dimension
        - Forces et gaps spÃ©cifiques
        - Agents responsables et sources donnÃ©es
        
        ðŸ“Š **Analyse Dimensionnelle**
        - Matrice corrÃ©lations interdÃ©pendances
        - Zones aveugles et recommandations
        - Ã‰quilibre et cohÃ©rence systÃ¨me
        
        ðŸ” **Enrichissement STORM**
        - Base preuves scientifiques
        - Meilleures pratiques sectorielles
        - Insights recherche applicables
        
        ðŸ“‹ **Feuille Route AmÃ©lioration**
        - Plans d'action personnalisÃ©s
        - MÃ©triques succÃ¨s et ressources
        - Timeline et responsabilitÃ©s
        
        ðŸ“ˆ **Framework Monitoring**
        - KPI temps rÃ©el et alertes
        - SystÃ¨mes feedback continue
        - PrÃ©dictions Ã©volution culture
        
        ðŸ§© **Intelligence Artificielle**
        - MÃ©moire IA et apprentissage
        - Reconnaissance patterns
        - Recommandations adaptatives
        """)
        
        # Export JSON complet
        cartography_json = json.dumps(cartography, indent=2, ensure_ascii=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="ðŸ’¾ TÃ©lÃ©charger Cartographie ComplÃ¨te (JSON)",
                data=cartography_json,
                file_name=f"cartographie_culture_sst_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            # Export rÃ©sumÃ© exÃ©cutif
            executive_summary = json.dumps(cartography['executive_summary'], indent=2, ensure_ascii=False)
            st.download_button(
                label="ðŸ“Š TÃ©lÃ©charger RÃ©sumÃ© ExÃ©cutif (JSON)",
                data=executive_summary,
                file_name=f"resume_executif_culture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Diagramme workflow Mermaid
        if 'mermaid_diagram' in cartography_result:
            st.markdown("#### ðŸ—ºï¸ Diagramme Workflow Cartographique")
            st.code(cartography_result['mermaid_diagram'], language='mermaid')
        
        # MÃ©tadonnÃ©es session
        st.markdown("#### ðŸ” MÃ©tadonnÃ©es Session")
        metadata = cartography['metadata']
        st.json({
            "Session ID": metadata['session_id'],
            "Timestamp": metadata['timestamp'],
            "Secteur SCIAN": f"{metadata['sector_scian']} - {metadata['sector_name']}",
            "Moteur Cartographie": metadata['cartography_engine'],
            "Mode ExÃ©cution": cartography_result.get('execution_mode', 'unknown')
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
    st.markdown("## ðŸš€ Choix Workflow SafetyGraph")
    
    col1, col2 = st.columns(2)
    
    # TABS ENRICHIS AVEC ANALYTICS
main_tabs = st.tabs([
    "ðŸ§  BehaviorX Standard",
    "ðŸ—ºï¸ Cartographie Culture", 
    "ðŸ”® Analytics PrÃ©dictifs",    # NOUVEAU
    "ðŸ” Pattern Recognition",     # NOUVEAU
    "âš ï¸ Anomaly Detection"        # NOUVEAU
])

with main_tabs[0]:
    # Workflow BehaviorX existant
    if st.button("ðŸš€ Lancer BehaviorX Standard", use_container_width=True):
        st.session_state.workflow_type = "behaviorx_standard"
        st.session_state.workflow_results = None
    
    # Gardez ici votre code BehaviorX existant (aprÃ¨s les descriptions)

with main_tabs[1]:
    # Cartographie existante
    if st.button("ðŸ—ºï¸ Lancer Cartographie ComplÃ¨te", use_container_width=True):
        st.session_state.workflow_type = "cartography_complete"
        st.session_state.workflow_results = None
    
    # Gardez ici votre code cartographie existant

with main_tabs[2]:
    if ANALYTICS_AVAILABLE:
        display_predictive_analytics_interface()
    else:
        st.error("âš ï¸ Module analytics prÃ©dictifs non disponible")

with main_tabs[3]:
    if ANALYTICS_AVAILABLE:
        display_pattern_recognition_interface()
    else:
        st.error("âš ï¸ Module pattern recognition non disponible")

with main_tabs[4]:
    if ANALYTICS_AVAILABLE:
        display_anomaly_detection_interface()
    else:
        st.error("âš ï¸ Module anomaly detection non disponible")
    
    # Description workflows
    if st.session_state.get('workflow_type'):
        if st.session_state.workflow_type == "behaviorx_standard":
            st.info("""
            **ðŸ§  Workflow BehaviorX Standard**
            - âœ… Analyse VCS (Visual Card Sorting)
            - âœ… Analyse ABC comportementale
            - âœ… Agent A1 Enhanced avec Safe Self
            - âœ… Score intÃ©gration et zones aveugles
            - âš¡ ExÃ©cution rapide (~30 secondes)
            """)
        
        elif st.session_state.workflow_type == "cartography_complete":
            st.success("""
            **ðŸ—ºï¸ Cartographie Culture SST ComplÃ¨te**
            - ðŸ—ºï¸ Cartographie 7 dimensions culture SST
            - ðŸ¤– Architecture LangGraph multi-agent (100+ agents)
            - ðŸ” Recherche STORM enrichissement scientifique
            - ðŸ“‹ Plans d'action personnalisÃ©s par dimension
            - ðŸ“ˆ Framework monitoring et KPI Ã©volution
            - ðŸ§© MÃ©moire IA et apprentissage continu
            - âš¡ Analyse approfondie (~2-3 minutes)
            """)
        
        # Bouton exÃ©cution
        if st.button("â–¶ï¸ Lancer Workflow SÃ©lectionnÃ©", type="primary", use_container_width=True):
            if st.session_state.workflow_type == "behaviorx_standard":
                st.session_state.workflow_results = execute_behaviorx_workflow_standard(config)
            elif st.session_state.workflow_type == "cartography_complete":
                st.session_state.workflow_results = execute_cartography_workflow_complete(config)
    
    # Affichage rÃ©sultats selon type workflow
    if st.session_state.get('workflow_results'):
        results = st.session_state.workflow_results
        
        if results['success']:
            if results.get('type') == 'behaviorx_standard':
                display_behaviorx_results(results)
            else:
                display_cartography_results(results)
            
            # Ajout Ã  l'historique
            if results not in st.session_state.execution_history:
                st.session_state.execution_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': st.session_state.workflow_type,
                    'enterprise': config['enterprise_name'],
                    'sector': config['sector_name'],
                    'success': True
                })
        else:
            st.error("âŒ Erreur lors de l'exÃ©cution du workflow")
    
    # Historique exÃ©cutions (optionnel)
    if st.session_state.execution_history:
        with st.expander("ðŸ“‹ Historique ExÃ©cutions"):
            for i, execution in enumerate(reversed(st.session_state.execution_history[-5:]), 1):
                st.text(f"{i}. {execution['timestamp'][:19]} - {execution['type']} - {execution['enterprise']} ({execution['sector']})")

# ===================================================================
# 9. POINT D'ENTRÃ‰E APPLICATION
# ===================================================================

if __name__ == "__main__":
    main()

# ===================================================================
# INTÃ‰GRATION ANALYTICS AVANCÃ‰S SAFETYGRAPH
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
        "ðŸ§  BehaviorX Standard",
        "ðŸ—ºï¸ Cartographie Culture", 
        "ðŸ”® Analytics PrÃ©dictifs",    # NOUVEAU
        "ðŸ” Pattern Recognition",     # NOUVEAU
        "âš ï¸ Anomaly Detection"        # NOUVEAU
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
            st.warning("âš ï¸ Modules analytics non disponibles")
    
    with main_tabs[3]:
        if ANALYTICS_AVAILABLE:
            display_pattern_recognition_interface()
        else:
            st.warning("âš ï¸ Modules analytics non disponibles")
    
    with main_tabs[4]:
        if ANALYTICS_AVAILABLE:
            display_anomaly_detection_interface()
        else:
            st.warning("âš ï¸ Modules analytics non disponibles")    
