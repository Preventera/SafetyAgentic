"""
Dashboard Supervisor Terrain - Mode Mobile BBS-ISO
Version Excellence Terrain - Intégration SafetyGraph + BBS + ISO 45001
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

def display_supervisor_dashboard(config):
    """Dashboard Supervisor Terrain - Excellence BBS-ISO 45001"""
    
    # Header Terrain Mobile-First avec BBS-ISO
    st.markdown("""
    <div style="background: linear-gradient(90deg, #FF6B35, #F7931E, #FFD23F); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <h1 style="color: white; margin: 0;">👷 Supervisor Terrain Dashboard</h1>
        <p style="color: #FFF8DC; margin: 0;">🚀 Actions Terrain • 👥 Mon Équipe • 🧠 BBS Immédiat • 🏆 ISO Ch.5.4 & 7</p>
    </div>
    """, unsafe_allow_html=True)
    
    # === MÉTRIQUES TERRAIN BBS-ISO ===
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("👥 Mon Équipe", "8/10", "+2 aujourd'hui")
    
    with col2:
        st.metric("🎯 Score BBS Équipe", "75.8%", "+2.1%", help="Behavioral Safety Score terrain")
    
    with col3:
        st.metric("⚡ Actions Terrain", "6 actives", "3 urgentes", help="Actions rapides en cours")
    
    with col4:
        st.metric("🏆 ISO Responsabilisation", "91.8%", "+1.5%", help="Ch.5.4 & 7 - Communication terrain")
    
    with col5:
        st.metric("🧠 Psychological Safety", "4.1/5", "+0.2", help="Sécurité psychologique équipe")
    
    # === ALERTES TERRAIN INTELLIGENTES ===
    st.markdown("### 🚨 **Alertes Terrain Prioritaires**")
    
    alert_col1, alert_col2 = st.columns(2)
    
    with alert_col1:
        st.error("🚨 **Zone D10-D12** : Comportement risqué détecté - Intervention immédiate")
        st.warning("⚠️ **Équipement Zone B** : Vérification EPI requise (2 employés)")
    
    with alert_col2:
        st.success("✅ **Observation Positive** : Équipe Alpha excellent comportement sécuritaire")
        st.info("📊 **Formation Due** : Module BBS équipe Nuit (planifiée 14h)")
    
    # === LAYOUT PRINCIPAL TERRAIN ===
    col_terrain, col_actions = st.columns([3, 2])
    
    with col_terrain:
        # === MON ÉQUIPE TEMPS RÉEL ===
        st.markdown("### 👥 **Mon Équipe - Status Temps Réel**")
        
        # Tableau équipe avec BBS
        team_members = [
            {"Nom": "Jean D.", "Zone": "A1-A3", "Status BBS": "🟢 Excellent", "Score": "89.2%", "Dernière Obs": "08:45", "Action": "✅ Coaching positif"},
            {"Nom": "Marie L.", "Zone": "B4-B6", "Status BBS": "🟡 Attention", "Score": "72.1%", "Dernière Obs": "09:12", "Action": "⚠️ Observation due"},
            {"Nom": "Pierre M.", "Zone": "C7-C9", "Status BBS": "🟢 Bon", "Score": "83.7%", "Dernière Obs": "08:52", "Action": "✅ Conforme"},
            {"Nom": "Sophie R.", "Zone": "A1-A3", "Status BBS": "🔴 Risque", "Score": "61.3%", "Dernière Obs": "07:30", "Action": "🚨 Coaching urgent"},
            {"Nom": "Luc B.", "Zone": "D10-D12", "Status BBS": "🟡 Surveillance", "Score": "76.8%", "Dernière Obs": "09:05", "Action": "👁️ Monitoring"},
            {"Nom": "Anna T.", "Zone": "E13-E15", "Status BBS": "🟢 Excellent", "Score": "91.4%", "Dernière Obs": "08:38", "Action": "✅ Renforcement"},
            {"Nom": "Tom W.", "Zone": "B4-B6", "Status BBS": "🟢 Bon", "Score": "85.9%", "Dernière Obs": "09:18", "Action": "✅ Conforme"},
            {"Nom": "Lisa K.", "Zone": "C7-C9", "Status BBS": "🟡 Formation", "Score": "69.5%", "Dernière Obs": "08:15", "Action": "📚 Formation BBS"}
        ]
        
        import pandas as pd
        team_df = pd.DataFrame(team_members)
        st.dataframe(team_df, use_container_width=True, hide_index=True)
        
        # === GRAPHIQUE PERFORMANCE ÉQUIPE ===
        st.markdown("#### 📊 **Performance BBS Équipe - Temps Réel**")
        
        fig_team = go.Figure()
        
        # Données performance équipe
        team_names = ["Jean D.", "Marie L.", "Pierre M.", "Sophie R.", "Luc B.", "Anna T.", "Tom W.", "Lisa K."]
        bbs_scores = [89.2, 72.1, 83.7, 61.3, 76.8, 91.4, 85.9, 69.5]
        colors = ['green' if score >= 85 else 'orange' if score >= 75 else 'red' for score in bbs_scores]
        
        fig_team.add_trace(go.Bar(
            x=team_names,
            y=bbs_scores,
            marker_color=colors,
            text=[f"{score}%" for score in bbs_scores],
            textposition='auto',
        ))
        
        fig_team.update_layout(
            title="Score BBS par Membre d'Équipe",
            xaxis_title="Équipe",
            yaxis_title="Score BBS (%)",
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig_team, use_container_width=True)
    
    with col_actions:
        # === ACTIONS RAPIDES TERRAIN ===
        st.markdown("### ⚡ **Actions Rapides Terrain**")
        
        # 1. OBSERVATION BBS IMMÉDIATE
        if st.button("🧠 Observation BBS", use_container_width=True, type="primary", key="obs_bbs_terrain"):
            st.success("✅ **Observation BBS terrain activée !**")
            
            with st.expander("📱 Observation Mobile Rapide", expanded=True):
                col_obs1, col_obs2 = st.columns(2)
                with col_obs1:
                    observed_member = st.selectbox("👤 Membre observé", team_names, key="obs_member")
                    behavior_observed = st.selectbox("🎯 Comportement", ["✅ Sûr", "⚠️ À corriger", "🚨 Dangereux"], key="obs_behavior")
                
                with col_obs2:
                    zone_obs = st.text_input("📍 Zone", placeholder="Ex: A1-A3", key="obs_zone")
                    immediate_feedback = st.checkbox("💬 Feedback donné", value=True, key="obs_feedback")
                
                if st.button("📤 Enregistrer Observation", use_container_width=True, key="save_obs_terrain"):
                    obs_report = f"""
🧠 OBSERVATION BBS TERRAIN - {datetime.now().strftime('%H:%M')}

👤 Membre: {observed_member}
📍 Zone: {zone_obs}
🎯 Comportement: {behavior_observed}
💬 Feedback immédiat: {'✅ Oui' if immediate_feedback else '❌ Non'}

👷 Superviseur: Terrain Mobile
⏰ {datetime.now().strftime('%d/%m/%Y à %H:%M')}
🏆 Contribution ISO Ch.5.4: Participation active ✅
                    """
                    
                    st.success("✅ **Observation BBS enregistrée !** Impact immédiat sur score équipe")
                    st.download_button("📥 Export Observation", data=obs_report, 
                                     file_name=f"obs_bbs_terrain_{datetime.now().strftime('%H%M')}.txt",
                                     mime="text/plain", key="download_obs_terrain")
        
        # 2. COACHING TERRAIN
        if st.button("🎯 Coaching Immédiat", use_container_width=True, key="coaching_terrain"):
            st.success("✅ **Coaching terrain activé !**")
            
            with st.expander("🎯 Coaching Mobile", expanded=True):
                target_member = st.selectbox("👤 Membre à coacher", team_names, key="coach_member")
                coaching_type = st.selectbox("🎯 Type", ["✅ Renforcement positif", "⚠️ Correction", "📚 Formation"], key="coach_type")
                
                if st.button("🚀 Démarrer Coaching", use_container_width=True, key="start_coaching"):
                    st.success(f"✅ **Coaching {coaching_type}** programmé pour {target_member}")
                    st.info("⏰ Durée estimée: 10-15 minutes terrain")
        
        # 3. ALERTE ÉQUIPE
        if st.button("📢 Alerte Équipe", use_container_width=True, key="alert_team"):
            st.warning("⚠️ **Alerte équipe diffusée !**")
            
            with st.expander("📢 Message Équipe", expanded=True):
                alert_type = st.selectbox("🎯 Type alerte", ["🚨 Sécurité", "📋 Procédure", "✅ Félicitations"], key="alert_type")
                alert_message = st.text_area("💬 Message", placeholder="Message pour l'équipe...", key="alert_msg")
                
                if st.button("📤 Diffuser Alerte", use_container_width=True, key="send_alert"):
                    st.success("✅ **Alerte diffusée** à toute l'équipe terrain")
                    st.info("📱 Notifications push envoyées sur mobiles équipe")
        
        # 4. RAPPORT TERRAIN EXPRESS
        if st.button("📊 Rapport Express", use_container_width=True, key="report_terrain"):
            st.success("✅ **Rapport terrain généré !**")
            
            terrain_report = f"""
📊 RAPPORT TERRAIN EXPRESS - {datetime.now().strftime('%H:%M')}
👷 Superviseur Terrain - Équipe de 8 membres

🎯 PERFORMANCE BBS ÉQUIPE:
• Score moyen équipe: 75.8% (+2.1% amélioration)
• Membres excellence (>85%): 3/8 (37.5%)
• Membres attention (<75%): 3/8 (37.5%)
• Psychological Safety: 4.1/5 (+0.2)

🚨 SITUATIONS TERRAIN:
• Zone D10-D12: Comportement risqué - Intervention en cours
• Sophie R.: Coaching urgent programmé
• Lisa K.: Formation BBS requise

✅ ACTIONS TERRAIN RÉALISÉES:
• Observations BBS: 12 effectuées aujourd'hui
• Coaching positif: 4 sessions terrain
• Alertes traitées: 6/6 résolues

🏆 CONFORMITÉ ISO TERRAIN:
• Ch.5.4 Responsabilisation: 91.8% ✅
• Ch.7 Communication: 89.3% ✅
• Participation active: 94.2% équipe

👷 Superviseur: Terrain Mobile
⏰ {datetime.now().strftime('%d/%m/%Y à %H:%M')}
📍 Zones: A1-A3, B4-B6, C7-C9, D10-D12, E13-E15
            """
            
            st.text_area("📄 Rapport Terrain", terrain_report, height=300, key="rapport_content")
            st.download_button("📥 Export Rapport Terrain", data=terrain_report,
                             file_name=f"rapport_terrain_{datetime.now().strftime('%H%M')}.txt",
                             mime="text/plain", key="download_rapport_terrain")
        
        # === ALERTES BBS-ISO TERRAIN ===
        st.markdown("### ⚠️ **Alertes BBS-ISO**")
        st.error("🚨 Sophie R. : Coaching urgent requis")
        st.warning("⚠️ Zone D10-D12 : Surveillance renforcée")
        st.success("✅ Anna T. : Performance exemplaire")
        st.info("📚 Lisa K. : Formation BBS planifiée")
    
    # === ONGLETS TERRAIN DÉTAILLÉS ===
    tab1, tab2, tab3 = st.tabs(["👥 Équipe Détail", "📊 Performance BBS", "🏆 ISO Terrain"])
    
    with tab1:
        st.markdown("#### 👥 **Gestion Équipe Terrain**")
        
        # Métriques équipe détaillées
        eq_col1, eq_col2, eq_col3, eq_col4 = st.columns(4)
        with eq_col1:
            st.metric("👥 Présents", "8/10")
        with eq_col2:
            st.metric("🎯 Score Moyen BBS", "75.8%")
        with eq_col3:
            st.metric("⚡ Actions en cours", "6")
        with eq_col4:
            st.metric("🏆 Conformité", "91.8%")
        
        # Planning équipe
        st.markdown("**📅 Planning Terrain:**")
        st.success("✅ **Jean D. & Anna T.** - Zone A1-A3 (Excellence BBS 89-91%)")
        st.warning("⚠️ **Marie L. & Tom W.** - Zone B4-B6 (Surveillance renforcée)")
        st.info("📍 **Pierre M.** - Zone C7-C9 (Performance stable 83%)")
        st.error("🚨 **Sophie R. & Luc B.** - Zone D10-D12 (Intervention requise)")
        
        # Actions recommandées
        st.markdown("**🎯 Actions Recommandées:**")
        st.info("1. **Coaching urgent** Sophie R. (Score 61.3%)")
        st.info("2. **Formation BBS** Lisa K. (Score 69.5%)")
        st.info("3. **Renforcement positif** Anna T. (Score 91.4%)")
        st.info("4. **Surveillance** Zone D10-D12 (risques détectés)")
    
    with tab2:
        st.markdown("#### 📊 **Performance BBS Terrain**")
        
        # Métriques BBS terrain
        bbs_col1, bbs_col2, bbs_col3 = st.columns(3)
        with bbs_col1:
            st.metric("🧠 Observations Terrain", "12/15", "+4 aujourd'hui")
        with bbs_col2:
            st.metric("💬 Feedback Immédiat", "94%", "Moyenne <2 min")
        with bbs_col3:
            st.metric("🎯 Coaching Efficacité", "87%", "+5% ce mois")
        
        # Évolution BBS équipe
        st.markdown("**📈 Évolution BBS Équipe (7 jours):**")
        
        fig_evolution = go.Figure()
        
        days = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
        team_score_evolution = [71.2, 72.8, 73.5, 74.1, 75.2, 75.6, 75.8]
        
        fig_evolution.add_trace(go.Scatter(
            x=days, y=team_score_evolution,
            mode='lines+markers',
            name='Score BBS Équipe',
            line=dict(color='orange', width=3),
            marker=dict(size=8)
        ))
        
        fig_evolution.update_layout(
            title="Progression BBS Équipe - 7 jours",
            xaxis_title="Jours",
            yaxis_title="Score BBS (%)",
            height=300
        )
        
        st.plotly_chart(fig_evolution, use_container_width=True)
        
        # Top performers
        st.markdown("**🏆 Top Performers BBS:**")
        st.success("🥇 **Anna T.** - 91.4% (Zone E13-E15)")
        st.success("🥈 **Jean D.** - 89.2% (Zone A1-A3)")
        st.success("🥉 **Tom W.** - 85.9% (Zone B4-B6)")
    
    with tab3:
        st.markdown("#### 🏆 **Conformité ISO 45001 Terrain**")
        
        # Conformité par chapitre
        iso_terrain_col1, iso_terrain_col2 = st.columns(2)
        
        with iso_terrain_col1:
            st.markdown("**🎯 Ch.5.4 Responsabilisation:**")
            st.metric("Score Conformité", "91.8%", "+1.5%")
            st.progress(0.918)
            st.info("✅ Délégation terrain efficace")
            st.info("✅ Autonomie équipe reconnue")
            st.info("✅ Prise d'initiative encouragée")
        
        with iso_terrain_col2:
            st.markdown("**💬 Ch.7 Communication:**")
            st.metric("Score Communication", "89.3%", "+2.1%")
            st.progress(0.893)
            st.info("✅ Feedback terrain <2 min")
            st.info("✅ Remontée d'information active")
            st.info("✅ Écoute bidirectionnelle")
        
        # Evidence ISO terrain
        st.markdown("**📋 Evidence ISO Terrain:**")
        evidence_data = {
            'Exigence ISO': ['Responsabilisation terrain', 'Communication immédiate', 'Participation active', 'Formation continue'],
            'Evidence': ['Délégation décisions', 'Feedback <2 min', '94% engagement', 'BBS formation'],
            'Score': ['91.8%', '89.3%', '94.2%', '85.7%'],
            'Status': ['✅ Conforme', '✅ Conforme', '✅ Excellence', '🟡 Amélioration']
        }
        evidence_df = pd.DataFrame(evidence_data)
        st.dataframe(evidence_df, use_container_width=True, hide_index=True)
    
    # === FOOTER TERRAIN ===
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 1rem; background: linear-gradient(90deg, #f8f9fa, #e9ecef); border-radius: 10px; border-left: 5px solid #FF6B35;">
        <strong>👷 Dashboard Supervisor Terrain - Excellence BBS-ISO</strong><br>
        <small>⏰ Dernière MAJ: {datetime.now().strftime("%H:%M")} | 
        🎯 Score Équipe: 75.8% | 👥 Équipe: 8/10 actifs | 
        🏆 ISO: 91.8% Responsabilisation | 🧠 BBS: 12 obs/jour</small>
    </div>
    """, unsafe_allow_html=True)