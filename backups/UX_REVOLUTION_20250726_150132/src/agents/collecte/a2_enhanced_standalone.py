"""
Agent A2 Enhanced Standalone avec Mem0
======================================

Version autonome qui ne d�pend pas des agents existants
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from memory.wrapper import add_agent_interaction, get_agent_context
import json
from typing import Dict, List, Any
from datetime import datetime

class AgentA2EnhancedStandalone:
    """
    Agent A2 Enhanced autonome avec m�moire Mem0
    
    Fonctionnalit�s:
    - Traitement observations s�curit�
    - M�moire persistante des interactions
    - Recommandations personnalis�es
    - Apprentissage �volutif des patterns
    """
    
    def __init__(self):
        self.agent_id = "A2"
        self.name = "Agent A2 Enhanced Standalone"
        print(f"? {self.name} initialis� avec m�moire Mem0")
    
    def process_autoevaluation_basic(self, data: Dict) -> Dict:
        """
        Traitement basique d'observation (version standalone)
        """
        questions = data.get('questions', [])
        domaine = data.get('domaine', 'general')
        
        # Calcul score simple
        total_questions = len(questions)
        score_positif = 0
        
        for q in questions:
            reponse = q.get('reponse', '').lower()
            if reponse in ['oui', 'yes', 'vrai', 'true']:
                score_positif += 3
            elif reponse in ['partiellement', 'partially', 'parfois']:
                score_positif += 1.5
            # Non/False = 0 points
        
        score_final = (score_positif / (total_questions * 3)) * 100 if total_questions > 0 else 0
        
        # �valuation qualitative
        if score_final >= 80:
            niveau = "Excellent"
            couleur = "vert"
        elif score_final >= 60:
            niveau = "Bon"
            couleur = "orange"
        else:
            niveau = "� am�liorer"
            couleur = "rouge"
        
        # Recommandations de base
        recommandations = self._generate_basic_recommendations(score_final, questions)
        
        return {
            "score_final": round(score_final, 1),
            "niveau_securite": niveau,
            "couleur_indicateur": couleur,
            "total_questions": total_questions,
            "domaine": domaine,
            "recommandations": recommandations,
            "timestamp": datetime.now().isoformat(),
            "agent_version": "A2_Enhanced_Standalone_v1.0"
        }
    
    def _generate_basic_recommendations(self, score: float, questions: List[Dict]) -> List[str]:
        """G�n�re recommandations basiques selon le score"""
        recommendations = []
        
        if score >= 80:
            recommendations.extend([
                "?? Excellente culture s�curit� ! Maintenez ces bonnes pratiques",
                "?? Partagez vos meilleures pratiques avec d'autres �quipes",
                "?? Continuez les audits r�guliers pour maintenir ce niveau"
            ])
        elif score >= 60:
            recommendations.extend([
                "?? Bon niveau g�n�ral, quelques am�liorations possibles",
                "?? Identifiez les domaines perfectibles",
                "?? Formation compl�mentaire recommand�e"
            ])
        else:
            recommendations.extend([
                "?? Attention : niveau s�curit� insuffisant",
                "?? Formation urgente en s�curit� recommand�e",
                "?? Audit approfondi des proc�dures n�cessaire",
                "? Plan d'action prioritaire � mettre en place"
            ])
        
        # Recommandations sp�cifiques selon les r�ponses
        for q in questions:
            if q.get('reponse', '').lower() in ['non', 'no', 'faux', 'false']:
                question_text = q.get('question', '')[:50]
                recommendations.append(f"?? Action requise: {question_text}...")
        
        return recommendations
    
    def process_with_memory(self, data: Dict, user_id: str = "default", secteur_scian: str = "236") -> Dict:
        """
        Traite observation avec m�moire persistante
        
        Args:
            data: Donn�es observation
            user_id: ID utilisateur/entreprise  
            secteur_scian: Code secteur SCIAN
            
        Returns:
            R�sultat enrichi avec contexte m�moire
        """
        try:
            print(f"?? Traitement observation pour {user_id} (secteur {secteur_scian})")
            
            # 1. R�cup�rer contexte m�moire
            memories = get_agent_context(self.agent_id, user_id, f"autoevaluation {secteur_scian}")
            print(f"?? {len(memories)} m�moires trouv�es dans l'historique")
            
            # 2. Traitement de base
            result = self.process_autoevaluation_basic(data)
            
            # 3. Enrichir avec insights m�moire
            if memories:
                memory_insights = self._analyze_memory_insights(memories, result)
                result["memory_insights"] = memory_insights
                result["enhanced_by_memory"] = True
                print(f"?? R�sultat enrichi avec {memory_insights['historical_evaluations']} �valuations pass�es")
            else:
                result["memory_insights"] = {
                    "historical_evaluations": 0,
                    "status": "premi�re_�valuation",
                    "message": "Premi�re �valuation enregistr�e - L'IA apprendra de vos futurs patterns",
                    "future_benefits": [
                        "Recommandations personnalis�es",
                        "D�tection des tendances d'am�lioration", 
                        "Alertes sur les r�gressions"
                    ]
                }
                result["enhanced_by_memory"] = False
                print("?? Premi�re �valuation - cr�ation de l'historique")
            
            # 4. M�moriser cette interaction
            self._memorize_interaction(user_id, data, result)
            
            return result
            
        except Exception as e:
            print(f"? Erreur A2 Enhanced: {e}")
            # Fallback vers traitement basique
            return self.process_autoevaluation_basic(data)
    
    def _analyze_memory_insights(self, memories: List[Dict], current_result: Dict) -> Dict:
        """Analyse les insights m�moire"""
        
        # Extraire scores historiques
        historical_scores = []
        for memory in memories:
            metadata = memory.get('metadata', {})
            if 'score' in metadata:
                historical_scores.append(metadata['score'])
        
        current_score = current_result.get('score_final', 0)
        
        # Calculer tendance
        trend_analysis = self._calculate_trend_analysis(historical_scores, current_score)
        
        # Recommandations personnalis�es
        personalized_recommendations = self._generate_personalized_recommendations(
            historical_scores, current_score, trend_analysis
        )
        
        return {
            "historical_evaluations": len(memories),
            "previous_scores": historical_scores[-5:],  # 5 derniers scores
            "current_score": current_score,
            "trend_analysis": trend_analysis,
            "personalized_recommendations": personalized_recommendations,
            "improvement_potential": self._calculate_improvement_potential(historical_scores, current_score)
        }
    
    def _calculate_trend_analysis(self, historical_scores: List[float], current_score: float) -> Dict:
        """Calcule l'analyse de tendance"""
        if not historical_scores:
            return {"trend": "no_data", "message": "Pas assez de donn�es historiques"}
        
        if len(historical_scores) == 1:
            prev_score = historical_scores[0]
            change = current_score - prev_score
            if change > 5:
                return {"trend": "improving", "change": change, "message": f"Am�lioration de {change:.1f} points"}
            elif change < -5:
                return {"trend": "declining", "change": change, "message": f"Baisse de {abs(change):.1f} points"}
            else:
                return {"trend": "stable", "change": change, "message": "Score stable"}
        
        # Analyse avec plusieurs points
        recent_avg = sum(historical_scores[-3:]) / min(3, len(historical_scores))
        overall_trend = current_score - recent_avg
        
        if overall_trend > 10:
            return {"trend": "strong_improvement", "change": overall_trend, "message": "Forte am�lioration continue"}
        elif overall_trend > 3:
            return {"trend": "improvement", "change": overall_trend, "message": "Am�lioration progressive"}
        elif overall_trend < -10:
            return {"trend": "concerning_decline", "change": overall_trend, "message": "Baisse pr�occupante"}
        elif overall_trend < -3:
            return {"trend": "decline", "change": overall_trend, "message": "L�g�re r�gression"}
        else:
            return {"trend": "stable", "change": overall_trend, "message": "Performance stable"}
    
    def _generate_personalized_recommendations(self, historical_scores: List[float], current_score: float, trend: Dict) -> List[str]:
        """G�n�re recommandations personnalis�es"""
        recommendations = []
        
        trend_type = trend.get('trend', 'no_data')
        
        if trend_type in ['strong_improvement', 'improvement']:
            recommendations.extend([
                "?? Excellente progression ! Continuez sur cette lanc�e",
                "?? Vos efforts portent leurs fruits - maintenez le cap", 
                "? Partagez vos bonnes pratiques avec d'autres �quipes"
            ])
        elif trend_type in ['concerning_decline', 'decline']:
            recommendations.extend([
                "?? ALERTE: R�gression d�tect�e dans vos pratiques",
                "?? Auditez les changements r�cents dans vos proc�dures",
                "?? Consid�rez une consultation en s�curit� industrielle",
                "? Plan d'action corrective prioritaire recommand�"
            ])
        elif trend_type == 'stable':
            if current_score >= 75:
                recommendations.append("? Performance stable et satisfaisante - continuez")
            else:
                recommendations.extend([
                    "?? Performance stable mais am�liorable",
                    "?? Formation continue recommand�e pour progresser"
                ])
        
        # Recommandations selon niveau actuel
        if current_score < 50:
            recommendations.extend([
                "?? URGENT: Score critique - intervention imm�diate requise",
                "?? Audit complet des pratiques s�curit� n�cessaire"
            ])
        elif current_score < 70:
            recommendations.append("? Score insuffisant - plan d'am�lioration prioritaire")
        
        return recommendations
    
    def _calculate_improvement_potential(self, historical_scores: List[float], current_score: float) -> str:
        """Calcule le potentiel d'am�lioration"""
        if not historical_scores:
            return "Premier diagnostic - potentiel � �tablir"
        
        max_historical = max(historical_scores)
        if current_score >= max_historical:
            return "Performance � son meilleur niveau historique"
        else:
            potential = max_historical - current_score
            return f"Potentiel d'am�lioration: +{potential:.1f} points (meilleur score: {max_historical})"
    
    def _memorize_interaction(self, user_id: str, input_data: Dict, result: Dict):
        """M�morise l'interaction pour apprentissage futur"""
        try:
            # Contenu structur� pour la m�moire
            content = f"""
            observation s�curit� - Secteur: {input_data.get('secteur_scian', 'N/A')}
            Domaine: {input_data.get('domaine', 'general')}
            Questions: {len(input_data.get('questions', []))}
            Score obtenu: {result.get('score_final', 0)}/100
            Niveau: {result.get('niveau_securite', 'N/A')}
            """
            
            # M�tadonn�es enrichies
            metadata = {
                "type": "autoevaluation",
                "agent_version": "A2_Enhanced_Standalone",
                "score": result.get('score_final', 0),
                "niveau": result.get('niveau_securite', 'unknown'),
                "domaine": input_data.get('domaine', 'general'),
                "nb_questions": len(input_data.get('questions', [])),
                "secteur_scian": input_data.get('secteur_scian', '236'),
                "enhanced_by_memory": result.get('enhanced_by_memory', False)
            }
            
            # Ajouter � la m�moire
            memory_result = add_agent_interaction(self.agent_id, user_id, input_data, result)
            if memory_result.get('success'):
                print(f"?? Interaction m�moris�e: {memory_result.get('memory_id', 'N/A')}")
            
        except Exception as e:
            print(f"?? Erreur m�morisation: {e}")

# Test int�gr�
def test_agent_A2_enhanced():
    """Test complet de l'Agent A2 Enhanced Standalone"""
    print("?? TEST AGENT A2 ENHANCED STANDALONE")
    print("=" * 50)
    
    try:
        # Initialisation
        agent = AgentA2EnhancedStandalone()
        
        # Donn�es test
        test_data = {
            'questions': [
                {'question': 'Formation s�curit� dispens�e r�guli�rement', 'reponse': 'Oui'},
                {'question': 'EPI fournis et utilis�s correctement', 'reponse': 'Oui'},
                {'question': 'Proc�dures urgence connues �quipe', 'reponse': 'Partiellement'},
                {'question': 'Incidents report�s syst�matiquement', 'reponse': 'Oui'}
            ],
            'domaine': 'construction',
            'secteur_scian': '236'
        }
        
        # Test 1�re �valuation
        print("\\n--- TEST 1: PREMI�RE �VALUATION ---")
        result1 = agent.process_with_memory(test_data, 'entreprise_test', '236')
        print(f"Score: {result1.get('score_final', 'N/A')}/100")
        print(f"Niveau: {result1.get('niveau_securite', 'N/A')}")
        print(f"Enhanced by memory: {result1.get('enhanced_by_memory', False)}")
        
        # Test 2�me �valuation (am�lior�e)
        print("\\n--- TEST 2: DEUXI�ME �VALUATION (AM�LIOR�E) ---")
        test_data2 = test_data.copy()
        test_data2['questions'][2]['reponse'] = 'Oui'  # Am�lioration
        
        result2 = agent.process_with_memory(test_data2, 'entreprise_test', '236')
        print(f"Score: {result2.get('score_final', 'N/A')}/100")
        print(f"Enhanced by memory: {result2.get('enhanced_by_memory', False)}")
        
        if 'memory_insights' in result2:
            insights = result2['memory_insights']
            print(f"�valuations historiques: {insights.get('historical_evaluations', 0)}")
            print(f"Tendance: {insights.get('trend_analysis', {}).get('trend', 'N/A')}")
        
        print("\\n?? AGENT A2 ENHANCED STANDALONE FONCTIONNEL !")
        return True
        
    except Exception as e:
        print(f"? Test �chou�: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_agent_A2_enhanced()
