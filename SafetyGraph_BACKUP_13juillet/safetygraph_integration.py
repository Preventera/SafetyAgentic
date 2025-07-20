#!/usr/bin/env python3
"""
SafetyGraph - Intégration Actions Rapides ↔ Culture SST ↔ ISO 45001
====================================================================
Architecture révolutionnaire liant actions utilisateur, culture SST et conformité ISO 45001
Mario Genest - Safety Agentique - 13 juillet 2025

🎯 Fonctionnalités :
- Actions rapides par profil utilisateur
- Calcul culture SST temps réel
- Conformité ISO 45001 automatique
- Prédiction certification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION PROFILS & ACTIONS RAPIDES
# ═══════════════════════════════════════════════════════════════

class ProfilUtilisateur(Enum):
    TRAVAILLEUR = "travailleur_terrain"
    SUPERVISEUR = "superviseur"
    COSS = "responsable_sst"
    DIRECTEUR_HSE = "directeur_hse"
    COMITE_SST = "membre_comite"
    DIRECTION = "direction_generale"

@dataclass
class ActionRapide:
    id: str
    nom: str
    description: str
    icone: str
    dimension_culture: str
    clause_iso_45001: str
    impact_culture: int
    poids_iso: float
    profils_autorises: List[ProfilUtilisateur]

# Configuration actions rapides par profil
ACTIONS_RAPIDES = {
    ProfilUtilisateur.TRAVAILLEUR: [
        ActionRapide(
            id="signaler_incident",
            nom="📱 Signaler Incident", 
            description="Signalement rapide incident avec photo",
            icone="📱",
            dimension_culture="engagement_proactif",
            clause_iso_45001="8.2_urgences",
            impact_culture=8,
            poids_iso=0.85,
            profils_autorises=[ProfilUtilisateur.TRAVAILLEUR]
        ),
        ActionRapide(
            id="check_securite",
            nom="✅ Check Sécurité",
            description="Liste vérification quotidienne",
            icone="✅", 
            dimension_culture="conformite_operationnelle",
            clause_iso_45001="8.1_maitrise_operationnelle",
            impact_culture=6,
            poids_iso=0.90,
            profils_autorises=[ProfilUtilisateur.TRAVAILLEUR]
        ),
        ActionRapide(
            id="formation_express",
            nom="🎓 Formation Express",
            description="Modules micro-learning",
            icone="🎓",
            dimension_culture="apprentissage_continu", 
            clause_iso_45001="7.2_competence",
            impact_culture=7,
            poids_iso=0.80,
            profils_autorises=[ProfilUtilisateur.TRAVAILLEUR]
        ),
        ActionRapide(
            id="alerte_urgence",
            nom="🆘 Alerte Urgence",
            description="Bouton panique + géolocalisation",
            icone="🆘",
            dimension_culture="confiance_systeme",
            clause_iso_45001="8.2_preparation_urgences",
            impact_culture=9,
            poids_iso=0.95,
            profils_autorises=[ProfilUtilisateur.TRAVAILLEUR]
        ),
        ActionRapide(
            id="score_personnel",
            nom="🏆 Mon Score Sécurité",
            description="Gamification personnelle",
            icone="🏆",
            dimension_culture="motivation_individuelle",
            clause_iso_45001="7.3_sensibilisation",
            impact_culture=5,
            poids_iso=0.70,
            profils_autorises=[ProfilUtilisateur.TRAVAILLEUR]
        )
    ],
    
    ProfilUtilisateur.COSS: [
        ActionRapide(
            id="dashboard_analytique",
            nom="📊 Dashboard Analytique",
            description="Métriques avancées culture SST",
            icone="📊",
            dimension_culture="pilotage_systemique",
            clause_iso_45001="9.1_surveillance_mesure",
            impact_culture=15,
            poids_iso=0.95,
            profils_autorises=[ProfilUtilisateur.COSS]
        ),
        ActionRapide(
            id="analyse_risques",
            nom="🔍 Analyse Risques",
            description="Pattern recognition approfondi",
            icone="🔍",
            dimension_culture="prevention_avancee",
            clause_iso_45001="6.1.2_identification_dangers",
            impact_culture=12,
            poids_iso=0.90,
            profils_autorises=[ProfilUtilisateur.COSS]
        ),
        ActionRapide(
            id="audit_conformite",
            nom="📋 Audit Conformité",
            description="Gap analysis normative",
            icone="📋",
            dimension_culture="excellence_normative",
            clause_iso_45001="9.2_audit_interne",
            impact_culture=10,
            poids_iso=0.92,
            profils_autorises=[ProfilUtilisateur.COSS]
        ),
        ActionRapide(
            id="tendances_predictives",
            nom="📈 Tendances Prédictives",
            description="ML 6-12 mois",
            icone="📈",
            dimension_culture="anticipation_strategique",
            clause_iso_45001="6.1.3_evaluation_risques",
            impact_culture=18,
            poids_iso=0.88,
            profils_autorises=[ProfilUtilisateur.COSS]
        ),
        ActionRapide(
            id="rapports_reglementaires",
            nom="📄 Rapports Réglementaires",
            description="CNESST, ISO 45001",
            icone="📄",
            dimension_culture="transparence_institutionnelle",
            clause_iso_45001="9.3_revue_direction",
            impact_culture=8,
            poids_iso=0.85,
            profils_autorises=[ProfilUtilisateur.COSS]
        )
    ],
    
    ProfilUtilisateur.DIRECTEUR_HSE: [
        ActionRapide(
            id="vue_executive",
            nom="🎯 Vue Exécutive",
            description="KPI stratégiques",
            icone="🎯",
            dimension_culture="leadership_strategique",
            clause_iso_45001="5.1_leadership_engagement",
            impact_culture=20,
            poids_iso=0.95,
            profils_autorises=[ProfilUtilisateur.DIRECTEUR_HSE]
        ),
        ActionRapide(
            id="roi_securite",
            nom="💰 ROI Sécurité",
            description="Analyse coûts/bénéfices",
            icone="💰",
            dimension_culture="valeur_economique",
            clause_iso_45001="5.4_consultation_participation",
            impact_culture=15,
            poids_iso=0.85,
            profils_autorises=[ProfilUtilisateur.DIRECTEUR_HSE]
        ),
        ActionRapide(
            id="benchmarking_secteur",
            nom="📊 Benchmarking Secteur",
            description="Comparaisons concurrence",
            icone="📊",
            dimension_culture="excellence_comparative",
            clause_iso_45001="9.1.2_evaluation_conformite",
            impact_culture=12,
            poids_iso=0.80,
            profils_autorises=[ProfilUtilisateur.DIRECTEUR_HSE]
        ),
        ActionRapide(
            id="initiatives_strategiques",
            nom="🚀 Initiatives Stratégiques",
            description="Projets amélioration",
            icone="🚀",
            dimension_culture="transformation_organisationnelle",
            clause_iso_45001="10.3_amelioration_continue",
            impact_culture=25,
            poids_iso=0.90,
            profils_autorises=[ProfilUtilisateur.DIRECTEUR_HSE]
        ),
        ActionRapide(
            id="rapport_direction",
            nom="📋 Rapport Direction",
            description="Synthèse conseil administration",
            icone="📋",
            dimension_culture="gouvernance_corporative",
            clause_iso_45001="5.3_responsabilites_organisationnelles",
            impact_culture=18,
            poids_iso=0.88,
            profils_autorises=[ProfilUtilisateur.DIRECTEUR_HSE]
        )
    ]
}

# ═══════════════════════════════════════════════════════════════
# MODÈLE CULTURE SST (7 DIMENSIONS)
# ═══════════════════════════════════════════════════════════════

@dataclass 
class DimensionCultureSST:
    nom: str
    description: str
    poids: float
    score_actuel: float = 0.0
    score_cible: float = 8.0
    tendance: str = "stable"

DIMENSIONS_CULTURE_SST = {
    "leadership_engagement": DimensionCultureSST(
        nom="Leadership & Engagement",
        description="Implication visible direction et management",
        poids=0.20
    ),
    "communication_participation": DimensionCultureSST(
        nom="Communication & Participation", 
        description="Dialogue ouvert et participation active",
        poids=0.15
    ),
    "apprentissage_amelioration": DimensionCultureSST(
        nom="Apprentissage & Amélioration",
        description="Formation continue et amélioration",
        poids=0.15
    ),
    "responsabilisation_autonomie": DimensionCultureSST(
        nom="Responsabilisation & Autonomie",
        description="Responsabilité partagée et autonomie",
        poids=0.15
    ),
    "collaboration_cohesion": DimensionCultureSST(
        nom="Collaboration & Cohésion",
        description="Travail d'équipe et cohésion sociale",
        poids=0.10
    ),
    "gestion_risques": DimensionCultureSST(
        nom="Gestion des Risques",
        description="Identification et maîtrise proactive",
        poids=0.15
    ),
    "performance_resultats": DimensionCultureSST(
        nom="Performance & Résultats",
        description="Orientation résultats et excellence",
        poids=0.10
    )
}

# ═══════════════════════════════════════════════════════════════
# MODÈLE CONFORMITÉ ISO 45001
# ═══════════════════════════════════════════════════════════════

@dataclass
class ClauseISO45001:
    numero: str
    titre: str
    description: str
    poids: float
    score_conformite: float = 0.0
    exigences: List[str] = None

CLAUSES_ISO_45001 = {
    "5.1_leadership_engagement": ClauseISO45001(
        numero="5.1",
        titre="Leadership et engagement",
        description="Engagement visible de la direction",
        poids=0.20,
        exigences=[
            "Responsabilité direction générale",
            "Intégration SST dans processus métier", 
            "Mise à disposition ressources",
            "Communication importance SST"
        ]
    ),
    "6.1.2_identification_dangers": ClauseISO45001(
        numero="6.1.2", 
        titre="Identification des dangers",
        description="Processus identification systématique dangers",
        poids=0.15,
        exigences=[
            "Processus identification continu",
            "Participation travailleurs",
            "Méthodes proactives et réactives",
            "Classification et documentation"
        ]
    ),
    "8.1_maitrise_operationnelle": ClauseISO45001(
        numero="8.1",
        titre="Planification et maîtrise opérationnelles", 
        description="Contrôles opérationnels activités SST",
        poids=0.15,
        exigences=[
            "Critères opérationnels établis",
            "Contrôles selon hiérarchie",
            "Maîtrise processus externes",
            "Adaptation changements"
        ]
    ),
    "9.1_surveillance_mesure": ClauseISO45001(
        numero="9.1",
        titre="Surveillance, mesure, analyse et évaluation",
        description="Système surveillance performance SST",
        poids=0.15,
        exigences=[
            "Méthodes surveillance définies",
            "Critères et indicateurs",
            "Étalonnage équipements",
            "Analyse et évaluation données"
        ]
    ),
    "10.3_amelioration_continue": ClauseISO45001(
        numero="10.3",
        titre="Amélioration continue",
        description="Amélioration continue performance SST",
        poids=0.10,
        exigences=[
            "Processus amélioration continue",
            "Opportunités d'amélioration",
            "Participation travailleurs",
            "Communication résultats"
        ]
    )
}

# ═══════════════════════════════════════════════════════════════
# MOTEUR CALCUL CULTURE SST & ISO 45001
# ═══════════════════════════════════════════════════════════════

class MoteurCultureSST:
    """Moteur de calcul culture SST et conformité ISO 45001"""
    
    def __init__(self):
        self.historique_actions = []
        self.scores_culture = DIMENSIONS_CULTURE_SST.copy()
        self.conformite_iso = CLAUSES_ISO_45001.copy()
        
    def enregistrer_action(self, user_profil: ProfilUtilisateur, action_id: str, 
                          timestamp: datetime = None) -> Dict:
        """Enregistre une action utilisateur et calcule impacts"""
        
        if timestamp is None:
            timestamp = datetime.now()
            
        # Trouver l'action
        action = self._trouver_action(user_profil, action_id)
        if not action:
            return {"erreur": "Action non trouvée"}
            
        # Enregistrer dans historique
        entry = {
            "timestamp": timestamp,
            "profil": user_profil,
            "action": action,
            "impact_culture": action.impact_culture,
            "impact_iso": action.poids_iso
        }
        self.historique_actions.append(entry)
        
        # Calculer nouveaux scores
        self._calculer_score_culture(action)
        self._calculer_conformite_iso(action)
        
        return {
            "success": True,
            "action_enregistree": action.nom,
            "impact_culture": action.impact_culture,
            "nouveau_score_culture": self._score_culture_global(),
            "nouveau_score_iso": self._score_iso_global()
        }
    
    def _trouver_action(self, profil: ProfilUtilisateur, action_id: str) -> Optional[ActionRapide]:
        """Trouve une action par profil et ID"""
        actions_profil = ACTIONS_RAPIDES.get(profil, [])
        for action in actions_profil:
            if action.id == action_id:
                return action
        return None
    
    def _calculer_score_culture(self, action: ActionRapide):
        """Met à jour score culture SST basé sur action"""
        dimension = action.dimension_culture
        
        # Mapping dimension culture
        mapping_dimensions = {
            "engagement_proactif": "leadership_engagement",
            "conformite_operationnelle": "gestion_risques", 
            "apprentissage_continu": "apprentissage_amelioration",
            "confiance_systeme": "collaboration_cohesion",
            "motivation_individuelle": "responsabilisation_autonomie",
            "pilotage_systemique": "leadership_engagement",
            "prevention_avancee": "gestion_risques",
            "excellence_normative": "performance_resultats",
            "anticipation_strategique": "apprentissage_amelioration",
            "transparence_institutionnelle": "communication_participation",
            "leadership_strategique": "leadership_engagement",
            "valeur_economique": "performance_resultats",
            "excellence_comparative": "performance_resultats",
            "transformation_organisationnelle": "apprentissage_amelioration",
            "gouvernance_corporative": "leadership_engagement"
        }
        
        dimension_cible = mapping_dimensions.get(dimension, "performance_resultats")
        
        if dimension_cible in self.scores_culture:
            # Formule : nouveau_score = ancien_score + (impact * facteur_temporel)
            facteur_temporel = self._calculer_facteur_temporel()
            increment = action.impact_culture * facteur_temporel * 0.1
            
            self.scores_culture[dimension_cible].score_actuel += increment
            
            # Limitation 0-10
            self.scores_culture[dimension_cible].score_actuel = max(0, 
                min(10, self.scores_culture[dimension_cible].score_actuel))
    
    def _calculer_conformite_iso(self, action: ActionRapide):
        """Met à jour conformité ISO 45001 basée sur action"""
        clause_iso = action.clause_iso_45001
        
        if clause_iso in self.conformite_iso:
            # Formule : conformité = (fréquence_actions * qualité_execution * poids_iso)
            facteur_frequence = self._calculer_frequence_action(action.id)
            increment = action.poids_iso * facteur_frequence * 0.15
            
            self.conformite_iso[clause_iso].score_conformite += increment
            
            # Limitation 0-100%
            self.conformite_iso[clause_iso].score_conformite = max(0,
                min(100, self.conformite_iso[clause_iso].score_conformite))
    
    def _calculer_facteur_temporel(self) -> float:
        """Calcule facteur temporel pour pondération récence"""
        # Plus l'action est récente, plus l'impact est fort
        return 1.0  # Simplifié pour demo
    
    def _calculer_frequence_action(self, action_id: str) -> float:
        """Calcule fréquence d'utilisation d'une action"""
        count = sum(1 for entry in self.historique_actions 
                   if entry["action"].id == action_id)
        return min(1.0, count / 10)  # Normalisé sur 10 utilisations
    
    def _score_culture_global(self) -> float:
        """Calcule score culture SST global pondéré"""
        score_total = 0
        for dimension_id, dimension in self.scores_culture.items():
            score_total += dimension.score_actuel * dimension.poids
        return round(score_total, 2)
    
    def _score_iso_global(self) -> float:
        """Calcule score conformité ISO 45001 global"""
        score_total = 0
        poids_total = 0
        for clause_id, clause in self.conformite_iso.items():
            score_total += clause.score_conformite * clause.poids
            poids_total += clause.poids
        return round(score_total / poids_total if poids_total > 0 else 0, 1)
    
    def generer_recommandations(self) -> List[Dict]:
        """Génère recommandations basées sur scores actuels"""
        recommandations = []
        
        # Recommandations culture SST
        for dimension_id, dimension in self.scores_culture.items():
            if dimension.score_actuel < dimension.score_cible:
                gap = dimension.score_cible - dimension.score_actuel
                recommandations.append({
                    "type": "culture_sst",
                    "dimension": dimension.nom,
                    "gap": round(gap, 1),
                    "priorite": "haute" if gap > 2 else "moyenne",
                    "actions_suggerees": self._actions_pour_dimension(dimension_id)
                })
        
        # Recommandations ISO 45001
        for clause_id, clause in self.conformite_iso.items():
            if clause.score_conformite < 85:  # Seuil conformité
                recommandations.append({
                    "type": "iso_45001",
                    "clause": clause.titre,
                    "score": clause.score_conformite,
                    "priorite": "critique" if clause.score_conformite < 70 else "importante",
                    "exigences_manquantes": clause.exigences
                })
                
        return recommandations
    
    def _actions_pour_dimension(self, dimension_id: str) -> List[str]:
        """Retourne actions recommandées pour améliorer dimension"""
        # Mapping simplifié pour demo
        actions_map = {
            "leadership_engagement": ["Vue Executive", "Initiatives Stratégiques"],
            "gestion_risques": ["Analyse Risques", "Check Sécurité"],
            "apprentissage_amelioration": ["Formation Express", "Tendances Prédictives"],
            "communication_participation": ["Rapport Direction", "Signaler Incident"],
            "performance_resultats": ["ROI Sécurité", "Audit Conformité"],
            "collaboration_cohesion": ["Alerte Urgence", "Score Personnel"],
            "responsabilisation_autonomie": ["Score Personnel", "Check Sécurité"]
        }
        return actions_map.get(dimension_id, ["Actions génériques"])

# ═══════════════════════════════════════════════════════════════
# INTERFACE STREAMLIT INTÉGRÉE
# ═══════════════════════════════════════════════════════════════

def afficher_actions_rapides_profil(profil: ProfilUtilisateur, moteur: MoteurCultureSST):
    """Affiche les 5 actions rapides pour un profil donné"""
    
    st.markdown(f"## ⚡ Actions Rapides - {profil.value.replace('_', ' ').title()}")
    
    actions = ACTIONS_RAPIDES.get(profil, [])
    
    # Disposition en colonnes
    cols = st.columns(5)
    
    for i, action in enumerate(actions):
        with cols[i]:
            if st.button(
                action.nom,
                key=f"action_{action.id}_{profil.value}",
                help=action.description,
                use_container_width=True
            ):
                # Enregistrer action et calculer impacts
                result = moteur.enregistrer_action(profil, action.id)
                
                if result.get("success"):
                    st.success(f"✅ {action.nom} exécutée!")
                    st.info(f"Impact Culture: +{result['impact_culture']} points")
                    
                    # Rerun pour mettre à jour les métriques
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de l'exécution")

def afficher_dashboard_culture_sst(moteur: MoteurCultureSST):
    """Dashboard culture SST avec métriques temps réel"""
    
    st.markdown("## 📊 Dashboard Culture SST")
    
    # Score global
    score_global = moteur._score_culture_global()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🎯 Score Culture Global",
            f"{score_global}/10",
            delta=f"+{0.3}",
            delta_color="normal"
        )
    
    with col2:
        niveau_maturite = "Excellente" if score_global >= 8 else "Bonne" if score_global >= 6 else "En développement"
        st.metric("📈 Niveau Maturité", niveau_maturite)
    
    with col3:
        actions_total = len(moteur.historique_actions)
        st.metric("⚡ Actions Réalisées", actions_total)
    
    with col4:
        score_iso = moteur._score_iso_global()
        st.metric("📋 Conformité ISO 45001", f"{score_iso}%")
    
    # Graphique radar culture SST
    categories = []
    values = []
    targets = []
    
    for dimension_id, dimension in moteur.scores_culture.items():
        categories.append(dimension.nom)
        values.append(dimension.score_actuel)
        targets.append(dimension.score_cible)
    
    fig = go.Figure()
    
    # Score actuel
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Score Actuel',
        line_color='rgb(67, 167, 181)'
    ))
    
    # Score cible
    fig.add_trace(go.Scatterpolar(
        r=targets,
        theta=categories,
        fill='toself',
        name='Score Cible',
        line_color='rgb(255, 127, 14)',
        opacity=0.6
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        title="Radar Culture SST - 7 Dimensions"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def afficher_conformite_iso45001(moteur: MoteurCultureSST):
    """Dashboard conformité ISO 45001"""
    
    st.markdown("## 📋 Conformité ISO 45001")
    
    # Scores par clause
    clauses_data = []
    for clause_id, clause in moteur.conformite_iso.items():
        clauses_data.append({
            "Clause": clause.numero,
            "Titre": clause.titre,
            "Score": clause.score_conformite,
            "Statut": "✅ Conforme" if clause.score_conformite >= 85 else "⚠️ À améliorer" if clause.score_conformite >= 70 else "❌ Non conforme"
        })
    
    df_conformite = pd.DataFrame(clauses_data)
    st.dataframe(df_conformite, use_container_width=True)
    
    # Graphique conformité
    fig = px.bar(
        df_conformite,
        x="Clause",
        y="Score", 
        title="Scores Conformité par Clause ISO 45001",
        color="Score",
        color_continuous_scale=["red", "orange", "green"],
        range_color=[0, 100]
    )
    
    fig.add_hline(y=85, line_dash="dash", line_color="green", 
                  annotation_text="Seuil Conformité (85%)")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Prédiction certification
    score_global_iso = moteur._score_iso_global()
    
    if score_global_iso >= 95:
        st.success("🏆 **PRÊT POUR CERTIFICATION** - Probabilité succès: 98%")
    elif score_global_iso >= 85:
        st.warning("🎯 **PRÉPARATION AVANCÉE** - Probabilité succès: 87%") 
    else:
        st.error("🔧 **DÉVELOPPEMENT REQUIS** - Actions correctives nécessaires")

def afficher_recommandations(moteur: MoteurCultureSST):
    """Affiche recommandations personnalisées"""
    
    st.markdown("## 🎯 Recommandations Intelligentes")
    
    recommandations = moteur.generer_recommandations()
    
    if not recommandations:
        st.success("🏆 Excellente performance ! Aucune recommandation critique.")
        return
    
    # Grouper par type
    reco_culture = [r for r in recommandations if r["type"] == "culture_sst"]
    reco_iso = [r for r in recommandations if r["type"] == "iso_45001"]
    
    if reco_culture:
        st.markdown("### 📊 Amélioration Culture SST")
        for reco in reco_culture:
            priorite_color = {"haute": "🔴", "moyenne": "🟡", "faible": "🟢"}
            st.markdown(f"""
            {priorite_color.get(reco['priorite'], '🔵')} **{reco['dimension']}**
            - Gap: {reco['gap']} points
            - Actions suggérées: {', '.join(reco['actions_suggerees'])}
            """)
    
    if reco_iso:
        st.markdown("### 📋 Conformité ISO 45001")
        for reco in reco_iso:
            priorite_color = {"critique": "🔴", "importante": "🟡", "faible": "🟢"}
            st.markdown(f"""
            {priorite_color.get(reco['priorite'], '🔵')} **{reco['clause']}**
            - Score actuel: {reco['score']}%
            - Exigences: {', '.join(reco['exigences_manquantes'][:2])}...
            """)

def interface_principale():
    """Interface principale SafetyGraph intégrée"""
    
    st.set_page_config(
        page_title="SafetyGraph - Actions Rapides & Culture SST",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialisation session state
    if "moteur_culture" not in st.session_state:
        st.session_state.moteur_culture = MoteurCultureSST()
    
    if "profil_utilisateur" not in st.session_state:
        st.session_state.profil_utilisateur = ProfilUtilisateur.COSS
    
    moteur = st.session_state.moteur_culture
    
    # ═══════════════════════════════════════════════════════════════
    # HEADER PRINCIPAL
    # ═══════════════════════════════════════════════════════════════
    
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0;">🛡️ SafetyGraph BehaviorX</h1>
        <h3 style="color: #a8d0ff; margin: 5px 0;">Actions Rapides ↔ Culture SST ↔ ISO 45001</h3>
        <p style="color: #e1ecff; margin: 0;">🏢 Powered by Safety Agentique | 🧠 IA Culture SST | 📋 Conformité Temps Réel</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SIDEBAR CONFIGURATION
    # ═══════════════════════════════════════════════════════════════
    
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # Sélection profil utilisateur
        profil_selected = st.selectbox(
            "👤 Profil Utilisateur",
            options=list(ProfilUtilisateur),
            format_func=lambda x: x.value.replace('_', ' ').title(),
            index=list(ProfilUtilisateur).index(st.session_state.profil_utilisateur)
        )
        
        if profil_selected != st.session_state.profil_utilisateur:
            st.session_state.profil_utilisateur = profil_selected
            st.rerun()
        
        st.markdown("---")
        
        # Métriques sidebar
        st.markdown("### 📊 Métriques Temps Réel")
        
        score_culture = moteur._score_culture_global()
        score_iso = moteur._score_iso_global()
        actions_count = len(moteur.historique_actions)
        
        st.metric("🎯 Culture SST", f"{score_culture}/10")
        st.metric("📋 ISO 45001", f"{score_iso}%")
        st.metric("⚡ Actions", actions_count)
        
        # Statut conformité
        if score_iso >= 95:
            st.success("🏆 Prêt Certification")
        elif score_iso >= 85:
            st.warning("🎯 Préparation Avancée")
        else:
            st.error("🔧 Développement Requis")
        
        st.markdown("---")
        
        # Actions debug
        st.markdown("### 🔧 Actions Debug")
        
        if st.button("🔄 Reset Données", help="Remet à zéro tous les scores"):
            st.session_state.moteur_culture = MoteurCultureSST()
            st.success("✅ Données réinitialisées")
            st.rerun()
        
        if st.button("📊 Données Demo", help="Charge données de démonstration"):
            charger_donnees_demo(moteur)
            st.success("✅ Données demo chargées")
            st.rerun()
    
    # ═══════════════════════════════════════════════════════════════
    # CONTENU PRINCIPAL - TABS
    # ═══════════════════════════════════════════════════════════════
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⚡ Actions Rapides",
        "📊 Culture SST", 
        "📋 ISO 45001",
        "🎯 Recommandations",
        "📈 Analytics Avancés"
    ])
    
    # ─────────────────────────────────────────────────────────────
    # TAB 1: ACTIONS RAPIDES
    # ─────────────────────────────────────────────────────────────
    
    with tab1:
        st.markdown("## ⚡ Actions Rapides par Profil")
        
        # Info profil actuel
        profil_actuel = st.session_state.profil_utilisateur
        st.info(f"👤 Profil actuel: **{profil_actuel.value.replace('_', ' ').title()}**")
        
        # Actions rapides du profil
        afficher_actions_rapides_profil(profil_actuel, moteur)
        
        st.markdown("---")
        
        # Historique actions récentes
        if moteur.historique_actions:
            st.markdown("### 📋 Historique Actions Récentes")
            
            historique_df = []
            for entry in moteur.historique_actions[-10:]:  # 10 dernières
                historique_df.append({
                    "Timestamp": entry["timestamp"].strftime("%H:%M:%S"),
                    "Profil": entry["profil"].value.replace('_', ' ').title(),
                    "Action": entry["action"].nom,
                    "Impact Culture": f"+{entry['impact_culture']}",
                    "Impact ISO": f"+{entry['impact_iso']:.1%}"
                })
            
            if historique_df:
                df = pd.DataFrame(historique_df)
                st.dataframe(df, use_container_width=True)
        else:
            st.info("💡 Exécutez des actions pour voir l'historique")
    
    # ─────────────────────────────────────────────────────────────
    # TAB 2: CULTURE SST
    # ─────────────────────────────────────────────────────────────
    
    with tab2:
        afficher_dashboard_culture_sst(moteur)
        
        # Détails par dimension
        st.markdown("### 📋 Détails par Dimension Culture SST")
        
        dimension_data = []
        for dim_id, dimension in moteur.scores_culture.items():
            progression = ((dimension.score_actuel / dimension.score_cible) * 100) if dimension.score_cible > 0 else 0
            dimension_data.append({
                "Dimension": dimension.nom,
                "Score Actuel": f"{dimension.score_actuel:.1f}/10",
                "Score Cible": f"{dimension.score_cible}/10", 
                "Progression": f"{progression:.1f}%",
                "Poids": f"{dimension.poids:.1%}",
                "Statut": "✅ Objectif atteint" if dimension.score_actuel >= dimension.score_cible else "🎯 En progression" if dimension.score_actuel >= dimension.score_cible * 0.8 else "⚠️ Attention requise"
            })
        
        df_dimensions = pd.DataFrame(dimension_data)
        st.dataframe(df_dimensions, use_container_width=True)
    
    # ─────────────────────────────────────────────────────────────
    # TAB 3: ISO 45001
    # ─────────────────────────────────────────────────────────────
    
    with tab3:
        afficher_conformite_iso45001(moteur)
        
        # Mapping actions → clauses ISO
        st.markdown("### 🔗 Mapping Actions → Clauses ISO 45001")
        
        mapping_data = []
        for profil, actions in ACTIONS_RAPIDES.items():
            for action in actions:
                clause = moteur.conformite_iso.get(action.clause_iso_45001)
                if clause:
                    mapping_data.append({
                        "Profil": profil.value.replace('_', ' ').title(),
                        "Action": action.nom,
                        "Clause ISO": clause.numero,
                        "Titre Clause": clause.titre,
                        "Impact": f"{action.poids_iso:.1%}",
                        "Statut": "✅" if clause.score_conformite >= 85 else "⚠️" if clause.score_conformite >= 70 else "❌"
                    })
        
        df_mapping = pd.DataFrame(mapping_data)
        st.dataframe(df_mapping, use_container_width=True)
    
    # ─────────────────────────────────────────────────────────────
    # TAB 4: RECOMMANDATIONS
    # ─────────────────────────────────────────────────────────────
    
    with tab4:
        afficher_recommandations(moteur)
        
        # Plan d'action priorisé
        st.markdown("### 📋 Plan d'Action Priorisé")
        
        recommandations = moteur.generer_recommandations()
        
        if recommandations:
            # Trier par priorité
            priorite_ordre = {"critique": 0, "haute": 1, "importante": 2, "moyenne": 3, "faible": 4}
            recommandations_triees = sorted(recommandations, 
                                          key=lambda x: priorite_ordre.get(x.get("priorite", "moyenne"), 3))
            
            for i, reco in enumerate(recommandations_triees[:5], 1):
                with st.expander(f"Action {i}: {reco.get('dimension', reco.get('clause', 'Action'))}", expanded=i<=2):
                    if reco["type"] == "culture_sst":
                        st.write(f"**Type:** Culture SST - {reco['dimension']}")
                        st.write(f"**Gap:** {reco['gap']} points")
                        st.write(f"**Priorité:** {reco['priorite']}")
                        st.write(f"**Actions suggérées:** {', '.join(reco['actions_suggerees'])}")
                    else:
                        st.write(f"**Type:** ISO 45001 - {reco['clause']}")
                        st.write(f"**Score actuel:** {reco['score']}%")
                        st.write(f"**Priorité:** {reco['priorite']}")
                        st.write(f"**Exigences:** {', '.join(reco['exigences_manquantes'][:3])}")
        else:
            st.success("🎉 Aucune action corrective nécessaire - Performance excellente !")
    
    # ─────────────────────────────────────────────────────────────
    # TAB 5: ANALYTICS AVANCÉS
    # ─────────────────────────────────────────────────────────────
    
    with tab5:
        st.markdown("## 📈 Analytics Avancés")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Évolution temporelle culture SST
            st.markdown("### 📊 Évolution Culture SST")
            
            # Simulation données temporelles
            dates = pd.date_range(start="2025-01-01", end="2025-07-13", freq="W")
            evolution_data = []
            
            base_score = 5.0
            for i, date in enumerate(dates):
                # Simulation progression réaliste
                noise = np.random.normal(0, 0.1)
                trend = i * 0.05  # Tendance positive
                score = base_score + trend + noise
                evolution_data.append({"Date": date, "Score Culture": max(0, min(10, score))})
            
            df_evolution = pd.DataFrame(evolution_data)
            
            fig_evolution = px.line(
                df_evolution,
                x="Date",
                y="Score Culture",
                title="Évolution Score Culture SST",
                markers=True
            )
            
            fig_evolution.add_hline(y=8, line_dash="dash", line_color="green", 
                                  annotation_text="Objectif (8/10)")
            
            st.plotly_chart(fig_evolution, use_container_width=True)
        
        with col2:
            # Répartition actions par profil
            st.markdown("### 👥 Répartition Actions par Profil")
            
            if moteur.historique_actions:
                profil_counts = {}
                for entry in moteur.historique_actions:
                    profil_name = entry["profil"].value.replace('_', ' ').title()
                    profil_counts[profil_name] = profil_counts.get(profil_name, 0) + 1
                
                fig_profils = px.pie(
                    values=list(profil_counts.values()),
                    names=list(profil_counts.keys()),
                    title="Actions par Profil Utilisateur"
                )
                
                st.plotly_chart(fig_profils, use_container_width=True)
            else:
                st.info("💡 Exécutez des actions pour voir la répartition")
        
        # Prédictions IA
        st.markdown("### 🔮 Prédictions IA")
        
        col3, col4, col5 = st.columns(3)
        
        with col3:
            # Prédiction certification ISO
            score_iso_actuel = moteur._score_iso_global()
            if score_iso_actuel >= 85:
                delai_certif = "2-3 mois"
                probabilite = "95%"
                couleur = "green"
            elif score_iso_actuel >= 70:
                delai_certif = "4-6 mois" 
                probabilite = "80%"
                couleur = "orange"
            else:
                delai_certif = "8-12 mois"
                probabilite = "60%"
                couleur = "red"
            
            st.markdown(f"""
            <div style="padding: 15px; border: 2px solid {couleur}; border-radius: 10px; text-align: center;">
                <h4>🏆 Certification ISO 45001</h4>
                <p><strong>Probabilité:</strong> {probabilite}</p>
                <p><strong>Délai estimé:</strong> {delai_certif}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Prédiction culture SST
            score_culture_actuel = moteur._score_culture_global()
            if score_culture_actuel >= 8:
                niveau_futur = "Excellence"
                progression = "+0.5 pts/mois"
                couleur = "green"
            elif score_culture_actuel >= 6:
                niveau_futur = "Maturité Avancée"
                progression = "+0.3 pts/mois"
                couleur = "orange"
            else:
                niveau_futur = "Développement"
                progression = "+0.8 pts/mois"
                couleur = "blue"
            
            st.markdown(f"""
            <div style="padding: 15px; border: 2px solid {couleur}; border-radius: 10px; text-align: center;">
                <h4>📊 Culture SST Future</h4>
                <p><strong>Niveau prédit:</strong> {niveau_futur}</p>
                <p><strong>Progression:</strong> {progression}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            # ROI investissement
            actions_total = len(moteur.historique_actions)
            roi_estime = actions_total * 1500  # 1500$ par action en valeur
            
            st.markdown(f"""
            <div style="padding: 15px; border: 2px solid green; border-radius: 10px; text-align: center;">
                <h4>💰 ROI Estimé</h4>
                <p><strong>Valeur générée:</strong> {roi_estime:,}$</p>
                <p><strong>Actions réalisées:</strong> {actions_total}</p>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════

def charger_donnees_demo(moteur: MoteurCultureSST):
    """Charge des données de démonstration"""
    
    # Simuler historique d'actions variées
    demo_actions = [
        (ProfilUtilisateur.TRAVAILLEUR, "signaler_incident", 5),
        (ProfilUtilisateur.TRAVAILLEUR, "check_securite", 12),
        (ProfilUtilisateur.SUPERVISEUR, "tableau_equipe", 8),
        (ProfilUtilisateur.COSS, "dashboard_analytique", 15),
        (ProfilUtilisateur.COSS, "analyse_risques", 6),
        (ProfilUtilisateur.DIRECTEUR_HSE, "vue_executive", 4),
        (ProfilUtilisateur.DIRECTEUR_HSE, "initiatives_strategiques", 3),
        (ProfilUtilisateur.TRAVAILLEUR, "formation_express", 8),
        (ProfilUtilisateur.COSS, "audit_conformite", 4),
        (ProfilUtilisateur.DIRECTEUR_HSE, "roi_securite", 2)
    ]
    
    # Ajouter les actions avec dates variées
    base_date = datetime.now() - timedelta(days=30)
    
    for profil, action_id, count in demo_actions:
        for i in range(count):
            timestamp = base_date + timedelta(days=i*2, hours=i%24)
            moteur.enregistrer_action(profil, action_id, timestamp)

def export_donnees_json(moteur: MoteurCultureSST) -> Dict:
    """Exporte toutes les données en JSON"""
    
    return {
        "timestamp_export": datetime.now().isoformat(),
        "version": "SafetyGraph v3.0",
        "scores_culture_sst": {
            dim_id: {
                "nom": dim.nom,
                "score_actuel": dim.score_actuel,
                "score_cible": dim.score_cible,
                "poids": dim.poids
            }
            for dim_id, dim in moteur.scores_culture.items()
        },
        "conformite_iso_45001": {
            clause_id: {
                "numero": clause.numero,
                "titre": clause.titre,
                "score_conformite": clause.score_conformite,
                "poids": clause.poids
            }
            for clause_id, clause in moteur.conformite_iso.items()
        },
        "historique_actions": [
            {
                "timestamp": entry["timestamp"].isoformat(),
                "profil": entry["profil"].value,
                "action_id": entry["action"].id,
                "action_nom": entry["action"].nom,
                "impact_culture": entry["impact_culture"],
                "impact_iso": entry["impact_iso"]
            }
            for entry in moteur.historique_actions
        ],
        "score_global_culture": moteur._score_culture_global(),
        "score_global_iso": moteur._score_iso_global(),
        "total_actions": len(moteur.historique_actions)
    }

# ═══════════════════════════════════════════════════════════════
# POINT D'ENTRÉE PRINCIPAL
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    interface_principale()

# ═══════════════════════════════════════════════════════════════
# DOCUMENTATION API
# ═══════════════════════════════════════════════════════════════

"""
API USAGE EXAMPLES:
==================

# Initialiser le moteur
moteur = MoteurCultureSST()

# Enregistrer une action
result = moteur.enregistrer_action(
    ProfilUtilisateur.COSS, 
    "dashboard_analytique"
)

# Obtenir scores
score_culture = moteur._score_culture_global()
score_iso = moteur._score_iso_global()

# Générer recommandations  
recommandations = moteur.generer_recommandations()

# Exporter données
data = export_donnees_json(moteur)

INTÉGRATION AVEC APP_BEHAVIORX.PY:
=================================

# Dans votre app principal, ajoutez:
from safetygraph_integration import MoteurCultureSST, afficher_actions_rapides_profil

# Initialisez dans session_state
if "moteur_culture" not in st.session_state:
    st.session_state.moteur_culture = MoteurCultureSST()

# Utilisez dans vos onglets
with main_tabs[0]:  # BehaviorX
    afficher_actions_rapides_profil(ProfilUtilisateur.TRAVAILLEUR, moteur)

PERSONNALISATION PROFILS:
========================

# Ajouter nouveaux profils
class ProfilUtilisateur(Enum):
    VOTRE_PROFIL = "votre_profil_custom"

# Ajouter actions personnalisées
ACTIONS_RAPIDES[ProfilUtilisateur.VOTRE_PROFIL] = [
    ActionRapide(
        id="votre_action",
        nom="🚀 Votre Action",
        # ... autres paramètres
    )
]

MÉTRIQUES AVANCÉES:
==================

# Calculs personnalisés
def calculer_roi_culture(moteur):
    actions = len(moteur.historique_actions)
    return actions * 1500  # ROI par action

def predire_certification(score_iso):
    if score_iso >= 95:
        return {"statut": "prêt", "délai": "2-3 mois"}
    # ... autres cas

SÉCURITÉ & PERFORMANCE:
======================

# Limitation historique (éviter surcharge mémoire)
MAX_HISTORIQUE = 1000

# Sauvegarde périodique
def sauvegarder_etat(moteur):
    data = export_donnees_json(moteur)
    with open(f"safetygraph_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json", "w") as f:
        json.dump(data, f, indent=2)

# Restauration état
def restaurer_etat(fichier_backup):
    # Implémentation restauration depuis JSON
    pass
"""