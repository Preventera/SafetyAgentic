# test_thunder_streamlit.py
import streamlit as st
import sys
import os

# Ajouter le répertoire racine au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration Streamlit
st.set_page_config(
    page_title="🚀 Test Thunder Client SafetyGraph",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🚀 Test Thunder Client - SafetyGraph Integration")
st.markdown("---")

# Test d'import du module
try:
    from src.api.thunder_integration import ThunderClientIntegration, add_thunder_client_tab
    
    # Message de succès
    st.success("✅ Module Thunder Client chargé avec succès !")
    
    # Affichage des statistiques dans la sidebar
    with st.sidebar:
        st.header("📊 Thunder Client Status")
        
        # Initialisation
        thunder = ThunderClientIntegration()
        stats = thunder.get_statistics()
        
        # Métriques
        st.metric("🗂️ Collections", stats['collections_count'])
        st.metric("📋 Total Requêtes", stats['total_requests'])
        st.text(f"🕐 Dernière MAJ: {stats['last_loaded']}")
        
        # Détails collections
        if stats['collections_count'] > 0:
            st.subheader("📁 Collections Détaillées")
            for i, collection_name in enumerate(stats['collections_names'], 1):
                # Nettoie le nom pour affichage
                display_name = collection_name.replace('thunder-collection_postman_', '')
                requests = thunder.get_collection_requests(collection_name)
                
                with st.expander(f"{i}. {display_name}"):
                    st.write(f"**Requêtes:** {len(requests)}")
                    if requests:
                        for req in requests:
                            st.write(f"• {req}")
                    else:
                        st.write("_Aucune requête détectée_")
        else:
            st.error("❌ Aucune collection trouvée")
    
    # Interface principale Thunder Client
    st.header("🎯 Interface Thunder Client")
    
    # Utilisation de l'interface complète
    add_thunder_client_tab()
    
except ImportError as e:
    st.error(f"❌ **Erreur d'import:** {e}")
    st.info("💡 **Solution:** Vérifiez que le fichier `src/api/thunder_integration.py` existe")
    
    # Affichage du chemin pour debug
    with st.expander("🔍 Debug Info"):
        st.write("**Répertoire de travail:**", os.getcwd())
        st.write("**Python Path:**", sys.path)
        
except Exception as e:
    st.error(f"❌ **Erreur générale:** {e}")
    
    # Debug détaillé
    with st.expander("🐛 Debug Détaillé"):
        import traceback
        st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown("**🛡️ SafetyGraph Thunder Client Integration** | Développé pour la protection des fonctionnalités HSE")