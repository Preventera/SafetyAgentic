"""
Agent A1 BehaviorX Enhanced - Safe Self + Mémoire IA
===================================================

ÉTAPE 1.1 - Intégration BehaviorX dans SafeGraph
Fusion Agent A1 Enhanced (mémoire) + Safe Self BehaviorX
"""

import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

# Import Agent A1 Enhanced existant
try:
    sys.path.append("../../")  # Remonter pour accéder aux modules
    from agents.collecte.a1_enhanced_memory import AgentA1Enhanced
    from memory.wrapper import get_memory, store_agent_memory
    print("✅ Import Agent A1 Enhanced réussi")
except ImportError as e:
    print(f"⚠️ Import Agent A1 Enhanced échoué: {e}")
    print("Mode simulation activé")
    
    # Classe de simulation si import échoue
    class AgentA1Enhanced:
        def __init__(self):
            pass
            
        def process_with_memory(self, data, company, secteur):
            return {
                'score_final': 75.0,
                'niveau_securite': 'ACCEPTABLE',
                'recommandations': [],
                'enhanced_by_memory': False
            }

class SafeSelfEvaluator:
    """Module Safe Self de BehaviorX - Autoévaluation comportementale"""
    
    def __init__(self):
        print("🧠 Initialisation Safe Self BehaviorX")
        self.behavioral_dimensions = {
            'attention_focus': 'Niveau d\'attention et concentration',
            'stress_level': 'Niveau de stress perçu', 
            'fatigue_state': 'État de fatigue physique/mentale',
            'risk_perception': 'Perception personnelle du risque',
            'safety_motivation': 'Motivation sécurité intrinsèque'
        }
        
    def generate_safe_self_questions(self, context: Dict) -> List[Dict]:
        """Génère questionnaire Safe Self adapté"""
        
        questions = [
            {
                'id': 'attention_1',
                'dimension': 'attention_focus',
                'question': 'Sur une échelle de 1 à 10, comment évaluez-vous votre niveau d\'attention aujourd\'hui ?',
                'type': 'scale',
                'scale': [1, 10]
            },
            {
                'id': 'stress_1', 
                'dimension': 'stress_level',
                'question': 'Ressentez-vous du stress qui pourrait affecter votre sécurité ?',
                'type': 'choice',
                'options': ['Aucun stress', 'Stress léger', 'Stress modéré', 'Stress élevé']
            },
            {
                'id': 'fatigue_1',
                'dimension': 'fatigue_state', 
                'question': 'Votre niveau de fatigue pourrait-il influencer votre sécurité ?',
                'type': 'boolean'
            },
            {
                'id': 'risk_perception_1',
                'dimension': 'risk_perception',
                'question': 'Comment percevez-vous le niveau de risque de vos tâches ?',
                'type': 'choice',
                'options': ['Très faible', 'Faible', 'Modéré', 'Élevé', 'Très élevé']
            },
            {
                'id': 'motivation_1',
                'dimension': 'safety_motivation',
                'question': 'À quel point êtes-vous motivé à respecter les procédures de sécurité ?',
                'type': 'scale', 
                'scale': [1, 10]
            }
        ]
        
        # Adaptation sectorielle
        secteur = context.get('secteur_scian', '236')
        if secteur.startswith('236'):  # Construction
            questions.append({
                'id': 'construction_epi',
                'dimension': 'risk_perception',
                'question': 'Vous sentez-vous parfaitement équipé en EPI pour vos tâches ?',
                'type': 'boolean'
            })
            
        print(f"✅ {len(questions)} questions Safe Self générées pour secteur {secteur}")
        return questions
    
    def analyze_safe_self_responses(self, responses: List[Dict]) -> Dict:
        """Analyse réponses Safe Self pour indicateurs comportementaux"""
        
        indicators = {
            'attention_score': 0,
            'stress_risk_level': 'low',
            'fatigue_impact': False,
            'risk_awareness_level': 'moderate',
            'safety_motivation_score': 0,
            'behavioral_risk_factors': [],
            'protective_factors': []
        }
        
        for response in responses:
            dimension = response.get('dimension')
            value = response.get('value')
            
            if dimension == 'attention_focus' and isinstance(value, (int, float)):
                indicators['attention_score'] = value
                if value < 6:
                    indicators['behavioral_risk_factors'].append('attention_deficit')
                elif value >= 8:
                    indicators['protective_factors'].append('high_attention')
                    
            elif dimension == 'stress_level':
                stress_map = {'Aucun stress': 'low', 'Stress léger': 'low',
                             'Stress modéré': 'moderate', 'Stress élevé': 'high'}
                indicators['stress_risk_level'] = stress_map.get(value, 'moderate')
                if indicators['stress_risk_level'] == 'high':
                    indicators['behavioral_risk_factors'].append('high_stress')
                    
            elif dimension == 'fatigue_state':
                indicators['fatigue_impact'] = bool(value)
                if indicators['fatigue_impact']:
                    indicators['behavioral_risk_factors'].append('fatigue_impact')
                    
            elif dimension == 'safety_motivation' and isinstance(value, (int, float)):
                indicators['safety_motivation_score'] = value
                if value < 6:
                    indicators['behavioral_risk_factors'].append('low_motivation')
                elif value >= 8:
                    indicators['protective_factors'].append('high_motivation')
        
        print(f"🧠 Analyse Safe Self: {len(indicators['behavioral_risk_factors'])} risques, {len(indicators['protective_factors'])} protections")
        return indicators

class AgentA1BehaviorXEnhanced(AgentA1Enhanced):
    """Agent A1 Enhanced + BehaviorX Safe Self"""
    
    def __init__(self):
        super().__init__()
        self.safe_self = SafeSelfEvaluator()
        self.behaviorx_version = "1.0"
        print("🤖 Agent A1 BehaviorX Enhanced initialisé")
        
    def process_with_behaviorx_memory(self, data: Dict, company: str, secteur: str) -> Dict:
        """Traitement intégré BehaviorX + Mémoire IA"""
        
        print(f"🚀 Agent A1 BehaviorX - Traitement pour {company}")
        print(f"📊 Secteur: {secteur}")
        
        try:
            # Étape 1: Contexte Safe Self
            context = {
                'secteur_scian': secteur,
                'company': company, 
                'timestamp': datetime.now().isoformat()
            }
            
            # Étape 2: Questions Safe Self
            safe_self_questions = self.safe_self.generate_safe_self_questions(context)
            
            # Étape 3: Simulation réponses (en production = vraies réponses)
            simulated_responses = self._simulate_safe_self_responses(safe_self_questions)
            
            # Étape 4: Analyse Safe Self
            safe_self_indicators = self.safe_self.analyze_safe_self_responses(simulated_responses)
            
            # Étape 5: Autoévaluation classique SafeGraph
            classical_evaluation = self.process_with_memory(data, company, secteur)
            
            # Étape 6: Fusion BehaviorX + SafeGraph
            integrated_result = self._integrate_behaviorx_safegraph(
                classical_evaluation, safe_self_indicators, context
            )
            
            print(f"✅ Score intégré: {integrated_result['score_final']}")
            print(f"🎯 Niveau: {integrated_result['niveau_securite']}")
            
            return integrated_result
            
        except Exception as e:
            print(f"❌ Erreur Agent A1 BehaviorX: {e}")
            # Fallback vers Agent A1 Enhanced standard
            return self.process_with_memory(data, company, secteur)
    
    def _simulate_safe_self_responses(self, questions: List[Dict]) -> List[Dict]:
        """Simulation réponses Safe Self (en production = vraies réponses)"""
        
        responses = []
        for question in questions:
            response = {
                'question_id': question['id'],
                'dimension': question['dimension'],
                'timestamp': datetime.now().isoformat()
            }
            
            # Simulation réaliste
            if question['type'] == 'scale':
                response['value'] = 7  # Score moyen réaliste
            elif question['type'] == 'choice':
                response['value'] = question['options'][1]  # 2ème option
            elif question['type'] == 'boolean':
                response['value'] = True  # Réponse positive par défaut
                
            responses.append(response)
            
        print(f"📝 {len(responses)} réponses Safe Self simulées")
        return responses
    
    def _integrate_behaviorx_safegraph(self, classical_result: Dict, safe_self: Dict, context: Dict) -> Dict:
        """Intégration résultats BehaviorX + SafeGraph"""
        
        # Score composite enrichi
        classical_score = classical_result.get('score_final', 75.0)
        behavioral_adjustment = self._calculate_behavioral_adjustment(safe_self)
        
        integrated_score = classical_score + behavioral_adjustment
        integrated_score = max(0, min(100, integrated_score))
        
        # Niveau sécurité enrichi comportementalement
        risk_factors = safe_self.get('behavioral_risk_factors', [])
        protective_factors = safe_self.get('protective_factors', [])
        
        if len(risk_factors) >= 3:
            niveau_securite = 'CRITIQUE_COMPORTEMENTAL'
            couleur_indicateur = '#DC2626'  # Rouge
        elif len(risk_factors) >= 2:
            niveau_securite = 'ATTENTION_COMPORTEMENTALE'
            couleur_indicateur = '#F59E0B'  # Orange
        elif len(protective_factors) >= 2:
            niveau_securite = 'EXCELLENT_COMPORTEMENTAL'
            couleur_indicateur = '#10B981'  # Vert
        else:
            niveau_securite = classical_result.get('niveau_securite', 'ACCEPTABLE')
            couleur_indicateur = classical_result.get('couleur_indicateur', '#6B7280')
        
        # Recommandations comportementales
        behaviorx_recommendations = self._generate_behaviorx_recommendations(safe_self)
        classical_recommendations = classical_result.get('recommandations', [])
        all_recommendations = classical_recommendations + behaviorx_recommendations
        
        return {
            # Données SafeGraph enrichies
            'score_final': integrated_score,
            'niveau_securite': niveau_securite,
            'couleur_indicateur': couleur_indicateur,
            'total_questions': classical_result.get('total_questions', 15),
            'domaine': classical_result.get('domaine', 'general'),
            'recommandations': all_recommendations,
            'timestamp': datetime.now().isoformat(),
            'agent_version': f"A1_BehaviorX_Enhanced_{self.behaviorx_version}",
            
            # Nouvelles données BehaviorX
            'safe_self_indicators': safe_self,
            'behavioral_risk_factors': risk_factors,
            'protective_factors': protective_factors,
            'behavioral_score_adjustment': behavioral_adjustment,
            
            # Métadonnées intégration
            'behaviorx_enhanced': True,
            'classical_score_base': classical_score,
            'enhancement_type': 'safe_self_integration',
            'memory_insights': classical_result.get('memory_insights', {}),
            'enhanced_by_memory': classical_result.get('enhanced_by_memory', False),
            'source': 'A1_BehaviorX_Enhanced'
        }
    
    def _calculate_behavioral_adjustment(self, safe_self: Dict) -> float:
        """Calcule ajustement score basé sur comportement"""
        
        adjustment = 0.0
        
        # Pénalités facteurs de risque  
        risk_factors = safe_self.get('behavioral_risk_factors', [])
        adjustment -= len(risk_factors) * 3.0  # -3 points par risque
        
        # Bonus facteurs protecteurs
        protective_factors = safe_self.get('protective_factors', [])
        adjustment += len(protective_factors) * 2.0  # +2 points par protection
        
        # Ajustements spécifiques
        attention_score = safe_self.get('attention_score', 0)
        if attention_score >= 8:
            adjustment += 5.0  # Bonus attention élevée
        elif attention_score <= 4:
            adjustment -= 8.0  # Pénalité attention faible
            
        if safe_self.get('stress_risk_level') == 'high':
            adjustment -= 10.0  # Pénalité stress élevé
            
        motivation_score = safe_self.get('safety_motivation_score', 0)
        if motivation_score >= 8:
            adjustment += 5.0  # Bonus motivation élevée
            
        return max(-25.0, min(25.0, adjustment))  # Bornes ±25 points
    
    def _generate_behaviorx_recommendations(self, safe_self: Dict) -> List[Dict]:
        """Génère recommandations comportementales BehaviorX"""
        
        recommendations = []
        risk_factors = safe_self.get('behavioral_risk_factors', [])
        
        if 'attention_deficit' in risk_factors:
            recommendations.append({
                'description': 'Pause attention de 5 minutes avant tâches critiques',
                'priority': 'High',
                'type': 'behavioral_intervention',
                'effort_days': 0,
                'source': 'behaviorx_safe_self',
                'behavioral_target': 'attention_focus'
            })
        
        if 'high_stress' in risk_factors:
            recommendations.append({
                'description': 'Techniques de gestion du stress avant prise de poste',
                'priority': 'High', 
                'type': 'behavioral_coaching',
                'effort_days': 1,
                'source': 'behaviorx_safe_self',
                'behavioral_target': 'stress_management'
            })
            
        if 'low_motivation' in risk_factors:
            recommendations.append({
                'description': 'Rappel des bénéfices personnels sécurité (famille, santé)',
                'priority': 'Medium',
                'type': 'motivational_enhancement', 
                'effort_days': 0,
                'source': 'behaviorx_safe_self',
                'behavioral_target': 'intrinsic_motivation'
            })
        
        print(f"💡 {len(recommendations)} recommandations BehaviorX générées")
        return recommendations

# Test intégration A1 BehaviorX
if __name__ == "__main__":
    print("🧪 TEST AGENT A1 BEHAVIORX ENHANCED")
    print("=" * 50)
    
    # Initialisation
    agent = AgentA1BehaviorXEnhanced()
    
    # Données test
    test_data = {
        'questions': [
            {'question': 'Procédures sécurité claires ?', 'reponse': 'Oui'},
            {'question': 'Port systématique EPI ?', 'reponse': 'Oui'},
            {'question': 'Supervision sécurité présente ?', 'reponse': 'Partiellement'}
        ],
        'domaine': 'construction',
        'secteur_scian': '236'
    }
    
    # Test intégration
    result = agent.process_with_behaviorx_memory(
        test_data,
        'Construction_BehaviorX_Test',
        '236 - Construction'
    )
    
    print("\n🎯 RÉSULTATS INTÉGRATION:")
    print(f"Score final: {result['score_final']}")
    print(f"Niveau sécurité: {result['niveau_securite']}")
    print(f"Facteurs de risque: {len(result['behavioral_risk_factors'])}")
    print(f"Facteurs protecteurs: {len(result['protective_factors'])}")
    print(f"Enhanced by Memory: {result.get('enhanced_by_memory', False)}")
    
    print("\n✅ ÉTAPE 1.1 TERMINÉE !")