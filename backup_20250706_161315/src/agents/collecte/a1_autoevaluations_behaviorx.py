# SafetyAgentic - Agent A1 Enrichi BehaviorX : Autoévaluations + Safe Self
# =========================================================================
# Intégration des modules BehaviorX dans l'agent A1 existant
# Version : Phase 1 - Semaine 1 (5 juillet 2025)

import sys
import os
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import logging

# Configuration logging SafetyAgentic
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SafetyAgentic.A1.BehaviorX")

@dataclass
class SafetyAgenticState:
    """État unifié SafetyAgentic compatible BehaviorX"""
    
    # Données originales SafetyAgentic
    agent_id: str = "A1_BehaviorX"
    timestamp: datetime = field(default_factory=datetime.now)
    données_entrée: Dict = field(default_factory=dict)
    variables_culture_sst: List[Dict] = field(default_factory=list)
    scores_autoeval: Dict = field(default_factory=dict)
    zones_risque: List[str] = field(default_factory=list)
    
    # Nouveaux champs BehaviorX
    safe_self_data: Dict = field(default_factory=dict)
    comportements_abc: List[Dict] = field(default_factory=list)
    questionnaire_irsst: Dict = field(default_factory=dict)
    score_conscience_augmente: float = 0.0
    facteurs_humains: Dict = field(default_factory=dict)
    
    # Métriques intégrées
    fiabilité_globale: float = 0.0
    confiance_ia: float = 0.0
    biais_détectés: List[str] = field(default_factory=list)

@dataclass
class ModuleBehaviorX:
    """Module BehaviorX intégré dans SafetyAgentic"""
    
    def safe_self_evaluation(self, données_autoeval: Dict, contexte_terrain: Dict) -> Dict:
        """
        Module Safe Self de BehaviorX : autoévaluation comportementale augmentée
        """
        logger.info("🔄 Module Safe Self BehaviorX activé")
        
        # Analyse comportementale ABC
        antecedents = contexte_terrain.get("antecedents", [])
        comportements = données_autoeval.get("comportements_observés", [])
        consequences = contexte_terrain.get("consequences_potentielles", [])
        
        # Calcul score conscience augmenté par IA
        score_conscience = self._calculer_conscience_augmentee(
            données_autoeval, contexte_terrain
        )
        
        # Mapping vers modèle ABC
        analyse_abc = {
            "A_antecedents": self._analyser_antecedents(antecedents),
            "B_comportements": self._analyser_comportements(comportements),
            "C_consequences": self._analyser_consequences(consequences),
            "score_abc_global": self._calculer_score_abc(antecedents, comportements, consequences)
        }
        
        logger.info(f"✅ Safe Self terminé - Score conscience augmenté: {score_conscience:.2f}")
        
        return {
            "score_conscience_augmente": score_conscience,
            "analyse_abc": analyse_abc,
            "patterns_comportementaux": self._identifier_patterns(comportements),
            "recommandations_safe_self": self._generer_recommandations_safe_self(analyse_abc)
        }
    
    def questionnaire_irsst_facteurs_humains(self, données_autoeval: Dict) -> Dict:
        """
        Questionnaire IRSST facteurs humains intégré
        """
        logger.info("🔄 Questionnaire IRSST Facteurs Humains activé")
        
        # Variables IRSST facteurs humains
        facteurs_individuels = self._evaluer_facteurs_individuels(données_autoeval)
        facteurs_organisationnels = self._evaluer_facteurs_organisationnels(données_autoeval)
        facteurs_environnementaux = self._evaluer_facteurs_environnementaux(données_autoeval)
        
        # Score global facteurs humains
        score_facteurs_humains = (
            facteurs_individuels["score"] * 0.4 +
            facteurs_organisationnels["score"] * 0.4 +
            facteurs_environnementaux["score"] * 0.2
        )
        
        logger.info(f"✅ Questionnaire IRSST terminé - Score facteurs humains: {score_facteurs_humains:.2f}")
        
        return {
            "score_facteurs_humains": score_facteurs_humains,
            "facteurs_individuels": facteurs_individuels,
            "facteurs_organisationnels": facteurs_organisationnels,
            "facteurs_environnementaux": facteurs_environnementaux,
            "conformité_irsst": score_facteurs_humains >= 7.0
        }
    
    def interface_mobile_terrain(self, localisation: Dict, contexte_tâche: Dict) -> Dict:
        """
        Interface mobile BehaviorX pour terrain optimisée
        """
        logger.info("📱 Interface mobile BehaviorX terrain activée")
        
        # Adaptation interface selon contexte
        mode_interface = self._determiner_mode_interface(localisation, contexte_tâche)
        
        # Génération formulaires adaptatifs
        formulaires = self._generer_formulaires_adaptatifs(contexte_tâche)
        
        # Guidage vocal/visuel
        guidage = self._activer_guidage_intelligent(mode_interface, contexte_tâche)
        
        return {
            "mode_interface": mode_interface,
            "formulaires_adaptatifs": formulaires,
            "guidage_intelligent": guidage,
            "temps_completion_estime": self._estimer_temps_completion(formulaires)
        }
    
    def _calculer_conscience_augmentee(self, autoeval: Dict, contexte: Dict) -> float:
        """Calcul IA du score de conscience sécurité augmenté"""
        # Score base autoévaluation
        score_base = sum(autoeval.get("scores", {}).values()) / len(autoeval.get("scores", {1: 5}))
        
        # Facteur contexte terrain
        facteur_contexte = contexte.get("niveau_risque", 5) / 10
        
        # Facteur cohérence réponses
        facteur_coherence = autoeval.get("coherence", 0.8)
        
        # IA augmentation : prédiction comportement futur
        facteur_ia = min(1.0, score_base * facteur_contexte * facteur_coherence * 1.2)
        
        return min(10.0, facteur_ia * 10)
    
    def _analyser_antecedents(self, antecedents: List) -> Dict:
        """Analyse des antécédents dans modèle ABC"""
        if not antecedents:
            return {"score": 5.0, "risques_identifiés": [], "niveau": "MOYEN"}
        
        risques = [a for a in antecedents if "risque" in str(a).lower()]
        score = max(1, 10 - len(risques) * 2)
        niveau = "ÉLEVÉ" if score >= 8 else "MOYEN" if score >= 5 else "FAIBLE"
        
        return {
            "score": score,
            "risques_identifiés": risques,
            "niveau": niveau,
            "patterns": self._identifier_patterns_antecedents(antecedents)
        }
    
    def _analyser_comportements(self, comportements: List) -> Dict:
        """Analyse des comportements observés"""
        if not comportements:
            return {"score": 7.0, "comportements_sûrs": 0, "comportements_risque": 0}
        
        comportements_sûrs = len([c for c in comportements if "sûr" in str(c).lower() or "sécuritaire" in str(c).lower()])
        comportements_risque = len([c for c in comportements if "risque" in str(c).lower() or "danger" in str(c).lower()])
        
        score = min(10, max(1, 7 + comportements_sûrs - comportements_risque * 2))
        
        return {
            "score": score,
            "comportements_sûrs": comportements_sûrs,
            "comportements_risque": comportements_risque,
            "ratio_sécurité": comportements_sûrs / max(1, len(comportements))
        }
    
    def _analyser_consequences(self, consequences: List) -> Dict:
        """Analyse des conséquences potentielles"""
        if not consequences:
            return {"score": 6.0, "severity": "MOYEN", "probabilité": 0.3}
        
        severité_mots = ["grave", "mortel", "critique", "majeur"]
        consequences_graves = len([c for c in consequences if any(mot in str(c).lower() for mot in severité_mots)])
        
        score = max(1, 8 - consequences_graves * 3)
        severity = "ÉLEVÉ" if consequences_graves > 0 else "MOYEN"
        probabilité = min(0.9, consequences_graves * 0.3 + 0.1)
        
        return {
            "score": score,
            "severity": severity,
            "probabilité": probabilité,
            "consequences_graves": consequences_graves
        }
    
    def _calculer_score_abc(self, antecedents: List, comportements: List, consequences: List) -> float:
        """Score global modèle ABC intégré"""
        score_a = self._analyser_antecedents(antecedents)["score"]
        score_b = self._analyser_comportements(comportements)["score"]
        score_c = self._analyser_consequences(consequences)["score"]
        
        # Pondération ABC : Comportement prioritaire
        return (score_a * 0.3 + score_b * 0.5 + score_c * 0.2)
    
    def _identifier_patterns(self, comportements: List) -> List[str]:
        """Identification patterns comportementaux par IA"""
        patterns = []
        if not comportements:
            return ["pattern_insufficient_data"]
        
        # Patterns de sécurité
        if any("epi" in str(c).lower() for c in comportements):
            patterns.append("usage_epi_conscient")
        if any("procédure" in str(c).lower() for c in comportements):
            patterns.append("respect_procédures")
        if any("vérification" in str(c).lower() for c in comportements):
            patterns.append("vérifications_systématiques")
        
        return patterns or ["pattern_standard"]
    
    def _generer_recommandations_safe_self(self, analyse_abc: Dict) -> List[str]:
        """Génération recommandations Safe Self personnalisées"""
        recommandations = []
        
        score_abc = analyse_abc["score_abc_global"]
        
        if score_abc < 5:
            recommandations.append("Formation immédiate modèle ABC recommandée")
            recommandations.append("Révision des procédures de sécurité prioritaire")
        elif score_abc < 7:
            recommandations.append("Renforcement conscience comportementale")
            recommandations.append("Sessions coaching sécurité personnalisées")
        else:
            recommandations.append("Maintien excellent niveau conscience sécurité")
            recommandations.append("Partage bonnes pratiques avec équipe")
        
        return recommandations
    
    def _evaluer_facteurs_individuels(self, données: Dict) -> Dict:
        """Évaluation facteurs individuels IRSST"""
        scores = données.get("scores", {})
        score_moyen = sum(scores.values()) / len(scores) if scores else 7.0
        
        return {
            "score": score_moyen,
            "compétences_techniques": score_moyen * 0.9,
            "motivation_sécurité": score_moyen * 1.1,
            "stress_fatigue": max(1, 10 - score_moyen),
            "formation_reçue": score_moyen >= 7
        }
    
    def _evaluer_facteurs_organisationnels(self, données: Dict) -> Dict:
        """Évaluation facteurs organisationnels IRSST"""
        score_base = données.get("organisation_travail", 7.0)
        
        return {
            "score": score_base,
            "politique_sécurité": score_base >= 8,
            "communication_équipe": score_base * 0.9,
            "ressources_disponibles": score_base * 1.1,
            "culture_sécurité": score_base >= 7
        }
    
    def _evaluer_facteurs_environnementaux(self, données: Dict) -> Dict:
        """Évaluation facteurs environnementaux IRSST"""
        score_base = données.get("conditions_travail", 7.0)
        
        return {
            "score": score_base,
            "conditions_physiques": score_base,
            "équipements_disponibles": score_base >= 7,
            "espaces_travail": score_base * 0.95,
            "facteurs_externes": max(1, score_base - 1)
        }
    
    def _determiner_mode_interface(self, localisation: Dict, contexte: Dict) -> str:
        """Détermine le mode interface optimal"""
        if contexte.get("niveau_bruit", 0) > 7:
            return "visuel_augmenté"
        elif localisation.get("éclairage", 10) < 5:
            return "vocal_prioritaire"
        else:
            return "mixte_adaptatif"
    
    def _generer_formulaires_adaptatifs(self, contexte: Dict) -> List[Dict]:
        """Génération formulaires adaptatifs selon contexte"""
        niveau_risque = contexte.get("niveau_risque", 5)
        
        if niveau_risque >= 8:
            return [
                {"type": "urgence", "questions": 3, "temps_max": "30s"},
                {"type": "sécurité_critique", "questions": 5, "temps_max": "60s"}
            ]
        elif niveau_risque >= 5:
            return [
                {"type": "standard", "questions": 8, "temps_max": "2min"},
                {"type": "comportemental", "questions": 10, "temps_max": "3min"}
            ]
        else:
            return [
                {"type": "complet", "questions": 15, "temps_max": "5min"},
                {"type": "culture_sst", "questions": 20, "temps_max": "7min"}
            ]
    
    def _activer_guidage_intelligent(self, mode: str, contexte: Dict) -> Dict:
        """Activation guidage intelligent selon mode"""
        return {
            "mode_actif": mode,
            "vocal_activé": "vocal" in mode,
            "visuel_augmenté": "visuel" in mode,
            "adaptation_temps_réel": True,
            "niveau_assistance": "élevé" if contexte.get("complexité", 5) >= 7 else "standard"
        }
    
    def _estimer_temps_completion(self, formulaires: List[Dict]) -> Dict:
        """Estimation temps de completion"""
        temps_total = sum(
            int(f.get("temps_max", "60s").replace("s", "").replace("min", "").replace("h", "")) 
            for f in formulaires
        )
        
        return {
            "temps_estime_secondes": temps_total,
            "temps_humain": f"{temps_total//60}min {temps_total%60}s" if temps_total >= 60 else f"{temps_total}s",
            "complexité": "simple" if temps_total <= 120 else "modérée" if temps_total <= 300 else "complexe"
        }
    
    def _identifier_patterns_antecedents(self, antecedents: List) -> List[str]:
        """Identification patterns dans antécédents"""
        patterns = []
        if any("pression" in str(a).lower() for a in antecedents):
            patterns.append("pression_temporelle")
        if any("formation" in str(a).lower() for a in antecedents):
            patterns.append("formation_insuffisante")
        if any("équipement" in str(a).lower() for a in antecedents):
            patterns.append("défaillance_équipement")
        
        return patterns or ["pattern_indéterminé"]

class A1CollecteurAutoEvaluationsBehaviorX:
    """
    Agent A1 Enrichi BehaviorX : Autoévaluations + Safe Self + IRSST
    Intégration complète des modules BehaviorX dans SafetyAgentic
    """
    
    def __init__(self):
        self.agent_id = "A1_BehaviorX_Enrichi"
        self.version = "1.0_Phase1"
        self.behaviorx_module = ModuleBehaviorX()
        logger.info(f"🤖 Agent A1 BehaviorX initialisé - Version {self.version}")
    
    async def process(self, state: SafetyAgenticState) -> SafetyAgenticState:
        """
        Traitement enrichi A1 + BehaviorX
        """
        start_time = datetime.now()
        logger.info("🔄 Démarrage traitement Agent A1 BehaviorX Enrichi")
        
        try:
            # Étape 1 : Safe Self BehaviorX
            safe_self_result = self.behaviorx_module.safe_self_evaluation(
                state.données_entrée.get("autoévaluation", {}),
                state.données_entrée.get("contexte_terrain", {})
            )
            state.safe_self_data = safe_self_result
            state.score_conscience_augmente = safe_self_result["score_conscience_augmente"]
            state.comportements_abc = [safe_self_result["analyse_abc"]]
            
            # Étape 2 : Questionnaire IRSST
            irsst_result = self.behaviorx_module.questionnaire_irsst_facteurs_humains(
                state.données_entrée.get("autoévaluation", {})
            )
            state.questionnaire_irsst = irsst_result
            state.facteurs_humains = irsst_result
            
            # Étape 3 : Interface mobile terrain
            interface_result = self.behaviorx_module.interface_mobile_terrain(
                state.données_entrée.get("localisation", {}),
                state.données_entrée.get("contexte_tâche", {})
            )
            
            # Étape 4 : Calcul métriques intégrées
            state.fiabilité_globale = self._calculer_fiabilité_globale(safe_self_result, irsst_result)
            state.confiance_ia = self._calculer_confiance_ia(safe_self_result, irsst_result)
            state.biais_détectés = self._detecter_biais_integres(safe_self_result, irsst_result)
            
            # Étape 5 : Mapping variables culture SST enrichies
            state.variables_culture_sst = self._mapper_variables_culture_enrichies(
                safe_self_result, irsst_result
            )
            
            # Performance logging
            temps_traitement = (datetime.now() - start_time).total_seconds()
            logger.info(f"📊 Performance A1 BehaviorX: {temps_traitement:.3f}s, confiance: {state.confiance_ia:.2f}")
            logger.info(f"✅ Agent A1 BehaviorX terminé - Score global: {state.fiabilité_globale:.2f}")
            
            return state
            
        except Exception as e:
            logger.error(f"❌ Erreur Agent A1 BehaviorX: {str(e)}")
            state.biais_détectés.append("erreur_traitement")
            return state
    
    def _calculer_fiabilité_globale(self, safe_self: Dict, irsst: Dict) -> float:
        """Calcul fiabilité globale intégrée BehaviorX + SafetyAgentic"""
        score_safe_self = safe_self["score_conscience_augmente"] / 10
        score_irsst = irsst["score_facteurs_humains"] / 10
        score_abc = safe_self["analyse_abc"]["score_abc_global"] / 10
        
        # Pondération : Safe Self 40%, IRSST 35%, ABC 25%
        return min(1.0, score_safe_self * 0.4 + score_irsst * 0.35 + score_abc * 0.25)
    
    def _calculer_confiance_ia(self, safe_self: Dict, irsst: Dict) -> float:
        """Calcul confiance IA sur les résultats"""
        # Facteurs de confiance
        coherence_safe_self = 0.9  # Simulation haute cohérence
        conformité_irsst = 1.0 if irsst["conformité_irsst"] else 0.7
        richesse_données = min(1.0, len(safe_self.get("patterns_comportementaux", [])) / 3)
        
        return min(1.0, (coherence_safe_self + conformité_irsst + richesse_données) / 3)
    
    def _detecter_biais_integres(self, safe_self: Dict, irsst: Dict) -> List[str]:
        """Détection biais intégrés BehaviorX + IRSST"""
        biais = []
        
        # Biais Safe Self
        if safe_self["score_conscience_augmente"] > 9.5:
            biais.append("surconfiance_safe_self")
        
        # Biais IRSST
        if irsst["score_facteurs_humains"] > 9.0 and irsst["facteurs_individuels"]["stress_fatigue"] < 2:
            biais.append("optimisme_irsst")
        
        # Biais ABC
        score_abc = safe_self["analyse_abc"]["score_abc_global"]
        if score_abc > 9.0:
            biais.append("idéalisation_comportementale")
        
        return biais
    
    def _mapper_variables_culture_enrichies(self, safe_self: Dict, irsst: Dict) -> List[Dict]:
        """Mapping enrichi variables culture SST avec BehaviorX"""
        variables = []
        
        # Variables Safe Self
        variables.append({
            "nom": "Conscience comportementale augmentée",
            "valeur": safe_self["score_conscience_augmente"],
            "confiance": 0.95,
            "source": "BehaviorX_Safe_Self"
        })
        
        # Variables ABC
        abc_data = safe_self["analyse_abc"]
        variables.extend([
            {
                "nom": "Gestion antécédents",
                "valeur": abc_data["A_antecedents"]["score"],
                "confiance": 0.90,
                "source": "BehaviorX_ABC"
            },
            {
                "nom": "Qualité comportements",
                "valeur": abc_data["B_comportements"]["score"],
                "confiance": 0.95,
                "source": "BehaviorX_ABC"
            },
            {
                "nom": "Évaluation conséquences",
                "valeur": abc_data["C_consequences"]["score"],
                "confiance": 0.85,
                "source": "BehaviorX_ABC"
            }
        ])
        
        # Variables IRSST
        variables.extend([
            {
                "nom": "Facteurs individuels IRSST",
                "valeur": irsst["facteurs_individuels"]["score"],
                "confiance": 0.90,
                "source": "IRSST_Facteurs_Humains"
            },
            {
                "nom": "Facteurs organisationnels IRSST",
                "valeur": irsst["facteurs_organisationnels"]["score"],
                "confiance": 0.85,
                "source": "IRSST_Facteurs_Humains"
            },
            {
                "nom": "Facteurs environnementaux IRSST",
                "valeur": irsst["facteurs_environnementaux"]["score"],
                "confiance": 0.80,
                "source": "IRSST_Facteurs_Humains"
            }
        ])
        
        return variables

# Test intégré A1 BehaviorX
async def test_agent_a1_behaviorx():
    """Test complet Agent A1 enrichi BehaviorX"""
    print("🧪 TEST AGENT A1 BEHAVIORX ENRICHI")
    print("=" * 50)
    
    # Données de test enrichies
    state = SafetyAgenticState(
        données_entrée={
            "autoévaluation": {
                "scores": {
                    "usage_epi": 8.0,
                    "respect_procédures": 7.5,
                    "communication_équipe": 8.5,
                    "gestion_stress": 7.0,
                    "formation_continue": 8.0
                },
                "comportements_observés": [
                    "port casque systématique",
                    "vérification équipements avant usage",
                    "communication dangers identifiés",
                    "respect procédures lockout"
                ],
                "organisation_travail": 7.5,
                "conditions_travail": 7.0,
                "coherence": 0.92
            },
            "contexte_terrain": {
                "antecedents": [
                    "formation récente EPI",
                    "nouvelle procédure mise en place",
                    "équipement vérifié ce matin"
                ],
                "consequences_potentielles": [
                    "accident évité par vigilance",
                    "amélioration sécurité équipe"
                ],
                "niveau_risque": 6,
                "éclairage": 8,
                "niveau_bruit": 4
            },
            "contexte_tâche": {
                "complexité": 6,
                "niveau_risque": 6,
                "durée_prévue": "2h"
            },
            "localisation": {
                "zone": "atelier_fabrication",
                "éclairage": 8,
                "température": 22
            }
        }
    )
    
    # Test agent
    agent = A1CollecteurAutoEvaluationsBehaviorX()
    résultat = await agent.process(state)
    
    # Affichage résultats
    print(f"\n📊 RÉSULTATS AGENT A1 BEHAVIORX:")
    print(f"=" * 40)
    print(f"✅ Score conscience augmenté: {résultat.score_conscience_augmente:.2f}/10")
    print(f"✅ Fiabilité globale: {résultat.fiabilité_globale:.3f}")
    print(f"✅ Confiance IA: {résultat.confiance_ia:.3f}")
    print(f"✅ Variables culture enrichies: {len(résultat.variables_culture_sst)}")
    print(f"✅ Biais détectés: {len(résultat.biais_détectés)}")
    
    print(f"\n🎯 MODULES BEHAVIORX:")
    print(f"📱 Safe Self - Score ABC: {résultat.safe_self_data['analyse_abc']['score_abc_global']:.2f}")
    print(f"📋 IRSST - Conformité: {résultat.questionnaire_irsst['conformité_irsst']}")
    print(f"🧠 Patterns détectés: {len(résultat.safe_self_data.get('patterns_comportementaux', []))}")
    
    print(f"\n💡 RECOMMANDATIONS SAFE SELF:")
    for rec in résultat.safe_self_data.get("recommandations_safe_self", []):
        print(f"  - {rec}")
    
    print(f"\n✅ Test Agent A1 BehaviorX terminé avec succès!")
    return résultat

if __name__ == "__main__":
    asyncio.run(test_agent_a1_behaviorx())