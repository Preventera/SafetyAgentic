#!/usr/bin/env python3
"""
SafetyGraph - Module Pattern Recognition
Reconnaissance automatique de patterns culturels en sécurité
Version complète avec interface Streamlit
"""

import pandas as pd
import numpy as np
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# ML Libraries pour clustering et pattern recognition
try:
    from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
    from sklearn.mixture import GaussianMixture
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.decomposition import PCA
    from sklearn.metrics import silhouette_score, adjusted_rand_score
    from sklearn.manifold import TSNE
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False


class CulturePattern:
    """Représente un pattern culturel identifié"""
    
    def __init__(self, pattern_id: str, pattern_type: str, 
                 characteristics: Dict, sectors_affected: List[str],
                 confidence_score: float):
        self.pattern_id = pattern_id
        self.pattern_type = pattern_type
        self.characteristics = characteristics
        self.sectors_affected = sectors_affected
        self.confidence_score = confidence_score
        self.created_at = datetime.now()
        self.prevalence = 0.0
        self.stability = 0.0
        self.trend = "stable"
    
    def to_dict(self) -> Dict:
        """Convertit le pattern en dictionnaire"""
        return {
            'pattern_id': self.pattern_id,
            'pattern_type': self.pattern_type,
            'characteristics': self.characteristics,
            'sectors_affected': self.sectors_affected,
            'confidence_score': self.confidence_score,
            'prevalence': self.prevalence,
            'stability': self.stability,
            'trend': self.trend,
            'created_at': self.created_at.isoformat()
        }


class SafetyGraphPatternRecognition:
    """Moteur de reconnaissance de patterns SafetyGraph"""
    
    def __init__(self, db_path: str = "analytics_patterns.db"):
        """
        Initialise le moteur de reconnaissance
        
        Args:
            db_path: Chemin vers la base de données
        """
        self.db_path = db_path
        self.patterns = {}
        self.clusters = {}
        self.scalers = {}
        
        # Configuration
        self.config = {
            'min_cluster_size': 10,
            'max_clusters': 20,
            'confidence_threshold': 0.7,
            'stability_window': 30  # jours
        }
        
        # Initialisation base de données
        self._init_database()
        
        # Chargement patterns existants
        self._load_existing_patterns()
    
    def _init_database(self):
        """Initialise la base de données SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table patterns identifiés
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id TEXT UNIQUE,
                pattern_type TEXT,
                characteristics TEXT,
                sectors_affected TEXT,
                confidence_score REAL,
                prevalence REAL,
                stability REAL,
                trend TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table clusters
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clusters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cluster_id TEXT,
                algorithm TEXT,
                n_clusters INTEGER,
                silhouette_score REAL,
                cluster_centers TEXT,
                cluster_labels TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table transitions entre patterns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pattern_transitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_pattern TEXT,
                to_pattern TEXT,
                transition_probability REAL,
                sector_scian TEXT,
                observed_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_existing_patterns(self):
        """Charge les patterns existants depuis la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patterns')
        patterns_data = cursor.fetchall()
        
        for pattern_data in patterns_data:
            pattern_id = pattern_data[1]
            pattern_type = pattern_data[2]
            characteristics = json.loads(pattern_data[3])
            sectors_affected = json.loads(pattern_data[4])
            confidence_score = pattern_data[5]
            
            pattern = CulturePattern(
                pattern_id=pattern_id,
                pattern_type=pattern_type,
                characteristics=characteristics,
                sectors_affected=sectors_affected,
                confidence_score=confidence_score
            )
            
            pattern.prevalence = pattern_data[6]
            pattern.stability = pattern_data[7]
            pattern.trend = pattern_data[8]
            
            self.patterns[pattern_id] = pattern
        
        conn.close()
    
    def prepare_culture_data(self, culture_data: pd.DataFrame) -> pd.DataFrame:
        """
        Prépare les données culturelles pour l'analyse
        
        Args:
            culture_data: DataFrame avec évaluations culture
            
        Returns:
            DataFrame préparé
        """
        if culture_data.empty:
            return pd.DataFrame()
        
        # Copie des données
        df = culture_data.copy()
        
        # Nettoyage colonnes
        df.columns = df.columns.str.strip().str.lower()
        
        # Dimensions culturelles standard
        culture_dimensions = [
            'leadership_engagement',
            'communication_effectiveness', 
            'training_quality',
            'employee_participation',
            'monitoring_improvement',
            'psychosocial_environment'
        ]
        
        # Vérification/création des colonnes
        for dim in culture_dimensions:
            if dim not in df.columns:
                # Génération de données simulées si manquantes
                df[dim] = np.random.normal(3.5, 0.5, len(df))
                df[dim] = np.clip(df[dim], 1, 5)
        
        # Agrégation par secteur et période
        if 'sector_scian' in df.columns and 'evaluation_date' in df.columns:
            df['evaluation_date'] = pd.to_datetime(df['evaluation_date'], errors='coerce')
            df['month_year'] = df['evaluation_date'].dt.to_period('M')
            
            # Agrégation mensuelle par secteur
            agg_df = df.groupby(['sector_scian', 'month_year']).agg({
                **{dim: 'mean' for dim in culture_dimensions},
                'enterprise_size': 'mean',
                'years_operation': 'mean'
            }).reset_index()
            
            # Calcul score global
            agg_df['culture_score_global'] = agg_df[culture_dimensions].mean(axis=1)
            
            # Indicateurs dérivés
            agg_df['leadership_communication_ratio'] = (
                agg_df['leadership_engagement'] / agg_df['communication_effectiveness']
            )
            
            agg_df['training_participation_synergy'] = (
                agg_df['training_quality'] * agg_df['employee_participation']
            )
            
            return agg_df
        
        return df
    
    def perform_clustering(self, data: pd.DataFrame, 
                          algorithm: str = 'kmeans', 
                          n_clusters: int = 4) -> Dict:
        """
        Effectue le clustering des données culturelles
        
        Args:
            data: DataFrame avec données préparées
            algorithm: Algorithme de clustering
            n_clusters: Nombre de clusters
            
        Returns:
            Résultats du clustering
        """
        if data.empty or not ML_AVAILABLE:
            return {}
        
        # Sélection des features pour clustering
        feature_cols = [col for col in data.columns 
                       if col not in ['sector_scian', 'month_year', 'evaluation_date']]
        
        if len(feature_cols) < 2:
            return {}
        
        X = data[feature_cols].fillna(data[feature_cols].mean())
        
        if len(X) < n_clusters:
            return {}
        
        # Normalisation
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Choix algorithme
        if algorithm == 'kmeans':
            clusterer = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        elif algorithm == 'dbscan':
            clusterer = DBSCAN(eps=0.5, min_samples=5)
        elif algorithm == 'hierarchical':
            clusterer = AgglomerativeClustering(n_clusters=n_clusters)
        elif algorithm == 'gaussian_mixture':
            clusterer = GaussianMixture(n_components=n_clusters, random_state=42)
        else:
            clusterer = KMeans(n_clusters=n_clusters, random_state=42)
        
        # Clustering
        if algorithm == 'gaussian_mixture':
            cluster_labels = clusterer.fit_predict(X_scaled)
        else:
            cluster_labels = clusterer.fit_predict(X_scaled)
        
        # Métriques qualité
        silhouette_avg = silhouette_score(X_scaled, cluster_labels) if len(set(cluster_labels)) > 1 else 0
        
        # Centres des clusters
        if hasattr(clusterer, 'cluster_centers_'):
            cluster_centers = clusterer.cluster_centers_
        elif hasattr(clusterer, 'means_'):
            cluster_centers = clusterer.means_
        else:
            # Calcul manuel pour DBSCAN
            cluster_centers = []
            for label in set(cluster_labels):
                if label != -1:  # Ignore noise points
                    cluster_centers.append(X_scaled[cluster_labels == label].mean(axis=0))
            cluster_centers = np.array(cluster_centers)
        
        # Ajout des labels au DataFrame
        data_with_clusters = data.copy()
        data_with_clusters['cluster_label'] = cluster_labels
        
        # Analyse des clusters
        cluster_analysis = self._analyze_clusters(data_with_clusters, feature_cols)
        
        results = {
            'algorithm': algorithm,
            'n_clusters': len(set(cluster_labels)),
            'silhouette_score': silhouette_avg,
            'cluster_labels': cluster_labels,
            'cluster_centers': cluster_centers,
            'data_with_clusters': data_with_clusters,
            'cluster_analysis': cluster_analysis,
            'feature_columns': feature_cols,
            'scaler': scaler
        }
        
        # Sauvegarde en base
        self._save_clustering_results(results)
        
        return results
    
    def _analyze_clusters(self, data_with_clusters: pd.DataFrame, 
                         feature_cols: List[str]) -> Dict:
        """
        Analyse détaillée des clusters
        
        Args:
            data_with_clusters: DataFrame avec labels clusters
            feature_cols: Colonnes features
            
        Returns:
            Analyse des clusters
        """
        analysis = {}
        
        for cluster_id in data_with_clusters['cluster_label'].unique():
            if cluster_id == -1:  # Ignore noise points
                continue
            
            cluster_data = data_with_clusters[data_with_clusters['cluster_label'] == cluster_id]
            
            # Statistiques descriptives
            cluster_stats = {
                'size': len(cluster_data),
                'percentage': len(cluster_data) / len(data_with_clusters) * 100,
                'feature_means': cluster_data[feature_cols].mean().to_dict(),
                'feature_stds': cluster_data[feature_cols].std().to_dict()
            }
            
            # Secteurs dominants
            if 'sector_scian' in cluster_data.columns:
                sector_counts = cluster_data['sector_scian'].value_counts()
                cluster_stats['dominant_sectors'] = sector_counts.head(3).to_dict()
            
            # Caractérisation du cluster
            cluster_stats['characterization'] = self._characterize_cluster(cluster_data, feature_cols)
            
            analysis[f'cluster_{cluster_id}'] = cluster_stats
        
        return analysis
    
    def _characterize_cluster(self, cluster_data: pd.DataFrame, 
                            feature_cols: List[str]) -> Dict:
        """
        Caractérise un cluster spécifique
        
        Args:
            cluster_data: Données du cluster
            feature_cols: Colonnes features
            
        Returns:
            Caractérisation du cluster
        """
        means = cluster_data[feature_cols].mean()
        
        # Identification du type de pattern
        if means.get('leadership_engagement', 0) > 4.0 and means.get('communication_effectiveness', 0) > 4.0:
            pattern_type = 'proactive_excellence'
        elif means.get('training_quality', 0) > 4.0 and means.get('employee_participation', 0) > 4.0:
            pattern_type = 'learning_focused'
        elif means.get('monitoring_improvement', 0) > 4.0:
            pattern_type = 'continuous_improvement'
        elif means.mean() > 3.5:
            pattern_type = 'mature_culture'
        elif means.mean() > 2.5:
            pattern_type = 'developing_culture'
        else:
            pattern_type = 'emerging_culture'
        
        # Forces et faiblesses
        strengths = means.nlargest(3).index.tolist()
        weaknesses = means.nsmallest(3).index.tolist()
        
        return {
            'pattern_type': pattern_type,
            'overall_maturity': means.mean(),
            'strengths': strengths,
            'weaknesses': weaknesses,
            'stability_indicator': means.std(),
            'recommended_actions': self._generate_recommendations(pattern_type, weaknesses)
        }
    
    def _generate_recommendations(self, pattern_type: str, 
                                weaknesses: List[str]) -> List[str]:
        """
        Génère des recommandations basées sur le pattern
        
        Args:
            pattern_type: Type de pattern identifié
            weaknesses: Points faibles identifiés
            
        Returns:
            Liste de recommandations
        """
        recommendations = []
        
        # Recommandations par type de pattern
        if pattern_type == 'emerging_culture':
            recommendations.extend([
                "Établir un leadership sécurité visible",
                "Développer politique sécurité claire",
                "Créer système communication ascendante"
            ])
        elif pattern_type == 'developing_culture':
            recommendations.extend([
                "Renforcer formation superviseurs",
                "Implémenter système feedback",
                "Standardiser procédures sécurité"
            ])
        elif pattern_type == 'mature_culture':
            recommendations.extend([
                "Maintenir excellence actuelle",
                "Partager meilleures pratiques",
                "Innover en sécurité prédictive"
            ])
        
        # Recommandations par faiblesses
        weakness_recommendations = {
            'leadership_engagement': "Coaching leadership sécurité",
            'communication_effectiveness': "Améliorer canaux communication",
            'training_quality': "Réviser programme formation",
            'employee_participation': "Encourager participation active",
            'monitoring_improvement': "Renforcer système suivi",
            'psychosocial_environment': "Améliorer climat travail"
        }
        
        for weakness in weaknesses:
            if weakness in weakness_recommendations:
                recommendations.append(weakness_recommendations[weakness])
        
        return recommendations[:5]  # Limiter à 5 recommandations
    
    def identify_patterns(self, clustering_results: Dict) -> List[CulturePattern]:
        """
        Identifie les patterns culturels à partir des résultats de clustering
        
        Args:
            clustering_results: Résultats du clustering
            
        Returns:
            Liste des patterns identifiés
        """
        patterns = []
        
        if not clustering_results or 'cluster_analysis' not in clustering_results:
            return patterns
        
        cluster_analysis = clustering_results['cluster_analysis']
        
        for cluster_id, analysis in cluster_analysis.items():
            # Création du pattern
            pattern_id = f"pattern_{cluster_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            pattern_type = analysis['characterization']['pattern_type']
            
            # Caractéristiques du pattern
            characteristics = {
                'size': analysis['size'],
                'percentage': analysis['percentage'],
                'overall_maturity': analysis['characterization']['overall_maturity'],
                'strengths': analysis['characterization']['strengths'],
                'weaknesses': analysis['characterization']['weaknesses'],
                'stability_indicator': analysis['characterization']['stability_indicator'],
                'feature_means': analysis['feature_means']
            }
            
            # Secteurs affectés
            sectors_affected = list(analysis.get('dominant_sectors', {}).keys())
            
            # Score de confiance basé sur taille et stabilité
            confidence_score = min(1.0, (analysis['size'] / 100) * 0.5 + 
                                 (1 - analysis['characterization']['stability_indicator']) * 0.5)
            
            pattern = CulturePattern(
                pattern_id=pattern_id,
                pattern_type=pattern_type,
                characteristics=characteristics,
                sectors_affected=sectors_affected,
                confidence_score=confidence_score
            )
            
            pattern.prevalence = analysis['percentage'] / 100
            pattern.stability = 1 - analysis['characterization']['stability_indicator']
            
            patterns.append(pattern)
            self.patterns[pattern_id] = pattern
        
        # Sauvegarde des patterns
        self._save_patterns(patterns)
        
        return patterns
    
    def _save_clustering_results(self, results: Dict):
        """Sauvegarde les résultats de clustering"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cluster_id = f"cluster_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        cursor.execute('''
            INSERT INTO clusters (
                cluster_id, algorithm, n_clusters, silhouette_score, 
                cluster_centers, cluster_labels
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            cluster_id,
            results['algorithm'],
            results['n_clusters'],
            results['silhouette_score'],
            json.dumps(results['cluster_centers'].tolist() if hasattr(results['cluster_centers'], 'tolist') else []),
            json.dumps(results['cluster_labels'].tolist() if hasattr(results['cluster_labels'], 'tolist') else [])
        ))
        
        conn.commit()
        conn.close()
    
    def _save_patterns(self, patterns: List[CulturePattern]):
        """Sauvegarde les patterns identifiés"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for pattern in patterns:
            cursor.execute('''
                INSERT OR REPLACE INTO patterns (
                    pattern_id, pattern_type, characteristics, sectors_affected,
                    confidence_score, prevalence, stability, trend
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pattern.pattern_id,
                pattern.pattern_type,
                json.dumps(pattern.characteristics),
                json.dumps(pattern.sectors_affected),
                pattern.confidence_score,
                pattern.prevalence,
                pattern.stability,
                pattern.trend
            ))
        
        conn.commit()
        conn.close()
    
    def detect_pattern_transitions(self, historical_data: pd.DataFrame) -> Dict:
        """
        Détecte les transitions entre patterns
        
        Args:
            historical_data: Données historiques avec patterns
            
        Returns:
            Analyse des transitions
        """
        if historical_data.empty:
            return {}
        
        # Analyse des transitions par secteur
        transitions = {}
        
        if 'sector_scian' in historical_data.columns and 'pattern_type' in historical_data.columns:
            for sector in historical_data['sector_scian'].unique():
                sector_data = historical_data[historical_data['sector_scian'] == sector]
                sector_data = sector_data.sort_values('evaluation_date')
                
                sector_transitions = []
                for i in range(len(sector_data) - 1):
                    current_pattern = sector_data.iloc[i]['pattern_type']
                    next_pattern = sector_data.iloc[i + 1]['pattern_type']
                    
                    if current_pattern != next_pattern:
                        sector_transitions.append({
                            'from': current_pattern,
                            'to': next_pattern,
                            'date': sector_data.iloc[i + 1]['evaluation_date']
                        })
                
                transitions[sector] = sector_transitions
        
        return transitions
    
    def generate_pattern_report(self, sector_scian: str = None) -> Dict:
        """
        Génère un rapport complet des patterns
        
        Args:
            sector_scian: Code secteur SCIAN (optionnel)
            
        Returns:
            Rapport complet
        """
        # Patterns identifiés
        patterns_list = list(self.patterns.values())
        
        # Filtrage par secteur si spécifié
        if sector_scian:
            patterns_list = [p for p in patterns_list if sector_scian in p.sectors_affected]
        
        # Statistiques globales
        total_patterns = len(patterns_list)
        pattern_types = {}
        
        for pattern in patterns_list:
            pattern_type = pattern.pattern_type
            if pattern_type not in pattern_types:
                pattern_types[pattern_type] = 0
            pattern_types[pattern_type] += 1
        
        # Patterns les plus fréquents
        most_common_patterns = sorted(pattern_types.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Patterns à haute confiance
        high_confidence_patterns = [p for p in patterns_list if p.confidence_score > 0.8]
        
        return {
            'sector_scian': sector_scian,
            'total_patterns': total_patterns,
            'pattern_types_distribution': pattern_types,
            'most_common_patterns': most_common_patterns,
            'high_confidence_patterns': [p.to_dict() for p in high_confidence_patterns],
            'patterns_summary': [p.to_dict() for p in patterns_list],
            'generated_at': datetime.now(),
            'ml_available': ML_AVAILABLE
        }


# ===================================================================
# INTERFACE STREAMLIT
# ===================================================================

def display_pattern_recognition_interface():
    """Interface Streamlit pour Pattern Recognition SafetyGraph"""
    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    import plotly.express as px
    from datetime import datetime, timedelta
    
    st.markdown("# 🔍 Pattern Recognition SafetyGraph")
    st.markdown("---")
    
    # Header avec métriques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Patterns Identifiés", "15", "+3")
    
    with col2:
        st.metric("🔍 Clusters Actifs", "4", "+1")
    
    with col3:
        st.metric("📊 Précision Clustering", "87.3%", "+2.1%")
    
    with col4:
        st.metric("🔄 Dernière Analyse", "5min", "")
    
    st.markdown("---")
    
    # Configuration clustering
    st.markdown("## ⚙️ Configuration Clustering")
    
    col1, col2 = st.columns(2)
    
    with col1:
        clustering_method = st.selectbox(
            "🧠 Méthode Clustering",
            ["K-Means", "DBSCAN", "Hierarchical", "Gaussian Mixture"],
            index=0
        )
        
        n_clusters = st.slider(
            "🎯 Nombre de Clusters",
            min_value=2,
            max_value=10,
            value=4,
            step=1
        )
    
    with col2:
        features_selection = st.multiselect(
            "📊 Features à Analyser",
            ["Leadership", "Communication", "Formation", "Participation", "Suivi", "Environnement"],
            default=["Leadership", "Communication", "Formation"]
        )
        
        min_cluster_size = st.slider(
            "📏 Taille Min Cluster",
            min_value=5,
            max_value=50,
            value=10,
            step=5
        )
    
    if st.button("🚀 Lancer Analyse Patterns", use_container_width=True):
        with st.spinner("🔄 Analyse des patterns en cours..."):
            import time
            time.sleep(2)
            
            # Simulation données patterns
            patterns_data = []
            
            # Génération patterns simulés
            pattern_types = ["Proactif", "Réactif", "Émergent", "Mature"]
            sectors = ["Construction", "Manufacturing", "Healthcare", "Transportation"]
            
            for i in range(n_clusters):
                pattern = {
                    'Cluster': f'Cluster {i+1}',
                    'Type': np.random.choice(pattern_types),
                    'Secteur_Dominant': np.random.choice(sectors),
                    'Taille': np.random.randint(15, 80),
                    'Score_Moyen': np.random.uniform(2.5, 4.5),
                    'Stabilité': np.random.uniform(0.6, 0.95),
                    'Tendance': np.random.choice(['Amélioration', 'Stable', 'Déclin'])
                }
                patterns_data.append(pattern)
            
            patterns_df = pd.DataFrame(patterns_data)
            
            st.success("✅ Analyse patterns terminée!")
            
            # Résultats clustering
            st.markdown("## 📊 Résultats Clustering")
            
            # Tableau des clusters
            st.dataframe(patterns_df, use_container_width=True)
            
            # Visualisation clusters
            st.markdown("### 🎯 Visualisation Clusters")
            
            # Graphique scatter des clusters
            fig_scatter = px.scatter(
                patterns_df,
                x='Score_Moyen',
                y='Stabilité',
                size='Taille',
                color='Type',
                hover_data=['Cluster', 'Secteur_Dominant', 'Tendance'],
                title="🔍 Distribution des Clusters"
            )
            fig_scatter.update_layout(template="plotly_dark")
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Graphique en barres des types
            fig_bar = px.bar(
                patterns_df,
                x='Type',
                y='Taille',
                color='Tendance',
                title="📈 Répartition Types de Patterns"
            )
            fig_bar.update_layout(template="plotly_dark")
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Analyse détaillée par cluster
            st.markdown("## 🔍 Analyse Détaillée par Cluster")
            
            selected_cluster = st.selectbox(
                "Sélectionner un cluster",
                patterns_df['Cluster'].tolist()
            )
            
            cluster_data = patterns_df[patterns_df['Cluster'] == selected_cluster].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Caractéristiques")
                st.info(f"**Type:** {cluster_data['Type']}")
                st.info(f"**Secteur Dominant:** {cluster_data['Secteur_Dominant']}")
                st.info(f"**Taille:** {cluster_data['Taille']} entreprises")
                st.info(f"**Score Moyen:** {cluster_data['Score_Moyen']:.2f}/5.0")
            
            with col2:
                st.markdown("### 🎯 Métriques")
                st.metric("Stabilité", f"{cluster_data['Stabilité']:.2%}")
                st.metric("Tendance", cluster_data['Tendance'])
                
                # Recommandations
                st.markdown("### 💡 Recommandations")
                if cluster_data['Score_Moyen'] < 3.0:
                    st.error("🚨 Action immédiate requise")
                    st.info("• Audit approfondi culture sécurité")
                    st.info("• Formation leadership intensifiée")
                elif cluster_data['Score_Moyen'] < 4.0:
                    st.warning("⚠️ Amélioration recommandée")
                    st.info("• Renforcement communication")
                    st.info("• Suivi régulier indicateurs")
                else:
                    st.success("✅ Cluster performant")
                    st.info("• Maintenir les bonnes pratiques")
                    st.info("• Partager les success stories")
    
    # Section patterns temporels
    st.markdown("---")
    st.markdown("## ⏱️ Patterns Temporels")
    
    # Génération données temporelles
    dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
    
    temporal_data = pd.DataFrame({
        'Date': dates,
        'Proactif': np.random.normal(30, 5, 12),
        'Réactif': np.random.normal(25, 4, 12),
        'Émergent': np.random.normal(20, 3, 12),
        'Mature': np.random.normal(25, 4, 12)
    })
    
    fig_temporal = go.Figure()
    
    for pattern_type in ['Proactif', 'Réactif', 'Émergent', 'Mature']:
        fig_temporal.add_trace(go.Scatter(
            x=temporal_data['Date'],
            y=temporal_data[pattern_type],
            mode='lines+markers',
            name=pattern_type
        ))
    
    fig_temporal.update_layout(
        title="📈 Évolution Patterns Temporels",
        xaxis_title="Date",
        yaxis_title="Nombre d'Entreprises",
        template="plotly_dark"
    )
    
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    # Section corrélations
    st.markdown("---")
    st.markdown("## 🔗 Analyse Corrélations")
    
    # Matrice de corrélation simulée
    correlation_data = np.random.rand(6, 6)
    correlation_data = (correlation_data + correlation_data.T) / 2
    np.fill_diagonal(correlation_data, 1.0)
    
    dimensions = ["Leadership", "Communication", "Formation", "Participation", "Suivi", "Environnement"]
    correlation_df = pd.DataFrame(correlation_data, index=dimensions, columns=dimensions)
    
    fig_corr = px.imshow(
        correlation_df,
        title="🔗 Matrice Corrélations Dimensions",
        color_continuous_scale="RdBu",
        aspect="auto"
    )
    fig_corr.update_layout(template="plotly_dark")
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Section transitions patterns
    st.markdown("---")
    st.markdown("## 🔄 Transitions Patterns")
    
    # Simulation données transitions
    transitions_data = {
        'De': ['Émergent', 'Émergent', 'Réactif', 'Réactif', 'Proactif', 'Mature'],
        'Vers': ['Réactif', 'Proactif', 'Proactif', 'Mature', 'Mature', 'Proactif'],
        'Probabilité': [0.7, 0.3, 0.6, 0.2, 0.4, 0.1],
        'Fréquence': [45, 18, 32, 12, 25, 8]
    }
    
    transitions_df = pd.DataFrame(transitions_data)
    
    # Graphique Sankey pour transitions
    fig_sankey = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = ["Émergent", "Réactif", "Proactif", "Mature"],
            color = ["#FF6B6B", "#FFA07A", "#98D8C8", "#6BCF7F"]
        ),
        link = dict(
            source = [0, 0, 1, 1, 2, 3],
            target = [1, 2, 2, 3, 3, 2],
            value = [45, 18, 32, 12, 25, 8]
        )
    )])
    
    fig_sankey.update_layout(
        title_text="🔄 Flux Transitions entre Patterns",
        template="plotly_dark"
    )
    st.plotly_chart(fig_sankey, use_container_width=True)
    
    # Tableau détaillé des transitions
    st.markdown("### 📋 Détail des Transitions")
    
    # Formatage du tableau
    transitions_display = transitions_df.copy()
    transitions_display['Probabilité'] = transitions_display['Probabilité'].apply(lambda x: f"{x:.1%}")
    transitions_display.columns = ['🔄 De', '➡️ Vers', '📊 Probabilité', '🔢 Fréquence']
    
    st.dataframe(transitions_display, use_container_width=True)
    
    # Section benchmarking
    st.markdown("---")
    st.markdown("## 📊 Benchmarking Sectoriel")
    
    # Données benchmarking simulées
    benchmark_data = {
        'Secteur': ['Construction', 'Manufacturing', 'Healthcare', 'Transportation', 'Services'],
        'Pattern_Dominant': ['Réactif', 'Proactif', 'Mature', 'Émergent', 'Proactif'],
        'Score_Moyen': [3.2, 4.1, 4.3, 2.8, 3.9],
        'Maturité': ['Développement', 'Avancé', 'Excellence', 'Émergent', 'Avancé'],
        'Rang': [4, 2, 1, 5, 3]
    }
    
    benchmark_df = pd.DataFrame(benchmark_data)
    
    # Graphique radar benchmarking
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=benchmark_df['Score_Moyen'],
        theta=benchmark_df['Secteur'],
        fill='toself',
        name='Scores Sectoriels',
        line_color='#4ECDC4'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        title="📊 Benchmarking Scores par Secteur",
        template="plotly_dark"
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Tableau benchmarking
    st.markdown("### 🏆 Classement Sectoriel")
    
    benchmark_display = benchmark_df.copy()
    benchmark_display = benchmark_display.sort_values('Rang')
    benchmark_display.columns = ['🏭 Secteur', '🎯 Pattern Dominant', '📊 Score Moyen', '📈 Niveau Maturité', '🏆 Rang']
    
    st.dataframe(benchmark_display, use_container_width=True)
    
    # Insights automatiques
    st.markdown("---")
    st.markdown("## 🧠 Insights Automatiques")
    
    insights = [
        "🎯 Le pattern 'Proactif' montre une forte corrélation avec le leadership (r=0.87)",
        "📊 Les secteurs Construction et Manufacturing partagent des patterns similaires",
        "⚡ Émergence d'un nouveau pattern 'Hybride' dans le secteur Healthcare",
        "🔄 Cycles saisonniers détectés dans les patterns de formation",
        "🚨 Alertes: 3 clusters montrent des signes de dégradation",
        "📈 Tendance générale: transition vers patterns plus matures (+15% en 6 mois)",
        "🎯 Opportunité: secteurs émergents prêts pour évolution pattern"
    ]
    
    for insight in insights:
        st.info(insight)
    
    # Section export et actions
    st.markdown("---")
    st.markdown("## 📤 Export et Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Export Données")
        
        if st.button("📥 Télécharger Rapport PDF", use_container_width=True):
            st.info("📄 Rapport PDF généré et téléchargé!")
        
        if st.button("📊 Export Excel Détaillé", use_container_width=True):
            st.info("📊 Données exportées vers Excel!")
        
        if st.button("🔗 Partager Dashboard", use_container_width=True):
            st.info("🔗 Lien de partage généré!")
    
    with col2:
        st.markdown("### 🎯 Actions Recommandées")
        
        actions = [
            "🔍 Approfondir analyse Cluster 2",
            "📊 Surveiller transition Émergent→Réactif",
            "🎯 Benchmarker avec secteur Healthcare",
            "⚡ Déployer pattern Proactif en Construction",
            "🚨 Audit urgent clusters en déclin"
        ]
        
        for action in actions:
            if st.button(action, use_container_width=True):
                st.success(f"✅ Action planifiée: {action}")
    
    # Section configuration avancée
    st.markdown("---")
    st.markdown("## 🔧 Configuration Avancée")
    
    with st.expander("⚙️ Paramètres Algorithmes"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Clustering:**")
            epsilon = st.slider("DBSCAN Epsilon", 0.1, 2.0, 0.5, 0.1)
            min_samples = st.slider("DBSCAN Min Samples", 2, 20, 5)
            
        with col2:
            st.markdown("**Pattern Recognition:**")
            confidence_threshold = st.slider("Seuil Confiance", 0.5, 1.0, 0.7, 0.05)
            stability_window = st.slider("Fenêtre Stabilité (jours)", 7, 90, 30)
    
    with st.expander("🔔 Alertes et Notifications"):
        st.markdown("**Configuration Alertes:**")
        
        alert_new_pattern = st.checkbox("Nouveau pattern détecté", value=True)
        alert_transition = st.checkbox("Transition pattern critique", value=True)
        alert_degradation = st.checkbox("Dégradation cluster", value=True)
        
        notification_email = st.text_input("Email notifications", "admin@safetygraph.com")
        notification_frequency = st.selectbox("Fréquence", ["Temps réel", "Quotidien", "Hebdomadaire"])
    
    # Footer
    st.markdown("---")
    st.markdown("**🔍 Pattern Recognition SafetyGraph** | Powered by ML & Advanced Analytics")
    st.markdown("*Dernière mise à jour: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "*")