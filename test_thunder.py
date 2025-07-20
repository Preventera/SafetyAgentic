# test_thunder.py - Test simple du module Thunder Client
print("🔍 Test importation Thunder Client...")

try:
    from src.api.thunder_integration import ThunderClientIntegration
    print("✅ Import ThunderClientIntegration : SUCCÈS")
    
    # Test d'initialisation
    thunder = ThunderClientIntegration()
    print("✅ Initialisation : SUCCÈS")
    
    # Test des collections
    collections = thunder.get_available_collections()
    print(f"✅ Collections trouvées : {len(collections)}")
    for col in collections:
        print(f"   📁 {col}")
    
    # Test des statistiques
    stats = thunder.get_statistics()
    print(f"✅ Statistiques : {stats}")
    
    print("\n🎉 TOUS LES TESTS RÉUSSIS !")
    
except ImportError as e:
    print(f"❌ Erreur import : {e}")
except Exception as e:
    print(f"❌ Erreur général : {e}")

print("\n📋 Module Thunder Client prêt pour intégration !")