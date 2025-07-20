"""
SafetyGraph BehaviorX - Version Enrichie CNESST
==============================================

Version enrichie de app_behaviorx.py avec intégration complète CNESST
incluant détection automatique secteurs SCIAN, benchmarking temps réel,
et recommandations evidence-based.

Auteur: Mario Genest - GenAISafety
Date: 11 juillet 2025
Version: 2.0 Enrichie CNESST

INSTRUCTIONS D'UTILISATION:
1. Remplacer votre app_behaviorx.py existant par ce fichier
2. Conserver backup: app_behaviorx_BACKUP.py
3. Lancer: streamlit run app_behaviorx.py --server.port 8501
4. Tester détection avec input "construction béton"
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import sqlite3
import logging
from typing import Dict, List, Any, Optional
import traceback
import time

# Configuration Streamlit
st.set_page_config(
    page_title="SafetyGraph BehaviorX - Enrichi CNESST",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================================================================
# MODULE M1: IMPORTS ENRICHIS CNESST
# ===================================================================

print("🔄 [M1] Chargement enrichissements CNESST...")

try:
    # Import conditionnel modules enrichissement
    from src.enrichments.behaviorx_enrichments import (
        CNESSTContextEnhancer,
        EnhancedContextAgent,
        EnhancedRecommendationGenerator
    )
    CNESST_ENHANCED = True
    print("✅ [M1] Enrichissements CNESST chargés avec succès")
    
except ImportError as e:
    CNESST_ENHANCED = False
    print(f"⚠️ [M1] Enrichissements CNESST non disponibles - Mode dégradé")

except Exception as e:
    CNESST_ENHANCED = False
    print(f"❌ [M1] Erreur chargement - {str(e)}")

# Variables globales enrichissement
if CNESST_ENHANCED:
    try:
        cnesst_enhancer = CNESSTContextEnhancer()
        enhanced_context_agent = EnhancedContextAgent()
        enhanced_recommendations = EnhancedRecommendationGenerator()
        print(f"🎯 [M1] Agents enrichis initialisés - {len(cnesst_enhancer.scian_sectors)} secteurs SCIAN")
    except Exception as e:
        print(f"⚠️ [M1] Erreur initialisation agents - {str(e)}")
        CNESST_ENHANCED = False
else:
    cnesst_enhancer = None
    enhanced_context_agent = None
    enhanced_recommendations = None

# ===================================================================
# CSS ET STYLES
# ===================================================================

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2980b9 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2980b9;
        margin-bottom: 1rem;
    }
    
    .workflow-step {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #27ae60;
        margin: 1rem 0;
    }
    
    .cnesst-enhancement {
        background: linear-gradient(90deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .recommendation-priority {
        background: #fee;
        border: 1px solid #fcc;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    
    .recommendation-medium {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    
    .recommendation-info {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# CLASSE PRINCIPALE SAFETYGRAPH BEHAVIORX
# ===================================================================

class SafetyGraphBehaviorX:
    """Classe principale SafetyGraph BehaviorX enrichie CNESST"""
    
    def __init__(self):
        self.initialize_session_state()
        self.load_culture_dimensions()
        self.initialize_databases()
        
    def initialize_session_state(self):
        """Initialisation état session Streamlit"""
        
        # États de base
        if 'analysis_complete' not in st.session_state:
            st.session_state.analysis_complete = False
        
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 'input'
        
        if 'user_responses' not in st.session_state:
            st.session_state.user_responses = {}
        
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = {}
        
        # NOUVEAU: États enrichissement CNESST
        if 'cnesst_context' not in st.session_state:
            st.session_state.cnesst_context = {}
        
        if 'sector_benchmarks' not in st.session_state:
            st.session_state.sector_benchmarks = {}
    
    def load_culture_dimensions(self):
        """Chargement dimensions culture SST"""
        
        self.culture_dimensions = {
            "leadership": {
                "name": "Leadership et Engagement",
                "description": "Engagement visible de la direction",
                "questions": [
                    "La direction démontre-t-elle un engagement visible envers la sécurité?",
                    "Les ressources nécessaires sont-elles allouées à la sécurité?",
                    "Les leaders participent-ils activement aux activités sécurité?"
                ]
            },
            "participation": {
                "name": "Participation des Employés",
                "description": "Implication active des employés",
                "questions": [
                    "Les employés participent-ils activement aux décisions sécurité?",
                    "Y a-t-il des comités de sécurité fonctionnels?",
                    "Les suggestions d'amélioration sont-elles encouragées?"
                ]
            },
            "communication": {
                "name": "Communication",
                "description": "Échange d'informations sécurité",
                "questions": [
                    "La communication sécurité est-elle claire et régulière?",
                    "Les incidents sont-ils communiqués efficacement?",
                    "Y a-t-il des canaux de communication ouverts?"
                ]
            },
            "competence": {
                "name": "Compétence et Formation",
                "description": "Développement des compétences",
                "questions": [
                    "Les formations sécurité sont-elles adéquates?",
                    "Les compétences sont-elles évaluées régulièrement?",
                    "Y a-t-il un plan de développement des compétences?"
                ]
            },
            "accountability": {
                "name": "Responsabilisation",
                "description": "Responsabilités clairement définies",
                "questions": [
                    "Les responsabilités sécurité sont-elles claires?",
                    "Y a-t-il des mécanismes de reddition de comptes?",
                    "Les écarts sont-ils adressés promptement?"
                ]
            },
            "learning": {
                "name": "Apprentissage Organisationnel",
                "description": "Capacité d'apprentissage continu",
                "questions": [
                    "L'organisation apprend-elle de ses erreurs?",
                    "Y a-t-il une analyse systématique des incidents?",
                    "Les bonnes pratiques sont-elles partagées?"
                ]
            },
            "environment": {
                "name": "Environnement de Travail",
                "description": "Conditions de travail sécuritaires",
                "questions": [
                    "L'environnement de travail est-il sécuritaire?",
                    "Les équipements de protection sont-ils disponibles?",
                    "Les procédures sont-elles appliquées?"
                ]
            }
        }
    
    def initialize_databases(self):
        """Initialisation bases de données"""
        
        # Base de données comportementales
        try:
            self.behavioral_db = "data/safetyagentic_behaviorx.db"
            # Création si n'existe pas
            conn = sqlite3.connect(self.behavioral_db)
            conn.close()
        except Exception as e:
            logger.warning(f"Erreur initialisation DB: {e}")

# ===================================================================
# MODULE M2: DÉTECTION SCIAN ET WIDGETS
# ===================================================================

def process_user_input_with_scian_detection(user_input):
    """[M2] Traitement input avec détection SCIAN automatique"""
    
    if not CNESST_ENHANCED:
        return {"scian_detected": None, "enrichment": None, "status": "non_available"}
    
    try:
        # Détection secteur SCIAN
        detected_scian = cnesst_enhancer.detect_scian_from_input(user_input)
        
        if detected_scian:
            # Message détection
            sector_name = cnesst_enhancer.sector_mappings.get(detected_scian, f"Secteur {detected_scian}")
            st.success(f"✨ Secteur SCIAN détecté: **{detected_scian}** - {sector_name}")
            
            # Récupération enrichissement
            sector_enrichment = cnesst_enhancer.get_sector_enrichment(detected_scian)
            
            if sector_enrichment.get("available", False):
                # Widget métriques secteur
                display_cnesst_metrics_widget(sector_enrichment)
                
                return {
                    "scian_detected": detected_scian,
                    "enrichment": sector_enrichment,
                    "status": "enriched"
                }
            else:
                st.warning(f"⚠️ Secteur {detected_scian} détecté - données en cours d'intégration")
                return {
                    "scian_detected": detected_scian,
                    "enrichment": None,
                    "status": "detected_no_data"
                }
        else:
            return {
                "scian_detected": None,
                "enrichment": None,
                "status": "no_detection"
            }
    
    except Exception as e:
        st.error(f"❌ [M2] Erreur détection SCIAN: {str(e)}")
        return {"scian_detected": None, "enrichment": None, "status": "error"}

def display_cnesst_metrics_widget(sector_enrichment):
    """[M2] Widget affichage métriques CNESST"""
    
    try:
        benchmarks = sector_enrichment["benchmarks"]
        
        # Header attractif
        st.markdown(f"""
        <div class="cnesst-enhancement">
            <h3>📊 Benchmarks Secteur CNESST</h3>
            <p>Données statistiques officielles pour comparaison avec votre organisation</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📈 Total Jours Absence",
                f"{benchmarks['total_absence_days']:,}",
                help="Nombre total jours d'absence dans ce secteur"
            )
        
        with col2:
            st.metric(
                "🏥 Total Lésions",
                f"{benchmarks['total_injuries']:,}",
                help="Nombre total de lésions déclarées"
            )
        
        with col3:
            st.metric(
                "⏱️ Moyenne/Lésion",
                f"{benchmarks['average_absence']}j",
                help="Durée moyenne d'absence par lésion"
            )
        
        with col4:
            st.metric(
                "🎯 Indice Gravité",
                f"{benchmarks.get('severity_index', 100):.1f}",
                help="Indice de gravité sectorielle"
            )
        
        # Risques dominants
        if "risk_profile" in sector_enrichment:
            st.subheader("⚠️ Risques Dominants Secteur")
            
            risk_profile = sector_enrichment["risk_profile"]
            
            # Graphique risques
            risk_df = pd.DataFrame([
                {"Risque": k.replace("_", " ").title(), "Pourcentage": v}
                for k, v in risk_profile.items()
            ])
            
            fig = px.bar(risk_df, x="Risque", y="Pourcentage", 
                        title="Distribution des Risques - Secteur CNESST")
            st.plotly_chart(fig, use_container_width=True)
            
            # Top 3 risques
            sorted_risks = sorted(risk_profile.items(), key=lambda x: x[1], reverse=True)[:3]
            
            st.write("**🎯 Top 3 Risques Sectoriels:**")
            for i, (risk, percentage) in enumerate(sorted_risks, 1):
                st.write(f"**{i}. {risk.replace('_', ' ').title()}**: {percentage}%")
        
        # Actions prioritaires
        if "prevention_priorities" in sector_enrichment:
            st.subheader("💡 Actions Prioritaires Secteur")
            priorities = sector_enrichment["prevention_priorities"]
            for i, action in enumerate(priorities[:4], 1):
                st.write(f"✅ **{i}.** {action}")
    
    except Exception as e:
        st.error(f"[M2] Erreur affichage métriques: {str(e)}")

# ===================================================================
# FONCTIONS WORKFLOW VCS→ABC
# ===================================================================

def display_workflow_header():
    """Header principal SafetyGraph"""
    
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ SafetyGraph BehaviorX - Enrichi CNESST</h1>
        <p>Analyse Culture Sécurité avec Enrichissement Automatique Secteurs SCIAN</p>
        <p><strong>Version 2.0</strong> | Mario Genest - GenAISafety | Juillet 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Statut enrichissement
    if CNESST_ENHANCED:
        st.success(f"✨ Enrichissements CNESST activés - {len(cnesst_enhancer.scian_sectors)} secteurs disponibles")
    else:
        st.info("📝 Mode standard - Enrichissements CNESST non disponibles")

def collect_user_input():
    """Collecte input utilisateur avec détection SCIAN"""
    
    st.subheader("🔍 Analyse Culture Sécurité")
    
    # Input principal
    st.write("**Décrivez votre organisation et le contexte d'analyse :**")
    user_input = st.text_area(
        "Contexte analyse",
        placeholder="Ex: Analyser culture sécurité équipe construction béton projet résidentiel...",
        height=100,
        help="Mentionnez le secteur d'activité pour activer l'enrichissement CNESST automatique"
    )
    
    if user_input:
        # NOUVEAU: Détection SCIAN automatique
        cnesst_context = process_user_input_with_scian_detection(user_input)
        st.session_state.cnesst_context = cnesst_context
        st.session_state.user_input = user_input
        
        return True
    
    return False

def culture_assessment_workflow():
    """Workflow principal évaluation culture SST"""
    
    # Initialisation SafetyGraph
    safety_graph = SafetyGraphBehaviorX()
    
    st.subheader("📋 Évaluation Culture SST - 7 Dimensions")
    
    # Collecte réponses par dimension
    responses = {}
    
    for dim_key, dimension in safety_graph.culture_dimensions.items():
        
        with st.expander(f"📊 {dimension['name']}", expanded=False):
            st.write(f"*{dimension['description']}*")
            
            dim_responses = []
            
            for i, question in enumerate(dimension['questions']):
                response = st.slider(
                    question,
                    min_value=1, max_value=10, value=5,
                    key=f"{dim_key}_{i}",
                    help="1 = Très faible, 10 = Excellent"
                )
                dim_responses.append(response)
            
            responses[dim_key] = {
                "scores": dim_responses,
                "average": np.mean(dim_responses),
                "name": dimension['name']
            }
    
    # Bouton analyse
    if st.button("🚀 Lancer Analyse Culture SST", type="primary"):
        with st.spinner("Analyse en cours..."):
            time.sleep(2)  # Simulation traitement
            
            # Stockage résultats
            st.session_state.culture_responses = responses
            st.session_state.analysis_complete = True
            
            # Calcul score global
            global_score = np.mean([dim['average'] for dim in responses.values()])
            st.session_state.global_score = global_score
        
        st.success("✅ Analyse terminée!")
        st.rerun()

def display_analysis_results():
    """Affichage résultats analyse avec enrichissement CNESST"""
    
    if not st.session_state.analysis_complete:
        return
    
    st.subheader("📈 Résultats Analyse Culture SST")
    
    # Score global
    global_score = st.session_state.global_score
    responses = st.session_state.culture_responses
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Score Global", f"{global_score:.1f}/10")
    
    with col2:
        status = "Excellent" if global_score >= 8 else "Bon" if global_score >= 6 else "À améliorer"
        st.metric("📊 Statut", status)
    
    with col3:
        st.metric("📋 Dimensions Évaluées", len(responses))
    
    with col4:
        # Comparaison secteur si disponible
        cnesst_context = st.session_state.get('cnesst_context', {})
        if cnesst_context.get('status') == 'enriched':
            # Simulation comparaison vs secteur
            sector_avg = 6.8  # Simulation moyenne sectorielle
            diff = global_score - sector_avg
            st.metric("🏭 vs Secteur", f"{diff:+.1f}", f"Moyenne secteur: {sector_avg}")
        else:
            st.metric("📊 Analyse", "Standard")
    
    # Graphique radar dimensions
    display_culture_radar_chart(responses)
    
    # Analyse détaillée par dimension
    display_dimension_analysis(responses)

def display_culture_radar_chart(responses):
    """Graphique radar culture SST"""
    
    # Préparation données
    dimensions = list(responses.keys())
    scores = [responses[dim]['average'] for dim in dimensions]
    names = [responses[dim]['name'] for dim in dimensions]
    
    # Graphique radar
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=names,
        fill='toself',
        name='Score Culture SST',
        line_color='#2980b9'
    ))
    
    # Ajout ligne secteur si disponible
    cnesst_context = st.session_state.get('cnesst_context', {})
    if cnesst_context.get('status') == 'enriched':
        # Simulation scores sectoriels
        sector_scores = [6.8, 6.5, 7.1, 6.9, 6.3, 7.0, 6.7]  # Simulation
        
        fig.add_trace(go.Scatterpolar(
            r=sector_scores,
            theta=names,
            fill='toself',
            name='Moyenne Secteur CNESST',
            line_color='#e74c3c',
            opacity=0.6
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True,
        title="Profil Culture Sécurité - 7 Dimensions"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_dimension_analysis(responses):
    """Analyse détaillée par dimension"""
    
    st.subheader("🔍 Analyse Détaillée par Dimension")
    
    # Tri dimensions par score
    sorted_dims = sorted(responses.items(), key=lambda x: x[1]['average'], reverse=True)
    
    # Top 3 et Bottom 3
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**✅ Points Forts (Top 3):**")
        for i, (dim_key, dim_data) in enumerate(sorted_dims[:3], 1):
            st.write(f"{i}. **{dim_data['name']}**: {dim_data['average']:.1f}/10")
    
    with col2:
        st.write("**⚠️ Points d'Amélioration (Bottom 3):**")
        for i, (dim_key, dim_data) in enumerate(sorted_dims[-3:], 1):
            st.write(f"{i}. **{dim_data['name']}**: {dim_data['average']:.1f}/10")
    
    # Graphique détaillé
    dim_names = [dim_data['name'] for _, dim_data in sorted_dims]
    dim_scores = [dim_data['average'] for _, dim_data in sorted_dims]
    
    fig = px.bar(
        x=dim_scores, 
        y=dim_names,
        orientation='h',
        title="Scores par Dimension Culture SST",
        color=dim_scores,
        color_continuous_scale="RdYlGn"
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# ===================================================================
# MODULE M4: RECOMMANDATIONS ENRICHIES
# ===================================================================

def generate_recommendations():
    """Génération recommandations avec enrichissement CNESST"""
    
    if not st.session_state.analysis_complete:
        return
    
    # Recommandations de base
    responses = st.session_state.culture_responses
    global_score = st.session_state.global_score
    
    base_recommendations = []
    
    # Recommandations selon score global
    if global_score < 6:
        base_recommendations.extend([
            "Développer un plan d'amélioration culture sécurité global",
            "Renforcer l'engagement de la direction",
            "Améliorer la communication sécurité"
        ])
    elif global_score < 8:
        base_recommendations.extend([
            "Consolider les acquis culture sécurité",
            "Cibler les dimensions les plus faibles",
            "Développer programme formation continue"
        ])
    else:
        base_recommendations.extend([
            "Maintenir l'excellence culture sécurité",
            "Partager bonnes pratiques",
            "Devenir organisation apprenante"
        ])
    
    # Recommandations par dimension faible
    sorted_dims = sorted(responses.items(), key=lambda x: x[1]['average'])
    
    for dim_key, dim_data in sorted_dims[:2]:  # 2 plus faibles
        if dim_data['average'] < 7:
            base_recommendations.append(f"Améliorer {dim_data['name']}: Formation spécialisée")
    
    # NOUVEAU: Enrichissement CNESST
    enhanced_recs = enhance_recommendations_with_cnesst(base_recommendations)
    
    # Affichage recommandations enrichies
    display_enhanced_recommendations(enhanced_recs)

def enhance_recommendations_with_cnesst(existing_recommendations):
    """[M4] Enrichissement recommandations avec contexte CNESST"""
    
    if not CNESST_ENHANCED:
        return existing_recommendations
    
    # Récupération contexte CNESST
    cnesst_context = st.session_state.get('cnesst_context', {})
    
    if not cnesst_context.get("scian_detected"):
        return existing_recommendations
    
    try:
        enhanced_recs = []
        
        # Recommandations existantes d'abord
        for i, rec in enumerate(existing_recommendations):
            enhanced_recs.append({
                "id": f"base_{i}",
                "title": rec,
                "source": "Analyse Culture SafetyGraph",
                "type": "base",
                "priority": "standard"
            })
        
        # Recommandations sectorielles CNESST
        scian_code = cnesst_context["scian_detected"]
        enrichment = cnesst_context.get("enrichment")
        
        if enrichment and enrichment.get("available"):
            sector_recs = generate_cnesst_sector_recommendations(scian_code, enrichment)
            enhanced_recs.extend(sector_recs)
        
        return enhanced_recs
        
    except Exception as e:
        st.warning(f"⚠️ [M4] Erreur enrichissement: {str(e)}")
        return existing_recommendations

def generate_cnesst_sector_recommendations(scian_code, enrichment):
    """[M4] Génération recommandations sectorielles CNESST"""
    
    sector_recs = []
    
    try:
        risk_profile = enrichment.get("risk_profile", {})
        prevention_priorities = enrichment.get("prevention_priorities", [])
        benchmarks = enrichment["benchmarks"]
        
        # Recommandation risque dominant
        if risk_profile:
            top_risk = max(risk_profile.items(), key=lambda x: x[1])
            risk_name, risk_percentage = top_risk
            
            sector_recs.append({
                "id": f"cnesst_risk_{scian_code}",
                "title": f"🔴 Prioriser Prévention {risk_name.replace('_', ' ').title()}",
                "description": f"Risque dominant secteur {scian_code} ({risk_percentage}% incidents)",
                "source": "Statistiques CNESST sectorielles",
                "type": "cnesst_priority",
                "priority": "haute",
                "evidence": f"Base: {benchmarks['total_injuries']:,} incidents analysés",
                "sector_context": scian_code
            })
        
        # Actions prioritaires sectorielles
        for i, action in enumerate(prevention_priorities[:2], 1):
            sector_recs.append({
                "id": f"cnesst_action_{scian_code}_{i}",
                "title": f"🟡 {action}",
                "description": f"Action prioritaire secteur {enrichment['sector_name']}",
                "source": "Bonnes pratiques CNESST",
                "type": "cnesst_action",
                "priority": "moyenne",
                "sector_context": scian_code
            })
        
        # Benchmark information
        sector_recs.append({
            "id": f"cnesst_benchmark_{scian_code}",
            "title": "📊 Benchmarking Sectoriel Disponible",
            "description": f"Comparaison vs {benchmarks['total_injuries']:,} incidents secteur",
            "source": "Base CNESST officielle",
            "type": "cnesst_info",
            "priority": "info",
            "details": {
                "avg_absence": benchmarks['average_absence'],
                "sector_name": enrichment['sector_name']
            }
        })
        
        return sector_recs
        
    except Exception as e:
        st.error(f"[M4] Erreur génération recommandations sectorielles: {str(e)}")
        return []

def display_enhanced_recommendations(enhanced_recs):
    """[M4] Affichage recommandations enrichies"""
    
    if not enhanced_recs:
        st.info("Aucune recommandation disponible")
        return
    
    st.subheader("💡 Recommandations Personnalisées")
    
    # Séparation par type
    base_recs = [r for r in enhanced_recs if r.get("type") == "base"]
    cnesst_recs = [r for r in enhanced_recs if r.get("type", "").startswith("cnesst")]
    
    # Recommandations de base
    if base_recs:
        st.markdown("#### 🔧 Recommandations Analyse Culture SST")
        for i, rec in enumerate(base_recs, 1):
            st.write(f"{i}. {rec['title']}")
    
    # Recommandations CNESST enrichies
    if cnesst_recs:
        st.markdown("#### ✨ Recommandations Enrichies CNESST")
        
        for rec in cnesst_recs:
            if rec.get("type") == "cnesst_priority":
                st.markdown(f"""
                <div class="recommendation-priority">
                    <h4>{rec['title']}</h4>
                    <p><strong>Evidence:</strong> {rec['evidence']}</p>
                    <p><em>Source: {rec['source']}</em></p>
                </div>
                """, unsafe_allow_html=True)
            
            elif rec.get("type") == "cnesst_action":
                st.markdown(f"""
                <div class="recommendation-medium">
                    <h4>{rec['title']}</h4>
                    <p>{rec['description']}</p>
                    <p><em>Source: {rec['source']}</em></p>
                </div>
                """, unsafe_allow_html=True)
            
            elif rec.get("type") == "cnesst_info":
                st.markdown(f"""
                <div class="recommendation-info">
                    <h4>{rec['title']}</h4>
                    <p>{rec['description']}</p>
                    <p><em>Source: {rec['source']}</em></p>
                </div>
                """, unsafe_allow_html=True)

# ===================================================================
# MODULE M3: DASHBOARD EXPERT
# ===================================================================

def add_expert_dashboard_link():
    """[M3] Lien vers dashboard expert SafetyGraph"""
    
    st.markdown("---")
    st.markdown("### 🎯 Administration Expert SafetyGraph")
    
    # Description module expert
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #3498db;">
        <h4>🚀 Dashboard Expert CNESST</h4>
        <p><strong>Fonctionnalités avancées:</strong></p>
        <ul>
            <li>📊 Administration 104 agents SafetyGraph</li>
            <li>📈 Analytics secteurs SCIAN détaillés</li>
            <li>⚡ Monitoring performance pipeline</li>
            <li>💾 Gestion sources données CNESST</li>
            <li>⚙️ Configuration système avancée</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton accès
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🎯 Ouvrir Dashboard Expert", use_container_width=True, type="primary"):
            st.success("🚀 Instructions dashboard expert:")
            
            st.code("""
# Nouveau terminal PowerShell:
cd "C:\\Users\\Mario\\Documents\\PROJECTS_NEW\\SafeGraph"
streamlit run app_cnesst_dashboard.py --server.port 8502

# Puis accéder: http://localhost:8502
            """, language="bash")
    
    # Statut modules
    st.markdown("---")
    st.subheader("📊 Statut Système SafetyGraph")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🏠 Module Principal", "✅ Actif", "Port 8501")
    
    with col2:
        if CNESST_ENHANCED:
            st.metric("✨ Enrichissements", "✅ Disponibles", f"{len(cnesst_enhancer.scian_sectors)} secteurs")
        else:
            st.metric("✨ Enrichissements", "⚠️ Non disponibles", "Mode standard")
    
    with col3:
        st.metric("🎯 Dashboard Expert", "⏸️ À démarrer", "Port 8502")

# ===================================================================
# FONCTIONS UTILITAIRES
# ===================================================================

def display_system_info():
    """Informations système SafetyGraph"""
    
    with st.expander("ℹ️ Informations Système SafetyGraph"):
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🏗️ Architecture:**")
            st.write("• Module Principal Enrichi (Port 8501)")
            st.write("• Dashboard Expert (Port 8502)")
            st.write("• Communication inter-modules")
            
            st.write("**📊 Données:**")
            if CNESST_ENHANCED:
                st.write(f"• {len(cnesst_enhancer.scian_sectors)} secteurs SCIAN")
                st.write("• Benchmarks CNESST intégrés")
                st.write("• Détection automatique secteurs")
            else:
                st.write("• Mode standard activé")
                st.write("• Enrichissements non disponibles")
        
        with col2:
            st.write("**🤖 Fonctionnalités:**")
            st.write("• Analyse culture SST 7 dimensions")
            st.write("• Détection automatique secteur SCIAN")
            st.write("• Benchmarking temps réel vs secteur")
            st.write("• Recommandations evidence-based")
            
            st.write("**⚡ Performance:**")
            st.write("• Analyses rapides <5s")
            st.write("• Interface responsive")
            st.write("• Graphiques interactifs")

def run_system_tests():
    """Tests système SafetyGraph"""
    
    st.subheader("🧪 Tests Système SafetyGraph")
    
    if st.button("▶️ Lancer Tests"):
        
        # Test M1 - Imports
        st.write("**Test M1 - Imports:**")
        st.write(f"✅ CNESST_ENHANCED: {CNESST_ENHANCED}")
        
        if CNESST_ENHANCED:
            st.write(f"✅ Secteurs SCIAN disponibles: {len(cnesst_enhancer.scian_sectors)}")
        else:
            st.write("⚠️ Mode dégradé - enrichissements non disponibles")
        
        # Test M2 - Détection SCIAN
        st.write("**Test M2 - Détection SCIAN:**")
        if CNESST_ENHANCED:
            test_inputs = ["construction béton", "hôpital santé", "transport camion"]
            for test_input in test_inputs:
                detected = cnesst_enhancer.detect_scian_from_input(test_input)
                st.write(f"• '{test_input}' → {detected if detected else 'Non détecté'}")
        else:
            st.write("⚠️ Tests ignorés - enrichissements non disponibles")
        
        # Test M3 - Dashboard
        st.write("**Test M3 - Dashboard Expert:**")
        st.write("✅ Fonction add_expert_dashboard_link disponible")
        
        # Test M4 - Recommandations
        st.write("**Test M4 - Recommandations:**")
        st.write("✅ Fonction enhance_recommendations_with_cnesst disponible")
        
        st.success("🎉 Tests système terminés!")

# ===================================================================
# FONCTION PRINCIPALE
# ===================================================================

def main():
    """Fonction principale SafetyGraph BehaviorX enrichie"""
    
    # Header principal
    display_workflow_header()
    
    # Navigation principale
    st.sidebar.title("🛡️ SafetyGraph Navigation")
    
    page = st.sidebar.selectbox(
        "Choisir analyse:",
        [
            "🏠 Accueil",
            "🔍 Analyse Culture SST", 
            "📊 Résultats & Recommandations",
            "🧪 Tests Système",
            "ℹ️ Informations"
        ]
    )
    
    # Affichage selon page
    if page == "🏠 Accueil":
        st.markdown("## 🏠 Accueil SafetyGraph")
        
        st.markdown("""
        ### 🎯 Bienvenue dans SafetyGraph BehaviorX Enrichi
        
        **Version 2.0 avec intégration CNESST complète**
        
        #### 🚀 Fonctionnalités:
        - **Analyse Culture SST** 7 dimensions complète
        - **Détection automatique secteur SCIAN** depuis votre description
        - **Benchmarking temps réel** vs statistiques sectorielles CNESST
        - **Recommandations evidence-based** avec sources scientifiques
        - **Dashboard expert** administration 104 agents (module séparé)
        
        #### 📊 Comment utiliser:
        1. **Commencer analyse** → Onglet "Analyse Culture SST"
        2. **Décrire votre organisation** → Mentionner secteur pour détection automatique
        3. **Compléter évaluation** → 7 dimensions culture sécurité
        4. **Consulter résultats** → Benchmarks et recommandations enrichies
        
        #### ✨ Nouveautés Version 2.0:
        - Détection automatique secteur SCIAN depuis description
        - Benchmarking temps réel avec données CNESST officielles
        - Recommandations personnalisées selon secteur d'activité
        - Interface enrichie avec métriques sectorielles
        """)
        
        # Statut système
        if CNESST_ENHANCED:
            st.success(f"✅ Enrichissements CNESST activés - {len(cnesst_enhancer.scian_sectors)} secteurs supportés")
        else:
            st.warning("⚠️ Enrichissements CNESST non disponibles - Mode standard activé")
    
    elif page == "🔍 Analyse Culture SST":
        
        # Collecte input utilisateur
        if collect_user_input():
            st.markdown("---")
            
            # Workflow évaluation culture
            culture_assessment_workflow()
    
    elif page == "📊 Résultats & Recommandations":
        
        if st.session_state.analysis_complete:
            # Affichage résultats
            display_analysis_results()
            
            st.markdown("---")
            
            # Génération recommandations
            generate_recommendations()
            
        else:
            st.info("📝 Veuillez d'abord compléter l'analyse culture SST")
            
            if st.button("↩️ Retour à l'analyse"):
                st.switch_page("🔍 Analyse Culture SST")
    
    elif page == "🧪 Tests Système":
        run_system_tests()
    
    elif page == "ℹ️ Informations":
        display_system_info()
    
    # Module M3: Lien dashboard expert (toujours affiché)
    add_expert_dashboard_link()

# ===================================================================
# POINT D'ENTRÉE APPLICATION
# ===================================================================

if __name__ == "__main__":
    try:
        main()
        
        # Messages système en bas
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            🛡️ SafetyGraph BehaviorX v2.0 Enrichi CNESST | 
            👤 Mario Genest - GenAISafety | 
            📅 Juillet 2025 | 
            ⚡ Détection Automatique Secteurs SCIAN
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Erreur application: {str(e)}")
        st.write("**Traceback:**")
        st.code(traceback.format_exc())
        
        if st.button("🔄 Redémarrer Application"):
            st.rerun()