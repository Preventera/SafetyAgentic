"""
Agent A1 Enhanced Standalone avec Mem0
======================================

Version autonome qui ne dépend pas des agents existants
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from memory.wrapper import add_agent_interaction, get_agent_context
import json
from typing import Dict, List, Any
from datetime import datetime

class AgentA1EnhancedStandalone:
    """
    Agent A1 Enhanced autonome avec mémoire Mem0
    
    Fonctionnalités:
    - Traitement autoévaluations sécurité
    - Mémoire persistante des interactions
    - Recommandations personnalisées
    - Apprentissage évolutif des patterns
    """
    
    def __init__(self):
        self.agent_id = "A1"
        self.name = "Agent A1 Enhanced Standalone"
        print(f"✅ {self.name} initialisé avec mémoire Mem0")
    
    def process_autoevaluation_basic(self, data: Dict) -> Dict:
        """
        Traitement basique d'autoévaluation (version standalone)
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
        
        # Évaluation qualitative
        if score_final >= 80:
            niveau = "Excellent"
            couleur = "vert"
        elif score_final >= 60:
            niveau = "Bon"
            couleur = "orange"
        else:
            niveau = "À améliorer"
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
            "agent_version": "A1_Enhanced_Standalone_v1.0"
        }
    
    def _generate_basic_recommendations(self, score: float, questions: List[Dict]) -> List[str]:
        """Génère recommandations basiques selon le score"""
        recommendations = []
        
        if score >= 80:
            recommendations.extend([
                "🎉 Excellente culture sécurité ! Maintenez ces bonnes pratiques",
                "📊 Partagez vos meilleures pratiques avec d'autres équipes",
                "🔄 Continuez les audits réguliers pour maintenir ce niveau"
            ])
        elif score >= 60:
            recommendations.extend([
                "⚠️ Bon niveau général, quelques améliorations possibles",
                "📋 Identifiez les domaines perfectibles",
                "🎓 Formation complémentaire recommandée"
            ])
        else:
            recommendations.extend([
                "🚨 Attention : niveau sécurité insuffisant",
                "📚 Formation urgente en sécurité recommandée",
                "👥 Audit approfondi des procédures nécessaire",
                "⏰ Plan d'action prioritaire à mettre en place"
            ])
        
        # Recommandations spécifiques selon les réponses
        for q in questions:
            if q.get('reponse', '').lower() in ['non', 'no', 'faux', 'false']:
                question_text = q.get('question', '')[:50]
                recommendations.append(f"🔍 Action requise: {question_text}...")
        
        return recommendations
    
    def process_with_memory(self, data: Dict, user_id: str = "default", secteur_scian: str = "236") -> Dict:
        """
        Traite autoévaluation avec mémoire persistante
        
        Args:
            data: Données autoévaluation
            user_id: ID utilisateur/entreprise  
            secteur_scian: Code secteur SCIAN
            
        Returns:
            Résultat enrichi avec contexte mémoire
        """
        try:
            print(f"🤖 Traitement autoévaluation pour {user_id} (secteur {secteur_scian})")
            
            # 1. Récupérer contexte mémoire
            memories = get_agent_context(self.agent_id, user_id, f"autoevaluation {secteur_scian}")
            print(f"📚 {len(memories)} mémoires trouvées dans l'historique")
            
            # 2. Traitement de base
            result = self.process_autoevaluation_basic(data)
            
            # 3. Enrichir avec insights mémoire
            if memories:
                memory_insights = self._analyze_memory_insights(memories, result)
                result["memory_insights"] = memory_insights
                result["enhanced_by_memory"] = True
                print(f"🧠 Résultat enrichi avec {memory_insights['historical_evaluations']} évaluations passées")
            else:
                result["memory_insights"] = {
                    "historical_evaluations": 0,
                    "status": "première_évaluation",
                    "message": "Première évaluation enregistrée - L'IA apprendra de vos futurs patterns",
                    "future_benefits": [
                        "Recommandations personnalisées",
                        "Détection des tendances d'amélioration", 
                        "Alertes sur les régressions"
                    ]
                }
                result["enhanced_by_memory"] = False
                print("🆕 Première évaluation - création de l'historique")
            
            # 4. Mémoriser cette interaction
            self._memorize_interaction(user_id, data, result)
            
            return result
            
        except Exception as e:
            print(f"❌ Erreur A1 Enhanced: {e}")
            # Fallback vers traitement basique
            return self.process_autoevaluation_basic(data)
    
    def _analyze_memory_insights(self, memories: List[Dict], current_result: Dict) -> Dict:
        """Analyse les insights mémoire"""
        
        # Extraire scores historiques
        historical_scores = []
        for memory in memories:
            metadata = memory.get('metadata', {})
            if 'score' in metadata:
                historical_scores.append(metadata['score'])
        
        current_score = current_result.get('score_final', 0)
        
        # Calculer tendance
        trend_analysis = self._calculate_trend_analysis(historical_scores, current_score)
        
        # Recommandations personnalisées
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
            return {"trend": "no_data", "message": "Pas assez de données historiques"}
        
        if len(historical_scores) == 1:
            prev_score = historical_scores[0]
            change = current_score - prev_score
            if change > 5:
                return {"trend": "improving", "change": change, "message": f"Amélioration de {change:.1f} points"}
            elif change < -5:
                return {"trend": "declining", "change": change, "message": f"Baisse de {abs(change):.1f} points"}
            else:
                return {"trend": "stable", "change": change, "message": "Score stable"}
        
        # Analyse avec plusieurs points
        recent_avg = sum(historical_scores[-3:]) / min(3, len(historical_scores))
        overall_trend = current_score - recent_avg
        
        if overall_trend > 10:
            return {"trend": "strong_improvement", "change": overall_trend, "message": "Forte amélioration continue"}
        elif overall_trend > 3:
            return {"trend": "improvement", "change": overall_trend, "message": "Amélioration progressive"}
        elif overall_trend < -10:
            return {"trend": "concerning_decline", "change": overall_trend, "message": "Baisse préoccupante"}
        elif overall_trend < -3:
            return {"trend": "decline", "change": overall_trend, "message": "Légère régression"}
        else:
            return {"trend": "stable", "change": overall_trend, "message": "Performance stable"}
    
    def _generate_personalized_recommendations(self, historical_scores: List[float], current_score: float, trend: Dict) -> List[str]:
        """Génère recommandations personnalisées"""
        recommendations = []
        
        trend_type = trend.get('trend', 'no_data')
        
        if trend_type in ['strong_improvement', 'improvement']:
            recommendations.extend([
                "🎯 Excellente progression ! Continuez sur cette lancée",
                "📈 Vos efforts portent leurs fruits - maintenez le cap", 
                "⭐ Partagez vos bonnes pratiques avec d'autres équipes"
            ])
        elif trend_type in ['concerning_decline', 'decline']:
            recommendations.extend([
                "⚠️ ALERTE: Régression détectée dans vos pratiques",
                "🔍 Auditez les changements récents dans vos procédures",
                "📞 Considérez une consultation en sécurité industrielle",
                "⏰ Plan d'action corrective prioritaire recommandé"
            ])
        elif trend_type == 'stable':
            if current_score >= 75:
                recommendations.append("✅ Performance stable et satisfaisante - continuez")
            else:
                recommendations.extend([
                    "📊 Performance stable mais améliorable",
                    "🎓 Formation continue recommandée pour progresser"
                ])
        
        # Recommandations selon niveau actuel
        if current_score < 50:
            recommendations.extend([
                "🚨 URGENT: Score critique - intervention immédiate requise",
                "📋 Audit complet des pratiques sécurité nécessaire"
            ])
        elif current_score < 70:
            recommendations.append("⚡ Score insuffisant - plan d'amélioration prioritaire")
        
        return recommendations
    
    def _calculate_improvement_potential(self, historical_scores: List[float], current_score: float) -> str:
        """Calcule le potentiel d'amélioration"""
        if not historical_scores:
            return "Premier diagnostic - potentiel à établir"
        
        max_historical = max(historical_scores)
        if current_score >= max_historical:
            return "Performance à son meilleur niveau historique"
        else:
            potential = max_historical - current_score
            return f"Potentiel d'amélioration: +{potential:.1f} points (meilleur score: {max_historical})"
    
    def _memorize_interaction(self, user_id: str, input_data: Dict, result: Dict):
        """Mémorise l'interaction pour apprentissage futur"""
        try:
            # Contenu structuré pour la mémoire
            content = f"""
            Autoévaluation sécurité - Secteur: {input_data.get('secteur_scian', 'N/A')}
            Domaine: {input_data.get('domaine', 'general')}
            Questions: {len(input_data.get('questions', []))}
            Score obtenu: {result.get('score_final', 0)}/100
            Niveau: {result.get('niveau_securite', 'N/A')}
            """
            
            # Métadonnées enrichies
            metadata = {
                "type": "autoevaluation",
                "agent_version": "A1_Enhanced_Standalone",
                "score": result.get('score_final', 0),
                "niveau": result.get('niveau_securite', 'unknown'),
                "domaine": input_data.get('domaine', 'general'),
                "nb_questions": len(input_data.get('questions', [])),
                "secteur_scian": input_data.get('secteur_scian', '236'),
                "enhanced_by_memory": result.get('enhanced_by_memory', False)
            }
            
            # Ajouter à la mémoire
            memory_result = add_agent_interaction(self.agent_id, user_id, input_data, result)
            if memory_result.get('success'):
                print(f"💾 Interaction mémorisée: {memory_result.get('memory_id', 'N/A')}")
            
        except Exception as e:
            print(f"⚠️ Erreur mémorisation: {e}")

# Test intégré
def test_agent_a1_enhanced():
    """Test complet de l'Agent A1 Enhanced Standalone"""
    print("🧪 TEST AGENT A1 ENHANCED STANDALONE")
    print("=" * 50)
    
    try:
        # Initialisation
        agent = AgentA1EnhancedStandalone()
        
        # Données test
        test_data = {
            'questions': [
                {'question': 'Formation sécurité dispensée régulièrement', 'reponse': 'Oui'},
                {'question': 'EPI fournis et utilisés correctement', 'reponse': 'Oui'},
                {'question': 'Procédures urgence connues équipe', 'reponse': 'Partiellement'},
                {'question': 'Incidents reportés systématiquement', 'reponse': 'Oui'}
            ],
            'domaine': 'construction',
            'secteur_scian': '236'
        }
        
        # Test 1ère évaluation
        print("\\n--- TEST 1: PREMIÈRE ÉVALUATION ---")
        result1 = agent.process_with_memory(test_data, 'entreprise_test', '236')
        print(f"Score: {result1.get('score_final', 'N/A')}/100")
        print(f"Niveau: {result1.get('niveau_securite', 'N/A')}")
        print(f"Enhanced by memory: {result1.get('enhanced_by_memory', False)}")
        
        # Test 2ème évaluation (améliorée)
        print("\\n--- TEST 2: DEUXIÈME ÉVALUATION (AMÉLIORÉE) ---")
        test_data2 = test_data.copy()
        test_data2['questions'][2]['reponse'] = 'Oui'  # Amélioration
        
        result2 = agent.process_with_memory(test_data2, 'entreprise_test', '236')
        print(f"Score: {result2.get('score_final', 'N/A')}/100")
        print(f"Enhanced by memory: {result2.get('enhanced_by_memory', False)}")
        
        if 'memory_insights' in result2:
            insights = result2['memory_insights']
            print(f"Évaluations historiques: {insights.get('historical_evaluations', 0)}")
            print(f"Tendance: {insights.get('trend_analysis', {}).get('trend', 'N/A')}")
        
        print("\\n🎉 AGENT A1 ENHANCED STANDALONE FONCTIONNEL !")
        return True
        
    except Exception as e:
        print(f"❌ Test échoué: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_agent_a1_enhanced()
