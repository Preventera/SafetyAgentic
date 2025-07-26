"""
Module Sélecteur Profil UX/UI SafetyGraph
=============================================
Fonctions de gestion des profils utilisateurs adaptatifs
- Initialisation profils
- Sélecteur sidebar
- En-tête adaptatif
"""

import streamlit as st

def init_user_profile():
    """Initialisation du profil utilisateur pour UX adaptatif"""
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = 'hse_manager'  # Profil par défaut
    
    # Dictionnaire des profils avec métadonnées
    profiles = {
        'hse_manager': {
            'name': '👨‍💼 HSE Manager',
            'description': 'Stratégie, conformité, ROI',
            'color': '#1f77b4',  # Bleu executive
            'dashboard_type': 'executive'
        },
        'safety_coordinator': {
            'name': '⚡ Safety Coordinator', 
            'description': 'Opérations, incidents, équipes',
            'color': '#ff7f0e',  # Orange opérationnel
            'dashboard_type': 'operations'
        },
        'supervisor': {
            'name': '👷 Supervisor',
            'description': 'Terrain, actions rapides',
            'color': '#2ca02c',  # Vert terrain
            'dashboard_type': 'field'
        },
        'c_suite': {
            'name': '💼 C-Suite Executive',
            'description': 'Vision, benchmark, impact business',
            'color': '#9467bd',  # Violet premium
            'dashboard_type': 'boardroom'
        },
        'chercheur': {
            'name': '🔬 Chercheur SST',
            'description': 'Analyse, données, innovation',
            'color': '#17becf',  # Teal scientifique
            'dashboard_type': 'research'
        }
    }
    return profiles

def display_profile_selector():
    """Affichage sélecteur profil dans sidebar"""
    profiles = init_user_profile()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👤 **Profil Utilisateur**")
    
    # Sélecteur de profil
    profile_options = {key: profile['name'] for key, profile in profiles.items()}
    
    selected_profile = st.sidebar.selectbox(
        "Choisissez votre profil :",
        options=list(profile_options.keys()),
        format_func=lambda x: profile_options[x],
        index=list(profile_options.keys()).index(st.session_state.user_profile),
        key="profile_selector"
    )
    
    # Mise à jour session state
    if selected_profile != st.session_state.user_profile:
        st.session_state.user_profile = selected_profile
        st.rerun()
    
    # Affichage métadonnées profil sélectionné
    current_profile = profiles[st.session_state.user_profile]
    
    st.sidebar.markdown(f"""
    **📋 Profil Actuel :**  
    {current_profile['name']}
    
    **🎯 Focus :**  
    {current_profile['description']}
    
    **🎨 Mode Interface :**  
    {current_profile['dashboard_type'].title()}
    """)
    
    return current_profile

def display_adaptive_header(profile_data):
    """En-tête adaptatif selon profil utilisateur"""
    profile_color = profile_data['color']
    
    # CSS personnalisé selon profil
    st.markdown(f"""
    <style>
    .profile-header {{
        background: linear-gradient(90deg, {profile_color}22, {profile_color}11);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid {profile_color};
        margin-bottom: 1rem;
    }}
    .profile-badge {{
        background: {profile_color};
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête adaptatif
    st.markdown(f"""
    <div class="profile-header">
        <h2>🏭 SafetyGraph Industries + Culture SST</h2>
        <p>
            <span class="profile-badge">{profile_data['name']}</span>
            <span style="margin-left: 1rem; color: #666;">
                Powered by Safety Agentique | LangGraph Multi-Agent | STORM Research | Mémoire IA Adaptative
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)