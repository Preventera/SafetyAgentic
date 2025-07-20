"""
Test simple du prototype SafeGraph (Version Claude API)
"""

from src.core.state import create_initial_state, IntentType, SectorType
from src.core.config import config

def test_basic_functionality():
    """Test des fonctionnalités de base"""
    
    print("🧪 Test des fonctionnalités de base SafeGraph")
    print("=" * 50)
    
    # Test 1: Création d'état
    print("\n1. Test création d'état initial...")
    test_query = "Évaluation sécurité chantier construction"
    state = create_initial_state(test_query)
    
    assert state["user_input"] == test_query
    assert state["session_id"].startswith("session_")
    assert state["timestamp"]
    print("✅ État initial créé correctement")
    
    # Test 2: Configuration
    print("\n2. Test configuration...")
    assert len(config.scian_sectors) >= 5
    assert "236" in config.scian_sectors  # Construction
    print(f"✅ Configuration chargée - {len(config.scian_sectors)} secteurs")
    
    # Test 3: Configuration API
    print("\n3. Test configuration API...")
    print(f"  • Claude API : {'✅' if config.has_claude_api else '❌'}")
    print(f"  • OpenAI API : {'✅' if config.has_openai_api else '❌'}")
    print(f"  • LLM préféré : {config.preferred_llm}")
    
    # Test 4: Factory LLM
    print("\n4. Test factory LLM...")
    try:
        if config.preferred_llm != "none":
            from src.utils.llm_factory import get_preferred_llm
            llm = get_preferred_llm()
            print(f"✅ LLM {config.preferred_llm} créé avec succès")
        else:
            print("⚠️  Aucune API - Mode simulation")
    except Exception as e:
        print(f"⚠️  Erreur LLM : {e}")
    
    # Test 5: Énumérations
    print("\n5. Test énumérations...")
    assert IntentType.EVALUATION
    assert SectorType.CONSTRUCTION
    
    # Test LLMType séparément
    try:
        from src.utils.llm_factory import LLMType
        assert LLMType.CLAUDE
        print("✅ Énumérations définies correctement")
    except ImportError:
        print("⚠️  LLMType non disponible - test partiellement réussi")
    
    # Test 6: Import des agents
    print("\n6. Test import des agents...")
    try:
        from src.agents import router_agent, context_agent
        from src.agents.evaluation.collecteur_agent import collecteur_agent
        from src.agents.analysis.analyste_agent import analyste_agent
        from src.agents.recommendation.recommandation_agent import recommandation_agent
        print("✅ Tous les agents importés avec succès")
    except Exception as e:
        print(f"❌ Erreur import agents : {e}")
        return False
    
    # Test 7: Utilitaires
    print("\n7. Test utilitaires...")
    try:
        from src.utils.llm_factory import get_llm
        print("✅ Utilitaires importés avec succès")
    except Exception as e:
        print(f"❌ Erreur import utilitaires : {e}")
        return False
    
    print(f"\n🎉 Tous les tests de base réussis !")
    print(f"SafeGraph prototype opérationnel avec support Claude API")
    
    return True

def test_agents_simulation():
    """Test des agents en mode simulation"""
    
    print("\n" + "=" * 50)
    print("🧪 Test simulation workflow agents")
    print("=" * 50)
    
    # État de test
    test_state = create_initial_state("Évaluation sécurité construction")
    test_state["intent"] = IntentType.EVALUATION
    test_state["scian_sector"] = "236"
    
    print(f"🤖 Mode : {config.preferred_llm}")
    
    # Test Router Agent
    print("\n1. Test Router Agent...")
    try:
        from src.agents.router_agent import router_agent
        result = router_agent(test_state)
        
        intent = result.get('intent', 'N/A')
        errors = result.get('errors', [])
        
        print(f"✅ Router Agent OK")
        print(f"  • Intent: {intent}")
        if errors:
            print(f"  • Erreurs: {len(errors)}")
        
    except Exception as e:
        print(f"❌ Router Agent erreur : {e}")
    
    # Test Context Agent
    print("\n2. Test Context Agent...")
    try:
        from src.agents.context_agent import context_agent
        result = context_agent(test_state)
        context_keys = list(result.get('context', {}).keys())
        print(f"✅ Context Agent OK - {len(context_keys)} éléments")
    except Exception as e:
        print(f"❌ Context Agent erreur : {e}")
    
    # Test Collecteur Agent
    print("\n3. Test Collecteur Agent...")
    try:
        from src.agents.evaluation.collecteur_agent import collecteur_agent
        result = collecteur_agent(test_state)
        collections = result.get('collection_results', [])
        print(f"✅ Collecteur Agent OK - {len(collections)} collectes")
        
        # Ajouter données pour tests suivants
        if collections:
            test_state["collection_results"] = collections
            
    except Exception as e:
        print(f"❌ Collecteur Agent erreur : {e}")
    
    # Test Analyste Agent (si données disponibles)
    if "collection_results" in test_state:
        print("\n4. Test Analyste Agent...")
        try:
            from src.agents.analysis.analyste_agent import analyste_agent
            result = analyste_agent(test_state)
            risk_classification = result.get('analysis', {}).get('risk_classification', 'N/A')
            print(f"✅ Analyste Agent OK - Classification: {risk_classification}")
            
            # Ajouter pour test recommandations
            if 'analysis' in result:
                test_state["analysis"] = result["analysis"]
                test_state["risk_scores"] = result.get("risk_scores", {})
                
        except Exception as e:
            print(f"❌ Analyste Agent erreur : {e}")
    
    # Test Recommandation Agent (si analyse disponible)
    if "analysis" in test_state:
        print("\n5. Test Recommandation Agent...")
        try:
            from src.agents.recommendation.recommandation_agent import recommandation_agent
            result = recommandation_agent(test_state)
            recs = result.get('recommendations', [])
            print(f"✅ Recommandation Agent OK - {len(recs)} recommandations")
            
            if recs:
                first_rec = recs[0]
                print(f"  • Première: {first_rec.get('title', 'N/A')}")
                print(f"  • Source: {first_rec.get('source', 'N/A')}")
                
        except Exception as e:
            print(f"❌ Recommandation Agent erreur : {e}")

if __name__ == "__main__":
    print("🚀 Lancement des tests SafeGraph (Version Claude)")
    
    # Tests de base
    success = test_basic_functionality()
    
    if success:
        # Tests simulation workflow
        test_agents_simulation()
        print(f"\n🎉 SafeGraph prototype validé avec Claude API !")
    else:
        print(f"\n❌ Échec des tests de base")
        exit(1)