# SafetyAgentic - Backup Corrigé pour Windows
import os
import shutil
import zipfile
import datetime
from pathlib import Path

def create_backup():
    print("🗄️ BACKUP SAFETYAGENTIC - DONNÉES INCLUSES")
    print("==========================================")
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"backup_complet_{timestamp}")
    backup_dir.mkdir(exist_ok=True)
    
    # BACKUP DONNÉES CNESST
    print("\n📊 BACKUP DONNÉES CNESST")
    print("========================")
    
    data_backup_dir = backup_dir / "data_cnesst"
    data_backup_dir.mkdir(exist_ok=True)
    
    # Chercher fichiers CNESST dans data/ et racine
    cnesst_files = []
    
    # Dans data/
    data_path = Path("data")
    if data_path.exists():
        cnesst_files.extend(list(data_path.glob("lesions*.csv")))
        print(f"  🔍 Trouvé {len(list(data_path.glob('lesions*.csv')))} fichiers dans data/")
    
    # À la racine aussi
    root_files = list(Path(".").glob("lesions*.csv"))
    cnesst_files.extend(root_files)
    if root_files:
        print(f"  🔍 Trouvé {len(root_files)} fichiers à la racine")
    
    total_size = 0
    backed_up_count = 0
    
    for file_path in cnesst_files:
        if file_path.is_file():
            try:
                dest_path = data_backup_dir / file_path.name
                shutil.copy2(file_path, dest_path)
                file_size = file_path.stat().st_size
                total_size += file_size
                backed_up_count += 1
                
                print(f"  ✅ {file_path.name} ({round(file_size/1024/1024, 1)} MB)")
                
            except Exception as e:
                print(f"  ❌ Erreur {file_path.name}: {e}")
    
    print(f"\n📊 RÉSUMÉ DONNÉES:")
    print(f"  • Fichiers CNESST: {backed_up_count}")
    print(f"  • Taille totale: {round(total_size / 1024 / 1024, 1)} MB")
    
    # BACKUP CODE PROJET
    print("\n💻 BACKUP CODE PROJET")
    print("=====================")
    
    code_dir = backup_dir / "project_code"
    code_dir.mkdir(exist_ok=True)
    
    code_patterns = ["*.py", "*.md", "*.txt"]
    code_count = 0
    
    for pattern in code_patterns:
        for file_path in Path(".").glob(pattern):
            if file_path.is_file():
                try:
                    shutil.copy2(file_path, code_dir / file_path.name)
                    code_count += 1
                    print(f"  ✅ {file_path.name}")
                except Exception as e:
                    print(f"  ❌ {file_path.name}: {e}")
    
    print(f"\n💻 RÉSUMÉ CODE: {code_count} fichiers")
    
    # CRÉATION ARCHIVE ZIP
    print("\n📦 CRÉATION ARCHIVE ZIP")
    print("=======================")
    
    zip_filename = f"SafetyAgentic_Backup_Complet_{timestamp}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(backup_dir)
                zipf.write(file_path, arcname)
    
    # Taille finale
    zip_size = Path(zip_filename).stat().st_size
    
    # NETTOYAGE
    try:
        shutil.rmtree(backup_dir)
        print("  ✅ Répertoire temporaire nettoyé")
    except:
        print("  ⚠️ Répertoire temporaire non supprimé")
    
    print(f"\n🎉 BACKUP COMPLET TERMINÉ!")
    print("==========================")
    print(f"📁 Archive: {zip_filename}")
    print(f"📊 Taille: {round(zip_size / 1024 / 1024, 1)} MB")
    print(f"🔒 {backed_up_count} fichiers CNESST + {code_count} fichiers code sauvegardés!")
    
    return zip_filename

if __name__ == "__main__":
    try:
        result = create_backup()
        print(f"\n✅ SUCCESS: {result}")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")