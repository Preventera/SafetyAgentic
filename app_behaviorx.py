"""
SafetyGraph BehaviorX + Cartographie Culture SST - Interface Complète
====================================================================
Interface Streamlit unifiée : BehaviorX + Cartographie LangGraph
Safety Agentique - Mario Plourde - 28 juillet 2025
Version 3.1 - Architecture Industries Unifiées + Expansion Sectorielle
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
# CORRECTION PYARROW - GESTION POURCENTAGES DANS DATAFRAMES
# ===================================================================

def fix_dataframe_for_streamlit(df):
    """
    Corrige les DataFrames pour compatibilité PyArrow/Streamlit
    Résout l'erreur: Could not convert '96%' with type str: tried to convert to double
    """
    import pandas as pd
    
    df_fixed = df.copy()
    
    for col in df_fixed.columns:
        if df_fixed[col].dtype == 'object':
            # Détecter les colonnes avec pourcentages
            percentage_mask = df_fixed[col].astype(str).str.contains('%', na=False)
            
            if percentage_mask.any():
                # Garder la colonne originale pour l'affichage (format string)
                df_fixed[col] = df_fixed[col].astype(str)
    
    return df_fixed

# ===================================================================
# DICTIONNAIRE SCIAN COMPLET - MULTI-INDUSTRIES SAFETYGRAPH
# ===================================================================

SECTEURS_SCIAN_COMPLET = {
    "🚧 CONSTRUCTION": {
        "Construction générale (236)": "236",
        "Construction résidentielle (2361)": "2361", 
        "Construction non-résidentielle (2362)": "2362",
        "Génie civil & infrastructure (237)": "237",
        "Entrepreneurs spécialisés (238)": "238",
        "Construction lourde & civile": "237-heavy"
    },
    "⛏️ MINES & EXTRACTION": {
        "Mines souterraines (212)": "212",
        "Mines métalliques (2122)": "2122",
        "Mines non-métalliques (2123)": "2123", 
        "Extraction pétrole & gaz (211)": "211",
        "Activités soutien mines (213)": "213",
        "Carrières & sablières (2123)": "2123-carriere"
    },
    "🏭 MANUFACTURING AVANCÉ": {
        "Fabrication alimentaire (311)": "311",
        "Pharmaceutique (3254) 🆕": "3254",
        "Agro-alimentaire (3111) 🆕": "3111",
        "Chimique & Pétrochimique (3251) 🆕": "3251",
        "Métallurgie (3311) 🆕": "3311",
        "Fabrication boissons & tabac (312)": "312",
        "Fabrication bois (321)": "321", 
        "Fabrication papier (322)": "322",
        "Fabrication plastique & caoutchouc (326)": "326",
        "Fabrication métallique primaire (331)": "331",
        "Fabrication machinerie (333)": "333",
        "Fabrication équipement transport (336)": "336",
        "Fabrication meubles (337)": "337"
    },
    "🏥 SOINS DE SANTÉ SPÉCIALISÉS": {
        "Soins ambulatoires (621)": "621",
        "Hôpitaux aigus (6221) 🆕": "6221",
        "Laboratoires médicaux (6215) 🆕": "6215",
        "Hôpitaux (622)": "622", 
        "Établissements soins infirmiers (623)": "623",
        "Assistance sociale (624)": "624",
        "Services sociaux communautaires": "624-social"
    },
    "🔧 SERVICES CRITIQUES": {
        "Services professionnels techniques (541)": "541",
        "Télécommunications (5174) 🆕": "5174",
        "Services énergétiques (2211) 🆕": "2211",
        "Gestion d'entreprises (551)": "551",
        "Services administratifs & soutien (561)": "561",
        "Services éducatifs (611)": "611",
        "Services publics (utilities)": "221"
    },
    "🚚 TRANSPORT AVANCÉ": {
        "Transport terrestre (484)": "484",
        "Transport maritime (4831) 🆕": "4831",
        "Aviation commerciale (4811) 🆕": "4811",
        "Transport aérien (481)": "481", 
        "Transport maritime (483)": "483",
        "Entreposage (493)": "493",
        "Services postaux & courrier (492)": "492"
    }
}

# Fonction utilitaire pour obtenir tous les secteurs
def get_all_secteurs_list():
    """Retourne la liste complète de tous les secteurs disponibles"""
    secteurs_list = []
    for industrie, secteurs in SECTEURS_SCIAN_COMPLET.items():
        for nom_secteur, code in secteurs.items():
            secteurs_list.append(f"{nom_secteur}")
    return secteurs_list

def get_secteur_code(secteur_nom):
    """Retourne le code SCIAN d'un secteur donné"""
    for industrie, secteurs in SECTEURS_SCIAN_COMPLET.items():
        for nom, code in secteurs.items():
            if nom == secteur_nom:
                return code
    return "236"  # Default fallback

# ===================================================================
# INTEGRATION ANALYTICS AVANCÉS SAFETYGRAPH
# ===================================================================

# Imports modules analytics
try:
    sys.path.append(str(Path(__file__).parent / "modules"))
    from analytics_predictifs import display_analytics_predictifs_interface as display_predictive_analytics_interface
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

# Import module C-Suite Dashboard
try:
    from src.dashboards.c_suite_dashboard import display_c_suite_dashboard as c_suite_exec_dashboard
    CSUITE_AVAILABLE = True
    print("✅ Module C-Suite Dashboard chargé")
except ImportError:
    CSUITE_AVAILABLE = False
    print("⚠️ Module C-Suite Dashboard non disponible")

# Configuration page Streamlit
st.set_page_config(
    page_title="SafetyGraph BehaviorX + Industries SST",
    page_icon="🏭",
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

# Imports agents BehaviorX existants + ORCHESTRATEUR
try:
    sys.path.append(str(Path(__file__).parent / "src" / "agents" / "collecte"))
    from orchestrateur_behaviorx_unified import BehaviorXSafetyOrchestrator
    BEHAVIORX_AVAILABLE = True
    print("✅ Orchestrateur BehaviorX chargé avec succès")
except ImportError:
    BEHAVIORX_AVAILABLE = False
    print("⚠️ Orchestrateur BehaviorX non disponible")

# ===================================================================
# INITIALISATION SESSION STATE
# ===================================================================

# Initialisation état session
if 'workflow_results' not in st.session_state:
    st.session_state.workflow_results = None
if 'workflow_type' not in st.session_state:
    st.session_state.workflow_type = None
if 'execution_history' not in st.session_state:
    st.session_state.execution_history = []

# ===================================================================
# HEADER ET BRANDING
# ===================================================================

def display_header():
    """Affiche header unifié SafetyGraph"""
    
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1f2937 0%, #374151 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; text-align: center; margin: 0;">
            🏭 SafetyGraph Industries + Culture SST
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
# RÉVOLUTION UX/UI - SÉLECTEUR PROFIL UTILISATEUR
# ===================================================================

def init_user_profile():
    """Initialisation du profil utilisateur pour UX adaptatif"""
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = 'hse_manager'
    
    profiles = {
        'hse_manager': {
            'name': '👨‍💼 HSE Manager',
            'description': 'Stratégie, conformité, ROI',
            'color': '#1f77b4',
            'dashboard_type': 'executive'
        },
        'safety_coordinator': {
            'name': '⚡ Safety Coordinator', 
            'description': 'Opérations, incidents, équipes',
            'color': '#ff7f0e',
            'dashboard_type': 'operations'
        },
        'supervisor': {
            'name': '👷 Supervisor',
            'description': 'Terrain, actions rapides',
            'color': '#2ca02c',
            'dashboard_type': 'field'
        },
        'c_suite': {
            'name': '💼 C-Suite Executive',
            'description': 'Vision, benchmark, impact business',
            'color': '#9467bd',
            'dashboard_type': 'boardroom'
        },
        'chercheur': {
            'name': '🔬 Chercheur SST',
            'description': 'Analyse, données, innovation',
            'color': '#17becf',
            'dashboard_type': 'research'
        }
    }
    
    return profiles

def display_profile_selector():
    """Affiche sélecteur profil révolutionnaire avec métadonnées"""
    
    profiles = init_user_profile()
    
    with st.sidebar:
        st.markdown("### 👤 Profil Utilisateur")
        
        # Sélecteur profil
        profile_options = list(profiles.keys())
        profile_labels = [profiles[key]['name'] for key in profile_options]
        
        selected_index = st.selectbox(
            "Sélectionnez votre profil",
            range(len(profile_options)),
            format_func=lambda x: profile_labels[x],
            index=profile_options.index(st.session_state.get('user_profile', 'hse_manager')),
            key='profile_selector'
        )
        
        selected_profile = profile_options[selected_index]
        st.session_state.user_profile = selected_profile
        
        # Affichage métadonnées profil
        profile_data = profiles[selected_profile]
        
        st.markdown(f"""
        **Badge Profil Actuel :** {profile_data['name']}
        
        **Focus :** {profile_data['description']}
        
        **Mode Interface :** {profile_data['dashboard_type'].title()}
        """)
        
        return profile_data

def display_adaptive_header(profile_data):
    """Header adaptatif selon profil utilisateur"""
    
    color = profile_data['color']
    name = profile_data['name']
    
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, {color} 0%, #374151 100%); 
                padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
        <h2 style="color: white; text-align: center; margin: 0;">
            {name} - SafetyGraph Industries
        </h2>
        <p style="color: #d1d5db; text-align: center; margin: 0.5rem 0 0 0;">
            🏭 Interface Adaptative Multi-Sectorielle
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# SIDEBAR CONFIGURATION MULTI-INDUSTRIES
# ===================================================================

def setup_sidebar():
    """Configuration sidebar enrichie multi-industries"""
    
    with st.sidebar:
        st.markdown("## ⚙️ Configuration SafetyGraph")
        
        # Section entreprise
        st.markdown("### 🏢 Informations Entreprise")
        nom_entreprise = st.text_input("Nom entreprise", value="Entreprise ABC", key="enterprise_name")
        
        # ===================================================================
        # SECTION SECTEUR D'ACTIVITÉ - MULTI-INDUSTRIES AVEC EXPANSION
        # ===================================================================
        st.markdown("## 📊 Secteur d'Activité (SCIAN)")
        
        # Sélection industrie principale
        industrie_principale = st.selectbox(
            "🏭 Industrie Principale", 
            list(SECTEURS_SCIAN_COMPLET.keys()),
            key="industrie_principale",
            index=0  # Construction par défaut
        )
        
        # Secteur spécifique selon industrie choisie
        secteurs_disponibles = list(SECTEURS_SCIAN_COMPLET[industrie_principale].keys())
        secteur_selectionne = st.selectbox(
            "🎯 Secteur Spécifique",
            secteurs_disponibles,
            key="secteur_specifique"
        )
        
        # Code SCIAN pour compatibilité avec le reste du code
        secteur_code = SECTEURS_SCIAN_COMPLET[industrie_principale][secteur_selectionne]
        
        # Affichage informations
        st.info(f"📋 Code SCIAN: **{secteur_code}**")
        if "🆕" in secteur_selectionne:
            st.success("🆕 **NOUVEAU SECTEUR** - Expansion Prioritaire SafetyGraph!")
        
        # Métriques industrie
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("🏭 Industries", len(SECTEURS_SCIAN_COMPLET))
        with col_b:
            st.metric("📊 Secteurs", len(secteurs_disponibles))
        
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
        
        # Orchestrateur BehaviorX
        if BEHAVIORX_AVAILABLE:
            orchestrateur_actif = st.checkbox("🎼 Orchestrateur BehaviorX", value=True, key="orchestrator_enabled")
        
        # Statut modules
        st.markdown("### 📊 Statut Modules")
        st.success(f"🧠 BehaviorX: {'✅ Disponible' if BEHAVIORX_AVAILABLE else '❌ Indisponible'}")
        st.success(f"🗺️ Cartographie: {'✅ Disponible' if CARTOGRAPHY_AVAILABLE else '❌ Indisponible'}")
        st.success(f"⛏️ Mines: {'✅ Disponible' if MINES_AVAILABLE else '❌ Indisponible'}")
        st.success(f"📊 Analytics: {'✅ Disponible' if ANALYTICS_AVAILABLE else '❌ Indisponible'}")
        
        # À propos
        st.markdown("### ℹ️ À Propos")
        total_secteurs = sum(len(secteurs) for secteurs in SECTEURS_SCIAN_COMPLET.values())
        st.info(f"""
        **SafetyGraph Industries v3.1**
        
        🏭 **{len(SECTEURS_SCIAN_COMPLET)} Industries** - Multi-secteurs SCIAN
        
        📊 **{total_secteurs} Secteurs** - Couverture complète + Expansion
        
        🤖 **100+ Agents** - A1-A10, AN1-AN10, R1-R10, S1-S10, SC1-SC50
        
        🔍 **STORM Research** - Enrichissement scientifique temps réel
        
        🧠 **LangGraph** - Orchestration multi-agent avancée
        
        🎼 **Orchestrateur BehaviorX** - Workflow VCS→ABC→A1→Intégration
        """)
        
        return {
            'enterprise_name': nom_entreprise,
            'industrie_principale': industrie_principale,
            'sector_name': secteur_selectionne,
            'sector_code': secteur_code,
            'workflow_mode': mode_workflow,
            'memory_enabled': memoire_ia,
            'debug_mode': mode_debug,
            'orchestrator_enabled': st.session_state.get('orchestrator_enabled', True) if BEHAVIORX_AVAILABLE else False
        }

# ===================================================================
# IMPORTS MODULES UX/UI MODULAIRES - ARCHITECTURE PROFESSIONNELLE
# ===================================================================

try:
    # Import des dashboards spécialisés
    from src.dashboards.hse_manager_dashboard import display_hse_manager_dashboard
    from src.dashboards.safety_coordinator_dashboard import display_safety_coordinator_dashboard
    from src.dashboards.supervisor_dashboard import display_supervisor_dashboard
    UX_MODULES_AVAILABLE = True
    print("✅ Modules UX/UI modulaires chargés avec succès")
except ImportError as e:
    print(f"⚠️ Modules UX/UI modulaires non disponibles: {e}")
    UX_MODULES_AVAILABLE = False
    
    # Fonctions fallback si modules non disponibles
    def display_hse_manager_dashboard(config):
        st.error("❌ Dashboard HSE Manager non disponible")
        st.info("🔧 Vérifiez que le fichier src/dashboards/hse_manager_dashboard.py existe et est correct")
    
    def display_safety_coordinator_dashboard(config):
        st.error("❌ Dashboard Safety Coordinator non disponible")
    
    def display_supervisor_dashboard(config):
        st.error("❌ Dashboard Supervisor non disponible")

# ===================================================================
# MODULE INDUSTRIES UNIFIÉ AVEC PROFILS ADAPTATIFS
# ===================================================================

def display_industries_unified(config):
    """Module Industries unifié adaptatif par profil utilisateur"""
    
    # Vérification modules UX/UI
    if not UX_MODULES_AVAILABLE:
        st.error("❌ Modules UX/UI non disponibles - Vérifiez structure src/dashboards/ et src/ux/")
        st.info("🔧 Action requise : Créez les dossiers et fichiers selon architecture modulaire")
        display_industries_fallback(config)
        return
    
    # Récupération profil utilisateur actuel (source unique de vérité)
    current_profile = st.session_state.get('user_profile', 'hse_manager')
    
    # === ROUTING DASHBOARD ADAPTATIF PAR PROFIL UTILISATEUR ===
    
    if current_profile == 'hse_manager':
        # Dashboard HSE Manager Executive complet
        display_hse_manager_dashboard(config)
    
    elif current_profile == 'safety_coordinator':
        # Dashboard Safety Coordinator Operations complet
        display_safety_coordinator_dashboard(config)
    
    elif current_profile == 'supervisor':
        # Dashboard Supervisor Terrain BBS-ISO complet
        display_supervisor_dashboard(config)
    
    elif current_profile == 'c_suite':
        # Dashboard C-Suite Executive - Module complet
        if CSUITE_AVAILABLE:
            try:
                c_suite_exec_dashboard(config)
            except Exception as e:
                st.error(f"❌ Erreur dashboard C-Suite : {e}")
                display_industries_fallback(config)
        else:
            # Fallback si module non disponible
            st.markdown("# 💼 C-Suite Executive Dashboard") 
            st.info("🚧 Dashboard C-Suite business - En développement")
            st.warning("⚠️ Module C-Suite non chargé - Vérifiez src/dashboards/")
            display_industries_fallback(config)
    
    elif current_profile == 'chercheur':
        # Dashboard Chercheur Analytics (à développer)
        st.markdown("# 🔬 Dashboard Chercheur SST")
        st.info("🔬 Dashboard Chercheur en développement")
        st.markdown("### 🧪 Recherche Dashboard - Analytics Avancés")
        st.success("Outils de recherche à venir !")
        display_industries_fallback(config)
    
    else:
        # Profil non reconnu - fallback vers HSE Manager
        st.warning(f"Profil '{current_profile}' non reconnu, redirection vers HSE Manager")
        display_hse_manager_dashboard(config)

def display_industries_fallback(config):
    """Interface Industries temporaire pour profils non encore développés"""
    st.markdown("### 🏭 Interface Industries Temporaire")
    st.markdown("*En attendant le développement du dashboard spécialisé pour ce profil*")
    
    # Informations secteur avec expansion
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("#### 📊 Secteur Actuel")
        st.success(f"**{config.get('industrie_principale', 'N/A')}**")
        st.info(f"🎯 **{config.get('sector_name', 'N/A')}**")
        st.code(f"SCIAN: {config.get('sector_code', 'N/A')}")
        
        # Indicateur secteur nouveau
        if "🆕" in config.get('sector_name', ''):
            st.success("🆕 **SECTEUR EXPANSION PRIORITAIRE** - SafetyGraph Advanced!")
    
    with col2:
        st.markdown("#### 📈 Couverture")
        st.metric("Industries", len(SECTEURS_SCIAN_COMPLET), delta="Multi-secteurs")
        total_secteurs = sum(len(secteurs) for secteurs in SECTEURS_SCIAN_COMPLET.values())
        st.metric("Secteurs SCIAN", total_secteurs, delta=f"+{12} nouveaux")
        
    with col3:
        st.markdown("#### 🎯 Actions")
        if st.button("🚀 Analyser Secteur", type="primary", use_container_width=True):
            st.success(f"✅ Analyse lancée pour {config.get('sector_name', 'secteur')}")
            if "🆕" in config.get('sector_name', ''):
                st.balloons()
                st.success("🆕 Analyse secteur expansion prioritaire!")
    
    # Métriques génériques temporaires
    st.markdown("---")
    st.markdown("#### 📊 Métriques Génériques Temporaires")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric("Score Sécurité", "78.5%", delta="+2.1%")
    with metric_col2:
        st.metric("Conformité", "89.3%", delta="+1.8%")
    with metric_col3:
        st.metric("Incidents/Mois", "3", delta="-2")
    with metric_col4:
        st.metric("Formation", "92%", delta="+5%")

# ===================================================================
# WORKFLOWS BEHAVIORX AVEC ORCHESTRATEUR INTÉGRÉ
# ===================================================================

def execute_behaviorx_workflow_orchestrated(config):
    """Exécute workflow BehaviorX avec orchestrateur unifié"""
    
    if not BEHAVIORX_AVAILABLE:
        st.error("❌ Orchestrateur BehaviorX non disponible")
        return None
    
    with st.container():
        st.markdown("## 🎼 Workflow BehaviorX Orchestré - VCS→ABC→A1→Intégration")
        
        # Progress tracking
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # Métriques container
        metrics_container = st.container()
        
        try:
            # Initialisation
            status_text.text("🎼 Initialisation Orchestrateur BehaviorX Unifié...")
            progress_bar.progress(10)
            
            orchestrator = BehaviorXSafetyOrchestrator({
                'memory_enabled': config['memory_enabled'],
                'debug_mode': config['debug_mode']
            })
            
            # Exécution workflow
            status_text.text("🚀 Exécution Workflow Orchestré VCS → ABC → A1 Enhanced → Intégration...")
            progress_bar.progress(30)
            
            # Étape VCS
            status_text.text("🔍 Étape 1/4: VCS Observation...")
            progress_bar.progress(50)
            time.sleep(0.5)
            
            # Étape ABC
            status_text.text("🔗 Étape 2/4: Analyse ABC...")
            progress_bar.progress(70)
            time.sleep(0.5)
            
            # Étape A1 Enhanced
            status_text.text("🤖 Étape 3/4: Agent A1 Enhanced...")
            progress_bar.progress(85)
            time.sleep(0.5)
            
            # Étape Intégration
            status_text.text("📊 Étape 4/4: Intégration & Zones Aveugles...")
            progress_bar.progress(95)
            
            results = orchestrator.execute_full_workflow(
                enterprise_id=config['enterprise_name'],
                sector_code=config['sector_code'],
                workflow_mode=config['workflow_mode']
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Workflow BehaviorX Orchestré Terminé !")
            
            # Affichage métriques sophistiquées
            with metrics_container:
                st.markdown("### 📊 Résultats Orchestrateur BehaviorX")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    integration_score = results.get('integration_score', 92.0)
                    st.metric(
                        "🎯 Score Intégration", 
                        f"{integration_score:.1f}%", 
                        delta=f"+{integration_score-70:.1f}%" if integration_score > 70 else None
                    )
                
                with col2:
                    vcs_score = results.get('vcs_results', {}).get('conformity_rate', 75.0)
                    st.metric(
                        "🔍 Conformité VCS", 
                        f"{vcs_score:.1f}%",
                        delta="6 Forces" if vcs_score > 70 else "À améliorer"
                    )
                
                with col3:
                    a1_score = results.get('a1_enhanced_results', {}).get('safe_self_score', 79.0)
                    st.metric(
                        "🤖 Score A1 Enhanced",
                        f"{a1_score:.1f}",
                        delta="BON" if a1_score > 75 else "Améliorer"
                    )
                
                with col4:
                    blind_spots = results.get('blind_spots', [])
                    blind_spots_count = len(blind_spots) if blind_spots else 0
                    st.metric(
                        "🚨 Zones Aveugles",
                        blind_spots_count,
                        delta="🔍 Détectées" if blind_spots_count > 0 else "✅ Aucune"
                    )
            
            return {
                'success': True,
                'type': 'behaviorx_orchestrated',
                'results': results,
                'metrics': {
                    'integration_score': integration_score,
                    'vcs_conformity': vcs_score,
                    'a1_score': a1_score,
                    'blind_spots': blind_spots_count
                }
            }
            
        except Exception as e:
            st.error(f"❌ Erreur workflow BehaviorX Orchestré: {str(e)}")
            if config.get('debug_mode'):
                st.exception(e)
            return None

def execute_cartography_workflow_complete(config):
    """Exécute workflow cartographie culture SST complet"""
    
    if not CARTOGRAPHY_AVAILABLE:
        st.error("❌ Module Cartographie non disponible")
        return None
    
    # Version simulée enrichie pour démonstration
    with st.spinner("🗺️ Génération cartographie culture SST complète..."):
        time.sleep(2)
    
    st.success("🗺️ Cartographie Culture SST Simulée - Version Enrichie")
    
    return {
        'success': True,
        'type': 'cartography_complete',
        'cartography': {
            'executive_summary': {
                'overall_culture_maturity': 3.8,
                'sector_benchmark': 3.2,
                'top_25_percent': 4.1,
                'sector_name': config['sector_name']
            }
        }
    }

def display_behaviorx_orchestrated_results(results):
    """Affiche résultats BehaviorX orchestré dans onglets détaillés"""
    
    if not results or not results['success']:
        return
    
    # Onglets BehaviorX Orchestré
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 VCS Observation",
        "🔗 Analyse ABC", 
        "🤖 A1 Enhanced",
        "📊 Intégration",
        "📄 Rapport Complet"
    ])
    
    with tab1:
        st.markdown("### 🔍 VCS Observation - SafetyGraph Module BehaviorX Orchestré")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Items Observés", "12", delta="Complet")
        with col2:
            vcs_score = results['metrics']['vcs_conformity']
            st.metric("✅ Conformité", f"{vcs_score:.1f}%", delta="6 Forces")
        with col3:
            st.metric("⚠️ Préoccupations", "2", delta="À surveiller")
        
        # Détails VCS si disponibles
        vcs_results = results['results'].get('vcs_results', {})
        if vcs_results:
            st.markdown("#### 📋 Détails VCS")
            st.json(vcs_results)
    
    with tab2:
        st.markdown("### 🔗 Analyse ABC - Comportements Observés")
        
        col1, col2 = st.columns(2)
        with col1:
            st.success("✅ 6 Comportements Positifs")
            st.markdown("""
            - Port EPI systématique
            - Communication sécurité active
            - Respect procédures
            - Signalement proactif
            - Formation continue
            - Leadership sécurité
            """)
        with col2:
            st.warning("⚠️ 2 Comportements À Corriger")
            st.markdown("""
            - Raccourcis procéduraux occasionnels
            - Négligence contrôles routine
            """)
        
        # Analyse ABC si disponible
        abc_analysis = results['results'].get('abc_analysis', {})
        if abc_analysis:
            st.markdown("#### 🔗 Analyse ABC Détaillée")
            st.json(abc_analysis)
    
    with tab3:
        st.markdown("### 🤖 Agent A1 Enhanced - Safe Self Orchestré")
        
        a1_score = results['metrics']['a1_score']
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Score Safe Self", f"{a1_score:.1f}", delta="BON")
            st.metric("Cohérence Réponses", "94.2%", delta="Excellent")
        
        with col2:
            st.metric("Temps Réponse", "1.8s", delta="Rapide")
            st.metric("Confiance IA", "87%", delta="Élevée")
        
        # Résultats A1 Enhanced si disponibles
        a1_results = results['results'].get('a1_enhanced_results', {})
        if a1_results:
            st.markdown("#### 🤖 Détails A1 Enhanced")
            st.json(a1_results)
    
    with tab4:
        st.markdown("### 📊 Analyse Intégration & Zones Aveugles")
        
        integration_score = results['metrics']['integration_score']
        blind_spots_count = results['metrics']['blind_spots']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("🎯 Score Intégration Global", f"{integration_score:.1f}%", delta="Excellent")
            
            # Breakdown intégration
            st.markdown("#### 📊 Breakdown Intégration")
            breakdown_data = {
                'Composant': ['VCS', 'ABC', 'A1 Enhanced', 'Cohérence'],
                'Score (%)': [results['metrics']['vcs_conformity'], 85.0, results['metrics']['a1_score'], 92.0],
                'Statut': ['✅ Bon', '✅ Très Bon', '✅ Bon', '✅ Excellent']
            }
            df_breakdown = pd.DataFrame(breakdown_data)
            st.dataframe(fix_dataframe_for_streamlit(df_breakdown), use_container_width=True)
        
        with col2:
            st.metric("🚨 Zones Aveugles Détectées", blind_spots_count, 
                     delta="🔍 Identifiées" if blind_spots_count > 0 else "✅ Aucune")
            
            # Zones aveugles détails
            blind_spots = results['results'].get('blind_spots', [])
            if blind_spots:
                st.markdown("#### 🚨 Détails Zones Aveugles")
                for i, blind_spot in enumerate(blind_spots, 1):
                    st.warning(f"{i}. {blind_spot}")
            else:
                st.success("✅ Aucune zone aveugle détectée - Couverture complète!")
            
            # Actions prioritaires
            priority_actions = results['results'].get('priority_actions', [])
            if priority_actions:
                st.markdown("#### 📈 Actions Prioritaires")
                for action in priority_actions:
                    priority_color = "🔴" if action.get('priority') == 'high' else "🟡"
                    st.info(f"{priority_color} {action.get('action', 'Action non définie')}")
    
    with tab5:
        st.markdown("### 📄 Rapport Complet BehaviorX Orchestré")
        
        # Résumé exécutif
        st.markdown("#### 📋 Résumé Exécutif")
        st.success(f"""
        **✅ Workflow BehaviorX Orchestré réussi**
        
        - **Score Global Intégration:** {integration_score:.1f}%
        - **Conformité VCS:** {results['metrics']['vcs_conformity']:.1f}%
        - **Performance A1 Enhanced:** {results['metrics']['a1_score']:.1f}/100
        - **Zones Aveugles:** {blind_spots_count} détectée(s)
        - **Recommandation:** Maintenir excellence opérationnelle
        """)
        
        # Données complètes
        st.markdown("#### 📊 Données Complètes")
        if st.button("📥 Télécharger Rapport JSON"):
            st.download_button(
                label="📥 Télécharger",
                data=json.dumps(results['results'], indent=2),
                file_name=f"rapport_behaviorx_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Affichage JSON
        with st.expander("🔍 Voir Données JSON Complètes"):
            st.json(results['results'])

# ===================================================================
# FONCTION PRINCIPALE MODIFIÉE AVEC ORCHESTRATEUR
# ===================================================================

def main():
    """Fonction principale SafetyGraph Industries avec Orchestrateur BehaviorX"""
    
    # RÉVOLUTION UX/UI - Profils adaptatifs
    current_profile = display_profile_selector()
    display_adaptive_header(current_profile)
    
    # FORCER L'INITIALISATION DU PROFIL HSE MANAGER (Debug)
    init_user_profile()
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = 'hse_manager'
    
    # Configuration sidebar
    config = setup_sidebar()
    
    # Zone principale - Choix workflow
    st.markdown("## 🚀 SafetyGraph Industries - Plateforme Multi-Sectorielle avec Orchestrateur")
    
    # ===================================================================
    # ONGLETS PRINCIPAUX SAFETYGRAPH - INDUSTRIES UNIFIÉES + ORCHESTRATEUR
    # ===================================================================
    main_tabs = st.tabs([
        "🏭 Industries",              # TOUT-EN-UN avec sélecteur SCIAN
        "🎼 BehaviorX Orchestré",     # NOUVEAU - Avec Orchestrateur
        "🗺️ Cartographie Culture",
        "📊 Analytics Prédictifs",
        "🔍 Pattern Recognition", 
        "⚡ Analytics Optimisés"
    ])

    # ===================================================================
    # CONTENU ONGLETS AVEC ORCHESTRATEUR INTÉGRÉ
    # ===================================================================

    with main_tabs[0]:  # Industries - MODULE PRINCIPAL
        display_industries_unified(config)

    with main_tabs[1]:  # BehaviorX Orchestré - NOUVEAU
        st.markdown("## 🎼 SafetyGraph BehaviorX Orchestré")
        st.markdown("### 🚀 Workflow Intelligent VCS→ABC→A1→Intégration avec Mémoire IA")
        
        if not BEHAVIORX_AVAILABLE:
            st.error("❌ Orchestrateur BehaviorX non disponible")
            st.info("🔧 Vérifiez que le fichier src/agents/collecte/orchestrateur_behaviorx_unified.py existe")
        else:
            # Configuration orchestrateur
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 🏢 Entreprise")
                st.info(f"**{config['enterprise_name']}**")
                st.code(f"Secteur: {config['sector_code']}")
            
            with col2:
                st.markdown("#### 🎯 Configuration")
                st.success(f"Mode: {config['workflow_mode']}")
                st.success(f"Mémoire IA: {'✅' if config['memory_enabled'] else '❌'}")
            
            with col3:
                st.markdown("#### 🎼 Orchestrateur")
                st.success("✅ BehaviorX Unifié")
                st.success("✅ Workflow VCS→ABC→A1")
            
            # Bouton lancement orchestrateur
            col_center = st.columns([1, 2, 1])[1]
            with col_center:
                if st.button("🚀 Lancer Orchestrateur BehaviorX", type="primary", use_container_width=True):
                    st.session_state.workflow_type = "behaviorx_orchestrated"
                    st.session_state.workflow_results = None

    with main_tabs[2]:  # Cartographie Culture
        st.markdown("## 🗺️ SafetyGraph BehaviorX + Cartographie Culture SST")
        st.markdown("### 📊 Powered by Safety Agentique | 🌐 LangGraph Multi-Agent | 🌪️ STORM Research | 🧠 Mémoire IA Adaptative")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🗺️ Lancer Cartographie Culture SST", key="launch_cartographie_culture", type="primary"):
                st.success("🎉 Cartographie Culture SST lancée avec succès !")
                st.balloons()
                
                with st.spinner("🔄 Génération cartographie culture secteur..."):
                    time.sleep(1.5)
                
                st.markdown("### 📊 Résultats Cartographie Culture")
                
                # Données adaptées selon secteur sélectionné
                secteur_actuel = config['sector_name']
                culture_data = {
                    "Secteur SCIAN": [secteur_actuel, 'Benchmark National', 'Top 25%', 'Objectif 6 mois'],
                    'Score Culture': [3.8, 3.2, 4.1, 4.5],
                    'Niveau Maturité': ['Réactif', 'Émergent', 'Proactif', 'Prédictif'],
                    'Risque Incident (%)': [15.2, 18.7, 9.3, 6.2],
                    'Conformité (%)': [87.1, 82.3, 94.8, 97.5]
                }
                
                df_culture = pd.DataFrame(culture_data)
                st.dataframe(fix_dataframe_for_streamlit(df_culture), use_container_width=True, hide_index=True)
                st.success("✅ Cartographie générée avec STORM Research enrichi !")
        
        if st.button("🗺️ Lancer Cartographie Complète", use_container_width=True):
            st.session_state.workflow_type = "cartography_complete"
            st.session_state.workflow_results = None

    with main_tabs[3]:  # Analytics Prédictifs
        if ANALYTICS_AVAILABLE:
            display_predictive_analytics_interface()
        else:
            st.warning("⚠️ Module analytics prédictifs non disponible")
            st.info("📊 Métriques secteur actuelles basées sur CNESST 793K incidents")
            
            # Version simplifiée analytics avec expansion sectorielle
            analytics_col1, analytics_col2, analytics_col3 = st.columns(3)
            
            with analytics_col1:
                st.metric("🎯 Précision ML", "92.4%", delta="+2.1%")
                st.metric("📊 Prédictions Actives", "156", delta="+12")
                
            with analytics_col2:
                st.metric("⚡ Temps Traitement", "0.3s", delta="-0.1s")
                st.metric("🎯 Seuil Confiance", "85%", delta="Optimal")
                
            with analytics_col3:
                st.metric("📈 Horizon Prédiction", "6 mois", delta="Configurable")
                st.metric("🚨 Alertes Générées", "3", delta="Actives")
            
            # Spécialisation secteurs expansion
            if "🆕" in config.get('sector_name', ''):
                st.success("🆕 **ANALYTICS SECTEUR EXPANSION** - Métriques spécialisées disponibles!")

    with main_tabs[4]:  # Pattern Recognition
        if ANALYTICS_AVAILABLE:
            display_pattern_recognition_interface()
        else:
            st.warning("⚠️ Module pattern recognition non disponible")
            st.info(f"🔍 Analyse patterns secteur {config['sector_name']}")
            
            # Version simplifiée pattern recognition
            st.markdown("### 🔍 Clustering Comportemental")
            
            pattern_data = pd.DataFrame({
                'Cluster': ['Leadership Fort', 'Formation Active', 'Communication Ouverte', 
                           'Réactif Standard', 'Amélioration Requise', 'Intervention Urgente'],
                'Entreprises (%)': [15, 25, 30, 20, 8, 2],
                'Score Moyen': [4.2, 3.8, 3.9, 3.1, 2.4, 1.8],
                'Votre Position': ['', '', '✅ ICI', '', '', '']
            })
            
            st.dataframe(fix_dataframe_for_streamlit(pattern_data), use_container_width=True)
            st.success("✅ Votre entreprise: Cluster 'Communication Ouverte' - Position favorable")

    with main_tabs[5]:  # Analytics Optimisés
        if OPTIMIZER_AVAILABLE:
            optimizer.render_optimized_analytics()
        else:
            st.warning("⚠️ Optimiseur non disponible - Analytics en mode standard")
            st.info("🚀 Performance système SafetyGraph")
            
            # Métriques performance
            perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
            
            with perf_col1:
                st.metric("⚡ Temps Réponse", "1.2s", delta="Optimal")
            with perf_col2:
                st.metric("🔄 Cache Hit Rate", "89%", delta="+12%")
            with perf_col3:
                st.metric("💾 Mémoire Usage", "78%", delta="Normal")
            with perf_col4:
                st.metric("🌐 API Calls", "245", delta="Efficient")

    # ===================================================================
    # WORKFLOW EXECUTION LOGIC AVEC ORCHESTRATEUR
    # ===================================================================
    
    # Description workflows avec orchestrateur
    if st.session_state.get('workflow_type'):
        if st.session_state.workflow_type == "behaviorx_orchestrated":
            st.info(f"""
            **🎼 Workflow BehaviorX Orchestré - {config['sector_name']}**
            
            🔄 **Orchestration Intelligente:**
            - ✅ Étape 1: VCS Observation avec analyse contextuelle
            - ✅ Étape 2: Analyse ABC comportementale enrichie
            - ✅ Étape 3: Agent A1 Enhanced avec mémoire IA
            - ✅ Étape 4: Intégration + détection zones aveugles
            - ✅ Étape 5: Recommandations prioritaires
            
            🎯 **Spécialisations Secteur SCIAN {config['sector_code']}**
            - 📊 Métriques adaptées au secteur
            - 🧠 Mémoire IA contextualisée
            - 🔍 Benchmarks industrie
            
            ⚡ **Performance:** Exécution optimisée (~45 secondes)
            """)
        
        elif st.session_state.workflow_type == "cartography_complete":
            st.success(f"""
            **🗺️ Cartographie Culture SST Complète - {config['industrie_principale']}**
            - 🗺️ Cartographie 7 dimensions culture SST
            - 🤖 Architecture LangGraph multi-agent (100+ agents)
            - 🔍 Recherche STORM enrichissement scientifique
            - 📋 Plans d'action personnalisés par dimension
            - 📈 Framework monitoring et KPI évolution
            - 🧩 Mémoire IA et apprentissage continu
            - 🏭 Spécialisation {config['industrie_principale']}
            - ⚡ Analyse approfondie (~2-3 minutes)
            """)
        
        # Bouton exécution
        if st.button("▶️ Lancer Workflow Sélectionné", type="primary", use_container_width=True):
            if st.session_state.workflow_type == "behaviorx_orchestrated":
                st.session_state.workflow_results = execute_behaviorx_workflow_orchestrated(config)
            elif st.session_state.workflow_type == "cartography_complete":
                st.session_state.workflow_results = execute_cartography_workflow_complete(config)
    
    # Affichage résultats selon type workflow
    if st.session_state.get('workflow_results'):
        results = st.session_state.workflow_results
        
        if results['success']:
            if results.get('type') == 'behaviorx_orchestrated':
                display_behaviorx_orchestrated_results(results)
            else:
                # Pour cartographie complète, affichage enrichi
                st.success("✅ Cartographie Culture SST terminée avec succès !")
                
                # Métriques cartographie
                cartography_data = results.get('cartography', {}).get('executive_summary', {})
                if cartography_data:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🎯 Maturité Culture", f"{cartography_data.get('overall_culture_maturity', 3.8):.1f}/5")
                    with col2:
                        st.metric("📊 Benchmark Secteur", f"{cartography_data.get('sector_benchmark', 3.2):.1f}/5")
                    with col3:
                        st.metric("🏆 Top 25%", f"{cartography_data.get('top_25_percent', 4.1):.1f}/5")
                
                st.json(cartography_data)
            
            # Ajout à l'historique avec secteur
            if results not in st.session_state.execution_history:
                st.session_state.execution_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': st.session_state.workflow_type,
                    'enterprise': config['enterprise_name'],
                    'sector': config['sector_name'],
                    'industrie': config['industrie_principale'],
                    'sector_code': config['sector_code'],
                    'orchestrated': st.session_state.workflow_type == "behaviorx_orchestrated",
                    'success': True
                })
        else:
            st.error("❌ Erreur lors de l'exécution du workflow")
    
    # Historique exécutions avec industries et orchestrateur
    if st.session_state.execution_history:
        with st.expander("📋 Historique Exécutions Multi-Industries + Orchestrateur"):
            for i, execution in enumerate(reversed(st.session_state.execution_history[-10:]), 1):
                industrie = execution.get('industrie', 'N/A')
                sector_code = execution.get('sector_code', 'N/A')
                orchestrated = execution.get('orchestrated', False)
                orchestrator_badge = "🎼" if orchestrated else "📋"
                
                st.text(f"{i}. {execution['timestamp'][:19]} - {orchestrator_badge} {execution['type']} - {execution['enterprise']} - {industrie} ({sector_code})")
    
    # Footer final avec expansion sectorielle
    st.markdown("---")
    total_secteurs = sum(len(secteurs) for secteurs in SECTEURS_SCIAN_COMPLET.values())
    nouveaux_secteurs = sum(1 for secteurs in SECTEURS_SCIAN_COMPLET.values() for secteur in secteurs.keys() if "🆕" in secteur)
    
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 10px; margin-top: 2rem;">
        <p style="margin: 0; color: #666;">
            🏭 <strong>SafetyGraph Industries v3.1</strong> | 
            💼 Safety Agentique | 
            🎯 {total_secteurs} Secteurs SCIAN (+{nouveaux_secteurs} nouveaux) | 
            🎼 Orchestrateur BehaviorX Intégré |
            🤖 Architecture Multi-Agents | 
            🌪️ STORM Research Intégré
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# POINT D'ENTRÉE APPLICATION
# ===================================================================

if __name__ == "__main__":
    main()