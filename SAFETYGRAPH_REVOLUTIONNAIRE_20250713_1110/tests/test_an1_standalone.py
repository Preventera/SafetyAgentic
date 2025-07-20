# Test AN1 Standalone - Analyste Écarts SafetyAgentic
# ===================================================
# Version autonome sans imports externes

import asyncio
import numpy as np
from datetime import datetime
import logging

# Configuration logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SafetyAgentic.AN1")

class AN1AnalysteEcarts:
    """
    Agent AN1 - Analyste des Écarts Culture Sécurité
    Version standalone pour test
    """
    
    def __init__(self):
        """Initialisation Agent AN1"""
        self.agent_id = "AN1"
        self.agent_name = "Analyste Écarts"
        self.version = "1.0.0"
        
        # Modèles HSE intégrés
        self.hse_models = {
            "hfacs_l1": "Échecs organisationnels",
            "hfacs_l2": "Supervision inadéquate", 
            "hfacs_l3": "Actes/conditions précurseurs",
            "hfacs_l4": "Actes/conditions dangereux",
            "swiss_cheese": "Défaillances barrières",
            "srk": "Niveaux comportement (Skill-Rule-Knowledge)",
            "reason": "Erreurs actives vs latentes",
            "bow_tie": "Analyse barrières préventives/protectives"
        }
        
        # Seuils d'écarts critiques
        self.ecart_thresholds = {
            "faible": 10,      # Écart < 10% = acceptable
            "modere": 25,      # Écart 10-25% = à surveiller
            "eleve": 50,       # Écart 25-50% = critique
            "critique": 100    # Écart > 50% = zone aveugle majeure
        }
        
        logger.info(f"🤖 Agent {self.agent_id} ({self.agent_name}) initialisé")
        print(f"🤖 Agent {self.agent_id} ({self.agent_name}) initialisé")
    
    async def process(self, data_a1, data_a2, context=None):
        """Traitement principal: analyser écarts A1 vs A2"""
        start_time = datetime.now()
        logger.info("🔄 Démarrage traitement Agent AN1")
        
        try:
            # 1. Validation données d'entrée
            self._validate_input_data(data_a1, data_a2)
            logger.info("✅ Validation des données d'entrée réussie")
            
            # 2. Calcul écarts variables culture SST
            ecarts_variables = self._calculate_culture_gaps(data_a1, data_a2)
            
            # 3. Application des modèles HSE
            analysis_hse = self._apply_hse_models(ecarts_variables, context)
            
            # 4. Identification zones aveugles
            zones_aveugles = self._identify_blind_spots(ecarts_variables)
            
            # 5. Calcul scores réalisme culturel
            realisme_scores = self._calculate_realism_scores(data_a1, data_a2)
            
            # 6. Génération recommandations ciblées
            recommendations = self._generate_targeted_recommendations(
                ecarts_variables, zones_aveugles, analysis_hse
            )
            
            # 7. Calcul métriques performance
            performance_time = (datetime.now() - start_time).total_seconds()
            confidence_score = self._calculate_confidence_score(ecarts_variables)
            
            logger.info(f"📊 Performance AN1: {performance_time:.2f}s, confidence: {confidence_score:.2f}")
            
            # 8. Construction résultat final
            result = {
                "agent_info": {
                    "agent_id": self.agent_id,
                    "agent_name": self.agent_name,
                    "version": self.version,
                    "timestamp": datetime.now().isoformat(),
                    "performance_time": performance_time,
                    "confidence_score": confidence_score
                },
                "ecarts_analysis": {
                    "ecarts_variables": ecarts_variables,
                    "zones_aveugles": zones_aveugles,
                    "realisme_scores": realisme_scores,
                    "nombre_ecarts_critiques": len([e for e in ecarts_variables.values() if e.get("niveau") == "critique"])
                },
                "hse_models_analysis": analysis_hse,
                "recommendations": recommendations,
                "summary": {
                    "ecart_moyen": np.mean([e.get("pourcentage", 0) for e in ecarts_variables.values()]),
                    "variables_critiques": len(zones_aveugles),
                    "actions_recommandees": len(recommendations),
                    "priorite_intervention": self._determine_intervention_priority(zones_aveugles)
                }
            }
            
            logger.info(f"✅ Agent AN1 terminé - Score confiance: {confidence_score:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur Agent AN1: {str(e)}")
            return {"error": str(e), "agent_id": self.agent_id}
    
    def _validate_input_data(self, data_a1, data_a2):
        """Validation des données A1 et A2"""
        if not data_a1 or not data_a2:
            raise ValueError("Données A1 ou A2 manquantes")
        
        required_a1 = ["variables_culture_sst"]
        required_a2 = ["variables_culture_terrain"]
        
        for field in required_a1:
            if field not in data_a1:
                raise ValueError(f"Champ manquant A1: {field}")
                
        for field in required_a2:
            if field not in data_a2:
                raise ValueError(f"Champ manquant A2: {field}")
    
    def _calculate_culture_gaps(self, data_a1, data_a2):
        """Calcul écarts entre variables culture A1 vs A2"""
        ecarts = {}
        
        vars_a1 = data_a1.get("variables_culture_sst", {})
        vars_a2 = data_a2.get("variables_culture_terrain", {})
        
        for variable in set(vars_a1.keys()).intersection(set(vars_a2.keys())):
            score_a1 = vars_a1[variable].get("score", 0)
            score_a2 = vars_a2[variable].get("score", 0)
            
            # Calcul écart relatif
            if score_a1 > 0:
                ecart_pct = abs(score_a1 - score_a2) / score_a1 * 100
            else:
                ecart_pct = abs(score_a2) * 10
            
            # Classification niveau écart
            if ecart_pct < self.ecart_thresholds["faible"]:
                niveau = "faible"
            elif ecart_pct < self.ecart_thresholds["modere"]:
                niveau = "modere"
            elif ecart_pct < self.ecart_thresholds["eleve"]:
                niveau = "eleve"
            else:
                niveau = "critique"
            
            ecarts[variable] = {
                "score_autoeval": score_a1,
                "score_terrain": score_a2,
                "ecart_absolu": abs(score_a1 - score_a2),
                "pourcentage": ecart_pct,
                "niveau": niveau,
                "direction": "surestimation" if score_a1 > score_a2 else "sous_estimation",
                "variable_source_a1": vars_a1[variable].get("source", "unknown"),
                "variable_source_a2": vars_a2[variable].get("source", "unknown")
            }
        
        return ecarts
    
    def _apply_hse_models(self, ecarts_variables, context=None):
        """Application des modèles HSE sur les écarts"""
        hse_analysis = {}
        
        for model_code, model_name in self.hse_models.items():
            if model_code.startswith("hfacs"):
                analysis = self._apply_hfacs_model(model_code, ecarts_variables)
            elif model_code == "swiss_cheese":
                analysis = self._apply_swiss_cheese_model(ecarts_variables)
            elif model_code == "srk":
                analysis = self._apply_srk_model(ecarts_variables)
            else:
                analysis = self._apply_generic_hse_model(model_code, ecarts_variables)
            
            hse_analysis[model_code] = {
                "model_name": model_name,
                "analysis": analysis,
                "variables_impliquees": len([v for v in ecarts_variables.keys() 
                                           if ecarts_variables[v]["niveau"] in ["eleve", "critique"]]),
                "score_applicabilite": self._calculate_model_applicability(model_code, ecarts_variables)
            }
        
        return hse_analysis
    
    def _apply_hfacs_model(self, level, ecarts):
        """Application modèle HFACS selon niveau"""
        hfacs_mapping = {
            "hfacs_l1": ["leadership_sst", "politique_securite"],
            "hfacs_l2": ["supervision_directe", "formation_securite"],
            "hfacs_l3": ["usage_epi", "respect_procedures"],
            "hfacs_l4": ["comportements_risque", "communication_risques"]
        }
        
        variables_concernees = hfacs_mapping.get(level, [])
        ecarts_niveau = {v: ecarts[v] for v in variables_concernees if v in ecarts}
        
        score_defaillance = np.mean([e["pourcentage"] for e in ecarts_niveau.values()]) if ecarts_niveau else 0
        
        return {
            "niveau_hfacs": level,
            "variables_analysees": len(ecarts_niveau),
            "ecarts_critiques": len([e for e in ecarts_niveau.values() if e["niveau"] == "critique"]),
            "score_defaillance": score_defaillance,
            "interpretation": self._interpret_hfacs_level(level, score_defaillance)
        }
    
    def _interpret_hfacs_level(self, level, score):
        """Interprétation du score HFACS par niveau"""
        interpretations = {
            "hfacs_l1": f"Défaillances organisationnelles: {score:.1f}% - Engagement leadership",
            "hfacs_l2": f"Supervision inadéquate: {score:.1f}% - Encadrement terrain", 
            "hfacs_l3": f"Conditions précurseurs: {score:.1f}% - Prévention incidents",
            "hfacs_l4": f"Actes dangereux: {score:.1f}% - Comportements risque"
        }
        return interpretations.get(level, f"Analyse {level}: {score:.1f}%")
    
    def _apply_swiss_cheese_model(self, ecarts):
        """Application modèle Swiss Cheese"""
        barrieres = {
            "organisationnelles": ["leadership_sst", "formation_securite"],
            "supervision": ["supervision_directe", "communication_risques"],
            "individuelles": ["usage_epi", "respect_procedures"]
        }
        
        defaillances = {}
        for barriere_type, variables in barrieres.items():
            ecarts_barriere = {v: ecarts[v] for v in variables if v in ecarts}
            if ecarts_barriere:
                defaillance_score = np.mean([e["pourcentage"] for e in ecarts_barriere.values()])
                defaillances[barriere_type] = {
                    "score_defaillance": defaillance_score,
                    "variables_impliquees": list(ecarts_barriere.keys()),
                    "niveau_risque": "high" if defaillance_score > 30 else "medium" if defaillance_score > 15 else "low"
                }
        
        return {
            "defaillances_barrieres": defaillances,
            "risque_global": max([d["score_defaillance"] for d in defaillances.values()]) if defaillances else 0,
            "barrieres_critiques": [k for k, v in defaillances.items() if v["niveau_risque"] == "high"]
        }
    
    def _apply_srk_model(self, ecarts):
        """Application modèle SRK"""
        srk_mapping = {
            "skill": ["usage_epi", "competences_techniques"],
            "rule": ["respect_procedures", "formation_securite"],
            "knowledge": ["communication_risques", "supervision_directe"]
        }
        
        srk_analysis = {}
        for niveau, variables in srk_mapping.items():
            ecarts_niveau = {v: ecarts[v] for v in variables if v in ecarts}
            if ecarts_niveau:
                score_ecart = np.mean([e["pourcentage"] for e in ecarts_niveau.values()])
                srk_analysis[niveau] = {
                    "score_ecart": score_ecart,
                    "variables_count": len(ecarts_niveau),
                    "niveau_defaillance": "critique" if score_ecart > 40 else "eleve" if score_ecart > 20 else "faible"
                }
        
        return srk_analysis
    
    def _apply_generic_hse_model(self, model_code, ecarts):
        """Analyse générique pour autres modèles HSE"""
        return {
            "model_code": model_code,
            "variables_analysees": len(ecarts),
            "score_global": np.mean([e["pourcentage"] for e in ecarts.values()]) if ecarts else 0
        }
    
    def _identify_blind_spots(self, ecarts_variables):
        """Identification zones aveugles culture sécurité"""
        zones_aveugles = []
        
        for variable, ecart_data in ecarts_variables.items():
            if ecart_data["niveau"] in ["eleve", "critique"]:
                zone_aveugle = {
                    "variable": variable,
                    "type_ecart": ecart_data["direction"],
                    "pourcentage_ecart": ecart_data["pourcentage"],
                    "niveau_critique": ecart_data["niveau"],
                    "score_autoeval": ecart_data["score_autoeval"],
                    "score_terrain": ecart_data["score_terrain"],
                    "explication": self._explain_blind_spot(variable, ecart_data),
                    "impact_potentiel": self._assess_blind_spot_impact(variable, ecart_data)
                }
                zones_aveugles.append(zone_aveugle)
        
        zones_aveugles.sort(key=lambda x: x["pourcentage_ecart"], reverse=True)
        return zones_aveugles
    
    def _explain_blind_spot(self, variable, ecart_data):
        """Explication textuelle de la zone aveugle"""
        direction = ecart_data["direction"]
        pct = ecart_data["pourcentage"]
        
        if direction == "surestimation":
            return f"Surestimation de {pct:.1f}% sur {variable}. L'équipe pense mieux performer qu'en réalité."
        else:
            return f"Sous-estimation de {pct:.1f}% sur {variable}. Performance terrain supérieure aux perceptions."
    
    def _assess_blind_spot_impact(self, variable, ecart_data):
        """Évaluation impact potentiel zone aveugle"""
        variable_criticality = {
            "usage_epi": "high",
            "respect_procedures": "high", 
            "supervision_directe": "high",
            "formation_securite": "medium",
            "communication_risques": "medium"
        }
        
        criticality = variable_criticality.get(variable, "medium")
        ecart_level = ecart_data["niveau"]
        
        if criticality == "high" and ecart_level == "critique":
            return "CRITIQUE - Risque incident majeur"
        elif criticality == "high" or ecart_level == "critique":
            return "ÉLEVÉ - Intervention urgente requise"
        else:
            return "MODÉRÉ - Surveillance renforcée"
    
    def _calculate_realism_scores(self, data_a1, data_a2):
        """Calcul scores réalisme culturel"""
        scores_a1 = data_a1.get("scores_autoeval", {})
        observations_a2 = data_a2.get("observations", {})
        
        score_global_a1 = scores_a1.get("score_global", 70)
        score_comportement_a2 = observations_a2.get("score_comportement", 50)
        
        realisme_global = max(0, 100 - abs(score_global_a1 - score_comportement_a2))
        
        return {
            "realisme_global": realisme_global,
            "fiabilite_autoeval": min(100, realisme_global + 10),
            "coherence_perception": realisme_global,
            "niveau_autocritique": "élevé" if realisme_global > 80 else "moyen" if realisme_global > 60 else "faible"
        }
    
    def _generate_targeted_recommendations(self, ecarts, zones_aveugles, hse_analysis):
        """Génération recommandations ciblées"""
        recommendations = []
        
        # Recommandations par zone aveugle
        for zone in zones_aveugles[:5]:
            rec = {
                "type": "zone_aveugle",
                "priorite": "URGENTE" if zone["niveau_critique"] == "critique" else "ÉLEVÉE",
                "variable_cible": zone["variable"],
                "action": f"Corriger écart {zone['type_ecart']} de {zone['pourcentage_ecart']:.1f}% sur {zone['variable']}",
                "methode": self._recommend_correction_method(zone["variable"], zone["type_ecart"]),
                "timeline": "2-4 semaines" if zone["niveau_critique"] == "critique" else "1-2 mois",
                "ressources_requises": self._estimate_resources(zone["variable"], zone["pourcentage_ecart"])
            }
            recommendations.append(rec)
        
        # Recommandations générales
        if len(zones_aveugles) > 2:
            recommendations.append({
                "type": "global",
                "priorite": "ÉLEVÉE", 
                "action": "Programme amélioration culture sécurité globale",
                "methode": "Formation management + observations terrain systématiques",
                "timeline": "3-6 mois"
            })
        
        return recommendations
    
    def _recommend_correction_method(self, variable, direction):
        """Recommandation méthode correction"""
        methods = {
            "usage_epi": {
                "surestimation": "Observations terrain ciblées + formations pratiques",
                "sous_estimation": "Sensibilisation performance + reconnaissance efforts"
            },
            "supervision_directe": {
                "surestimation": "Formation superviseurs + audits conformité",
                "sous_estimation": "Valorisation encadrement + outils supervision"
            },
            "respect_procedures": {
                "surestimation": "Audit conformité + coaching terrain",
                "sous_estimation": "Communication succès + reconnaissance"
            }
        }
        
        return methods.get(variable, {}).get(direction, "Formation ciblée + suivi renforcé")
    
    def _estimate_resources(self, variable, ecart_pct):
        """Estimation ressources requises"""
        if ecart_pct > 50:
            return "Ressources importantes - Formation complète équipe"
        elif ecart_pct > 25:
            return "Ressources modérées - Formation superviseurs"
        else:
            return "Ressources limitées - Sensibilisation ciblée"
    
    def _calculate_model_applicability(self, model_code, ecarts):
        """Calcul score applicabilité modèle"""
        variables_critiques = len([e for e in ecarts.values() if e["niveau"] in ["eleve", "critique"]])
        total_variables = len(ecarts) if ecarts else 1
        
        base_score = (variables_critiques / total_variables) * 100
        return min(95, max(20, base_score + 20))
    
    def _calculate_confidence_score(self, ecarts_variables):
        """Calcul score confiance global"""
        if not ecarts_variables:
            return 0.5
        
        coherence = np.mean([1 - min(1, e["pourcentage"] / 100) for e in ecarts_variables.values()])
        completude = min(1.0, len(ecarts_variables) / 8)
        
        return max(0.3, min(0.95, (coherence * 0.7) + (completude * 0.3)))
    
    def _determine_intervention_priority(self, zones_aveugles):
        """Détermination priorité intervention"""
        if not zones_aveugles:
            return "FAIBLE"
        
        critiques = len([z for z in zones_aveugles if z["niveau_critique"] == "critique"])
        eleves = len([z for z in zones_aveugles if z["niveau_critique"] == "eleve"])
        
        if critiques >= 3:
            return "URGENTE"
        elif critiques >= 1 or eleves >= 5:
            return "ÉLEVÉE"
        elif eleves >= 2:
            return "MOYENNE"
        else:
            return "FAIBLE"


async def test_agent_an1_standalone():
    """Test standalone Agent AN1"""
    
    print("🧪 TEST AGENT AN1 - ANALYSTE ÉCARTS")
    print("=" * 40)
    print("🎯 Focus: Analyse écarts A1 (autoéval) vs A2 (terrain)")
    print("🔬 Modèles HSE: HFACS, Swiss Cheese, SRK, Bow-Tie")
    print("⚠️ Zones aveugles: Identification automatique")
    
    # Données A1 (autoévaluations) - Scores optimistes
    print("\n📊 DONNÉES A1 (AUTOÉVALUATIONS):")
    data_a1 = {
        "variables_culture_sst": {
            "usage_epi": {"score": 8.5, "source": "questionnaire", "confiance": 0.9},
            "respect_procedures": {"score": 7.8, "source": "questionnaire", "confiance": 0.8},
            "formation_securite": {"score": 7.2, "source": "questionnaire", "confiance": 0.8},
            "supervision_directe": {"score": 7.5, "source": "questionnaire", "confiance": 0.7},
            "communication_risques": {"score": 6.8, "source": "questionnaire", "confiance": 0.8},
            "leadership_sst": {"score": 7.0, "source": "questionnaire", "confiance": 0.7}
        },
        "scores_autoeval": {
            "score_global": 74,
            "fiabilite": 0.8,
            "biais_detectes": ["surconfiance", "desirabilite_sociale"]
        }
    }
    
    for var, data in data_a1["variables_culture_sst"].items():
        print(f"  • {var}: {data['score']}/10 (confiance: {data['confiance']})")
    
    # Données A2 (observations terrain) - Réalité moins optimiste
    print("\n🔍 DONNÉES A2 (OBSERVATIONS TERRAIN):")
    data_a2 = {
        "variables_culture_terrain": {
            "usage_epi": {"score": 4.8, "source": "observation_epi", "observations": 15},
            "respect_procedures": {"score": 5.2, "source": "procedure_compliance", "observations": 12},
            "formation_securite": {"score": 7.0, "source": "behavioral_analysis", "observations": 8},
            "supervision_directe": {"score": 3.5, "source": "hazard_detection", "observations": 10},
            "communication_risques": {"score": 5.5, "source": "behavioral_analysis", "observations": 6},
            "leadership_sst": {"score": 4.2, "source": "hazard_detection", "observations": 5}
        },
        "observations": {
            "score_comportement": 48,
            "dangers_detectes": 3,
            "epi_analyses": 15,
            "conformite_procedures": 45.0
        }
    }
    
    for var, data in data_a2["variables_culture_terrain"].items():
        print(f"  • {var}: {data['score']}/10 (observations: {data['observations']})")
    
    # Contexte
    context = {
        "secteur_scian": "CONSTRUCTION",
        "type_incident": "CHUTE_HAUTEUR", 
        "gravite": "MAJEUR"
    }
    
    print(f"\n🏗️ CONTEXTE: {context['secteur_scian']} - {context['type_incident']}")
    
    print("\n🤖 Initialisation Agent AN1...")
    agent_an1 = AN1AnalysteEcarts()
    
    print("\n🔄 ANALYSE ÉCARTS A1 vs A2:")
    print("=" * 35)
    
    result = await agent_an1.process(data_a1, data_a2, context)
    
    if "error" in result:
        print(f"❌ Erreur: {result['error']}")
        return
    
    # Résultats
    print(f"✅ Score confiance: {result['agent_info']['confidence_score']:.3f}")
    print(f"📊 Variables analysées: {len(result['ecarts_analysis']['ecarts_variables'])}")
    print(f"⚠️ Écarts critiques: {result['ecarts_analysis']['nombre_ecarts_critiques']}")
    print(f"🔬 Modèles HSE: {len(result['hse_models_analysis'])}")
    print(f"💡 Recommandations: {len(result['recommendations'])}")
    
    # Écarts détaillés
    print("\n🎯 ÉCARTS DÉTECTÉS PAR VARIABLE:")
    for var, ecart in result['ecarts_analysis']['ecarts_variables'].items():
        autoeval = ecart['score_autoeval']
        terrain = ecart['score_terrain']
        pct = ecart['pourcentage']
        niveau = ecart['niveau']
        direction = ecart['direction']
        
        icon = "🚨" if niveau == "critique" else "⚠️" if niveau == "eleve" else "📊"
        print(f"  {icon} {var}:")
        print(f"     Autoéval: {autoeval}/10 | Terrain: {terrain}/10")
        print(f"     Écart: {pct:.1f}% ({niveau}) - {direction}")
    
    # Zones aveugles
    print("\n⚠️ ZONES AVEUGLES IDENTIFIÉES:")
    zones = result['ecarts_analysis']['zones_aveugles']
    if zones:
        for i, zone in enumerate(zones[:3], 1):
            print(f"  {i}. {zone['variable']} ({zone['niveau_critique'].upper()})")
            print(f"     → Écart: {zone['pourcentage_ecart']:.1f}% - {zone['type_ecart']}")
            print(f"     → Impact: {zone['impact_potentiel']}")
            print(f"     → {zone['explication']}")
    else:
        print("  ✅ Aucune zone aveugle critique détectée")
    
    # Modèles HSE
    print("\n🔬 ANALYSE MODÈLES HSE:")
    for model_code, analysis in result['hse_models_analysis'].items():
        print(f"  🎯 {analysis['model_name']}")
        print(f"     Applicabilité: {analysis['score_applicabilite']:.0f}%")
        
        if 'interpretation' in analysis['analysis']:
            print(f"     → {analysis['analysis']['interpretation']}")
        elif 'barrieres_critiques' in analysis['analysis']:
            barrieres = analysis['analysis']['barrieres_critiques']
            if barrieres:
                print(f"     → Barrières critiques: {', '.join(barrieres)}")
    
    # Recommandations
    print("\n💡 RECOMMANDATIONS PRIORITAIRES:")
    for i, rec in enumerate(result['recommendations'][:4], 1):
        priorite = rec['priorite']
        icon = "🚨" if priorite == "URGENTE" else "⚠️" if priorite == "ÉLEVÉE" else "📋"
        print(f"  {i}. {icon} {priorite}")
        print(f"     Action: {rec['action']}")
        if 'methode' in rec:
            print(f"     Méthode: {rec['methode']}")
        if 'timeline' in rec:
            print(f"     Timeline: {rec['timeline']}")
    
    # Résumé
    print("\n" + "=" * 50)
    print("📋 RÉSUMÉ ANALYSE ÉCARTS AN1")
    print("=" * 50)
    summary = result['summary']
    print(f"✅ Confiance: {result['agent_info']['confidence_score']:.1%}")
    print(f"📊 Écart moyen: {summary['ecart_moyen']:.1f}%")
    print(f"⚠️ Variables critiques: {summary['variables_critiques']}")
    print(f"🎯 Actions recommandées: {summary['actions_recommandees']}")
    print(f"🚨 Priorité: {summary['priorite_intervention']}")
    
    # Interprétation
    if summary['priorite_intervention'] == 'URGENTE':
        print("\n🚨 ALERTE: Écarts critiques - Intervention immédiate requise")
        print("   → Risque incident majeur si non corrigé rapidement")
    elif summary['priorite_intervention'] == 'ÉLEVÉE':
        print("\n⚠️ ATTENTION: Écarts significatifs - Action rapide recommandée")
        print("   → Planifier interventions dans les 2-4 semaines")
    else:
        print("\n✅ SITUATION: Écarts gérables - Surveillance renforcée")
        print("   → Maintenir vigilance et amélioration continue")
    
    print(f"\n🎉 TEST AGENT AN1 TERMINÉ!")
    print(f"⏱️ Performance: {result['agent_info']['performance_time']:.3f}s")
    print(f"🎯 Agent AN1 prêt pour orchestration SafetyAgentic")
    
    return result

if __name__ == "__main__":
    asyncio.run(test_agent_an1_standalone())