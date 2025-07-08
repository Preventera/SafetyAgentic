"""
Script pour intégrer automatiquement la mémoire IA dans app.py
"""

import re

def integrate_memory_into_app():
    # Lire le fichier actuel
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Code à ajouter en haut (après les imports existants)
    memory_import = """
# === INTÉGRATION MÉMOIRE IA MEM0 ===
try:
    from safegraph_memory_integration import (
        integrate_memory_into_safegraph,
        enhance_analysis_with_memory,
        render_memory_enhanced_results,
        MEMORY_AVAILABLE
    )
    print("✅ Mémoire IA Mem0 intégrée dans SafeGraph")
except ImportError as e:
    print(f"⚠️ Mémoire IA non disponible: {e}")
    MEMORY_AVAILABLE = False
    
    # Fonctions fallback
    def integrate_memory_into_safegraph():
        return {"memory_available": False}
    
    def enhance_analysis_with_memory(text, company, secteur="236"):
        return {"error": "Mémoire non disponible", "standard_mode": True}
    
    def render_memory_enhanced_results(result):
        st.warning("⚠️ Résultats en mode standard")

"""
    
    # Trouver où insérer (après les imports)
    import_pattern = r"(import streamlit as st.*?\n)"
    if re.search(import_pattern, content):
        content = re.sub(import_pattern, r"\1" + memory_import, content)
    else:
        # Si pas trouvé, ajouter au début après la première ligne
        lines = content.split('\n')
        lines.insert(1, memory_import)
        content = '\n'.join(lines)
    
    # Code à ajouter dans la fonction principale
    sidebar_integration = """
    # === INTÉGRATION SIDEBAR MÉMOIRE ===
    if MEMORY_AVAILABLE:
        memory_config = integrate_memory_into_safegraph()
    else:
        memory_config = {"memory_available": False}
    """
    
    # Chercher la fonction main ou le début de l'interface
    if "def main():" in content:
        content = content.replace("def main():", f"def main():\n{sidebar_integration}")
    elif "st.title" in content:
        title_pattern = r"(st\.title\([^)]+\))"
        content = re.sub(title_pattern, f"{sidebar_integration}\n    \\1", content)
    
    # Sauvegarder le fichier modifié
    with open("app_with_memory.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ Fichier app_with_memory.py créé avec intégration mémoire")
    return True

if __name__ == "__main__":
    integrate_memory_into_app()
