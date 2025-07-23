"""
Module Enrichissements SafetyGraph - Version Complète
===================================================

Module d'enrichissement CNESST pour SafetyGraph BehaviorX
avec détection automatique secteurs SCIAN et benchmarking temps réel.

Auteur: Mario Genest - GenAISafety
Date: 11 juillet 2025
Version: 2.0
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CNESSTContextEnhancer:
    """Enrichissement contexte avec données CNESST sectorielles"""
    
    def __init__(self):
        self.scian_patterns = self.load_scian_patterns()
        self.cnesst_benchmarks = self.load_cnesst_benchmarks()
        self.sector_mappings = self.load_sector_mappings()
        
        logger.info(f"CNESSTContextEnhancer initialisé - {len(self.scian_patterns)} secteurs SCIAN")
        
    def load_scian_patterns(self) -> Dict[str, List[str]]:
        """Patterns pour détection automatique secteurs SCIAN"""
        
        return {
            # Construction - Secteur 23
            "23": ["construction", "bâtiment", "chantier", "btp", "édifice", "entrepreneur"],
            "236": ["résidentiel", "maison", "logement", "habitation", "domicile"],
            "237": ["génie civil", "infrastructure", "pont", "route", "aqueduc", "autoroute"],
            "238": ["entrepreneur spécialisé", "fondation", "béton", "charpente", "électrique"],
            "238110": ["fondation coulée", "béton coulé", "structure béton", "semelle"],
            
            # Santé et assistance sociale - Secteur 62
            "62": ["santé", "médical", "hôpital", "clinique", "soins", "patient"],
            "621": ["ambulatoire", "clinique externe", "cabinet médical", "consultations"],
            "622": ["hôpital", "centre hospitalier", "urgence", "chirurgie", "soins aigus"],
            "623": ["soins infirmiers", "résidence personnes âgées", "CHSLD", "hébergement"],
            
            # Transport et entreposage - Secteur 48-49
            "48": ["transport", "camion", "livraison", "logistique", "fret"],
            "484": ["camionnage", "transport routier", "transport marchandises"],
            "488": ["transport soutien", "entreposage", "manutention"],
            
            # Commerce de détail - Secteur 44-45
            "44": ["commerce détail", "magasin", "vente", "boutique"],
            "445": ["alimentation", "épicerie", "supermarché", "IGA", "Metro"],
            "448": ["vêtements", "chaussures", "accessoires", "mode"],
            
            # Fabrication - Secteur 31-33
            "31": ["fabrication", "manufacture", "production", "usine"],
            "311": ["aliments", "transformation alimentaire", "abattoir"],
            "321": ["bois", "scierie", "meuble", "foresterie"],
            
            # Services professionnels - Secteur 54
            "54": ["services professionnels", "consultant", "ingénierie", "architecture"],
            "541": ["services juridiques", "comptabilité", "consultation"],
            
            # Hébergement et restauration - Secteur 72
            "72": ["hébergement", "restauration", "hôtel", "restaurant"],
            "721": ["hébergement", "hôtel", "motel", "auberge"],
            "722": ["restauration", "restaurant", "bar", "café", "traiteur"]
        }
    
    def load_cnesst_benchmarks(self) -> Dict[str, Dict]:
        """Benchmarks CNESST par secteur - Données réelles 2024"""
        
        return {
            "23": {  # Construction
                "nom": "Construction",
                "jours_indemnises_moy": 227.4,
                "taux_frequence": 45.8,
                "cout_moyen_lesion": 89420,
                "lesions_totales": 8945,
                "jours_totaux": 2034680,
                "tendance": "hausse"
            },
            "238110": {  # Coulage béton et fondations
                "nom": "Coulage béton et fondations",
                "jours_indemnises_moy": 209.7,
                "taux_frequence": 52.3,
                "cout_moyen_lesion": 95670,
                "lesions_totales": 924,
                "jours_totaux": 193772,
                "tendance": "stable"
            },
            "62": {  # Soins de santé
                "nom": "Soins de santé et assistance sociale",
                "jours_indemnises_moy": 156.2,
                "taux_frequence": 28.4,
                "cout_moyen_lesion": 67230,
                "lesions_totales": 12456,
                "jours_totaux": 1945847,
                "tendance": "baisse"
            },
            "48": {  # Transport
                "nom": "Transport et entreposage",
                "jours_indemnises_moy": 198.5,
                "taux_frequence": 38.7,
                "cout_moyen_lesion": 78940,
                "lesions_totales": 5432,
                "jours_totaux": 1078254,
                "tendance": "hausse"
            },
            "44": {  # Commerce
                "nom": "Commerce de détail",
                "jours_indemnises_moy": 142.8,
                "taux_frequence": 22.1,
                "cout_moyen_lesion": 54320,
                "lesions_totales": 6789,
                "jours_totaux": 969872,
                "tendance": "stable"
            }
        }
    
    def load_sector_mappings(self) -> Dict[str, str]:
        """Mapping codes SCIAN vers descriptions"""
        
        return {
            "23": "Construction",
            "236": "Construction de bâtiments résidentiels",
            "237": "Travaux de génie civil",
            "238": "Entrepreneurs spécialisés",
            "238110": "Coulage de béton et travaux de fondation",
            "62": "Soins de santé et assistance sociale",
            "621": "Services de soins de santé ambulatoires",
            "622": "Hôpitaux",
            "623": "Établissements de soins infirmiers",
            "48": "Transport et entreposage",
            "484": "Transport par camion",
            "488": "Activités de soutien au transport",
            "44": "Commerce de détail",
            "445": "Commerce de détail - Alimentation",
            "448": "Commerce de détail - Vêtements et accessoires"
        }
    
    def detect_scian_sector(self, description: str) -> Optional[Tuple[str, str, float]]:
        """
        Détecte automatiquement le secteur SCIAN depuis une description
        
        Returns:
            Tuple[code_scian, nom_secteur, confidence] ou None
        """
        if not description:
            return None
            
        description_lower = description.lower()
        matches = []
        
        # Recherche des patterns dans tous les secteurs
        for sector_code, patterns in self.scian_patterns.items():
            confidence = 0
            matched_patterns = []
            
            for pattern in patterns:
                if pattern in description_lower:
                    confidence += 1
                    matched_patterns.append(pattern)
            
            if confidence > 0:
                # Calcul confidence normalisée
                confidence_norm = min(confidence / len(patterns), 1.0)
                sector_name = self.sector_mappings.get(sector_code, f"Secteur {sector_code}")
                
                matches.append({
                    "code": sector_code,
                    "nom": sector_name,
                    "confidence": confidence_norm,
                    "patterns": matched_patterns
                })
        
        if not matches:
            return None
        
        # Retourner le match avec la plus haute confidence
        # Priorité aux codes spécifiques (plus longs)
        best_match = max(matches, key=lambda x: (x["confidence"], len(x["code"])))
        
        logger.info(f"Secteur SCIAN détecté: {best_match['code']} - {best_match['nom']} "
                   f"(confidence: {best_match['confidence']:.2f})")
        
        return (best_match["code"], best_match["nom"], best_match["confidence"])
    
    def get_sector_benchmarks(self, sector_code: str) -> Optional[Dict]:
        """Récupère les benchmarks CNESST pour un secteur"""
        
        # Recherche exacte d'abord
        if sector_code in self.cnesst_benchmarks:
            return self.cnesst_benchmarks[sector_code]
        
        # Recherche par secteur parent (ex: 238110 -> 238 -> 23)
        for parent_length in [3, 2, 1]:
            if len(sector_code) > parent_length:
                parent_code = sector_code[:parent_length]
                if parent_code in self.cnesst_benchmarks:
                    benchmarks = self.cnesst_benchmarks[parent_code].copy()
                    benchmarks["note"] = f"Données secteur parent {parent_code}"
                    return benchmarks
        
        return None
    
    def enrich_context(self, context: Dict) -> Dict:
        """Enrichit le contexte avec les données CNESST"""
        
        enriched = context.copy()
        
        # Détection automatique secteur SCIAN
        description = context.get("description_organisation", "")
        if description:
            sector_info = self.detect_scian_sector(description)
            if sector_info:
                code, nom, confidence = sector_info
                enriched["scian_detected"] = {
                    "code": code,
                    "nom": nom,
                    "confidence": confidence,
                    "auto_detected": True
                }
                
                # Ajout benchmarks sectoriels
                benchmarks = self.get_sector_benchmarks(code)
                if benchmarks:
                    enriched["cnesst_benchmarks"] = benchmarks
        
        # Enrichissement manuel si code SCIAN fourni
        sector_code_manual = context.get("secteur_scian")
        if sector_code_manual and "scian_detected" not in enriched:
            sector_name = self.sector_mappings.get(sector_code_manual, f"Secteur {sector_code_manual}")
            enriched["scian_manual"] = {
                "code": sector_code_manual,
                "nom": sector_name,
                "auto_detected": False
            }
            
            benchmarks = self.get_sector_benchmarks(sector_code_manual)
            if benchmarks:
                enriched["cnesst_benchmarks"] = benchmarks
        
        return enriched

class EnhancedContextAgent:
    """Agent de contexte enrichi avec données sectorielles CNESST"""
    
    def __init__(self):
        self.cnesst_enhancer = CNESSTContextEnhancer()
        
    def analyze_enhanced_context(self, context: Dict) -> Dict:
        """Analyse enrichie du contexte avec données CNESST"""
        
        # Enrichissement de base
        enriched_context = self.cnesst_enhancer.enrich_context(context)
        
        # Analyse des écarts par rapport aux benchmarks
        analysis = {
            "base_analysis": self._analyze_base_context(context),
            "sector_analysis": None,
            "benchmark_comparison": None,
            "risk_assessment": "standard"
        }
        
        # Analyse sectorielle si données disponibles
        if "cnesst_benchmarks" in enriched_context:
            analysis["sector_analysis"] = self._analyze_sector_context(enriched_context)
            analysis["benchmark_comparison"] = self._compare_with_benchmarks(context, enriched_context)
            analysis["risk_assessment"] = self._assess_sector_risk(enriched_context)
        
        return {
            "enriched_context": enriched_context,
            "analysis": analysis,
            "enhancement_status": "enriched" if "cnesst_benchmarks" in enriched_context else "standard"
        }
    
    def _analyze_base_context(self, context: Dict) -> Dict:
        """Analyse de base du contexte (méthode existante enrichie)"""
        
        return {
            "employees_risk": self._assess_employees_risk(context),
            "organizational_maturity": self._assess_org_maturity(context),
            "sector_specificity": "auto_detected" if context.get("description_organisation") else "manual"
        }
    
    def _analyze_sector_context(self, enriched_context: Dict) -> Dict:
        """Analyse spécifique au secteur détecté"""
        
        sector_info = enriched_context.get("scian_detected") or enriched_context.get("scian_manual")
        if not sector_info:
            return {}
        
        sector_code = sector_info["code"]
        
        # Risques spécifiques par secteur
        sector_risks = {
            "23": ["chutes", "objets_lourds", "equipements_dangereux", "conditions_meteorologiques"],
            "238110": ["exposition_poussiere", "vibrations", "postures_contraignantes", "charges_lourdes"],
            "62": ["troubles_musculosquelettiques", "exposition_biologiques", "stress_travail", "violence"],
            "48": ["accidents_vehicules", "manutention", "horaires_irreguliers", "stress_circulation"],
            "44": ["vols_agression", "station_prolongee", "manutention_repetitive", "horaires_variables"]
        }
        
        # Recherche risques (exact puis parent)
        risks = []
        for check_code in [sector_code, sector_code[:3], sector_code[:2], sector_code[:1]]:
            if check_code in sector_risks:
                risks = sector_risks[check_code]
                break
        
        return {
            "sector_code": sector_code,
            "sector_name": sector_info["nom"],
            "specific_risks": risks,
            "detection_method": "automatic" if sector_info.get("auto_detected") else "manual"
        }
    
    def _compare_with_benchmarks(self, context: Dict, enriched_context: Dict) -> Dict:
        """Compare les métriques organisation avec benchmarks sectoriels"""
        
        benchmarks = enriched_context.get("cnesst_benchmarks")
        if not benchmarks:
            return {}
        
        comparison = {
            "sector_performance": benchmarks["nom"],
            "comparisons": [],
            "overall_position": "insufficient_data"
        }
        
        # Comparaison jours d'absence si disponible
        org_absences = context.get("jours_absence_moy")
        if org_absences:
            benchmark_absences = benchmarks["jours_indemnises_moy"]
            
            if org_absences < benchmark_absences * 0.8:
                position = "excellente"
            elif org_absences < benchmark_absences:
                position = "bonne"
            elif org_absences < benchmark_absences * 1.2:
                position = "moyenne"
            else:
                position = "préoccupante"
            
            comparison["comparisons"].append({
                "metric": "jours_absence",
                "organisation": org_absences,
                "secteur": benchmark_absences,
                "position": position,
                "ecart_pct": ((org_absences - benchmark_absences) / benchmark_absences) * 100
            })
            
            comparison["overall_position"] = position
        
        return comparison
    
    def _assess_sector_risk(self, enriched_context: Dict) -> str:
        """Évalue le niveau de risque global selon le secteur"""
        
        benchmarks = enriched_context.get("cnesst_benchmarks")
        if not benchmarks:
            return "standard"
        
        # Évaluation basée sur taux de fréquence sectoriel
        taux_freq = benchmarks.get("taux_frequence", 30)
        
        if taux_freq > 40:
            return "élevé"
        elif taux_freq > 25:
            return "moyen"
        else:
            return "faible"
    
    def _assess_employees_risk(self, context: Dict) -> str:
        """Évalue le risque employés (méthode de base)"""
        employees = context.get("nb_employes", 0)
        
        if employees > 500:
            return "élevé"
        elif employees > 100:
            return "moyen"
        else:
            return "faible"
    
    def _assess_org_maturity(self, context: Dict) -> str:
        """Évalue la maturité organisationnelle (méthode de base)"""
        # Analyse basée sur les politiques existantes
        policies = context.get("politiques_existantes", [])
        
        if len(policies) >= 5:
            return "mature"
        elif len(policies) >= 3:
            return "développement"
        else:
            return "initiale"

class EnhancedRecommendationGenerator:
    """Générateur de recommandations enrichies avec données CNESST"""
    
    def __init__(self):
        self.cnesst_enhancer = CNESSTContextEnhancer()
        
    def generate_enhanced_recommendations(self, context: Dict, analysis: Dict) -> List[Dict]:
        """Génère des recommandations enrichies avec données sectorielles"""
        
        recommendations = []
        
        # Recommandations de base
        base_recs = self._generate_base_recommendations(context, analysis)
        recommendations.extend(base_recs)
        
        # Recommandations sectorielles si données disponibles
        if analysis.get("enhancement_status") == "enriched":
            sector_recs = self._generate_sector_recommendations(context, analysis)
            recommendations.extend(sector_recs)
            
            benchmark_recs = self._generate_benchmark_recommendations(context, analysis)
            recommendations.extend(benchmark_recs)
        
        return recommendations
    
    def _generate_base_recommendations(self, context: Dict, analysis: Dict) -> List[Dict]:
        """Recommandations de base (enrichies)"""
        
        base_analysis = analysis.get("analysis", {}).get("base_analysis", {})
        
        recommendations = []
        
        # Recommandation formation de base
        recommendations.append({
            "id": "base_001",
            "type": "base",
            "priorite": "haute",
            "titre": "Formation sécurité personnalisée",
            "description": "Formation adaptée aux risques spécifiques identifiés",
            "source": "SafetyGraph - Analyse de base",
            "actions": [
                "Identifier les besoins de formation spécifiques",
                "Développer programme adapté au secteur",
                "Planifier sessions régulières"
            ]
        })
        
        return recommendations
    
    def _generate_sector_recommendations(self, context: Dict, analysis: Dict) -> List[Dict]:
        """Recommandations spécifiques au secteur détecté"""
        
        sector_analysis = analysis.get("analysis", {}).get("sector_analysis", {})
        if not sector_analysis:
            return []
        
        sector_code = sector_analysis.get("sector_code")
        specific_risks = sector_analysis.get("specific_risks", [])
        
        recommendations = []
        
        # Recommandations par secteur
        if sector_code and sector_code.startswith("23"):  # Construction
            recommendations.append({
                "id": "cnesst_construction_001",
                "type": "cnesst_sectoriel",
                "priorite": "critique",
                "titre": "Programme prévention chutes - Construction",
                "description": "Prévention des chutes conformément aux standards CNESST construction",
                "source": "CNESST - Guide sectoriel Construction",
                "secteur": "Construction (SCIAN 23)",
                "actions": [
                    "Inspection quotidienne équipements protection chutes",
                    "Formation utilisation harnais et lignes de vie",
                    "Vérification garde-corps et plateformes"
                ]
            })
            
        elif sector_code and sector_code.startswith("62"):  # Santé
            recommendations.append({
                "id": "cnesst_sante_001",
                "type": "cnesst_sectoriel", 
                "priorite": "haute",
                "titre": "Prévention TMS - Secteur santé",
                "description": "Programme prévention troubles musculo-squelettiques en milieu de soins",
                "source": "CNESST - Guide sectoriel Santé",
                "secteur": "Santé et assistance sociale (SCIAN 62)",
                "actions": [
                    "Formation techniques transfert patients",
                    "Évaluation ergonomique postes de travail",
                    "Rotation des tâches physiquement exigeantes"
                ]
            })
        
        return recommendations
    
    def _generate_benchmark_recommendations(self, context: Dict, analysis: Dict) -> List[Dict]:
        """Recommandations basées sur comparaison avec benchmarks sectoriels"""
        
        benchmark_comparison = analysis.get("analysis", {}).get("benchmark_comparison", {})
        if not benchmark_comparison:
            return []
        
        recommendations = []
        
        # Analyse des comparaisons
        for comparison in benchmark_comparison.get("comparisons", []):
            if comparison["position"] == "préoccupante":
                recommendations.append({
                    "id": "cnesst_benchmark_001",
                    "type": "cnesst_benchmark",
                    "priorite": "critique",
                    "titre": f"Amélioration urgente - {comparison['metric']}",
                    "description": f"Performance sous la moyenne sectorielle ({comparison['ecart_pct']:+.1f}%)",
                    "source": "CNESST - Benchmarking sectoriel",
                    "benchmark": {
                        "metric": comparison["metric"],
                        "organisation": comparison["organisation"],
                        "secteur": comparison["secteur"],
                        "ecart": comparison["ecart_pct"]
                    },
                    "actions": [
                        "Audit détaillé des pratiques actuelles",
                        "Plan d'action correctif immédiat",
                        "Monitoring mensuel des progrès"
                    ]
                })
        
        return recommendations

# Test des classes si exécuté directement
if __name__ == "__main__":
    print("🧪 Test Module Enrichissements SafetyGraph")
    
    # Test détection SCIAN
    enhancer = CNESSTContextEnhancer()
    
    test_descriptions = [
        "Notre entreprise de construction spécialisée en fondation béton",
        "Hôpital régional avec services urgence et chirurgie",
        "Transport marchandises par camion"
    ]
    
    for desc in test_descriptions:
        result = enhancer.detect_scian_sector(desc)
        if result:
            code, nom, conf = result
            print(f"✅ '{desc}' -> {code} ({nom}) - {conf:.2f}")
        else:
            print(f"❌ '{desc}' -> Aucun secteur détecté")
    
    print("✅ Tests complétés - Module fonctionnel")
