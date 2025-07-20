# debug_collections.py - Analyser le format des collections
import json
import os
from pathlib import Path

def analyze_collection_format():
    """Analyse le format des fichiers JSON Thunder Client"""
    
    collections_path = Path("api_collections/thunder_exports/")
    
    print("🔍 ANALYSE FORMAT COLLECTIONS THUNDER CLIENT")
    print("=" * 50)
    
    if not collections_path.exists():
        print(f"❌ Dossier non trouvé: {collections_path}")
        return
    
    json_files = list(collections_path.glob("*.json"))
    
    if not json_files:
        print(f"❌ Aucun fichier JSON dans: {collections_path}")
        return
    
    for json_file in json_files:
        print(f"\n📁 FICHIER: {json_file.name}")
        print("-" * 40)
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✅ Chargement réussi")
            print(f"📊 Type: {type(data)}")
            
            if isinstance(data, dict):
                print(f"🗂️ Clés principales: {list(data.keys())}")
                
                # Analyser structure
                for key, value in data.items():
                    print(f"  • {key}: {type(value)}")
                    
                    if key == "requests" and isinstance(value, list):
                        print(f"    → {len(value)} requêtes trouvées")
                        
                        # Analyser première requête
                        if value:
                            first_req = value[0]
                            print(f"    → Première requête: {type(first_req)}")
                            if isinstance(first_req, dict):
                                print(f"      Clés: {list(first_req.keys())}")
                    
                    elif isinstance(value, list):
                        print(f"    → Liste de {len(value)} éléments")
                        if value:
                            print(f"      Premier élément: {type(value[0])}")
                            if isinstance(value[0], dict):
                                print(f"      Clés premier élément: {list(value[0].keys())}")
            
            elif isinstance(data, list):
                print(f"📋 Liste de {len(data)} éléments")
                if data:
                    print(f"  Premier élément: {type(data[0])}")
                    if isinstance(data[0], dict):
                        print(f"  Clés: {list(data[0].keys())}")
            
            # Afficher extrait du contenu
            print(f"\n📄 EXTRAIT DU CONTENU:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:500] + "...")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 RECOMMANDATIONS BASÉES SUR L'ANALYSE")

if __name__ == "__main__":
    analyze_collection_format()