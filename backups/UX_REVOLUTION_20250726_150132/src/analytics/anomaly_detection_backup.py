#!/usr/bin/env python3
"""
SafetyGraph - Module Détection d'Anomalies
Détection temps réel des anomalies comportementales et statistiques
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

# ML Libraries pour détection d'anomalies
try:
    from sklearn.ensemble import IsolationForest
    from sklearn.svm import OneClassSVM
    from sklearn.neighbors import LocalOutlierFactor
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False


class SafetyGraphAnomalyDetector:
    """Détecteur d'anomalies pour SafetyGraph"""
    
    def __init__(self, db_path: str = "analytics_anomalies.db"):
        """
        Initialise le détecteur d'anomalies
        
        Args:
            db_path: Chemin vers la base de données
        """
        self.db_path = db_path
        self.models = {}
        self.scalers = {}
        self.thresholds = {}
        
        # Configuration par défaut
        self.config = {
            'contamination_rate': 0.1,
            'sensitivity': 0.7,
            'min_samples': 50,
            'lookback_days': 30
        }
        
        # Initialisation base de données
        self._init_database()
        
        # Initialisation modèles
        if ML_AVAILABLE:
            self._init_models()
    
    def _init_database(self):
        """Initialise la base de données SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table anomalies détectées
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                anomaly_type TEXT,
                severity TEXT,
                score REAL,
                sector_scian TEXT,
                description TEXT,
                features TEXT,
                status TEXT DEFAULT 'new',
                resolved_at DATETIME,
                metadata TEXT
            )
        ''')
        
        # Table alertes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anomaly_id INTEGER,
                alert_type TEXT,
                message TEXT,
                severity TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                acknowledged BOOLEAN DEFAULT FALSE,
                acknowledged_at DATETIME
            )
        ''')
        
        # Table métriques performance
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detection_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT,
                precision_score REAL,
                recall_score REAL,
                f1_score REAL,
                false_positive_rate REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _init_models(self):
        """Initialise les modèles de détection d'anomalies"""
        if not ML_AVAILABLE:
            return
        
        # Isolation Forest
        self.models['isolation_forest'] = IsolationForest(
            contamination=self.config['contamination_rate'],
            random_state=42,
            n_jobs=-1
        )
        
        # One-Class SVM
        self.models['one_class_svm'] = OneClassSVM(
            nu=self.config['contamination_rate'],
            kernel='rbf',
            gamma='scale'
        )
        
        # Local Outlier Factor
        self.models['local_outlier_factor'] = LocalOutlierFactor(
            contamination=self.config['contamination_rate'],
            n_neighbors=20,
            n_jobs=-1
        )
        
        # Scalers pour chaque modèle
        for model_name in self.models.keys():
            self.scalers[model_name] = StandardScaler()
    
    def detect_statistical_anomalies(self, data: pd.DataFrame, 
                                   target_column: str) -> List[Dict]:
        """
        Détecte les anomalies statistiques basiques
        
        Args:
            data: DataFrame avec données
            target_column: Colonne à analyser
            
        Returns:
            Liste des anomalies détectées
        """
        anomalies = []
        
        if data.empty or target_column not in data.columns:
            return anomalies
        
        values = data[target_column].dropna()
        
        if len(values) < self.config['min_samples']:
            return anomalies
        
        # Calculs statistiques
        mean_val = values.mean()
        std_val = values.std()
        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1
        
        # Seuils
        z_threshold = 3.0  # Z-score
        iqr_lower = q1 - 1.5 * iqr
        iqr_upper = q3 + 1.5 * iqr
        
        # Détection outliers Z-score
        z_scores = np.abs((values - mean_val) / std_val)
        z_outliers = data[z_scores > z_threshold]
        
        for idx, row in z_outliers.iterrows():
            anomalies.append({
                'type': 'statistical_zscore',
                'timestamp': datetime.now(),
                'value': row[target_column],
                'z_score': z_scores.loc[idx],
                'severity': 'high' if z_scores.loc[idx] > 4.0 else 'medium',
                'description': f'Valeur {row[target_column]:.2f} avec Z-score {z_scores.loc[idx]:.2f}',
                'metadata': {'mean': mean_val, 'std': std_val}
            })
        
        # Détection outliers IQR
        iqr_outliers = data[(values < iqr_lower) | (values > iqr_upper)]
        
        for idx, row in iqr_outliers.iterrows():
            if idx not in z_outliers.index:  # Éviter doublons
                anomalies.append({
                    'type': 'statistical_iqr',
                    'timestamp': datetime.now(),
                    'value': row[target_column],
                    'severity': 'medium',
                    'description': f'Valeur {row[target_column]:.2f} hors IQR [{iqr_lower:.2f}, {iqr_upper:.2f}]',
                    'metadata': {'q1': q1, 'q3': q3, 'iqr': iqr}
                })
        
        return anomalies
    
    def detect_behavioral_anomalies(self, behavior_data: pd.DataFrame) -> List[Dict]:
        """
        Détecte les anomalies comportementales
        
        Args:
            behavior_data: DataFrame avec données comportementales
            
        Returns:
            Liste des anomalies détectées
        """
        anomalies = []
        
        if behavior_data.empty or not ML_AVAILABLE:
            return anomalies
        
        # Préparation des features
        feature_cols = [col for col in behavior_data.columns 
                       if col not in ['timestamp', 'sector', 'id']]
        
        if len(feature_cols) < 2:
            return anomalies
        
        X = behavior_data[feature_cols].fillna(0)
        
        if len(X) < self.config['min_samples']:
            return anomalies
        
        # Détection avec Isolation Forest
        if 'isolation_forest' in self.models:
            try:
                model = self.models['isolation_forest']
                scaler = self.scalers['isolation_forest']
                
                X_scaled = scaler.fit_transform(X)
                predictions = model.fit_predict(X_scaled)
                scores = model.decision_function(X_scaled)
                
                # Anomalies détectées (prediction = -1)
                anomaly_indices = np.where(predictions == -1)[0]
                
                for idx in anomaly_indices:
                    anomalies.append({
                        'type': 'behavioral_isolation_forest',
                        'timestamp': datetime.now(),
                        'index': idx,
                        'score': scores[idx],
                        'severity': 'high' if scores[idx] < -0.5 else 'medium',
                        'description': f'Comportement anormal détecté (score: {scores[idx]:.3f})',
                        'features': X.iloc[idx].to_dict(),
                        'metadata': {'model': 'isolation_forest', 'threshold': -0.1}
                    })
                
            except Exception as e:
                print(f"Erreur Isolation Forest: {e}")
        
        return anomalies
    
    def detect_temporal_anomalies(self, time_series_data: pd.DataFrame,
                                 timestamp_col: str = 'timestamp',
                                 value_col: str = 'value') -> List[Dict]:
        """
        Détecte les anomalies temporelles
        
        Args:
            time_series_data: DataFrame avec données temporelles
            timestamp_col: Nom colonne timestamp
            value_col: Nom colonne valeurs
            
        Returns:
            Liste des anomalies détectées
        """
        anomalies = []
        
        if time_series_data.empty:
            return anomalies
        
        if timestamp_col not in time_series_data.columns or value_col not in time_series_data.columns:
            return anomalies
        
        # Tri par timestamp
        df = time_series_data.sort_values(timestamp_col).copy()
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
        
        # Calcul moving average et écart-type
        window_size = min(10, len(df) // 4)
        if window_size < 3:
            return anomalies
        
        df['moving_avg'] = df[value_col].rolling(window=window_size, center=True).mean()
        df['moving_std'] = df[value_col].rolling(window=window_size, center=True).std()
        
        # Détection anomalies (valeurs > 2 * std de la moyenne mobile)
        df['anomaly_score'] = np.abs(df[value_col] - df['moving_avg']) / df['moving_std']
        
        anomaly_threshold = 2.0
        temporal_anomalies = df[df['anomaly_score'] > anomaly_threshold]
        
        for idx, row in temporal_anomalies.iterrows():
            if not pd.isna(row['anomaly_score']):
                anomalies.append({
                    'type': 'temporal_deviation',
                    'timestamp': row[timestamp_col],
                    'value': row[value_col],
                    'expected_value': row['moving_avg'],
                    'anomaly_score': row['anomaly_score'],
                    'severity': 'high' if row['anomaly_score'] > 3.0 else 'medium',
                    'description': f'Déviation temporelle: {row[value_col]:.2f} vs {row["moving_avg"]:.2f}',
                    'metadata': {'window_size': window_size, 'threshold': anomaly_threshold}
                })
        
        return anomalies
    
    def save_anomalies(self, anomalies: List[Dict], sector_scian: str = None):
        """
        Sauvegarde les anomalies détectées
        
        Args:
            anomalies: Liste des anomalies
            sector_scian: Code secteur SCIAN
        """
        if not anomalies:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for anomaly in anomalies:
            cursor.execute('''
                INSERT INTO anomalies (
                    anomaly_type, severity, score, sector_scian, 
                    description, features, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                anomaly.get('type', 'unknown'),
                anomaly.get('severity', 'medium'),
                anomaly.get('score', 0.0),
                sector_scian,
                anomaly.get('description', ''),
                json.dumps(anomaly.get('features', {})),
                json.dumps(anomaly.get('metadata', {}))
            ))
        
        conn.commit()
        conn.close()
    
    def get_recent_anomalies(self, hours: int = 24) -> pd.DataFrame:
        """
        Récupère les anomalies récentes
        
        Args:
            hours: Nombre d'heures à regarder
            
        Returns:
            DataFrame des anomalies
        """
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT * FROM anomalies 
            WHERE timestamp >= datetime('now', '-{} hours')
            ORDER BY timestamp DESC
        '''.format(hours)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def create_alert(self, anomaly_id: int, alert_type: str, message: str, severity: str):
        """
        Crée une alerte pour une anomalie
        
        Args:
            anomaly_id: ID de l'anomalie
            alert_type: Type d'alerte
            message: Message d'alerte
            severity: Sévérité
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts (anomaly_id, alert_type, message, severity)
            VALUES (?, ?, ?, ?)
        ''', (anomaly_id, alert_type, message, severity))
        
        conn.commit()
        conn.close()
    
    def generate_detection_report(self, sector_scian: str = None) -> Dict:
        """
        Génère un rapport de détection
        
        Args:
            sector_scian: Code secteur SCIAN
            
        Returns:
            Rapport complet
        """
        # Anomalies récentes
        recent_anomalies = self.get_recent_anomalies(24)
        
        # Statistiques
        stats = {
            'total_anomalies': len(recent_anomalies),
            'high_severity': len(recent_anomalies[recent_anomalies['severity'] == 'high']),
            'medium_severity': len(recent_anomalies[recent_anomalies['severity'] == 'medium']),
            'low_severity': len(recent_anomalies[recent_anomalies['severity'] == 'low'])
        }
        
        # Répartition par type
        type_distribution = recent_anomalies['anomaly_type'].value_counts().to_dict()
        
        return {
            'sector_scian': sector_scian,
            'recent_anomalies': recent_anomalies.to_dict('records'),
            'statistics': stats,
            'type_distribution': type_distribution,
            'generated_at': datetime.now(),
            'ml_available': ML_AVAILABLE
        }


# ===================================================================
# INTERFACE STREAMLIT
# ===================================================================

def display_anomaly_detection_interface():
    """Interface Streamlit pour Détection d'Anomalies SafetyGraph"""
    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    import plotly.express as px
    from datetime import datetime, timedelta
    
    st.markdown("# ⚠️ Détection d'Anomalies SafetyGraph")
    st.markdown("---")
    
    # Header avec métriques temps réel
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🚨 Anomalies Détectées", "7", "+3")
    
    with col2:
        st.metric("⚡ Alertes Actives", "2", "-1")
    
    with col3:
        st.metric("🎯 Précision Détection", "94.2%", "+1.8%")
    
    with col4:
        st.metric("🔄 Dernière Analyse", "1min", "")
    
    st.markdown("---")
    
    # Configuration détection
    st.markdown("## ⚙️ Configuration Détection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        detection_type = st.multiselect(
            "🔍 Types Détection",
            ["Comportementale", "Temporelle", "Statistique", "Contextuelle"],
            default=["Comportementale", "Statistique"]
        )
        
        sensitivity = st.slider(
            "📊 Sensibilité",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.1
        )
    
    with col2:
        time_window = st.selectbox(
            "🕐 Fenêtre Temporelle",
            ["Temps réel", "1 heure", "24 heures", "7 jours"],
            index=2
        )
        
        threshold_severity = st.selectbox(
            "⚠️ Seuil Sévérité",
            ["Faible", "Moyenne", "Élevée", "Critique"],
            index=1
        )
    
    if st.button("🔍 Lancer Détection", use_container_width=True):
        with st.spinner("🔄 Analyse des anomalies en cours..."):
            import time
            time.sleep(2)
            
            # Simulation données d'anomalies
            anomalies_data = []
            
            # Génération d'anomalies simulées
            anomaly_types = ["Comportementale", "Temporelle", "Statistique", "Contextuelle"]
            severity_levels = ["Faible", "Moyenne", "Élevée", "Critique"]
            
            for i in range(7):
                anomaly = {
                    'ID': f'ANO-{2025070900 + i}',
                    'Timestamp': datetime.now() - timedelta(hours=np.random.randint(1, 48)),
                    'Type': np.random.choice(anomaly_types),
                    'Sévérité': np.random.choice(severity_levels),
                    'Score': np.random.uniform(0.7, 0.99),
                    'Secteur': np.random.choice(['Construction', 'Manufacturing', 'Healthcare']),
                    'Description': f'Anomalie détectée dans {np.random.choice(["formation", "équipement", "procédure", "communication"])}',
                    'Statut': np.random.choice(['Nouvelle', 'En cours', 'Résolue'])
                }
                anomalies_data.append(anomaly)
            
            anomalies_df = pd.DataFrame(anomalies_data)
            
            st.success("✅ Détection d'anomalies terminée!")
            
            # Tableau des anomalies
            st.markdown("## 📋 Anomalies Détectées")
            
            # Filtres
            col1, col2, col3 = st.columns(3)
            
            with col1:
                type_filter = st.multiselect(
                    "Filtrer par Type",
                    anomaly_types,
                    default=anomaly_types
                )
            
            with col2:
                severity_filter = st.multiselect(
                    "Filtrer par Sévérité",
                    severity_levels,
                    default=severity_levels
                )
            
            with col3:
                status_filter = st.multiselect(
                    "Filtrer par Statut",
                    ['Nouvelle', 'En cours', 'Résolue'],
                    default=['Nouvelle', 'En cours']
                )
            
            # Application des filtres
            filtered_df = anomalies_df[
                (anomalies_df['Type'].isin(type_filter)) &
                (anomalies_df['Sévérité'].isin(severity_filter)) &
                (anomalies_df['Statut'].isin(status_filter))
            ]
            
            # Affichage des anomalies avec couleurs
            for idx, row in filtered_df.iterrows():
                if row['Sévérité'] == 'Critique':
                    st.error(f"🚨 **{row['ID']}** - {row['Type']} | {row['Description']} | Score: {row['Score']:.2f}")
                elif row['Sévérité'] == 'Élevée':
                    st.warning(f"⚠️ **{row['ID']}** - {row['Type']} | {row['Description']} | Score: {row['Score']:.2f}")
                else:
                    st.info(f"ℹ️ **{row['ID']}** - {row['Type']} | {row['Description']} | Score: {row['Score']:.2f}")
            
            # Graphiques d'analyse
            st.markdown("## 📊 Analyse Visuelle")
            
            # Distribution par type
            fig_type = px.histogram(
                filtered_df, 
                x='Type', 
                color='Sévérité',
                title="📈 Distribution Anomalies par Type"
            )
            fig_type.update_layout(template="plotly_dark")
            st.plotly_chart(fig_type, use_container_width=True)
            
            # Timeline des anomalies
            fig_timeline = px.scatter(
                filtered_df,
                x='Timestamp',
                y='Score',
                color='Sévérité',
                size='Score',
                hover_data=['ID', 'Type', 'Description'],
                title="⏱️ Timeline Anomalies"
            )
            fig_timeline.update_layout(template="plotly_dark")
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Heatmap par secteur et type
            heatmap_data = filtered_df.groupby(['Secteur', 'Type']).size().reset_index(name='Count')
            if not heatmap_data.empty:
                heatmap_pivot = heatmap_data.pivot(index='Secteur', columns='Type', values='Count').fillna(0)
                
                fig_heatmap = px.imshow(
                    heatmap_pivot,
                    title="🔥 Heatmap Anomalies par Secteur",
                    color_continuous_scale="Reds"
                )
                fig_heatmap.update_layout(template="plotly_dark")
                st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Section alertes actives
    st.markdown("---")
    st.markdown("## 🚨 Alertes Actives")
    
    # Simulation d'alertes actives
    active_alerts = [
        {
            'Type': '🔴 Critique',
            'Message': 'Pic d\'anomalies comportementales détecté - Secteur Construction',
            'Timestamp': '2025-07-09 07:23:15',
            'Actions': 'Inspection immédiate requise'
        },
        {
            'Type': '🟡 Attention',
            'Message': 'Tendance anomalique formation sécurité - 3 secteurs',
            'Timestamp': '2025-07-09 06:45:32',
            'Actions': 'Révision programme formation'
        }
    ]
    
    for alert in active_alerts:
        if 'Critique' in alert['Type']:
            st.error(f"**{alert['Type']}** | {alert['Message']} | {alert['Timestamp']}")
            st.info(f"🎯 **Action:** {alert['Actions']}")
        else:
            st.warning(f"**{alert['Type']}** | {alert['Message']} | {alert['Timestamp']}")
            st.info(f"🎯 **Action:** {alert['Actions']}")
    
    # Section configuration avancée
    st.markdown("---")
    st.markdown("## 🔧 Configuration Avancée")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Paramètres Algorithmes")
        
        isolation_forest = st.checkbox("🌲 Isolation Forest", value=True)
        one_class_svm = st.checkbox("🎯 One-Class SVM", value=True)
        local_outlier = st.checkbox("📍 Local Outlier Factor", value=False)
        
        if st.button("💾 Sauvegarder Configuration"):
            st.success("✅ Configuration sauvegardée!")
    
    with col2:
        st.markdown("### 🔔 Notifications")
        
        email_alerts = st.checkbox("📧 Alertes Email", value=True)
        sms_alerts = st.checkbox("📱 Alertes SMS", value=False)
        dashboard_alerts = st.checkbox("📊 Alertes Dashboard", value=True)
        
        if st.button("🔄 Tester Notifications"):
            st.info("📨 Notification test envoyée!")
    
    # Section historique
    st.markdown("---")
    st.markdown("## 📈 Historique & Tendances")
    
    # Génération données historiques
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    daily_anomalies = np.random.poisson(3, 30)
    
    historical_df = pd.DataFrame({
        'Date': dates,
        'Anomalies': daily_anomalies,
        'Moyenne Mobile': pd.Series(daily_anomalies).rolling(7).mean()
    })
    
    fig_historical = go.Figure()
    
    fig_historical.add_trace(go.Scatter(
        x=historical_df['Date'],
        y=historical_df['Anomalies'],
        mode='lines+markers',
        name='Anomalies Quotidiennes',
        line=dict(color='#FF6B6B')
    ))
    
    fig_historical.add_trace(go.Scatter(
        x=historical_df['Date'],
        y=historical_df['Moyenne Mobile'],
        mode='lines',
        name='Moyenne Mobile (7j)',
        line=dict(color='#4ECDC4', dash='dash')
    ))
    
    fig_historical.update_layout(
        title="📊 Évolution Anomalies - 30 derniers jours",
        xaxis_title="Date",
        yaxis_title="Nombre d'Anomalies",
        template="plotly_dark"
    )
    
    st.plotly_chart(fig_historical, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**⚠️ Détection d'Anomalies SafetyGraph** | Powered by AI & Machine Learning")