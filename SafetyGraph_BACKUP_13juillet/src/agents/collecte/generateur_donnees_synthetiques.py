# Générateur Données Synthétiques A2 - SafetyAgentic (VERSION CORRIGÉE)
# =====================================================================
# Génère des observations terrain réalistes basées sur statistiques CNESST

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import logging
from dataclasses import dataclass
from enum import Enum
import random

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SafetyAgentic.SyntheticGenerator")

class SecteurActivite(Enum):
    """Secteurs d'activité basés données CNESST"""
    CONSTRUCTION = "CONSTRUCTION"
    SOINS_SANTE = "SOINS_SANTE"
    FABRICATION = "FABRICATION"
    TRANSPORT = "TRANSPORT"
    SERVICES = "SERVICES"
    AUTRE = "AUTRE"

class TypeIncident(Enum):
    """Types d'incidents basés données CNESST"""
    CHUTE_HAUTEUR = "CHUTE_DE_HAUTEUR"
    CHUTE_NIVEAU = "CHUTE_AU_MEME_NIVEAU"
    FRAPPE_OBJET = "FRAPPE_PAR_UN_OBJET"
    EFFORT_EXCESSIF = "EFFORT_EXCESSIF"
    CONTACT_OBJET = "CONTACT_AVEC_OBJET"
    AUTRE = "AUTRE"

@dataclass
class ProfileSecteur:
    """Profil statistique d'un secteur basé données CNESST"""
    nom: str
    variables_base: Dict[str, float]
    dangers_typiques: List[str]
    epi_obligatoires: List[str]
    entreprises_type: List[str]
    incidents_frequents: List[str]
    facteurs_risque: Dict[str, float]

class GenerateurDonneesSynthetiques:
    """
    Générateur de données synthétiques d'observations terrain A2
    Basé sur les statistiques réelles des 793K incidents CNESST
    """
    
    def __init__(self, seed: Optional[int] = None):
        """Initialisation du générateur"""
        if seed:
            np.random.seed(seed)
            random.seed(seed)
        
        self.seed = seed
        self.profiles_secteurs = self._init_profiles_secteurs()
        self.distributions_qualite = self._init_distributions_qualite()
        
        logger.info("🔬 Générateur données synthétiques initialisé")
    
    def _init_profiles_secteurs(self) -> Dict[SecteurActivite, ProfileSecteur]:
        """Initialisation profils secteurs basés statistiques CNESST"""
        
        return {
            SecteurActivite.CONSTRUCTION: ProfileSecteur(
                nom="Construction",
                variables_base={
                    "usage_epi": 6.2,
                    "respect_procedures": 5.8,
                    "formation_securite": 6.5,
                    "supervision_directe": 5.5,
                    "communication_risques": 6.0,
                    "leadership_sst": 5.9
                },
                dangers_typiques=["hauteur", "chute_materiel", "machines_construction", "electrique"],
                epi_obligatoires=["casque", "chaussures_securite", "gants", "harnais"],
                entreprises_type=[
                    "Bâtiments XYZ Ltée", "Construction ABC Inc.", "Rénovations Pro",
                    "Toiture Expert", "Maçonnerie Plus", "Électricité Moderne"
                ],
                incidents_frequents=["chute_hauteur", "frappe_objet", "contact_electrique"],
                facteurs_risque={"hauteur": 0.8, "machines": 0.6, "materiel_lourd": 0.7}
            ),
            
            SecteurActivite.FABRICATION: ProfileSecteur(
                nom="Fabrication",
                variables_base={
                    "usage_epi": 7.1,
                    "respect_procedures": 6.8,
                    "formation_securite": 7.2,
                    "supervision_directe": 6.5,
                    "communication_risques": 6.9,
                    "leadership_sst": 6.7
                },
                dangers_typiques=["machines", "produits_chimiques", "bruit", "ergonomie"],
                epi_obligatoires=["lunettes", "gants", "protection_auditive", "chaussures_securite"],
                entreprises_type=[
                    "Usine Métal Plus", "Fabrication Québec", "Plastiques Industriels",
                    "Textiles Modernes", "Alimentaire Pro", "Chimie Avancée"
                ],
                incidents_frequents=["contact_machine", "exposition_chimique", "effort_excessif"],
                facteurs_risque={"machines": 0.9, "chimique": 0.7, "bruit": 0.6}
            ),
            
            SecteurActivite.SOINS_SANTE: ProfileSecteur(
                nom="Soins de santé",
                variables_base={
                    "usage_epi": 8.2,
                    "respect_procedures": 8.0,
                    "formation_securite": 8.5,
                    "supervision_directe": 7.8,
                    "communication_risques": 8.1,
                    "leadership_sst": 7.9
                },
                dangers_typiques=["biologique", "ergonomie", "stress", "violence"],
                epi_obligatoires=["gants", "masques", "blouses", "lunettes"],
                entreprises_type=[
                    "Hôpital Général", "CLSC Ville", "Clinique Santé+",
                    "CHSLD Résidence", "Laboratoire Bio", "Pharmacie Plus"
                ],
                incidents_frequents=["effort_excessif", "exposition_biologique", "stress"],
                facteurs_risque={"biologique": 0.8, "ergonomie": 0.9, "stress": 0.7}
            ),
            
            SecteurActivite.TRANSPORT: ProfileSecteur(
                nom="Transport",
                variables_base={
                    "usage_epi": 6.8,
                    "respect_procedures": 6.2,
                    "formation_securite": 6.9,
                    "supervision_directe": 5.8,
                    "communication_risques": 6.3,
                    "leadership_sst": 6.1
                },
                dangers_typiques=["vehicules", "manutention", "fatigue", "routes"],
                epi_obligatoires=["casque", "gilet_haute_visibilite", "chaussures_securite", "gants"],
                entreprises_type=[
                    "Transport Québec", "Livraisons Express", "Autobus Metro",
                    "Camionnage Pro", "Logistics Plus", "Déménagement Rapide"
                ],
                incidents_frequents=["effort_excessif", "contact_vehicule", "chute_niveau"],
                facteurs_risque={"vehicules": 0.8, "manutention": 0.7, "fatigue": 0.6}
            ),
            
            SecteurActivite.SERVICES: ProfileSecteur(
                nom="Services",
                variables_base={
                    "usage_epi": 6.5,
                    "respect_procedures": 6.8,
                    "formation_securite": 7.0,
                    "supervision_directe": 6.9,
                    "communication_risques": 7.2,
                    "leadership_sst": 7.1
                },
                dangers_typiques=["ergonomie", "stress", "glissades", "bureautique"],
                epi_obligatoires=["chaussures_antiderapantes", "support_ergonomique"],
                entreprises_type=[
                    "Services Ville", "Bureau Conseil", "Nettoyage Pro",
                    "Sécurité Plus", "Informatique Inc", "Restaurant Central"
                ],
                incidents_frequents=["chute_niveau", "effort_excessif", "stress"],
                facteurs_risque={"ergonomie": 0.7, "stress": 0.8, "glissades": 0.5}
            ),
            
            SecteurActivite.AUTRE: ProfileSecteur(
                nom="Autre",
                variables_base={
                    "usage_epi": 6.0,
                    "respect_procedures": 6.0,
                    "formation_securite": 6.2,
                    "supervision_directe": 6.0,
                    "communication_risques": 6.1,
                    "leadership_sst": 6.0
                },
                dangers_typiques=["divers", "ergonomie", "stress"],
                epi_obligatoires=["gants", "chaussures_securite"],
                entreprises_type=[
                    "Entreprise Générale", "Services Divers", "Multi-Secteurs Inc"
                ],
                incidents_frequents=["effort_excessif", "chute_niveau"],
                facteurs_risque={"divers": 0.5}
            )
        }
    
    def _init_distributions_qualite(self) -> Dict[str, Dict]:
        """Distributions qualité culture selon secteur"""
        return {
            "excellente": {
                "multiplicateur": 1.4,
                "variance": 0.2,
                "conformite_base": 85
            },
            "bonne": {
                "multiplicateur": 1.2,
                "variance": 0.3,
                "conformite_base": 70
            },
            "moyenne": {
                "multiplicateur": 1.0,
                "variance": 0.4,
                "conformite_base": 55
            },
            "faible": {
                "multiplicateur": 0.7,
                "variance": 0.6,
                "conformite_base": 35
            }
        }
    
    def generate_observation_synthetique(
        self,
        secteur: Optional[SecteurActivite] = None,
        type_incident: Optional[TypeIncident] = None,
        qualite_culture: Optional[str] = None,
        nb_travailleurs: Optional[int] = None,
        duree_observation: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Génère une observation terrain synthétique
        
        Args:
            secteur: Secteur d'activité (aléatoire si None)
            type_incident: Type incident analysé (aléatoire si None)
            qualite_culture: Qualité culture ("excellente", "bonne", "moyenne", "faible")
            nb_travailleurs: Nombre de travailleurs observés
            duree_observation: Durée observation en heures
            
        Returns:
            Dict avec observation synthétique complète
        """
        
        # Sélection aléatoire des paramètres manquants
        if secteur is None:
            secteur = np.random.choice(list(SecteurActivite))
        
        if type_incident is None:
            type_incident = np.random.choice(list(TypeIncident))
        
        if qualite_culture is None:
            qualite_culture = np.random.choice(
                ["excellente", "bonne", "moyenne", "faible"],
                p=[0.15, 0.35, 0.35, 0.15]  # Distribution réaliste
            )
        
        if nb_travailleurs is None:
            nb_travailleurs = np.random.randint(2, 12)
        
        if duree_observation is None:
            duree_observation = np.random.uniform(0.5, 4.0)
        
        # Récupération profil secteur
        profil = self.profiles_secteurs[secteur]
        distribution = self.distributions_qualite[qualite_culture]
        
        # Génération variables culture avec ajustement qualité
        variables_culture = {}
        for var, score_base in profil.variables_base.items():
            # Application multiplicateur qualité culture
            score_ajuste = score_base * distribution["multiplicateur"]
            
            # Ajout variance réaliste
            variance = distribution["variance"]
            score_final = np.random.normal(score_ajuste, variance)
            
            # Contrainte 1-10
            score_final = max(1, min(10, score_final))
            variables_culture[var] = int(round(score_final))
        
        # Sélection entreprise du secteur
        entreprises_secteur = profil.entreprises_type
        if entreprises_secteur:  # CORRECTION: Vérification liste non vide
            entreprise = np.random.choice(entreprises_secteur)
        else:
            entreprise = f"Entreprise {secteur.value}"
        
        # Génération dangers détectés
        dangers_detectes = self._generer_dangers(profil, qualite_culture)
        
        # Génération conformité EPI
        conformite_epi = self._generer_conformite_epi(profil, distribution, nb_travailleurs)
        
        # Contexte observation
        contexte = {
            "secteur_activite": secteur.value,
            "type_incident_base": type_incident.value,
            "nb_travailleurs_observes": nb_travailleurs,
            "duree_observation": duree_observation,
            "conditions_meteo": np.random.choice(["ensoleille", "nuageux", "pluvieux"], p=[0.5, 0.3, 0.2]),
            "periode_jour": np.random.choice(["matin", "apres_midi", "soir"], p=[0.4, 0.5, 0.1]),
            "entreprise": entreprise
        }
        
        # Méta-information génération
        meta_generation = {
            "seed_utilise": self.seed,
            "timestamp_generation": datetime.now().isoformat(),
            "qualite_culture_cible": qualite_culture,
            "secteur_base": secteur.value,
            "type_incident_base": type_incident.value,
            "distribution_appliquee": distribution
        }
        
        return {
            "variables_culture": variables_culture,
            "conformite": conformite_epi,
            "contexte": contexte,
            "meta_generation": meta_generation
        }
    
    def _generer_dangers(self, profil: ProfileSecteur, qualite_culture: str) -> List[str]:
        """Génère les dangers détectés selon profil secteur et qualité culture"""
        
        # Nombre dangers selon qualité culture
        if qualite_culture == "excellente":
            nb_dangers = np.random.randint(0, 2)
        elif qualite_culture == "bonne":
            nb_dangers = np.random.randint(1, 3)
        elif qualite_culture == "moyenne":
            nb_dangers = np.random.randint(2, 4)
        else:  # faible
            nb_dangers = np.random.randint(3, 6)
        
        # Sélection aléatoire des dangers du secteur
        dangers_disponibles = profil.dangers_typiques
        if nb_dangers >= len(dangers_disponibles):
            return dangers_disponibles
        else:
            return list(np.random.choice(dangers_disponibles, nb_dangers, replace=False))
    
    def _generer_conformite_epi(
        self, 
        profil: ProfileSecteur, 
        distribution: Dict, 
        nb_travailleurs: int
    ) -> Dict[str, Any]:
        """Génère données conformité EPI"""
        
        epi_types = profil.epi_obligatoires
        conformite_base = distribution["conformite_base"]
        
        # Nombre EPI analysés (peut être < nb_travailleurs si pas tous observés)
        epi_analyses = min(nb_travailleurs, np.random.randint(1, nb_travailleurs + 1))
        
        # Calcul conformes selon qualité culture
        taux_conformite = conformite_base + np.random.normal(0, 10)
        taux_conformite = max(0, min(100, taux_conformite)) / 100
        
        epi_conformes = int(epi_analyses * taux_conformite)
        
        return {
            "epi_types": epi_types,
            "epi_analyses": epi_analyses,
            "epi_conformes": epi_conformes,
            "taux_conformite": epi_conformes / max(epi_analyses, 1) * 100,
            "dangers": self._generer_dangers(profil, 
                self._get_qualite_from_conformite(taux_conformite * 100))
        }
    
    def _get_qualite_from_conformite(self, taux: float) -> str:
        """Détermine qualité culture selon taux conformité"""
        if taux >= 80:
            return "excellente"
        elif taux >= 65:
            return "bonne"
        elif taux >= 45:
            return "moyenne"
        else:
            return "faible"
    
    def generer_batch_observations(
        self,
        nombre: int,
        secteur_filtre: Optional[SecteurActivite] = None,
        qualite_distribution: Optional[Dict[str, float]] = None
    ) -> List[Dict[str, Any]]:
        """
        Génère un batch d'observations synthétiques
        
        Args:
            nombre: Nombre d'observations à générer
            secteur_filtre: Secteur spécifique (None = tous secteurs)
            qualite_distribution: Distribution qualité personnalisée
        
        Returns:
            Liste d'observations synthétiques
        """
        
        logger.info(f"🔄 Génération {nombre} observations synthétiques...")
        
        if qualite_distribution is None:
            qualite_distribution = {
                "excellente": 0.15,
                "bonne": 0.35,
                "moyenne": 0.35,
                "faible": 0.15
            }
        
        observations = []
        
        for i in range(nombre):
            # Sélection qualité selon distribution
            qualite = np.random.choice(
                list(qualite_distribution.keys()),
                p=list(qualite_distribution.values())
            )
            
            # Génération observation
            obs = self.generate_observation_synthetique(
                secteur=secteur_filtre,
                qualite_culture=qualite
            )
            
            # Ajout ID unique
            obs["id_observation"] = f"SYNTH_{datetime.now().strftime('%Y%m%d')}_{i+1:04d}"
            
            observations.append(obs)
        
        logger.info(f"✅ {nombre} observations générées")
        return observations
    
    def analyser_statistiques_batch(self, observations: List[Dict]) -> Dict[str, Any]:
        """Analyse statistiques d'un batch d'observations"""
        
        if not observations:
            return {"erreur": "Aucune observation à analyser"}
        
        # Extraction données
        secteurs = [obs["contexte"]["secteur_activite"] for obs in observations]
        qualites = [obs["meta_generation"]["qualite_culture_cible"] for obs in observations]
        
        variables_moyennes = {}
        all_variables = observations[0]["variables_culture"].keys()
        
        for var in all_variables:
            scores = [obs["variables_culture"][var] for obs in observations]
            variables_moyennes[var] = {
                "moyenne": np.mean(scores),
                "mediane": np.median(scores),
                "ecart_type": np.std(scores),
                "min": np.min(scores),
                "max": np.max(scores)
            }
        
        return {
            "nombre_observations": len(observations),
            "distribution_secteurs": {s: secteurs.count(s) for s in set(secteurs)},
            "distribution_qualites": {q: qualites.count(q) for q in set(qualites)},
            "variables_statistiques": variables_moyennes,
            "score_culture_moyen": np.mean([
                np.mean(list(obs["variables_culture"].values())) 
                for obs in observations
            ]),
            "conformite_epi_moyenne": np.mean([
                obs["conformite"]["taux_conformite"] 
                for obs in observations
            ])
        }


def demo_generateur():
    """Démonstration du générateur synthétique"""
    
    print("🔬 DÉMONSTRATION GÉNÉRATEUR DONNÉES SYNTHÉTIQUES")
    print("=" * 55)
    
    # Initialisation générateur
    generateur = GenerateurDonneesSynthetiques(seed=42)
    
    # 1. Génération observation unique
    print("\n1️⃣ GÉNÉRATION OBSERVATION UNIQUE")
    print("-" * 35)
    
    obs_unique = generateur.generate_observation_synthetique(
        secteur=SecteurActivite.CONSTRUCTION,
        qualite_culture="moyenne"
    )
    
    print(f"Secteur: {obs_unique['contexte']['secteur_activite']}")
    print(f"Entreprise: {obs_unique['contexte']['entreprise']}")
    print(f"Score culture moyen: {np.mean(list(obs_unique['variables_culture'].values())):.1f}/10")
    print(f"Conformité EPI: {obs_unique['conformite']['epi_conformes']}/{obs_unique['conformite']['epi_analyses']}")
    print(f"Dangers détectés: {obs_unique['conformite']['dangers']}")
    
    # 2. Génération batch
    print("\n2️⃣ GÉNÉRATION BATCH (20 OBSERVATIONS)")
    print("-" * 40)
    
    batch_obs = generateur.generer_batch_observations(20)
    stats = generateur.analyser_statistiques_batch(batch_obs)
    
    print(f"📊 Observations générées: {stats['nombre_observations']}")
    print(f"🏢 Secteurs: {list(stats['distribution_secteurs'].keys())}")
    print(f"📈 Score culture moyen: {stats['score_culture_moyen']:.1f}/10")
    print(f"🛡️ Conformité EPI moyenne: {stats['conformite_epi_moyenne']:.1f}%")
    
    # 3. Test par secteur
    print("\n3️⃣ TEST PAR SECTEUR")
    print("-" * 20)
    
    for secteur in [SecteurActivite.CONSTRUCTION, SecteurActivite.SOINS_SANTE, SecteurActivite.FABRICATION]:
        obs_secteur = generateur.generate_observation_synthetique(
            secteur=secteur,
            qualite_culture="bonne"
        )
        score_moyen = np.mean(list(obs_secteur['variables_culture'].values()))
        print(f"🏢 {secteur.value}: {score_moyen:.1f}/10 culture, {len(obs_secteur['conformite']['dangers'])} dangers")
    
    # 4. Test qualités culture
    print("\n4️⃣ TEST QUALITÉS CULTURE")
    print("-" * 25)
    
    for qualite in ["excellente", "bonne", "moyenne", "faible"]:
        obs_qualite = generateur.generate_observation_synthetique(
            secteur=SecteurActivite.CONSTRUCTION,
            qualite_culture=qualite
        )
        score_moyen = np.mean(list(obs_qualite['variables_culture'].values()))
        conformite = obs_qualite['conformite']['taux_conformite']
        print(f"🎯 {qualite.upper()}: {score_moyen:.1f}/10 culture, {conformite:.1f}% conformité")
    
    print(f"\n✅ DÉMONSTRATION TERMINÉE")
    print(f"🔬 Générateur validé avec seed {generateur.seed}")
    
    return batch_obs

if __name__ == "__main__":
    observations_demo = demo_generateur()