"""
Test simple du prototype SafeGraph
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
    
    # Test 3: Énumérations
    print("\n3. Test énumérations...")
    assert IntentType.EVALUATION
    assert SectorType.CONSTRUCTION
    print("✅ Énumérations définies correctement")
    
    # Test 4: Import des agents
    print("\n4. Test import des agents...")
    try:
        from src.agents import router_agent, context_agent
        from src.agents.evaluation.collecteur_agent import collecteur_agent
        from src.agents.analysis.analyste_agent import analyste_agent
        from src.agents.recommendation.recommandation_agent import recommandation_agent
        print("✅ Tous les agents importés avec succès")
    except Exception as e:
        print(f"❌ Erreur import agents : {e}")
        return False
    
    print(f"\n🎉 Tous les tests de base réussis !")
    print(f"SafeGraph prototype opérationnel")
    
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    exit(0 if success else 1)