#!/usr/bin/env python3
"""
Module Vectorisation Normes ISO/SCIAN - SafetyGraph
==================================================
Intégration unifiée des normes ISO 45001, SCIAN, CSA pour SafetyGraph
Mario Genest - Safety Agentique - 12 juillet 2025

🎯 Fonctionnalités :
- Vectorisation corpus normatif unifié
- Recherche sémantique dans standards
- Recommandations conformité automatiques
- Adaptation sectorielle SCIAN précise
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import json
import logging
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION ET STRUCTURES DE DONNÉES
# ═══════════════════════════════════════════════════════════════

@dataclass
class RecommandationNormative:
    """Structure pour recommandation basée sur normes"""
    titre: str
    description: str
    norme_source: str
    section_iso: str
    secteur_scian: str
    niveau_priorite: int  # 1-5
    actions_concretes: List[str]
    references: List[str]
    conformite_score: float  # 0-1

class MoteurVectorisationNormes:
    """Moteur principal de vectorisation des normes HSE"""
    
    def __init__(self):
        self.normes_iso_45001 = self._charger_iso_45001()
        self.secteurs_scian = self._charger_secteurs_scian()
        self.normes_csa = self._charger_normes_csa()
        self.categories_cnesst = self._charger_categories_cnesst()
        self.corpus_vectorise = None
        self.index_semantique = {}
        
        # Configuration logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _charger_iso_45001(self) -> Dict:
        """Charge la structure complète ISO 45001"""
        return {
            "4_contexte": {
                "titre": "Contexte de l'organisation",
                "sections": {
                    "4.1": "Compréhension de l'organisation et de son contexte",
                    "4.2": "Compréhension des besoins et attentes des parties intéressées",
                    "4.3": "Détermination du domaine d'application du système de management SST",
                    "4.4": "Système de management de la SST"
                },
                "mots_cles": ["contexte", "organisation", "parties_interessees", "domaine_application"]
            },
            "5_leadership": {
                "titre": "Leadership et participation des travailleurs",
                "sections": {
                    "5.1": "Leadership et engagement",
                    "5.2": "Politique de SST",
                    "5.3": "Rôles, responsabilités et autorités organisationnelles",
                    "5.4": "Consultation et participation des travailleurs"
                },
                "mots_cles": ["leadership", "engagement", "politique", "responsabilites", "consultation", "participation"]
            },
            "6_planification": {
                "titre": "Planification",
                "sections": {
                    "6.1": "Actions à mettre en œuvre face aux risques et opportunités",
                    "6.2": "Objectifs de SST et planification pour les atteindre"
                },
                "mots_cles": ["planification", "risques", "opportunites", "objectifs", "planification_action"]
            },
            "7_support": {
                "titre": "Support",
                "sections": {
                    "7.1": "Ressources",
                    "7.2": "Compétences",
                    "7.3": "Sensibilisation",
                    "7.4": "Communication",
                    "7.5": "Informations documentées"
                },
                "mots_cles": ["ressources", "competences", "sensibilisation", "communication", "documentation"]
            },
            "8_realisation": {
                "titre": "Réalisation des activités opérationnelles",
                "sections": {
                    "8.1": "Planification et maîtrise opérationnelles",
                    "8.2": "Préparation et réponse aux situations d'urgence"
                },
                "mots_cles": ["operations", "maitrise", "urgence", "preparation", "reponse"]
            },
            "9_evaluation": {
                "titre": "Évaluation des performances",
                "sections": {
                    "9.1": "Surveillance, mesure, analyse et évaluation des performances",
                    "9.2": "Audit interne",
                    "9.3": "Revue de direction"
                },
                "mots_cles": ["surveillance", "mesure", "analyse", "evaluation", "audit", "revue"]
            },
            "10_amelioration": {
                "titre": "Amélioration",
                "sections": {
                    "10.1": "Généralités",
                    "10.2": "Incident, non-conformité et action corrective",
                    "10.3": "Amélioration continue"
                },
                "mots_cles": ["amelioration", "incident", "non_conformite", "action_corrective", "continue"]
            }
        }
    
    def _charger_secteurs_scian(self) -> Dict:
        """Charge les secteurs SCIAN prioritaires avec risques spécifiques"""
        return {
            "236": {
                "nom": "Construction de bâtiments",
                "risques_principaux": [
                    "chutes_hauteur", "electrocution", "blessures_outils", 
                    "exposition_substances", "troubles_musculosquelettiques"
                ],
                "normes_specifiques": ["CSA_Z1000", "CSA_Z45001"],
                "exigences_particulieres": [
                    "Plan de sécurité chantier obligatoire",
                    "Formation travail en hauteur",
                    "Procédures cadenassage énergies"
                ]
            },
            "311-333": {
                "nom": "Fabrication",
                "risques_principaux": [
                    "machines_dangereuses", "substances_chimiques", "bruit_excessif",
                    "espaces_confines", "manutention_manuelle"
                ],
                "normes_specifiques": ["CSA_Z1002", "ISO_12100"],
                "exigences_particulieres": [
                    "Analyse sécurité machines",
                    "Programme protection respiratoire",
                    "Surveillance exposition chimique"
                ]
            },
            "621": {
                "nom": "Services de soins de santé ambulatoires",
                "risques_principaux": [
                    "exposition_pathogenes", "piqures_aiguilles", "troubles_psychosociaux",
                    "violence_workplace", "troubles_musculosquelettiques"
                ],
                "normes_specifiques": ["CSA_Z1003", "OSHA_Bloodborne"],
                "exigences_particulieres": [
                    "Plan exposition professionnelle",
                    "Programme vaccination",
                    "Protocoles prévention violence"
                ]
            },
            "722": {
                "nom": "Services de restauration et débits de boissons",
                "risques_principaux": [
                    "brulures", "coupures", "glissades_chutes", 
                    "troubles_musculosquelettiques", "stress_thermique"
                ],
                "normes_specifiques": ["CSA_Z1000"],
                "exigences_particulieres": [
                    "Formation manipulation aliments",
                    "Procédures nettoyage sécuritaire",
                    "Gestion équipements chauffage"
                ]
            },
            "484": {
                "nom": "Transport par camion",
                "risques_principaux": [
                    "accidents_circulation", "troubles_musculosquelettiques", 
                    "fatigue_conduite", "exposition_intemperies"
                ],
                "normes_specifiques": ["CSA_Z1002", "Transport_Canada"],
                "exigences_particulieres": [
                    "Formation conduite défensive",
                    "Programmes gestion fatigue",
                    "Inspections véhicules régulières"
                ]
            },
            "541": {
                "nom": "Services professionnels, scientifiques et techniques",
                "risques_principaux": [
                    "troubles_musculosquelettiques", "fatigue_oculaire",
                    "stress_psychosocial", "ergonomie_bureau"
                ],
                "normes_specifiques": ["CSA_Z1000"],
                "exigences_particulieres": [
                    "Évaluation postes travail",
                    "Programmes pause écran",
                    "Gestion charge travail"
                ]
            }
        }
    
    def _charger_normes_csa(self) -> Dict:
        """Charge les normes CSA canadiennes"""
        return {
            "Z1000": {
                "titre": "Gestion de la santé et sécurité au travail",
                "domaines": ["management", "consultation", "evaluation_risques"],
                "complement_iso": "Adaptation canadienne ISO 45001"
            },
            "Z1002": {
                "titre": "Santé et sécurité au travail - Exigences pour les systèmes de management",
                "domaines": ["systeme_management", "amelioration_continue"],
                "complement_iso": "Spécifications techniques précises"
            },
            "Z1003": {
                "titre": "Gestion des risques psychosociaux au travail",
                "domaines": ["psychosocial", "violence", "harcelement"],
                "complement_iso": "Addendum spécialisé"
            },
            "Z45001": {
                "titre": "Workplace psychological health and safety",
                "domaines": ["sante_mentale", "bien_etre", "prevention"],
                "complement_iso": "Extension santé psychologique"
            }
        }
    
    def _charger_categories_cnesst(self) -> Dict:
        """Charge les catégories d'incidents CNESST"""
        return {
            "accidents_travail": {
                "categories": [
                    "chutes_glissades", "contact_objets", "surmenage",
                    "exposition_substances", "violence_agression"
                ],
                "codes_lesion": ["10-19", "20-29", "30-39", "40-49", "50-59"]
            },
            "maladies_professionnelles": {
                "categories": [
                    "troubles_musculosquelettiques", "maladies_respiratoires",
                    "dermatoses", "pertes_auditives", "troubles_psychiques"
                ],
                "codes_lesion": ["60-69", "70-79", "80-89", "90-99"]
            },
            "prevention": {
                "mesures": [
                    "formation_sensibilisation", "equipements_protection",
                    "procedures_securite", "surveillance_sante", "amenagement_postes"
                ]
            }
        }

# ═══════════════════════════════════════════════════════════════
# MOTEUR DE RECHERCHE SÉMANTIQUE
# ═══════════════════════════════════════════════════════════════

    def vectoriser_corpus_normatif(self):
        """Vectorise l'ensemble du corpus normatif pour recherche sémantique"""
        corpus_elements = []
        
        # Vectorisation ISO 45001
        for section_id, section_data in self.normes_iso_45001.items():
            for sous_section, description in section_data["sections"].items():
                element = {
                    "type": "iso_45001",
                    "section": section_id,
                    "sous_section": sous_section,
                    "texte": description,
                    "mots_cles": section_data["mots_cles"],
                    "poids": 1.0
                }
                corpus_elements.append(element)
        
        # Vectorisation SCIAN
        for code, secteur_data in self.secteurs_scian.items():
            for risque in secteur_data["risques_principaux"]:
                element = {
                    "type": "scian_risque",
                    "secteur": code,
                    "secteur_nom": secteur_data["nom"],
                    "texte": risque.replace("_", " "),
                    "mots_cles": [risque],
                    "poids": 0.8
                }
                corpus_elements.append(element)
        
        # Vectorisation CSA
        for norme_id, norme_data in self.normes_csa.items():
            element = {
                "type": "csa",
                "norme": norme_id,
                "texte": norme_data["titre"],
                "mots_cles": norme_data["domaines"],
                "poids": 0.9
            }
            corpus_elements.append(element)
        
        self.corpus_vectorise = corpus_elements
        self._construire_index_semantique()
        
        self.logger.info(f"✅ Corpus vectorisé: {len(corpus_elements)} éléments")
        return corpus_elements
    
    def _construire_index_semantique(self):
        """Construit l'index sémantique pour recherche rapide"""
        if not self.corpus_vectorise:
            return
            
        # Index par mots-clés
        for idx, element in enumerate(self.corpus_vectorise):
            for mot_cle in element["mots_cles"]:
                if mot_cle not in self.index_semantique:
                    self.index_semantique[mot_cle] = []
                self.index_semantique[mot_cle].append(idx)
        
        # Index par type
        self.index_par_type = {}
        for idx, element in enumerate(self.corpus_vectorise):
            type_elem = element["type"]
            if type_elem not in self.index_par_type:
                self.index_par_type[type_elem] = []
            self.index_par_type[type_elem].append(idx)

    def rechercher_normes_applicables(self, contexte_analyse: str, secteur_scian: str = None) -> List[RecommandationNormative]:
        """Recherche les normes applicables selon le contexte"""
        if not self.corpus_vectorise:
            self.vectoriser_corpus_normatif()
        
        # Analyse du contexte pour extraire mots-clés
        mots_cles_contexte = self._extraire_mots_cles(contexte_analyse.lower())
        
        # Recherche par similarité sémantique
        resultats_bruts = []
        for mot_cle in mots_cles_contexte:
            if mot_cle in self.index_semantique:
                for idx in self.index_semantique[mot_cle]:
                    element = self.corpus_vectorise[idx]
                    score = self._calculer_score_pertinence(element, mots_cles_contexte, secteur_scian)
                    resultats_bruts.append((element, score))
        
        # Tri par pertinence et génération recommandations
        resultats_bruts.sort(key=lambda x: x[1], reverse=True)
        
        recommandations = []
        for element, score in resultats_bruts[:10]:  # Top 10
            if score > 0.3:  # Seuil de pertinence
                recommandation = self._generer_recommandation(element, score, secteur_scian)
                if recommandation:
                    recommandations.append(recommandation)
        
        return recommandations
    
    def _extraire_mots_cles(self, texte: str) -> List[str]:
        """Extrait les mots-clés pertinents du texte d'analyse"""
        # Mots-clés HSE prioritaires
        mots_cles_hse = [
            "formation", "securite", "risque", "accident", "incident", "prevention",
            "equipement", "protection", "procedure", "evaluation", "surveillance",
            "amelioration", "conformite", "audit", "inspection", "maintenance",
            "communication", "consultation", "participation", "leadership",
            "competence", "sensibilisation", "urgence", "planification"
        ]
        
        mots_trouves = []
        for mot in mots_cles_hse:
            if mot in texte:
                mots_trouves.append(mot)
        
        # Ajout mots-clés sectoriels si SCIAN détecté
        if any(secteur in texte for secteur in ["construction", "fabrication", "transport"]):
            mots_trouves.extend(["secteur", "industrie", "specifique"])
        
        return list(set(mots_trouves))  # Suppression doublons
    
    def _calculer_score_pertinence(self, element: Dict, mots_cles_contexte: List[str], secteur_scian: str = None) -> float:
        """Calcule le score de pertinence d'un élément normatif"""
        score = 0.0
        
        # Score base sur mots-clés
        mots_element = element["mots_cles"]
        intersection = set(mots_cles_contexte) & set(mots_element)
        if mots_element:
            score += len(intersection) / len(mots_element) * element["poids"]
        
        # Bonus secteur SCIAN
        if secteur_scian and element["type"] == "scian_risque":
            if element.get("secteur") == secteur_scian:
                score += 0.5
        
        # Bonus ISO 45001 (toujours pertinent)
        if element["type"] == "iso_45001":
            score += 0.2
        
        return min(score, 1.0)  # Cap à 1.0
    
    def _generer_recommandation(self, element: Dict, score: float, secteur_scian: str = None) -> Optional[RecommandationNormative]:
        """Génère une recommandation normative structurée"""
        if element["type"] == "iso_45001":
            return self._generer_recommandation_iso(element, score)
        elif element["type"] == "scian_risque":
            return self._generer_recommandation_scian(element, score, secteur_scian)
        elif element["type"] == "csa":
            return self._generer_recommandation_csa(element, score)
        
        return None
    
    def _generer_recommandation_iso(self, element: Dict, score: float) -> RecommandationNormative:
        """Génère recommandation basée sur ISO 45001"""
        section = element["section"]
        sous_section = element["sous_section"]
        
        # Actions concrètes par section ISO
        actions_iso = {
            "4_contexte": [
                "Réaliser analyse du contexte organisationnel",
                "Identifier parties intéressées pertinentes",
                "Définir domaine d'application SST"
            ],
            "5_leadership": [
                "Établir politique SST claire",
                "Définir rôles et responsabilités",
                "Mettre en place consultation travailleurs"
            ],
            "6_planification": [
                "Conduire évaluation des risques",
                "Établir objectifs SST mesurables",
                "Planifier actions préventives"
            ],
            "7_support": [
                "Assurer ressources suffisantes",
                "Développer compétences équipes",
                "Améliorer communication SST"
            ],
            "8_realisation": [
                "Implémenter contrôles opérationnels",
                "Préparer réponse situations urgence",
                "Maintenir surveillance continue"
            ],
            "9_evaluation": [
                "Effectuer audits internes réguliers",
                "Mesurer performance SST",
                "Réviser système management"
            ],
            "10_amelioration": [
                "Traiter non-conformités rapidement",
                "Implémenter amélioration continue",
                "Analyser incidents préventive"
            ]
        }
        
        return RecommandationNormative(
            titre=f"ISO 45001 - {self.normes_iso_45001[section]['titre']}",
            description=element["texte"],
            norme_source="ISO 45001:2018",
            section_iso=sous_section,
            secteur_scian="Universel",
            niveau_priorite=max(1, int(score * 5)),
            actions_concretes=actions_iso.get(section, ["Consulter norme complète"]),
            references=[f"ISO 45001:2018 - Section {sous_section}"],
            conformite_score=score
        )
    
    def _generer_recommandation_scian(self, element: Dict, score: float, secteur_scian: str) -> RecommandationNormative:
        """Génère recommandation basée sur secteur SCIAN"""
        secteur_info = self.secteurs_scian[element["secteur"]]
        risque = element["texte"]
        
        # Actions spécifiques par risque
        actions_risques = {
            "chutes hauteur": [
                "Installer systèmes protection collective",
                "Former personnel travail hauteur",
                "Inspecter équipements protection individuelle"
            ],
            "troubles musculosquelettiques": [
                "Analyser postes de travail ergonomiques",
                "Former techniques manutention",
                "Implémenter pauses régulières"
            ],
            "exposition substances": [
                "Évaluer exposition professionnelle",
                "Installer ventilation adéquate",
                "Fournir équipements protection respiratoire"
            ]
        }
        
        actions = actions_risques.get(risque, [
            f"Évaluer risques spécifiques {risque}",
            "Implémenter mesures préventives",
            "Former personnel concerné"
        ])
        
        return RecommandationNormative(
            titre=f"Prévention {risque} - Secteur {secteur_info['nom']}",
            description=f"Mesures préventives pour {risque} dans secteur {secteur_info['nom']}",
            norme_source=f"SCIAN {element['secteur']}",
            section_iso="Spécifique secteur",
            secteur_scian=element["secteur"],
            niveau_priorite=max(2, int(score * 5)),
            actions_concretes=actions,
            references=[f"Guide sectoriel SCIAN {element['secteur']}"] + secteur_info["normes_specifiques"],
            conformite_score=score
        )
    
    def _generer_recommandation_csa(self, element: Dict, score: float) -> RecommandationNormative:
        """Génère recommandation basée sur norme CSA"""
        norme_info = self.normes_csa[element["norme"]]
        
        return RecommandationNormative(
            titre=f"CSA {element['norme']} - {norme_info['titre']}",
            description=norme_info["complement_iso"],
            norme_source=f"CSA {element['norme']}",
            section_iso="Complément canadien",
            secteur_scian="Canada",
            niveau_priorite=max(1, int(score * 4)),
            actions_concretes=[
                f"Consulter norme CSA {element['norme']}",
                "Adapter exigences contexte canadien",
                "Valider conformité réglementaire"
            ],
            references=[f"CSA {element['norme']}", "Réglementation provinciale"],
            conformite_score=score
        )

# ═══════════════════════════════════════════════════════════════
# FONCTIONS D'INTERFACE POUR SAFETYGRAPH
# ═══════════════════════════════════════════════════════════════

def initialiser_moteur_vectorisation() -> MoteurVectorisationNormes:
    """Initialise et retourne le moteur de vectorisation"""
    moteur = MoteurVectorisationNormes()
    moteur.vectoriser_corpus_normatif()
    return moteur

def rechercher_normes_applicables(moteur: MoteurVectorisationNormes, contexte: str, secteur: str = None) -> List[Dict]:
    """Interface simplifiée pour SafetyGraph"""
    recommandations = moteur.rechercher_normes_applicables(contexte, secteur)
    
    # Conversion en dictionnaires pour compatibilité
    resultats = []
    for rec in recommandations:
        resultats.append({
            "titre": rec.titre,
            "description": rec.description,
            "norme_source": rec.norme_source,
            "section_iso": rec.section_iso,
            "secteur_scian": rec.secteur_scian,
            "niveau_priorite": rec.niveau_priorite,
            "actions_concretes": rec.actions_concretes,
            "references": rec.references,
            "conformite_score": rec.conformite_score
        })
    
    return resultats

def obtenir_statistiques_corpus(moteur: MoteurVectorisationNormes) -> Dict:
    """Retourne statistiques du corpus normatif"""
    if not moteur.corpus_vectorise:
        return {"erreur": "Corpus non initialisé"}
    
    stats = {
        "total_elements": len(moteur.corpus_vectorise),
        "elements_iso": len(moteur.index_par_type.get("iso_45001", [])),
        "elements_scian": len(moteur.index_par_type.get("scian_risque", [])),
        "elements_csa": len(moteur.index_par_type.get("csa", [])),
        "mots_cles_indexes": len(moteur.index_semantique),
        "secteurs_scian_couverts": len(moteur.secteurs_scian)
    }
    
    return stats

# ═══════════════════════════════════════════════════════════════
# TEST ET VALIDATION
# ═══════════════════════════════════════════════════════════════

def test_vectorisation_normes():
    """Test complet du système de vectorisation"""
    
    print("🧪 TEST VECTORISATION NORMES ISO/SCIAN")
    print("=" * 50)
    
    # Initialisation
    print("📦 Initialisation moteur...")
    moteur = initialiser_moteur_vectorisation()
    
    # Statistiques
    stats = obtenir_statistiques_corpus(moteur)
    print(f"📊 Corpus: {stats['total_elements']} éléments")
    print(f"   - ISO 45001: {stats['elements_iso']} sections")
    print(f"   - SCIAN: {stats['elements_scian']} risques")
    print(f"   - CSA: {stats['elements_csa']} normes")
    
    # Tests recherche
    contextes_test = [
        ("formation sécurité construction", "236"),
        ("accident travail équipement protection", None),
        ("amélioration continue surveillance", None),
        ("troubles musculosquelettiques fabrication", "311-333")
    ]
    
    for contexte, secteur in contextes_test:
        print(f"\n🔍 Test: '{contexte}' (secteur: {secteur or 'Auto'})")
        recommandations = rechercher_normes_applicables(moteur, contexte, secteur)
        
        print(f"   📋 {len(recommandations)} recommandations trouvées")
        for i, rec in enumerate(recommandations[:3], 1):
            print(f"   {i}. {rec['titre']} (Score: {rec['conformite_score']:.2f})")
    
    print(f"\n✅ Tests terminés avec succès!")
    return True

if __name__ == "__main__":
    # Exécution des tests si lancé directement
    test_vectorisation_normes()