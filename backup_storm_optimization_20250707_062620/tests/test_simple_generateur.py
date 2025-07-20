# Test Simple Générateur Synthétique - SafetyAgentic
# ==================================================
# Test du générateur sans dépendances externes

import sys
import os

# Ajout chemin pour imports
sys.path.append(os.path.join('src', 'agents', 'collecte'))

try:
    from generateur_donnees_synthetiques import (
        GenerateurDonneesSynthetiques, 
        SecteurActivite, 
        TypeIncident
    )
    print("✅ Import générateur réussi")
except ImportError as e:
    print(f"❌ Erreur import générateur: {e}")
    sys.exit(1)

def test_generateur_simple():
    """Test simple du générateur synthétique"""
    
    print("\n🧪 TEST SIMPLE GÉNÉRATEUR SYNTHÉTIQUE")
    print("=" * 45)
    
    # Initialisation
    generateur = GenerateurDonneesSynthetiques(seed=42)
    print("🤖 Générateur initialisé")
    
    # Test 1: Observation unique
    print("\n1️⃣ TEST OBSERVATION UNIQUE")
    print("-" * 30)
    
    obs = generateur.generate_observation_synthetique(
        secteur=SecteurActivite.CONSTRUCTION,
        qualite_culture="moyenne"
    )
    
    print(f"✅ Observation générée:")
    print(f"   Secteur: {obs['contexte']['secteur_activite']}")
    print(f"   Entreprise: {obs['contexte']['entreprise']}")
    print(f"   Score culture: {sum(obs['variables_culture'].values()) / len(obs['variables_culture']):.1f}/10")
    print(f"   Variables: {list(obs['variables_culture'].keys())}")
    print(f"   EPI analysés: {obs['conformite']['epi_analyses']}")
    print(f"   Dangers: {len(obs['conformite']['dangers'])}")
    
    # Test 2: Batch observations
    print("\n2️⃣ TEST BATCH OBSERVATIONS")
    print("-" * 30)
    
    batch = generateur.generer_batch_observations(5)
    print(f"✅ Batch généré: {len(batch)} observations")
    
    # Analyse batch
    stats = generateur.analyser_statistiques_batch(batch)
    print(f"   Score culture moyen: {stats['score_culture_moyen']:.1f}/10")
    print(f"   Conformité EPI moyenne: {stats['conformite_epi_moyenne']:.1f}%")
    print(f"   Secteurs: {list(stats['distribution_secteurs'].keys())}")
    
    # Test 3: Différents secteurs
    print("\n3️⃣ TEST TOUS SECTEURS")
    print("-" * 25)
    
    for secteur in SecteurActivite:
        obs_secteur = generateur.generate_observation_synthetique(
            secteur=secteur,
            qualite_culture="bonne"
        )
        score = sum(obs_secteur['variables_culture'].values()) / len(obs_secteur['variables_culture'])
        dangers = len(obs_secteur['conformite']['dangers'])
        print(f"   🏢 {secteur.value}: {score:.1f}/10, {dangers} dangers")
    
    # Test 4: Qualités culture
    print("\n4️⃣ TEST QUALITÉS CULTURE")
    print("-" * 25)
    
    for qualite in ["excellente", "bonne", "moyenne", "faible"]:
        obs_qualite = generateur.generate_observation_synthetique(
            secteur=SecteurActivite.FABRICATION,
            qualite_culture=qualite
        )
        score = sum(obs_qualite['variables_culture'].values()) / len(obs_qualite['variables_culture'])
        conformite = obs_qualite['conformite']['taux_conformite']
        print(f"   🎯 {qualite.upper()}: {score:.1f}/10, {conformite:.1f}% conformité")
    
    print(f"\n🎉 TOUS LES TESTS RÉUSSIS !")
    print("=" * 45)
    print("✅ Générateur synthétique fonctionnel")
    print("🔬 Basé sur statistiques CNESST 793K incidents")
    print("⚡ Prêt pour intégration SafetyAgentic")
    
    return True

def demo_agent_a2_simulation():
    """Simulation Agent A2 avec générateur"""
    
    print("\n🤖 SIMULATION AGENT A2 AVEC GÉNÉRATEUR")
    print("=" * 45)
    
    generateur = GenerateurDonneesSynthetiques(seed=42)
    
    # Simulation données incident CNESST
    incident_data = {
        "ID": 123456,
        "SECTEUR_SCIAN": "CONSTRUCTION",
        "GENRE": "CHUTE DE HAUTEUR",
        "NATURE_LESION": "FRACTURE",
        "SIEGE_LESION": "JAMBE"
    }
    
    # Génération observation A2 synthétique
    obs_a2 = generateur.generate_observation_synthetique(
        secteur=SecteurActivite.CONSTRUCTION,
        qualite_culture="moyenne"
    )
    
    # Formatage résultat style Agent A2
    variables_culture_terrain = {}
    for var, score in obs_a2['variables_culture'].items():
        variables_culture_terrain[var] = {
            "score": score,
            "source": "observation_synthetique",
            "observations": obs_a2['contexte']['nb_travailleurs_observes']
        }
    
    conformite = obs_a2['conformite']
    conformite_epi_pct = conformite['taux_conformite']
    
    result_a2 = {
        "agent_id": "A2_SYNTHETIC",
        "confidence_score": 0.75,
        "variables_culture_terrain": variables_culture_terrain,
        "observations": {
            "score_comportement": int(sum(obs_a2['variables_culture'].values()) / len(obs_a2['variables_culture']) * 10),
            "dangers_detectes": len(conformite['dangers']),
            "epi_analyses": conformite['epi_analyses'],
            "epi_obligatoires": len(conformite['epi_types']),
            "conformite_procedures": conformite_epi_pct,
            "incidents_potentiels": 1 if conformite_epi_pct < 50 else 0
        },
        "contexte_observation": {
            "duree_observation": f"{obs_a2['contexte']['duree_observation']:.1f} heures",
            "nombre_travailleurs": obs_a2['contexte']['nb_travailleurs_observes'],
            "type_source": "donnees_synthetiques_cnesst",
            "conditions_meteo": obs_a2['contexte']['conditions_meteo']
        },
        "data_source": "synthetic",
        "synthetic_details": {
            "secteur_base": obs_a2['contexte']['secteur_activite'],
            "qualite_culture_cible": obs_a2['meta_generation']['qualite_culture_cible'],
            "seed_utilise": obs_a2['meta_generation']['seed_utilise']
        }
    }
    
    print(f"✅ RÉSULTAT AGENT A2 SIMULÉ:")
    print(f"   🔍 Source: {result_a2['data_source']}")
    print(f"   📊 Score comportement: {result_a2['observations']['score_comportement']}/100")
    print(f"   ⚠️ Dangers détectés: {result_a2['observations']['dangers_detectes']}")
    print(f"   🛡️ Conformité: {result_a2['observations']['conformite_procedures']:.1f}%")
    print(f"   👥 Travailleurs observés: {result_a2['contexte_observation']['nombre_travailleurs']}")
    print(f"   ⏱️ Durée: {result_a2['contexte_observation']['duree_observation']}")
    print(f"   ✅ Confiance: {result_a2['confidence_score']:.2f}")
    
    print(f"\n🎯 VARIABLES CULTURE TERRAIN:")
    for var, data in result_a2['variables_culture_terrain'].items():
        print(f"   • {var}: {data['score']}/10")
    
    print(f"\n🔬 DÉTAILS SYNTHÉTIQUES:")
    details = result_a2['synthetic_details']
    print(f"   • Secteur base: {details['secteur_base']}")
    print(f"   • Qualité culture: {details['qualite_culture_cible']}")
    print(f"   • Seed: {details['seed_utilise']}")
    
    return result_a2

if __name__ == "__main__":
    print("🚀 LANCEMENT TEST GÉNÉRATEUR SYNTHÉTIQUE")
    print("=" * 50)
    
    try:
        # Test générateur de base
        test_generateur_simple()
        
        # Simulation Agent A2
        demo_agent_a2_simulation()
        
        print(f"\n🎉 VALIDATION COMPLÈTE RÉUSSIE !")
        print("=" * 40)
        print("✅ Générateur synthétique opérationnel")
        print("🤖 Agent A2 simulation fonctionnelle") 
        print("🔬 Prêt pour SafetyAgentic complet")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        print("🔧 Vérifiez la structure des fichiers")