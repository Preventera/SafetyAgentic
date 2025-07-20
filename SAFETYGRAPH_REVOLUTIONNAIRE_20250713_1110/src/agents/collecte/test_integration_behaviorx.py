"""
Test Intégration A1+A2 BehaviorX Enhanced
========================================

ÉTAPE 1.3 - Test coordination A1 + A2 BehaviorX
Validation workflow intégré Safe Self + VCS + ABC
"""

import sys
import json
from datetime import datetime
from typing import Dict, List, Any

# Import agents BehaviorX créés
try:
    from a1_behaviorx_enhanced import AgentA1BehaviorXEnhanced
    from a2_behaviorx_enhanced import AgentA2BehaviorXEnhanced
    print("✅ Import agents BehaviorX réussi")
except ImportError as e:
    print(f"❌ Erreur import agents BehaviorX: {e}")
    sys.exit(1)

class IntegrationTesterBehaviorX:
    """Testeur intégration A1 + A2 BehaviorX"""
    
    def __init__(self):
        print("🧪 Initialisation testeur intégration BehaviorX")
        self.agent_a1 = AgentA1BehaviorXEnhanced()
        self.agent_a2 = AgentA2BehaviorXEnhanced()
        
    def run_integration_test(self, scenario: Dict) -> Dict:
        """Lance test intégration complet A1+A2 BehaviorX"""
        
        print(f"\n🎯 SCÉNARIO TEST: {scenario['name']}")
        print("=" * 60)
        
        # Contexte partagé
        company = scenario['company']
        secteur = scenario['secteur']
        context = scenario['context']
        
        results = {
            'scenario': scenario['name'],
            'company': company,
            'secteur': secteur,
            'timestamp': datetime.now().isoformat(),
            'a1_results': None,
            'a2_results': None,
            'integration_analysis': {}
        }
        
        try:
            # Test Agent A1 BehaviorX (Safe Self + Autoévaluations)
            print("\n🤖 PHASE 1: Agent A1 BehaviorX Enhanced")
            print("-" * 40)
            
            a1_data = scenario['a1_test_data']
            a1_results = self.agent_a1.process_with_behaviorx_memory(
                a1_data, company, secteur
            )
            results['a1_results'] = a1_results
            
            self._display_a1_results(a1_results)
            
            # Test Agent A2 BehaviorX (VCS + ABC Observations)
            print("\n🔍 PHASE 2: Agent A2 BehaviorX Enhanced")
            print("-" * 40)
            
            a2_results = self.agent_a2.process_observations_behaviorx(
                context, mode='mode_6_vcs'
            )
            results['a2_results'] = a2_results
            
            self._display_a2_results(a2_results)
            
            # Analyse intégration
            print("\n🔗 PHASE 3: Analyse Intégration A1+A2")
            print("-" * 40)
            
            integration_analysis = self._analyze_integration(a1_results, a2_results)
            results['integration_analysis'] = integration_analysis
            
            self._display_integration_analysis(integration_analysis)
            
            return results
            
        except Exception as e:
            print(f"❌ Erreur test intégration: {e}")
            results['error'] = str(e)
            return results
    
    def _display_a1_results(self, results: Dict):
        """Affiche résultats Agent A1 BehaviorX"""
        
        print(f"📊 Score final A1: {results.get('score_final', 'N/A')}")
        print(f"🎯 Niveau sécurité: {results.get('niveau_securite', 'N/A')}")
        print(f"🧠 Enhanced by Memory: {results.get('enhanced_by_memory', False)}")
        print(f"⚠️  Facteurs de risque comportementaux: {len(results.get('behavioral_risk_factors', []))}")
        print(f"✅ Facteurs protecteurs: {len(results.get('protective_factors', []))}")
        print(f"💡 Recommandations Safe Self: {len([r for r in results.get('recommandations', []) if 'behaviorx' in r.get('source', '')])}")
        
        # Détail facteurs comportementaux
        if results.get('behavioral_risk_factors'):
            print(f"   Risques: {', '.join(results['behavioral_risk_factors'])}")
        if results.get('protective_factors'):
            print(f"   Protections: {', '.join(results['protective_factors'])}")
    
    def _display_a2_results(self, results: Dict):
        """Affiche résultats Agent A2 BehaviorX"""
        
        print(f"📊 Score comportemental A2: {results.get('score_comportemental', 'N/A')}")
        print(f"🎯 Niveau comportemental: {results.get('niveau_comportemental', 'N/A')}")
        print(f"📋 Conformité VCS: {results.get('taux_conformite_vcs', 0):.1f}%")
        print(f"✅ Forces comportementales: {len(results.get('behavioral_strengths', []))}")
        print(f"⚠️  Préoccupations comportementales: {len(results.get('behavioral_concerns', []))}")
        print(f"🔗 Points d'intervention ABC: {len(results.get('intervention_points', []))}")
        print(f"💡 Recommandations VCS: {len(results.get('recommandations', []))}")
        
        # Détail catégories
        if results.get('behavioral_strengths'):
            print(f"   Forces: {', '.join(results['behavioral_strengths'])}")
        if results.get('behavioral_concerns'):
            print(f"   Préoccupations: {', '.join(results['behavioral_concerns'])}")
    
    def _analyze_integration(self, a1_results: Dict, a2_results: Dict) -> Dict:
        """Analyse l'intégration A1+A2 BehaviorX"""
        
        analysis = {
            'coherence_score': 0.0,
            'alignment_perception_observation': 'unknown',
            'behavioral_consistency': 'unknown',
            'integrated_recommendations': [],
            'zones_aveugles_detected': False,
            'overall_risk_level': 'unknown',
            'intervention_priority': 'unknown'
        }
        
        # Cohérence scores A1 vs A2
        a1_score = a1_results.get('score_final', 0)
        a2_score = a2_results.get('score_comportemental', 0)
        
        if a1_score > 0 and a2_score > 0:
            score_diff = abs(a1_score - a2_score)
            analysis['coherence_score'] = max(0, 100 - score_diff)
            
            # Alignement perception vs observation
            if score_diff <= 10:
                analysis['alignment_perception_observation'] = 'excellent'
            elif score_diff <= 20:
                analysis['alignment_perception_observation'] = 'bon'
            elif score_diff <= 30:
                analysis['alignment_perception_observation'] = 'modere'
            else:
                analysis['alignment_perception_observation'] = 'faible'
                analysis['zones_aveugles_detected'] = True
        
        # Consistance comportementale
        a1_risk_factors = len(a1_results.get('behavioral_risk_factors', []))
        a2_concerns = len(a2_results.get('behavioral_concerns', []))
        
        total_issues = a1_risk_factors + a2_concerns
        if total_issues == 0:
            analysis['behavioral_consistency'] = 'excellent'
            analysis['overall_risk_level'] = 'faible'
        elif total_issues <= 2:
            analysis['behavioral_consistency'] = 'bon'
            analysis['overall_risk_level'] = 'modere'
        elif total_issues <= 4:
            analysis['behavioral_consistency'] = 'modere'
            analysis['overall_risk_level'] = 'eleve'
        else:
            analysis['behavioral_consistency'] = 'faible'
            analysis['overall_risk_level'] = 'critique'
        
        # Priorisation interventions
        if analysis['zones_aveugles_detected'] or analysis['overall_risk_level'] == 'critique':
            analysis['intervention_priority'] = 'urgente'
        elif analysis['overall_risk_level'] == 'eleve':
            analysis['intervention_priority'] = 'haute'
        elif analysis['overall_risk_level'] == 'modere':
            analysis['intervention_priority'] = 'moyenne'
        else:
            analysis['intervention_priority'] = 'faible'
        
        # Recommandations intégrées
        a1_recommendations = a1_results.get('recommandations', [])
        a2_recommendations = a2_results.get('recommandations', [])
        
        # Fusion intelligente recommandations
        analysis['integrated_recommendations'] = self._merge_recommendations(
            a1_recommendations, a2_recommendations, analysis
        )
        
        return analysis
    
    def _merge_recommendations(self, a1_recs: List[Dict], a2_recs: List[Dict], 
                             analysis: Dict) -> List[Dict]:
        """Fusionne recommandations A1 et A2 intelligemment"""
        
        integrated = []
        
        # Recommandations urgentes si zones aveugles
        if analysis.get('zones_aveugles_detected'):
            integrated.append({
                'description': 'ZONES AVEUGLES DÉTECTÉES - Analyse écart perception/réalité critique',
                'priority': 'Critical',
                'type': 'zone_aveugle_intervention',
                'effort_days': 1,
                'source': 'integration_behaviorx',
                'a1_a2_gap': abs(analysis.get('coherence_score', 100) - 100)
            })
        
        # Ajout recommandations A1 (Safe Self)
        for rec in a1_recs:
            if 'behaviorx' in rec.get('source', ''):
                integrated.append({
                    **rec,
                    'integration_source': 'a1_safe_self'
                })
        
        # Ajout recommandations A2 (VCS/ABC)
        for rec in a2_recs:
            if rec.get('priority') in ['High', 'Critical']:
                integrated.append({
                    **rec,
                    'integration_source': 'a2_vcs_abc'
                })
        
        # Recommandation de suivi intégré
        integrated.append({
            'description': 'Suivi intégré A1+A2 BehaviorX dans 1 semaine',
            'priority': 'Medium',
            'type': 'follow_up_integration',
            'effort_days': 0,
            'source': 'integration_behaviorx',
            'next_evaluation_date': '1 semaine'
        })
        
        return integrated
    
    def _display_integration_analysis(self, analysis: Dict):
        """Affiche analyse d'intégration"""
        
        print(f"🎯 Score cohérence A1↔A2: {analysis.get('coherence_score', 0):.1f}%")
        print(f"🔗 Alignement perception↔observation: {analysis.get('alignment_perception_observation', 'unknown')}")
        print(f"🧠 Consistance comportementale: {analysis.get('behavioral_consistency', 'unknown')}")
        print(f"⚠️  Niveau risque global: {analysis.get('overall_risk_level', 'unknown')}")
        print(f"🚨 Zones aveugles détectées: {'OUI' if analysis.get('zones_aveugles_detected') else 'NON'}")
        print(f"📈 Priorité intervention: {analysis.get('intervention_priority', 'unknown')}")
        print(f"💡 Recommandations intégrées: {len(analysis.get('integrated_recommendations', []))}")
        
        # Recommandations critiques
        critical_recs = [r for r in analysis.get('integrated_recommendations', []) 
                        if r.get('priority') in ['Critical', 'High']]
        if critical_recs:
            print(f"\n🚨 RECOMMANDATIONS CRITIQUES:")
            for i, rec in enumerate(critical_recs, 1):
                print(f"   {i}. {rec.get('description', 'N/A')} (Priorité: {rec.get('priority', 'N/A')})")

def main():
    """Fonction principale test intégration"""
    
    print("🧪 TEST INTÉGRATION A1+A2 BEHAVIORX ENHANCED")
    print("=" * 60)
    
    # Initialisation testeur
    tester = IntegrationTesterBehaviorX()
    
    # Scénarios de test
    scenarios = [
        {
            'name': 'Construction - Chantier à risque élevé',
            'company': 'ConstructionTest_BehaviorX',
            'secteur': '236 - Construction',
            'context': {
                'secteur_scian': '236 - Construction',
                'site': 'Chantier Test Intégration',
                'observer': 'Superviseur BehaviorX',
                'shift': 'matin',
                'time_pressure': True,
                'weather': 'pluvieux'
            },
            'a1_test_data': {
                'questions': [
                    {'question': 'Procédures sécurité claires et appliquées ?', 'reponse': 'Partiellement'},
                    {'question': 'EPI disponibles et utilisés systématiquement ?', 'reponse': 'Oui'},
                    {'question': 'Supervision sécurité présente et active ?', 'reponse': 'Non'},
                    {'question': 'Formation sécurité récente et adaptée ?', 'reponse': 'Partiellement'},
                    {'question': 'Communication risques efficace équipe ?', 'reponse': 'Non'}
                ],
                'domaine': 'construction',
                'secteur_scian': '236'
            }
        },
        {
            'name': 'Construction - Chantier sécurisé',
            'company': 'ConstructionExcellente_BehaviorX',
            'secteur': '236 - Construction',
            'context': {
                'secteur_scian': '236 - Construction',
                'site': 'Chantier Modèle BehaviorX',
                'observer': 'Expert Sécurité',
                'shift': 'journée',
                'time_pressure': False,
                'weather': 'ensoleillé'
            },
            'a1_test_data': {
                'questions': [
                    {'question': 'Procédures sécurité claires et appliquées ?', 'reponse': 'Oui'},
                    {'question': 'EPI disponibles et utilisés systématiquement ?', 'reponse': 'Oui'},
                    {'question': 'Supervision sécurité présente et active ?', 'reponse': 'Oui'},
                    {'question': 'Formation sécurité récente et adaptée ?', 'reponse': 'Oui'},
                    {'question': 'Communication risques efficace équipe ?', 'reponse': 'Oui'}
                ],
                'domaine': 'construction',
                'secteur_scian': '236'
            }
        }
    ]
    
    # Exécution tests
    all_results = []
    for scenario in scenarios:
        result = tester.run_integration_test(scenario)
        all_results.append(result)
    
    # Synthèse finale
    print("\n" + "=" * 60)
    print("📊 SYNTHÈSE TESTS INTÉGRATION BEHAVIORX")
    print("=" * 60)
    
    for i, result in enumerate(all_results, 1):
        if 'error' not in result:
            analysis = result.get('integration_analysis', {})
            print(f"\n🧪 Test {i}: {result['scenario']}")
            print(f"   Cohérence A1↔A2: {analysis.get('coherence_score', 0):.1f}%")
            print(f"   Zones aveugles: {'OUI' if analysis.get('zones_aveugles_detected') else 'NON'}")
            print(f"   Priorité: {analysis.get('intervention_priority', 'unknown')}")
        else:
            print(f"\n❌ Test {i}: ÉCHEC - {result.get('error', 'Erreur inconnue')}")
    
    print(f"\n✅ ÉTAPE 1.3 TERMINÉE - {len([r for r in all_results if 'error' not in r])}/{len(all_results)} tests réussis")

if __name__ == "__main__":
    main()