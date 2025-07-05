# Test Orchestrateur SafetyAgentic - Workflow A1+A2+AN1
# ======================================================

import asyncio
from datetime import datetime

# Import de l'orchestrateur (code intégré pour simplicité)
from orchestrateur_safetyagentic import SafetyAgenticOrchestrator

async def test_orchestrateur_incident_reel():
    """Test orchestrateur avec incident CNESST réel"""
    
    print("🧪 TEST ORCHESTRATEUR SAFETYAGENTIC")
    print("=" * 45)
    print("🎯 Workflow complet: A1 → A2 → AN1 → Synthèse")
    print("🔬 Analyse culture sécurité avec zones aveugles")
    print("💡 Recommandations priorisées et timeline")
    print("💰 Impact business et ROI intervention")
    
    # Incident CNESST construction réaliste
    incident_construction = {
        "ID": 98765,
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
    
    # Contexte entreprise construction
    context_entreprise = {
        "nom_entreprise": "Construction ABC Inc.",
        "taille_entreprise": "PME - 45 employés",
        "experience_sst": "Intermédiaire - 3 ans programme",
        "incidents_recents": 3,
        "formation_recente_sst": False,
        "secteur_risque": "Élevé - Construction résidentielle",
        "certification": "Aucune certification SST",
        "budget_sst_annuel": 25000,
        "responsable_sst": "Contremaître principal"
    }
    
    print(f"\n📋 INCIDENT ANALYSÉ:")
    print(f"   • ID CNESST: {incident_construction['ID']}")
    print(f"   • Nature: {incident_construction['NATURE_LESION']}")
    print(f"   • Type: {incident_construction['GENRE']}")
    print(f"   • Secteur: {incident_construction['SECTEUR_SCIAN']}")
    print(f"   • Agent causal: {incident_construction['AGENT_CAUSAL_LESION']}")
    print(f"   • Âge travailleur: {incident_construction['GROUPE_AGE']}")
    
    print(f"\n🏢 CONTEXTE ENTREPRISE:")
    print(f"   • Nom: {context_entreprise['nom_entreprise']}")
    print(f"   • Taille: {context_entreprise['taille_entreprise']}")
    print(f"   • Expérience SST: {context_entreprise['experience_sst']}")
    print(f"   • Incidents récents: {context_entreprise['incidents_recents']}")
    print(f"   • Budget SST: {context_entreprise['budget_sst_annuel']:,}$")
    
    # Initialisation orchestrateur
    print(f"\n🤖 Initialisation Orchestrateur SafetyAgentic...")
    orchestrator = SafetyAgenticOrchestrator()
    
    # Démarrage analyse complète
    print(f"\n🚀 LANCEMENT ANALYSE CULTURE SÉCURITÉ")
    print("=" * 50)
    
    start_time = datetime.now()
    
    # Exécution workflow complet
    rapport_final = await orchestrator.analyze_safety_culture(
        incident_construction, 
        context_entreprise
    )
    
    end_time = datetime.now()
    
    if "error" in rapport_final:
        print(f"❌ ERREUR: {rapport_final['error']}")
        return
    
    # Analyse des résultats
    print(f"\n" + "=" * 60)
    print("🎉 ANALYSE SAFETYAGENTIC TERMINÉE AVEC SUCCÈS !")
    print("=" * 60)
    
    # Performance globale
    performance = rapport_final["analysis_info"]["performance_time"]
    print(f"⏱️ Performance totale: {performance:.3f}s")
    print(f"🎯 Analyse ID: {rapport_final['analysis_info']['analysis_id']}")
    
    # Insights détaillés
    synthesis = rapport_final["final_synthesis"]
    metrics = rapport_final["global_metrics"]
    exec_summary = rapport_final["executive_summary"]
    
    print(f"\n🔍 INSIGHTS DÉTAILLÉS:")
    print("-" * 25)
    
    # Zones aveugles critiques
    zones_aveugles = synthesis["zones_aveugles_critiques"]
    print(f"⚠️ ZONES AVEUGLES DÉTECTÉES: {len(zones_aveugles)}")
    for i, zone in enumerate(zones_aveugles, 1):
        ecart = zone.get("pourcentage_ecart", 0)
        impact = zone.get("impact_potentiel", "INCONNU")
        print(f"   {i}. {zone.get('variable', 'Variable')} - {ecart:.1f}% écart ({impact})")
    
    # Causes racines
    causes_racines = synthesis["causes_racines"]
    print(f"\n🎯 CAUSES RACINES IDENTIFIÉES: {len(causes_racines)}")
    for i, cause in enumerate(causes_racines, 1):
        print(f"   {i}. {cause['cause']} (Niveau: {cause['level']})")
        print(f"      Evidence: {cause['evidence']}")
        print(f"      Impact: {cause['impact']}")
    
    # Actions prioritaires avec timeline
    actions = synthesis["actions_prioritaires"][:5]
    print(f"\n💡 TOP 5 ACTIONS PRIORITAIRES:")
    for i, action in enumerate(actions, 1):
        priorite = action.get("priorite", "MOYENNE")
        timeline = action.get("timeline", "Non spécifiée")
        icon = "🚨" if priorite == "URGENTE" else "⚠️" if priorite == "ÉLEVÉE" else "📋"
        
        print(f"   {i}. {icon} {priorite} - {timeline}")
        print(f"      Action: {action.get('action', 'Action')}")
        if "methode" in action:
            print(f"      Méthode: {action['methode']}")
        if "ressources_requises" in action:
            print(f"      Ressources: {action['ressources_requises']}")
    
    # Timeline d'intervention
    timeline = synthesis["timeline_intervention"]
    print(f"\n📅 TIMELINE D'INTERVENTION:")
    if timeline.get("immediate"):
        print(f"   🚨 Actions immédiates (0-2 sem): {len(timeline['immediate'])}")
        for action in timeline["immediate"][:2]:
            print(f"      → {action}")
    
    if timeline.get("short_term"):
        print(f"   ⚠️ Court terme (2-8 sem): {len(timeline['short_term'])}")
        for action in timeline["short_term"][:2]:
            print(f"      → {action}")
    
    if timeline.get("medium_term"):
        print(f"   📋 Moyen terme (2-6 mois): {len(timeline['medium_term'])}")
    
    # Impact business détaillé
    business_impact = synthesis["impact_business"]
    print(f"\n💰 IMPACT BUSINESS DÉTAILLÉ:")
    print(f"   • Coût zones aveugles: {business_impact['cout_zones_aveugles']:,}$")
    print(f"   • Probabilité incident: {business_impact['probabilite_incident']:.1%}")
    print(f"   • Coût incident potentiel: {business_impact['cout_incident_potentiel']:,}$")
    print(f"   • Espérance de perte: {business_impact['esperance_perte']:,}$")
    
    roi_info = business_impact["roi_intervention"]
    print(f"\n📈 ROI INTERVENTION:")
    print(f"   • Coût intervention: {roi_info['cout_intervention']:,}$")
    print(f"   • Économies potentielles: {roi_info['economies_potentielles']:,}$")
    print(f"   • Ratio ROI: {roi_info['roi_ratio']}x")
    
    # Métriques de succès
    success_metrics = synthesis["success_metrics"]
    print(f"\n📊 MÉTRIQUES DE SUCCÈS:")
    for i, metric in enumerate(success_metrics[:3], 1):
        print(f"   {i}. {metric['variable']}")
        print(f"      Baseline: {metric['baseline_ecart']:.1f}% écart")
        print(f"      Objectif: <{metric['target_ecart']:.1f}% écart")
        print(f"      Méthode: {metric['measurement_method']}")
        print(f"      Fréquence: {metric['frequency']}")
    
    # Évaluation risque résiduel
    risk_assessment = synthesis["risk_assessment"]
    print(f"\n⚠️ ÉVALUATION RISQUE RÉSIDUEL:")
    print(f"   • Niveau risque: {risk_assessment['niveau_risque']}")
    print(f"   • Description: {risk_assessment['description']}")
    print(f"   • Zones critiques: {risk_assessment['zones_critiques']}")
    print(f"   • Action requise: {risk_assessment['action_requise']}")
    
    # Qualité de l'analyse
    quality = rapport_final["quality_assessment"]
    print(f"\n✅ QUALITÉ DE L'ANALYSE:")
    print(f"   • Score qualité: {quality['score_qualite']}/100")
    print(f"   • Niveau: {quality['niveau_qualite']}")
    print(f"   • Recommandation: {quality['recommandation_qualite']}")
    
    if quality.get("issues_detectees"):
        print(f"   • Issues: {', '.join(quality['issues_detectees'])}")
    
    # Recommandations pour l'entreprise
    print(f"\n🎯 RECOMMANDATIONS SPÉCIFIQUES ENTREPRISE:")
    print(f"   Basé sur: {context_entreprise['nom_entreprise']}")
    
    if context_entreprise["budget_sst_annuel"] < 30000:
        print(f"   💰 Budget SST insuffisant ({context_entreprise['budget_sst_annuel']:,}$)")
        print(f"      → Recommander augmentation à min 50,000$ (ROI: {roi_info['roi_ratio']}x)")
    
    if not context_entreprise["formation_recente_sst"]:
        print(f"   📚 Formation SST non récente")
        print(f"      → Planifier formation superviseurs prioritaire")
    
    if context_entreprise["incidents_recents"] >= 3:
        print(f"   🚨 Incidents fréquents ({context_entreprise['incidents_recents']})")
        print(f"      → Audit système SST complet recommandé")
    
    # Message final
    priorite_globale = exec_summary["priorite_globale"]
    message_cle = exec_summary["message_cle"]
    
    print(f"\n" + "=" * 60)
    print("📋 RÉSUMÉ EXÉCUTIF FINAL")
    print("=" * 60)
    print(f"🎯 {message_cle}")
    print(f"🚨 Priorité globale: {priorite_globale}")
    print(f"⏰ Timeline critique: {exec_summary['timeline_critique']}")
    print(f"💸 Impact business: {exec_summary['impact_business']:,}$")
    print(f"⚠️ Niveau risque: {exec_summary['niveau_risque']}")
    
    if priorite_globale in ["URGENTE", "ÉLEVÉE"]:
        print(f"\n🚨 ALERTE: Action immédiate requise dans les {exec_summary['timeline_critique']}")
        print(f"   Zones aveugles critiques détectées - Risque incident élevé")
    else:
        print(f"\n✅ SITUATION: Amélioration continue recommandée")
        print(f"   Surveillance renforcée et actions préventives")
    
    print(f"\n🎉 ANALYSE SAFETYAGENTIC TERMINÉE AVEC SUCCÈS !")
    print(f"⏱️ Performance totale: {(end_time - start_time).total_seconds():.3f}s")
    print(f"🎯 Rapport disponible pour implémentation")
    
    return rapport_final

if __name__ == "__main__":
    # Exécution test orchestrateur
    asyncio.run(test_orchestrateur_incident_reel())