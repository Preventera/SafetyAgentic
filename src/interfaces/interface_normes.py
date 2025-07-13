#!/usr/bin/env python3
"""
Interface Normes & Conformité - Module Séparé SafetyGraph
========================================================
Module d'interface pour recherche normative ISO/SCIAN
Mario Genest - Safety Agentique - 12 juillet 2025

🎯 Utilisation simple dans app_behaviorx.py :
   from src.interfaces.interface_normes import render_normes_tab, init_normes_sidebar
"""

import streamlit as st
from typing import Dict, List, Optional

try:
    from src.normes.vectorisation_normes import (
        initialiser_moteur_vectorisation, 
        rechercher_normes_applicables,
        obtenir_statistiques_corpus
    )
    NORMES_AVAILABLE = True
except ImportError:
    NORMES_AVAILABLE = False
    
    # Fonctions fallback
    def initialiser_moteur_vectorisation(): return None
    def rechercher_normes_applicables(moteur, contexte, secteur=None): return []
    def obtenir_statistiques_corpus(moteur): return {}

# ═══════════════════════════════════════════════════════════════
# INTERFACE SIDEBAR NORMES
# ═══════════════════════════════════════════════════════════════

def init_normes_sidebar():
    """Initialise la section normes dans la sidebar"""
    
    if NORMES_AVAILABLE:
        st.sidebar.success("📋 Normes ISO/SCIAN ✅")
        
        # Initialisation moteur (une seule fois)
        if 'moteur_normes' not in st.session_state:
            with st.spinner("🔄 Initialisation corpus normatif..."):  # CORRECTION ICI !
                try:
                    st.session_state.moteur_normes = initialiser_moteur_vectorisation()
                    st.sidebar.success("✅ Corpus normatif chargé")
                except Exception as e:
                    st.sidebar.error(f"❌ Erreur chargement: {e}")
                    st.session_state.moteur_normes = None
        
        # Statistiques corpus
        if st.session_state.get('moteur_normes'):
            stats = obtenir_statistiques_corpus(st.session_state.moteur_normes)
            st.sidebar.caption(f"📊 {stats.get('total_elements', 0)} normes • {stats.get('elements_iso', 0)} ISO • {stats.get('elements_scian', 0)} SCIAN")
        
        return True
    else:
        st.sidebar.error("📋 Normes ISO/SCIAN ❌")
        st.sidebar.caption("Module vectorisation non disponible")
        return False

# ═══════════════════════════════════════════════════════════════
# INTERFACE ONGLET NORMES COMPLET
# ═══════════════════════════════════════════════════════════════

def render_normes_tab():
    """Rend l'onglet Normes & Conformité complet"""
    
    if not NORMES_AVAILABLE:
        render_normes_unavailable()
        return
    
    if not st.session_state.get('moteur_normes'):
        render_normes_loading()
        return
    
    # Interface principale
    st.header("📋 Recherche Normes & Conformité ISO/SCIAN")
    
    # Section recherche
    render_search_interface()
    
    # Section statistiques
    render_stats_section()

def render_normes_unavailable():
    """Interface quand module normes non disponible"""
    st.error("❌ Module Normes & Conformité Non Disponible")
    
    st.info("""
    **💡 Pour activer la recherche normative :**
    
    1. Vérifiez que le module `src/normes/vectorisation_normes.py` existe
    2. Installez les dépendances Python requises
    3. Relancez l'application SafetyGraph
    """)
    
    # Interface dégradée avec informations statiques
    st.subheader("📚 Normes de Référence (Mode Statique)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🌍 ISO 45001:2018**")
        st.write("• Système management SST")
        st.write("• Leadership et participation")
        st.write("• Planification des risques")
        st.write("• Amélioration continue")
    
    with col2:
        st.write("**🇨🇦 Normes CSA**")
        st.write("• Z1000 - Management SST")
        st.write("• Z1002 - Exigences système")
        st.write("• Z1003 - Risques psychosociaux")
        st.write("• Z45001 - Santé psychologique")

def render_normes_loading():
    """Interface pendant chargement"""
    st.warning("⏳ Corpus normatif en cours d'initialisation...")
    
    if st.button("🔄 Réinitialiser Corpus"):
        if 'moteur_normes' in st.session_state:
            del st.session_state.moteur_normes
        st.rerun()

def render_search_interface():
    """Interface de recherche normative"""
    
    # Formulaire de recherche
    with st.form("recherche_normes"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            contexte_recherche = st.text_area(
                "🔍 Contexte d'analyse HSE",
                placeholder="Ex: formation sécurité construction, troubles musculosquelettiques, audit interne...",
                height=100,
                help="Décrivez votre situation HSE pour obtenir les normes applicables"
            )
        
        with col2:
            secteur_force = st.selectbox(
                "🏭 Secteur SCIAN",
                [
                    "Auto-détection",
                    "236 - Construction", 
                    "311-333 - Fabrication", 
                    "621 - Santé", 
                    "722 - Restauration", 
                    "484 - Transport", 
                    "541 - Services"
                ],
                help="Forcer un secteur spécifique ou laisser auto-détection"
            )
            
            recherche_avancee = st.checkbox("🎯 Recherche avancée", help="Options supplémentaires")
        
        # Options avancées
        if recherche_avancee:
            col_adv1, col_adv2 = st.columns(2)
            with col_adv1:
                priorite_min = st.slider("Priorité minimale", 1, 5, 2)
            with col_adv2:
                score_min = st.slider("Score pertinence min", 0.0, 1.0, 0.3, 0.1)
        else:
            priorite_min = 1
            score_min = 0.3
        
        # Bouton recherche
        rechercher = st.form_submit_button("🔍 Rechercher Normes Applicables", type="primary")
    
    # Traitement recherche
    if rechercher and contexte_recherche.strip():
        process_search_request(contexte_recherche, secteur_force, priorite_min, score_min)
    elif rechercher:
        st.error("❌ Veuillez saisir un contexte d'analyse")

def process_search_request(contexte: str, secteur_force: str, priorite_min: int, score_min: float):
    """Traite la demande de recherche"""
    
    # Préparation paramètres
    secteur_code = None
    if secteur_force != "Auto-détection":
        secteur_code = secteur_force.split(" - ")[0]
    
    # Recherche
    with st.spinner("🔄 Recherche dans corpus normatif..."):
        try:
            recommandations = rechercher_normes_applicables(
                st.session_state.moteur_normes, 
                contexte, 
                secteur_code
            )
            
            # Filtrage selon critères avancés
            recommandations_filtrees = [
                r for r in recommandations 
                if r['niveau_priorite'] >= priorite_min and r['conformite_score'] >= score_min
            ]
            
        except Exception as e:
            st.error(f"❌ Erreur recherche: {e}")
            return
    
    # Affichage résultats
    render_search_results(recommandations_filtrees, contexte, secteur_code)

def render_search_results(recommandations: List[Dict], contexte: str, secteur: Optional[str]):
    """Affiche les résultats de recherche"""
    
    if not recommandations:
        st.warning("⚠️ Aucune recommandation trouvée pour ce contexte")
        st.info("""
        **💡 Suggestions pour améliorer la recherche :**
        • Utilisez des mots-clés HSE spécifiques (formation, risque, sécurité...)
        • Précisez le secteur d'activité
        • Réduisez le score de pertinence minimum
        """)
        return
    
    # Métriques résultats
    st.success(f"✅ **{len(recommandations)} recommandations** trouvées pour : *{contexte}*")
    
    if secteur:
        st.info(f"🏭 Secteur spécialisé : {secteur}")
    
    # Onglets résultats
    tab_liste, tab_priorite, tab_export = st.tabs(["📋 Liste complète", "⭐ Par priorité", "📤 Export"])
    
    with tab_liste:
        render_recommendations_list(recommandations)
    
    with tab_priorite:
        render_recommendations_by_priority(recommandations)
    
    with tab_export:
        render_export_options(recommandations, contexte)

def render_recommendations_list(recommandations: List[Dict]):
    """Affiche la liste complète des recommandations"""
    
    for i, rec in enumerate(recommandations, 1):
        priorite_emoji = "🔴" if rec['niveau_priorite'] >= 4 else "🟡" if rec['niveau_priorite'] >= 3 else "🟢"
        
        with st.expander(f"{priorite_emoji} **{i}. {rec['titre']}** (Pertinence: {rec['conformite_score']:.1%})"):
            
            # Infos principales
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.write(f"**📚 Source :** {rec['norme_source']}")
                st.write(f"**🎯 Section ISO :** {rec['section_iso']}")
                st.write(f"**⭐ Priorité :** {rec['niveau_priorite']}/5")
            
            with col_info2:
                st.write(f"**🏭 Secteur :** {rec['secteur_scian']}")
                st.write(f"**📊 Score :** {rec['conformite_score']:.2f}")
            
            # Description
            st.write(f"**📖 Description :** {rec['description']}")
            
            # Actions concrètes
            if rec['actions_concretes']:
                st.write("**🔧 Actions concrètes à implémenter :**")
                for j, action in enumerate(rec['actions_concretes'], 1):
                    st.write(f"   {j}. {action}")
            
            # Références
            if rec['references']:
                st.write(f"**📖 Références :** {' • '.join(rec['references'])}")

def render_recommendations_by_priority(recommandations: List[Dict]):
    """Affiche les recommandations regroupées par priorité"""
    
    # Regroupement par priorité
    by_priority = {}
    for rec in recommandations:
        prio = rec['niveau_priorite']
        if prio not in by_priority:
            by_priority[prio] = []
        by_priority[prio].append(rec)
    
    # Affichage par priorité décroissante
    for priorite in sorted(by_priority.keys(), reverse=True):
        recs = by_priority[priorite]
        priorite_label = {5: "🔴 CRITIQUE", 4: "🟠 ÉLEVÉE", 3: "🟡 MOYENNE", 2: "🟢 FAIBLE", 1: "⚫ OPTIONNELLE"}
        
        st.subheader(f"Priorité {priorite}/5 - {priorite_label.get(priorite, '❓')} ({len(recs)} éléments)")
        
        for rec in recs:
            st.write(f"• **{rec['titre']}** ({rec['norme_source']}) - Score: {rec['conformite_score']:.1%}")

def render_export_options(recommandations: List[Dict], contexte: str):
    """Options d'export des recommandations"""
    
    st.subheader("📤 Export des Recommandations")
    
    # Préparation données export
    import pandas as pd
    import json
    from datetime import datetime
    
    df_export = pd.DataFrame([
        {
            'Titre': rec['titre'],
            'Source': rec['norme_source'],
            'Section_ISO': rec['section_iso'],
            'Secteur_SCIAN': rec['secteur_scian'],
            'Priorité': rec['niveau_priorite'],
            'Score_Pertinence': rec['conformite_score'],
            'Description': rec['description'],
            'Actions': ' | '.join(rec['actions_concretes']),
            'Références': ' | '.join(rec['references'])
        }
        for rec in recommandations
    ])
    
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    
    with col_exp1:
        # Export CSV
        csv_data = df_export.to_csv(index=False)
        st.download_button(
            "📊 Télécharger CSV",
            csv_data,
            f"normes_recommandations_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            "text/csv"
        )
    
    with col_exp2:
        # Export JSON
        json_data = json.dumps(recommandations, indent=2, ensure_ascii=False)
        st.download_button(
            "🔗 Télécharger JSON",
            json_data,
            f"normes_recommandations_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            "application/json"
        )
    
    with col_exp3:
        # Rapport texte
        rapport = generer_rapport_texte(recommandations, contexte)
        st.download_button(
            "📄 Rapport Texte",
            rapport,
            f"rapport_normes_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            "text/plain"
        )

def generer_rapport_texte(recommandations: List[Dict], contexte: str) -> str:
    """Génère un rapport texte des recommandations"""
    
    from datetime import datetime
    
    rapport = f"""
RAPPORT CONFORMITÉ NORMATIVE - SAFETYGRAPH
==========================================
Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Contexte analysé: {contexte}
Nombre de recommandations: {len(recommandations)}

"""
    
    for i, rec in enumerate(recommandations, 1):
        rapport += f"""
{i}. {rec['titre']}
{'-' * len(rec['titre'])}
Source: {rec['norme_source']}
Section ISO: {rec['section_iso']}
Secteur SCIAN: {rec['secteur_scian']}
Priorité: {rec['niveau_priorite']}/5
Score de pertinence: {rec['conformite_score']:.1%}

Description:
{rec['description']}

Actions concrètes:
"""
        for j, action in enumerate(rec['actions_concretes'], 1):
            rapport += f"  {j}. {action}\n"
        
        rapport += f"\nRéférences: {', '.join(rec['references'])}\n\n"
    
    return rapport

def render_stats_section():
    """Section statistiques du corpus"""
    
    with st.expander("📊 Statistiques Corpus Normatif"):
        if st.session_state.get('moteur_normes'):
            stats = obtenir_statistiques_corpus(st.session_state.moteur_normes)
            
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            
            with col_stat1:
                st.metric("📋 Total éléments", stats.get('total_elements', 0))
            
            with col_stat2:
                st.metric("🌍 Sections ISO", stats.get('elements_iso', 0))
            
            with col_stat3:
                st.metric("🏭 Risques SCIAN", stats.get('elements_scian', 0))
            
            with col_stat4:
                st.metric("🇨🇦 Normes CSA", stats.get('elements_csa', 0))
            
            st.write(f"**🔍 Mots-clés indexés :** {stats.get('mots_cles_indexes', 0)}")
            st.write(f"**🏭 Secteurs SCIAN couverts :** {stats.get('secteurs_scian_couverts', 0)}")

# ═══════════════════════════════════════════════════════════════
# FONCTION D'ENRICHISSEMENT BEHAVIORX
# ═══════════════════════════════════════════════════════════════

def enrichir_behaviorx_normes(user_input: str, secteur_scian: Optional[str] = None) -> Optional[Dict]:
    """Enrichit les résultats BehaviorX avec recommandations normatives"""
    
    if not NORMES_AVAILABLE or not st.session_state.get('moteur_normes'):
        return None
    
    try:
        normes_applicables = rechercher_normes_applicables(
            st.session_state.moteur_normes,
            user_input,
            secteur_scian
        )
        
        # Top 3 plus pertinentes
        top_normes = normes_applicables[:3]
        
        if top_normes:
            return {
                'normes_trouvees': len(normes_applicables),
                'top_recommandations': top_normes,
                'moyenne_pertinence': sum(r['conformite_score'] for r in top_normes) / len(top_normes)
            }
    
    except Exception as e:
        st.error(f"Erreur enrichissement normes: {e}")
    
    return None

def render_enrichissement_behaviorx(enrichissement: Dict):
    """Affiche l'enrichissement normatif dans BehaviorX"""
    
    if not enrichissement:
        return
    
    st.subheader("📋 Conformité Normative Recommandée")
    
    st.info(f"🎯 **{enrichissement['normes_trouvees']} normes applicables** trouvées (Pertinence moyenne: {enrichissement['moyenne_pertinence']:.1%})")
    
    for i, rec in enumerate(enrichissement['top_recommandations'], 1):
        priorite_emoji = "🔴" if rec['niveau_priorite'] >= 4 else "🟡" if rec['niveau_priorite'] >= 3 else "🟢"
        
        st.write(f"{priorite_emoji} **{i}. {rec['norme_source']}** - {rec['titre']} (Pertinence: {rec['conformite_score']:.1%})")
        
        if rec['actions_concretes']:
            st.write(f"   💡 Action prioritaire: {rec['actions_concretes'][0]}")