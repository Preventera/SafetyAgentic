"""
Dashboard Safety Coordinator - Mode Operations
Version COMPLÈTE - Actions Rapides avec génération de rapports intégrée
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

def display_safety_coordinator_dashboard(config):
    """Dashboard Safety Coordinator - Mode Operations avec Actions Rapides et Rapports Complets"""
    
    # Header professionnel avec contexte opérationnel
    st.markdown("## ⚡ Safety Coordinator Operations Dashboard")
    st.markdown("*Mode Opérationnel - Coordination terrain et incidents*")
    
    # === MÉTRIQUES TEMPS RÉEL ===
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🚨 Incidents Actifs", "7", delta="-2")
    
    with col2:
        st.metric("📊 Compliance", "91%", delta="3%")
    
    with col3:
        st.metric("👥 Équipes Actives", "12/15", delta="2")
    
    with col4:
        st.metric("⏱️ Temps Moyen Résolution", "2.4h", delta="-0.3h")
    
    # === LAYOUT PRINCIPAL ===
    col_main, col_actions = st.columns([2, 1])
    
    with col_main:
        # === TIMELINE INTERACTIVE AMÉLIORÉE ===
        st.markdown("### 📅 Timeline Opérationnelle")
        
        # Timeline avec composants natifs Streamlit - Plus lisible
        timeline_events = [
            {"time": "08:15", "event": "Inspection Zone A terminée", "status": "✅ TERMINÉ", "priority": "success"},
            {"time": "09:30", "event": "Incident mineur Secteur B", "status": "🔄 EN COURS", "priority": "warning"},
            {"time": "10:45", "event": "Formation équipe Nuit", "status": "📚 PLANIFIÉ", "priority": "info"},
            {"time": "11:20", "event": "Maintenance préventive", "status": "⚡ URGENT", "priority": "error"},
            {"time": "12:00", "event": "Réunion coordination", "status": "📅 PROGRAMMÉ", "priority": "info"}
        ]
        
        for event in timeline_events:
            if event["priority"] == "error":
                st.error(f"**{event['time']}** - {event['event']} - {event['status']}")
            elif event["priority"] == "warning":
                st.warning(f"**{event['time']}** - {event['event']} - {event['status']}")
            elif event["priority"] == "success":
                st.success(f"**{event['time']}** - {event['event']} - {event['status']}")
            else:
                st.info(f"**{event['time']}** - {event['event']} - {event['status']}")
    
    with col_actions:
        # === ACTIONS RAPIDES AVEC GÉNÉRATION DE RAPPORTS COMPLÈTE ===
        st.markdown("### 🎯 Actions Rapides")
        
        # 1. DÉCLARER INCIDENT avec formulaire intégré
        if st.button("🚨 Déclarer Incident", use_container_width=True, type="primary", key="safety_coord_incident"):
            st.balloons()
            st.success("✅ Formulaire incident Safety Coordinator ouvert !")
            
            # Mini-formulaire incident rapide
            with st.expander("📋 Saisie Rapide Incident", expanded=True):
                col_form1, col_form2 = st.columns(2)
                with col_form1:
                    incident_type = st.selectbox("Type", ["Chute", "Équipement", "Chimique", "Autre"], key="inc_type")
                    severity = st.selectbox("Gravité", ["🔴 Critique", "🟡 Modéré", "🟢 Mineur"], key="inc_severity")
                with col_form2:
                    location = st.text_input("Zone", placeholder="Ex: Secteur A-12", key="inc_location")
                    time_reported = st.time_input("Heure", key="inc_time")
                
                description = st.text_area("Description rapide", placeholder="Détails de l'incident...", key="inc_desc")
                
                if st.button("📤 Envoyer Rapport", use_container_width=True, key="send_incident_report"):
                    # Génération du rapport incident
                    incident_report = f"""
🚨 RAPPORT INCIDENT - {datetime.now().strftime('%d/%m/%Y %H:%M')}

📍 Zone: {location}
🕐 Heure: {time_reported}
⚠️ Type: {incident_type}
🎯 Gravité: {severity}

📝 Description:
{description}

👤 Rapporté par: Safety Coordinator
🔗 ID: INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}
📍 Localisation GPS: 45.5017° N, 73.5673° W
🏢 Site: SafetyGraph Industries - Enterprise ABC
                    """
                    
                    st.success("✅ Rapport incident généré et envoyé au management !")
                    st.download_button(
                        label="📥 Télécharger Rapport Incident",
                        data=incident_report,
                        file_name=f"incident_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="download_incident"
                    )
        
        # 2. STATUT ÉQUIPES avec détails temps réel
        if st.button("👥 Statut Équipes Live", use_container_width=True, key="safety_coord_teams"):
            st.success("✅ Vue temps réel équipes Safety Coordinator !")
            
            with st.expander("📊 Détail Équipes Actives", expanded=True):
                teams_data = {
                    'Équipe': ['Alpha', 'Beta', 'Gamma', 'Delta', 'Echo'],
                    'Zone': ['A1-A3', 'B4-B6', 'C7-C9', 'D10-D12', 'E13-E15'],
                    'Statut': ['🟢 Actif', '🟡 Pause', '🟢 Actif', '🔴 Urgence', '🟢 Actif'],
                    'Dernière MAJ': ['08:45', '09:12', '08:52', '09:05', '08:38']
                }
                st.dataframe(teams_data, use_container_width=True)
                
                # Bouton génération rapport équipes
                if st.button("📊 Générer Rapport Équipes", key="gen_team_report"):
                    team_report = f"""
👥 RAPPORT ÉQUIPES - {datetime.now().strftime('%d/%m/%Y %H:%M')}

📈 STATISTIQUES:
• Équipes actives: 4/5 (80%)
• Équipes en pause: 1/5 (20%)
• Situations urgentes: 1

📍 DÉTAIL PAR ÉQUIPE:
• Alpha (A1-A3): Actif - Inspection routine
• Beta (B4-B6): Pause - Rotation équipe
• Gamma (C7-C9): Actif - Formation terrain
• Delta (D10-D12): URGENCE - Incident en cours
• Echo (E13-E15): Actif - Maintenance préventive

🚨 ALERTES:
• Équipe Delta nécessite assistance immédiate
• Beta en retard de 15 minutes sur planning
• 2 équipes dépassent quota heures supplémentaires

⏰ Rapport généré: {datetime.now().strftime('%d/%m/%Y à %H:%M')}
👤 Par: Safety Coordinator
🏢 Site: SafetyGraph Industries - Enterprise ABC
                    """
                    
                    st.download_button(
                        label="📥 Télécharger Rapport Équipes",
                        data=team_report,
                        file_name=f"rapport_equipes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="download_teams"
                    )
        
        # 3. FORMATIONS avec planning automatique
        if st.button("📚 Formations Urgentes", use_container_width=True, key="safety_coord_training"):
            st.warning("⚠️ 5 certifications expirent cette semaine")
            st.success("✅ Module formations Safety Coordinator activé !")
            
            with st.expander("📅 Planning Formation Automatique", expanded=True):
                formations_data = {
                    'Employé': ['Jean D.', 'Marie L.', 'Pierre M.', 'Sophie R.', 'Luc B.'],
                    'Formation': ['Hauteur', 'CNESST', 'Chimique', 'Secours', 'Équipement'],
                    'Expiration': ['28/07', '29/07', '30/07', '31/07', '01/08'],
                    'Priorité': ['🔴 Urgent', '🔴 Urgent', '🟡 Élevé', '🟡 Élevé', '🟢 Normal']
                }
                st.dataframe(formations_data, use_container_width=True)
                
                if st.button("📋 Générer Plan Formation", key="gen_training_plan"):
                    training_report = f"""
📚 PLAN FORMATION URGENT - {datetime.now().strftime('%d/%m/%Y')}

🚨 CERTIFICATIONS EXPIRANTES:

🔴 PRIORITÉ CRITIQUE (48h):
• Jean D. - Formation Hauteur (expire 28/07)
• Marie L. - Certification CNESST (expire 29/07)

🟡 PRIORITÉ ÉLEVÉE (cette semaine):
• Pierre M. - Formation Chimique (expire 30/07)
• Sophie R. - Formation Secours (expire 31/07)

🟢 PRIORITÉ NORMALE (semaine prochaine):
• Luc B. - Formation Équipement (expire 01/08)

📅 PLANNING PROPOSÉ:
• Lundi 28/07: Formation Hauteur (Jean D.) - Salle A, 9h-12h
• Mardi 29/07: Certification CNESST (Marie L.) - Salle B, 8h-17h
• Mercredi 30/07: Formation Chimique (Pierre M.) - Labo C, 13h-16h
• Jeudi 31/07: Formation Secours (Sophie R.) - Terrain, 9h-15h
• Vendredi 01/08: Formation Équipement (Luc B.) - Atelier D, 14h-17h

💰 COÛT ESTIMÉ: 3,250$ CAD
👥 FORMATEURS REQUIS: 3 internes + 2 externes
📋 MATÉRIEL: Équipement spécialisé + Manuels CNESST

👤 Plan généré par: Safety Coordinator
⏰ Le: {datetime.now().strftime('%d/%m/%Y à %H:%M')}
🏢 Site: SafetyGraph Industries - Enterprise ABC
                    """
                    
                    st.download_button(
                        label="📥 Télécharger Plan Formation",
                        data=training_report,
                        file_name=f"plan_formation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="download_training"
                    )
        
        # 4. RAPPORT FLASH avec synthèse opérationnelle complète
        if st.button("📊 Rapport Flash", use_container_width=True, key="safety_coord_report"):
            st.success("✅ Génération rapport Safety Coordinator !")
            
            with st.expander("📈 Rapport Flash - Synthèse Opérationnelle", expanded=True):
                # Génération automatique du rapport flash
                flash_report = f"""
⚡ RAPPORT FLASH OPÉRATIONNEL
📅 {datetime.now().strftime('%d/%m/%Y à %H:%M')}
🏢 SafetyGraph Industries - Enterprise ABC

📊 MÉTRIQUES TEMPS RÉEL:
• Incidents actifs: 7 (-2 vs hier) ✅
• Compliance: 91% (+3% ce mois) ✅
• Équipes actives: 12/15 (80% opérationnel)
• Temps résolution moyen: 2.4h (-0.3h amélioration) ✅

🚨 SITUATIONS CRITIQUES:
• 1 maintenance préventive urgente (11:20) - Zone industrielle
• 2 équipes en retard sur inspections (Beta, Delta)
• 5 certifications expirent cette semaine
• Équipe Delta en situation d'urgence - Zone D10-D12

✅ POINTS POSITIFS:
• Inspection Zone A terminée avec succès (08:15)
• Formation équipe Nuit planifiée (10:45)
• Amélioration temps résolution (-0.3h vs moyenne)
• Compliance en hausse (+3% mensuel)

🎯 ACTIONS RECOMMANDÉES:
1. Traiter maintenance urgente prioritaire (délai: 2h)
2. Rattrapage inspections équipes Beta/Delta (planning ajusté)
3. Planifier formations certifications expirantes (5 employés)
4. Assistance immédiate équipe Delta - Zone D10-D12
5. Maintenir cadence résolution incidents

📍 ZONES À SURVEILLER:
• Secteur B: Incident mineur en cours (09:30)
• Zone D10-D12: Équipe Delta en situation urgente
• Atelier maintenance: Intervention préventive urgente

📈 TENDANCES:
• Incidents: Baisse 22% cette semaine ✅
• Formations: 85% planning respecté ✅
• Temps résolution: Amélioration constante ✅
• Équipes: Rotation optimisée 📊

💡 PROCHAINES ÉCHÉANCES:
• 12:00 - Réunion coordination équipes
• 14:00 - Formation sécurité équipe Nuit
• 15:30 - Inspection routine Secteur C
• 16:00 - Débriefing incidents journée

👤 Rapport généré par: Safety Coordinator
🔗 Version: SafetyGraph Industries v3.1
📍 Localisation: Site Enterprise ABC - Construction générale (236)
⏰ Dernière MAJ: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
                """
                
                st.text_area("📄 Contenu du Rapport Flash", flash_report, height=400, key="flash_content")
                
                col_export1, col_export2 = st.columns(2)
                with col_export1:
                    st.download_button(
                        label="📥 Export TXT",
                        data=flash_report,
                        file_name=f"rapport_flash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True,
                        key="download_flash"
                    )
                with col_export2:
                    # Simulation envoi email management
                    if st.button("📧 Envoyer Management", use_container_width=True, key="send_management"):
                        st.success("✅ Rapport envoyé au management !")
                        st.info("📬 Email envoyé à: direction@safetygraph.com")
        
        # === ALERTES CONTEXTUELLES ===
        st.markdown("### ⚠️ Alertes")
        st.warning("2 équipes en retard sur inspections")
        st.info("Formation sécurité planifiée 14h")
        st.error("Maintenance urgente Zone D - Action requise")
    
    # === ONGLETS DÉTAILLÉS ===
    tab1, tab2, tab3 = st.tabs(["📊 Incidents", "👥 Équipes", "📈 Performance"])
    
    with tab1:
        st.markdown("#### Incidents en Cours")
        
        # Graphique évolution incidents
        fig_incidents = go.Figure()
        fig_incidents.add_trace(go.Scatter(
            x=['Lun', 'Mar', 'Mer', 'Jeu', 'Ven'],
            y=[12, 8, 15, 7, 9],
            mode='lines+markers',
            name='Incidents',
            line=dict(color='orange', width=3),
            marker=dict(size=8)
        ))
        fig_incidents.update_layout(
            title="Évolution Incidents Semaine",
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig_incidents, use_container_width=True, key="safety_coord_incidents_chart")
        
        # Tableau incidents détaillés
        incidents_data = {
            'ID': ['INC-2025-001', 'INC-2025-002', 'INC-2025-003'],
            'Zone': ['Secteur A', 'Secteur B', 'Zone C'],
            'Type': ['Chute', 'Équipement', 'Chimique'],
            'Priorité': ['🔴 Haute', '🟡 Moyenne', '🔴 Haute'],
            'Statut': ['En cours', 'Résolu', 'Investigation']
        }
        st.dataframe(incidents_data, use_container_width=True)
    
    with tab2:
        st.markdown("#### Gestion Équipes")
        
        # Métriques équipes
        eq_col1, eq_col2, eq_col3 = st.columns(3)
        with eq_col1:
            st.metric("Équipes Jour", "8/10")
        with eq_col2:
            st.metric("Équipes Nuit", "4/5")
        with eq_col3:
            st.metric("Disponibilité", "85%")
        
        # Planning équipes simplifié
        st.markdown("**Planning du Jour:**")
        st.success("✅ Équipe Alpha - Zone 1-3 (8h-16h)")
        st.warning("⚠️ Équipe Beta - Zone 4-6 (9h-17h) - Retard")
        st.info("📍 Équipe Gamma - Zone 7-9 (10h-18h)")
        st.error("🚨 Équipe Delta - Zone 10-12 (Emergency)")
    
    with tab3:
        st.markdown("#### Performance Opérationnelle")
        
        # Graphique répartition types incidents
        fig_types = go.Figure(data=[go.Pie(
            labels=['Chutes', 'Équipement', 'Chimique', 'Autre'],
            values=[35, 25, 20, 20],
            hole=.3,
            marker_colors=['red', 'orange', 'yellow', 'blue']
        )])
        fig_types.update_layout(
            title="Répartition Types d'Incidents",
            height=300
        )
        st.plotly_chart(fig_types, use_container_width=True, key="safety_coord_types_chart")
        
        # Tableau temps de résolution
        resolution_data = {
            'Période': ['Cette semaine', 'Semaine dernière', 'Moyenne mensuelle'],
            'Temps Moyen': ['2.4h', '2.7h', '3.1h'],
            'Incidents': [7, 12, 45],
            'Tendance': ['📈 +10%', '📉 -15%', '📊 Stable']
        }
        st.dataframe(resolution_data, use_container_width=True)