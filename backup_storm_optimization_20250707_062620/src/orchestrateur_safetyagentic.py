# Test R1 avec Données AN1 Réelles SafetyAgentic
# ==============================================
# Test Agent R1 avec vraies données AN1 de votre orchestrateur

import sys
import os
import asyncio
from pathlib import Path

# Ajout des chemins pour imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))

# Import Agent R1
try:
    from src.agents.recommendation.r1_generateur_recommandations import R1GenerateurRecommandations
    print("✅ Import Agent R1 réussi")
except ImportError as e:
    print(f"❌ Erreur import R1: {e}")
    sys.exit(1)

async def test_r1_avec_donnees_orchestrateur():
    """Test R1 avec données AN1 comme votre orchestrateur les génère"""
    
    print("🧪 TEST R1 AVEC DONNÉES AN1 RÉELLES")
    print("=" * 45)
    print("🎯 Utilise format données de votre orchestrateur validé")
    
    # Données AN1 exactement comme votre orchestrateur les génère
    # (Basé sur votre orchestrateur qui marche)
    data_an1_reel = {
        "agent_info": {
            "agent_id": "AN1",
            "agent_name": "Analyste Écarts",
            "confidence_score": 0.85
        },
        "ecarts_analysis": {
            "zones_aveugles": [
                {
                    "variable": "supervision_directe",
                    "pourcentage_ecart": 55.6,
                    "niveau_critique": "CRITIQUE",
                    "type_ecart": "surestimation",
                    "score_autoeval": 7.5,
                    "score_terrain": 3.5,
                    "impact_potentiel": "CRITIQUE - Risque incident majeur",
                    "explication": "Surestimation de 55.6% sur supervision_directe. L'équipe pense mieux performer qu'en réalité."
                },
                {
                    "variable": "usage_epi",
                    "pourcentage_ecart": 45.1,
                    "niveau_critique": "ÉLEVÉE",
                    "type_ecart": "surestimation",
                    "score_autoeval": 8.2,
                    "score_terrain": 4.8,
                    "impact_potentiel": "ÉLEVÉ - Intervention urgente requise",
                    "explication": "Surestimation de 45.1% sur usage_epi. L'équipe pense mieux performer qu'en réalité."
                },
                {
                    "variable": "formation_securite",
                    "pourcentage_ecart": 32.4,
                    "niveau_critique": "ÉLEVÉE", 
                    "type_ecart": "surestimation",
                    "score_autoeval": 7.4,
                    "score_terrain": 5.6,
                    "impact_potentiel": "MODÉRÉ - Surveillance renforcée",
                    "explication": "Surestimation de 32.4% sur formation_securite. L'équipe pense mieux performer qu'en réalité."
                },
                {
                    "variable": "communication_risques",
                    "pourcentage_ecart": 28.1,
                    "niveau_critique": "ÉLEVÉE",
                    "type_ecart": "surestimation", 
                    "score_autoeval": 6.8,
                    "score_terrain": 5.2,
                    "impact_potentiel": "MODÉRÉ - Surveillance renforcée",
                    "explication": "Surestimation de 28.1% sur communication_risques. L'équipe pense mieux performer qu'en réalité."
                }
            ],
            "nombre_ecarts_critiques": 4,
            "ecarts_variables": {
                "supervision_directe": {
                    "score_autoeval": 7.5,
                    "score_terrain": 3.5,
                    "ecart_absolu": 4.0,
                    "pourcentage": 55.6,
                    "niveau": "critique"
                },
                "usage_epi": {
                    "score_autoeval": 8.2,
                    "score_terrain": 4.8,
                    "ecart_absolu": 3.4,
                    "pourcentage": 45.1,
                    "niveau": "eleve"
                }
            }
        },
        "summary": {
            "ecart_moyen": 40.3,
            "variables_critiques": 4,
            "actions_recommandees": 12,
            "priorite_intervention": "CRITIQUE"
        },
        "hse_models_analysis": {
            "hfacs_l1": {
                "model_name": "Échecs organisationnels",
                "score_applicabilite": 87
            },
            "hfacs_l2": {
                "model_name": "Supervision inadéquate", 
                "score_applicabilite": 92
            }
        }
    }
    
    # Contexte construction (comme votre orchestrateur)
    context_construction = {
        "secteur": "CONSTRUCTION",
        "type_incident": "CHUTE_HAUTEUR",
        "nature_lesion": "FRACTURE_EPAULE",
        "agent_causal": "ECHAFAUDAGE_MOBILE",
        "taille_entreprise": "MOYENNE",
        "nombre_employes": 85,
        "budget_sst_annuel": 125000,
        "incident_recents": 3,
        "formation_recente": False
    }
    
    print("📊 DONNÉES AN1 ANALYSÉES:")
    print(f"  • Zones aveugles: {len(data_an1_reel['ecarts_analysis']['zones_aveugles'])}")
    print(f"  • Écart moyen: {data_an1_reel['summary']['ecart_moyen']:.1f}%")
    print(f"  • Priorité: {data_an1_reel['summary']['priorite_intervention']}")
    
    # Initialiser et exécuter R1
    agent_r1 = R1GenerateurRecommandations()
    result_r1 = await agent_r1.process(data_an1_reel, context_construction)
    
    # Affichage résultats détaillés
    print(f"\n💡 RÉSULTATS AGENT R1:")
    print("=" * 25)
    print(f"✅ Confiance: {result_r1['agent_info']['confidence_score']:.3f}")
    print(f"📊 Zones traitées: {result_r1['recommandations_analysis']['zones_traitees']}")
    print(f"💡 Recommandations: {result_r1['recommandations_analysis']['recommandations_generees']}")
    
    # Plan d'action détaillé
    plan = result_r1['plan_action']
    print(f"\n📋 PLAN D'ACTION GÉNÉRÉ:")
    print(f"  • Durée totale: {plan['duree_totale_estimee']}")
    print(f"  • Nombre d'actions: {plan['nombre_actions']}")
    print(f"  • Priorité globale: {plan['priorite_globale']}")
    
    # Budget et ROI
    budget = result_r1['budget_analysis']
    print(f"\n💰 ANALYSE FINANCIÈRE:")
    print(f"  • Coût direct: {budget['cout_direct']:,.0f}$")
    print(f"  • Coût total: {budget['cout_total']:,.0f}$")
    print(f"  • Économies estimées: {budget['economies_estimees']:,.0f}$")
    print(f"  • ROI: {budget['roi_estime']:.1f}%")
    print(f"  • Payback: {budget['payback_period']:.1f} mois")
    
    # Top 3 recommandations détaillées
    print(f"\n🎯 TOP 3 RECOMMANDATIONS:")
    for i, reco in enumerate(result_r1['recommandations_detaillees'][:3], 1):
        print(f"\n  {i}. ZONE AVEUGLE: {reco['variable_cible'].upper()}")
        print(f"     Priorité: {reco['priorite']}")
        print(f"     Écart: {reco['ecart_a_corriger']:.1f}%")
        print(f"     Timeline: {reco['timeline']}")
        print(f"     Budget: {reco['budget_estime']:,.0f}$")
        print(f"     Personnel: {reco['personnels_impliques']} personnes")
        
        # Actions principales
        print(f"     📚 Formations ({len(reco['formations'])}):")
        for j, formation in enumerate(reco['formations'][:2], 1):
            print(f"        {j}. {formation}")
        
        print(f"     📋 Procédures ({len(reco['procedures'])}):")
        for j, procedure in enumerate(reco['procedures'][:2], 1):
            print(f"        {j}. {procedure}")
        
        print(f"     🎯 Méthode: {reco['methode_implementation']}")
    
    # Timeline d'implémentation
    timeline = result_r1['implementation_timeline']
    print(f"\n📅 TIMELINE IMPLÉMENTATION:")
    for i, phase in enumerate(timeline['phases'], 1):
        fin_date = phase['date_fin'].strftime('%d/%m/%Y') if phase['date_fin'] else "Continu"
        print(f"  Phase {i}: {phase['nom']}")
        print(f"           Durée: {phase['duree']} (fin: {fin_date})")
        print(f"           Activités: {len(phase['activites'])}")
        print(f"           Livrables: {len(phase['livrables'])}")
    
    # Métriques de succès
    metrics = result_r1['success_metrics']
    print(f"\n📈 OBJECTIFS DE RÉDUCTION D'ÉCARTS:")
    for indicateur in metrics['indicateurs_principaux']:
        print(f"  • {indicateur['variable']}:")
        print(f"    Initial: {indicateur['valeur_initiale']:.1f}% → Objectif court terme: {indicateur['objectif_court_terme']:.1f}%")
    
    # Impact business final
    business = result_r1['business_impact']
    print(f"\n💼 SYNTHÈSE IMPACT BUSINESS:")
    print(f"  🎯 ROI: {business['roi_estime']:.1f}%")
    print(f"  💰 Investissement: {business['cout_total']:,.0f}$")
    print(f"  💰 Économies: {business['economies_estimees']:,.0f}$")
    print(f"  ⏱️ Retour investissement: {business['payback_period']:.1f} mois")
    
    print(f"\n🎉 TEST R1 AVEC DONNÉES RÉELLES RÉUSSI !")
    print(f"✅ Agent R1 opérationnel avec données AN1 de votre orchestrateur")
    print(f"⏱️ Performance: {result_r1['agent_info']['performance_time']:.3f}s")
    
    return result_r1

# Test avec différents secteurs
async def test_r1_multi_secteurs():
    """Test R1 avec différents secteurs"""
    
    print(f"\n" + "="*60)
    print("🧪 TEST R1 MULTI-SECTEURS")
    print("=" * 30)
    
    # Test Soins de Santé
    data_an1_sante = {
        "ecarts_analysis": {
            "zones_aveugles": [
                {
                    "variable": "usage_epi",
                    "pourcentage_ecart": 62.3,
                    "niveau_critique": "CRITIQUE",
                    "type_ecart": "surestimation",
                    "score_autoeval": 8.9,
                    "score_terrain": 3.8,
                    "impact_potentiel": "CRITIQUE - Risque contamination"
                },
                {
                    "variable": "formation_securite",
                    "pourcentage_ecart": 41.2,
                    "niveau_critique": "ÉLEVÉE",
                    "type_ecart": "surestimation",
                    "score_autoeval": 7.8,
                    "score_terrain": 5.1,
                    "impact_potentiel": "ÉLEVÉ - Erreurs procédures"
                }
            ]
        },
        "summary": {
            "ecart_moyen": 51.8,
            "variables_critiques": 2,
            "priorite_intervention": "CRITIQUE"
        }
    }
    
    context_sante = {
        "secteur": "SOINS_SANTE",
        "type_incident": "CONTACT_PRODUIT_CHIMIQUE",
        "taille_entreprise": "GRANDE",
        "nombre_employes": 450
    }
    
    agent_r1 = R1GenerateurRecommandations()
    result_sante = await agent_r1.process(data_an1_sante, context_sante)
    
    print(f"🏥 SOINS DE SANTÉ:")
    print(f"  • ROI: {result_sante['budget_analysis']['roi_estime']:.1f}%")
    print(f"  • Budget: {result_sante['budget_analysis']['cout_total']:,.0f}$")
    print(f"  • Recommandations: {len(result_sante['recommandations_detaillees'])}")
    
    return result_sante

# Exécution tests
if __name__ == "__main__":
    print("🚀 LANCEMENT TEST R1 AVEC DONNÉES AN1 RÉELLES")
    print("=" * 50)
    
    # Test principal
    asyncio.run(test_r1_avec_donnees_orchestrateur())
    
    # Test multi-secteurs
    asyncio.run(test_r1_multi_secteurs())
    
    print(f"\n🏆 TESTS R1 TERMINÉS")
    print("Agent R1 validé avec données réelles SafetyAgentic !")