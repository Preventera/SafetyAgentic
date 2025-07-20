# Configuration Agents SafetyAgentic - Spécialisation Chute
# ========================================================
# Adaptation des agents A1, A2, AN1, R1 pour cas de chute réels

import json
from datetime import datetime

class ConfigurationAgentsChute:
    """
    Configuration spécialisée des agents SafetyAgentic pour analyse des chutes
    Basée sur les patterns identifiés dans les 87,651 cas CNESST
    """
    
    def __init__(self):
        self.config_chute = self.generer_config_specialisee()
    
    def generer_config_specialisee(self):
        """
        Configuration spécialisée basée sur l'analyse ÉTAPE 4B
        """
        return {
            "agent_a1_config": {
                "nom": "A1_Collecteur_Autoeval_Chute",
                "description": "Collecteur spécialisé autoévaluations risques de chute",
                "variables_cles_chute": [
                    "perception_hauteur",
                    "usage_epi_antichute", 
                    "formation_travail_hauteur",
                    "signalisation_zones_risque",
                    "maintenance_equipements",
                    "conditions_meteorologiques",
                    "fatigue_vigilance",
                    "pression_temporelle"
                ],
                "seuils_alertes": {
                    "perception_risque_faible": 70,  # % en dessous = alerte
                    "formation_insuffisante": 80,
                    "usage_epi_faible": 85
                },
                "prompts_specialises": {
                    "evaluation_hauteur": "Sur une échelle de 1-10, comment évaluez-vous votre perception des risques lors du travail en hauteur?",
                    "usage_harnais": "À quelle fréquence utilisez-vous correctement votre harnais de sécurité?",
                    "signalisation": "Les zones de risque de chute sont-elles clairement signalisées sur votre lieu de travail?"
                }
            },
            
            "agent_a2_config": {
                "nom": "A2_Capteur_Observations_Chute", 
                "description": "Capteur spécialisé observations terrain chutes",
                "zones_observation_prioritaires": [
                    "travail_hauteur_3m_plus",
                    "utilisation_echelles",
                    "surfaces_glissantes", 
                    "ouvertures_non_protegees",
                    "echafaudages_temporaires"
                ],
                "indicateurs_comportementaux": [
                    "port_harnais_systematique",
                    "verification_equipements",
                    "respect_procedures_hauteur",
                    "signalement_dangers",
                    "nettoyage_surfaces"
                ],
                "detecteurs_automatiques": {
                    "mots_cles_chute": [
                        "CHUTE", "CHUT", "TOMB", "GLISS", "TREBU",
                        "ECHELLE", "ESCALIER", "HAUTEUR", "SURFACE",
                        "PLANCHERS", "PASSAGES", "SURFACES DE SOL"
                    ],
                    "agents_causaux_prioritaires": [
                        "ECHELLES", "ECHAFAUDAGES", "TOITURES",
                        "PLANCHERS", "ESCALIERS", "OUVERTURES"
                    ]
                }
            },
            
            "agent_an1_config": {
                "nom": "AN1_Analyste_Ecarts_Chute",
                "description": "Analyste spécialisé écarts perception/réalité chutes", 
                "modeles_hse_chute": {
                    "hfacs_chute": {
                        "niveau_1": "Actes_dangereux_hauteur",
                        "niveau_2": "Conditions_dangereuses_equipements", 
                        "niveau_3": "Supervision_inadequate_travail_hauteur",
                        "niveau_4": "Facteurs_organisationnels_formation"
                    },
                    "swiss_cheese_chute": {
                        "barriere_1": "Formation_travail_hauteur",
                        "barriere_2": "Equipements_protection_individuelle",
                        "barriere_3": "Equipements_protection_collective",
                        "barriere_4": "Procedures_travail_hauteur",
                        "barriere_5": "Supervision_directe"
                    },
                    "bow_tie_chute": {
                        "evenement_central": "Chute_de_hauteur",
                        "causes_primaires": [
                            "Défaillance_EPI", "Surface_glissante", 
                            "Équipement_défaillant", "Facteur_humain"
                        ],
                        "consequences": [
                            "Blessure_légère", "Blessure_grave", 
                            "Incapacité", "Décès"
                        ]
                    }
                },
                "calculs_criticite_chute": {
                    "facteur_hauteur": "hauteur_m * 0.3",
                    "facteur_experience": "(10 - annees_experience) * 0.1", 
                    "facteur_equipement": "defaillance_epi * 0.4",
                    "facteur_environnement": "conditions_meteo * 0.2"
                }
            },
            
            "agent_r1_config": {
                "nom": "R1_Generateur_Recommandations_Chute",
                "description": "Générateur spécialisé recommandations prévention chutes",
                "actions_types_chute": {
                    "formation": {
                        "travail_hauteur_avance": {"cout": 1200, "efficacite": 85, "duree_semaines": 2},
                        "usage_epi_antichute": {"cout": 600, "efficacite": 75, "duree_semaines": 1},
                        "secourisme_hauteur": {"cout": 800, "efficacite": 60, "duree_semaines": 1}
                    },
                    "equipements": {
                        "harnais_nouvelle_gen": {"cout": 350, "efficacite": 90, "duree_semaines": 0},
                        "lignes_vie_temporaires": {"cout": 2500, "efficacite": 95, "duree_semaines": 2},
                        "detecteurs_mouvement": {"cout": 1800, "efficacite": 70, "duree_semaines": 1}
                    },
                    "procedures": {
                        "check_list_pre_travail": {"cout": 200, "efficacite": 65, "duree_semaines": 1},
                        "buddy_system_hauteur": {"cout": 150, "efficacite": 70, "duree_semaines": 0},
                        "inspection_quotidienne": {"cout": 400, "efficacite": 80, "duree_semaines": 1}
                    }
                },
                "calculs_roi_chute": {
                    "cout_incident_moyen": 6150,  # $ CAD basé CNESST
                    "cout_incident_grave": 45000,
                    "facteur_reduction_risque": 0.7,  # 70% réduction moyenne
                    "periode_projection": 36  # mois
                },
                "priorisation_actions": {
                    "criticite_elevee": "Formation + Équipements + Procédures",
                    "criticite_moyenne": "Formation + Procédures", 
                    "criticite_faible": "Procédures seulement"
                }
            },
            
            "orchestrateur_config": {
                "workflow_chute": {
                    "etape_1": "A1_collecte_perceptions_chute",
                    "etape_2": "A2_observations_terrain_chute", 
                    "etape_3": "AN1_analyse_ecarts_chute_12_modeles",
                    "etape_4": "R1_recommandations_chute_roi"
                },
                "seuils_performance": {
                    "duree_max_workflow": 1000,  # ms
                    "confiance_min": 70,         # %
                    "roi_min": 1000              # %
                },
                "options_reporting": {
                    "niveau_detail": "complet",
                    "format_sortie": ["json", "pdf", "dashboard"],
                    "alertes_temps_reel": True
                }
            }
        }
    
    def adapter_agent_a1(self, agent_a1_existant):
        """
        Adaptation de l'agent A1 existant pour spécialisation chute
        """
        config_a1 = self.config_chute["agent_a1_config"]
        
        # Mise à jour des variables de collecte
        agent_a1_existant.variables_specialisees = config_a1["variables_cles_chute"]
        agent_a1_existant.seuils_alertes = config_a1["seuils_alertes"]
        agent_a1_existant.prompts_chute = config_a1["prompts_specialises"]
        
        print(f"✅ Agent A1 adapté pour chutes avec {len(config_a1['variables_cles_chute'])} variables spécialisées")
        return agent_a1_existant
    
    def adapter_agent_a2(self, agent_a2_existant):
        """
        Adaptation de l'agent A2 existant pour spécialisation chute
        """
        config_a2 = self.config_chute["agent_a2_config"]
        
        # Configuration détection automatique
        agent_a2_existant.detecteurs_chute = config_a2["detecteurs_automatiques"]
        agent_a2_existant.zones_prioritaires = config_a2["zones_observation_prioritaires"]
        agent_a2_existant.indicateurs_comportementaux = config_a2["indicateurs_comportementaux"]
        
        print(f"✅ Agent A2 adapté pour chutes avec {len(config_a2['zones_observation_prioritaires'])} zones prioritaires")
        return agent_a2_existant
    
    def adapter_agent_an1(self, agent_an1_existant):
        """
        Adaptation de l'agent AN1 existant pour spécialisation chute
        """
        config_an1 = self.config_chute["agent_an1_config"]
        
        # Intégration modèles HSE spécialisés chute
        agent_an1_existant.modeles_hse_chute = config_an1["modeles_hse_chute"]
        agent_an1_existant.calculs_criticite = config_an1["calculs_criticite_chute"]
        
        print(f"✅ Agent AN1 adapté pour chutes avec {len(config_an1['modeles_hse_chute'])} modèles HSE spécialisés")
        return agent_an1_existant
    
    def adapter_agent_r1(self, agent_r1_existant):
        """
        Adaptation de l'agent R1 existant pour spécialisation chute
        """
        config_r1 = self.config_chute["agent_r1_config"]
        
        # Configuration recommandations spécialisées
        agent_r1_existant.actions_chute = config_r1["actions_types_chute"]
        agent_r1_existant.calculs_roi = config_r1["calculs_roi_chute"]
        agent_r1_existant.priorisation = config_r1["priorisation_actions"]
        
        total_actions = sum(len(cat) for cat in config_r1["actions_types_chute"].values())
        print(f"✅ Agent R1 adapté pour chutes avec {total_actions} types d'actions disponibles")
        return agent_r1_existant
    
    def configurer_orchestrateur(self, orchestrateur_existant):
        """
        Configuration de l'orchestrateur pour workflow chute optimisé
        """
        config_orch = self.config_chute["orchestrateur_config"]
        
        # Workflow spécialisé chute
        orchestrateur_existant.workflow_chute = config_orch["workflow_chute"]
        orchestrateur_existant.seuils_performance = config_orch["seuils_performance"]
        orchestrateur_existant