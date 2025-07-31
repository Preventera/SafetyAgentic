"""
Dashboard HSE Manager - SafetyGraph Industries
==============================================
Interface executive spécialisée pour HSE Managers
Version 4.0 - ULTRA ENRICHIE + Restauration Exacte Originale
Basée sur les spécifications exactes + Enrichissements massifs
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import json

def display_hse_manager_dashboard(config):
    """Dashboard HSE Manager Executive - Excellence Mondiale ULTRA COMPLET"""
    
    # Header Executive Premium avec gradient sophistiqué ENRICHI
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 70%, #ff6b6b 100%); 
                padding: 3rem; border-radius: 25px; margin-bottom: 2rem; 
                box-shadow: 0 20px 60px rgba(0,0,0,0.2); position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; 
                    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>'); opacity: 0.3;"></div>
        <h1 style="color: white; text-align: center; margin: 0; font-size: 3.5rem; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); position: relative; z-index: 1;">
            🎯 HSE Manager Executive Dashboard
        </h1>
        <p style="color: #e2e8f0; text-align: center; margin: 1rem 0 0 0; font-size: 1.6rem; position: relative; z-index: 1; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
            🎯 Stratégie • 💰 ROI • 📊 BBS-ISO 45001 • 🏆 Excellence Mondiale • 🚀 Innovation
        </p>
        <div style="text-align: center; margin-top: 1rem; position: relative; z-index: 1;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; color: white; font-size: 1rem;">
                ⚡ Temps Réel • 🔄 Synchronisé • 🛡️ Sécurisé • 🌐 Multi-Sites
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # NOUVELLE SECTION : Alertes Temps Réel Executive
    st.markdown("### 🚨 Alertes Executive Temps Réel")
    
    alert_col1, alert_col2, alert_col3 = st.columns(3)
    
    with alert_col1:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #ef4444, #dc2626); padding: 1rem; border-radius: 10px; color: white;">
            <h5 style="margin: 0;">🔥 CRITIQUE</h5>
            <p style="margin: 0.5rem 0 0 0;">Site Nord - Non-conformité Ch.6<br>
            <small>⏰ Il y a 23 min • Action requise</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with alert_col2:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #f59e0b, #d97706); padding: 1rem; border-radius: 10px; color: white;">
            <h5 style="margin: 0;">⚠️ ATTENTION</h5>
            <p style="margin: 0.5rem 0 0 0;">Formation EPI retardée<br>
            <small>⏰ Il y a 1h12 • 12 employés</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with alert_col3:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #10b981, #059669); padding: 1rem; border-radius: 10px; color: white;">
            <h5 style="margin: 0;">✅ SUCCÈS</h5>
            <p style="margin: 0.5rem 0 0 0;">Audit ISO réussi Site Est<br>
            <small>⏰ Il y a 2h • Certification validée</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Executive KPIs - 6 Métriques Clés ENRICHIES (au lieu de 5)
    st.markdown("### 🏆 Executive KPIs - Performance Stratégique Enrichie")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric(
            "🎯 HSE Score Global", 
            "87.3%", 
            delta="↗ +3.2%",
            help="Performance HSE consolidée multisite"
        )
        
    with col2:
        st.metric(
            "💰 ROI Total Int. ⚡", 
            "420%", 
            delta="↗ +78%",
            help="ROI intégré SafetyGraph + BBS + ISO"
        )
        
    with col3:
        st.metric(
            "📊 Excellence BBS-ISO", 
            "96.7%", 
            delta="↗ +4.3%",
            help="Performance intégrée BBS + ISO 45001"
        )
        
    with col4:
        st.metric(
            "✅ Conformité ISO 45001", 
            "96.7%", 
            delta="↗ +2.4%",
            help="Conformité chapitres ISO 45001"
        )
    
    with col5:
        st.metric(
            "🏆 Benchmark Mondial", 
            "Top 1%", 
            delta="↗ +14 positions",
            help="Position mondiale excellence HSE"
        )
    
    with col6:
        st.metric(
            "🚀 Innovation Index", 
            "94.8%", 
            delta="↗ +12.5%",
            help="Index innovation technologique HSE"
        )
    
    # NOUVELLE SECTION : Métriques Temps Réel Avancées
    st.markdown("### ⚡ Métriques Temps Réel Avancées")
    
    real_time_col1, real_time_col2, real_time_col3, real_time_col4 = st.columns(4)
    
    with real_time_col1:
        st.metric("👥 Employés Actifs", "1,247", delta="+23 vs hier")
        st.metric("🔄 Observations/h", "18.5", delta="+2.3")
    
    with real_time_col2:
        st.metric("📱 App Mobile Usage", "89.4%", delta="+5.7%")
        st.metric("🎯 Coaching Sessions", "156", delta="+34")
    
    with real_time_col3:
        st.metric("🛡️ Interventions Préventives", "67", delta="+12")
        st.metric("📊 Rapports Générés", "89", delta="+18")
    
    with real_time_col4:
        st.metric("🌐 Sites Connectés", "4/4", delta="100%")
        st.metric("⚡ Uptime Système", "99.97%", delta="↗ Optimal")
    
    st.divider()
    
    # Triple Excellence - Section Principale EXACTE ORIGINALE + ENRICHIE
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1e3a8a 0%, #3730a3 50%, #1e40af 100%); 
                padding: 2rem; border-radius: 20px; margin-bottom: 2rem; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <h2 style="color: white; text-align: center; margin: 0; font-size: 2.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🎯 Triple Excellence : SafetyGraph × BBS × ISO 45001
        </h2>
        <p style="color: #cbd5e1; text-align: center; margin: 1rem 0 0 0; font-size: 1.2rem;">
            Performance Triple Intégration - Vision Executive Mondiale
        </p>
        <div style="text-align: center; margin-top: 1rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 15px; color: white; margin: 0 0.5rem;">
                🔄 Synchronisation Temps Réel
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 15px; color: white; margin: 0 0.5rem;">
                🎯 KPIs Unifiés
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 15px; color: white; margin: 0 0.5rem;">
                🚀 Innovation Continue
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Les 3 colonnes de Triple Excellence - EXACTE RESTAURATION ORIGINALE
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e40af, #1d4ed8); padding: 2rem; border-radius: 15px; color: white; box-shadow: 0 8px 25px rgba(0,0,0,0.15);">
            <h4 style="margin: 0; color: #ddd6fe; text-align: center; font-size: 1.3rem;">🔷 SafetyGraph Analytics</h4>
            <hr style="border: 1px solid rgba(255,255,255,0.3); margin: 1rem 0;">
            <ul style="margin: 1rem 0; list-style: none; padding: 0;">
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Culture SST</strong> 
                    <span>80.8% 🔶️ ©Â</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>ROI Plateforme</strong> 
                    <span>4.2M$ (340%)</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Benchmark</strong> 
                    <span>78e percentile 🔶️ ©Â</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Conformité ⚡</strong> 
                    <span>94.2% 🔶️©Â</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Prédictions IA</strong> 
                    <span>97.3% 🆕</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Efficacité Agents</strong> 
                    <span>92.1% 🆕</span>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #059669, #047857); padding: 2rem; border-radius: 15px; color: white; box-shadow: 0 8px 25px rgba(0,0,0,0.15);">
            <h4 style="margin: 0; color: #d1fae5; text-align: center; font-size: 1.3rem;">📋 Behavioral Safety (BBS)</h4>
            <hr style="border: 1px solid rgba(255,255,255,0.3); margin: 1rem 0;">
            <ul style="margin: 1rem 0; list-style: none; padding: 0;">
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Score BBS</strong> 
                    <span>88.7% 🔶️ ©Â</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Leadership Visibility</strong> 
                    <span>18h/semaine</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Coaching Efficacité ⚡</strong> 
                    <span>89.3%</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>ROI BBS</strong> 
                    <span>1.8M$ (380%)</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Observations Terrain</strong> 
                    <span>2,847 🆕</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Actions Correctives</strong> 
                    <span>156 🆕</span>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #dc2626, #b91c1c); padding: 2rem; border-radius: 15px; color: white; box-shadow: 0 8px 25px rgba(0,0,0,0.15);">
            <h4 style="margin: 0; color: #fecaca; text-align: center; font-size: 1.3rem;">🏅 ISO 45001 Compliance</h4>
            <hr style="border: 1px solid rgba(255,255,255,0.3); margin: 1rem 0;">
            <ul style="margin: 1rem 0; list-style: none; padding: 0;">
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Leadership (Ch.5)</strong> 
                    <span>96.7% 🔶️©Â</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Performance (Ch.9)</strong> 
                    <span>95.2% 🔶️©Â</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Amélioration (Ch.10)</strong> 
                    <span>92.7% 🔶️©Â</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Certification ⚡</strong> 
                    <span>Q3 2024 🔶️©Â</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Audit Readiness</strong> 
                    <span>98.1% 🆕</span>
                </li>
                <li style="margin: 0.8rem 0; display: flex; justify-content: space-between;">
                    <strong>Documentation</strong> 
                    <span>100% 🆕</span>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # NOUVELLE SECTION : Dashboard Temps Réel Multi-Sites
    st.markdown("### 🌐 Dashboard Temps Réel Multi-Sites")
    
    # Carte de statut des sites
    sites_col1, sites_col2 = st.columns(2)
    
    with sites_col1:
        st.markdown("#### 🏢 Statut Sites en Temps Réel")
        
        sites_data = {
            'Site': ['Site Principal', 'Site Nord', 'Site Est', 'Site Ouest'],
            'Statut': ['🟢 Optimal', '🟡 Attention', '🟢 Optimal', '🟢 Optimal'],
            'Score HSE': [89.2, 76.8, 92.1, 85.7],
            'Employés': [456, 234, 389, 168],
            'Dernière MAJ': ['Il y a 2 min', 'Il y a 5 min', 'Il y a 1 min', 'Il y a 3 min']
        }
        
        df_sites = pd.DataFrame(sites_data)
        st.dataframe(df_sites, use_container_width=True)
    
    with sites_col2:
        st.markdown("#### 📊 Performance Sites - Graphique")
        
        fig_sites = px.bar(
            df_sites, 
            x='Site', 
            y='Score HSE',
            color='Score HSE',
            color_continuous_scale='RdYlGn',
            title="Scores HSE par Site - Temps Réel"
        )
        fig_sites.update_layout(height=300)
        st.plotly_chart(fig_sites, use_container_width=True)
    
    st.divider()
    
    # Performance Triple Intégration - Vision Executive (Graphique Radar ENRICHI)
    st.markdown("### 📊 Performance Triple Intégration - Vision Executive Enrichie")
    
    # Graphique Radar sophisticated comme dans vos captures + ENRICHISSEMENTS
    categories = [
        'Management Leadership',
        'Performance BBS', 
        'Observations Terrain',
        'Communication SST',
        'Coaching Efficacité',
        'ROI Consolidé',
        'Innovation IA',  # NOUVEAU
        'Prédictions Risques',  # NOUVEAU
        'Engagement Employés'  # NOUVEAU
    ]
    
    # Données actuelles vs objectifs 2025 ENRICHIES
    valeurs_actuelles = [85, 88.7, 82, 78, 89.3, 85, 91.2, 87.5, 83.8]
    objectifs_2025 = [90, 92, 88, 85, 92, 90, 95, 90, 88]
    valeurs_concurrence = [78, 82, 75, 71, 83, 79, 85, 80, 76]  # NOUVEAU : Benchmark concurrence
    
    fig_radar = go.Figure()
    
    # Trace Performance Actuelle
    fig_radar.add_trace(go.Scatterpolar(
        r=valeurs_actuelles,
        theta=categories,
        fill='toself',
        name='Performance Actuelle',
        line_color='#3b82f6',
        fillcolor='rgba(59, 130, 246, 0.3)'
    ))
    
    # Trace Objectifs 2025
    fig_radar.add_trace(go.Scatterpolar(
        r=objectifs_2025,
        theta=categories,
        fill='toself',
        name='Objectifs 2025',
        line_color='#10b981',
        fillcolor='rgba(16, 185, 129, 0.2)'
    ))
    
    # NOUVEAU : Trace Benchmark Concurrence
    fig_radar.add_trace(go.Scatterpolar(
        r=valeurs_concurrence,
        theta=categories,
        fill='toself',
        name='Benchmark Concurrence',
        line_color='#ef4444',
        fillcolor='rgba(239, 68, 68, 0.1)'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Performance vs Objectifs 2025 vs Concurrence - Radar Analysis Enrichi",
        height=600
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Tableau Performance Détaillée ENRICHI
    st.markdown("#### 📈 Tableau Performance vs Objectifs 2025 - Enrichi")
    
    performance_data = {
        'Dimension': categories,
        'Score Actuel (%)': valeurs_actuelles,
        'Objectif 2025 (%)': objectifs_2025,
        'Concurrence (%)': valeurs_concurrence,
        'Écart vs Objectif': [obj - act for act, obj in zip(valeurs_actuelles, objectifs_2025)],
        'Avantage vs Concurrence': [act - conc for act, conc in zip(valeurs_actuelles, valeurs_concurrence)],
        'Statut': ['🟢' if act >= obj-5 else '🟡' if act >= obj-10 else '🔴' 
                  for act, obj in zip(valeurs_actuelles, objectifs_2025)],
        'Priorité': ['Élevée' if act < obj-5 else 'Moyenne' if act < obj else 'Faible'
                    for act, obj in zip(valeurs_actuelles, objectifs_2025)]
    }
    
    df_performance = pd.DataFrame(performance_data)
    st.dataframe(df_performance, use_container_width=True)
    
    st.divider()
    
    # Actions Rapides Executive - 12 Boutons ENRICHIES (au lieu de 8)
    st.markdown("### ⚡ Actions Rapides Executive - One-Click Operations Enrichies")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Rapport Board", key="hse_rapport_board"):
            st.balloons()
            st.success("✅ Rapport Board généré et envoyé !")
            
        if st.button("🎯 BBS Status", key="hse_bbs_status"):
            st.success("✅ Status BBS mis à jour !")
            
        if st.button("🚀 IA Prédictions", key="hse_ia_predictions"):  # NOUVEAU
            st.success("✅ Prédictions IA actualisées !")
    
    with col2:
        if st.button("🏆 Excellence Review", key="hse_excellence_review"):
            st.success("✅ Excellence Review programmé !")
            
        if st.button("📋 ISO Audit Prep", key="hse_iso_audit"):
            st.success("✅ Préparation audit ISO activée !")
            
        if st.button("🔄 Sync Multi-Sites", key="hse_sync_sites"):  # NOUVEAU
            st.success("✅ Synchronisation 4 sites terminée !")
    
    with col3:
        if st.button("💰 ROI Analysis", key="hse_roi_analysis"):
            st.success("✅ Analyse ROI actualisée !")
            
        if st.button("⚡ Alert Urgent", key="hse_alert_urgent"):
            st.warning("⚠️ Alerte urgente envoyée aux équipes !")
            
        if st.button("📱 Mobile Sync", key="hse_mobile_sync"):  # NOUVEAU
            st.success("✅ Apps mobiles synchronisées !")
    
    with col4:
        if st.button("📈 KPI Dashboard", key="hse_kpi_dashboard"):
            st.success("✅ KPIs dashboard refresh !")
            
        if st.button("🔄 Sync ERP", key="hse_sync_erp"):
            st.success("✅ Synchronisation ERP terminée !")
            
        if st.button("🌐 Export Global", key="hse_export_global"):  # NOUVEAU
            st.success("✅ Export global multi-sites généré !")
    
    st.divider()
    
    # NOUVELLE SECTION : Analytics Avancés
    st.markdown("### 📊 Analytics Avancés - Insights Executive")
    
    analytics_tabs = st.tabs(["📈 Tendances", "🎯 Prédictions", "🔍 Deep Dive", "🏆 Benchmarks"])
    
    with analytics_tabs[0]:  # Tendances
        st.markdown("#### 📈 Tendances Performance - 12 Mois")
        
        # Graphique tendances enrichi
        mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 
                'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
        
        tendances_data = {
            'Mois': mois,
            'HSE Score': [82.1, 83.5, 84.2, 85.8, 86.1, 86.9, 87.3, 87.8, 88.2, 88.7, 89.1, 89.5],
            'ROI (%)': [280, 295, 315, 340, 365, 385, 402, 415, 420, 425, 430, 435],
            'BBS Score': [84.2, 85.1, 86.3, 87.1, 87.8, 88.2, 88.7, 89.1, 89.5, 89.8, 90.2, 90.6],
            'ISO Compliance': [91.2, 92.1, 93.5, 94.2, 95.1, 95.8, 96.2, 96.5, 96.7, 97.1, 97.3, 97.6]
        }
        
        df_tendances = pd.DataFrame(tendances_data)
        
        fig_tendances = go.Figure()
        
        for column in ['HSE Score', 'BBS Score', 'ISO Compliance']:
            fig_tendances.add_trace(go.Scatter(
                x=df_tendances['Mois'],
                y=df_tendances[column],
                mode='lines+markers',
                name=column,
                line=dict(width=3),
                marker=dict(size=8)
            ))
        
        fig_tendances.update_layout(
            title="Évolution Performance 2024 - Tendances Executive",
            xaxis_title="Mois",
            yaxis_title="Score (%)",
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig_tendances, use_container_width=True)
    
    with analytics_tabs[1]:  # Prédictions
        st.markdown("#### 🎯 Prédictions IA - 6 Mois")
        
        # Prédictions avec IA
        mois_futurs = ['Jan 2025', 'Fév 2025', 'Mar 2025', 'Avr 2025', 'Mai 2025', 'Jun 2025']
        
        predictions_data = {
            'Mois': mois_futurs,
            'HSE Score Prédit': [90.1, 90.7, 91.2, 91.8, 92.3, 92.9],
            'Confiance (%)': [94, 92, 89, 87, 85, 83],
            'ROI Prédit (%)': [445, 460, 475, 490, 505, 520],
            'Incidents Évités': [52, 58, 63, 69, 74, 80]
        }
        
        df_predictions = pd.DataFrame(predictions_data)
        st.dataframe(df_predictions, use_container_width=True)
        
        # Graphique prédictions
        fig_pred = px.line(
            df_predictions, 
            x='Mois', 
            y='HSE Score Prédit',
            title="Prédictions HSE Score - IA SafetyGraph",
            markers=True
        )
        fig_pred.update_layout(height=300)
        st.plotly_chart(fig_pred, use_container_width=True)
    
    with analytics_tabs[2]:  # Deep Dive
        st.markdown("#### 🔍 Deep Dive Analysis")
        
        # Matrice de corrélation
        st.markdown("##### 📊 Matrice de Corrélation - Facteurs HSE")
        
        correlation_data = {
            'Facteur': ['Leadership', 'Formation', 'BBS', 'ISO', 'ROI', 'Innovation'],
            'Leadership': [1.00, 0.87, 0.92, 0.89, 0.84, 0.76],
            'Formation': [0.87, 1.00, 0.79, 0.82, 0.73, 0.68],
            'BBS': [0.92, 0.79, 1.00, 0.88, 0.91, 0.74],
            'ISO': [0.89, 0.82, 0.88, 1.00, 0.86, 0.71],
            'ROI': [0.84, 0.73, 0.91, 0.86, 1.00, 0.69],
            'Innovation': [0.76, 0.68, 0.74, 0.71, 0.69, 1.00]
        }
        
        df_corr = pd.DataFrame(correlation_data)
        df_corr = df_corr.set_index('Facteur')
        
        fig_heatmap = px.imshow(
            df_corr.values,
            x=df_corr.columns,
            y=df_corr.index,
            color_continuous_scale='RdYlGn',
            title="Matrice de Corrélation - Facteurs HSE"
        )
        fig_heatmap.update_layout(height=400)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Analyse des goulots d'étranglement
        st.markdown("##### 🔍 Goulots d'Étranglement Identifiés")
        
        bottlenecks = [
            "🔴 **Formation EPI** : 12 employés en retard (Site Nord)",
            "🟡 **Communication SST** : Score 78% < Objectif 85%",
            "🟡 **Observations Terrain** : 82% < Objectif 88%",
            "🟢 **Leadership Visibility** : 18h/sem > Objectif 15h/sem"
        ]
        
        for bottleneck in bottlenecks:
            st.markdown(bottleneck)
    
    with analytics_tabs[3]:  # Benchmarks
        st.markdown("#### 🏆 Benchmarks Sectoriels")
        
        benchmark_data = {
            'Secteur': ['Construction', 'Manufacturing', 'Mines', 'Chimie', 'Pharma', 'VOTRE ENTREPRISE'],
            'HSE Score': [76.2, 81.4, 79.8, 83.1, 85.3, 87.3],
            'ROI (%)': [180, 215, 195, 245, 285, 420],
            'ISO Compliance': [89.1, 91.2, 87.6, 93.4, 94.8, 96.7],
            'Position': [6, 4, 5, 3, 2, 1]
        }
        
        df_benchmark = pd.DataFrame(benchmark_data)
        
        # Graphique benchmark
        fig_benchmark = px.scatter(
            df_benchmark, 
            x='HSE Score', 
            y='ROI (%)',
            size='ISO Compliance',
            color='Position',
            hover_name='Secteur',
            title="Position Concurrentielle - HSE vs ROI",
            color_continuous_scale='RdYlGn_r'
        )
        fig_benchmark.update_layout(height=400)
        st.plotly_chart(fig_benchmark, use_container_width=True)
        
        st.dataframe(df_benchmark, use_container_width=True)
    
    st.divider()
    
    # Graphique Évolution Incidents ENRICHI (comme dans vos captures)
    st.markdown("### 📉 Évolution Incidents - Trend Analysis Enrichi")
    
    # Données réalistes sur 12 mois ENRICHIES
    mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 
            'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
    
    incidents_data = {
        'Mois': mois,
        'Incidents Déclarés': [15, 12, 18, 10, 8, 14, 9, 11, 7, 13, 6, 9],
        'Incidents Évités': [25, 28, 32, 35, 40, 38, 45, 42, 48, 44, 52, 47],
        'Near Miss': [45, 42, 38, 40, 35, 41, 33, 36, 29, 38, 25, 31],
        'Prédictions IA': [23, 26, 30, 33, 37, 36, 42, 39, 45, 41, 49, 44],  # NOUVEAU
        'Actions Préventives': [67, 71, 75, 78, 82, 79, 85, 81, 88, 84, 91, 87]  # NOUVEAU
    }
    
    df_incidents = pd.DataFrame(incidents_data)
    
    fig_incidents = go.Figure()
    
    # Incidents déclarés
    fig_incidents.add_trace(go.Scatter(
        x=df_incidents['Mois'],
        y=df_incidents['Incidents Déclarés'],
        mode='lines+markers',
        name='Incidents Déclarés',
        line=dict(color='#dc2626', width=3),
        marker=dict(size=8)
    ))
    
    # Incidents évités
    fig_incidents.add_trace(go.Scatter(
        x=df_incidents['Mois'],
        y=df_incidents['Incidents Évités'],
        mode='lines+markers',
        name='Incidents Évités',
        line=dict(color='#10b981', width=3),
        marker=dict(size=8)
    ))
    
    # Near Miss
    fig_incidents.add_trace(go.Scatter(
        x=df_incidents['Mois'],
        y=df_incidents['Near Miss'],
        mode='lines+markers',
        name='Near Miss',
        line=dict(color='#f59e0b', width=3),
        marker=dict(size=8)
    ))
    
    # NOUVEAU : Prédictions IA
    fig_incidents.add_trace(go.Scatter(
        x=df_incidents['Mois'],
        y=df_incidents['Prédictions IA'],
        mode='lines+markers',
        name='Prédictions IA',
        line=dict(color='#8b5cf6', width=3, dash='dash'),
        marker=dict(size=8)
    ))
    
    # NOUVEAU : Actions Préventives
    fig_incidents.add_trace(go.Scatter(
        x=df_incidents['Mois'],
        y=df_incidents['Actions Préventives'],
        mode='lines+markers',
        name='Actions Préventives',
        line=dict(color='#06b6d4', width=3),
        marker=dict(size=8)
    ))
    
    fig_incidents.update_layout(
        title="Évolution Incidents 2024 - SafetyGraph Impact Enrichi",
        xaxis_title="Mois",
        yaxis_title="Nombre d'Incidents/Actions",
        height=500,
        showlegend=True
    )
    
    st.plotly_chart(fig_incidents, use_container_width=True)
    
    # NOUVELLE SECTION : Tableau de Bord Incidents Détaillé
    st.markdown("#### 🔍 Tableau de Bord Incidents Détaillé")
    
    incidents_detail_data = {
        'ID': ['INC-2024-089', 'INC-2024-090', 'INC-2024-091', 'INC-2024-092', 'INC-2024-093'],
        'Site': ['Site Nord', 'Site Principal', 'Site Est', 'Site Ouest', 'Site Nord'],
        'Type': ['Équipement', 'Comportemental', 'Environnemental', 'Procédural', 'Équipement'],
        'Gravité': ['🟡 Moyenne', '🟢 Faible', '🔴 Élevée', '🟡 Moyenne', '🟢 Faible'],
        'Statut': ['En cours', 'Résolu', 'Investigation', 'Résolu', 'En cours'],
        'BBS Score': [76.2, 89.3, 67.8, 82.1, 78.9],
        'Action Coaching': ['Programmé', 'Terminé', 'Urgent', 'Terminé', 'En cours'],
        'Temps Résolution (h)': [18, 6, None, 12, 24]
    }
    
    df_incidents_detail = pd.DataFrame(incidents_detail_data)
    st.dataframe(df_incidents_detail, use_container_width=True)
    
    st.divider()
    
    # NOUVELLE SECTION : ROI Analysis Détaillée
    st.markdown("### 💰 ROI Analysis Détaillée - Impact Financier")
    
    roi_col1, roi_col2 = st.columns(2)
    
    with roi_col1:
        st.markdown("#### 💵 Breakdown ROI par Composante")
        
        roi_breakdown = {
            'Composante': [
                'SafetyGraph Platform',
                'BBS Implementation', 
                'ISO 45001 Certification',
                'Formation & Training',
                'Innovation IA',
                'Mobile Applications',
                'Consulting & Support'
            ],
            'Investissement (k€)': [180, 95, 75, 120, 85, 45, 60],
            'Économies (k€)': [650, 420, 285, 380, 310, 165, 195],
            'ROI (%)': [261, 342, 280, 217, 265, 267, 225],
            'Payback (mois)': [14, 8, 12, 16, 13, 11, 15]
        }
        
        df_roi = pd.DataFrame(roi_breakdown)
        st.dataframe(df_roi, use_container_width=True)
    
    with roi_col2:
        st.markdown("#### 📊 Visualisation ROI")
        
        fig_roi_scatter = px.scatter(
            df_roi, 
            x='Investissement (k€)', 
            y='Économies (k€)',
            size='ROI (%)',
            color='Payback (mois)',
            hover_name='Composante',
            title="ROI Analysis - Investissement vs Économies",
            color_continuous_scale='RdYlGn_r'
        )
        fig_roi_scatter.update_layout(height=400)
        st.plotly_chart(fig_roi_scatter, use_container_width=True)
    
    # ROI Timeline Evolution
    st.markdown("#### 📈 Évolution ROI - Timeline 2024")
    
    roi_timeline = {
        'Trimestre': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024'],
        'ROI Cumulé (%)': [125, 245, 350, 420],
        'Économies Cumulées (M€)': [0.8, 1.9, 3.2, 4.7],
        'Incidents Évités': [89, 187, 298, 425]
    }
    
    df_roi_timeline = pd.DataFrame(roi_timeline)
    
    fig_roi_timeline = go.Figure()
    
    fig_roi_timeline.add_trace(go.Scatter(
        x=df_roi_timeline['Trimestre'],
        y=df_roi_timeline['ROI Cumulé (%)'],
        mode='lines+markers',
        name='ROI Cumulé (%)',
        line=dict(color='#10b981', width=4),
        marker=dict(size=12)
    ))
    
    fig_roi_timeline.update_layout(
        title="Évolution ROI Cumulé 2024 - Performance Executive",
        xaxis_title="Trimestre",
        yaxis_title="ROI (%)",
        height=350
    )
    
    st.plotly_chart(fig_roi_timeline, use_container_width=True)
    
    st.divider()
    
    # NOUVELLE SECTION : Export et Actions Avancées
    st.markdown("### 📁 Export & Actions Executive Avancées")
    
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        st.markdown("#### 📊 Exports Standards")
        
        if st.button("📋 Rapport Executive PDF", key="export_pdf_exec"):
            st.success("✅ Rapport Executive PDF généré !")
            
        if st.button("📊 Dashboard Excel", key="export_excel_dash"):
            st.success("✅ Dashboard Excel exporté !")
            
        if st.button("📈 Analytics JSON", key="export_json_analytics"):
            st.success("✅ Analytics JSON exporté !")
    
    with export_col2:
        st.markdown("#### 🌐 Exports Multi-Sites")
        
        if st.button("🏢 Rapport Consolidé", key="export_consolidated"):
            st.success("✅ Rapport 4 sites consolidé !")
            
        if st.button("📊 Benchmarks Sectoriels", key="export_benchmarks"):
            st.success("✅ Benchmarks sectoriels exportés !")
            
        if st.button("🎯 Prédictions IA", key="export_predictions"):
            st.success("✅ Prédictions IA exportées !")
    
    with export_col3:
        st.markdown("#### 🚀 Actions Stratégiques")
        
        if st.button("📧 Alerte Board", key="alert_board"):
            st.warning("⚠️ Alerte envoyée au Board of Directors !")
            
        if st.button("📅 Planifier Audit", key="schedule_audit"):
            st.success("✅ Audit ISO 45001 planifié !")
            
        if st.button("🔄 Sync Temps Réel", key="realtime_sync"):
            st.success("✅ Synchronisation temps réel activée !")
    
    # Export Dashboard Complet ENRICHI (bouton principal rouge)
    st.divider()
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        if st.button(
            "🔴 EXPORT DASHBOARD COMPLET BBS-ISO ENRICHI", 
            key="export_dashboard_complet_enrichi",
            type="primary",
            use_container_width=True
        ):
            st.balloons()
            st.success("✅ Dashboard executive enrichi exporté avec succès !")
            st.info("""
            📊 **Export inclut** : 
            • Performance Triple Enrichie (SafetyGraph × BBS × ISO)
            • ROI 420% avec breakdown détaillé
            • Métriques temps réel 4 sites
            • Prédictions IA 6 mois
            • Benchmarks sectoriels
            • Analytics avancés et corrélations
            • Actions executive et alertes
            """)
    
    # NOUVELLE SECTION : Notifications et Alertes Temps Réel
    st.divider()
    
    st.markdown("### 🔔 Notifications & Alertes Temps Réel")
    
    notif_col1, notif_col2 = st.columns(2)
    
    with notif_col1:
        st.markdown("#### 📱 Notifications Récentes")
        
        notifications = [
            "🟢 **Il y a 5 min** : Audit ISO Site Est - Certification validée",
            "🟡 **Il y a 12 min** : Formation EPI Site Nord - 12 employés en attente",
            "🔴 **Il y a 23 min** : Non-conformité Ch.6 ISO - Action requise",
            "🟢 **Il y a 1h** : ROI Q4 - Objectif 420% atteint",
            "🟡 **Il y a 2h** : Maintenance préventive - Programmée demain"
        ]
        
        for notif in notifications:
            st.markdown(notif)
    
    with notif_col2:
        st.markdown("#### ⚡ Actions Immédiates Requises")
        
        actions_immediates = [
            "🔥 **URGENT** : Site Nord - Audit interne Ch.6 ISO (< 48h)",
            "⚠️ **PRIORITÉ** : Formation EPI - 12 employés (< 1 semaine)",
            "📊 **SUIVI** : Coaching BBS - 3 sessions à programmer",
            "🔄 **ROUTINE** : Synchronisation ERP - Planifiée ce soir"
        ]
        
        for action in actions_immediates:
            st.markdown(action)
    
    # Footer Informatif Executive ENRICHI
    st.divider()
    
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f1f5f9, #e2e8f0); padding: 2rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h3 style="color: #1e293b; margin: 0; font-size: 1.5rem;">🏆 HSE Manager Executive Dashboard - Excellence Mondiale</h3>
        <div style="margin: 1rem 0; display: flex; justify-content: center; flex-wrap: wrap; gap: 2rem;">
            <div style="text-align: center;">
                <strong style="color: #3730a3;">Triple Intégration</strong><br>
                <span style="color: #64748b;">SafetyGraph × BBS × ISO 45001</span>
            </div>
            <div style="text-align: center;">
                <strong style="color: #059669;">Position Mondiale</strong><br>
                <span style="color: #64748b;">Top 1% (+14 positions)</span>
            </div>
            <div style="text-align: center;">
                <strong style="color: #dc2626;">ROI Exceptionnel</strong><br>
                <span style="color: #64748b;">420% Consolidé</span>
            </div>
            <div style="text-align: center;">
                <strong style="color: #7c3aed;">Innovation IA</strong><br>
                <span style="color: #64748b;">Prédictions 97.3%</span>
            </div>
        </div>
        <hr style="border: 1px solid #cbd5e1; margin: 1rem 0;">
        <p style="color: #64748b; margin: 0; font-size: 0.95rem;">
            <strong>Dernière MAJ :</strong> {current_time} | 
            <strong>Sites :</strong> 4 sites synchronisés temps réel | 
            <strong>Employés :</strong> 1,247 actifs | 
            <strong>Uptime :</strong> 99.97%<br>
            <strong>Certification :</strong> ISO 45001:2018 Excellence | 
            <strong>Next Audit :</strong> Décembre 2024 | 
            <strong>Version :</strong> SafetyGraph v4.0 Ultra
        </p>
    </div>
    """, unsafe_allow_html=True)