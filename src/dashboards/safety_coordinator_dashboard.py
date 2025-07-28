"""
Dashboard Safety Coordinator - Mode Operations OPTIMISÉ BBS-ISO 45001
Version RÉVOLUTIONNAIRE - Intégration complète métriques comportementales et conformité normative
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

def display_safety_coordinator_dashboard(config):
    """Dashboard Safety Coordinator - Mode Operations avec BBS-ISO 45001 intégré"""
    
    # Header professionnel avec contexte opérationnel
    st.markdown("## ⚡ Safety Coordinator Operations Dashboard")
    st.markdown("*Mode Opérationnel - Coordination terrain et incidents | BBS-ISO 45001 Intégré*")
    
    # === MÉTRIQUES TEMPS RÉEL ENRICHIES BBS-ISO ===
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🚨 Incidents Actifs", "7", delta="-2")
    
    with col2:
        st.metric("📊 Compliance ISO", "94.3%", delta="+1.8%", help="ISO 45001 Ch.5.4 Participation")
    
    with col3:
        st.metric("👥 Équipes Actives", "12/15", delta="2")
    
    with col4:
        st.metric("⏱️ Temps Résolution", "2.4h", delta="-0.3h")
    
    with col5:
        st.metric("🎯 BBS Score", "85.2%", delta="+2.1%", help="Behavioral Safety Index")
    
    # === SECTION BBS DÉDIÉE (NOUVEAU) ===
    st.markdown("### 🧠 **Behavioral Safety (BBS) - Performance Temps Réel**")
    
    bbs_col1, bbs_col2, bbs_col3, bbs_col4 = st.columns(4)
    
    with bbs_col1:
        st.metric(
            "📊 Observations BBS", 
            "47/60", 
            delta="12 aujourd'hui",
            help="Target: 60 observations/jour"
        )
    
    with bbs_col2:
        st.metric(
            "✅ Comportements Sûrs", 
            "88.7%", 
            delta="+3.2%",
            help="% Comportements conformes observés"
        )
    
    with bbs_col3:
        st.metric(
            "⚡ Feedback Moyen", 
            "12 min", 
            delta="-3 min",
            help="Target: <15 minutes post-observation"
        )
    
    with bbs_col4:
        st.metric(
            "🎯 Coaching Ratio", 
            "78/22", 
            delta="Target 80/20",
            help="Positif/Correctif (ISO Ch.7 Communication)"
        )
    
    # === ALERTES BBS INTELLIGENTES (NOUVEAU) ===
    st.markdown("### 🚨 **Alertes BBS Intelligentes**")
    
    alert_col1, alert_col2 = st.columns(2)
    
    with alert_col1:
        st.warning("⚠️ **Observation BBS Due**: Équipe Beta - Zone B4-B6 (dernière: 3h)")
        st.info("📊 **Pattern Détecté**: Augmentation EPI non conformes Zone C (+15%)")
    
    with alert_col2:
        st.success("✅ **Coaching Positif**: Équipe Alpha excellent comportement sécuritaire")
        st.error("🚨 **Comportement Risqué**: Zone D10-D12 - Intervention BBS requise")
    
    # === LAYOUT PRINCIPAL ===
    col_main, col_actions = st.columns([2, 1])
    
    with col_main:
        # === TIMELINE INTERACTIVE ENRICHIE BBS ===
        st.markdown("### 📅 Timeline Opérationnelle + BBS")
        
        # Timeline avec composants BBS intégrés
        timeline_events = [
            {"time": "08:15", "event": "Inspection Zone A terminée + 5 observations BBS", "status": "✅ TERMINÉ", "priority": "success", "bbs": True},
            {"time": "09:30", "event": "Incident mineur Secteur B + Analyse comportementale", "status": "🔄 EN COURS", "priority": "warning", "bbs": True},
            {"time": "10:45", "event": "Formation équipe Nuit + Module BBS", "status": "📚 PLANIFIÉ", "priority": "info", "bbs": True},
            {"time": "11:20", "event": "Maintenance préventive + Observations sécurité", "status": "⚡ URGENT", "priority": "error", "bbs": True},
            {"time": "12:00", "event": "Réunion coordination + Feedback BBS équipes", "status": "📅 PROGRAMMÉ", "priority": "info", "bbs": True},
            {"time": "13:30", "event": "Coaching BBS Équipe Delta", "status": "🎯 BBS", "priority": "bbs_focus", "bbs": True},
            {"time": "14:15", "event": "Observation positive Équipe Gamma", "status": "✅ BBS+", "priority": "bbs_positive", "bbs": True}
        ]
        
        for event in timeline_events:
            # Icône BBS si applicable
            bbs_icon = "🧠 " if event.get("bbs") else ""
            
            if event["priority"] == "error":
                st.error(f"**{event['time']}** - {bbs_icon}{event['event']} - {event['status']}")
            elif event["priority"] == "warning":
                st.warning(f"**{event['time']}** - {bbs_icon}{event['event']} - {event['status']}")
            elif event["priority"] == "success":
                st.success(f"**{event['time']}** - {bbs_icon}{event['event']} - {event['status']}")
            elif event["priority"] == "bbs_focus":
                st.markdown(f"🎯 **{event['time']}** - {event['event']} - {event['status']}")
            elif event["priority"] == "bbs_positive":
                st.markdown(f"🟢 **{event['time']}** - {event['event']} - {event['status']}")
            else:
                st.info(f"**{event['time']}** - {bbs_icon}{event['event']} - {event['status']}")
    
    with col_actions:
        # === ACTIONS RAPIDES ENRICHIES BBS-ISO ===
        st.markdown("### 🎯 Actions Rapides BBS-ISO")
        
        # 1. OBSERVATION BBS (NOUVEAU)
        if st.button("🧠 Observation BBS", use_container_width=True, type="primary", key="bbs_observation"):
            st.success("✅ Module Observation BBS activé !")
            
            with st.expander("📋 Saisie Observation Comportementale", expanded=True):
                col_obs1, col_obs2 = st.columns(2)
                with col_obs1:
                    team_observed = st.selectbox("Équipe", ["Alpha", "Beta", "Gamma", "Delta", "Echo"], key="obs_team")
                    behavior_type = st.selectbox("Comportement", ["✅ Sûr", "⚠️ À risque", "🚨 Dangereux"], key="obs_behavior")
                with col_obs2:
                    location = st.text_input("Zone", placeholder="Ex: A1-A3", key="obs_location")
                    observer = st.text_input("Observateur", value="Safety Coordinator", key="obs_observer")
                
                behavior_detail = st.text_area("Détail comportement observé", 
                                               placeholder="Description précise du comportement...", 
                                               key="obs_detail")
                
                # Feedback immédiat
                feedback_given = st.checkbox("Feedback donné immédiatement", key="obs_feedback")
                
                if st.button("📤 Enregistrer Observation BBS", use_container_width=True, key="save_bbs_obs"):
                    # Génération rapport BBS
                    bbs_report = f"""
🧠 OBSERVATION BBS - {datetime.now().strftime('%d/%m/%Y %H:%M')}

👥 Équipe observée: {team_observed}
📍 Zone: {location}
🎯 Type comportement: {behavior_type}
👤 Observateur: {observer}

📝 Description comportement:
{behavior_detail}

💬 Feedback immédiat: {'✅ Oui' if feedback_given else '❌ Non'}

📊 SCORING BBS:
• Observation #47 du jour (Target: 60)
• Contribution score équipe: +2.3%
• Impact culture sécurité: Positif

🏆 CONFORMITÉ ISO 45001:
• Ch.5.4 Participation travailleurs: ✅
• Ch.7 Communication efficace: ✅
• Ch.10 Amélioration continue: ✅

⏰ Temps observation: {datetime.now().strftime('%d/%m/%Y à %H:%M')}
🔗 ID Observation: BBS-{datetime.now().strftime('%Y%m%d-%H%M%S')}
👤 Safety Coordinator: {observer}
🏢 Site: SafetyGraph Industries - Enterprise ABC
                    """
                    
                    st.success("✅ Observation BBS enregistrée et intégrée au scoring global !")
                    st.download_button(
                        label="📥 Export Observation BBS",
                        data=bbs_report,
                        file_name=f"observation_bbs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="download_bbs_obs"
                    )
        
        # 2. DÉCLARER INCIDENT enrichi BBS
        if st.button("🚨 Déclarer Incident + BBS", use_container_width=True, key="incident_bbs"):
            st.balloons()
            st.success("✅ Formulaire incident + Analyse comportementale !")
            
            with st.expander("📋 Incident + Analyse BBS", expanded=True):
                col_form1, col_form2 = st.columns(2)
                with col_form1:
                    incident_type = st.selectbox("Type", ["Chute", "Équipement", "Chimique", "Autre"], key="inc_type_bbs")
                    severity = st.selectbox("Gravité", ["🔴 Critique", "🟡 Modéré", "🟢 Mineur"], key="inc_severity_bbs")
                with col_form2:
                    location = st.text_input("Zone", placeholder="Ex: Secteur A-12", key="inc_location_bbs")
                    team_involved = st.selectbox("Équipe impliquée", ["Alpha", "Beta", "Gamma", "Delta", "Echo"], key="inc_team")
                
                description = st.text_area("Description incident", placeholder="Détails de l'incident...", key="inc_desc_bbs")
                
                # Section BBS
                st.markdown("**🧠 Analyse Comportementale (BBS)**")
                behavioral_factor = st.selectbox("Facteur comportemental", 
                                                ["Aucun", "Procédure non suivie", "Formation insuffisante", 
                                                 "Pression temps", "Équipement inadéquat", "Communication défaillante"],
                                                key="bbs_factor")
                
                if behavioral_factor != "Aucun":
                    bbs_recommendation = st.text_area("Recommandations BBS", 
                                                      placeholder="Actions comportementales recommandées...",
                                                      key="bbs_recommendations")
                
                if st.button("📤 Envoyer Rapport Incident+BBS", use_container_width=True, key="send_incident_bbs"):
                    # Génération du rapport enrichi
                    incident_bbs_report = f"""
🚨 RAPPORT INCIDENT + ANALYSE BBS - {datetime.now().strftime('%d/%m/%Y %H:%M')}

📍 Zone: {location}
🕐 Heure: {datetime.now().strftime('%H:%M')}
⚠️ Type: {incident_type}
🎯 Gravité: {severity}
👥 Équipe impliquée: {team_involved}

📝 Description incident:
{description}

🧠 ANALYSE COMPORTEMENTALE (BBS):
• Facteur comportemental identifié: {behavioral_factor}
{'• Recommandations BBS: ' + bbs_recommendation if behavioral_factor != "Aucun" else '• Aucun facteur comportemental identifié'}

📊 IMPACT SUR MÉTRIQUES BBS:
• Révision observations équipe {team_involved}
• Formation ciblée requise: {'✅ Oui' if behavioral_factor != "Aucun" else '❌ Non'}
• Coaching additionnel: {'✅ Recommandé' if behavioral_factor != "Aucun" else '❌ Non requis'}

🏆 CONFORMITÉ ISO 45001:
• Ch.6 Gestion risques: Investigation comportementale ✅
• Ch.10 Amélioration continue: Plan d'action BBS ✅
• Ch.5.4 Participation: Implication équipe ✅

👤 Rapporté par: Safety Coordinator
🔗 ID: INC-BBS-{datetime.now().strftime('%Y%m%d-%H%M%S')}
📍 Localisation GPS: 45.5017° N, 73.5673° W
🏢 Site: SafetyGraph Industries - Enterprise ABC
                    """
                    
                    st.success("✅ Rapport incident + analyse BBS généré et envoyé !")
                    st.download_button(
                        label="📥 Télécharger Rapport Incident+BBS",
                        data=incident_bbs_report,
                        file_name=f"incident_bbs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="download_incident_bbs"
                    )
        
        # 3. COACHING BBS (NOUVEAU)
        if st.button("🎯 Session Coaching BBS", use_container_width=True, key="coaching_bbs"):
            st.success("✅ Module Coaching BBS activé !")
            
            with st.expander("🎯 Coaching Comportemental", expanded=True):
                coach_col1, coach_col2 = st.columns(2)
                with coach_col1:
                    target_team = st.selectbox("Équipe cible", ["Alpha", "Beta", "Gamma", "Delta", "Echo"], key="coach_team")
                    coaching_type = st.selectbox("Type coaching", ["✅ Renforcement positif", "⚠️ Correction comportement", "📚 Formation ciblée"], key="coach_type")
                with coach_col2:
                    coach_location = st.text_input("Zone intervention", placeholder="Ex: B4-B6", key="coach_location")
                    duration = st.selectbox("Durée estimée", ["15 min", "30 min", "45 min", "1h"], key="coach_duration")
                
                coaching_objective = st.text_area("Objectifs coaching", 
                                                  placeholder="Comportements spécifiques à adresser...",
                                                  key="coach_objectives")
                
                if st.button("🚀 Programmer Coaching", use_container_width=True, key="schedule_coaching"):
                    coaching_plan = f"""
🎯 PLAN COACHING BBS - {datetime.now().strftime('%d/%m/%Y %H:%M')}

👥 Équipe cible: {target_team}
📍 Zone intervention: {coach_location}
🎯 Type coaching: {coaching_type}
⏱️ Durée: {duration}

📝 Objectifs coaching:
{coaching_objective}

📅 PLANIFICATION:
• Heure prévue: {(datetime.now() + timedelta(hours=1)).strftime('%H:%M')}
• Méthode: Coaching terrain direct
• Approche: {'Positive - Renforcement' if 'positif' in coaching_type else 'Corrective - Amélioration'}

📊 SUIVI BBS:
• Impact attendu score équipe: +5-10%
• Indicateurs surveillance: Observations post-coaching
• Feedback requis: 24-48h post-intervention

🏆 ALIGNEMENT ISO 45001:
• Ch.5.4 Consultation: Approche participative ✅
• Ch.7 Communication: Dialogue ouvert ✅
• Ch.10 Amélioration: Actions concrètes ✅

👤 Coach: Safety Coordinator
⏰ Programmé: {datetime.now().strftime('%d/%m/%Y à %H:%M')}
🏢 Site: SafetyGraph Industries - Enterprise ABC
                    """
                    
                    st.success("✅ Session coaching BBS programmée avec succès !")
                    st.download_button(
                        label="📥 Export Plan Coaching",
                        data=coaching_plan,
                        file_name=f"coaching_bbs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="download_coaching"
                    )
        
        # 4. RAPPORT FLASH BBS-ISO (ENRICHI)
        if st.button("📊 Rapport Flash BBS-ISO", use_container_width=True, key="report_bbs_iso"):
            st.success("✅ Génération rapport intégré BBS-ISO 45001 !")
            
            with st.expander("📈 Rapport Flash - Synthèse BBS-ISO 45001", expanded=True):
                flash_report_bbs = f"""
⚡ RAPPORT FLASH BBS-ISO 45001 INTÉGRÉ
📅 {datetime.now().strftime('%d/%m/%Y à %H:%M')}
🏢 SafetyGraph Industries - Enterprise ABC

📊 MÉTRIQUES TEMPS RÉEL CONSOLIDÉES:
• Incidents actifs: 7 (-2 vs hier) ✅
• Compliance ISO 45001: 94.3% (+1.8% ce mois) 🏆
• BBS Score global: 85.2% (+2.1% amélioration) 🧠
• Équipes actives: 12/15 (80% opérationnel)
• Temps résolution: 2.4h (-0.3h amélioration) ✅

🧠 PERFORMANCE BBS DÉTAILLÉE:
• Observations réalisées: 47/60 (78% objectif quotidien)
• Comportements sûrs: 88.7% (+3.2% vs semaine dernière) ✅
• Feedback moyen: 12 min (-3 min amélioration) ✅
• Coaching ratio: 78/22 (Target 80/20 - Ajustement requis)
• Sessions coaching: 3 programmées aujourd'hui

🏆 CONFORMITÉ ISO 45001 PAR CHAPITRE:
• Ch.5 Leadership: 96.7% - Engagement direction visible ✅
• Ch.5.4 Participation: 94.3% - BBS favorise implication ✅
• Ch.7 Communication: 93.1% - Feedback BBS efficace ✅
• Ch.8 Opérations: 91.8% - Procédures intégrées BBS ✅
• Ch.9 Performance: 95.2% - Monitoring BBS continu ✅
• Ch.10 Amélioration: 92.7% - Actions correctives BBS ✅

🚨 SITUATIONS CRITIQUES BBS-ISO:
• Zone D10-D12: Comportement risqué détecté - Coaching urgent ✅
• Équipe Beta: Retard observations (3h sans BBS) - Action requise
• Formation BBS: 2 équipes nécessitent mise à niveau
• Ratio coaching: Ajustement vers 80/20 (actuellement 78/22)

✅ POINTS POSITIFS BBS-ISO:
• Équipe Alpha: Excellent comportement - Renforcement positif ✅
• Zone A: Inspection + 5 observations BBS réussies ✅
• Formation nuit: Module BBS intégré planifié ✅
• Trend positif: +3.2% comportements sûrs cette semaine ✅

🎯 ACTIONS RECOMMANDÉES BBS-ISO:
1. Coaching urgent Zone D10-D12 (comportement risqué)
2. Rattrapage observations Équipe Beta (3h sans BBS)
3. Formation BBS pour 2 équipes (certification à jour)
4. Ajustement coaching ratio: +2% positif pour atteindre 80/20
5. Capitaliser excellence Équipe Alpha (best practices)

📍 ZONES SURVEILLANCE RENFORCÉE:
• Zone D10-D12: Intervention BBS immédiate requise
• Secteur B: Incident + analyse comportementale en cours
• Équipes Beta/Delta: Surveillance observations renforcée

📈 TENDANCES BBS-ISO INTÉGRÉES:
• Score BBS: +15% amélioration mensuelle 🧠
• Conformité ISO: +8% progression trimestrielle 🏆
• Incidents avec facteur comportemental: -22% ✅
• Participation équipes: +12% engagement volontaire ✅
• Coaching efficacité: 87% (target 90%) 📊

💡 PROCHAINES ÉCHÉANCES BBS-ISO:
• 12:00 - Réunion coordination + Feedback BBS équipes
• 13:30 - Coaching BBS Équipe Delta (programmé)
• 14:15 - Formation équipe Nuit + Module BBS
• 15:30 - Audit ISO Ch.5.4 Participation (préparation)
• 16:00 - Débriefing incidents + Analyse comportementale

🎯 OBJECTIFS SEMAINE BBS-ISO:
• Atteindre 60 observations/jour (actuellement 47)
• Maintenir 90%+ comportements sûrs
• Coaching ratio optimal 80/20
• Conformité ISO maintenir >94%
• Zéro incident avec facteur comportemental

👤 Rapport généré par: Safety Coordinator
🔗 Version: SafetyGraph Industries v3.1 BBS-ISO Enhanced
📍 Site: Enterprise ABC - Construction (SCIAN 236)
⏰ Dernière MAJ: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
🏆 Certification: ISO 45001 en cours (audit Q3 2024)
                """
                
                st.text_area("📄 Rapport Flash BBS-ISO Intégré", flash_report_bbs, height=500, key="flash_bbs_content")
                
                col_export1, col_export2 = st.columns(2)
                with col_export1:
                    st.download_button(
                        label="📥 Export Rapport BBS-ISO",
                        data=flash_report_bbs,
                        file_name=f"rapport_bbs_iso_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True,
                        key="download_flash_bbs"
                    )
                with col_export2:
                    if st.button("📧 Envoyer Management+ISO", use_container_width=True, key="send_management_bbs"):
                        st.success("✅ Rapport BBS-ISO envoyé au management + auditeur ISO !")
                        st.info("📬 Email envoyé à: direction@safetygraph.com, iso.auditor@safetygraph.com")
        
        # === ALERTES CONTEXTUELLES ENRICHIES ===
        st.markdown("### ⚠️ Alertes BBS-ISO")
        st.warning("🧠 Observation BBS due: Équipe Beta (3h)")
        st.info("🎯 Coaching BBS planifié 13h30")
        st.error("🚨 Comportement risqué Zone D - BBS urgent")
        st.success("✅ ISO Ch.5.4: Participation excellente")
    
    # === ONGLETS DÉTAILLÉS ENRICHIS BBS-ISO ===
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Incidents+BBS", "👥 Équipes+Coaching", "📈 Performance BBS", "🏆 Conformité ISO"])
    
    with tab1:
        st.markdown("#### Incidents + Analyse Comportementale")
        
        # Graphique évolution incidents avec facteurs BBS
        fig_incidents = go.Figure()
        fig_incidents.add_trace(go.Scatter(
            x=['Lun', 'Mar', 'Mer', 'Jeu', 'Ven'],
            y=[12, 8, 15, 7, 9],
            mode='lines+markers',
            name='Incidents Total',
            line=dict(color='orange', width=3),
            marker=dict(size=8)
        ))
        fig_incidents.add_trace(go.Scatter(
            x=['Lun', 'Mar', 'Mer', 'Jeu', 'Ven'],
            y=[4, 2, 6, 2, 1],
            mode='lines+markers',
            name='Avec Facteur Comportemental',
            line=dict(color='red', width=2),
            marker=dict(size=6)
        ))
        fig_incidents.update_layout(
            title="Évolution Incidents + Analyse BBS",
            height=300
        )
        st.plotly_chart(fig_incidents, use_container_width=True, key="incidents_bbs_chart")
        
        # Tableau incidents avec analyse BBS
        incidents_bbs_data = {
            'ID': ['INC-BBS-001', 'INC-BBS-002', 'INC-BBS-003'],
            'Zone': ['D10-D12', 'Secteur B', 'Zone C'],
            'Type': ['Chute', 'Équipement', 'Chimique'],
            'Facteur BBS': ['Procédure ignorée', 'Formation insuffisante', 'Aucun'],
            'Coaching': ['✅ Programmé', '🔄 En cours', '❌ Non requis'],
            'Statut': ['Investigation BBS', 'Résolu+Formation', 'Clos']
        }
        st.dataframe(incidents_bbs_data, use_container_width=True)
    
    with tab2:
        st.markdown("#### Gestion Équipes + Coaching BBS")
        
        # Métriques équipes avec BBS
        eq_col1, eq_col2, eq_col3, eq_col4 = st.columns(4)
        with eq_col1:
            st.metric("Équipes Actives", "12/15")
        with eq_col2:
            st.metric("Score BBS Moyen", "85.2%")
        with eq_col3:
            st.metric("Coaching Sessions", "3/jour")
        with eq_col4:
            st.metric("Participation BBS", "94.3%")
        
        # Tableau équipes avec scoring BBS
        teams_bbs_data = {
            'Équipe': ['Alpha', 'Beta', 'Gamma', 'Delta', 'Echo'],
            'Zone': ['A1-A3', 'B4-B6', 'C7-C9', 'D10-D12', 'E13-E15'],
            'Score BBS': ['92.1%', '78.3%', '89.7%', '71.2%', '86.8%'],
            'Observations': ['12/12', '8/12', '11/12', '6/12', '10/12'],
            'Coaching': ['✅ Positif', '⚠️ Requis', '✅ Excellent', '🚨 Urgent', '✅ Bon'],
            'ISO Ch.5.4': ['96%', '89%', '94%', '85%', '92%']
        }
        st.dataframe(teams_bbs_data, use_container_width=True)
    
    with tab3:
        st.markdown("#### Performance BBS Détaillée")
        
        # Graphique comportements sûrs/à risque
        fig_behavior = go.Figure(data=[go.Pie(
            labels=['Comportements Sûrs', 'À Risque', 'Dangereux'],
            values=[88.7, 9.8, 1.5],
            hole=.3,
            marker_colors=['green', 'orange', 'red']
        )])
        fig_behavior.update_layout(
            title="Répartition Comportements Observés (BBS)",
            height=300
        )
        st.plotly_chart(fig_behavior, use_container_width=True, key="behavior_distribution")
        
        # Métriques de coaching
        coaching_col1, coaching_col2, coaching_col3 = st.columns(3)
        with coaching_col1:
            st.metric("Coaching Positif", "78%", delta="Target: 80%")
        with coaching_col2:
            st.metric("Coaching Correctif", "22%", delta="Target: 20%")
        with coaching_col3:
            st.metric("Efficacité Coaching", "87%", delta="Target: 90%")
        
        # Timeline BBS des dernières 24h
        st.markdown("**Timeline BBS - Dernières 24h**")
        bbs_timeline_data = {
            'Heure': ['08:15', '09:30', '10:45', '12:00', '13:30', '14:15', '15:00'],
            'Action BBS': [
                'Observation positive Équipe Alpha',
                'Comportement risqué détecté Zone D',
                'Coaching correctif Équipe Beta',
                'Formation BBS équipe Nuit',
                'Observation excellente Équipe Gamma',
                'Feedback positif donné',
                'Révision procédure Zone C'
            ],
            'Impact': ['+2.3%', '-1.1%', '+1.8%', '+0.5%', '+2.7%', '+1.2%', '+0.8%'],
            'Statut': ['✅ Complété', '🔄 En cours', '✅ Complété', '📚 Planifié', '✅ Complété', '✅ Complété', '📋 En révision']
        }
        st.dataframe(bbs_timeline_data, use_container_width=True)
    
    with tab4:
        st.markdown("#### Conformité ISO 45001 - Intégration BBS")
        
        # Scoring par chapitre ISO 45001
        iso_chapters = [
            {'Chapitre': 'Ch.5 Leadership', 'Score': 96.7, 'BBS Integration': '✅ Leadership visibility tours', 'Statut': '🏆 Excellent'},
            {'Chapitre': 'Ch.5.4 Participation', 'Score': 94.3, 'BBS Integration': '✅ Observations volontaires', 'Statut': '🏆 Excellent'},
            {'Chapitre': 'Ch.7 Communication', 'Score': 93.1, 'BBS Integration': '✅ Feedback immédiat', 'Statut': '✅ Conforme'},
            {'Chapitre': 'Ch.8 Opérations', 'Score': 91.8, 'BBS Integration': '✅ Procédures BBS intégrées', 'Statut': '✅ Conforme'},
            {'Chapitre': 'Ch.9 Performance', 'Score': 95.2, 'BBS Integration': '✅ Monitoring comportemental', 'Statut': '🏆 Excellent'},
            {'Chapitre': 'Ch.10 Amélioration', 'Score': 92.7, 'BBS Integration': '✅ Actions correctives BBS', 'Statut': '✅ Conforme'}
        ]
        
        iso_df = pd.DataFrame(iso_chapters)
        st.dataframe(iso_df, use_container_width=True)
        
        # Graphique radar conformité ISO
        fig_iso = go.Figure()
        
        fig_iso.add_trace(go.Scatterpolar(
            r=[96.7, 94.3, 93.1, 91.8, 95.2, 92.7],
            theta=['Leadership', 'Participation', 'Communication', 'Opérations', 'Performance', 'Amélioration'],
            fill='toself',
            name='Score Actuel',
            line_color='blue'
        ))
        
        fig_iso.add_trace(go.Scatterpolar(
            r=[95, 95, 95, 95, 95, 95],
            theta=['Leadership', 'Participation', 'Communication', 'Opérations', 'Performance', 'Amélioration'],
            fill='toself',
            name='Target ISO',
            line_color='green',
            line=dict(dash='dash')
        ))
        
        fig_iso.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[80, 100]
                )),
            title="Conformité ISO 45001 - Intégration BBS",
            height=400
        )
        st.plotly_chart(fig_iso, use_container_width=True, key="iso_compliance_radar")
        
        # Actions d'amélioration ISO-BBS
        st.markdown("**🎯 Plan d'Action ISO-BBS**")
        st.info("📋 **Ch.8 Opérations** : Intégrer davantage procédures BBS (91.8% → 95%)")
        st.info("📋 **Ch.10 Amélioration** : Systématiser retour d'expérience BBS (92.7% → 95%)")
        st.success("🏆 **Ch.5 Leadership** : Excellence maintenue - Leadership visibility (96.7%)")
        st.success("🏆 **Ch.9 Performance** : Monitoring BBS optimal (95.2%)")
        
        # Prochaines échéances audit ISO
        st.markdown("**📅 Échéances Audit ISO 45001**")
        audit_schedule = {
            'Date': ['15 Août 2024', '22 Août 2024', '29 Août 2024', '05 Sept 2024'],
            'Audit': ['Ch.5 Leadership', 'Ch.5.4 & 7 Participation/Communication', 'Ch.8 & 9 Opérations/Performance', 'Ch.10 Amélioration Continue'],
            'Préparation BBS': ['Tours direction + BBS', 'Observations + Feedback', 'Procédures + Monitoring', 'Actions correctives'],
            'Statut': ['✅ Prêt', '🔄 En préparation', '📋 À préparer', '📋 À préparer']
        }
        st.dataframe(audit_schedule, use_container_width=True)
    
    # === FOOTER AVEC RÉSUMÉ GLOBAL ===
    st.markdown("---")
    st.markdown("### 📈 **Résumé Performance Globale BBS-ISO 45001**")
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        st.markdown("""
        **🧠 Performance BBS**
        - Score global: **85.2%** ↗️
        - Observations: **47/60** (78%)
        - Comportements sûrs: **88.7%** ✅
        - Coaching ratio: **78/22** (→80/20)
        """)
    
    with summary_col2:
        st.markdown("""
        **🏆 Conformité ISO 45001**
        - Score global: **94.3%** ✅
        - Leadership (Ch.5): **96.7%** 🏆
        - Participation (Ch.5.4): **94.3%** ✅
        - Performance (Ch.9): **95.2%** 🏆
        """)
    
    with summary_col3:
        st.markdown("""
        **🎯 Actions Prioritaires**
        - Coaching urgent Zone D10-D12 🚨
        - Rattrapage observations Équipe Beta ⚠️
        - Optimiser ratio coaching 80/20 📊
        - Préparation audit ISO Ch.8-10 📋
        """)
    
    # === BOUTON EXPORT GLOBAL ===
    st.markdown("---")
    if st.button("📊 **EXPORT DASHBOARD COMPLET BBS-ISO**", use_container_width=True, type="primary", key="export_complete_dashboard"):
        
        complete_export = f"""
⚡ DASHBOARD SAFETY COORDINATOR COMPLET - BBS-ISO 45001 INTÉGRÉ
📅 Export généré: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
🏢 SafetyGraph Industries - Enterprise ABC - Safety Coordinator Operations

═══════════════════════════════════════════════════════════════════

📊 MÉTRIQUES PRINCIPALES CONSOLIDÉES:
• Incidents actifs: 7 (-2 vs hier)
• Compliance ISO 45001: 94.3% (+1.8% mensuel)
• BBS Score global: 85.2% (+2.1% amélioration)
• Équipes actives: 12/15 (80% opérationnel)
• Temps résolution: 2.4h (-0.3h amélioration)

🧠 PERFORMANCE BBS DÉTAILLÉE:
• Observations réalisées: 47/60 (78% objectif quotidien)
• Comportements sûrs: 88.7% (+3.2% vs semaine dernière)
• Feedback moyen: 12 min (-3 min amélioration)
• Coaching ratio: 78/22 (Target 80/20)
• Sessions coaching programmées: 3 aujourd'hui

🏆 CONFORMITÉ ISO 45001 DÉTAILLÉE:
• Ch.5 Leadership: 96.7% - Leadership visibility excellent
• Ch.5.4 Participation: 94.3% - BBS favorise implication
• Ch.7 Communication: 93.1% - Feedback BBS efficace
• Ch.8 Opérations: 91.8% - Procédures BBS intégrées
• Ch.9 Performance: 95.2% - Monitoring continu
• Ch.10 Amélioration: 92.7% - Actions correctives systématiques

🎯 PERFORMANCE PAR ÉQUIPE:
• Équipe Alpha (A1-A3): 92.1% BBS - ✅ Excellence
• Équipe Beta (B4-B6): 78.3% BBS - ⚠️ Amélioration requise
• Équipe Gamma (C7-C9): 89.7% BBS - ✅ Très bon
• Équipe Delta (D10-D12): 71.2% BBS - 🚨 Intervention urgente
• Équipe Echo (E13-E15): 86.8% BBS - ✅ Bon niveau

🚨 ALERTES ET ACTIONS CRITIQUES:
• Zone D10-D12: Comportement risqué - Coaching BBS urgent
• Équipe Beta: 3h sans observation - Rattrapage immédiat
• Ratio coaching: Ajustement +2% positif requis (78→80%)
• Formation BBS: 2 équipes nécessitent mise à niveau

📅 PLANNING ACTIONS BBS-ISO:
• 12:00 - Réunion coordination + Feedback BBS équipes
• 13:30 - Coaching BBS urgent Équipe Delta
• 14:15 - Formation équipe Nuit + Module BBS
• 15:30 - Audit ISO Ch.5.4 préparation
• 16:00 - Débriefing incidents + Analyse comportementale

📈 TENDANCES ÉVOLUTION (30 jours):
• Score BBS: +15% amélioration progressive
• Conformité ISO: +8% progression trimestrielle
• Incidents comportementaux: -22% réduction
• Participation volontaire: +12% engagement
• Efficacité coaching: 87% (target 90%)

🎯 OBJECTIFS SEMAINE BBS-ISO:
• Atteindre 60 observations/jour (actuellement 47)
• Maintenir 90%+ comportements sûrs
• Optimiser coaching ratio 80/20
• Conformité ISO >94% tous chapitres
• Zéro incident avec facteur comportemental

🏆 CERTIFICATION ISO 45001:
• Statut: En cours de certification
• Audit prévu: Q3 2024 (Août-Septembre)
• Préparation: 94.3% conforme
• Points forts: Leadership + Performance + BBS
• Points amélioration: Opérations + Amélioration continue

═══════════════════════════════════════════════════════════════════

👤 Dashboard généré par: Safety Coordinator
🔗 Version: SafetyGraph Industries v3.1 BBS-ISO Enhanced
📍 Site: Enterprise ABC - Construction (SCIAN 236)
⏰ Export: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
🌐 Plateforme: SafetyGraph Industries + Culture SST + BehaviorX
        """
        
        st.success("✅ Export dashboard complet BBS-ISO 45001 généré avec succès !")
        
        st.download_button(
            label="📥 **TÉLÉCHARGER DASHBOARD COMPLET BBS-ISO**",
            data=complete_export,
            file_name=f"dashboard_safety_coordinator_bbs_iso_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_complete_dashboard"
        )
        
        st.balloons()
        st.success("🎉 **Dashboard Safety Coordinator BBS-ISO 45001 - Version Révolutionnaire Prête !**")