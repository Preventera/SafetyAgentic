# debug_simple.py - Voir le contenu exact d'un fichier
import json
import os

def show_file_content():
    # Vérifier le fichier Mines
    file_path = "api_collections/thunder_exports/Mines_Souterraines_SCIAN_212.json"
    
    print("🔍 CONTENU EXACT DU FICHIER MINES")
    print("=" * 50)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("📄 CONTENU BRUT:")
        print(content)
        
        print("\n" + "-" * 50)
        
        # Parse JSON
        data = json.loads(content)
        print("📊 STRUCTURE JSON:")
        print(f"Type: {type(data)}")
        
        if isinstance(data, dict):
            print(f"Clés principales: {list(data.keys())}")
            
            for key, value in data.items():
                print(f"\n🔹 {key}:")
                print(f"  Type: {type(value)}")
                
                if isinstance(value, list):
                    print(f"  Longueur: {len(value)}")
                    if value:
                        print(f"  Premier élément: {type(value[0])}")
                        if isinstance(value[0], dict):
                            print(f"  Clés premier élément: {list(value[0].keys())}")
                elif isinstance(value, dict):
                    print(f"  Clés: {list(value.keys())}")
                else:
                    print(f"  Valeur: {str(value)[:100]}")
        
    except FileNotFoundError:
        print("❌ Fichier Mines non trouvé")
        print("📁 Fichiers disponibles:")
        for f in os.listdir("api_collections/thunder_exports/"):
            if f.endswith('.json'):
                print(f"  • {f}")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Maintenant regarder un fichier qui fonctionne
    print("\n" + "=" * 50)
    print("🔍 COMPARAISON AVEC FICHIER QUI FONCTIONNE")
    
    working_file = "api_collections/thunder_exports/thunder-collection_postman_BehaviorX_Analyses_HSE.json"
    
    try:
        with open(working_file, 'r', encoding='utf-8') as f:
            working_content = f.read()
        
        print("📄 STRUCTURE FICHIER BEHAVIORX (premiers 500 char):")
        print(working_content[:500])
        
        working_data = json.loads(working_content)
        print(f"\n📊 Clés BehaviorX: {list(working_data.keys())}")
        
    except Exception as e:
        print(f"❌ Erreur fichier BehaviorX: {e}")

if __name__ == "__main__":
    show_file_content()