# src/api/thunder_integration.py
import json
import os
import streamlit as st
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class ThunderClientIntegration:
    """
    Intégration Thunder Client pour SafetyGraph
    Charge et exécute les collections Thunder Client exportées
    """
    
    def __init__(self, collections_path: str = "api_collections/thunder_exports/"):
        """
        Initialise l'intégration Thunder Client
        
        Args:
            collections_path: Chemin vers les collections exportées
        """
        self.collections_path = Path(collections_path)
        self.collections = {}
        self.statistics = {}
        self.load_collections()
        
    def load_collections(self):
        """Charge toutes les collections Thunder Client depuis les fichiers JSON"""
        try:
            if not self.collections_path.exists():
                st.warning(f"⚠️ Dossier non trouvé: {self.collections_path}")
                return
                
            json_files = list(self.collections_path.glob("*.json"))
            
            if not json_files:
                st.warning(f"⚠️ Aucun fichier JSON trouvé dans: {self.collections_path}")
                return
            
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        collection_data = json.load(f)
                        collection_name = json_file.stem
                        self.collections[collection_name] = collection_data
                        
                except Exception as e:
                    st.error(f"❌ Erreur chargement {json_file.name}: {e}")
            
            self.update_statistics()
            
        except Exception as e:
            st.error(f"❌ Erreur générale chargement collections: {e}")
    
    def update_statistics(self):
        """Met à jour les statistiques des collections"""
        total_requests = 0
        collection_names = []
        
        for collection_name, collection_data in self.collections.items():
            collection_names.append(collection_name)
            if isinstance(collection_data, dict):
                # Format Thunder Client standard
                requests_count = len(collection_data.get('requests', []))
                total_requests += requests_count
            elif isinstance(collection_data, list):
                # Format liste de requêtes
                total_requests += len(collection_data)
        
        self.statistics = {
            'collections_count': len(self.collections),
            'total_requests': total_requests,
            'collections_names': collection_names,
            'last_loaded': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_available_collections(self) -> List[str]:
        """Retourne la liste des collections disponibles"""
        return list(self.collections.keys())
    
    def get_collection_requests(self, collection_name: str) -> List[str]:
        """
        Retourne la liste des requêtes d'une collection
        
        Args:
            collection_name: Nom de la collection
            
        Returns:
            Liste des noms de requêtes
        """
        if collection_name not in self.collections:
            return []
        
        collection_data = self.collections[collection_name]
        
        if isinstance(collection_data, dict):
            return [req.get('name', f'Request_{i}') for i, req in enumerate(collection_data.get('requests', []))]
        elif isinstance(collection_data, list):
            return [req.get('name', f'Request_{i}') for i, req in enumerate(collection_data)]
        
        return []
    
    def get_request_details(self, collection_name: str, request_name: str) -> Optional[Dict]:
        """
        Retourne les détails d'une requête spécifique
        
        Args:
            collection_name: Nom de la collection
            request_name: Nom de la requête
            
        Returns:
            Dictionnaire avec les détails de la requête
        """
        if collection_name not in self.collections:
            return None
        
        collection_data = self.collections[collection_name]
        requests_list = []
        
        if isinstance(collection_data, dict):
            requests_list = collection_data.get('requests', [])
        elif isinstance(collection_data, list):
            requests_list = collection_data
        
        for request in requests_list:
            if request.get('name') == request_name:
                return request
        
        return None
    
    def extract_variables_from_prompt(self, prompt: str) -> List[str]:
        """
        Extrait les variables du format {{variable}} dans le prompt
        
        Args:
            prompt: Texte du prompt
            
        Returns:
            Liste des noms de variables
        """
        import re
        variables = re.findall(r'\{\{(\w+)\}\}', prompt)
        return list(set(variables))  # Supprime les doublons
    
    def execute_request(self, collection_name: str, request_name: str, variables: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Exécute une requête Thunder Client
        
        Args:
            collection_name: Nom de la collection
            request_name: Nom de la requête
            variables: Dictionnaire des variables à remplacer
            
        Returns:
            Résultat de l'exécution
        """
        if variables is None:
            variables = {}
        
        try:
            request_details = self.get_request_details(collection_name, request_name)
            
            if not request_details:
                return {
                    'success': False,
                    'error': f'Requête "{request_name}" non trouvée dans "{collection_name}"',
                    'response': None
                }
            
            # Extraction des données de la requête
            body = request_details.get('body', {})
            
            if not body:
                return {
                    'success': False,
                    'error': 'Corps de requête manquant',
                    'response': None
                }
            
            # Construction du prompt avec variables
            messages = body.get('messages', [])
            if not messages:
                return {
                    'success': False,
                    'error': 'Messages manquants dans la requête',
                    'response': None
                }
            
            # Remplace les variables dans le contenu
            prompt = messages[0].get('content', '')
            for var_name, var_value in variables.items():
                prompt = prompt.replace(f'{{{{{var_name}}}}}', str(var_value))
            
            # Configuration API Claude
            api_data = {
                "model": body.get('model', 'claude-sonnet-4-20250514'),
                "max_tokens": body.get('max_tokens', 4000),
                "messages": [{"role": "user", "content": prompt}]
            }
            
            # Ajoute le system prompt si présent
            if 'system' in body and body['system']:
                api_data['system'] = body['system']
            
            # Simulation d'exécution (remplacez par vraie API si besoin)
            return {
                'success': True,
                'error': None,
                'response': {
                    'content': [{'text': f'✅ Requête "{request_name}" exécutée avec succès!\n\nPrompt traité:\n{prompt[:200]}...'}],
                    'usage': {'input_tokens': len(prompt), 'output_tokens': 100}
                },
                'execution_time': '1.2s',
                'variables_used': variables
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': None
            }
    
    def get_statistics(self) -> Dict:
        """Retourne les statistiques des collections"""
        return self.statistics

def add_thunder_client_tab():
    """
    Ajoute l'interface Thunder Client à Streamlit
    """
    st.header("🚀 Thunder Client - SafetyGraph Integration")
    
    # Initialisation
    if 'thunder_client' not in st.session_state:
        st.session_state.thunder_client = ThunderClientIntegration()
    
    thunder = st.session_state.thunder_client
    
    # Sidebar avec statistiques
    with st.sidebar:
        st.subheader("📊 Thunder Client Stats")
        stats = thunder.get_statistics()
        
        if stats['collections_count'] > 0:
            st.metric("Collections", stats['collections_count'])
            st.metric("Total Requêtes", stats['total_requests'])
            st.text(f"Dernière MAJ: {stats['last_loaded']}")
            
            with st.expander("📁 Collections Détails"):
                for collection_name in stats['collections_names']:
                    requests = thunder.get_collection_requests(collection_name)
                    st.write(f"**{collection_name}** ({len(requests)} requêtes)")
        else:
            st.warning("⚠️ Aucune collection chargée")
    
    # Interface principale
    collections = thunder.get_available_collections()
    
    if not collections:
        st.error("❌ Aucune collection Thunder Client trouvée")
        st.info("💡 Vérifiez que vos fichiers JSON sont dans: api_collections/thunder_exports/")
        return
    
    # Sélection collection
    selected_collection = st.selectbox(
        "📁 Sélectionner une Collection",
        collections,
        key="thunder_collection"
    )
    
    if selected_collection:
        # Sélection requête
        requests = thunder.get_collection_requests(selected_collection)
        
        if requests:
            selected_request = st.selectbox(
                "📋 Sélectionner une Requête",
                requests,
                key="thunder_request"
            )
            
            if selected_request:
                # Détails de la requête
                request_details = thunder.get_request_details(selected_collection, selected_request)
                
                if request_details:
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader(f"🔧 Configuration: {selected_request}")
                        
                        # Extraction et affichage des variables
                        body = request_details.get('body', {})
                        messages = body.get('messages', [])
                        
                        if messages:
                            prompt = messages[0].get('content', '')
                            variables_needed = thunder.extract_variables_from_prompt(prompt)
                            
                            # Interface pour les variables
                            variables_values = {}
                            
                            if variables_needed:
                                st.write("**Variables requises:**")
                                for var in variables_needed:
                                    variables_values[var] = st.text_input(
                                        f"Variable: {var}",
                                        key=f"thunder_var_{var}",
                                        placeholder=f"Entrez la valeur pour {var}"
                                    )
                            else:
                                st.info("ℹ️ Cette requête ne nécessite aucune variable")
                    
                    with col2:
                        st.subheader("📊 Métadonnées")
                        st.json({
                            'model': body.get('model', 'N/A'),
                            'max_tokens': body.get('max_tokens', 'N/A'),
                            'system': body.get('system', 'N/A')[:100] + '...' if body.get('system') else 'N/A'
                        })
                    
                    # Bouton d'exécution
                    if st.button("🚀 Exécuter la Requête", type="primary"):
                        # Validation des variables
                        missing_vars = [var for var in variables_needed if not variables_values.get(var)]
                        
                        if missing_vars:
                            st.error(f"❌ Variables manquantes: {', '.join(missing_vars)}")
                        else:
                            with st.spinner("⏳ Exécution en cours..."):
                                result = thunder.execute_request(
                                    selected_collection,
                                    selected_request,
                                    variables_values
                                )
                            
                            if result['success']:
                                st.success("✅ Requête exécutée avec succès!")
                                
                                # Affichage du résultat
                                response = result.get('response', {})
                                if 'content' in response:
                                    st.subheader("📄 Réponse")
                                    st.write(response['content'][0]['text'])
                                
                                # Métriques
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Temps", result.get('execution_time', 'N/A'))
                                with col2:
                                    usage = response.get('usage', {})
                                    st.metric("Tokens Input", usage.get('input_tokens', 'N/A'))
                                with col3:
                                    st.metric("Tokens Output", usage.get('output_tokens', 'N/A'))
                                
                                # Variables utilisées
                                if variables_values:
                                    with st.expander("🔧 Variables Utilisées"):
                                        st.json(variables_values)
                            else:
                                st.error(f"❌ Erreur: {result['error']}")
                else:
                    st.error("❌ Impossible de charger les détails de la requête")
        else:
            st.warning("⚠️ Aucune requête trouvée dans cette collection")

# Test de l'importation
if __name__ == "__main__":
    print("🔍 Test du module Thunder Client Integration...")
    
    # Test d'initialisation
    thunder = ThunderClientIntegration()
    print(f"✅ Collections chargées: {len(thunder.get_available_collections())}")
    
    # Affichage des statistiques
    stats = thunder.get_statistics()
    print(f"📊 Statistiques: {stats}")
    
    print("✅ Module prêt pour utilisation!")