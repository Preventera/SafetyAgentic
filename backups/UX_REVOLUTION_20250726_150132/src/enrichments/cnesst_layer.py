"""
SafetyGraph CNESST Layer - Enrichissement Sectoriel
==================================================

Layer d'enrichissement pour intégration données CNESST par secteur SCIAN.
Compatible avec SafetyGraph existant - Fallback automatique.

Author: Mario Genest - GenAISafety 
Version: 1.0.0
Date: 2025-07-11
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CNESSTEnrichmentLayer:
    """Layer d'enrichissement CNESST pour SafetyGraph"""
    
    def __init__(self):
        self.config_path = "data/cnesst/sectors_config.json"
        self.sectors_data = self._load_sectors_config()
        self.enabled = self.sectors_data is not None
        
        if self.enabled:
            logger.info("✅ CNESST Layer activé - 3 secteurs chargés")
        else:
            logger.warning("⚠️ CNESST Layer en mode dégradé")
    
    def _load_sectors_config(self) -> Optional[Dict]:
        """Charge la configuration secteurs CNESST"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Erreur chargement config CNESST: {e}")
        return None
    
    def detect_scian_sector(self, description: str) -> Optional[Tuple[str, str, float]]:
        """
        Détecte automatiquement le secteur SCIAN depuis une description
        
        Args:
            description: Description de l'organisation ou activité
            
        Returns:
            Tuple (code_scian, nom_secteur, confidence) ou None
        """
        if not self.enabled or not description:
            return None
        
        description_lower = description.lower()
        best_match = None
        best_confidence = 0
        
        # Recherche patterns dans configuration
        patterns = self.sectors_data.get("detection_patterns", {})
        
        for sector_type, keywords in patterns.items():
            confidence = 0
            matched_keywords = []
            
            for keyword in keywords:
                if keyword in description_lower:
                    confidence += 1
                    matched_keywords.append(keyword)
            
            if confidence > best_confidence:
                # Mapping secteur type vers code SCIAN
                scian_mapping = {
                    "construction": "23",
                    "sante": "62", 
                    "transport": "48"
                }
                
                scian_code = scian_mapping.get(sector_type)
                if scian_code and scian_code in self.sectors_data["sectors"]:
                    sector_info = self.sectors_data["sectors"][scian_code]
                    confidence_norm = min(confidence / len(keywords), 1.0)
                    
                    best_match = (scian_code, sector_info["nom"], confidence_norm)
                    best_confidence = confidence
        
        if best_match and best_match[2] > 0.3:  # Seuil confiance minimum
            logger.info(f"Secteur SCIAN détecté: {best_match[0]} - {best_match[1]} (conf: {best_match[2]:.2f})")
            return best_match
        
        return None
    
    def get_sector_benchmarks(self, scian_code: str) -> Optional[Dict]:
        """Récupère les benchmarks CNESST pour un secteur"""
        if not self.enabled:
            return None
        
        sectors = self.sectors_data.get("sectors", {})
        
        # Recherche exacte d'abord
        if scian_code in sectors:
            return sectors[scian_code]
        
        # Recherche secteur parent si sous-secteur
        for length in [1, 2]:
            if len(scian_code) > length:
                parent_code = scian_code[:length]
                if parent_code in sectors:
                    benchmarks = sectors[parent_code].copy()
                    benchmarks["note"] = f"Données secteur parent {parent_code}"
                    return benchmarks
        
        return None
    
    def enrich_context(self, context: Dict) -> Dict:
        """
        Enrichit le contexte avec données CNESST
        
        Args:
            context: Contexte original SafetyGraph
            
        Returns:
            Contexte enrichi avec données sectorielles
        """
        if not self.enabled:
            # Fallback - retourne contexte original
            return context
        
        enriched = context.copy()
        
        # Détection automatique secteur depuis description
        description = context.get("description_organisation", "")
        if description:
            sector_detection = self.detect_scian_sector(description)
            if sector_detection:
                code, nom, confidence = sector_detection
                
                enriched["cnesst_enrichment"] = {
                    "detected_sector": {
                        "scian_code": code,
                        "nom": nom,
                        "confidence": confidence,
                        "auto_detected": True
                    }
                }
                
                # Ajout benchmarks sectoriels
                benchmarks = self.get_sector_benchmarks(code)
                if benchmarks:
                    enriched["cnesst_enrichment"]["benchmarks"] = benchmarks
                    enriched["cnesst_enrichment"]["enriched"] = True
        
        # Enrichissement manuel si code SCIAN fourni
        manual_scian = context.get("secteur_scian")
        if manual_scian and "cnesst_enrichment" not in enriched:
            benchmarks = self.get_sector_benchmarks(manual_scian)
            if benchmarks:
                enriched["cnesst_enrichment"] = {
                    "manual_sector": {
                        "scian_code": manual_scian,
                        "nom": benchmarks["nom"],
                        "auto_detected": False
                    },
                    "benchmarks": benchmarks,
                    "enriched": True
                }
        
        return enriched
    
    def get_enrichment_status(self) -> Dict:
        """Retourne le statut de l'enrichissement CNESST"""
        if not self.enabled:
            return {
                "status": "disabled",
                "message": "Enrichissements CNESST non disponibles",
                "sectors_available": 0
            }
        
        sectors_count = len(self.sectors_data.get("sectors", {}))
        total_incidents = self.sectors_data.get("metadata", {}).get("total_incidents", 0)
        
        return {
            "status": "enabled",
            "message": "Enrichissements CNESST activés",
            "sectors_available": sectors_count,
            "total_incidents": total_incidents,
            "version": "1.0.0"
        }

# Instance globale pour utilisation dans SafetyGraph
cnesst_enrichment = CNESSTEnrichmentLayer()

def enrich_safetygraph_context(context: Dict) -> Dict:
    """
    Fonction utilitaire pour enrichissement contexte SafetyGraph
    
    Usage dans app_behaviorx.py:
    from src.enrichments.cnesst_layer import enrich_safetygraph_context
    enriched_context = enrich_safetygraph_context(user_context)
    """
    return cnesst_enrichment.enrich_context(context)

def get_cnesst_status() -> Dict:
    """Fonction utilitaire pour statut enrichissement"""
    return cnesst_enrichment.get_enrichment_status()

# Test du module si exécuté directement
if __name__ == "__main__":
    print("🧪 Test CNESST Enrichment Layer")
    
    # Test détection secteurs
    test_descriptions = [
        "Notre entreprise de construction spécialisée en fondation béton",
        "Hôpital régional avec services soins ambulatoires",
        "Entreprise transport marchandises par camion"
    ]
    
    layer = CNESSTEnrichmentLayer()
    
    for desc in test_descriptions:
        result = layer.detect_scian_sector(desc)
        if result:
            code, nom, conf = result
            print(f"✅ '{desc[:40]}...' → {code} ({nom}) - {conf:.2f}")
        else:
            print(f"❌ '{desc[:40]}...' → Aucun secteur détecté")
    
    # Test enrichissement contexte
    test_context = {
        "description_organisation": "construction béton fondations",
        "nb_employes": 150
    }
    
    enriched = layer.enrich_context(test_context)
    print(f"\n📊 Test enrichissement:")
    print(f"Original: {len(test_context)} clés")
    print(f"Enrichi: {len(enriched)} clés")
    
    if "cnesst_enrichment" in enriched:
        print("✅ Enrichissement CNESST appliqué")
    else:
        print("❌ Enrichissement CNESST non appliqué")
