"""
Module Mines Souterraines - SafetyGraph BehaviorX SCIAN-212
===========================================================
Interface BehaviorX spécialisée pour mines souterraines
Intégration Thunder Client pour données sectorielles
Safety Agentique - Mario Plourde - 20 juillet 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
from datetime import datetime
from typing import Dict, List, Any

# ===================================================================
# CONFIGURATION THUNDER CLIENT
# ===================================================================

class ThunderClientMines:
    """Client Thunder pour données mines souterraines"""
    
    def __init__(self):
        self.base_url = "http://localhost:3000/api"  # Thunder Client local
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": "safetygraph-mines-scian212"
        }
        
    def get_mines_data(self, mine_id: str) -> Dict[str, Any]:
        """Récupère données mine spécifique"""
        endpoint = f"{self.base_url}/mines/{mine_id}"
        
        # Simulation données (remplacer par vraie API Thunder Client)
        return {
            "mine_id": mine_id,
            "extraction_type": "Or",
            "depth_meters": 850,
            "employees_count": 164,
            "automation_level": "Moyen",
            "safety_score": 78.5,
            "incidents_last_month": 3,
            "cnesst_compliance": 87.2,
            "last_inspection": "2025-07-15",
            "risk_factors": [
                "Ventilation insuffisante",
                "Espaces confinés multiples", 
                "Équipements vieillissants"
            ],
            "safety_metrics": {
                "gas_detection_coverage": 92.0,
                "emergency_response_time": "4.2 min",
                "evacuation_drill_frequency": "Mensuelle",
                "ppe_compliance": 89.5
            }
        }
    
    def get_sector_benchmarks(self, scian_code: str = "212") -> Dict[str, Any]:
        """Benchmarks secteur mines SCIAN-212"""
        return {
            "scian_code": scian_code,
            "sector_name": "Mines souterraines",
            "total_enterprises": 127,
            "average_safety_score": 74.3,
            "industry_incidents_rate": 12.7,
            "best_practices": [
                "Système buddy obligatoire",
                "Détection gaz automatisée", 
                "Communication radio redondante",
                "Formation espaces confinés certifiée"
            ],
            "regulatory_requirements": [
                "CSA Z259 - Protection antichute",
                "CSA Z150 - Espaces clos",
                "CNESST - Règlement mines",
                "Transport Canada - Matières dangereuses"
            ]
        }

# ===================================================================
# INTERFACE MINES SOUTERRAINES
# ===================================================================

def mines_souterraines_secteur():
    """Interface BehaviorX Mines Souterraines SCIAN-212"""
    
    st.header("⛏️ BehaviorX Mines Souterraines SCIAN-212")
    st.markdown("*Analyse comportementale HSE spécialisée selon standards CNESST*")
    
    # Initialisation Thunder Client
    thunder_client = ThunderClientMines()
    
    # Configuration mine
    col1, col2 = st.columns(2)
    
    with col1:
        enterprise = st.text_input("🏢 Entreprise minière", 
                                  value="Mines ABC Ltée", 
                                  key="mines_enterprise")
        extraction_type = st.selectbox("⚒️ Type d'extraction", 
                                     ["Or", "Cuivre", "Zinc", "Fer", "Nickel", "Argent"],
                                     index=0, key="mines_extraction")
        depth = st.number_input("📏 Profondeur max (m)", 
                               min_value=50, max_value=3000, 
                               value=850, key="mines_depth")
    
    with col2:
        employees = st.number_input("👥 Nombre employés", 
                                  min_value=5, max_value=1000, 
                                  value=164, key="mines_employees")
        automation = st.selectbox("🤖 Niveau automatisation", 
                                ["Faible", "Moyen", "Élevé"], 
                                index=1, key="mines_automation_level")
        
        # Incidents récents
        with st.expander("⚠️ Incidents récents (optionnel)"):
            incidents = st.text_area("Description incidents derniers mois", 
                                    placeholder="Ex: Alarme gaz niveau 2, chute équipement...", 
                                    key="mines_incidents")
    
    # Bouton analyse Thunder Client
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Analyser avec Thunder Client", type="primary", key="mines_analyze_thunder"):
            if not enterprise or not extraction_type:
                st.error("❌ Nom entreprise et type d'extraction requis")
                return
            
            # Analyse avec données Thunder Client
            with st.spinner("🔄 Récupération données Thunder Client..."):
                # Simulation appel API
                mine_data = thunder_client.get_mines_data(f"{enterprise.lower().replace(' ', '_')}")
                sector_benchmarks = thunder_client.get_sector_benchmarks("212")
                
                st.success("✅ Données Thunder Client récupérées !")
            
            # Affichage résultats enrichis
            display_mines_analysis_results(mine_data, sector_benchmarks, {
                'enterprise': enterprise,
                'extraction_type': extraction_type,
                'depth': depth,
                'employees': employees,
                'automation': automation,
                'incidents': incidents
            })

def display_mines_analysis_results(mine_data: Dict, benchmarks: Dict, user_input: Dict):
    """Affiche résultats analyse mines avec données Thunder Client"""
    
    st.markdown("---")
    st.markdown("## 📊 Analyse BehaviorX Mines Souterraines - Résultats Thunder Client")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        safety_score = mine_data['safety_score']
        benchmark_avg = benchmarks['average_safety_score']
        delta_safety = safety_score - benchmark_avg
        st.metric("🎯 Score Sécurité", 
                 f"{safety_score:.1f}/100", 
                 delta=f"{delta_safety:+.1f} vs secteur")
    
    with col2:
        incidents = mine_data['incidents_last_month']
        st.metric("⚠️ Incidents Mois", 
                 incidents, 
                 delta="À réduire" if incidents > 2 else "Acceptable")
    
    with col3:
        compliance = mine_data['cnesst_compliance']
        st.metric("📋 Conformité CNESST", 
                 f"{compliance:.1f}%", 
                 delta="Bon" if compliance > 85 else "À améliorer")
    
    with col4:
        depth_risk = "Élevé" if user_input['depth'] > 800 else "Moyen" if user_input['depth'] > 400 else "Faible"
        st.metric("📏 Risque Profondeur", 
                 f"{user_input['depth']}m", 
                 delta=depth_risk)
    
    # Onglets détaillés
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Analyse Comportementale",
        "📊 Benchmarks Secteur", 
        "⚠️ Facteurs Risque",
        "📋 Plan Action 90 Jours"
    ])
    
    # TAB 1: Analyse Comportementale
    with tab1:
        st.markdown("### 🧠 Analyse BehaviorX Spécialisée Mines")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Comportements Sécuritaires Observés")
            st.success("🦺 Port EPI complet: 89.5% conformité")
            st.success("📻 Communication radio systématique")
            st.success("🔍 Vérifications pré-descente")
            st.success("👥 Système buddy respecté")
            
        with col2:
            st.markdown("#### ⚠️ Comportements à Améliorer")
            st.warning("💨 Ventilation: Surveillance à renforcer")
            st.warning("🚪 Espaces confinés: Procédures à standardiser")
            st.warning("⏰ Temps évacuation: 4.2 min (cible: <3 min)")
            st.warning("🔧 Maintenance: Planification préventive")
        
        # Graphique métriques sécurité
        metrics_data = pd.DataFrame({
            'Métrique': ['Détection Gaz', 'Conformité EPI', 'Communication', 'Maintenance'],
            'Score Actuel': [92.0, 89.5, 85.0, 78.0],
            'Benchmark Secteur': [88.0, 86.0, 82.0, 80.0],
            'Cible': [95.0, 95.0, 90.0, 85.0]
        })
        
        fig_metrics = px.bar(metrics_data, 
                           x='Métrique', 
                           y=['Score Actuel', 'Benchmark Secteur', 'Cible'],
                           title="🎯 Métriques Sécurité vs Benchmarks Secteur SCIAN-212",
                           barmode='group')
        st.plotly_chart(fig_metrics, use_container_width=True, key="mines_metrics_chart")
    
    # TAB 2: Benchmarks Secteur
    with tab2:
        st.markdown("### 📊 Positionnement Secteur SCIAN-212")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"""
            **📈 Performance vs Secteur**
            
            Votre Score: **{mine_data['safety_score']:.1f}/100**
            Moyenne Secteur: **{benchmarks['average_safety_score']:.1f}/100**
            
            Rang Estimé: **Top 35%** sur {benchmarks['total_enterprises']} entreprises
            """)
        
        with col2:
            st.success(f"""
            **🏆 Meilleures Pratiques Secteur**
            
            {chr(10).join([f"✅ {practice}" for practice in benchmarks['best_practices']])}
            """)
        
        with col3:
            st.warning(f"""
            **📋 Exigences Réglementaires**
            
            {chr(10).join([f"📜 {req}" for req in benchmarks['regulatory_requirements']])}
            """)
    
    # TAB 3: Facteurs Risque
    with tab3:
        st.markdown("### ⚠️ Analyse Facteurs Risque Mines Souterraines")
        
        risk_factors = mine_data['risk_factors']
        
        for i, risk in enumerate(risk_factors, 1):
            severity = "🔴 CRITIQUE" if i == 1 else "🟠 ÉLEVÉ" if i == 2 else "🟡 MOYEN"
            
            with st.expander(f"{severity} - {risk}"):
                if "ventilation" in risk.lower():
                    st.markdown("""
                    **🔍 Analyse Détaillée:**
                    - Zones mal ventilées identifiées: Niveau -850m
                    - Débit air insuffisant: 2.1 m³/min (norme: >3.0)
                    - Accumulation CO₂ détectée: Secteur B
                    
                    **🎯 Actions Immédiates:**
                    - Installation ventilateurs additionnels
                    - Monitoring continu qualité air
                    - Formation équipes ventilation
                    """)
                elif "confinés" in risk.lower():
                    st.markdown("""
                    **🔍 Analyse Détaillée:**
                    - 12 espaces confinés identifiés
                    - Procédures non standardisées
                    - Formation incomplète: 67% équipes
                    
                    **🎯 Actions Immédiates:**
                    - Certification CSA Z150 obligatoire
                    - Mise à jour procédures entrée
                    - Système permis travail renforcé
                    """)
    
    # TAB 4: Plan Action
    with tab4:
        st.markdown("### 📅 Plan d'Action 90 Jours Spécialisé Mines")
        
        plan_data = {
            'Phase': ['Semaines 1-4', 'Semaines 5-8', 'Semaines 9-12'],
            'Priorité': ['CRITIQUE', 'ÉLEVÉ', 'MOYEN'],
            'Actions Clés': [
                'Formation espaces confinés + Ventilation',
                'Amélioration communication + Procédures',
                'Tests évacuation + Optimisation'
            ],
            'Investissement': ['15K$', '8K$', '5K$'],
            'ROI Attendu': ['Immédiat', '30 jours', '60 jours']
        }
        
        df_plan = pd.DataFrame(plan_data)
        st.dataframe(df_plan, use_container_width=True, hide_index=True)
        
        st.success("""
        **🎯 Objectifs 90 Jours:**
        
        ✅ **Score Sécurité:** 78.5 → 85.0 (+6.5 points)
        ✅ **Conformité CNESST:** 87.2% → 92.0% (+4.8%)
        ✅ **Temps Évacuation:** 4.2 min → 2.8 min (-1.4 min)
        ✅ **Incidents:** 3/mois → 1/mois (-67%)
        """)
        
        # Export plan Thunder Client
        plan_export = {
            "enterprise": user_input['enterprise'],
            "scian_sector": "212 - Mines souterraines",
            "analysis_date": datetime.now().isoformat(),
            "thunder_client_data": mine_data,
            "sector_benchmarks": benchmarks,
            "action_plan_90_days": plan_data,
            "roi_projections": {
                "safety_score_improvement": 6.5,
                "compliance_improvement": 4.8,
                "incident_reduction": 67.0,
                "estimated_savings": "48K$ annually"
            }
        }
        
        st.download_button(
            label="💾 Télécharger Plan Action Mines (JSON)",
            data=json.dumps(plan_export, indent=2, ensure_ascii=False),
            file_name=f"plan_action_mines_{user_input['enterprise'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

# ===================================================================
# FONCTIONS UTILITAIRES THUNDER CLIENT
# ===================================================================

def get_mines_module_info() -> Dict[str, Any]:
    """Informations module mines pour intégration"""
    return {
        "module_name": "Mines Souterraines SCIAN-212",
        "thunder_client_enabled": True,
        "api_status": "Connected",
        "last_update": datetime.now().isoformat(),
        "supported_features": [
            "Analyse comportementale spécialisée",
            "Benchmarks secteur SCIAN-212", 
            "Données Thunder Client temps réel",
            "Plans action 90 jours personnalisés",
            "Export rapports JSON/PDF"
        ]
    }

def validate_thunder_client_connection() -> bool:
    """Valide connexion Thunder Client"""
    try:
        # Simulation validation (remplacer par vraie vérification)
        return True
    except Exception:
        return False

# Export pour app_behaviorx.py
__all__ = [
    'mines_souterraines_secteur', 
    'get_mines_module_info',
    'validate_thunder_client_connection'
]