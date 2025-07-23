"""
SafetyGraph Design System
========================
Système design unifié pour expérience utilisateur optimisée
"""

import streamlit as st
from typing import Dict, List, Any

class SafetyDesignSystem:
    """Design system SafetyGraph avec thèmes adaptatifs"""
    
    # Palette couleurs par rôle utilisateur
    COLORS = {
        "employe_terrain": {
            "primary": "#2e7d32",      # Vert sécurité
            "secondary": "#66bb6a",    # Vert clair
            "accent": "#4caf50",       # Vert action
            "background": "#e8f5e8",   # Vert très clair
            "text": "#1b5e20"
        },
        "manager_sst": {
            "primary": "#1565c0",      # Bleu management
            "secondary": "#42a5f5",    # Bleu clair
            "accent": "#2196f3",       # Bleu action
            "background": "#e3f2fd",   # Bleu très clair
            "text": "#0d47a1"
        },
        "analyste_sst": {
            "primary": "#6a1b9a",      # Violet analyse
            "secondary": "#ab47bc",    # Violet clair
            "accent": "#9c27b0",       # Violet action
            "background": "#f3e5f5",   # Violet très clair
            "text": "#4a148c"
        },
        "direction": {
            "primary": "#d32f2f",      # Rouge executive
            "secondary": "#ef5350",    # Rouge clair
            "accent": "#f44336",       # Rouge action
            "background": "#ffebee",   # Rouge très clair
            "text": "#b71c1c"
        },
        "admin": {
            "primary": "#455a64",      # Gris admin
            "secondary": "#78909c",    # Gris clair
            "accent": "#607d8b",       # Gris action
            "background": "#eceff1",   # Gris très clair
            "text": "#263238"
        }
    }
    
    # États système universels
    STATUS_COLORS = {
        "success": "#4caf50",
        "warning": "#ff9800", 
        "error": "#f44336",
        "info": "#2196f3",
        "neutral": "#9e9e9e"
    }
    
    @staticmethod
    def apply_theme(user_role: str = "employe_terrain"):
        """Application thème selon rôle utilisateur"""
        theme = SafetyDesignSystem.COLORS.get(user_role, SafetyDesignSystem.COLORS["employe_terrain"])
        
        # CSS personnalisé pour Streamlit
        st.markdown(f"""
        <style>
        /* === THEME {user_role.upper()} === */
        
        /* Header principal */
        .main-header {{
            background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']});
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        /* Cartes métriques */
        .metric-card {{
            background: {theme['background']};
            border-left: 4px solid {theme['primary']};
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        /* Boutons d'action */
        .stButton > button {{
            background-color: {theme['primary']};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stButton > button:hover {{
            background-color: {theme['accent']};
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        /* Navigation sidebar */
        .css-1d391kg {{
            background-color: {theme['background']};
        }}
        
        /* Métriques Streamlit */
        div[data-testid="metric-container"] {{
            background-color: {theme['background']};
            border: 1px solid {theme['secondary']};
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid {theme['primary']};
        }}
        
        /* Alertes par statut */
        .alert-success {{
            background-color: {SafetyDesignSystem.STATUS_COLORS['success']}20;
            border-left: 4px solid {SafetyDesignSystem.STATUS_COLORS['success']};
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }}
        
        .alert-warning {{
            background-color: {SafetyDesignSystem.STATUS_COLORS['warning']}20;
            border-left: 4px solid {SafetyDesignSystem.STATUS_COLORS['warning']};
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }}
        
        .alert-error {{
            background-color: {SafetyDesignSystem.STATUS_COLORS['error']}20;
            border-left: 4px solid {SafetyDesignSystem.STATUS_COLORS['error']};
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }}
        
        /* Animations subtiles */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .css-1d391kg, .main-content {{
            animation: fadeIn 0.5s ease-out;
        }}
        
        /* Progress bars */
        .stProgress > div > div > div > div {{
            background-color: {theme['primary']};
        }}
        
        /* Badges gamification */
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.5rem;
            background: {theme['accent']};
            color: white;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header(title: str, subtitle: str = "", user_role: str = "employe_terrain"):
        """Rendu header principal avec thème"""
        theme = SafetyDesignSystem.COLORS.get(user_role, SafetyDesignSystem.COLORS["employe_terrain"])
        
        st.markdown(f"""
        <div class="main-header">
            <h1 style="margin: 0; font-size: 2.5rem;">🚀 {title}</h1>
            {f'<p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">{subtitle}</p>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_metric_card(title: str, value: str, delta: str = None, 
                          status: str = "neutral", help_text: str = ""):
        """Rendu carte métrique stylisée"""
        delta_html = ""
        if delta:
            delta_color = SafetyDesignSystem.STATUS_COLORS["success"] if "+" in delta else SafetyDesignSystem.STATUS_COLORS["error"]
            delta_html = f'<span style="color: {delta_color}; font-weight: 600;">{delta}</span>'
        
        help_html = f'<small style="opacity: 0.7;">{help_text}</small>' if help_text else ""
        
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin: 0; color: #333;">{title}</h4>
            <h2 style="margin: 0.5rem 0; color: #1a1a1a;">{value}</h2>
            {delta_html}
            {help_html}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_progress_with_animation(label: str, value: float, target: float = 1.0):
        """Barre progression avec animation"""
        progress = min(value / target, 1.0)
        percentage = int(progress * 100)
        
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 600;">{label}</span>
                <span style="font-weight: 600; color: #666;">{percentage}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(progress)
    
    @staticmethod
    def render_alert(message: str, alert_type: str = "info"):
        """Rendu alerte stylisée"""
        icons = {
            "success": "✅",
            "warning": "⚠️", 
            "error": "❌",
            "info": "💡"
        }
        
        icon = icons.get(alert_type, "💡")
        
        st.markdown(f"""
        <div class="alert-{alert_type}">
            {icon} <strong>{message}</strong>
        </div>
        """, unsafe_allow_html=True)

# Factory function pour création rapide
def apply_safety_theme(user_role: str = "employe_terrain"):
    """Application rapide thème SafetyGraph"""
    SafetyDesignSystem.apply_theme(user_role)

if __name__ == "__main__":
    print("✅ SafetyGraph Design System créé avec succès")
    print("🎨 5 thèmes utilisateur disponibles")
    print("📱 Responsive design intégré") 
    print("✨ Animations et micro-interactions incluses")
