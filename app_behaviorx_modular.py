# app_behaviorx_modular.py
"""
SafetyGraph BehaviorX - Interface Principale Modulaire
Version: 2.0 - Architecture modulaire maintenir 
Lignes: ~290 (respect limite 300)
"""

import streamlit as st
import sys
from pathlib import Path
from typing import Dict, Any
import traceback

# Configuration page
st.set_page_config(
    page_title="SafetyGraph BehaviorX",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ajout path modules - CORRECTION
import os
modules_path = os.path.join(os.getcwd(), "modules")
if os.path.exists(modules_path):
    sys.path.insert(0, modules_path)
    print(f"✅ Path modules ajouté: {modules_path}")  # Debug
else:
    print(f"❌ Dossier modules non trouvé: {modules_path}")  # Debug
class SafetyGraphModularApp:
    """Application SafetyGraph avec architecture modulaire"""
    
    def __init__(self):
        self.modules_status = {}
        self.initialize_modules()
    
    def initialize_modules(self):
        """Initialise tous les modules avec gestion d'erreurs"""
        
        # Module STORM
        try:
            from storm_integration import get_storm_module_info
            self.modules_status['storm'] = get_storm_module_info()
        except ImportError as e:
            self.modules_status['storm'] = {
                "name": "STORM Research", "status": "ERREUR", 
                "icon": "🌪️", "available": False, "error": str(e)
            }
        
        # Module Analytics Prédictifs
        try:
            from analytics_predictifs import get_analytics_predictifs_info
            self.modules_status['analytics'] = get_analytics_predictifs_info()
        except ImportError as e:
            self.modules_status['analytics'] = {
                "name": "Analytics Prédictifs", "status": "ERREUR",
                "icon": "📊", "available": False, "error": str(e)
            }
        
        # Module Pattern Recognition
        try:
            from pattern_recognition import get_pattern_recognition_info
            self.modules_status['patterns'] = get_pattern_recognition_info()
        except ImportError as e:
            self.modules_status['patterns'] = {
                "name": "Pattern Recognition", "status": "ERREUR",
                "icon": "🔍", "available": False, "error": str(e)
            }
        
        # Module Anomaly Detection
        try:
            from anomaly_detection import get_anomaly_detection_info
            self.modules_status['anomalies'] = get_anomaly_detection_info()
        except ImportError as e:
            self.modules_status['anomalies'] = {
                "name": "Anomaly Detection", "status": "ERREUR",
                "icon": "🚨", "available": False, "error": str(e)
            }
    
    def display_sidebar_status(self):
        """Affiche statut modules dans sidebar"""
        st.sidebar.markdown("## 🔧 Status Modules")
        
        for module_key, module_info in self.modules_status.items():
            status_icon = "✅" if module_info["available"] else "❌"
            st.sidebar.markdown(
                f"{status_icon} {module_info['icon']} {module_info['name']}: **{module_info['status']}**"
            )
            
            if not module_info["available"] and "error" in module_info:
                with st.sidebar.expander(f"🔧 Debug {module_info['name']}"):
                    st.code(module_info["error"])
        
        # Métriques globales
        total_modules = len(self.modules_status)
        active_modules = sum(1 for m in self.modules_status.values() if m["available"])
        
        st.sidebar.markdown("---")
        st.sidebar.metric("Modules Actifs", f"{active_modules}/{total_modules}")
    
    def display_header(self):
        """Header principal application"""
        st.markdown("# 🎯 SafetyGraph BehaviorX - Modulaire")
        st.markdown("## 🚀 Powered by Safety Agentique | 🌐 LangGraph Multi-Agent | 🌪️ STORM Research | 🧠 Mémoire IA Adaptive")
        st.markdown("---")
    
    def display_main_interface(self):
        """Interface principale avec onglets"""
        
        # Onglets principaux
        tabs = st.tabs([
            "🎯 BehaviorX Standard",
            "📊 Cartographie Culture", 
            "📈 Analytics Prédictifs",
            "🔍 Pattern Recognition",
            "🚨 Anomaly Detection",
            "🌪️ STORM Research"
        ])
        
        # Tab 1: BehaviorX Standard
        with tabs[0]:
            self.display_behaviorx_standard()
        
        # Tab 2: Cartographie Culture  
        with tabs[1]:
            self.display_cartographie_culture()
        
        # Tab 3: Analytics Prédictifs
        with tabs[2]:
            if self.modules_status['analytics']['available']:
                try:
                    from analytics_predictifs import display_analytics_predictifs_interface
                    display_analytics_predictifs_interface()
                except Exception as e:
                    st.error(f"Erreur module Analytics: {e}")
            else:
                st.error("❌ Module Analytics Prédictifs non disponible")
        
        # Tab 4: Pattern Recognition
        with tabs[3]:
            if self.modules_status['patterns']['available']:
                try:
                    from pattern_recognition import display_pattern_recognition_interface
                    display_pattern_recognition_interface()
                except Exception as e:
                    st.error(f"Erreur module Patterns: {e}")
            else:
                st.error("❌ Module Pattern Recognition non disponible")
        
        # Tab 5: Anomaly Detection
        with tabs[4]:
            if self.modules_status['anomalies']['available']:
                try:
                    from anomaly_detection import display_anomaly_detection_interface
                    display_anomaly_detection_interface()
                except Exception as e:
                    st.error(f"Erreur module Anomalies: {e}")
            else:
                st.error("❌ Module Anomaly Detection non disponible")
        
        # Tab 6: STORM Research
        with tabs[5]:
            if self.modules_status['storm']['available']:
                try:
                    from storm_integration import display_storm_interface
                    display_storm_interface()
                except Exception as e:
                    st.error(f"Erreur module STORM: {e}")
            else:
                st.error("❌ Module STORM Research non disponible")
    
    def display_behaviorx_standard(self):
        """Interface BehaviorX Standard simplifiée"""
        st.subheader("🎯 BehaviorX Standard - Workflow Principal")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📋 Sélection Workflow")
            workflow = st.selectbox(
                "Choisir le workflow:",
                ["VCS + ABC Standard", "ABC Seul", "VCS Seul", "Workflow Complet"],
                index=0
            )
        
        with col2:
            if st.button("🚀 Lancer BehaviorX", type="primary", use_container_width=True):
                with st.spinner("Traitement BehaviorX..."):
                    st.session_state.workflow_results = {
                        "workflow": workflow,
                        "status": "Terminé",
                        "score_culture": 4.2,
                        "recommendations": [
                            "Renforcer formation leadership",
                            "Améliorer communication équipes",
                            "Optimiser processus sécurité"
                        ]
                    }
        
        # Affichage résultats
        if 'workflow_results' in st.session_state:
            results = st.session_state.workflow_results
            
            st.success(f"✅ Workflow {results['workflow']} - {results['status']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Score Culture", f"{results['score_culture']}/5", "+0.3")
            with col2:
                st.metric("Améliorations", len(results['recommendations']))
            
            st.markdown("**Recommandations:**")
            for rec in results['recommendations']:
                st.markdown(f"• {rec}")
    
    def display_cartographie_culture(self):
        """Interface Cartographie Culture simplifiée"""
        st.subheader("🗺️ Cartographie Culture SST")
        
        if st.button("📊 Lancer Cartographie Culture SST", type="primary"):
            with st.spinner("Génération cartographie..."):
                # Simulation données sectorielles
                data = {
                    "Secteur SCIAN": ["Construction (236)", "Manufacturier (311-333)", "Transport (484-488)", "Services (541)"],
                    "Score Culture": [3.8, 4.2, 3.6, 4.0],
                    "Niveau Maturité": ["Réactif", "Proactif", "Réactif", "Proactif"],
                    "Risque Incident (%)": [15.2, 8.7, 12.3, 6.9]
                }
                
                st.session_state.cartographie_results = data
        
        if 'cartographie_results' in st.session_state:
            st.success("🎉 Cartographie Culture SST lancée avec succès !")
            
            import pandas as pd
            df = pd.DataFrame(st.session_state.cartographie_results)
            st.dataframe(df, use_container_width=True)

def main():
    """Point d'entrée principal"""
    
    # Initialisation application
    if 'safety_app' not in st.session_state:
        st.session_state.safety_app = SafetyGraphModularApp()
    
    app = st.session_state.safety_app
    
    # Affichage interface
    app.display_header()
    app.display_sidebar_status()
    app.display_main_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("**SafetyGraph BehaviorX v2.0** - Architecture Modulaire | Développé par GenAISafety")

if __name__ == "__main__":
    main()