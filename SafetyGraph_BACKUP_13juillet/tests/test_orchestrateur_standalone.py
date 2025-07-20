# Test Orchestrateur SafetyAgentic - Version Standalone Complète
# ==============================================================

import asyncio
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Configuration logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SafetyAgentic.Orchestrateur")

class SafetyAgenticOrchestrator:
    """
    Orchestrateur principal SafetyAgentic - Version complète standalone
    
    Coordonne les agents A1, A2, AN1 pour une analyse complète 
    de la culture sécurité avec détection des zones aveugles.
    """
    
    def __init__(self):
        """Initialisation orchestrateur"""
        self.orchestrator_id = "ORCHESTRATEUR_SAFETYAGENTIC"
        self.version = "1.0.0"
        self.workflow_steps = ["A1", "A2", "AN1", "SYNTHESE"]
        
        logger.info(f"🤖 {self.orchestrator_id} v{self.version} initialisé")
        print(f"🤖 {self.orchestrator_id} v{self.version} initialisé")
    
    async def analyze_safety_culture(self, incident_data: Dict, context: Dict = None) -> Dict:
        """Analyse complète culture sécurité pour un incident donné"""
        start_time = datetime.now()
        analysis_id = f"SA_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"🔄 Démarrage analyse SafetyAgentic - ID: {analysis_id}")
        print(f"\n🔄 ANALYSE SAFETYAGENTIC - ID: {analysis_id}")
        print("=" * 60)
        
        try:
            # Préparation contexte analyse
            analysis_context = self._prepare_analysis_context(incident_data, context)
            print(f"📋 Contexte: {analysis_context['secteur']} - {analysis_context['type_incident']}")
            
            # Workflow séquentiel A1 → A2 → AN1
            workflow_results = {}
            
            # ÉTAPE 1: Agent A1 - Autoévaluations
            print(f"\n🎯 ÉTAPE 1/4 - AGENT A1 (AUTOÉVALUATIONS)")
            print("-" * 45)
            result_a1 = await self._execute_agent_a1(incident_data, analysis_context)
            workflow_results["A1"] = result_a1
            self._display_a1_summary(result_a1)
            
            # ÉTAPE 2: Agent A2 - Observations terrain
            print(f"\n🔍 ÉTAPE 2/4 - AGENT A2 (OBSERVATIONS TERRAIN)")  
            print("-" * 50)
            result_a2 = await self._execute_agent_a2(incident_data, analysis_context, result_a1)
            workflow_results["A2"] = result_a2
            self._display_a2_summary(result_a2)
            
            # ÉTAPE 3: Agent AN1 - Analyse écarts
            print(f"\n🔬 ÉTAPE 3/4 - AGENT AN1 (ANALYSE ÉCARTS)")
            print("-" * 45)
            result_an1 = await self._execute_agent_an1(result_a1, result_a2, analysis_context)
            workflow_results["AN1"] = result_an1
            self._display_an1_summary(result_an1)
            
            # ÉTAPE 4: Synthèse finale
            print(f"\n📊 ÉTAPE 4/4 - SYNTHÈSE FINALE")
            print("-" * 35)
            final_synthesis = await self._generate_final_synthesis(
                workflow_results, incident_data, analysis_context
            )
            
            # Calcul métriques globales
            global_metrics = self._calculate_global_metrics(workflow_results)
            
            # Construction rapport final
            performance_time = (datetime.now() - start_time).total_seconds()
            
            final_report = {
                "analysis_info": {
                    "analysis_id": analysis_id,
                    "orchestrator_version": self.version,
                    "timestamp": datetime.now().isoformat(),
                    "performance_time": performance_time,
                    "incident_context": analysis_context
                },
                "workflow_results": workflow_results,
                "global_metrics": global_metrics,
                "final_synthesis": final_synthesis,
                "quality_assessment": self._assess_analysis_quality(workflow_results, global_metrics),
                "executive_summary": self._generate_executive_summary(final_synthesis, global_metrics)
            }
            
            # Affichage rapport final
            self._display_final_report(final_report)
            
            logger.info(f"✅ Analyse SafetyAgentic terminée - {performance_time:.2f}s")
            return final_report
            
        except Exception as e:
            logger.error(f"❌ Erreur orchestrateur: {str(e)}")
            return {
                "error": str(e),
                "analysis_id": analysis_id,
                "orchestrator_id": self.orchestrator_id
            }
    
    def _prepare_analysis_context(self, incident_data: Dict, context: Dict) -> Dict:
        """Préparation contexte d'analyse"""
        return {
            "secteur": incident_data.get("SECTEUR_SCIAN", "CONSTRUCTION"),
            "type_incident": incident_data.get("GENRE", "CHUTE_HAUTEUR"),
            "nature_lesion": incident_data.get("NATURE_LESION", "TRAUMA_MUSCLES"),
            "siege_lesion": incident_data.get("SIEGE_LESION", "MEMBRES"),
            "agent_causal": incident_data.get("AGENT_CAUSAL_LESION", "ECHAFAUDAGE"),
            "age_groupe": incident_data.get("GROUPE_AGE", "30-39"),
            "sexe": incident_data.get("SEXE_PERS_PHYS", "M"),
            "organisation_context": context or {}
        }
    
    async def _execute_agent_a1(self, incident_data: Dict, context: Dict) -> Dict:
        """Simulation Agent A1 - Autoévaluations"""
        print("🤖 Initialisation Agent A1...")
        await asyncio.sleep(0.2)  # Simulation traitement
        
        result = {
            "agent_id": "A1",
            "confidence_score": 0.82,
            "variables_culture_sst": {
                "usage_epi": {"score": 8.2, "source": "questionnaire", "confiance": 0.9},
                "respect_procedures": {"score": 7.5, "source": "questionnaire", "confiance": 0.8},
                "formation_securite": {"score": 7.8, "source": "questionnaire", "confiance": 0.8},
                "supervision_directe": {"score": 7.2, "source": "questionnaire", "confiance": 0.7},
                "communication_risques": {"score": 6.9, "source": "questionnaire", "confiance": 0.8},
                "leadership_sst": {"score": 7.1, "source": "questionnaire", "confiance": 0.7}
            },
            "scores_autoeval": {
                "score_global": 75,
                "fiabilite": 0.8,
                "biais_detectes": ["surconfiance", "desirabilite_sociale"]
            },
            "variables_prioritaires": ["usage_epi", "supervision_directe"],
            "recommendations": [
                {
                    "priorite": "ÉLEVÉE",
                    "action": "Renforcer formation EPI secteur construction",
                    "timeline": "4-6 semaines",
                    "variable_cible": "usage_epi"
                },
                {
                    "priorite": "MOYENNE",
                    "action": "Améliorer communication risques chantier",
                    "timeline": "2-3 mois",
                    "variable_cible": "communication_risques"
                }
            ]
        }
        
        print(f"✅ Agent A1 terminé - Confiance: {result['confidence_score']:.2f}")
        return result
    
    async def _execute_agent_a2(self, incident_data: Dict, context: Dict, result_a1: Dict) -> Dict:
        """Simulation Agent A2 - Observations terrain"""
        print("🤖 Initialisation Agent A2...")
        await asyncio.sleep(0.2)
        
        result = {
            "agent_id": "A2", 
            "confidence_score": 0.78,
            "variables_culture_terrain": {
                "usage_epi": {"score": 4.5, "source": "observation_epi", "observations": 15},
                "respect_procedures": {"score": 5.8, "source": "procedure_compliance", "observations": 12},
                "formation_securite": {"score": 7.2, "source": "behavioral_analysis", "observations": 8},
                "supervision_directe": {"score": 3.2, "source": "hazard_detection", "observations": 10},
                "communication_risques": {"score": 5.5, "source": "behavioral_analysis", "observations": 6},
                "leadership_sst": {"score": 4.1, "source": "hazard_detection", "observations": 4}
            },
            "observations": {
                "score_comportement": 52,
                "dangers_detectes": 3,
                "epi_analyses": 15,
                "epi_obligatoires": 12,
                "conformite_procedures": 48.0,
                "incidents_potentiels": 2
            },
            "contexte_observation": {
                "duree_observation": "4 heures",
                "nombre_travailleurs": 6,
                "type_chantier": "construction_residentielle",
                "conditions_meteo": "venteux"
            },
            "recommendations": [
                {
                    "priorite": "URGENTE",
                    "action": "Contrôle port EPI immédiat sur chantier",
                    "timeline": "1-2 semaines",
                    "variable_cible": "usage_epi"
                },
                {
                    "priorite": "ÉLEVÉE", 
                    "action": "Renforcer supervision terrain échafaudages",
                    "timeline": "2-4 semaines",
                    "variable_cible": "supervision_directe"
                },
                {
                    "priorite": "ÉLEVÉE",
                    "action": "Formation procédures travail hauteur",
                    "timeline": "3-4 semaines",
                    "variable_cible": "respect_procedures"
                }
            ]
        }
        
        print(f"✅ Agent A2 terminé - Confiance: {result['confidence_score']:.2f}")
        return result
    
    async def _execute_agent_an1(self, result_a1: Dict, result_a2: Dict, context: Dict) -> Dict:
        """Simulation Agent AN1 - Analyse écarts"""
        print("🤖 Initialisation Agent AN1...")
        await asyncio.sleep(0.2)
        
        # Calcul écarts réalistes
        vars_a1 = result_a1["variables_culture_sst"]
        vars_a2 = result_a2["variables_culture_terrain"]
        
        ecarts_variables = {}
        zones_aveugles = []
        
        for var in vars_a1.keys():
            if var in vars_a2:
                score_a1 = vars_a1[var]["score"]
                score_a2 = vars_a2[var]["score"]
                ecart_pct = abs(score_a1 - score_a2) / score_a1 * 100 if score_a1 > 0 else 0
                
                if ecart_pct > 50:
                    niveau = "critique"
                elif ecart_pct > 25:
                    niveau = "eleve"
                elif ecart_pct > 10:
                    niveau = "modere"
                else:
                    niveau = "faible"
                
                direction = "surestimation" if score_a1 > score_a2 else "sous_estimation"
                
                ecarts_variables[var] = {
                    "score_autoeval": score_a1,
                    "score_terrain": score_a2,
                    "ecart_absolu": abs(score_a1 - score_a2),
                    "pourcentage": ecart_pct,
                    "niveau": niveau,
                    "direction": direction
                }
                
                # Zone aveugle si écart élevé ou critique
                if niveau in ["eleve", "critique"]:
                    impact = "CRITIQUE - Risque incident majeur" if niveau == "critique" else "ÉLEVÉ - Intervention urgente requise"
                    zones_aveugles.append({
                        "variable": var,
                        "pourcentage_ecart": ecart_pct,
                        "niveau_critique": niveau,
                        "type_ecart": direction,
                        "impact_potentiel": impact,
                        "explication": f"{direction.title()} de {ecart_pct:.1f}% sur {var}"
                    })
        
        # Tri zones aveugles par écart décroissant
        zones_aveugles.sort(key=lambda x: x["pourcentage_ecart"], reverse=True)
        
        result = {
            "agent_id": "AN1",
            "confidence_score": 0.85,
            "ecarts_analysis": {
                "ecarts_variables": ecarts_variables,
                "zones_aveugles": zones_aveugles,
                "nombre_ecarts_critiques": len([e for e in ecarts_variables.values() if e["niveau"] == "critique"]),
                "realisme_scores": {
                    "realisme_global": 68,
                    "fiabilite_autoeval": 72,
                    "niveau_autocritique": "moyen"
                }
            },
            "hse_models_analysis": {
                "hfacs_l1": {
                    "model_name": "HFACS L1 - Échecs organisationnels",
                    "score_applicabilite": 85,
                    "analysis": {"score_defaillance": 35.2, "interpretation": "Défaillances organisationnelles modérées"}
                },
                "hfacs_l2": {
                    "model_name": "HFACS L2 - Supervision inadéquate",
                    "score_applicabilite": 92,
                    "analysis": {"score_defaillance": 48.7, "interpretation": "Supervision inadéquate critique"}
                },
                "swiss_cheese": {
                    "model_name": "Swiss Cheese - Défaillances barrières",
                    "score_applicabilite": 88,
                    "analysis": {"barrieres_critiques": ["supervision", "individuelles"], "risque_global": 45.3}
                }
            },
            "recommendations": [
                {
                    "priorite": "URGENTE",
                    "action": "Corriger défaillance supervision critique",
                    "variable_cible": "supervision_directe",
                    "methode": "Formation superviseurs + audits terrain quotidiens",
                    "timeline": "2-4 semaines",
                    "ressources_requises": "Formation complète équipe supervision + consultant externe"
                },
                {
                    "priorite": "ÉLEVÉE",
                    "action": "Programme correction écart EPI",
                    "variable_cible": "usage_epi",
                    "methode": "Observations terrain ciblées + formations pratiques",
                    "timeline": "3-6 semaines",
                    "ressources_requises": "Formation équipe + contrôles renforcés + nouveaux EPI"
                },
                {
                    "priorite": "ÉLEVÉE",
                    "action": "Amélioration leadership SST",
                    "variable_cible": "leadership_sst",
                    "methode": "Formation management + engagement visible",
                    "timeline": "1-2 mois",
                    "ressources_requises": "Formation management + communication renforcée"
                }
            ],
            "summary": {
                "ecart_moyen": np.mean([e["pourcentage"] for e in ecarts_variables.values()]),
                "variables_critiques": len(zones_aveugles),
                "actions_recommandees": 3,
                "priorite_intervention": "ÉLEVÉE"
            }
        }
        
        print(f"✅ Agent AN1 terminé - Confiance: {result['confidence_score']:.2f}")
        return result
    
    async def _generate_final_synthesis(self, workflow_results: Dict, incident_data: Dict, context: Dict) -> Dict:
        """Génération synthèse finale intelligente"""
        
        a1_data = workflow_results["A1"]
        a2_data = workflow_results["A2"] 
        an1_data = workflow_results["AN1"]
        
        # Extraction insights clés
        zones_aveugles = an1_data["ecarts_analysis"]["zones_aveugles"]
        
        # Consolidation recommandations
        all_recommendations = (a1_data.get("recommendations", []) + 
                             a2_data.get("recommendations", []) + 
                             an1_data.get("recommendations", []))
        
        prioritized_actions = self._prioritize_recommendations(all_recommendations, zones_aveugles)
        
        # Identification causes racines
        root_causes = self._identify_root_causes(zones_aveugles, context)
        
        # Calcul impact business
        business_impact = self._calculate_business_impact(zones_aveugles, context)
        
        return {
            "zones_aveugles_critiques": zones_aveugles[:3],
            "causes_racines": root_causes,
            "actions_prioritaires": prioritized_actions[:6],
            "impact_business": business_impact,
            "timeline_intervention": self._generate_intervention_timeline(prioritized_actions),
            "success_metrics": self._define_success_metrics(zones_aveugles),
            "risk_assessment": self._assess_residual_risk(zones_aveugles)
        }
    
    def _prioritize_recommendations(self, recommendations: List, zones_aveugles: List) -> List:
        """Priorisation intelligente des recommandations"""
        priority_scores = {}
        
        for rec in recommendations:
            score = 0
            priorite = rec.get("priorite", "MOYENNE")
            
            # Score base selon priorité
            if priorite == "URGENTE":
                score += 100
            elif priorite == "ÉLEVÉE":
                score += 75
            elif priorite == "MOYENNE":
                score += 50
            else:
                score += 25
            
            # Bonus si liée à zone aveugle critique
            variable_cible = rec.get("variable_cible", "")
            for zone in zones_aveugles:
                if zone.get("variable") == variable_cible and zone.get("niveau_critique") == "critique":
                    score += 50
                    break
            
            priority_scores[rec.get("action", "Action")] = score
        
        return sorted(recommendations, 
                     key=lambda x: priority_scores.get(x.get("action", ""), 0), 
                     reverse=True)
    
    def _identify_root_causes(self, zones_aveugles: List, context: Dict) -> List[Dict]:
        """Identification causes racines des zones aveugles"""
        root_causes = []
        
        # Analyse patterns zones aveugles
        if len(zones_aveugles) >= 2:
            # Pattern supervision défaillante
            supervision_issues = [z for z in zones_aveugles if "supervision" in z.get("variable", "").lower()]
            if supervision_issues:
                root_causes.append({
                    "cause": "Défaillance système supervision",
                    "evidence": f"{len(supervision_issues)} zone(s) aveugle(s) supervision détectée(s)",
                    "impact": "Perte de contrôle opérationnel sur chantier",
                    "level": "organisationnel"
                })
            
            # Pattern formation/compétences
            formation_issues = [z for z in zones_aveugles if any(kw in z.get("variable", "").lower() 
                               for kw in ["formation", "epi", "procedure"])]
            if len(formation_issues) >= 2:
                root_causes.append({
                    "cause": "Lacunes formation et application procédures",
                    "evidence": f"{len(formation_issues)} zone(s) aveugle(s) formation/EPI/procédures",
                    "impact": "Exposition risques évitables - Non-respect standards",
                    "level": "individuel_collectif"
                })
        
        # Cause sectorielle construction
        org_context = context.get("organisation_context", {})
        if org_context.get("secteur_risque") == "Élevé - Construction résidentielle":
            root_causes.append({
                "cause": "Pression temporelle et économique projets construction",
                "evidence": "Secteur construction avec délais serrés et marges faibles",
                "impact": "Compromis sécurité vs productivité et rentabilité",
                "level": "sectoriel_economique"
            })
        
        # Budget SST insuffisant
        if org_context.get("budget_sst_annuel", 0) < 30000:
            root_causes.append({
                "cause": "Sous-investissement ressources sécurité",
                "evidence": f"Budget SST {org_context.get('budget_sst_annuel', 0):,}$ insuffisant pour PME",
                "impact": "Manque moyens formation, équipements, supervision",
                "level": "organisationnel_financier"
            })
        
        return root_causes
    
    def _calculate_business_impact(self, zones_aveugles: List, context: Dict) -> Dict:
        """Calcul impact business des zones aveugles"""
        
        # Coûts estimés par zone aveugle
        cost_per_critical_zone = 75000  # Construction = risque élevé
        cost_per_elevated_zone = 35000
        
        nb_zones_critiques = len([z for z in zones_aveugles if z.get("niveau_critique") == "critique"])
        nb_zones_elevees = len([z for z in zones_aveugles if z.get("niveau_critique") == "eleve"])
        
        estimated_cost = (nb_zones_critiques * cost_per_critical_zone + 
                         nb_zones_elevees * cost_per_elevated_zone)
        
        # Probabilité incident construction avec zones aveugles
        base_probability = 0.12  # Construction base
        zone_multiplier = 1 + (nb_zones_critiques * 0.3) + (nb_zones_elevees * 0.15)
        incident_probability = min(0.4, base_probability * zone_multiplier)
        
        # Coût incident construction (chute hauteur)
        average_incident_cost = 280000  # Construction = coûts élevés
        
        return {
            "cout_zones_aveugles": estimated_cost,
            "zones_critiques": nb_zones_critiques,
            "zones_elevees": nb_zones_elevees,
            "probabilite_incident": incident_probability,
            "cout_incident_potentiel": average_incident_cost,
            "esperance_perte": int(incident_probability * average_incident_cost),
            "roi_intervention": {
                "cout_intervention": estimated_cost // 2,  # 50% coût correction
                "economies_potentielles": int(incident_probability * average_incident_cost),
                "roi_ratio": int((incident_probability * average_incident_cost) / (estimated_cost // 2)) if estimated_cost > 0 else 0
            }
        }
    
    def _generate_intervention_timeline(self, actions: List) -> Dict:
        """Génération timeline d'intervention"""
        timeline = {
            "immediate": [],      # 0-2 semaines
            "short_term": [],     # 2-8 semaines  
            "medium_term": [],    # 2-6 mois
            "long_term": []       # 6+ mois
        }
        
        for action in actions:
            timeline_info = action.get("timeline", "1-2 mois")
            priorite = action.get("priorite", "MOYENNE")
            action_text = action.get("action", "Action")
            
            if "semaine" in timeline_info and priorite == "URGENTE":
                timeline["immediate"].append(action_text)
            elif "semaine" in timeline_info:
                timeline["short_term"].append(action_text)
            elif "mois" in timeline_info and any(x in timeline_info for x in ["1", "2", "3"]):
                timeline["medium_term"].append(action_text)
            else:
                timeline["long_term"].append(action_text)
        
        return timeline
    
    def _define_success_metrics(self, zones_aveugles: List) -> List[Dict]:
        """Définition métriques de succès"""
        metrics = []
        
        for zone in zones_aveugles[:3]:  # Top 3 zones
            variable = zone.get("variable", "")
            ecart_current = zone.get("pourcentage_ecart", 0)
            
            # Objectif: réduire écart de 60% minimum pour construction
            target_reduction = max(60, ecart_current * 0.6)
            target_ecart = max(5, ecart_current - target_reduction)
            
            metrics.append({
                "variable": variable,
                "baseline_ecart": ecart_current,
                "target_ecart": target_ecart,
                "reduction_objective": f"{target_reduction:.0f}%",
                "measurement_method": f"Observations terrain hebdomadaires + autoévaluation {variable}",
                "frequency": "Hebdomadaire (4 premières semaines) puis mensuelle",
                "success_threshold": f"Écart < {max(10, target_reduction//2)}% maintenu 3 mois",
                "kpi_specifique": self._get_variable_kpi(variable)
            })
        
        return metrics
    
    def _get_variable_kpi(self, variable: str) -> str:
        """KPI spécifique par variable"""
        kpi_mapping = {
            "usage_epi": "% conformité port EPI observé (objectif >90%)",
            "supervision_directe": "Nb rondes supervision/jour (objectif ≥3)",
            "respect_procedures": "% procédures suivies audits (objectif >85%)",
            "formation_securite": "% employés formés 12 mois (objectif 100%)",
            "leadership_sst": "Score engagement visible management (objectif >8/10)"
        }
        return kpi_mapping.get(variable, f"Amélioration score {variable} (objectif +20%)")
    
    def _assess_residual_risk(self, zones_aveugles: List) -> Dict:
        """Évaluation risque résiduel"""
        nb_critiques = len([z for z in zones_aveugles if z.get("niveau_critique") == "critique"])
        nb_eleves = len([z for z in zones_aveugles if z.get("niveau_critique") == "eleve"])
        
        if nb_critiques >= 2:
            risk_level = "ÉLEVÉ"
            risk_description = "Zones aveugles multiples critiques - Risque incident majeur"
            action_requise = "IMMÉDIATE"
        elif nb_critiques >= 1:
            risk_level = "MODÉRÉ-ÉLEVÉ"
            risk_description = "Zone aveugle critique identifiée - Surveillance intensive"
            action_requise = "RAPIDE"
        elif nb_eleves >= 3:
            risk_level = "MODÉRÉ"
            risk_description = "Multiples zones aveugles élevées - Amélioration systémique"
            action_requise = "PLANIFIÉE"
        else:
            risk_level = "FAIBLE-MODÉRÉ"
            risk_description = "Zones aveugles limitées - Surveillance standard"
            action_requise = "CONTINUE"
        
        return {
            "niveau_risque": risk_level,
            "description": risk_description,
            "zones_critiques": nb_critiques,
            "zones_elevees": nb_eleves,
            "action_requise": action_requise,
            "probabilite_incident": "Élevée" if nb_critiques >= 1 else "Modérée" if nb_eleves >= 2 else "Faible",
            "impact_potentiel": "Majeur" if nb_critiques >= 1 else "Modéré"
        }
    
    def _calculate_global_metrics(self, workflow_results: Dict) -> Dict:
        """Calcul métriques globales analyse"""
        confidence_scores = []
        for agent, results in workflow_results.items():
            if "confidence_score" in results:
                confidence_scores.append(results["confidence_score"])
        
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        # Métriques AN1 spécifiques
        an1_data = workflow_results.get("AN1", {})
        ecarts_analysis = an1_data.get("ecarts_analysis", {})
        
        return {
            "confidence_globale": avg_confidence,
            "agents_executes": len(workflow_results),
            "variables_analysees": len(ecarts_analysis.get("ecarts_variables", {})),
            "zones_aveugles_detectees": len(ecarts_analysis.get("zones_aveugles", [])),
            "ecart_moyen": an1_data.get("summary", {}).get("ecart_moyen", 0),
            "priorite_intervention": an1_data.get("summary", {}).get("priorite_intervention", "INCONNUE"),
            "qualite_analyse": "ÉLEVÉE" if avg_confidence > 0.75 else "MOYENNE" if avg_confidence > 0.6 else "FAIBLE"
        }
    
    def _assess_analysis_quality(self, workflow_results: Dict, global_metrics: Dict) -> Dict:
        """Évaluation qualité de l'analyse"""
        quality_score = 0
        issues = []
        
        # Critère 1: Confiance globale
        confidence = global_metrics.get("confidence_globale", 0)
        if confidence >= 0.75:
            quality_score += 30
        elif confidence >= 0.6:
            quality_score += 20
        else:
            issues.append(f"Confiance faible: {confidence:.2f}")
        
        # Critère 2: Nombre variables analysées
        nb_variables = global_metrics.get("variables_analysees", 0)
        if nb_variables >= 5:
            quality_score += 25
        elif nb_variables >= 3:
            quality_score += 15
        else:
            issues.append(f"Variables insuffisantes: {nb_variables}")
        
        # Critère 3: Détection zones aveugles
        nb_zones = global_metrics.get("zones_aveugles_detectees", 0)
        if 1 <= nb_zones <= 5:
            quality_score += 25
        elif nb_zones == 0:
            quality_score += 10  # Peut être normal
            issues.append("Aucune zone aveugle détectée")
        else:
            issues.append(f"Zones aveugles nombreuses: {nb_zones}")
        
        # Critère 4: Cohérence agents
        if len(workflow_results) == 3:  # A1, A2, AN1
            quality_score += 20
        
        return {
            "score_qualite": quality_score,
            "niveau_qualite": ("EXCELLENT" if quality_score >= 90 else 
                              "BON" if quality_score >= 70 else 
                              "ACCEPTABLE" if quality_score >= 50 else "FAIBLE"),
            "issues_detectees": issues,
            "recommandation_qualite": ("Analyse très fiable" if quality_score >= 80 else
                                      "Analyse fiable" if quality_score >= 60 else 
                                      "Validation recommandée")
        }
    
    def _generate_executive_summary(self, synthesis: Dict, metrics: Dict) -> Dict:
        """Génération résumé exécutif"""
        zones_aveugles = synthesis.get("zones_aveugles_critiques", [])
        priorite = metrics.get("priorite_intervention", "INCONNUE")
        
        # Message clé selon priorité
        if priorite == "URGENTE":
            key_message = "🚨 INTERVENTION IMMÉDIATE REQUISE - Zones aveugles critiques multiples"
        elif priorite == "ÉLEVÉE":
            key_message = "⚠️ ACTION RAPIDE RECOMMANDÉE - Écarts significatifs culture sécurité"
        else:
            key_message = "📊 SURVEILLANCE RENFORCÉE - Écarts modérés à surveiller"
        
        # Top 3 actions
        actions = synthesis.get("actions_prioritaires", [])[:3]
        top_actions = [action.get("action", "Action") for action in actions]
        
        return {
            "message_cle": key_message,
            "priorite_globale": priorite,
            "zones_aveugles_nb": len(zones_aveugles),
            "top_3_actions": top_actions,
            "impact_business": synthesis.get("impact_business", {}).get("esperance_perte", 0),
            "timeline_critique": "2-4 semaines" if priorite in ["URGENTE", "ÉLEVÉE"] else "1-3 mois",
            "niveau_risque": synthesis.get("risk_assessment", {}).get("niveau_risque", "INCONNU"),
            "roi_intervention": synthesis.get("impact_business", {}).get("roi_intervention", {}).get("roi_ratio", 0)
        }
    
    # ==========================================
    # MÉTHODES D'AFFICHAGE
    # ==========================================
    
    def _display_a1_summary(self, result_a1: Dict):
        """Affichage résumé A1"""
        variables = result_a1.get("variables_culture_sst", {})
        score_global = result_a1.get("scores_autoeval", {}).get("score_global", 0)
        
        print(f"📊 Score global autoévaluation: {score_global}/100")
        print(f"🎯 Variables culture analysées: {len(variables)}")
        print(f"💡 Recommandations générées: {len(result_a1.get('recommendations', []))}")
        print(f"✅ Confiance agent: {result_a1.get('confidence_score', 0):.2f}")
    
    def _display_a2_summary(self, result_a2: Dict):
        """Affichage résumé A2"""
        observations = result_a2.get("observations", {})
        score_comportement = observations.get("score_comportement", 0)
        dangers = observations.get("dangers_detectes", 0)
        
        print(f"🔍 Score comportement terrain: {score_comportement}/100")
        print(f"⚠️ Dangers détectés: {dangers}")
        print(f"🛡️ Conformité EPI: {observations.get('conformite_procedures', 0):.1f}%")
        print(f"💡 Recommandations générées: {len(result_a2.get('recommendations', []))}")
        print(f"✅ Confiance agent: {result_a2.get('confidence_score', 0):.2f}")
    
    def _display_an1_summary(self, result_an1: Dict):
        """Affichage résumé AN1"""
        ecarts = result_an1.get("ecarts_analysis", {})
        zones_aveugles = ecarts.get("zones_aveugles", [])
        summary = result_an1.get("summary", {})
        
        print(f"📊 Écart moyen détecté: {summary.get('ecart_moyen', 0):.1f}%")
        print(f"⚠️ Zones aveugles identifiées: {len(zones_aveugles)}")
        print(f"🔬 Modèles HSE appliqués: {len(result_an1.get('hse_models_analysis', {}))}")
        print(f"🚨 Priorité intervention: {summary.get('priorite_intervention', 'INCONNUE')}")
        print(f"✅ Confiance agent: {result_an1.get('confidence_score', 0):.2f}")
    
    def _display_final_report(self, report: Dict):
        """Affichage rapport final"""
        
        print("\n" + "=" * 60)
        print("📋 RAPPORT FINAL SAFETYAGENTIC")
        print("=" * 60)
        
        # Résumé exécutif
        exec_summary = report["executive_summary"]
        print(f"\n🎯 MESSAGE CLÉ:")
        print(f"   {exec_summary['message_cle']}")
        
        # Métriques globales
        metrics = report["global_metrics"]
        print(f"\n📊 MÉTRIQUES GLOBALES:")
        print(f"   • Confiance analyse: {metrics['confidence_globale']:.1%}")
        print(f"   • Variables analysées: {metrics['variables_analysees']}")
        print(f"   • Zones aveugles détectées: {metrics['zones_aveugles_detectees']}")
        print(f"   • Qualité analyse: {metrics['qualite_analyse']}")
        
        # Zones aveugles critiques
        synthesis = report["final_synthesis"]
        zones = synthesis["zones_aveugles_critiques"]
        if zones:
            print(f"\n⚠️ ZONES AVEUGLES CRITIQUES (TOP {len(zones)}):")
            for i, zone in enumerate(zones, 1):
                niveau = zone.get('niveau_critique', 'inconnu')
                icon = "🚨" if niveau == "critique" else "⚠️" if niveau == "eleve" else "📊"
                print(f"   {i}. {icon} {zone.get('variable', 'Variable')} - {zone.get('pourcentage_ecart', 0):.1f}% écart")
                print(f"      → {zone.get('impact_potentiel', 'Impact inconnu')}")
        
        # Actions prioritaires
        actions = synthesis["actions_prioritaires"][:4]
        print(f"\n💡 ACTIONS PRIORITAIRES (TOP {len(actions)}):")
        for i, action in enumerate(actions, 1):
            priorite = action.get('priorite', 'MOYENNE')
            icon = "🚨" if priorite == "URGENTE" else "⚠️" if priorite == "ÉLEVÉE" else "📋"
            print(f"   {i}. {icon} {priorite} - {action.get('timeline', 'Timeline inconnue')}")
            print(f"      {action.get('action', 'Action')}")
        
        # Impact business
        business = synthesis["impact_business"]
        print(f"\n💰 IMPACT BUSINESS:")
        print(f"   • Coût zones aveugles: {business['cout_zones_aveugles']:,}$")
        print(f"   • Probabilité incident: {business['probabilite_incident']:.1%}")
        print(f"   • Espérance perte: {business['esperance_perte']:,}$")
        print(f"   • ROI intervention: {business['roi_intervention']['roi_ratio']}x")
        
        # Évaluation qualité
        quality = report["quality_assessment"]
        print(f"\n✅ QUALITÉ: {quality['niveau_qualite']} ({quality['score_qualite']}/100)")
        print(f"   Recommandation: {quality['recommandation_qualite']}")


async def test_orchestrateur_incident_construction():
    """Test orchestrateur avec incident construction réaliste"""
    
    print("🧪 TEST ORCHESTRATEUR SAFETYAGENTIC")
    print("=" * 45)
    print("🎯 Workflow complet: A1 → A2 → AN1 → Synthèse")
    print("🔬 Analyse culture sécurité avec zones aveugles")
    print("💡 Recommandations priorisées et impact business")
    print("🏗️ Cas réel: Chute de hauteur construction")
    
    # Incident CNESST construction réaliste
    incident_construction = {
        "ID": 2024156789,
        "NATURE_LESION": "BLES. TRAUMA. OS,NERFS,MOELLE EPINI....",
        "SIEGE_LESION": "COLONNE VERTEBRALE...",
        "GENRE": "CHUTE DE HAUTEUR...",
        "AGENT_CAUSAL_LESION": "ECHAFAUDAGE,PLATEFORME ELEVATRICE...",
        "SEXE_PERS_PHYS": "M",
        "GROUPE_AGE": "25-29 ANS",
        "SECTEUR_SCIAN": "CONSTRUCTION", 
        "IND_LESION_SURDITE": "NON",
        "IND_LESION_MACHINE": "NON",
        "IND_LESION_TMS": "NON",
        "IND_LESION_PSY": "NON",
        "IND_LESION_COVID_19": "NON"
    }
    
    # Contexte entreprise construction PME
    context_entreprise = {
        "nom_entreprise": "Construction Sommet Inc.",
        "taille_entreprise": "PME - 38 employés",
        "experience_sst": "Intermédiaire - Programme SST 3 ans",
        "incidents_recents": 4,
        "formation_recente_sst": False,
        "secteur_risque": "Élevé - Construction résidentielle",
        "certification_sst": "Aucune",
        "budget_sst_annuel": 22000,
        "responsable_sst": "Contremaître senior",
        "type_projets": "Maisons unifamiliales",
        "chiffre_affaires": 2800000,
        "marge_beneficiaire": "7%"
    }
    
    print(f"\n📋 INCIDENT ANALYSÉ:")
    print(f"   • ID CNESST: {incident_construction['ID']}")
    print(f"   • Nature lésion: {incident_construction['NATURE_LESION']}")
    print(f"   • Type incident: {incident_construction['GENRE']}")
    print(f"   • Siège lésion: {incident_construction['SIEGE_LESION']}")
    print(f"   • Agent causal: {incident_construction['AGENT_CAUSAL_LESION']}")
    print(f"   • Profil travailleur: {incident_construction['SEXE_PERS_PHYS']}, {incident_construction['GROUPE_AGE']}")
    
    print(f"\n🏢 CONTEXTE ENTREPRISE:")
    print(f"   • {context_entreprise['nom_entreprise']}")
    print(f"   • Taille: {context_entreprise['taille_entreprise']}")
    print(f"   • Expérience SST: {context_entreprise['experience_sst']}")
    print(f"   • Incidents récents: {context_entreprise['incidents_recents']}")
    print(f"   • Budget SST: {context_entreprise['budget_sst_annuel']:,}$ ({context_entreprise['budget_sst_annuel']/context_entreprise['chiffre_affaires']*100:.1f}% CA)")
    print(f"   • Spécialité: {context_entreprise['type_projets']}")
    
    # Initialisation orchestrateur
    print(f"\n🤖 Initialisation Orchestrateur SafetyAgentic...")
    orchestrator = SafetyAgenticOrchestrator()
    
    # Démarrage analyse complète
    print(f"\n🚀 LANCEMENT ANALYSE CULTURE SÉCURITÉ")
    print("=" * 50)
    
    debut_analyse = datetime.now()
    
    # Exécution workflow complet
    rapport_final = await orchestrator.analyze_safety_culture(
        incident_construction, 
        context_entreprise
    )
    
    fin_analyse = datetime.now()
    
    if "error" in rapport_final:
        print(f"❌ ERREUR ORCHESTRATEUR: {rapport_final['error']}")
        return
    
    # Analyse détaillée des résultats
    print(f"\n" + "=" * 60)
    print("🎉 ANALYSE SAFETYAGENTIC TERMINÉE AVEC SUCCÈS !")
    print("=" * 60)
    
    # Performance et info générale
    performance = rapport_final["analysis_info"]["performance_time"]
    total_time = (fin_analyse - debut_analyse).total_seconds()
    
    print(f"⏱️ Performance orchestrateur: {performance:.3f}s")
    print(f"⏱️ Temps total: {total_time:.3f}s")
    print(f"🎯 ID analyse: {rapport_final['analysis_info']['analysis_id']}")
    
    # Extraction données clés
    synthesis = rapport_final["final_synthesis"]
    metrics = rapport_final["global_metrics"]
    exec_summary = rapport_final["executive_summary"]
    quality = rapport_final["quality_assessment"]
    
    # Insights approfondis
    print(f"\n🔍 INSIGHTS APPROFONDIS:")
    print("-" * 30)
    
    # Zones aveugles avec détails
    zones_aveugles = synthesis["zones_aveugles_critiques"]
    print(f"⚠️ ZONES AVEUGLES DÉTECTÉES: {len(zones_aveugles)}")
    for i, zone in enumerate(zones_aveugles, 1):
        variable = zone.get('variable', 'Variable')
        ecart = zone.get("pourcentage_ecart", 0)
        niveau = zone.get('niveau_critique', 'inconnu')
        impact = zone.get("impact_potentiel", "Inconnu")
        explication = zone.get("explication", "")
        
        icon = "🚨" if niveau == "critique" else "⚠️" if niveau == "eleve" else "📊"
        print(f"   {i}. {icon} {variable.upper()} ({niveau.upper()})")
        print(f"      → Écart: {ecart:.1f}% | Impact: {impact}")
        print(f"      → {explication}")
    
    # Causes racines détaillées
    causes_racines = synthesis["causes_racines"]
    print(f"\n🎯 CAUSES RACINES IDENTIFIÉES: {len(causes_racines)}")
    for i, cause in enumerate(causes_racines, 1):
        print(f"   {i}. {cause['cause']} (Niveau: {cause['level']})")
        print(f"      📋 Evidence: {cause['evidence']}")
        print(f"      💥 Impact: {cause['impact']}")
    
    # Actions prioritaires avec détails
    actions = synthesis["actions_prioritaires"]
    print(f"\n💡 PLAN D'ACTION DÉTAILLÉ ({len(actions)} actions):")
    for i, action in enumerate(actions, 1):
        priorite = action.get("priorite", "MOYENNE")
        timeline = action.get("timeline", "Non spécifiée")
        methode = action.get("methode", "")
        ressources = action.get("ressources_requises", "")
        
        icon = "🚨" if priorite == "URGENTE" else "⚠️" if priorite == "ÉLEVÉE" else "📋"
        
        print(f"   {i}. {icon} PRIORITÉ {priorite} - {timeline}")
        print(f"      🎯 Action: {action.get('action', 'Action')}")
        if methode:
            print(f"      🔧 Méthode: {methode}")
        if ressources:
            print(f"      💰 Ressources: {ressources}")
        print()
    
    # Timeline d'intervention détaillée
    timeline = synthesis["timeline_intervention"]
    print(f"📅 TIMELINE D'INTERVENTION STRUCTURÉE:")
    
    if timeline.get("immediate"):
        print(f"   🚨 ACTIONS IMMÉDIATES (0-2 semaines): {len(timeline['immediate'])}")
        for j, action in enumerate(timeline["immediate"], 1):
            print(f"      {j}. {action}")
    
    if timeline.get("short_term"):
        print(f"   ⚠️ COURT TERME (2-8 semaines): {len(timeline['short_term'])}")
        for j, action in enumerate(timeline["short_term"], 1):
            print(f"      {j}. {action}")
    
    if timeline.get("medium_term"):
        print(f"   📋 MOYEN TERME (2-6 mois): {len(timeline['medium_term'])}")
        for j, action in enumerate(timeline["medium_term"], 1):
            print(f"      {j}. {action}")
    
    # Impact business très détaillé
    business_impact = synthesis["impact_business"]
    roi_info = business_impact["roi_intervention"]
    
    print(f"\n💰 ANALYSE IMPACT BUSINESS APPROFONDIE:")
    print(f"   📊 Zones aveugles: {business_impact['zones_critiques']} critiques + {business_impact['zones_elevees']} élevées")
    print(f"   💸 Coût zones aveugles: {business_impact['cout_zones_aveugles']:,}$ ({business_impact['cout_zones_aveugles']/context_entreprise['chiffre_affaires']*100:.1f}% du CA)")
    print(f"   ⚡ Probabilité incident: {business_impact['probabilite_incident']:.1%} (vs 12% base construction)")
    print(f"   💥 Coût incident potentiel: {business_impact['cout_incident_potentiel']:,}$")
    print(f"   📈 Espérance de perte: {business_impact['esperance_perte']:,}$")
    
    print(f"\n📊 ANALYSE ROI INTERVENTION:")
    print(f"   💰 Investissement intervention: {roi_info['cout_intervention']:,}$")
    print(f"   💵 Économies potentielles: {roi_info['economies_potentielles']:,}$")
    print(f"   🎯 ROI ratio: {roi_info['roi_ratio']}x (retour {roi_info['roi_ratio']}$ par dollar investi)")
    print(f"   ⏰ Période récupération: ~{12//max(1, roi_info['roi_ratio'])} mois")
    
    # Métriques de succès
    success_metrics = synthesis["success_metrics"]
    print(f"\n📊 MÉTRIQUES DE SUCCÈS DÉFINIES ({len(success_metrics)}):")
    for i, metric in enumerate(success_metrics, 1):
        print(f"   {i}. {metric['variable'].upper()}")
        print(f"      📈 Baseline: {metric['baseline_ecart']:.1f}% écart")
        print(f"      🎯 Objectif: {metric['target_ecart']:.1f}% écart (réduction {metric['reduction_objective']})")
        print(f"      📏 Mesure: {metric['measurement_method']}")
        print(f"      🔄 Fréquence: {metric['frequency']}")
        print(f"      ✅ Seuil succès: {metric['success_threshold']}")
        print(f"      📊 KPI: {metric['kpi_specifique']}")
        print()
    
    # Évaluation risque résiduel approfondie
    risk_assessment = synthesis["risk_assessment"]
    print(f"⚠️ ÉVALUATION RISQUE RÉSIDUEL COMPLÈTE:")
    print(f"   🚨 Niveau risque: {risk_assessment['niveau_risque']}")
    print(f"   📝 Description: {risk_assessment['description']}")
    print(f"   📊 Zones critiques: {risk_assessment['zones_critiques']} | Zones élevées: {risk_assessment['zones_elevees']}")
    print(f"   ⚡ Probabilité incident: {risk_assessment['probabilite_incident']}")
    print(f"   💥 Impact potentiel: {risk_assessment['impact_potentiel']}")
    print(f"   🎯 Action requise: {risk_assessment['action_requise']}")
    
    # Recommandations spécifiques entreprise
    print(f"\n🎯 RECOMMANDATIONS SPÉCIFIQUES ENTREPRISE:")
    print(f"   Analyse pour: {context_entreprise['nom_entreprise']}")
    
    # Budget SST insuffisant
    pct_budget_sst = context_entreprise['budget_sst_annuel'] / context_entreprise['chiffre_affaires'] * 100
    if pct_budget_sst < 1.0:
        budget_recommande = int(context_entreprise['chiffre_affaires'] * 0.015)  # 1.5% CA
        print(f"   💰 Budget SST insuffisant ({context_entreprise['budget_sst_annuel']:,}$ = {pct_budget_sst:.1f}% CA)")
        print(f"      → Recommandation: {budget_recommande:,}$ (1.5% CA)")
        print(f"      → Augmentation: +{budget_recommande - context_entreprise['budget_sst_annuel']:,}$")
        print(f"      → ROI attendu: {roi_info['roi_ratio']}x")
    
    # Incidents fréquents
    if context_entreprise["incidents_recents"] >= 3:
        print(f"   🚨 Taux incidents élevé ({context_entreprise['incidents_recents']} récents)")
        print(f"      → Audit système SST complet recommandé")
        print(f"      → Investigation causes systémiques")
    
    # Formation manquante
    if not context_entreprise["formation_recente_sst"]:
        print(f"   📚 Formation SST non récente")
        print(f"      → Formation superviseurs PRIORITÉ #1")
        print(f"      → Certification travail hauteur obligatoire")
    
    # Aucune certification
    if context_entreprise.get("certification_sst") == "Aucune":
        print(f"   🏆 Aucune certification SST")
        print(f"      → Viser certification COR (Certificate of Recognition)")
        print(f"      → Avantages: réduction primes assurance + image")
    
    # Message final et recommandations
    priorite_globale = exec_summary["priorite_globale"]
    message_cle = exec_summary["message_cle"]
    timeline_critique = exec_summary["timeline_critique"]
    
    print(f"\n" + "=" * 60)
    print("📋 RÉSUMÉ EXÉCUTIF FINAL")
    print("=" * 60)
    print(f"🎯 {message_cle}")
    print(f"🚨 Priorité globale: {priorite_globale}")
    print(f"⏰ Timeline critique: {timeline_critique}")
    print(f"💸 Impact business: {exec_summary['impact_business']:,}$")
    print(f"📈 ROI intervention: {exec_summary['roi_intervention']}x")
    print(f"⚠️ Niveau risque: {exec_summary['niveau_risque']}")
    print(f"✅ Qualité analyse: {quality['niveau_qualite']} ({quality['score_qualite']}/100)")
    
    # Alerte finale selon priorité
    if priorite_globale in ["URGENTE", "ÉLEVÉE"]:
        print(f"\n🚨 ALERTE DIRECTION:")
        print(f"   Action immédiate requise dans les {timeline_critique}")
        print(f"   Zones aveugles critiques = risque incident grave")
        print(f"   Coût inaction: {business_impact['esperance_perte']:,}$ espérance perte")
        print(f"   Investissement requis: {roi_info['cout_intervention']:,}$ (ROI {roi_info['roi_ratio']}x)")
    else:
        print(f"\n✅ SITUATION GÉRABLE:")
        print(f"   Amélioration continue avec surveillance renforcée")
        print(f"   Implémenter actions préventives selon timeline")
    
    print(f"\n🎉 ANALYSE SAFETYAGENTIC TERMINÉE - RAPPORT COMPLET GÉNÉRÉ")
    print(f"⏱️ Performance totale: {total_time:.3f}s")
    print(f"📊 Recommandation: {quality['recommandation_qualite']}")
    print(f"🎯 Prêt pour implémentation immédiate")
    
    return rapport_final

if __name__ == "__main__":
    # Exécution test orchestrateur complet
    asyncio.run(test_orchestrateur_incident_construction())