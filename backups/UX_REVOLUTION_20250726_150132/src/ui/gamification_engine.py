"""
SafetyGraph Gamification Engine
==============================
Système gamification pour engagement terrain +200%
"""

import streamlit as st
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta

class SafetyGamificationEngine:
    """Moteur gamification SafetyGraph"""
    
    # Système progression
    LEVELS = {
        1: {"name": "🌱 Apprenti Sécurité", "threshold": 0, "color": "#81c784"},
        2: {"name": "🔍 Observateur", "threshold": 50, "color": "#66bb6a"}, 
        3: {"name": "🎯 Expert Terrain", "threshold": 150, "color": "#4caf50"},
        4: {"name": "🛡️ Gardien Sécurité", "threshold": 300, "color": "#388e3c"},
        5: {"name": "🌟 Maître SafetyGraph", "threshold": 500, "color": "#2e7d32"}
    }
    
    # Badges système
    BADGES = {
        "premier_pas": {"icon": "🚀", "name": "Premier Pas", "desc": "Première observation"},
        "oeil_lynx": {"icon": "👀", "name": "Œil de Lynx", "desc": "10 observations en 1 semaine"},
        "flash_reporter": {"icon": "⚡", "name": "Flash Reporter", "desc": "Signalement <2min"},
        "mentor": {"icon": "🎓", "name": "Mentor", "desc": "Formation d'un collègue"},
        "innovateur": {"icon": "💡", "name": "Innovateur", "desc": "Suggestion adoptée"},
        "zero_incident": {"icon": "🏆", "name": "Zéro Incident", "desc": "Équipe 0 incident 3 mois"}
    }
    
    @staticmethod
    def calculate_user_level(total_points: int):
        """Calcul niveau utilisateur selon points"""
        current_level = 1
        for level, info in SafetyGamificationEngine.LEVELS.items():
            if total_points >= info['threshold']:
                current_level = level
        return current_level, SafetyGamificationEngine.LEVELS[current_level]
    
    @staticmethod
    def render_gamification_sidebar():
        """Rendu sidebar gamification"""
        with st.sidebar:
            st.markdown("### 🎮 Votre Progression")
            
            # Simulation données utilisateur
            user_points = st.session_state.get('user_points', 127)
            
            # Niveau actuel
            level, level_info = SafetyGamificationEngine.calculate_user_level(user_points)
            
            # Affichage niveau
            st.markdown(f"**{level_info['name']}**")
            st.caption(f"Niveau {level}")
            
            # Points totaux
            st.metric("⭐ Points Totaux", f"{user_points:,}", "+12 aujourd'hui")
            
            # Badges récents
            st.markdown("#### 🏆 Badges Récents")
            st.markdown("🚀 **Premier Pas** - Récent")
            st.markdown("👀 **Œil de Lynx** - Cette semaine")
            
            # Défi du jour
            st.markdown("#### 🎯 Défi du Jour")
            st.info("🎪 **Complétez 10 observations cette semaine**")
            st.progress(0.8)
            st.caption("Récompense: +50 points | 8/10 complété")

if __name__ == "__main__":
    print("✅ SafetyGraph Gamification Engine créé")
    print("🎮 5 niveaux progression")
    print("🏆 6 badges système")
    print("⭐ Système points contextuel")
