# modules/storm_integration.py
"""
Module STORM Integration - SafetyGraph BehaviorX
Version: 1.0 - Modulaire et maintenable
Lignes: ~140 (respect limite 150)
"""

import streamlit as st
import sys
from pathlib import Path
import traceback
from typing import Dict, Any, Optional

class StormIntegrationManager:
    """Gestionnaire intégration STORM avec gestion d'erreurs robuste"""
    
    def __init__(self):
        self.storm_available = False
        self.storm_launcher = None
        self.research_manager = None
        self.error_log = []
        
    def initialize_storm(self) -> bool:
        """Initialise STORM avec gestion d'erreurs complète"""
        try:
            # Ajout chemin STORM
            storm_path = Path(__file__).parent.parent / "src" / "storm_research"
            if storm_path.exists():
                sys.path.insert(0, str(storm_path))
            
            # Import modules STORM
            from storm_launcher import STORMLauncher
            from research_topics import ResearchTopicsManager
            
            self.storm_launcher = STORMLauncher()
            self.research_manager = ResearchTopicsManager()
            self.storm_available = True
            
            return True
            
        except ImportError as e:
            self.error_log.append(f"Import STORM: {str(e)}")
            return False
        except Exception as e:
            self.error_log.append(f"Init STORM: {str(e)}")
            return False
    
    def get_storm_status(self) -> Dict[str, Any]:
        """Retourne statut détaillé STORM"""
        if not self.storm_available:
            return {
                "status": "INACTIF",
                "available": False,
                "errors": self.error_log,
                "topics_loaded": 0,
                "last_research": None
            }
        
        try:
            topics_count = len(self.research_manager.get_all_topics()) if self.research_manager else 0
            return {
                "status": "ACTIF",
                "available": True,
                "errors": [],
                "topics_loaded": topics_count,
                "last_research": "Récent"  # À améliorer avec vraie date
            }
        except:
            return {
                "status": "ERREUR",
                "available": False,
                "errors": ["Erreur lecture statut"],
                "topics_loaded": 0,
                "last_research": None
            }
    
    def launch_research(self, topic: str) -> Dict[str, Any]:
        """Lance recherche STORM sur un topic"""
        if not self.storm_available:
            return {"success": False, "error": "STORM non disponible"}
        
        try:
            result = self.storm_launcher.research_topic(topic)
            return {
                "success": True,
                "topic": topic,
                "sources_found": result.get("sources_count", 0),
                "insights": result.get("insights", []),
                "execution_time": result.get("duration", 0)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

def display_storm_interface():
    """Interface STORM pour SafetyGraph"""
    st.subheader("🌪️ STORM Research Integration")
    
    # Initialisation manager
    if 'storm_manager' not in st.session_state:
        st.session_state.storm_manager = StormIntegrationManager()
        st.session_state.storm_manager.initialize_storm()
    
    manager = st.session_state.storm_manager
    status = manager.get_storm_status()
    
    # Affichage statut
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if status["available"]:
            st.success(f"✅ STORM {status['status']}")
        else:
            st.error(f"❌ STORM {status['status']}")
    
    with col2:
        st.metric("Topics Chargés", status["topics_loaded"])
    
    with col3:
        st.info(f"Dernière recherche: {status['last_research'] or 'Jamais'}")
    
    # Interface recherche
    if status["available"]:
        st.markdown("### 🔍 Lancer Recherche STORM")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            topic = st.text_input(
                "Topic de recherche:", 
                placeholder="Ex: culture sécurité construction"
            )
        
        with col2:
            if st.button("🚀 Rechercher", type="primary"):
                if topic.strip():
                    with st.spinner("Recherche STORM en cours..."):
                        result = manager.launch_research(topic.strip())
                    
                    if result["success"]:
                        st.success(f"✅ Recherche terminée: {result['sources_found']} sources trouvées")
                        if result["insights"]:
                            st.markdown("**Insights:**")
                            for insight in result["insights"][:3]:  # Top 3
                                st.markdown(f"• {insight}")
                    else:
                        st.error(f"❌ Erreur: {result['error']}")
                else:
                    st.warning("⚠️ Veuillez saisir un topic de recherche")
    
    # Erreurs debug
    if status["errors"]:
        with st.expander("🔧 Debug - Erreurs détectées"):
            for error in status["errors"]:
                st.code(error)

def get_storm_module_info() -> Dict[str, Any]:
    """Informations module pour interface principale"""
    if 'storm_manager' not in st.session_state:
        return {
            "name": "STORM Research",
            "status": "NON_INIT",
            "icon": "🌪️",
            "available": False
        }
    
    manager = st.session_state.storm_manager
    status = manager.get_storm_status()
    
    return {
        "name": "STORM Research", 
        "status": status["status"],
        "icon": "🌪️",
        "available": status["available"],
        "topics_count": status["topics_loaded"]
    }

# Export pour app_behaviorx.py
__all__ = ['display_storm_interface', 'get_storm_module_info', 'StormIntegrationManager']