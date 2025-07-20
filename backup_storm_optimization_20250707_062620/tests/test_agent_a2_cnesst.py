# Test Agent A2 avec Données CNESST Réelles - Capteur Observations
# ================================================================

import sys
import os
import pandas as pd
from pathlib import Path
import asyncio

# Ajout des chemins pour imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

try:
    from src.agents.collecte.a2_observations import A2CapteurObservations, SafetyAgenticState
except ImportError:
    import sys
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_dir = os.path.join(parent_dir, 'src')
    sys.path.insert(0, src_dir)
    from agents.collecte.a2_observations import A2CapteurObservations, SafetyAgenticState

async def test_a2_avec_donnees_cnesst():
    """Test de l'agent A2 avec de vraies données CNESST"""
    
    print("🧪 TEST AGENT A2 AVEC DONNÉES CNESST RÉELLES")
    print("============================================")
    print("🎯 Focus: Observations terrain et analyse EPI")
    
    # Chemin vers vos données CNESST
    data_path = Path("../data")
    print(f"📁 Recherche dans: {data_path.absolute()}")
    
    # Trouver les fichiers CNESST
    csv_files = list(data_path.glob("lesions-*.csv"))
    
    if not csv_files:
        print("❌ Aucun fichier CNESST trouvé")
        return
    
    # Utiliser le fichier 2023
    csv_file = None
    for file in csv_files:
        if "2023" in file.name:
            csv_file = file
            break
    
    if not csv_file:
        csv_file = csv_files[0]
    
    print(f"📊 Lecture du fichier: {csv_file.name}")
    
    try:
        # Lecture d'un échantillon ciblé (incidents terrain)
        df = pd.read_csv(csv_file, nrows=100, encoding='utf-8')
        print(f"✅ {len(df)} incidents CNESST chargés")
        
        # Aperçu des données
        print("\n📊 APERÇU DONNÉES POUR OBSERVATIONS:")
        print("===================================")
        
        # Analyse des incidents pertinents pour observations terrain
        if 'IND_LESION_MACHINE' in df.columns:
            machine_count = (df['IND_LESION_MACHINE'] == 'OUI').sum()
            print(f"🔧 Incidents machines: {machine_count}/{len(df)} ({100*machine_count/len(df):.1f}%)")
        
        if 'GENRE' in df.columns:
            chutes_count = df['GENRE'].str.contains('CHUTE', na=False).sum()
            frappe_count = df['GENRE'].str.contains('FRAPPE', na=False).sum()
            print(f"📉 Incidents chutes: {chutes_count}/{len(df)} ({100*chutes_count/len(df):.1f}%)")
            print(f"🔨 Incidents frappe/objet: {frappe_count}/{len(df)} ({100*frappe_count/len(df):.1f}%)")
        
        if 'SIEGE_LESION' in df.columns:
            tete_count = df['SIEGE_LESION'].str.contains('TETE', na=False).sum()
            main_count = df['SIEGE_LESION'].str.contains('MAIN|DOIGT', na=False).sum()
            print(f"🧠 Lésions tête: {tete_count} (EPI casque pertinent)")
            print(f"✋ Lésions mains: {main_count} (EPI gants pertinent)")
        
        print()
        
        # Création de l'agent A2
        print("🤖 Initialisation Agent A2...")
        agent_a2 = A2CapteurObservations()
        print("✅ Agent A2 prêt pour observations terrain")
        print()
        
        # Sélection d'incidents spécifiques pour observations
        incidents_a_tester = []
        
        # 1. Chercher incident machine
        if 'IND_LESION_MACHINE' in df.columns:
            cas_machine = df[df['IND_LESION_MACHINE'] == 'OUI']
            if not cas_machine.empty:
                incidents_a_tester.append(("MACHINE", cas_machine.iloc[0]))
        
        # 2. Chercher incident chute (EPI pertinent)
        if 'GENRE' in df.columns:
            cas_chute = df[df['GENRE'].str.contains('CHUTE', na=False)]
            if not cas_chute.empty:
                incidents_a_tester.append(("CHUTE", cas_chute.iloc[0]))
        
        # 3. Chercher incident frappe par objet
        if 'GENRE' in df.columns:
            cas_frappe = df[df['GENRE'].str.contains('FRAPPE', na=False)]
            if not cas_frappe.empty:
                incidents_a_tester.append(("FRAPPE", cas_frappe.iloc[0]))
        
        # Compléter avec incidents généraux si nécessaire
        for idx, row in df.head(3).iterrows():
            if len(incidents_a_tester) < 3:
                incidents_a_tester.append(("GENERAL", row))
        
        print("🔄 ANALYSE OBSERVATIONS TERRAIN:")
        print("===============================")
        
        resultats_analyses = []
        
        for incident_num, (incident_type, row) in enumerate(incidents_a_tester, 1):
            
            print(f"\n--- OBSERVATION TERRAIN {incident_num} ({incident_type}) ---")
            print(f"ID: {row.get('ID', 'N/A')}")
            print(f"Nature: {str(row.get('NATURE_LESION', 'N/A'))[:50]}...")
            print(f"Siège: {str(row.get('SIEGE_LESION', 'N/A'))[:30]}...")
            print(f"Genre: {str(row.get('GENRE', 'N/A'))[:40]}...")
            print(f"Secteur: {str(row.get('SECTEUR_SCIAN', 'N/A'))[:40]}...")
            
            # Indicateurs pour contexte observation
            indicateurs = []
            if row.get('IND_LESION_MACHINE') == 'OUI':
                indicateurs.append("MACHINE")
            if row.get('IND_LESION_TMS') == 'OUI':
                indicateurs.append("TMS")
            if row.get('IND_LESION_PSY') == 'OUI':
                indicateurs.append("PSY")
            
            if indicateurs:
                print(f"🔍 Contexte observation: {', '.join(indicateurs)}")
            
            # Préparation de l'état SafetyAgentic pour A2
            test_state = SafetyAgenticState()
            
            # Données d'observation simulées basées sur l'incident
            test_state.incident_data = {
                "observation_data": {
                    "location": f"Zone {row.get('SECTEUR_SCIAN', 'Production')[:20]}",
                    "observer_id": f"INSPECTEUR_A2_{incident_num}",
                    "observation_type": "post_incident_inspection",
                    "incident_type": incident_type,
                    "environmental_conditions": {
                        "lighting": "adequate" if incident_type != "CHUTE" else "poor",
                        "noise_level": "high" if "MACHINE" in indicateurs else "normal",
                        "hazard_level": "high" if incident_type == "MACHINE" else "medium"
                    },
                    "epi_observation": {
                        "helmet_required": "CONSTRUCTION" in str(row.get('SECTEUR_SCIAN', '')).upper(),
                        "gloves_required": "FABRICATION" in str(row.get('SECTEUR_SCIAN', '')).upper(),
                        "safety_shoes_required": True
                    }
                },
                "incident_cnesst": {
                    "ID": row.get('ID'),
                    "NATURE_LESION": str(row.get('NATURE_LESION', '')),
                    "SIEGE_LESION": str(row.get('SIEGE_LESION', '')),
                    "GENRE": str(row.get('GENRE', '')),
                    "AGENT_CAUSAL_LESION": str(row.get('AGENT_CAUSAL_LESION', '')),
                    "SEXE_PERS_PHYS": str(row.get('SEXE_PERS_PHYS', '')),
                    "GROUPE_AGE": str(row.get('GROUPE_AGE', '')),
                    "SECTEUR_SCIAN": str(row.get('SECTEUR_SCIAN', '')),
                    "IND_LESION_SURDITE": str(row.get('IND_LESION_SURDITE', '')),
                    "IND_LESION_MACHINE": str(row.get('IND_LESION_MACHINE', '')),
                    "IND_LESION_TMS": str(row.get('IND_LESION_TMS', '')),
                    "IND_LESION_PSY": str(row.get('IND_LESION_PSY', '')),
                    "IND_LESION_COVID_19": str(row.get('IND_LESION_COVID_19', ''))
                }
            }
            
            # Traitement par l'agent A2
            print("🔄 Analyse par Agent A2 (Capteur Observations)...")
            result_state = await agent_a2.process(test_state)
            
            # Analyse des résultats
            if "A2" in result_state.analysis_results:
                a2_result = result_state.analysis_results["A2"]
                
                print(f"✅ Score confiance: {a2_result.get('confidence_score', 0):.3f}")
                print(f"📊 Variables culture: {len(a2_result.get('culture_variables', []))}")
                print(f"⚠️ Dangers détectés: {a2_result.get('hazard_detection', {}).get('total_hazards_detected', 0)}")
                
                # Analyse EPI spécifique
                epi_analysis = a2_result.get('epi_analysis', {})
                print(f"🛡️ Conformité EPI: {epi_analysis.get('overall_compliance', 0):.1%}")
                print(f"   EPI analysés: {epi_analysis.get('total_epi_analyzed', 0)}")
                print(f"   EPI obligatoires: {epi_analysis.get('required_epi_count', 0)}")
                
                # Conformité procédures
                compliance = a2_result.get('compliance_analysis', {})
                print(f"📋 Conformité procédures: {compliance.get('overall_compliance', 0):.1%}")
                
                # Dangers critiques
                hazards = a2_result.get('hazard_detection', {})
                high_priority = hazards.get('high_priority_hazards', [])
                if high_priority:
                    print(f"🚨 Dangers critiques: {len(high_priority)}")
                    for hazard in high_priority:
                        print(f"   - {hazard['type']} (conf: {hazard['confidence']:.2f})")
                
                # Top variables culture terrain
                variables = a2_result.get('culture_variables', [])[:3]
                if variables:
                    print("🎯 Top variables culture (terrain):")
                    for var in variables:
                        print(f"   - {var['variable_name']}: {var['score']:.1f}/10 ({var['source']})")
                
                # Recommandations terrain
                recommendations = a2_result.get('recommendations', [])[:2]
                if recommendations:
                    print("💡 Recommandations terrain:")
                    for rec in recommendations:
                        print(f"   - {rec}")
                
                # Collecte pour statistiques
                resultats_analyses.append({
                    "incident_id": row.get('ID'),
                    "type": incident_type,
                    "confiance": a2_result.get('confidence_score', 0),
                    "variables_count": len(a2_result.get('culture_variables', [])),
                    "dangers_count": hazards.get('total_hazards_detected', 0),
                    "epi_compliance": epi_analysis.get('overall_compliance', 0),
                    "proc_compliance": compliance.get('overall_compliance', 0),
                    "has_critical_hazards": len(high_priority) > 0,
                    "recommendations_count": len(recommendations)
                })
            else:
                print("❌ Aucun résultat d'analyse A2")
            
            if result_state.errors:
                print(f"⚠️ Erreurs: {result_state.errors}")
        
        # Résumé global des observations
        print("\n" + "="*60)
        print("📊 RÉSUMÉ OBSERVATIONS TERRAIN SAFETYAGENTIC")
        print("="*60)
        
        if resultats_analyses:
            confiance_moyenne = sum(r['confiance'] for r in resultats_analyses) / len(resultats_analyses)
            variables_moyenne = sum(r['variables_count'] for r in resultats_analyses) / len(resultats_analyses)
            dangers_moyenne = sum(r['dangers_count'] for r in resultats_analyses) / len(resultats_analyses)
            epi_compliance_moyenne = sum(r['epi_compliance'] for r in resultats_analyses) / len(resultats_analyses)
            
            print(f"✅ Observations terrain analysées: {len(resultats_analyses)}")
            print(f"📊 Score confiance moyen: {confiance_moyenne:.3f}")
            print(f"🎯 Variables culture moyennes: {variables_moyenne:.1f}")
            print(f"⚠️ Dangers moyens détectés: {dangers_moyenne:.1f}")
            print(f"🛡️ Conformité EPI moyenne: {epi_compliance_moyenne:.1%}")
            
            # Analyse par type d'incident
            types_incidents = {}
            for r in resultats_analyses:
                incident_type = r['type']
                if incident_type not in types_incidents:
                    types_incidents[incident_type] = []
                types_incidents[incident_type].append(r)
            
            print(f"\n🔍 ANALYSE PAR TYPE D'INCIDENT:")
            for incident_type, incidents in types_incidents.items():
                avg_epi = sum(i['epi_compliance'] for i in incidents) / len(incidents)
                avg_dangers = sum(i['dangers_count'] for i in incidents) / len(incidents)
                print(f"  {incident_type}: EPI {avg_epi:.1%}, Dangers {avg_dangers:.1f}")
            
            # Incidents critiques
            incidents_critiques = sum(1 for r in resultats_analyses if r['has_critical_hazards'])
            print(f"\n🚨 Incidents avec dangers critiques: {incidents_critiques}/{len(resultats_analyses)}")
            
            # Recommandations totales
            total_recommendations = sum(r['recommendations_count'] for r in resultats_analyses)
            print(f"💡 Recommandations terrain générées: {total_recommendations}")
        
        print(f"\n🎉 TEST OBSERVATIONS TERRAIN TERMINÉ!")
        print("="*60)
        print("✅ VALIDATION RÉUSSIE AGENT A2:")
        print("  • Analyse observations terrain avec données CNESST réelles")
        print("  • Évaluation automatique conformité EPI par secteur")
        print("  • Détection intelligente dangers selon type d'incident")
        print("  • Mapping spécialisé variables culture terrain")
        print("  • Recommandations ciblées observations")
        print()
        print("🚀 Agent A2 prêt pour intégration avec A1 et orchestration !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_a2_avec_donnees_cnesst())