# Agent R1 - Générateur Recommandations SafetyAgentic
# ===================================================
# Transforme zones aveugles AN1 en plan d'action concret
# Basé sur meilleures pratiques HSE et données CNESST

import asyncio
from typing import Dict, List, Tuple, Optional
import json
import logging
from datetime import datetime, timedelta
import numpy as np

# Configuration logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SafetyAgentic.R1")

class R1GenerateurRecommandations:
    """
    Agent R1 - Générateur de Recommandations
    
    Fonctions principales:
    1. Analyser zones aveugles AN1 et contexte incident
    2. Générer recommandations spécifiques par zone aveugle
    3. Créer plan d'action structuré avec priorités
    4. Calculer ressources, budgets et ROI estimés
    5. Adapter recommandations selon secteur SCIAN
    6. Intégrer meilleures pratiques HSE sectorielles
    """
    
    def __init__(self):
        """Initialisation Agent R1"""
        self.agent_id = "R1"
        self.agent_name = "Générateur Recommandations"
        self.version = "1.0.0"
        
        # Base de connaissances recommandations par variable
        self.recommandations_db = {
            "usage_epi": {
                "formations": [
                    "Formation pratique port EPI obligatoire",
                    "Sensibilisation risques spécifiques poste",
                    "Démonstration équipements protection"
                ],
                "procedures": [
                    "Check-list quotidienne EPI par poste",
                    "Contrôles visuels superviseurs",
                    "Sanctions progressives non-conformité"
                ],
                "equipements": [
                    "Audit qualité EPI fournis",
                    "Remplacement équipements défaillants",
                    "Test confort et ergonomie EPI"
                ],
                "budget_unitaire": 150,  # $ par employé
                "duree_formation": 4     # heures
            },
            
            "supervision_directe": {
                "formations": [
                    "Formation supervision sécurité superviseurs",
                    "Techniques communication risques",
                    "Leadership sécurité terrain"
                ],
                "procedures": [
                    "Rondes sécurité obligatoires (2x/jour)",
                    "Check-lists supervision standardisées",
                    "Reporting hebdomadaire sécurité"
                ],
                "organisationnel": [
                    "Définir ratio superviseur/employé optimal",
                    "Réorganiser planning supervision",
                    "Système reconnaissance supervision exemplaire"
                ],
                "budget_unitaire": 800,
                "duree_formation": 16
            },
            
            "formation_securite": {
                "formations": [
                    "Mise à jour formations sécurité sectorielles",
                    "Certifications obligatoires par poste",
                    "Recyclage annuel competences sécurité"
                ],
                "procedures": [
                    "Matrice compétences sécurité par poste",
                    "Évaluation pratique post-formation",
                    "Suivi continu acquisitions compétences"
                ],
                "pedagogique": [
                    "Supports formation interactifs",
                    "Simulations incidents sectoriels",
                    "Mentorat sécurité senior/junior"
                ],
                "budget_unitaire": 400,
                "duree_formation": 8
            },
            
            "communication_risques": {
                "formations": [
                    "Formation communication risques efficace",
                    "Techniques feedback sécurité",
                    "Animation toolbox meetings"
                ],
                "procedures": [
                    "Meetings sécurité hebdomadaires obligatoires",
                    "Système remontée incidents/presqu'accidents",
                    "Affichage risques spécifiques postes"
                ],
                "organisationnel": [
                    "Nomination référents sécurité par équipe",
                    "Boîte à idées amélioration sécurité",
                    "Feedback loop management/terrain"
                ],
                "budget_unitaire": 200,
                "duree_formation": 6
            },
            
            "leadership_sst": {
                "formations": [
                    "Leadership sécurité pour managers",
                    "Excellence opérationnelle et sécurité",
                    "Culture sécurité haute performance"
                ],
                "procedures": [
                    "Engagement visible leadership terrain",
                    "Objectifs sécurité dans évaluations",
                    "Reconnaissance comportements sécuritaires"
                ],
                "strategique": [
                    "Politique sécurité renforcée direction",
                    "Investissements sécurité prioritaires",
                    "Certification management sécurité"
                ],
                "budget_unitaire": 1200,
                "duree_formation": 24
            },
            
            "respect_procedures": {
                "formations": [
                    "Formation procédures sécurité spécifiques",
                    "Importance respect consignes",
                    "Conséquences non-conformités"
                ],
                "procedures": [
                    "Simplification procédures complexes",
                    "Audit conformité procédures mensuel",
                    "Système suggestions amélioration"
                ],
                "organisationnel": [
                    "Révision procédures obsolètes",
                    "Co-construction procédures avec terrain",
                    "Digitalisation check-lists terrain"
                ],
                "budget_unitaire": 300,
                "duree_formation": 6
            }
        }
        
        # Facteurs sectoriels SCIAN
        self.facteurs_sectoriels = {
            "CONSTRUCTION": {
                "multiplicateur_budget": 1.3,
                "duree_implementation": 1.2,
                "priorites_specifiques": ["hauteur", "machines_lourdes", "coordination_equipes"],
                "regulations": ["CSTC", "CCQ", "CSST"]
            },
            "SOINS_SANTE": {
                "multiplicateur_budget": 0.9,
                "duree_implementation": 0.8,
                "priorites_specifiques": ["infections", "manutention_patients", "produits_chimiques"],
                "regulations": ["MSSS", "OIQ", "OIIQ"]
            },
            "FABRICATION": {
                "multiplicateur_budget": 1.1,
                "duree_implementation": 1.0,
                "priorites_specifiques": ["machines_production", "produits_chimiques", "bruit"],
                "regulations": ["CNESST", "MAPAQ", "ECCC"]
            },
            "TRANSPORT": {
                "multiplicateur_budget": 1.0,
                "duree_implementation": 0.9,
                "priorites_specifiques": ["fatigue", "conduite_defensive", "manutention"],
                "regulations": ["MTQ", "TC", "SAAQ"]
            }
        }
        
        # Templates d'actions par niveau priorité
        self.action_templates = {
            "CRITIQUE": {
                "timeline": "0-2 semaines",
                "niveau_ressources": "Maximum",
                "suivi": "Quotidien",
                "indicateurs": ["Réduction écart >80%", "Zéro incident"]
            },
            "URGENTE": {
                "timeline": "2-4 semaines", 
                "niveau_ressources": "Élevé",
                "suivi": "Hebdomadaire",
                "indicateurs": ["Réduction écart >60%", "Conformité >90%"]
            },
            "ÉLEVÉE": {
                "timeline": "1-2 mois",
                "niveau_ressources": "Modéré",
                "suivi": "Bi-hebdomadaire", 
                "indicateurs": ["Réduction écart >40%", "Conformité >80%"]
            },
            "MOYENNE": {
                "timeline": "2-3 mois",
                "niveau_ressources": "Standard",
                "suivi": "Mensuel",
                "indicateurs": ["Réduction écart >25%", "Conformité >70%"]
            }
        }
        
        logger.info(f"🤖 Agent {self.agent_id} ({self.agent_name}) initialisé")
    
    async def process(self, data_an1: Dict, context: Dict = None) -> Dict:
        """
        Traitement principal: générer recommandations depuis zones aveugles AN1
        
        Args:
            data_an1: Résultats agent AN1 avec zones aveugles
            context: Contexte incident/secteur/organisation
            
        Returns:
            Dict avec plan d'action complet et recommandations
        """
        start_time = datetime.now()
        logger.info("🔄 Démarrage traitement Agent R1")
        
        try:
            # 1. Validation données AN1
            self._validate_an1_data(data_an1)
            logger.info("✅ Validation données AN1 réussie")
            
            # 2. Extraction zones aveugles prioritaires
            zones_aveugles = data_an1.get("ecarts_analysis", {}).get("zones_aveugles", [])
            priorite_globale = data_an1.get("summary", {}).get("priorite_intervention", "MOYENNE")
            
            # 3. Génération recommandations par zone aveugle
            recommandations_detaillees = self._generate_detailed_recommendations(
                zones_aveugles, context
            )
            
            # 4. Création plan d'action structuré
            plan_action = self._create_action_plan(
                recommandations_detaillees, priorite_globale, context
            )
            
            # 5. Calcul budgets et ressources
            budget_analysis = self._calculate_budget_resources(
                recommandations_detaillees, context
            )
            
            # 6. Génération timeline d'implémentation
            implementation_timeline = self._generate_implementation_timeline(
                plan_action, context
            )
            
            # 7. Métriques de succès et KPIs
            success_metrics = self._define_success_metrics(
                zones_aveugles, recommandations_detaillees
            )
            
            # 8. Calcul performance et confiance
            performance_time = (datetime.now() - start_time).total_seconds()
            confidence_score = self._calculate_confidence_score(zones_aveugles, context)
            
            logger.info(f"📊 Performance R1: {performance_time:.2f}s, confidence: {confidence_score:.2f}")
            
            # 9. Construction résultat final
            result = {
                "agent_info": {
                    "agent_id": self.agent_id,
                    "agent_name": self.agent_name, 
                    "version": self.version,
                    "timestamp": datetime.now().isoformat(),
                    "performance_time": performance_time,
                    "confidence_score": confidence_score
                },
                "recommandations_analysis": {
                    "zones_traitees": len(zones_aveugles),
                    "recommandations_generees": len(recommandations_detaillees),
                    "priorite_globale": priorite_globale,
                    "secteur_cible": context.get("secteur", "GENERAL") if context else "GENERAL"
                },
                "plan_action": plan_action,
                "recommandations_detaillees": recommandations_detaillees,
                "budget_analysis": budget_analysis,
                "implementation_timeline": implementation_timeline,
                "success_metrics": success_metrics,
                "business_impact": {
                    "roi_estime": budget_analysis.get("roi_estime", 0),
                    "cout_total": budget_analysis.get("cout_total", 0),
                    "economies_estimees": budget_analysis.get("economies_estimees", 0),
                    "payback_period": budget_analysis.get("payback_period", 0)
                }
            }
            
            logger.info(f"✅ Agent R1 terminé - {len(recommandations_detaillees)} recommandations générées")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur Agent R1: {str(e)}")
            return {"error": str(e), "agent_id": self.agent_id}
    
    def _validate_an1_data(self, data_an1: Dict):
        """Validation données AN1"""
        if not data_an1:
            raise ValueError("Données AN1 manquantes")
        
        required_fields = ["ecarts_analysis", "summary"]
        for field in required_fields:
            if field not in data_an1:
                raise ValueError(f"Champ AN1 manquant: {field}")
    
    def _generate_detailed_recommendations(self, zones_aveugles: List[Dict], context: Dict) -> List[Dict]:
        """Génération recommandations détaillées par zone aveugle"""
        recommandations = []
        
        secteur = context.get("secteur", "GENERAL") if context else "GENERAL"
        taille_entreprise = context.get("taille_entreprise", "MOYENNE") if context else "MOYENNE"
        
        for i, zone in enumerate(zones_aveugles, 1):
            variable = zone.get("variable", "")
            ecart_pct = zone.get("pourcentage_ecart", 0)
            niveau_critique = zone.get("niveau_critique", "MOYENNE")
            
            # Base recommandations depuis DB
            base_reco = self.recommandations_db.get(variable, {})
            if not base_reco:
                continue
            
            # Adaptation sectorielle
            facteur_sectoriel = self.facteurs_sectoriels.get(secteur, {
                "multiplicateur_budget": 1.0,
                "duree_implementation": 1.0,
                "priorites_specifiques": [],
                "regulations": []
            })
            
            # Template action selon priorité
            action_template = self.action_templates.get(niveau_critique, self.action_templates["MOYENNE"])
            
            # Calcul budget adapté
            budget_base = base_reco.get("budget_unitaire", 200)
            budget_adapte = budget_base * facteur_sectoriel["multiplicateur_budget"]
            
            # Ajustement selon taille entreprise
            multiplicateur_taille = {
                "PME": 0.7,
                "MOYENNE": 1.0, 
                "GRANDE": 1.4
            }.get(taille_entreprise, 1.0)
            
            budget_final = budget_adapte * multiplicateur_taille
            
            # Construction recommandation détaillée
            recommendation = {
                "id": f"R1_{i:02d}",
                "variable_cible": variable,
                "zone_aveugle": zone,
                "priorite": niveau_critique,
                "ecart_a_corriger": ecart_pct,
                
                # Actions détaillées
                "formations": base_reco.get("formations", []),
                "procedures": base_reco.get("procedures", []),
                "actions_organisationnelles": base_reco.get("organisationnel", []),
                "equipements": base_reco.get("equipements", []),
                
                # Planification
                "timeline": action_template["timeline"],
                "niveau_ressources": action_template["niveau_ressources"],
                "suivi_frequence": action_template["suivi"],
                "indicateurs_succes": action_template["indicateurs"],
                
                # Budget et ressources
                "budget_estime": budget_final,
                "duree_formation": base_reco.get("duree_formation", 4),
                "personnels_impliques": self._estimate_personnel_count(variable, taille_entreprise),
                
                # Adaptation sectorielle
                "specificites_secteur": facteur_sectoriel["priorites_specifiques"],
                "regulations_applicables": facteur_sectoriel["regulations"],
                
                # Méthode d'implémentation
                "methode_implementation": self._generate_implementation_method(
                    variable, niveau_critique, secteur
                ),
                "risques_implementation": self._identify_implementation_risks(variable, secteur),
                "facteurs_succes": self._identify_success_factors(variable, niveau_critique)
            }
            
            recommandations.append(recommendation)
        
        return recommandations
    
    def _create_action_plan(self, recommandations: List[Dict], priorite_globale: str, context: Dict) -> Dict:
        """Création plan d'action structuré"""
        
        # Grouper par priorité
        actions_par_priorite = {}
        for reco in recommandations:
            priorite = reco["priorite"]
            if priorite not in actions_par_priorite:
                actions_par_priorite[priorite] = []
            actions_par_priorite[priorite].append(reco)
        
        # Séquencement optimal
        sequence_optimale = self._optimize_action_sequence(recommandations)
        
        # Jalons clés
        jalons = self._define_key_milestones(recommandations, context)
        
        plan = {
            "priorite_globale": priorite_globale,
            "nombre_actions": len(recommandations),
            "duree_totale_estimee": self._calculate_total_duration(recommandations),
            "actions_par_priorite": actions_par_priorite,
            "sequence_optimale": sequence_optimale,
            "jalons_cles": jalons,
            "coordination_requise": self._identify_coordination_needs(recommandations),
            "ressources_critiques": self._identify_critical_resources(recommandations)
        }
        
        return plan
    
    def _calculate_budget_resources(self, recommandations: List[Dict], context: Dict) -> Dict:
        """Calcul budgets et ressources requis"""
        
        cout_total = sum(reco["budget_estime"] for reco in recommandations)
        duree_formations = sum(reco["duree_formation"] for reco in recommandations)
        
        # Coûts indirects (temps personnel, logistique)
        cout_indirect = cout_total * 0.3  # 30% de coûts indirects
        cout_total_avec_indirect = cout_total + cout_indirect
        
        # Estimation économies (réduction incidents)
        cout_incident_moyen = 75000  # Basé données CNESST
        reduction_risque_estimee = min(80, len(recommandations) * 15)  # Max 80%
        economies_estimees = cout_incident_moyen * (reduction_risque_estimee / 100)
        
        # ROI et payback
        roi_estime = ((economies_estimees - cout_total_avec_indirect) / cout_total_avec_indirect * 100) if cout_total_avec_indirect > 0 else 0
        payback_period = (cout_total_avec_indirect / economies_estimees * 12) if economies_estimees > 0 else 999  # mois
        
        return {
            "cout_direct": cout_total,
            "cout_indirect": cout_indirect, 
            "cout_total": cout_total_avec_indirect,
            "duree_formations_totale": duree_formations,
            "economies_estimees": economies_estimees,
            "roi_estime": roi_estime,
            "payback_period": min(payback_period, 60),  # Max 5 ans
            "budget_par_priorite": self._calculate_budget_by_priority(recommandations),
            "ressources_humaines": self._calculate_hr_resources(recommandations),
            "planning_budgetaire": self._create_budget_timeline(recommandations)
        }
    
    def _generate_implementation_timeline(self, plan_action: Dict, context: Dict) -> Dict:
        """Génération timeline d'implémentation détaillée"""
        
        today = datetime.now()
        timeline = {
            "date_debut": today.isoformat(),
            "duree_totale": plan_action["duree_totale_estimee"],
            "phases": []
        }
        
        # Phase 1: Préparation (Semaine 1-2)
        phase_prep = {
            "nom": "Préparation et mobilisation",
            "duree": "2 semaines",
            "date_debut": today,
            "date_fin": today + timedelta(weeks=2),
            "activites": [
                "Constitution équipe projet sécurité",
                "Communication plan à l'organisation",
                "Préparation supports formation",
                "Planification détaillée interventions"
            ],
            "livrables": ["Plan projet détaillé", "Équipe mobilisée", "Supports prêts"],
            "ressources": ["Chef projet SST", "RH", "Direction"]
        }
        timeline["phases"].append(phase_prep)
        
        # Phase 2: Actions critiques (Semaine 3-6)
        actions_critiques = [r for r in plan_action.get("actions_par_priorite", {}).get("CRITIQUE", [])]
        if actions_critiques:
            phase_critique = {
                "nom": "Actions critiques urgentes",
                "duree": "4 semaines",
                "date_debut": today + timedelta(weeks=2),
                "date_fin": today + timedelta(weeks=6),
                "activites": [f"Traiter {a['variable_cible']}" for a in actions_critiques],
                "livrables": ["Zones critiques corrigées", "Conformité >80%"],
                "ressources": ["Superviseurs", "Formateurs", "Équipe terrain"]
            }
            timeline["phases"].append(phase_critique)
        
        # Phase 3: Actions élevées (Semaine 7-14)
        actions_elevees = [r for r in plan_action.get("actions_par_priorite", {}).get("ÉLEVÉE", [])]
        if actions_elevees:
            phase_elevee = {
                "nom": "Renforcement et consolidation",
                "duree": "8 semaines", 
                "date_debut": today + timedelta(weeks=6),
                "date_fin": today + timedelta(weeks=14),
                "activites": [f"Renforcer {a['variable_cible']}" for a in actions_elevees],
                "livrables": ["Culture sécurité renforcée", "Procédures optimisées"],
                "ressources": ["Coaches sécurité", "Référents terrain"]
            }
            timeline["phases"].append(phase_elevee)
        
        # Phase 4: Suivi et amélioration continue (Semaine 15+)
        phase_suivi = {
            "nom": "Suivi et amélioration continue",
            "duree": "Continu",
            "date_debut": today + timedelta(weeks=14),
            "date_fin": None,
            "activites": [
                "Mesure indicateurs de succès",
                "Ajustements selon retours terrain",
                "Reconnaissance réussites",
                "Planification cycles suivants"
            ],
            "livrables": ["Tableau bord mensuel", "Plan amélioration continue"],
            "ressources": ["Équipe SST", "Data analyst"]
        }
        timeline["phases"].append(phase_suivi)
        
        return timeline
    
    def _define_success_metrics(self, zones_aveugles: List[Dict], recommandations: List[Dict]) -> Dict:
        """Définition métriques de succès et KPIs"""
        
        metrics = {
            "indicateurs_principaux": [],
            "objectifs_court_terme": {},  # 1-3 mois
            "objectifs_moyen_terme": {},  # 3-12 mois  
            "objectifs_long_terme": {},   # 12+ mois
            "frequence_mesure": "Mensuel",
            "responsable_suivi": "Responsable SST + Direction"
        }
        
        # Indicateurs par zone aveugle
        for zone in zones_aveugles:
            variable = zone["variable"]
            ecart_initial = zone["pourcentage_ecart"]
            
            # Objectifs de réduction d'écart
            objectif_court = max(5, ecart_initial * 0.4)      # Réduire de 60%
            objectif_moyen = max(3, ecart_initial * 0.2)      # Réduire de 80%
            objectif_long = max(1, ecart_initial * 0.1)       # Réduire de 90%
            
            indicateur = {
                "variable": variable,
                "valeur_initiale": ecart_initial,
                "objectif_court_terme": objectif_court,
                "objectif_moyen_terme": objectif_moyen, 
                "objectif_long_terme": objectif_long,
                "unite": "% écart",
                "methode_mesure": "Audit SafetyAgentic mensuel"
            }
            metrics["indicateurs_principaux"].append(indicateur)
        
        # Métriques globales
        metrics["indicateurs_globaux"] = {
            "score_culture_global": {
                "objectif_court": 80,
                "objectif_moyen": 85,
                "objectif_long": 90,
                "unite": "/100"
            },
            "taux_incidents": {
                "objectif_court": -30,  # Réduction 30%
                "objectif_moyen": -50,  # Réduction 50%
                "objectif_long": -70,   # Réduction 70%
                "unite": "% variation"
            },
            "conformite_epi": {
                "objectif_court": 85,
                "objectif_moyen": 90,
                "objectif_long": 95,
                "unite": "% conformité"
            }
        }
        
        return metrics
    
    # Méthodes utilitaires
    def _estimate_personnel_count(self, variable: str, taille_entreprise: str) -> int:
        """Estimation nombre personnes impliquées"""
        base_counts = {
            "PME": {"usage_epi": 15, "supervision_directe": 5, "formation_securite": 12},
            "MOYENNE": {"usage_epi": 45, "supervision_directe": 12, "formation_securite": 35},
            "GRANDE": {"usage_epi": 120, "supervision_directe": 25, "formation_securite": 80}
        }
        return base_counts.get(taille_entreprise, {}).get(variable, 20)
    
    def _generate_implementation_method(self, variable: str, priorite: str, secteur: str) -> str:
        """Génération méthode d'implémentation spécifique"""
        methods = {
            "usage_epi": f"Formation pratique + contrôles quotidiens superviseurs + système sanctions progressives",
            "supervision_directe": f"Formation leadership + rondes obligatoires + reporting hebdomadaire",
            "formation_securite": f"Mise à jour contenus secteur {secteur} + certification + évaluation pratique"
        }
        return methods.get(variable, "Formation + procédures + suivi mensuel")
    
    def _identify_implementation_risks(self, variable: str, secteur: str) -> List[str]:
        """Identification risques d'implémentation"""
        return [
            "Résistance au changement équipes terrain",
            "Manque de temps pour formations durant production",
            "Coûts imprévus équipements/ressources",
            "Turnover personnel formé"
        ]
    
    def _identify_success_factors(self, variable: str, priorite: str) -> List[str]:
        """Identification facteurs clés de succès"""
        return [
            "Engagement visible direction et management",
            "Communication claire bénéfices sécurité",
            "Formation adaptée aux réalités terrain",
            "Système reconnaissance/récompenses",
            "Suivi régulier et ajustements"
        ]
    
    def _optimize_action_sequence(self, recommandations: List[Dict]) -> List[str]:
        """Optimisation séquence d'actions"""
        # Trier par priorité puis par dépendances
        sequence = []
        priorites = ["CRITIQUE", "URGENTE", "ÉLEVÉE", "MOYENNE"]
        
        for priorite in priorites:
            reco_priorite = [r for r in recommandations if r["priorite"] == priorite]
            sequence.extend([r["id"] for r in reco_priorite])
        
        return sequence
    
    def _define_key_milestones(self, recommandations: List[Dict], context: Dict) -> List[Dict]:
        """Définition jalons clés"""
        return [
            {"nom": "Formations critiques terminées", "semaine": 4},
            {"nom": "Procédures mises à jour", "semaine": 8}, 
            {"nom": "Première évaluation SafetyAgentic", "semaine": 12},
            {"nom": "Objectifs court terme atteints", "semaine": 16}
        ]
    
    def _identify_coordination_needs(self, recommandations: List[Dict]) -> List[str]:
        """Identification besoins de coordination"""
        return [
            "Coordination formation/production pour minimiser impact",
            "Synchronisation changements procédures entre équipes", 
            "Alignement budgets RH/SST/Production",
            "Communication cohérente vers toutes parties prenantes"
        ]
    
    def _identify_critical_resources(self, recommandations: List[Dict]) -> List[str]:
        """Identification ressources critiques"""
        return [
            "Formateurs SST qualifiés secteur",
            "Temps superviseurs pour formation",
            "Budget équipements EPI/sécurité",
            "Support IT pour digitalisation"
        ]
    
    def _calculate_budget_by_priority(self, recommandations: List[Dict]) -> Dict:
        """Calcul budget par priorité"""
        budget_priorite = {}
        for reco in recommandations:
            priorite = reco["priorite"]
            budget = reco["budget_estime"]
            if priorite not in budget_priorite:
                budget_priorite[priorite] = 0
            budget_priorite[priorite] += budget
        return budget_priorite
    
    def _calculate_hr_resources(self, recommandations: List[Dict]) -> Dict:
        """Calcul ressources humaines requises"""
        total_personnel = sum(reco["personnels_impliques"] for reco in recommandations)
        total_heures_formation = sum(
            reco["duree_formation"] * reco["personnels_impliques"] 
            for reco in recommandations
        )
        
        return {
            "personnel_total_implique": total_personnel,
            "heures_formation_totales": total_heures_formation,
            "jours_formation_equivalents": total_heures_formation / 8,
            "formateurs_requis": max(1, total_heures_formation // 40),  # 40h par formateur
            "coordinateurs_requis": max(1, len(recommandations) // 3)   # 1 coord pour 3 actions
        }
    
    def _create_budget_timeline(self, recommandations: List[Dict]) -> Dict:
        """Création planning budgétaire"""
        today = datetime.now()
        planning = {}
        
        # Répartition par trimestre
        for i, trimestre in enumerate(["T1", "T2", "T3", "T4"]):
            budget_trimestre = 0
            actions_trimestre = []
            
            for reco in recommandations:
                # Simplification: répartir selon priorité
                if reco["priorite"] in ["CRITIQUE", "URGENTE"] and i == 0:
                    budget_trimestre += reco["budget_estime"]
                    actions_trimestre.append(reco["id"])
                elif reco["priorite"] == "ÉLEVÉE" and i == 1:
                    budget_trimestre += reco["budget_estime"]
                    actions_trimestre.append(reco["id"])
                elif reco["priorite"] == "MOYENNE" and i in [2, 3]:
                    budget_trimestre += reco["budget_estime"] / 2
                    actions_trimestre.append(reco["id"])
            
            planning[trimestre] = {
                "budget": budget_trimestre,
                "actions": actions_trimestre,
                "periode": f"{today + timedelta(weeks=i*13):%B %Y}"
            }
        
        return planning
    
    def _calculate_total_duration(self, recommandations: List[Dict]) -> str:
        """Calcul durée totale estimée"""
        durees_priorite = {
            "CRITIQUE": 4,   # semaines
            "URGENTE": 6,
            "ÉLEVÉE": 12,
            "MOYENNE": 20
        }
        
        duree_max = 0
        for reco in recommandations:
            duree_priorite = durees_priorite.get(reco["priorite"], 12)
            duree_max = max(duree_max, duree_priorite)
        
        return f"{duree_max} semaines"
    
    def _calculate_confidence_score(self, zones_aveugles: List[Dict], context: Dict) -> float:
        """Calcul score confiance recommandations"""
        if not zones_aveugles:
            return 0.5
        
        # Facteurs de confiance
        nombre_zones = len(zones_aveugles)
        facteur_nombre = min(1.0, nombre_zones / 5)  # Optimal à 5 zones
        
        # Qualité des données contextuelles
        facteur_contexte = 0.8 if context and context.get("secteur") else 0.6
        
        # Cohérence des écarts
        ecarts = [z.get("pourcentage_ecart", 0) for z in zones_aveugles]
        coherence = 1.0 - (np.std(ecarts) / 100) if ecarts else 0.5
        
        confidence = (facteur_nombre * 0.3) + (facteur_contexte * 0.4) + (coherence * 0.3)
        return max(0.3, min(0.95, confidence))


# Test fonctionnel R1
async def test_r1_generateur_recommandations():
    """Test fonctionnel Agent R1 avec zones aveugles AN1"""
    
    print("🧪 TEST AGENT R1 - GÉNÉRATEUR RECOMMANDATIONS")
    print("=" * 50)
    
    # Données simulées AN1 (zones aveugles détectées)
    data_an1_with_blind_spots = {
        "ecarts_analysis": {
            "zones_aveugles": [
                {
                    "variable": "supervision_directe",
                    "pourcentage_ecart": 55.6,
                    "niveau_critique": "CRITIQUE",
                    "type_ecart": "surestimation",
                    "score_autoeval": 7.5,
                    "score_terrain": 3.5,
                    "impact_potentiel": "CRITIQUE - Risque incident majeur"
                },
                {
                    "variable": "usage_epi",
                    "pourcentage_ecart": 43.5,
                    "niveau_critique": "ÉLEVÉE",
                    "type_ecart": "surestimation", 
                    "score_autoeval": 8.5,
                    "score_terrain": 4.8,
                    "impact_potentiel": "ÉLEVÉ - Intervention urgente requise"
                },
                {
                    "variable": "formation_securite",
                    "pourcentage_ecart": 28.3,
                    "niveau_critique": "ÉLEVÉE",
                    "type_ecart": "surestimation",
                    "score_autoeval": 7.2,
                    "score_terrain": 5.8,
                    "impact_potentiel": "MODÉRÉ - Surveillance renforcée"
                }
            ],
            "nombre_ecarts_critiques": 3
        },
        "summary": {
            "ecart_moyen": 42.5,
            "variables_critiques": 3,
            "priorite_intervention": "CRITIQUE"
        }
    }
    
    # Contexte réaliste construction
    context_construction = {
        "secteur": "CONSTRUCTION",
        "type_incident": "CHUTE_HAUTEUR",
        "taille_entreprise": "MOYENNE",
        "nombre_employes": 85,
        "budget_sst_annuel": 125000,
        "certification_existante": "ISO45001"
    }
    
    # Initialiser et tester R1
    agent_r1 = R1GenerateurRecommandations()
    result = await agent_r1.process(data_an1_with_blind_spots, context_construction)
    
    # Affichage résultats
    print("📊 RÉSULTATS AGENT R1:")
    print("=" * 25)
    print(f"✅ Score confiance: {result['agent_info']['confidence_score']:.3f}")
    print(f"📊 Zones traitées: {result['recommandations_analysis']['zones_traitees']}")
    print(f"💡 Recommandations générées: {result['recommandations_analysis']['recommandations_generees']}")
    print(f"🎯 Priorité globale: {result['recommandations_analysis']['priorite_globale']}")
    
    # Plan d'action
    plan_action = result['plan_action']
    print(f"\n📋 PLAN D'ACTION:")
    print(f"  • Durée totale: {plan_action['duree_totale_estimee']}")
    print(f"  • Actions par priorité: {len(plan_action['actions_par_priorite'])}")
    print(f"  • Séquence optimisée: {len(plan_action['sequence_optimale'])} étapes")
    
    # Budget analysis
    budget = result['budget_analysis']
    print(f"\n💰 ANALYSE BUDGÉTAIRE:")
    print(f"  • Coût direct: {budget['cout_direct']:,.0f}$")
    print(f"  • Coût total: {budget['cout_total']:,.0f}$")
    print(f"  • Économies estimées: {budget['economies_estimees']:,.0f}$")
    print(f"  • ROI estimé: {budget['roi_estime']:.1f}%")
    print(f"  • Payback: {budget['payback_period']:.1f} mois")
    
    # Recommandations détaillées (top 2)
    print(f"\n💡 TOP RECOMMANDATIONS:")
    for i, reco in enumerate(result['recommandations_detaillees'][:2], 1):
        print(f"  {i}. {reco['variable_cible']} (Priorité: {reco['priorite']})")
        print(f"     📊 Écart à corriger: {reco['ecart_a_corriger']:.1f}%")
        print(f"     ⏱️ Timeline: {reco['timeline']}")
        print(f"     💰 Budget: {reco['budget_estime']:,.0f}$")
        print(f"     🎯 Formations: {len(reco['formations'])} modules")
        
        # Actions principales
        if reco['formations']:
            print(f"     📚 Formation clé: {reco['formations'][0]}")
        if reco['procedures']:
            print(f"     📋 Procédure clé: {reco['procedures'][0]}")
    
    # Timeline d'implémentation
    timeline = result['implementation_timeline']
    print(f"\n📅 TIMELINE IMPLÉMENTATION:")
    for phase in timeline['phases'][:3]:  # Top 3 phases
        print(f"  • {phase['nom']}: {phase['duree']}")
        print(f"    └── {len(phase['activites'])} activités prévues")
    
    # Métriques de succès
    metrics = result['success_metrics']
    print(f"\n📈 MÉTRIQUES DE SUCCÈS:")
    for indicateur in metrics['indicateurs_principaux'][:2]:
        print(f"  • {indicateur['variable']}:")
        print(f"    Initial: {indicateur['valeur_initiale']:.1f}% → Objectif: {indicateur['objectif_court_terme']:.1f}%")
    
    # Impact business
    business_impact = result['business_impact']
    print(f"\n💼 IMPACT BUSINESS:")
    print(f"  • ROI: {business_impact['roi_estime']:.1f}%")
    print(f"  • Économies: {business_impact['economies_estimees']:,.0f}$")
    print(f"  • Investissement: {business_impact['cout_total']:,.0f}$")
    print(f"  • Retour sur investissement: {business_impact['payback_period']:.1f} mois")
    
    print(f"\n✅ Test Agent R1 terminé avec succès!")
    print(f"⏱️ Performance: {result['agent_info']['performance_time']:.3f}s")
    return result

# Exécution test si script appelé directement
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_r1_generateur_recommandations())