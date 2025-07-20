import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

def check_storm_status():
    base_path = Path('.')
    logs_path = base_path / 'logs'
    storm_path = base_path / 'data' / 'storm_knowledge'
    
    print('🔍 VÉRIFICATION STATUT STORM')
    print('=' * 40)
    
    # Vérifier corpus récent
    corpus_files = list(storm_path.glob('safety_agentique_corpus_*.json'))
    if corpus_files:
        latest_corpus = max(corpus_files, key=lambda x: x.stat().st_mtime)
        corpus_age = datetime.now() - datetime.fromtimestamp(latest_corpus.stat().st_mtime)
        
        print(f'📚 Dernier corpus: {latest_corpus.name}')
        print(f'⏱️  Âge: {corpus_age}')
        
        if corpus_age > timedelta(days=2):
            print('⚠️  Corpus ancien - Enrichissement requis')
        else:
            print('✅ Corpus récent')
    else:
        print('❌ Aucun corpus trouvé')
    
    print('=' * 40)

if __name__ == '__main__':
    check_storm_status()
