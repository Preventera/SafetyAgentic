"""
Safety Agentique - SafetyGraph BehaviorX Interface
================================================
Interface spécialisée pour le workflow BehaviorX-SafetyAgentic
VCS → ABC → A1 Enhanced → Intégration
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime
import json

# Configuration page
st.set_page_config(
    page_title="SafetyGraph BehaviorX | Safety Agentique",
    page_icon="🎼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import BehaviorX Orchestrator
try:
    sys.path.append(str(Path(__file__).parent / "src" / "agents" / "collecte"))
    from orchestrateur_behaviorx_unified import BehaviorXSafetyOrchestrator
    BEHAVIORX_AVAILABLE = True
except ImportError as e:
    BEHAVIORX_AVAILABLE = False
    st.error(f"❌ BehaviorX Orchestrator non disponible: {e}")

def render_header():
    """Afficher l'en-tête de l'interface Safety Agentique"""
    
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; text-align: center; margin: 0;">
            🎼 SafetyGraph BehaviorX
        </h1>
        <p style="color: #e0e6ed; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.1em;">
            Workflow Intégré VCS → ABC → A1 Enhanced → Intégration
        </p>
        <p style="color: #b8c6db; text-align: center; margin: 0.3rem 0 0 0; font-size: 0.9em;">
            Powered by Safety Agentique
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Interface de configuration dans la sidebar"""
    
    st.sidebar.markdown("### ⚙️ Configuration BehaviorX")
    st.sidebar.markdown("*Module Safety Agentique*")
    
    # Configuration entreprise
    enterprise_name = st.sidebar.text_input(
        "🏢 Nom de l'entreprise",
        value="Construction ABC",
        help="Nom de l'entreprise à analyser"
    )
    
    # Sélection secteur
    sectors = {
        "Construction": "236",
        "Soins de santé": "622", 
        "Fabrication alimentaire": "311",
        "Services professionnels": "541"
    }
    
    sector = st.sidebar.selectbox(
        "📊 Secteur d'activité",
        options=list(sectors.keys()),
        index=0,
        help="Secteur selon classification SCIAN"
    )
    
    # Mode workflow
    workflow_modes = {
        "Hybrid (VCS + Safe Self)": "hybrid",
        "VCS + ABC seulement": "vcs_abc",
        "Safe Self seulement": "self_assessment"
    }
    
    workflow_mode = st.sidebar.selectbox(
        "⚙️ Mode Workflow",
        options=list(workflow_modes.keys()),
        index=0,
        help="Type d'analyse comportementale SafetyGraph"
    )
    
    # Options avancées
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Options Avancées")
    
    enable_memory = st.sidebar.checkbox(
        "🧠 Mémoire IA",
        value=True,
        help="Utiliser la mémoire persistante pour l'apprentissage"
    )
    
    debug_mode = st.sidebar.checkbox(
        "🔍 Mode Debug",
        value=False,
        help="Afficher les détails techniques"
    )
    
    # Information Safety Agentique
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ À propos")
    st.sidebar.info(
        "**Safety Agentique** - Plateforme innovante d'analyse HSE\n\n"
        "**SafetyGraph** - Système d'analyse graphique de culture sécuritaire\n\n"
        "**BehaviorX** - Module d'analyse comportementale avancée"
    )
    
    return {
        'enterprise_name': enterprise_name,
        'sector': sector,
        'sector_code': sectors[sector],
        'workflow_mode': workflow_modes[workflow_mode],
        'enable_memory': enable_memory,
        'debug_mode': debug_mode
    }

def execute_behaviorx_workflow(config):
    """Exécuter le workflow BehaviorX complet"""
    
    if not BEHAVIORX_AVAILABLE:
        st.error("❌ BehaviorX Orchestrator non disponible")
        return None
    
    # Container principal
    with st.container():
        st.markdown("## 🚀 Exécution Workflow BehaviorX")
        
        # Progress tracking
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
        # Colonnes pour les métriques temps réel
        metrics_container = st.container()
        
        try:
            # Étape 1: Initialisation
            status_text.text("🎼 Initialisation Orchestrateur SafetyGraph BehaviorX...")
            progress_bar.progress(10)
            
            orchestrator = BehaviorXSafetyOrchestrator({
                'memory_enabled': config['enable_memory'],
                'debug_mode': config['debug_mode']
            })
            
            # Étape 2: Exécution workflow
            status_text.text("🚀 Exécution Workflow VCS → ABC → A1 Enhanced → Intégration...")
            progress_bar.progress(30)
            
            # Simulation du progress pendant l'exécution
            import time
            for i in range(30, 90, 10):
                time.sleep(0.5)
                progress_bar.progress(i)
            
            results = orchestrator.execute_full_workflow(
                enterprise_id=config['enterprise_name'],
                sector_code=config['sector_code'],
                workflow_mode=config['workflow_mode']
            )
            
            # Étape 3: Finalisation
            progress_bar.progress(100)
            status_text.text("✅ Workflow SafetyGraph BehaviorX Terminé avec Succès !")
            
            # Affichage résultats
            display_workflow_results(results, config)
            
            return results
            
        except Exception as e:
            st.error(f"❌ Erreur lors de l'exécution du workflow SafetyGraph: {e}")
            progress_bar.progress(0)
            status_text.text("❌ Échec du Workflow")
            return None

def display_workflow_results(results, config):
    """Afficher les résultats détaillés du workflow"""
    
    st.markdown("---")
    st.markdown("## 📊 Résultats Workflow SafetyGraph BehaviorX")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        integration_score = results.integration_score
        delta_text = "Excellent" if integration_score > 90 else "Bon" if integration_score > 75 else "À améliorer"
        st.metric(
            "🎯 Score Intégration",
            f"{integration_score:.1f}%",
            delta=delta_text
        )
    
    with col2:
        vcs_conformity = results.vcs_results.get('conformity_rate', 0) if results.vcs_results else 0
        vcs_strengths = results.vcs_results.get('strengths', 0) if results.vcs_results else 0
        st.metric(
            "🔍 Conformité VCS", 
            f"{vcs_conformity:.1f}%",
            delta=f"Forces: {vcs_strengths}"
        )
    
    with col3:
        a1_score = results.a1_enhanced_results.get('safe_self_score', 0) if results.a1_enhanced_results else 0
        a1_level = results.a1_enhanced_results.get('behavioral_level', 'N/A') if results.a1_enhanced_results else 'N/A'
        st.metric(
            "🤖 Score A1 Enhanced",
            f"{a1_score:.1f}",
            delta=a1_level
        )
    
    with col4:
        blind_spots_count = len(results.blind_spots) if results.blind_spots else 0
        delta_text = "Aucune" if blind_spots_count == 0 else f"{blind_spots_count} détectée(s)"
        delta_color = "normal" if blind_spots_count == 0 else "inverse"
        st.metric(
            "🚨 Zones Aveugles",
            blind_spots_count,
            delta=delta_text
        )
    
    # Onglets détaillés
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 VCS Observation", 
        "🔗 Analyse ABC", 
        "🤖 A1 Enhanced", 
        "📈 Intégration",
        "📋 Rapport Complet"
    ])
    
    with tab1:
        display_vcs_results(results)
    
    with tab2:
        display_abc_results(results)
    
    with tab3:
        display_a1_results(results)
    
    with tab4:
        display_integration_results(results)
    
    with tab5:
        display_full_report(results, config)

def display_vcs_results(results):
    """Afficher les résultats VCS"""
    
    st.markdown("#### 🔍 Résultats VCS (Visite Comportementale Sécurité)")
    st.markdown("*Analyse SafetyGraph - Module BehaviorX*")
    
    if not results.vcs_results:
        st.warning("Aucun résultat VCS disponible")
        return
    
    vcs_data = results.vcs_results
    
    # Statistiques VCS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Items Observés", vcs_data.get('checklist_items', 0))
    with col2:
        st.metric("💪 Forces", vcs_data.get('strengths', 0))
    with col3:
        st.metric("⚠️ Préoccupations", vcs_data.get('concerns', 0))
    
    # Graphique conformité (simulation)
    if vcs_data.get('observations'):
        obs_data = vcs_data['observations']
        
        # Créer DataFrame pour visualisation
        df_obs = pd.DataFrame(obs_data)
        
        # Graphique en barres
        fig_bar = px.bar(
            df_obs,
            x='category',
            y='score',
            color='conforme',
            title="📊 Scores VCS par Catégorie - SafetyGraph Analysis",
            color_discrete_map={True: '#28a745', False: '#dc3545'},
            labels={'category': 'Catégorie', 'score': 'Score', 'conforme': 'Conforme'}
        )
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Tableau détaillé
        st.markdown("**📋 Détail des Observations:**")
        df_display = df_obs.copy()
        df_display['conforme'] = df_display['conforme'].map({True: '✅', False: '❌'})
        st.dataframe(df_display, use_container_width=True)

def display_abc_results(results):
    """Afficher les résultats ABC"""
    
    st.markdown("#### 🔗 Analyse ABC (Antécédent-Comportement-Conséquence)")
    st.markdown("*Framework BehaviorX - Safety Agentique*")
    
    if not results.abc_analysis:
        st.warning("Aucune analyse ABC disponible")
        return
    
    abc_data = results.abc_analysis
    patterns = abc_data.get('behavioral_patterns', {})
    
    # Métriques ABC
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Comportements Positifs", patterns.get('positive_behaviors', 0))
    with col2:
        st.metric("❌ Comportements Négatifs", patterns.get('negative_behaviors', 0))
    with col3:
        st.metric("🚨 Interventions Urgentes", patterns.get('high_priority_interventions', 0))
    
    # Points d'intervention
    interventions = abc_data.get('intervention_points', [])
    if interventions:
        st.markdown("**🎯 Points d'Intervention Prioritaires:**")
        
        for intervention in interventions:
            priority = intervention.get('priority', 'medium')
            category = intervention.get('category', 'N/A')
            intervention_type = intervention.get('intervention_type', 'planned')
            
            priority_color = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"
            
            with st.container():
                col1, col2, col3 = st.columns([1, 2, 2])
                with col1:
                    st.write(priority_color)
                with col2:
                    st.write(f"**{category}**")
                with col3:
                    st.write(f"Type: {intervention_type}")

def display_a1_results(results):
    """Afficher les résultats A1 Enhanced"""
    
    st.markdown("#### 🤖 Agent A1 Enhanced (Safe Self + Mémoire IA)")
    st.markdown("*SafetyGraph Intelligence - Safety Agentique*")
    
    if not results.a1_enhanced_results:
        st.warning("Aucun résultat A1 Enhanced disponible")
        return
    
    a1_data = results.a1_enhanced_results
    
    # Gauge du score Safe Self
    score = a1_data.get('safe_self_score', 0)
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Score Safe Self - SafetyGraph"},
        delta = {'reference': 75},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 45], 'color': "lightgray"},
                {'range': [45, 75], 'color': "yellow"},
                {'range': [75, 90], 'color': "lightgreen"},
                {'range': [90, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Détails A1
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📈 Niveau Comportemental", a1_data.get('behavioral_level', 'N/A'))
        st.metric("⚠️ Facteurs de Risque", a1_data.get('risk_factors', 0))
    with col2:
        st.metric("🛡️ Facteurs Protecteurs", a1_data.get('protective_factors', 0))
        st.metric("🧠 Enrichi par ABC", "✅" if a1_data.get('abc_enriched') else "❌")
    
    # Recommandations
    recommendations = a1_data.get('recommendations', [])
    if recommendations:
        st.markdown("**💡 Recommandations SafetyGraph A1:**")
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")

def display_integration_results(results):
    """Afficher les résultats d'intégration"""
    
    st.markdown("#### 📈 Analyse d'Intégration A1↔VCS")
    st.markdown("*SafetyGraph Intelligence - Safety Agentique*")
    
    # Score de cohérence
    coherence_score = results.integration_score
    
    # Graphique de cohérence
    fig_coherence = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = coherence_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Cohérence A1↔VCS (%) - SafetyGraph"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "purple"},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 70], 'color': "yellow"},
                {'range': [70, 90], 'color': "lightgreen"},
                {'range': [90, 100], 'color': "green"}
            ]
        }
    ))
    st.plotly_chart(fig_coherence, use_container_width=True)
    
    # Zones aveugles
    if results.blind_spots:
        st.markdown("**🚨 Zones Aveugles Détectées:**")
        for spot in results.blind_spots:
            st.warning(f"⚠️ {spot}")
    else:
        st.success("✅ Aucune zone aveugle détectée - Cohérence excellente entre perception et observation")
    
    # Actions prioritaires
    if results.priority_actions:
        st.markdown("**🚀 Actions Prioritaires SafetyGraph:**")
        for i, action in enumerate(results.priority_actions, 1):
            priority_emoji = "🔴" if action.get("priority") == "high" else "🟡"
            st.write(f"{i}. {priority_emoji} {action.get('action', 'Action non définie')}")

def display_full_report(results, config):
    """Afficher le rapport complet"""
    
    st.markdown("#### 📋 Rapport Complet SafetyGraph BehaviorX")
    st.markdown("*Safety Agentique - Analyse Comportementale Intégrée*")
    
    # Informations de session
    st.markdown("**📊 Informations de Session:**")
    session_info = {
        "🏢 Entreprise": config['enterprise_name'],
        "📊 Secteur": f"{config['sector']} ({config['sector_code']})",
        "⚙️ Mode Workflow": config['workflow_mode'],
        "🧠 Mémoire IA": "✅ Activée" if config['enable_memory'] else "❌ Désactivée",
        "🎼 Plateforme": "Safety Agentique - SafetyGraph BehaviorX",
        "🕐 Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    for key, value in session_info.items():
        st.write(f"{key}: {value}")
    
    # Synthèse exécutive
    st.markdown("**📈 Synthèse Exécutive Safety Agentique:**")
    
    integration_score = results.integration_score
    if integration_score > 90:
        assessment = "🟢 **EXCELLENT** - Cohérence parfaite entre perception et observation selon SafetyGraph"
    elif integration_score > 75:
        assessment = "🟡 **BON** - Cohérence satisfaisante avec quelques points d'attention identifiés par BehaviorX"
    else:
        assessment = "🔴 **À AMÉLIORER** - Écarts significatifs nécessitant une intervention selon l'analyse SafetyGraph"
    
    st.write(assessment)
    
    # Signatures Safety Agentique
    st.markdown("**🏆 Certification Safety Agentique:**")
    st.info(
        "Cette analyse a été réalisée par **SafetyGraph BehaviorX**, "
        "module avancé de la plateforme **Safety Agentique**. "
        "L'analyse respecte les standards HSE et utilise l'intelligence artificielle "
        "pour une évaluation comportementale précise et objective."
    )
    
    # Données JSON pour export
    with st.expander("💾 Données Complètes SafetyGraph (JSON)", expanded=False):
        export_data = {
            "platform": "Safety Agentique",
            "system": "SafetyGraph",
            "module": "BehaviorX",
            "version": "v2.0",
            "session_info": session_info,
            "integration_score": results.integration_score,
            "vcs_results": results.vcs_results,
            "abc_analysis": results.abc_analysis,
            "a1_enhanced_results": results.a1_enhanced_results,
            "blind_spots": results.blind_spots,
            "priority_actions": results.priority_actions
        }
        st.json(export_data)

def main():
    """Fonction principale de l'interface Safety Agentique"""
    
    # En-tête Safety Agentique
    render_header()
    
    # Configuration sidebar
    config = render_sidebar()
    
    # Vérification disponibilité BehaviorX
    if not BEHAVIORX_AVAILABLE:
        st.error("❌ SafetyGraph BehaviorX Orchestrator non disponible. Vérifiez l'installation.")
        st.info("💡 Pour résoudre ce problème, assurez-vous que le fichier `orchestrateur_behaviorx_unified.py` est présent dans `src/agents/collecte/`")
        return
    
    # Interface principale
    st.markdown("### 🎯 Lancement Workflow SafetyGraph BehaviorX")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(
            "🚀 Lancer Workflow SafetyGraph BehaviorX Complet",
            key="launch_behaviorx",
            help="Exécute le workflow VCS → ABC → A1 Enhanced → Intégration",
            use_container_width=True,
            type="primary"
        ):
            if config['enterprise_name']:
                execute_behaviorx_workflow(config)
            else:
                st.warning("⚠️ Veuillez saisir un nom d'entreprise dans la configuration")
    
    # Informations sur le workflow
    with st.expander("ℹ️ À propos du Workflow SafetyGraph BehaviorX", expanded=False):
        st.markdown("""
        **🎼 Workflow SafetyGraph BehaviorX-Safety Agentique Intégré:**
        
        1. **🔍 VCS (Visite Comportementale Sécurité)** - Observation terrain SafetyGraph
        2. **🔗 Analyse ABC** - Framework Antécédent-Comportement-Conséquence BehaviorX
        3. **🤖 Agent A1 Enhanced** - Safe Self enrichi par mémoire IA Safety Agentique
        4. **📈 Analyse d'Intégration** - Cohérence perception↔observation SafetyGraph
        
        **Avantages Safety Agentique:**
        - ✅ Détection automatique des zones aveugles
        - ✅ Recommandations personnalisées par secteur SCIAN
        - ✅ Mémoire IA pour apprentissage évolutif
        - ✅ Score d'intégration comportementale précis
        - ✅ Conformité standards HSE canadiens
        """)
    
    # Informations produits Safety Agentique
    with st.expander("🏢 Gamme Safety Agentique", expanded=False):
        st.markdown("""
        **🎯 Safety Agentique** - Plateforme HSE innovante
        
        **Produits disponibles:**
        - 📊 **SafetyGraph** - Analyse graphique de culture sécuritaire
        - 🧠 **BehaviorX** - Module d'analyse comportementale avancée
        - 🤖 **Agents Enhanced** - Intelligence artificielle pour HSE
        - 📈 **Memory Systems** - Apprentissage évolutif persistant
        
        **Secteurs desservis:**
        - 🏗️ Construction (SCIAN 236)
        - 🏥 Soins de santé (SCIAN 622)
        - 🏭 Fabrication (SCIAN 311)
        - 💼 Services professionnels (SCIAN 541)
        """)
    
    # Footer Safety Agentique
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>"
        "<strong>SafetyGraph BehaviorX v2.0</strong> | "
        "Orchestrateur Intégré | "
        "<em>Powered by Safety Agentique</em>"
        "</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()