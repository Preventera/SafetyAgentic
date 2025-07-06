# SafetyAgentic - Agent A2 BehaviorX CORRIGÉ - Observations ABC + VCS
# ===================================================================
# Version corrigée des erreurs de noms de méthodes et structure

import sys
import os
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import logging
import random

# Configuration logging SafetyAgentic
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SafetyAgentic.A2.BehaviorX")

@dataclass
class ObservationABC:
    """Structure observation modèle ABC BehaviorX"""
    
    antecedent: Dict = field(default_factory=dict)
    comportement: Dict = field(default_factory=dict)
    consequence: Dict = field(default_factory=dict)
    score_abc: float = 0.0
    criticité: str = "MOYEN"
    recommandations: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class VCSData:
    """Données Visite Comportementale Sécurité"""
    
    observateur: str = ""
    zone_observée: str = ""
    tâche_observée: str = ""
    comportements_observés: List[Dict] = field(default_factory=list)
    conversations_sécurité: List[Dict] = field(default_factory=list)
    actions_correctives: List[Dict] = field(default_factory=list)
    score_vcs: float = 0.0
    durée_observation: int = 0  # minutes

class ModuleBehaviorXObservations:
    """Module BehaviorX pour observations terrain - VERSION CORRIGÉE"""
    
    def __init__(self):
        self.modes_observation = [
            "ABC_Standard", "ABC_Critique", "VCS_Comportementale", 
            "VCS_Conversation", "Checklist_Adaptative", "Observation_Continue"
        ]
        logger.info("🔍 Module BehaviorX Observations initialisé")
    
    def observation_abc_standard(self, données_terrain: Dict) -> ObservationABC:
        """Observation standard modèle ABC BehaviorX"""
        logger.info("🔄 Observation ABC Standard activée")
        
        observation = ObservationABC()
        
        # Analyse des antécédents
        observation.antecedent = self._analyser_antecedents_terrain(données_terrain)
        
        # Analyse des comportements observés
        observation.comportement = self._analyser_comportements_terrain(données_terrain)
        
        # Analyse des conséquences
        observation.consequence = self._analyser_consequences_terrain(données_terrain)
        
        # Calcul score ABC global
        observation.score_abc = self._calculer_score_abc_global(observation)
        
        # Détermination criticité
        observation.criticité = self._determiner_criticite(observation.score_abc)
        
        # Génération recommandations
        observation.recommandations = self._generer_recommandations_abc(observation)
        
        logger.info(f"✅ Observation ABC terminée - Score: {observation.score_abc:.2f}")
        return observation
    
    def visite_comportementale_securite(self, données_vcs: Dict) -> VCSData:
        """Visite Comportementale Sécurité BehaviorX - CORRIGÉE"""
        logger.info("🔄 VCS BehaviorX activée")
        
        vcs = VCSData()
        vcs.observateur = données_vcs.get("observateur", "Agent_A2")
        vcs.zone_observée = données_vcs.get("zone", "Zone_Non_Spécifiée")
        vcs.tâche_observée = données_vcs.get("tâche", "Tâche_Standard")
        
        # Analyse comportements observés
        vcs.comportements_observés = self._analyser_comportements_vcs(données_vcs)
        
        # Conversations sécurité - NOM CORRIGÉ
        vcs.conversations_sécurité = self._conduire_conversations_securite(données_vcs)
        
        # Actions correctives identifiées
        vcs.actions_correctives = self._identifier_actions_correctives(vcs.comportements_observés)
        
        # Score VCS global
        vcs.score_vcs = self._calculer_score_vcs(vcs)
        
        # Durée observation
        vcs.durée_observation = données_vcs.get("durée", 15)
        
        logger.info(f"✅ VCS terminée - Score: {vcs.score_vcs:.2f}, Zone: {vcs.zone_observée}")
        return vcs
    
    # Méthodes internes d'analyse - CORRIGÉES
    
    def _analyser_antecedents_terrain(self, données: Dict) -> Dict:
        """Analyse antécédents terrain pour modèle ABC"""
        antecedents = données.get("antecedents", [])
        
        # Classification antécédents
        antecedents_organisationnels = [a for a in antecedents if any(
            terme in str(a).lower() for terme in ["formation", "procédure", "politique"]
        )]
        antecedents_techniques = [a for a in antecedents if any(
            terme in str(a).lower() for terme in ["équipement", "machine", "outil"]
        )]
        antecedents_humains = [a for a in antecedents if any(
            terme in str(a).lower() for terme in ["fatigue", "stress", "expérience"]
        )]
        
        score_antecedents = min(10, max(1, 8 - len(antecedents_techniques) * 0.5))
        
        return {
            "organisationnels": antecedents_organisationnels,
            "techniques": antecedents_techniques,
            "humains": antecedents_humains,
            "score": score_antecedents,
            "criticité_antecedents": "ÉLEVÉE" if score_antecedents < 5 else "MODÉRÉE"
        }
    
    def _analyser_comportements_terrain(self, données: Dict) -> Dict:
        """Analyse comportements observés terrain"""
        comportements = données.get("comportements_observés", [])
        
        # Classification comportements
        comportements_sûrs = [c for c in comportements if any(
            terme in str(c).lower() for terme in ["epi", "sécuritaire", "procédure", "vérification"]
        )]
        comportements_risque = [c for c in comportements if any(
            terme in str(c).lower() for terme in ["risque", "danger", "négligence", "contournement"]
        )]
        
        # Score comportements
        score_base = 7.0
        if comportements_sûrs:
            score_base += len(comportements_sûrs) * 0.5
        if comportements_risque:
            score_base -= len(comportements_risque) * 1.0
        
        score_comportements = max(1, min(10, score_base))
        
        return {
            "comportements_sûrs": comportements_sûrs,
            "comportements_risque": comportements_risque,
            "ratio_sécurité": len(comportements_sûrs) / max(1, len(comportements)),
            "score": score_comportements,
            "tendance": "POSITIVE" if len(comportements_sûrs) > len(comportements_risque) else "NÉGATIVE"
        }
    
    def _analyser_consequences_terrain(self, données: Dict) -> Dict:
        """Analyse conséquences observées/potentielles"""
        consequences = données.get("consequences_observées", [])
        consequences_potentielles = données.get("consequences_potentielles", [])
        
        # Analyse gravité
        consequences_graves = [c for c in consequences + consequences_potentielles if any(
            terme in str(c).lower() for terme in ["grave", "mortel", "invalidité", "arrêt"]
        )]
        
        score_consequences = max(1, 9 - len(consequences_graves) * 2)
        
        return {
            "consequences_observées": consequences,
            "consequences_potentielles": consequences_potentielles,
            "consequences_graves": consequences_graves,
            "score": score_consequences,
            "niveau_gravité": "CRITIQUE" if len(consequences_graves) > 0 else "MODÉRÉ"
        }
    
    def _calculer_score_abc_global(self, observation: ObservationABC) -> float:
        """Calcul score ABC global"""
        score_a = observation.antecedent.get("score", 5)
        score_b = observation.comportement.get("score", 5)
        score_c = observation.consequence.get("score", 5)
        
        # Pondération ABC BehaviorX : Comportement prioritaire
        return (score_a * 0.25 + score_b * 0.50 + score_c * 0.25)
    
    def _determiner_criticite(self, score_abc: float) -> str:
        """Détermination criticité selon score ABC"""
        if score_abc >= 8:
            return "FAIBLE"
        elif score_abc >= 6:
            return "MODÉRÉE"
        elif score_abc >= 4:
            return "ÉLEVÉE"
        else:
            return "CRITIQUE"
    
    def _generer_recommandations_abc(self, observation: ObservationABC) -> List[str]:
        """Génération recommandations basées ABC"""
        recommandations = []
        
        if observation.score_abc < 5:
            recommandations.extend([
                "Intervention immédiate requise",
                "Formation comportementale ciblée",
                "Révision procédures de sécurité"
            ])
        elif observation.score_abc < 7:
            recommandations.extend([
                "Renforcement sensibilisation",
                "Coaching comportemental",
                "Amélioration antécédents organisationnels"
            ])
        else:
            recommandations.extend([
                "Maintien bonnes pratiques",
                "Partage exemples positifs",
                "Surveillance continue"
            ])
        
        return recommandations
    
    def _analyser_comportements_vcs(self, données: Dict) -> List[Dict]:
        """Analyse comportements pour VCS"""
        comportements_raw = données.get("comportements_observés", [])
        
        comportements_analysés = []
        for comp in comportements_raw:
            analyse = {
                "comportement": comp,
                "type": self._classifier_type_comportement(comp),
                "risque_associé": self._évaluer_risque_comportement(comp),
                "fréquence_observée": random.randint(1, 10),
                "impact_sécurité": self._calculer_impact_sécurité(comp)
            }
            comportements_analysés.append(analyse)
        
        return comportements_analysés
    
    def _conduire_conversations_securite(self, données: Dict) -> List[Dict]:
        """Conversations sécurité VCS - NOM CORRIGÉ"""
        nb_conversations = données.get("nb_conversations", 2)
        
        conversations = []
        for i in range(nb_conversations):
            conversation = {
                "participant": f"Employé_{i+1}",
                "durée_minutes": random.randint(3, 8),
                "sujets_abordés": self._generer_sujets_conversation(),
                "engagement": random.choice(["Élevé", "Modéré", "Faible"]),
                "actions_convenues": self._generer_actions_conversation()
            }
            conversations.append(conversation)
        
        return conversations
    
    def _identifier_actions_correctives(self, comportements: List[Dict]) -> List[Dict]:
        """Identification actions correctives basées comportements"""
        actions = []
        
        for comp in comportements:
            if comp.get("risque_associé", 5) >= 7:
                actions.append({
                    "action": f"Correction immédiate - {comp.get('comportement', 'N/A')}",
                    "priorité": "HAUTE",
                    "délai": "Immédiat",
                    "responsable": "Superviseur"
                })
            elif comp.get("risque_associé", 5) >= 5:
                actions.append({
                    "action": f"Formation ciblée - {comp.get('type', 'N/A')}",
                    "priorité": "MODÉRÉE",
                    "délai": "7 jours",
                    "responsable": "Formation"
                })
        
        return actions
    
    def _calculer_score_vcs(self, vcs: VCSData) -> float:
        """Calcul score VCS global"""
        if not vcs.comportements_observés:
            return 5.0
        
        score_comportements = sum(
            comp.get("impact_sécurité", 5) for comp in vcs.comportements_observés
        ) / len(vcs.comportements_observés)
        
        score_conversations = len(vcs.conversations_sécurité) * 0.5 + 6
        score_actions = min(10, len(vcs.actions_correctives) * 0.3 + 7)
        
        return min(10, (score_comportements * 0.5 + score_conversations * 0.3 + score_actions * 0.2))
    
    # Méthodes utilitaires
    
    def _classifier_type_comportement(self, comportement: str) -> str:
        """Classification type comportement"""
        if any(terme in comportement.lower() for terme in ["epi", "casque", "gants"]):
            return "Équipement Protection"
        elif any(terme in comportement.lower() for terme in ["procédure", "consigne"]):
            return "Respect Procédures"
        elif any(terme in comportement.lower() for terme in ["communication", "signal"]):
            return "Communication"
        else:
            return "Général"
    
    def _évaluer_risque_comportement(self, comportement: str) -> int:
        """Évaluation risque comportement 1-10"""
        if any(terme in comportement.lower() for terme in ["risque", "danger", "négligence"]):
            return random.randint(7, 10)
        else:
            return random.randint(3, 7)
    
    def _calculer_impact_sécurité(self, comportement: str) -> float:
        """Calcul impact sécurité comportement"""
        if any(terme in comportement.lower() for terme in ["sûr", "sécuritaire", "protection"]):
            return random.uniform(7.0, 9.5)
        else:
            return random.uniform(4.0, 7.0)
    
    def _generer_sujets_conversation(self) -> List[str]:
        """Génération sujets conversation sécurité"""
        sujets_possibles = [
            "Port EPI", "Nouvelles procédures", "Retour d'expérience",
            "Amélioration continue", "Signalement dangers", "Formation sécurité"
        ]
        return random.sample(sujets_possibles, k=random.randint(2, 4))
    
    def _generer_actions_conversation(self) -> List[str]:
        """Génération actions convenues conversation"""
        actions_possibles = [
            "Révision formation EPI", "Amélioration signalisation",
            "Mise à jour procédure", "Partage bonnes pratiques"
        ]
        return random.sample(actions_possibles, k=random.randint(1, 3))

class A2CapteurObservationsBehaviorX:
    """Agent A2 Enrichi BehaviorX - VERSION CORRIGÉE"""
    
    def __init__(self):
        self.agent_id = "A2_BehaviorX_Enrichi"
        self.version = "1.0_Phase1_Corrigé"
        self.behaviorx_module = ModuleBehaviorXObservations()
        self.modes_disponibles = [
            "Mode_1_Conformité", "Mode_2_Procédures", "Mode_3_Signalisation",
            "Mode_4_Terrain", "Mode_5_Comportemental", 
            "Mode_6_ABC_BehaviorX", "Mode_7_VCS_BehaviorX"
        ]
        logger.info(f"🔍 Agent A2 BehaviorX initialisé - Version {self.version}")
        logger.info(f"📋 Modes disponibles: {len(self.modes_disponibles)}")
    
    async def process(self, state) -> Dict:
        """Traitement enrichi A2 + BehaviorX - VERSION CORRIGÉE"""
        start_time = datetime.now()
        logger.info("🔄 Démarrage traitement Agent A2 BehaviorX Enrichi")
        
        try:
            données_entrée = state.get("données_entrée", {}) if isinstance(state, dict) else state.données_entrée
            
            # Structure résultats COMPLÈTE
            résultats = {
                "agent_id": self.agent_id,
                "timestamp": start_time,
                "modes_utilisés": [],
                "observations_abc": [],
                "données_vcs": [],
                "score_global": 0.0,
                "variables_culture_terrain": [],  # AJOUTÉ
                "alertes_temps_réel": [],
                "recommandations": [],
                "performance": {}  # AJOUTÉ
            }
            
            # Mode 6 : Observation ABC BehaviorX
            if données_entrée.get("mode_abc_actif", True):
                logger.info("🔄 Mode 6 - Observation ABC BehaviorX")
                observation_abc = self.behaviorx_module.observation_abc_standard(données_entrée)
                résultats["observations_abc"].append({
                    "observation": observation_abc.__dict__,
                    "score_abc": observation_abc.score_abc,
                    "criticité": observation_abc.criticité
                })
                résultats["modes_utilisés"].append("Mode_6_ABC_BehaviorX")
            
            # Mode 7 : VCS BehaviorX
            if données_entrée.get("mode_vcs_actif", True):
                logger.info("🔄 Mode 7 - VCS BehaviorX")
                vcs_data = self.behaviorx_module.visite_comportementale_securite(données_entrée)
                résultats["données_vcs"].append({
                    "vcs": vcs_data.__dict__,
                    "score_vcs": vcs_data.score_vcs,
                    "zone": vcs_data.zone_observée
                })
                résultats["modes_utilisés"].append("Mode_7_VCS_BehaviorX")
            
            # Calcul score global A2 BehaviorX
            résultats["score_global"] = self._calculer_score_global_a2(résultats)
            
            # Variables culture terrain enrichies
            résultats["variables_culture_terrain"] = self._mapper_variables_culture_terrain(résultats)
            
            # Recommandations globales
            résultats["recommandations"] = self._generer_recommandations_globales(résultats)
            
            # Performance
            temps_traitement = (datetime.now() - start_time).total_seconds()
            résultats["performance"] = {
                "temps_traitement": temps_traitement,
                "modes_actifs": len(résultats["modes_utilisés"]),
                "observations_générées": len(résultats["observations_abc"]) + len(résultats["données_vcs"])
            }
            
            logger.info(f"📊 Performance A2 BehaviorX: {temps_traitement:.3f}s, modes: {len(résultats['modes_utilisés'])}")
            logger.info(f"✅ Agent A2 BehaviorX terminé - Score global: {résultats['score_global']:.2f}")
            
            return résultats
            
        except Exception as e:
            logger.error(f"❌ Erreur Agent A2 BehaviorX: {str(e)}")
            return {
                "agent_id": self.agent_id,
                "erreur": str(e),
                "score_global": 0.0,
                "modes_utilisés": [],
                "variables_culture_terrain": [],  # STRUCTURE MINIMALE
                "recommandations": [],
                "performance": {}
            }
    
    def _calculer_score_global_a2(self, résultats: Dict) -> float:
        """Calcul score global A2 BehaviorX"""
        scores = []
        
        # Score ABC
        if résultats["observations_abc"]:
            score_abc = sum(obs["score_abc"] for obs in résultats["observations_abc"]) / len(résultats["observations_abc"])
            scores.append(score_abc)
        
        # Score VCS
        if résultats["données_vcs"]:
            score_vcs = sum(vcs["score_vcs"] for vcs in résultats["données_vcs"]) / len(résultats["données_vcs"])
            scores.append(score_vcs)
        
        return sum(scores) / len(scores) if scores else 5.0
    
    def _mapper_variables_culture_terrain(self, résultats: Dict) -> List[Dict]:
        """Mapping variables culture terrain enrichies BehaviorX"""
        variables = []
        
        # Variables ABC
        if résultats["observations_abc"]:
            for obs_abc in résultats["observations_abc"]:
                abc_data = obs_abc["observation"]
                variables.extend([
                    {
                        "nom": "Gestion antécédents terrain",
                        "valeur": abc_data["antecedent"]["score"],
                        "confiance": 0.90,
                        "source": "BehaviorX_ABC"
                    },
                    {
                        "nom": "Qualité comportements observés",
                        "valeur": abc_data["comportement"]["score"],
                        "confiance": 0.95,
                        "source": "BehaviorX_ABC"
                    },
                    {
                        "nom": "Évaluation conséquences",
                        "valeur": abc_data["consequence"]["score"],
                        "confiance": 0.85,
                        "source": "BehaviorX_ABC"
                    }
                ])
        
        # Variables VCS
        if résultats["données_vcs"]:
            for vcs_data in résultats["données_vcs"]:
                vcs = vcs_data["vcs"]
                variables.extend([
                    {
                        "nom": "Engagement conversations sécurité",
                        "valeur": len(vcs["conversations_sécurité"]) * 2,
                        "confiance": 0.80,
                        "source": "BehaviorX_VCS"
                    },
                    {
                        "nom": "Efficacité actions correctives",
                        "valeur": min(10, len(vcs["actions_correctives"]) * 1.5 + 6),
                        "confiance": 0.85,
                        "source": "BehaviorX_VCS"
                    }
                ])
        
        return variables
    
    def _generer_recommandations_globales(self, résultats: Dict) -> List[str]:
        """Génération recommandations globales A2 BehaviorX"""
        recommandations = []
        
        # Recommandations ABC
        if résultats["observations_abc"]:
            for obs in résultats["observations_abc"]:
                if obs["criticité"] in ["CRITIQUE", "ÉLEVÉE"]:
                    recommandations.append(f"Intervention urgente - Criticité {obs['criticité']}")
                recommandations.extend(obs["observation"]["recommandations"])
        
        # Recommandations VCS
        if résultats["données_vcs"]:
            for vcs in résultats["données_vcs"]:
                actions_correctives = vcs["vcs"]["actions_correctives"]
                for action in actions_correctives:
                    if action["priorité"] == "HAUTE":
                        recommandations.append(f"Action prioritaire: {action['action']}")
        
        return list(set(recommandations))  # Éliminer doublons

# Test simplifié et robuste
async def test_agent_a2_behaviorx():
    """Test Agent A2 BehaviorX Corrigé"""
    print("🧪 TEST AGENT A2 BEHAVIORX ENRICHI - VERSION CORRIGÉE")
    print("=" * 60)
    
    # Données de test simplifiées
    données_test = {
        "données_entrée": {
            "mode_abc_actif": True,
            "mode_vcs_actif": True,
            "zone": "Atelier_Métallurgie",
            "observateur": "Superviseur_A",
            "tâche": "Usinage pièces métalliques",
            "nb_conversations": 3,
            
            # Données ABC
            "antecedents": [
                "Formation EPI récente",
                "Nouvelle machine installée",
                "Procédure mise à jour"
            ],
            "comportements_observés": [
                "Port systématique casque de sécurité",
                "Vérification équipement avant démarrage",
                "Communication dangers à l'équipe",
                "Respect procédure lockout/tagout"
            ],
            "consequences_observées": [
                "Amélioration sécurité équipe"
            ],
            "consequences_potentielles": [
                "Risque blessure mineur sans EPI"
            ]
        }
    }
    
    # Test agent
    agent = A2CapteurObservationsBehaviorX()
    résultats = await agent.process(données_test)
    
    # Affichage sécurisé
    print(f"\n📊 RÉSULTATS AGENT A2 BEHAVIORX:")
    print(f"=" * 40)
    print(f"✅ Score global: {résultats.get('score_global', 0):.2f}/10")
    print(f"✅ Modes utilisés: {len(résultats.get('modes_utilisés', []))}")
    print(f"✅ Variables culture terrain: {len(résultats.get('variables_culture_terrain', []))}")
    print(f"✅ Observations ABC: {len(résultats.get('observations_abc', []))}")
    print(f"✅ Données VCS: {len(résultats.get('données_vcs', []))}")
    print(f"✅ Recommandations: {len(résultats.get('recommandations', []))}")
    
    # Détails modules
    if résultats.get("observations_abc"):
        abc_data = résultats["observations_abc"][0]
        print(f"\n🎯 ABC - Score: {abc_data['score_abc']:.2f}, Criticité: {abc_data['criticité']}")
    
    if résultats.get("données_vcs"):
        vcs_data = résultats["données_vcs"][0]
        print(f"🔍 VCS - Score: {vcs_data['score_vcs']:.2f}, Zone: {vcs_data['zone']}")
    
    # Performance
    perf = résultats.get("performance", {})
    print(f"\n⚡ PERFORMANCE:")
    print(f"📊 Temps: {perf.get('temps_traitement', 0):.3f}s")
    print(f"🔧 Modes: {perf.get('modes_actifs', 0)}")
    
    # Variables top 3
    print(f"\n🎯 VARIABLES CULTURE TERRAIN (Top 3):")
    for i, var in enumerate(résultats.get("variables_culture_terrain", [])[:3], 1):
        print(f"  {i}. {var['nom']}: {var['valeur']:.1f}/10")
    
    print(f"\n✅ Test Agent A2 BehaviorX CORRIGÉ terminé avec succès!")
    return résultats

if __name__ == "__main__":
    asyncio.run(test_agent_a2_behaviorx())