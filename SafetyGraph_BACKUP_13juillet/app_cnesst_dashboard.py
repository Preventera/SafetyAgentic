"""
SafetyGraph CNESST Dashboard - Module Expert
===========================================

Module d'administration expert pour 104 agents SafetyGraph
avec enrichissement CNESST complet et analytics sectoriels.

Author: Mario Genest - GenAISafety
Date: 11 juillet 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time
import logging
from pathlib import Path

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration Streamlit
st.set_page_config(
    page_title="SafetyGraph CNESST - Expert Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Mobile-First
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2980b9 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2980b9;
        margin-bottom: 1rem;
    }
    
    .agent-status-active {
        color: #27ae60;
        font-weight: bold;
    }
    
    .agent-status-idle {
        color: #f39c12;
        font-weight: bold;
    }
    
    .agent-status-error {
        color: #e74c3c;
        font-weight: bold;
    }
    
    .alert-critical {
        background: #fee;
        border: 1px solid #fcc;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 0.9rem;
            padding: 0.8rem;
        }
        
        .metric-card {
            padding: 0.8rem;
            font-size: 0.9rem;
        }
    }
</style>
""", unsafe_allow_html=True)

class CNESSTDashboard:
    """Dashboard principal CNESST SafetyGraph"""
    
    def __init__(self):
        self.initialize_data()
        self.load_agent_configs()
        
    def initialize_data(self):
        """Initialisation données système"""
        
        # Secteurs SCIAN supportés
        self.scian_sectors = {
            "23": "Construction",
            "236": "Construction bâtiments résidentiels", 
            "237": "Construction ouvrages génie civil",
            "238": "Entrepreneurs spécialisés",
            "238110": "Entrepreneurs fondations/structure béton",
            "62": "Soins santé et assistance sociale",
            "621": "Services soins santé ambulatoires",
            "622": "Hôpitaux",
            "623": "Établissements soins infirmiers",
            "48": "Transport et entreposage",
            "484": "Transport par camion",
            "44": "Commerce de détail",
            "445": "Magasins alimentation",
            "72": "Hébergement et restauration"
        }
        
        # Données CNESST exemple (secteur 238110)
        self.cnesst_benchmark = {
            "238110": {
                "total_absence_days": 209907,
                "total_injuries": 924,
                "average_absence": 227,
                "risk_distribution": {
                    "effort_excessif": 16.7,
                    "reaction_corps": 15.0,
                    "frappe_objet": 14.3,
                    "chute_niveau": 12.8,
                    "chute_meme_niveau": 12.4
                },
                "top_professions": {
                    "charpentiers": {"days": 46815, "injuries": 247, "avg": 190},
                    "manoeuvres_maintenance": {"days": 29209, "injuries": 122, "avg": 239},
                    "manoeuvres_batiment": {"days": 25962, "injuries": 87, "avg": 298}
                }
            }
        }
        
    def load_agent_configs(self):
        """Chargement configuration 104 agents"""
        
        self.agents_config = {
            # Agents Core (4)
            "R1": {"name": "Router Agent", "status": "active", "sector": "core", "performance": 94.2},
            "C1": {"name": "Context Agent", "status": "active", "sector": "core", "performance": 91.8},
            "A1": {"name": "Collecte Autoeval", "status": "active", "sector": "core", "performance": 89.3},
            "A2": {"name": "Collecte Observations", "status": "active", "sector": "core", "performance": 92.1},
            
            # Agents Sectoriels Construction (10)
            "SC23": {"name": "Construction Global", "status": "active", "sector": "23", "performance": 94.2},
            "SC236": {"name": "Bâtiments Résidentiels", "status": "active", "sector": "236", "performance": 88.7},
            "SC237": {"name": "Génie Civil", "status": "idle", "sector": "237", "performance": 91.2},
            "SC238": {"name": "Entrepreneurs Spécialisés", "status": "overload", "sector": "238", "performance": 87.1},
            "SC238110": {"name": "Fondations Béton", "status": "active", "sector": "238110", "performance": 89.8},
            
            # Agents Sectoriels Santé (8) 
            "SC62": {"name": "Santé Global", "status": "idle", "sector": "62", "performance": 91.8},
            "SC621": {"name": "Soins Ambulatoires", "status": "active", "sector": "621", "performance": 89.3},
            "SC622": {"name": "Hôpitaux", "status": "active", "sector": "622", "performance": 92.1},
            "SC623": {"name": "Soins Infirmiers", "status": "active", "sector": "623", "performance": 88.9},
            
            # Agents Sectoriels Transport (6)
            "SC48": {"name": "Transport Global", "status": "active", "sector": "48", "performance": 85.4},
            "SC484": {"name": "Transport Camion", "status": "active", "sector": "484", "performance": 87.2},
            
            # Agents Sectoriels Commerce (8)
            "SC44": {"name": "Commerce Détail", "status": "active", "sector": "44", "performance": 83.1},
            "SC445": {"name": "Magasins Alimentation", "status": "idle", "sector": "445", "performance": 86.7},
            
            # Agents Analytics (15)
            "AN1": {"name": "Analyste Écarts", "status": "active", "sector": "analytics", "performance": 91.2},
            "AN2": {"name": "Pattern Recognition", "status": "active", "sector": "analytics", "performance": 88.9},
            "AN3": {"name": "Anomaly Detection", "status": "active", "sector": "analytics", "performance": 90.1},
            "AN4": {"name": "Predictive Models", "status": "active", "sector": "analytics", "performance": 87.8},
            
            # Agents Recommandations (12)
            "R1": {"name": "Générateur Recommandations", "status": "active", "sector": "recommendations", "performance": 93.4},
            "R2": {"name": "Evidence-Based Actions", "status": "active", "sector": "recommendations", "performance": 89.7},
            
            # Agents STORM Research (5)
            "ST1": {"name": "STORM Knowledge", "status": "active", "sector": "research", "performance": 94.8},
            "ST2": {"name": "Scientific Citations", "status": "active", "sector": "research", "performance": 91.3}
        }
        
        # Génération agents restants pour atteindre 104
        additional_sectors = ["311", "312", "321", "322", "331", "332", "411", "412", "441", "442", 
                            "451", "452", "453", "454", "481", "482", "483", "485", "486", "487",
                            "511", "512", "515", "517", "518", "519", "521", "522", "523", "524",
                            "531", "532", "533", "541", "542", "543", "544", "545", "546", "547",
                            "561", "562", "611", "612", "613", "621", "711", "712", "713", "721",
                            "722", "811", "812", "813", "814", "911", "912", "913", "914", "919"]
        
        for i, sector in enumerate(additional_sectors[:60]):  # Compléter jusqu'à 104
            agent_id = f"SC{sector}"
            if agent_id not in self.agents_config:
                self.agents_config[agent_id] = {
                    "name": f"Agent Secteur {sector}",
                    "status": "generated" if i < 40 else "pending",
                    "sector": sector,
                    "performance": round(85 + (i % 10), 1)
                }

def create_header():
    """Header principal dashboard"""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 SafetyGraph CNESST - Administration Expert</h1>
        <p>👤 Mario Genest • 🏭 104 Agents SafetyGraph • ⚡ Temps réel</p>
    </div>
    """, unsafe_allow_html=True)

def tab_vue_ensemble(dashboard):
    """Tab 1: Vue d'ensemble système"""
    
    st.header("📊 Métriques Système Temps Réel")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    # Calcul métriques
    active_agents = len([a for a in dashboard.agents_config.values() if a["status"] == "active"])
    total_agents = len(dashboard.agents_config)
    avg_performance = sum([a["performance"] for a in dashboard.agents_config.values()]) / total_agents
    
    with col1:
        st.metric(
            "🤖 Agents Actifs", 
            f"{active_agents}/{total_agents}",
            f"{round((active_agents/total_agents)*100, 1)}%"
        )
    
    with col2:
        st.metric(
            "📈 Analyses/Jour", 
            "234",
            "+12%"
        )
    
    with col3:
        st.metric(
            "🎯 Précision Globale", 
            f"{round(avg_performance, 1)}%",
            "+2.1%"
        )
    
    with col4:
        st.metric(
            "⚡ Latence P95", 
            "1.8s",
            "-0.3s"
        )
    
    # Alertes prioritaires
    st.subheader("🚨 Alertes Prioritaires")
    
    alerts = [
        ("🔴 CRITIQUE", "Agent SC238 (Construction): Surcharge 156% capacité"),
        ("🟡 ATTENTION", "Secteur SCIAN 621 (Santé): Nouveau pattern détecté"),
        ("🔵 INFO", "Base CNESST: Mise à jour disponible (lesions-2024.csv)")
    ]
    
    for severity, message in alerts:
        st.markdown(f"""
        <div class="alert-critical">
            <strong>{severity}</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    
    # Actions rapides
    st.subheader("🔥 Actions Rapides")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⚡ Lancer Analyse Secteur"):
            st.success("Analyse secteur lancée!")
    
    with col2:
        if st.button("🔄 Sync Données CNESST"):
            st.info("Synchronisation en cours...")
    
    with col3:
        if st.button("📊 Rapport Performance"):
            st.info("Génération rapport...")
    
    with col4:
        if st.button("🎯 Calibrage Agents"):
            st.info("Calibrage en cours...")
    
    # Graphique performance temps réel
    st.subheader("📈 Performance Agents Temps Réel")
    
    # Données simulées pour graphique
    agents_data = []
    for agent_id, config in list(dashboard.agents_config.items())[:20]:  # Top 20
        agents_data.append({
            "Agent": agent_id,
            "Performance": config["performance"],
            "Secteur": config["sector"],
            "Statut": config["status"]
        })
    
    df_agents = pd.DataFrame(agents_data)
    
    fig = px.scatter(
        df_agents,
        x="Agent",
        y="Performance", 
        color="Statut",
        size="Performance",
        hover_data=["Secteur"],
        title="Performance vs Agents (Top 20)"
    )
    
    fig.update_layout(
        xaxis_tickangle=45,
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def tab_agents_management(dashboard):
    """Tab 2: Administration agents"""
    
    st.header("🤖 Administration 104 Agents SafetyGraph")
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "Statut", 
            ["Tous", "active", "idle", "overload", "generated", "pending", "error"]
        )
    
    with col2:
        sector_filter = st.selectbox(
            "Secteur",
            ["Tous"] + list(set([a["sector"] for a in dashboard.agents_config.values()]))
        )
    
    with col3:
        performance_filter = st.slider("Performance min (%)", 0, 100, 80)
    
    # Application filtres
    filtered_agents = {}
    for agent_id, config in dashboard.agents_config.items():
        
        # Filtre statut
        if status_filter != "Tous" and config["status"] != status_filter:
            continue
            
        # Filtre secteur
        if sector_filter != "Tous" and config["sector"] != sector_filter:
            continue
            
        # Filtre performance
        if config["performance"] < performance_filter:
            continue
            
        filtered_agents[agent_id] = config
    
    st.write(f"📊 {len(filtered_agents)} agents affichés sur {len(dashboard.agents_config)} total")
    
    # Tableau agents
    if filtered_agents:
        
        agents_data = []
        for agent_id, config in filtered_agents.items():
            
            # Statut avec couleur
            status_emoji = {
                "active": "🟢",
                "idle": "🟡", 
                "overload": "🔴",
                "generated": "🔵",
                "pending": "⚪",
                "error": "❌"
            }.get(config["status"], "❓")
            
            agents_data.append({
                "ID": agent_id,
                "Nom": config["name"],
                "Statut": f"{status_emoji} {config['status'].upper()}",
                "Secteur": config["sector"],
                "Performance": f"{config['performance']}%",
                "Dernière Activité": "2024-07-11 14:23"
            })
        
        df_agents = pd.DataFrame(agents_data)
        
        # Affichage avec sélection
        selected_agent = st.selectbox(
            "Sélectionner agent pour détails:",
            options=list(filtered_agents.keys()),
            format_func=lambda x: f"{x} - {filtered_agents[x]['name']}"
        )
        
        # Détails agent sélectionné
        if selected_agent:
            agent_config = filtered_agents[selected_agent]
            
            st.subheader(f"📈 Détails Agent: {selected_agent}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Performance", f"{agent_config['performance']}%")
                st.metric("Statut", agent_config['status'])
            
            with col2:
                st.metric("Analyses 24h", "156")
                st.metric("Temps Réponse", "2.3s")
            
            with col3:
                st.metric("Précision", "87.1%")
                st.metric("Satisfaction", "4.2/5")
            
            # Actions agent
            st.subheader("⚙️ Actions Agent")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("🔄 Redémarrer"):
                    st.success(f"Agent {selected_agent} redémarré!")
            
            with col2:
                if st.button("⏸️ Suspendre"):
                    st.info(f"Agent {selected_agent} suspendu")
            
            with col3:
                if st.button("📊 Logs"):
                    st.info("Affichage logs...")
            
            with col4:
                if st.button("⚙️ Configurer"):
                    st.info("Configuration agent...")
        
        # Tableau global
        st.subheader("📋 Liste Complète")
        st.dataframe(df_agents, use_container_width=True)

def tab_scian_analytics(dashboard):
    """Tab 3: Analytics secteurs SCIAN"""
    
    st.header("📊 Analytics Secteurs SCIAN Détaillés")
    
    # Sélection secteur
    col1, col2 = st.columns(2)
    
    with col1:
        selected_sector = st.selectbox(
            "Secteur SCIAN:",
            options=list(dashboard.scian_sectors.keys()),
            format_func=lambda x: f"{x} - {dashboard.scian_sectors[x]}"
        )
    
    with col2:
        if selected_sector in dashboard.cnesst_benchmark:
            st.success(f"✅ Données CNESST disponibles pour {selected_sector}")
        else:
            st.warning(f"⚠️ Données CNESST non disponibles pour {selected_sector}")
    
    # Données CNESST si disponibles
    if selected_sector in dashboard.cnesst_benchmark:
        
        benchmark_data = dashboard.cnesst_benchmark[selected_sector]
        
        st.subheader(f"📊 Données CNESST Secteur {selected_sector}")
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Jours Absence",
                f"{benchmark_data['total_absence_days']:,}"
            )
        
        with col2:
            st.metric(
                "Total Lésions",
                f"{benchmark_data['total_injuries']:,}"
            )
        
        with col3:
            st.metric(
                "Moyenne/Lésion",
                f"{benchmark_data['average_absence']}j"
            )
        
        with col4:
            st.metric(
                "Indice Gravité",
                f"{round(benchmark_data['average_absence']/200*100)}%"
            )
        
        # Graphique distribution risques
        st.subheader("🎯 Distribution Risques Secteur")
        
        risk_data = benchmark_data['risk_distribution']
        
        fig_risks = px.pie(
            values=list(risk_data.values()),
            names=list(risk_data.keys()),
            title=f"Répartition Risques - Secteur {selected_sector}"
        )
        
        st.plotly_chart(fig_risks, use_container_width=True)
        
        # Top professions
        if 'top_professions' in benchmark_data:
            st.subheader("👷 Professions les Plus Touchées")
            
            prof_data = benchmark_data['top_professions']
            
            professions = []
            for prof, data in prof_data.items():
                professions.append({
                    "Profession": prof.replace("_", " ").title(),
                    "Jours Absence": f"{data['days']:,}",
                    "Nb Lésions": data['injuries'],
                    "Moyenne": f"{data['avg']}j"
                })
            
            df_prof = pd.DataFrame(professions)
            st.dataframe(df_prof, use_container_width=True)
    
    else:
        st.info(f"Secteur {selected_sector} en cours d'intégration. Données disponibles bientôt.")
        
        # Simulation données génériques
        st.subheader("📈 Données Estimées")
        st.write("Basées sur secteurs similaires et moyennes nationales")
        
        # Graphique simulé
        simulated_risks = {
            "TMS": 25.0,
            "Chutes": 20.0, 
            "Coupures": 15.0,
            "Brûlures": 12.0,
            "Autres": 28.0
        }
        
        fig_sim = px.bar(
            x=list(simulated_risks.keys()),
            y=list(simulated_risks.values()),
            title=f"Estimation Risques - Secteur {selected_sector}"
        )
        
        st.plotly_chart(fig_sim, use_container_width=True)

def tab_performance_pipeline(dashboard):
    """Tab 4: Performance pipeline"""
    
    st.header("⚡ Monitoring Pipeline 25→104 Agents")
    
    # Progression globale
    total_agents = 104
    current_agents = len([a for a in dashboard.agents_config.values() if a["status"] in ["active", "idle", "overload"]])
    progress = current_agents / total_agents
    
    st.progress(progress)
    st.write(f"📊 Progression: {current_agents}/{total_agents} agents ({round(progress*100, 1)}%)")
    
    # Métriques pipeline
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📈 Métriques Temps Réel")
        st.metric("Throughput", "42 req/s")
        st.metric("Latence P95", "1.8s ✅")
        st.metric("Disponibilité", "99.7% ✅")
    
    with col2:
        st.subheader("🔄 Génération Auto")
        st.metric("Agents générés", f"{current_agents-25}/79")
        st.metric("Template base", "agent_a2_config")
        st.metric("Prochains", "SC311, SC312")
    
    with col3:
        st.subheader("🎯 Qualité")
        st.metric("Tests réussis", "156/164 (95.1%)")
        st.metric("Précision moy", "88.7% ✅")
        st.metric("Erreurs 24h", "3 (non-critiques)")
    
    # Graphique génération agents
    st.subheader("📊 Évolution Génération Agents")
    
    # Données simulées évolution
    dates = pd.date_range(start="2024-07-01", end="2024-07-11", freq="D")
    agents_generated = [25, 28, 32, 35, 41, 48, 56, 63, 72, 81, current_agents]
    
    fig_evolution = px.line(
        x=dates,
        y=agents_generated,
        title="Évolution Nombre Agents Générés",
        labels={"x": "Date", "y": "Nombre Agents"}
    )
    
    fig_evolution.add_hline(y=104, line_dash="dash", line_color="red", annotation_text="Objectif 104 agents")
    
    st.plotly_chart(fig_evolution, use_container_width=True)
    
    # Performance par secteur
    st.subheader("📊 Performance par Secteur")
    
    sector_performance = {}
    for agent_id, config in dashboard.agents_config.items():
        sector = config["sector"]
        if sector not in sector_performance:
            sector_performance[sector] = []
        sector_performance[sector].append(config["performance"])
    
    sector_avg = {sector: round(sum(perfs)/len(perfs), 1) 
                  for sector, perfs in sector_performance.items()}
    
    fig_sectors = px.bar(
        x=list(sector_avg.keys())[:15],  # Top 15 secteurs
        y=list(sector_avg.values())[:15],
        title="Performance Moyenne par Secteur (Top 15)"
    )
    
    st.plotly_chart(fig_sectors, use_container_width=True)

def tab_data_sources(dashboard):
    """Tab 5: Gestion sources données"""
    
    st.header("💾 Gestion Sources Données")
    
    # État sources
    st.subheader("📊 État Sources Données")
    
    sources = [
        {"Source": "CNESST", "Type": "CSV", "Taille": "129.9 MB", "Statut": "✅ Opérationnel", "Dernière MAJ": "2024-07-10 14:23"},
        {"Source": "BehaviorX", "Type": "SQLite", "Taille": "20 KB", "Statut": "✅ Opérationnel", "Dernière MAJ": "2024-07-11 09:15"},
        {"Source": "Analytics", "Type": "SQLite", "Taille": "45 MB", "Statut": "✅ Opérationnel", "Dernière MAJ": "2024-07-11 14:23"},
        {"Source": "Unified State", "Type": "SQLite", "Taille": "2.1 MB", "Statut": "✅ Opérationnel", "Dernière MAJ": "2024-07-11 14:25"}
    ]
    
    df_sources = pd.DataFrame(sources)
    st.dataframe(df_sources, use_container_width=True)
    
    # Synchronisation
    st.subheader("🔄 Synchronisation Données")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 CNESST**")
        st.write("Dernière sync: 2024-07-10 14:23 ✅")
        st.write("Prochaine sync auto: 2024-07-11 02:00")
        
        if st.button("🔄 Synchroniser CNESST maintenant"):
            with st.spinner("Synchronisation en cours..."):
                time.sleep(2)
            st.success("Synchronisation CNESST terminée!")
    
    with col2:
        st.write("**🤖 BehaviorX**")
        st.write("Dernière sync: 2024-07-11 09:15 ✅")
        st.write("Mode: Temps réel")
        
        if st.button("📊 Analyser intégrité données"):
            with st.spinner("Analyse en cours..."):
                time.sleep(1.5)
            st.success("Intégrité données validée!")
    
    # Nouvelles données disponibles
    st.subheader("📥 Nouvelles Données Disponibles")
    
    st.info("📊 CNESST Q2 2024: +12,847 nouveaux incidents disponibles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Télécharger"):
            st.info("Téléchargement en cours...")
    
    with col2:
        if st.button("🔄 Intégrer"):
            st.info("Intégration planifiée...")
    
    with col3:
        if st.button("📋 Prévisualiser"):
            st.info("Prévisualisation données...")

def tab_configuration(dashboard):
    """Tab 6: Configuration système"""
    
    st.header("⚙️ Configuration Système SafetyGraph")
    
    # Secteurs prioritaires
    st.subheader("🎯 Secteurs SCIAN Prioritaires")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Secteurs Activés:**")
        priority_sectors = ["Construction (23)", "Santé (62)", "Transport (48)", "Commerce (44-45)"]