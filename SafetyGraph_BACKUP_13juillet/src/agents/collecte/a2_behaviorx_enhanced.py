"""
Agent A2 BehaviorX Enhanced - Observations VCS + ABC
===================================================

ÉTAPE 1.2 - Extension Agent A2 avec BehaviorX
Mode 6 : VCS (Visite Comportementale Sécurité) + ABC Framework
"""

import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

print("🔍 Agent A2 BehaviorX Enhanced - Initialisation")

class VCSObservationEngine:
    """Moteur VCS (Visite Comportementale Sécurité) BehaviorX"""
    
    def __init__(self):
        print("🎯 Initialisation VCS Observation Engine")
        self.vcs_categories = {
            'positioning_movement': 'Positionnement et mouvement',
            'epi_usage': 'Utilisation EPI', 
            'tools_equipment': 'Outils et équipements',
            'procedures_compliance': 'Respect des procédures',
            'communication_interaction': 'Communication et interaction',
            'attention_focus': 'Attention et concentration',
            'risk_perception': 'Perception du risque',
            'proactive_safety': 'Sécurité proactive'
        }
        
    def generate_vcs_checklist(self, context: Dict) -> List[Dict]:
        """Génère checklist VCS adaptée au contexte"""
        
        sector = context.get('secteur_scian', '236')
        
        base_checklist = [
            {
                'id': 'pos_1',
                'category': 'positioning_movement',
                'observation': 'Position de travail stable et équilibrée',
                'type': 'binary',
                'behavioral_focus': 'body_mechanics'
            },
            {
                'id': 'epi_1', 
                'category': 'epi_usage',
                'observation': 'Port effectif et correct des EPI requis',
                'type': 'binary',
                'behavioral_focus': 'compliance'
            },
            {
                'id': 'tools_1',
                'category': 'tools_equipment', 
                'observation': 'Inspection visuelle outils avant utilisation',
                'type': 'binary',
                'behavioral_focus': 'preparation'
            },
            {
                'id': 'proc_1',
                'category': 'procedures_compliance',
                'observation': 'Respect séquence procédure établie', 
                'type': 'binary',
                'behavioral_focus': 'adherence'
            },
            {
                'id': 'comm_1',
                'category': 'communication_interaction',
                'observation': 'Communication claire avant manœuvres',
                'type': 'binary', 
                'behavioral_focus': 'coordination'
            },
            {
                'id': 'att_1',
                'category': 'attention_focus',
                'observation': 'Attention soutenue sur la tâche',
                'type': 'scale',
                'scale': [1, 5],
                'behavioral_focus': 'vigilance'
            },
            {
                'id': 'risk_1',
                'category': 'risk_perception',
                'observation': 'Identification spontanée des dangers',
                'type': 'binary',
                'behavioral_focus': 'awareness'
            },
            {
                'id': 'proact_1',
                'category': 'proactive_safety',
                'observation': 'Initiative d\'amélioration sécurité',
                'type': 'binary', 
                'behavioral_focus': 'leadership'
            }
        ]
        
        # Adaptation sectorielle Construction
        if sector.startswith('236'):
            base_checklist.extend([
                {
                    'id': 'const_1',
                    'category': 'positioning_movement',
                    'observation': 'Respect zone de sécurité autour équipements',
                    'type': 'binary',
                    'behavioral_focus': 'spatial_awareness'
                },
                {
                    'id': 'const_2',
                    'category': 'tools_equipment',
                    'observation': 'Vérification stabilité échafaudages/échelles',
                    'type': 'binary',
                    'behavioral_focus': 'verification'
                }
            ])
            
        print(f"✅ Checklist VCS générée: {len(base_checklist)} items pour secteur {sector}")
        return base_checklist
    
    def analyze_vcs_observations(self, observations: List[Dict]) -> Dict:
        """Analyse observations VCS pour indicateurs comportementaux"""
        
        analysis = {
            'compliance_rate': 0.0,
            'behavioral_strengths': [],
            'behavioral_concerns': [], 
            'category_scores': {},
            'improvement_opportunities': []
        }
        
        # Calcul taux conformité global
        binary_observations = [obs for obs in observations if obs.get('type') == 'binary']
        if binary_observations:
            compliant_count = sum(1 for obs in binary_observations if obs.get('value') == True)
            analysis['compliance_rate'] = compliant_count / len(binary_observations) * 100
        
        # Analyse par catégorie
        categories = {}
        for obs in observations:
            cat = obs.get('category', 'unknown')
            if cat not in categories:
                categories[cat] = {'total': 0, 'positive': 0}
            categories[cat]['total'] += 1
            if obs.get('value') in [True, 4, 5]:  # Valeurs positives
                categories[cat]['positive'] += 1
        
        # Calcul scores par catégorie
        for cat, data in categories.items():
            if data['total'] > 0:
                score = (data['positive'] / data['total']) * 100
                analysis['category_scores'][cat] = score
                
                if score >= 80:
                    analysis['behavioral_strengths'].append(cat)
                elif score < 60:
                    analysis['behavioral_concerns'].append(cat)
        
        # Opportunités d'amélioration
        if analysis['compliance_rate'] < 80:
            analysis['improvement_opportunities'].append({
                'type': 'general_compliance',
                'priority': 'high',
                'description': f'Taux conformité {analysis["compliance_rate"]:.1f}% à améliorer'
            })
            
        for concern in analysis['behavioral_concerns']:
            analysis['improvement_opportunities'].append({
                'type': 'category_specific',
                'priority': 'medium',
                'category': concern,
                'description': f'Catégorie {concern} nécessite attention'
            })
        
        print(f"📊 Analyse VCS: {analysis['compliance_rate']:.1f}% conformité, {len(analysis['behavioral_strengths'])} forces, {len(analysis['behavioral_concerns'])} préoccupations")
        return analysis

class ABCObservationFramework:
    """Framework ABC (Antécédent-Comportement-Conséquence) BehaviorX"""
    
    def __init__(self):
        print("📋 Initialisation ABC Framework")
        self.abc_model = {
            'antecedents': {
                'environmental': ['weather', 'noise', 'lighting', 'space'],
                'organizational': ['time_pressure', 'supervision', 'procedures', 'training'],
                'personal': ['fatigue', 'stress', 'motivation', 'competence'],
                'social': ['peer_influence', 'culture', 'communication']
            },
            'behaviors': {
                'safe': ['epi_usage', 'procedure_following', 'communication', 'vigilance'],
                'unsafe': ['shortcuts', 'risk_taking', 'non_compliance', 'distraction'],
                'proactive': ['hazard_reporting', 'peer_coaching', 'improvement_suggestions']
            },
            'consequences': {
                'immediate': ['comfort', 'efficiency', 'social_approval', 'task_completion'],
                'delayed': ['safety_outcomes', 'learning', 'habit_formation']
            }
        }
    
    def structure_abc_observation(self, raw_observation: Dict) -> Dict:
        """Structure observation selon modèle ABC"""
        
        abc_structured = {
            'observation_id': raw_observation.get('id', str(uuid.uuid4())),
            'timestamp': datetime.now().isoformat(),
            'context': raw_observation.get('context', {}),
            'abc_analysis': {
                'antecedents': [],
                'behaviors': [],
                'consequences': []
            },
            'behavioral_chain': [],
            'intervention_points': []
        }
        
        # Extraction comportements observés
        behaviors = raw_observation.get('behaviors_observed', [])
        for behavior in behaviors:
            behavior_type = self._classify_behavior(behavior)
            abc_structured['abc_analysis']['behaviors'].append({
                'behavior': behavior.get('action', behavior.get('observation', '')),
                'type': behavior_type,
                'compliant': behavior.get('compliant', behavior.get('value', False)),
                'safety_impact': self._assess_safety_impact(behavior_type)
            })
        
        # Identification points d'intervention
        abc_structured['intervention_points'] = self._identify_intervention_points(
            abc_structured['abc_analysis']
        )
        
        print(f"🔗 ABC structuré: {len(abc_structured['abc_analysis']['behaviors'])} comportements, {len(abc_structured['intervention_points'])} interventions")
        return abc_structured
    
    def _classify_behavior(self, behavior: Dict) -> str:
        """Classifie comportement selon catégories ABC"""
        action = str(behavior.get('action', behavior.get('observation', ''))).lower()
        
        # Comportements sûrs
        safe_keywords = ['epi', 'procedure', 'check', 'communication', 'signal', 'inspection']
        if any(keyword in action for keyword in safe_keywords):
            return 'safe'
        
        # Comportements non sûrs  
        unsafe_keywords = ['shortcut', 'skip', 'ignore', 'rush', 'bypass']
        if any(keyword in action for keyword in unsafe_keywords):
            return 'unsafe'
            
        # Comportements proactifs
        proactive_keywords = ['suggest', 'improve', 'report', 'help', 'initiative']
        if any(keyword in action for keyword in proactive_keywords):
            return 'proactive'
            
        return 'neutral'
    
    def _assess_safety_impact(self, behavior_type: str) -> str:
        """Évalue impact sécurité d'un comportement"""
        impact_mapping = {
            'safe': 'positive',
            'unsafe': 'negative',
            'proactive': 'very_positive',
            'neutral': 'neutral'
        }
        return impact_mapping.get(behavior_type, 'neutral')
    
    def _identify_intervention_points(self, abc_analysis: Dict) -> List[Dict]:
        """Identifie points d'intervention optimaux"""
        intervention_points = []
        
        # Comportements à modifier/renforcer
        for behavior in abc_analysis.get('behaviors', []):
            if behavior.get('type') == 'unsafe':
                intervention_points.append({
                    'type': 'behavior_modification',
                    'target': behavior.get('behavior'),
                    'priority': 'high',
                    'description': f'Modifier comportement unsafe: {behavior.get("behavior")}'
                })
            elif behavior.get('type') == 'safe' and behavior.get('compliant'):
                intervention_points.append({
                    'type': 'behavior_reinforcement',
                    'target': behavior.get('behavior'),
                    'priority': 'medium', 
                    'description': f'Renforcer comportement safe: {behavior.get("behavior")}'
                })
        
        return intervention_points

class AgentA2BehaviorXEnhanced:
    """Agent A2 Enhanced avec intégration BehaviorX - Mode 6 VCS + ABC"""
    
    def __init__(self):
        print("🤖 Agent A2 BehaviorX Enhanced - Initialisation")
        self.modes_available = {
            'mode_1': 'Données réelles terrain',
            'mode_2': 'Données synthétiques statistiques', 
            'mode_3': 'Mode hybride intelligent',
            'mode_4': 'Mode démonstration',
            'mode_5': 'Mode test validation',
            'mode_6_vcs': 'VCS BehaviorX + ABC'  # NOUVEAU MODE
        }
        
        self.vcs_engine = VCSObservationEngine()
        self.abc_framework = ABCObservationFramework()
        self.behaviorx_version = "1.0"
        print(f"✅ Agent A2 BehaviorX Enhanced v{self.behaviorx_version} prêt")
    
    def process_observations_behaviorx(self, context: Dict, mode: str = 'mode_6_vcs') -> Dict:
        """Traitement observations avec BehaviorX VCS + ABC"""
        
        print(f"🔍 Agent A2 BehaviorX - Mode {mode}")
        print(f"📊 Contexte: {context.get('secteur_scian', 'Non défini')}")
        
        if mode == 'mode_6_vcs':
            return self._process_vcs_abc_mode(context)
        else:
            # Fallback vers modes existants (simulation)
            return self._process_standard_mode(context, mode)
    
    def _process_vcs_abc_mode(self, context: Dict) -> Dict:
        """Mode 6 : VCS + ABC observations"""
        
        try:
            # Étape 1: Génération checklist VCS
            vcs_checklist = self.vcs_engine.generate_vcs_checklist(context)
            
            # Étape 2: Simulation observations VCS
            vcs_observations = self._simulate_vcs_observations(vcs_checklist, context)
            
            # Étape 3: Analyse VCS
            vcs_analysis = self.vcs_engine.analyze_vcs_observations(vcs_observations)
            
            # Étape 4: Structure ABC
            abc_observation = self._create_abc_observation(vcs_observations, context)
            abc_structured = self.abc_framework.structure_abc_observation(abc_observation)
            
            # Étape 5: Génération résultat A2 enrichi
            result = self._generate_a2_behaviorx_result(vcs_analysis, abc_structured, context)
            
            return result
            
        except Exception as e:
            print(f"❌ Erreur Mode VCS: {e}")
            return self._generate_fallback_result(context)
    
    def _simulate_vcs_observations(self, checklist: List[Dict], context: Dict) -> List[Dict]:
        """Simulation observations VCS (en production = vraies observations)"""
        
        observations = []
        
        for item in checklist:
            observation = {
                'id': item['id'],
                'category': item['category'],
                'observation': item['observation'],
                'type': item['type'],
                'behavioral_focus': item['behavioral_focus'],
                'timestamp': datetime.now().isoformat()
            }
            
            # Simulation valeurs réalistes (80% conformité moyenne)
            if item['type'] == 'binary':
                observation['value'] = True if hash(item['id']) % 5 != 0 else False
            elif item['type'] == 'scale':
                observation['value'] = min(5, max(1, 3 + (hash(item['id']) % 3)))
            
            observations.append(observation)
        
        print(f"📝 {len(observations)} observations VCS simulées")
        return observations
    
    def _create_abc_observation(self, vcs_observations: List[Dict], context: Dict) -> Dict:
        """Crée observation structurée ABC à partir VCS"""
        
        abc_observation = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'context': {
                'sector': context.get('secteur_scian', '236'),
                'site': context.get('site', 'Site Test'),
                'supervision_present': True,
                'weather': 'normal'
            },
            'behaviors_observed': []
        }
        
        # Conversion observations VCS en comportements ABC
        for obs in vcs_observations:
            behavior = {
                'action': obs['observation'],
                'category': obs['category'],
                'compliant': obs.get('value', False),
                'observation_type': obs['type']
            }
            abc_observation['behaviors_observed'].append(behavior)
        
        return abc_observation
    
    def _generate_a2_behaviorx_result(self, vcs_analysis: Dict, abc_structured: Dict, context: Dict) -> Dict:
        """Génère résultat A2 enrichi BehaviorX"""
        
        # Score comportemental composite
        compliance_rate = vcs_analysis['compliance_rate']
        behavioral_bonus = self._calculate_behavioral_bonus(abc_structured)
        behavioral_score = min(100, compliance_rate + behavioral_bonus)
        
        # Classification sécurité comportementale
        if behavioral_score >= 85:
            niveau_comportemental = 'EXCELLENT_COMPORTEMENTAL'
            couleur = '#10B981'  # Vert
        elif behavioral_score >= 70:
            niveau_comportemental = 'BON_COMPORTEMENTAL'
            couleur = '#F59E0B'  # Orange
        elif behavioral_score >= 50:
            niveau_comportemental = 'ATTENTION_COMPORTEMENTALE'
            couleur = '#F59E0B'  # Orange
        else:
            niveau_comportemental = 'CRITIQUE_COMPORTEMENTAL'
            couleur = '#DC2626'  # Rouge
        
        # Recommandations BehaviorX
        behaviorx_recommendations = self._generate_behaviorx_recommendations(vcs_analysis, abc_structured)
        
        return {
            'mode_utilise': 'mode_6_vcs_behaviorx',
            'score_comportemental': behavioral_score,
            'niveau_comportemental': niveau_comportemental,
            'couleur_indicateur': couleur,
            'taux_conformite_vcs': compliance_rate,
            'categories_evaluation': len(vcs_analysis['category_scores']),
            'recommandations': behaviorx_recommendations,
            'timestamp': datetime.now().isoformat(),
            'agent_version': f"A2_BehaviorX_Enhanced_{self.behaviorx_version}",
            
            # Données VCS détaillées
            'vcs_analysis': vcs_analysis,
            'abc_structured': abc_structured,
            'behavioral_strengths': vcs_analysis['behavioral_strengths'],
            'behavioral_concerns': vcs_analysis['behavioral_concerns'],
            'intervention_points': abc_structured['intervention_points'],
            
            # Métadonnées
            'behaviorx_enhanced': True,
            'observation_count': len(abc_structured.get('abc_analysis', {}).get('behaviors', [])),
            'enhancement_type': 'vcs_abc_integration',
            'source': 'A2_BehaviorX_Enhanced'
        }
    
    def _calculate_behavioral_bonus(self, abc_structured: Dict) -> float:
        """Calcule bonus basé sur analyse ABC"""
        
        bonus = 0.0
        
        # Bonus pour comportements proactifs
        behaviors = abc_structured.get('abc_analysis', {}).get('behaviors', [])
        proactive_count = sum(1 for b in behaviors if b.get('type') == 'proactive')
        bonus += proactive_count * 5.0
        
        # Bonus pour comportements sûrs
        safe_count = sum(1 for b in behaviors if b.get('type') == 'safe' and b.get('compliant'))
        bonus += safe_count * 2.0
        
        return min(15.0, bonus)  # Maximum +15 points
    
    def _generate_behaviorx_recommendations(self, vcs_analysis: Dict, abc_structured: Dict) -> List[Dict]:
        """Génère recommandations spécifiques BehaviorX"""
        
        recommendations = []
        
        # Recommandations basées sur préoccupations VCS
        for concern in vcs_analysis.get('behavioral_concerns', []):
            recommendations.append({
                'description': f'Amélioration ciblée catégorie {concern}',
                'priority': 'High',
                'type': 'vcs_improvement',
                'effort_days': 1,
                'source': 'behaviorx_vcs',
                'category_target': concern
            })
        
        # Recommandations basées sur points d'intervention ABC
        for intervention in abc_structured.get('intervention_points', []):
            if intervention.get('priority') == 'high':
                recommendations.append({
                    'description': intervention.get('description'),
                    'priority': 'High',
                    'type': 'abc_intervention',
                    'effort_days': 2,
                    'source': 'behaviorx_abc',
                    'intervention_type': intervention.get('type')
                })
        
        # Recommandations de renforcement
        for strength in vcs_analysis.get('behavioral_strengths', []):
            recommendations.append({
                'description': f'Maintenir excellence catégorie {strength}',
                'priority': 'Low',
                'type': 'reinforcement', 
                'effort_days': 0,
                'source': 'behaviorx_vcs',
                'category_target': strength
            })
        
        print(f"💡 {len(recommendations)} recommandations BehaviorX générées")
        return recommendations
    
    def _process_standard_mode(self, context: Dict, mode: str) -> Dict:
        """Modes standard A2 (fallback)"""
        return {
            'mode_utilise': mode,
            'score_comportemental': 75.0,
            'niveau_comportemental': 'STANDARD',
            'couleur_indicateur': '#6B7280',
            'timestamp': datetime.now().isoformat(),
            'source': 'A2_Standard_Fallback'
        }
    
    def _generate_fallback_result(self, context: Dict) -> Dict:
        """Résultat de secours"""
        return {
            'mode_utilise': 'fallback',
            'score_comportemental': 70.0,
            'niveau_comportemental': 'FALLBACK', 
            'error': 'Mode BehaviorX indisponible',
            'timestamp': datetime.now().isoformat(),
            'source': 'A2_Fallback'
        }

# Test intégration A2 BehaviorX
if __name__ == "__main__":
    print("🧪 TEST AGENT A2 BEHAVIORX ENHANCED")
    print("=" * 50)
    
    # Initialisation
    agent_a2 = AgentA2BehaviorXEnhanced()
    
    # Contexte test
    test_context = {
        'secteur_scian': '236 - Construction',
        'site': 'Chantier Test BehaviorX',
        'observer': 'Superviseur Test',
        'shift': 'matin'
    }
    
    # Test Mode 6 VCS
    result = agent_a2.process_observations_behaviorx(test_context, mode='mode_6_vcs')
    
    print("\n🎯 RÉSULTATS A2 BEHAVIORX:")
    print(f"Score comportemental: {result['score_comportemental']}")
    print(f"Niveau: {result['niveau_comportemental']}")
    print(f"Taux conformité VCS: {result.get('taux_conformite_vcs', 0):.1f}%")
    print(f"Forces comportementales: {len(result.get('behavioral_strengths', []))}")
    print(f"Préoccupations: {len(result.get('behavioral_concerns', []))}")
    print(f"Points d'intervention: {len(result.get('intervention_points', []))}")
    print(f"Recommandations: {len(result.get('recommandations', []))}")
    
    print("\n✅ ÉTAPE 1.2 TERMINÉE !")