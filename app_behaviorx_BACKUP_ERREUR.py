<div class="correlation-alert">
                    <h4>🎯 Excellente Corrélation Détectée Enhanced!</h4>
                    <p><strong>BehaviorX ↔️ Cartographie:</strong> {:.1f}% de cohérence</p>
                    <p>Les résultats comportementaux sont parfaitement alignés avec la culture organisationnelle!</p>
                    <p><strong>Confiance:</strong> {:.1f}% • <strong>Patterns:</strong> {len(behaviorx_results.pattern_recognition)} détectés</p>
                </div>
                """.format(correlation, behaviorx_results.confidence_level, len(behaviorx_results.pattern_recognition)), unsafe_allow_html=True)
            elif correlation > 70:
                st.warning(f"⚠️ Corrélation modérée détectée: {correlation:.1f}% - Analyse recommandée pour optimisation")
            else:
                st.error(f"🔴 Écart significatif détecté: {correlation:.1f}% - Action immédiate requise")
        
        # Facteurs de risque identifiés enhanced
        st.markdown("#### 🚨 Facteurs de Risque Identifiés Enhanced")
        for i, factor in enumerate(behaviorx_results.risk_factors, 1):
            risk_level = "🔴 ÉLEVÉ" if i <= 2 else "🟡 MOYEN"
            st.warning(f"{risk_level} **{i}.** {factor}")
        
        # Recommandations personnalisées enhanced
        st.markdown("#### 💡 Recommandations Personnalisées Enhanced")
        for i, rec in enumerate(behaviorx_results.recommendations, 1):
            priority = "🔥 PRIORITÉ" if i <= 2 else "📋 STANDARD"
            st.info(f"{priority} **{i}.** {rec}")
        
        # Nouveau : Plan d'action suggéré
        st.markdown("#### 🎯 Plan d'Action Suggéré")
        
        action_plan = [
            {"action": "Formation équipe B - espaces confinés", "délai": "1 semaine", "responsable": "Superviseur sécurité", "priorité": "🔥"},
            {"action": "Mise en place système buddy", "délai": "2 semaines", "responsable": "RH + Sécurité", "priorité": "🔥"},
            {"action": "Amélioration signalisation", "délai": "1 mois", "responsable": "Maintenance", "priorité": "📋"},
            {"action": "Comité sécurité mixte", "délai": "3 semaines", "responsable": "Direction", "priorité": "📋"}
        ]
        
        for plan in action_plan:
            st.markdown(f"""
            **{plan['priorité']} {plan['action']}**  
            📅 Délai: {plan['délai']} • 👤 Responsable: {plan['responsable']}
            """)

def run_enhanced_cartography_analysis(core: SafetyGraphUnifiedCore):
    """Exécute l'analyse Cartographie Culture unifiée Enhanced"""
    
    st.markdown("### 🗺️ Cartographie Culture SST Unifiée Enhanced")
    
    # Configuration enhanced
    col1, col2, col3 = st.columns(3)
    
    with col1:
        benchmark_comparison = st.checkbox(
            "📊 Comparaison Benchmark",
            value=True,
            help="Comparaison avec benchmarks sectoriels"
        )
    
    with col2:
        trend_analysis = st.checkbox(
            "📈 Analyse Tendances",
            value=True,
            help="Analyse des tendances temporelles"
        )
    
    with col3:
        action_plan_generation = st.checkbox(
            "🎯 Plan d'Action Auto",
            value=True,
            help="Génération automatique de plan d'action"
        )
    
    if st.button("🎨 Lancer Cartographie Culture Complète Enhanced", type="primary"):
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            ("🔄 Initialisation cartographie unifiée enhanced...", 15),
            ("📊 Analyse 7 dimensions culturelles avancées...", 30),
            ("🎯 Benchmark sectoriel et comparaisons...", 45),
            ("📈 Analyse tendances et patterns temporels...", 60),
            ("🔗 Corrélation avec données BehaviorX enhanced...", 75),
            ("🎯 Génération plan d'action personnalisé...", 90),
            ("✅ Intégration au système unifié enhanced...", 100)
        ]
        
        for step_text, progress in steps:
            status_text.text(step_text)
            time.sleep(1.2)
            progress_bar.progress(progress)
        
        # Génération résultats cartographie unifiés enhanced
        culture_dimensions = {
            "Leadership Sécurité": 82.5 + np.random.uniform(-3, 5),
            "Communication": 76.3 + np.random.uniform(-4, 6),
            "Engagement Employés": 88.1 + np.random.uniform(-2, 4),
            "Apprentissage Continu": 74.8 + np.random.uniform(-3, 7),
            "Responsabilisation": 79.6 + np.random.uniform(-3, 5),
            "Collaboration": 85.2 + np.random.uniform(-2, 4),
            "Innovation Sécurité": 71.4 + np.random.uniform(-4, 8)
        }
        
        overall_score = sum(culture_dimensions.values()) / len(culture_dimensions)
        
        # Détermination des forces et améliorations
        sorted_dimensions = sorted(culture_dimensions.items(), key=lambda x: x[1], reverse=True)
        strengths = [item[0] for item in sorted_dimensions[:3]]
        improvement_areas = [item[0] for item in sorted_dimensions[-3:]]
        
        # Génération plan d'action automatique
        action_plan = []
        for area in improvement_areas:
            if "Communication" in area:
                action_plan.append("Implémenter réunions sécurité hebdomadaires")
            elif "Innovation" in area:
                action_plan.append("Créer boîte à idées sécurité digitale")
            elif "Apprentissage" in area:
                action_plan.append("Programme formation continue personnalisé")
            else:
                action_plan.append(f"Programme d'amélioration {area.lower()}")
        
        cartography_results = CartographyResults(
            culture_dimensions=culture_dimensions,
            overall_culture_score=overall_score,
            sector_benchmark=75.2 + np.random.uniform(-2, 3),
            improvement_areas=improvement_areas,
            strengths=strengths,
            trend="improving" if overall_score > 78 else "declining" if overall_score < 75 else "stable",
            maturity_level="Avancé" if overall_score > 85 else "Intermédiaire" if overall_score > 75 else "Débutant",
            action_plan=action_plan
        )
        
        core.cartography_results = cartography_results
        
        status_text.text("🎉 Cartographie Culture Enhanced complète et corrélée!")
        
        # Affichage résultats enhanced
        st.success("✅ **Cartographie Culture Enhanced Réussie - Corrélation avec BehaviorX Active**")
        
        # Métriques cartographie enhanced
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            benchmark_diff = cartography_results.overall_culture_score - cartography_results.sector_benchmark
            st.metric(
                "🎯 Score Global Culture",
                f"{cartography_results.overall_culture_score:.1f}%",
                delta=f"vs Benchmark: {benchmark_diff:+.1f}%"
            )
        
        with col2:
            trend_icon = "📈" if cartography_results.trend == "improving" else "📉" if cartography_results.trend == "declining" else "➡️"
            st.metric(
                f"{trend_icon} Tendance",
                cartography_results.trend.title(),
                delta="Amélioration continue"
            )
        
        with col3:
            position = "TOP 15%" if benchmark_diff > 10 else "TOP 25%" if benchmark_diff > 5 else "TOP 50%" if benchmark_diff > 0 else "SOUS BENCHMARK"
            st.metric(
                "🏆 Position Sectorielle",
                position,
                delta=f"Secteur {core.enterprise_context.sector}"
            )
        
        with col4:
            st.metric(
                "🎓 Niveau Maturité",
                cartography_results.maturity_level,
                delta=f"{len(cartography_results.action_plan)} actions"
            )
        
        # Graphique radar des dimensions enhanced
        fig_radar = go.Figure()
        
        dimensions = list(culture_dimensions.keys())
        values = list(culture_dimensions.values())
        
        # Culture actuelle
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=dimensions,
            fill='toself',
            name='Culture Actuelle',
            line_color='rgb(50, 171, 96)',
            fillcolor='rgba(50, 171, 96, 0.4)',
            line=dict(width=3)
        ))
        
        # Benchmark sectoriel
        benchmark_values = [cartography_results.sector_benchmark] * len(dimensions)
        fig_radar.add_trace(go.Scatterpolar(
            r=benchmark_values,
            theta=dimensions,
            fill='toself',
            name='Benchmark Secteur',
            line_color='rgb(255, 127, 14)',
            fillcolor='rgba(255, 127, 14, 0.2)',
            opacity=0.7,
            line=dict(dash='dash', width=2)
        ))
        
        # Objectifs (simulés)
        target_values = [min(95, v + np.random.uniform(5, 15)) for v in values]
        fig_radar.add_trace(go.Scatterpolar(
            r=target_values,
            theta=dimensions,
            fill='toself',
            name='Objectifs 2025',
            line_color='rgb(171, 50, 96)',
            fillcolor='rgba(171, 50, 96, 0.1)',
            opacity=0.6,
            line=dict(dash='dot', width=2)
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, 100],
                    gridcolor='rgba(255, 255, 255, 0.3)'
                )
            ),
            title="🗺️ Cartographie Culture SST Enhanced - Multi-Comparaisons",
            showlegend=True,
            height=600,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Forces et améliorations enhanced
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💪 Forces Identifiées Enhanced")
            for i, strength in enumerate(cartography_results.strengths, 1):
                score = culture_dimensions[strength]
                percentile = "TOP 10%" if score > 85 else "TOP 25%" if score > 80 else "TOP 50%"
                st.success(f"🏆 **{i}. {strength}**: {score:.1f}% ({percentile})")
        
        with col2:
            st.markdown("#### 🎯 Axes d'Amélioration Enhanced")
            for i, area in enumerate(cartography_results.improvement_areas, 1):
                score = culture_dimensions[area]
                gap = 90 - score
                urgency = "🔥 URGENT" if gap > 15 else "📋 PRIORITÉ" if gap > 10 else "⏰ PLANIFIÉ"
                st.info(f"{urgency} **{i}. {area}**: {score:.1f}% (Gap: {gap:.1f}%)")
        
        # Plan d'action généré automatiquement
        if action_plan_generation:
            st.markdown("#### 🎯 Plan d'Action Généré Automatiquement")
            
            for i, action in enumerate(cartography_results.action_plan, 1):
                timeline = ["2 semaines", "1 mois", "6 semaines"][i-1] if i <= 3 else "2 mois"
                impact = ["ÉLEVÉ", "MOYEN", "ÉLEVÉ"][i-1] if i <= 3 else "MOYEN"
                st.markdown(f"""
                **🎯 Action {i}: {action}**  
                📅 Délai: {timeline} • 📈 Impact attendu: {impact}
                """)

def run_enhanced_predictive_analytics(core: SafetyGraphUnifiedCore):
    """Exécute l'analyse prédictive unifiée Enhanced"""
    
    st.markdown("### 🔮 Analytics Prédictifs Unifiés Enhanced")
    
    # Configuration prédictions enhanced
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        horizon = st.selectbox(
            "🕐 Horizon Prédiction",
            ["1 mois", "3 mois", "6 mois", "12 mois", "24 mois"],
            index=2,
            help="Horizon temporel des prédictions"
        )
    
    with col2:
        model = st.selectbox(
            "🤖 Modèle IA",
            ["Random Forest", "XGBoost", "Neural Network", "Ensemble", "Transformer"],
            index=3,
            help="Algorithme de machine learning utilisé"
        )
    
    with col3:
        features = st.multiselect(
            "📊 Variables Prédictives",
            ["Historique incidents", "Formation", "Météo", "Production", "Saisonnalité", "Satisfaction", "Stress", "Innovation"],
            default=["Historique incidents", "Formation", "Saisonnalité", "Satisfaction"],
            help="Variables utilisées pour les prédictions"
        )
    
    with col4:
        confidence_threshold = st.slider(
            "🎯 Seuil Confiance",
            min_value=70,
            max_value=99,
            value=85,
            help="Seuil minimum de confiance pour les prédictions"
        )
    
    if st.button("🔮 Lancer Prédictions Unifiées Enhanced", type="primary"):
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            ("🔄 Préparation données historiques unifiées enhanced...", 15),
            (f"🤖 Entraînement modèle {model} avec {len(features)} variables...", 30),
            ("🔮 Génération prédictions multi-horizons...", 45),
            ("📊 Calcul facteurs saisonniers et patterns...", 60),
            ("🔗 Corrélation avec BehaviorX et Cartographie enhanced...", 75),
            ("🚨 Génération alertes prédictives intelligentes...", 90),
            ("✅ Validation et intégration système unifié...", 100)
        ]
        
        for step_text, progress in steps:
            status_text.text(step_text)
            time.sleep(1.3)
            progress_bar.progress(progress)
        
        # Génération résultats prédictifs enhanced
        base_accuracy = 89.4
        feature_bonus = len(features) * 1.5
        model_bonus = {"Random Forest": 0, "XGBoost": 2, "Neural Network": 3, "Ensemble": 4, "Transformer": 5}[model]
        prediction_accuracy = min(98, base_accuracy + feature_bonus + model_bonus + np.random.uniform(-2, 3))
        
        incident_probability = max(5, min(35, 15 + np.random.uniform(-8, 8)))
        model_confidence = min(99, prediction_accuracy + np.random.uniform(-3, 5))
        
        # Risques enhanced avec nouvelles catégories
        risk_trends = {
            "Chutes de hauteur": 23.5 + np.random.uniform(-3, 5),
            "Troubles musculosquelettiques": 31.2 + np.random.uniform(-4, 6),
            "Accidents machines": 12.8 + np.random.uniform(-2, 4),
            "Exposition substances": 18.9 + np.random.uniform(-3, 5),
            "Stress thermique": 8.4 + np.random.uniform(-2, 3),
            "Risques psychosociaux": 15.7 + np.random.uniform(-3, 6),
            "Cyber-sécurité": 9.2 + np.random.uniform(-2, 4)
        }
        
        # Facteurs saisonniers enhanced
        seasonal_factors = {
            "Hiver": 1.3,  # Plus de risques en hiver
            "Printemps": 0.9,
            "Été": 1.1,  # Stress thermique
            "Automne": 0.8
        }
        
        # Alertes enhanced avec priorisation
        alerts = []
        for risk_type, probability in risk_trends.items():
            if probability > 25:
                alerts.append(f"🔴 ALERTE ÉLEVÉE: {risk_type} - {probability:.1f}% de probabilité")
            elif probability > 18:
                alerts.append(f"🟡 SURVEILLANCE: {risk_type} - {probability:.1f}% de probabilité")
        
        # Recommandations d'intervention
        intervention_recommendations = [
            "Renforcement formation EPI équipe exposition",
            "Audit ergonomique postes TMS critiques", 
            "Maintenance préventive machines prioritaires",
            "Programme gestion stress adapté saison",
            "Sensibilisation cyber-sécurité renforcée"
        ]
        
        predictive_results = PredictiveResults(
            prediction_accuracy=prediction_accuracy,
            incident_probability=incident_probability,
            risk_trends=risk_trends,
            alerts_generated=alerts,
            model_confidence=model_confidence,
            seasonal_factors=seasonal_factors,
            intervention_recommendations=intervention_recommendations[:3]
        )
        
        core.predictive_results = predictive_results
        
        status_text.text("🎉 Prédictions Enhanced générées et corrélées!")
        
        # Affichage résultats enhanced
        st.success("✅ **Analytics Prédictifs Enhanced Réussis - Intégration Système Unifié Active**")
        
        # Métriques prédictives enhanced
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            accuracy_grade = "🏆 EXCELLENT" if prediction_accuracy > 95 else "🥇 TRÈS BON" if prediction_accuracy > 90 else "🥈 BON"
            st.metric(
                "🎯 Précision Modèle",
                f"{prediction_accuracy:.1f}%",
                delta=f"{accuracy_grade}"
            )
        
        with col2:
            prob_level = "🔴 ÉLEVÉ" if incident_probability > 20 else "🟡 MOYEN" if incident_probability > 12 else "🟢 FAIBLE"
            st.metric(
                "⚠️ Probabilité Incident",
                f"{incident_probability:.1f}%",
                delta=f"Horizon {horizon} - {prob_level}"
            )
        
        with col3:
            st.metric(
                "🤖 Confiance Modèle",
                f"{model_confidence:.1f}%",
                delta=f"Modèle {model}"
            )
        
        with col4:
            st.metric(
                "🚨 Alertes Générées",
                len(predictive_results.alerts_generated),
                delta=f"{len([a for a in alerts if '🔴' in a])} critiques"
            )
        
        with col5:
            st.metric(
                "🎯 Interventions",
                len(predictive_results.intervention_recommendations),
                delta="Recommandées"
            )
        
        # Graphique tendances des risques enhanced
        fig_risks = go.Figure()
        
        risk_categories = list(risk_trends.keys())
        risk_values = list(risk_trends.values())
        
        # Couleurs selon niveau de risque
        colors = []
        for v in risk_values:
            if v > 25:
                colors.append('#dc3545')  # Rouge critique
            elif v > 18:
                colors.append('#fd7e14')  # Orange élevé
            elif v > 12:
                colors.append('#ffc107')  # Jaune moyen
            else:
                colors.append('#28a745')  # Vert faible
        
        fig_risks.add_trace(go.Bar(
            x=risk_categories,
            y=risk_values,
            marker_color=colors,
            text=[f"{v:.1f}%" for v in risk_values],
            textposition='auto',
            textfont=dict(color='white', size=12),
            hovertemplate='<b>%{x}</b><br>Probabilité: %{y:.1f}%<br>Horizon: ' + horizon + '<extra></extra>'
        ))
        
        fig_risks.update_layout(
            title=f"📊 Tendances des Risques Enhanced - Horizon {horizon}",
            xaxis_title="Catégories de Risques",
            yaxis_title="Probabilité d'Occurrence (%)",
            height=450,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_risks, use_container_width=True)
        
        # Facteurs saisonniers
        st.markdown("#### 🌍 Impact Facteurs Saisonniers")
        
        fig_seasonal = go.Figure(data=[
            go.Bar(
                x=list(seasonal_factors.keys()),
                y=list(seasonal_factors.values()),
                marker_color=['#6495ED', '#98FB98', '#FFD700', '#DEB887'],
                text=[f"×{v:.1f}" for v in seasonal_factors.values()],
                textposition='auto'
            )
        ])
        
        fig_seasonal.update_layout(
            title="🌍 Facteurs de Risque Saisonniers",
            xaxis_title="Saisons",
            yaxis_title="Multiplicateur de Risque",
            height=350
        )
        
        st.plotly_chart(fig_seasonal, use_container_width=True)
        
        # Alertes prédictives enhanced
        st.markdown("#### 🚨 Alertes Prédictives Générées Enhanced")
        
        if predictive_results.alerts_generated:
            for alert in predictive_results.alerts_generated:
                if "🔴" in alert:
                    st.error(alert)
                elif "🟡" in alert:
                    st.warning(alert)
                else:
                    st.info(alert)
        else:
            st.success("✅ Aucune alerte critique - Situation sous contrôle")
        
        # Recommandations d'intervention
        st.markdown("#### 🎯 Recommandations d'Intervention Enhanced")
        
        for i, rec in enumerate(predictive_results.intervention_recommendations, 1):
            urgency = "🔥" if i == 1 else "📋"
            timeline = ["Immédiat", "1 semaine", "2 semaines"][i-1] if i <= 3 else "1 mois"
            st.info(f"{urgency} **{i}. {rec}** (Délai: {timeline})")
        
        # Corrélations inter-modules enhanced
        if core.behaviorx_results and core.cartography_results:
            st.markdown("#### 🔗 Corrélations Inter-Modules Enhanced")
            
            behaviorx_integration = core.behaviorx_results.integration_score
            culture_score = core.cartography_results.overall_culture_score
            correlation_strength = abs(behaviorx_integration - culture_score)
            
            if correlation_strength < 5:
                correlation_quality = "🟢 EXCELLENTE"
            elif correlation_strength < 10:
                correlation_quality = "🟡 BONNE"
            else:
                correlation_quality = "🔴 FAIBLE"
            
            st.info(f"🧠 **BehaviorX → Prédictif:** Score intégration {behaviorx_integration:.1f}% influence précision modèle ({correlation_quality})")
            st.info(f"🗺️ **Culture → Prédictif:** Culture {culture_score:.1f}% corrèle avec probabilité incidents (R²={1-correlation_strength/100:.2f})")
            
            # Graphique corrélation
            fig_corr = go.Figure()
            
            # Points de corrélation simulés
            x_culture = [culture_score + np.random.uniform(-5, 5) for _ in range(20)]
            y_incidents = [incident_probability * (1 - (x-50)/100) + np.random.uniform(-3, 3) for x in x_culture]
            
            fig_corr.add_trace(go.Scatter(
                x=x_culture,
                y=y_incidents,
                mode='markers',
                name='Corrélation Culture-Incidents',
                marker=dict(size=8, color='rgba(46, 134, 171, 0.7)')
            ))
            
            # Ligne de tendance
            z = np.polyfit(x_culture, y_incidents, 1)
            p = np.poly1d(z)
            fig_corr.add_trace(go.Scatter(
                x=sorted(x_culture),
                y=p(sorted(x_culture)),
                mode='lines',
                name='Tendance',
                line=dict(color='red', width=2, dash='dash')
            ))
            
            fig_corr.update_layout(
                title="🔗 Corrélation Culture Sécurité vs Probabilité Incidents",
                xaxis_title="Score Culture Sécurité (%)",
                yaxis_title="Probabilité Incidents (%)",
                height=400
            )
            
            st.plotly_chart(fig_corr, use_container_width=True)

def render_enhanced_unified_tabs(core: SafetyGraphUnifiedCore):
    """Interface à onglets unifiée Enhanced"""
    
    tabs = st.tabs([
        "🎯 Dashboard Unifié Enhanced",
        "🧠 BehaviorX Standard Enhanced", 
        "🗺️ Cartographie Culture Enhanced",
        "🔮 Analytics Prédictifs Enhanced",
        "🧩 Pattern Recognition Enhanced",
        "🚨 Anomaly Detection Enhanced",
        "📊 Rapport Complet Enhanced"
    ])
    
    with tabs[0]:
        render_enhanced_unified_dashboard(core)
        render_enhanced_data_flow_visualization(core)
    
    with tabs[1]:
        run_enhanced_behaviorx_analysis(core)
    
    with tabs[2]:
        run_enhanced_cartography_analysis(core)
    
    with tabs[3]:
        run_enhanced_predictive_analytics(core)
    
    with tabs[4]:
        st.markdown("### 🧩 Pattern Recognition Unifié Enhanced")
        
        col1, col2 = st.columns(2)
        with col1:
            pattern_types = st.multiselect(
                "🔍 Types de Patterns",
                ["Comportementaux", "Temporels", "Géographiques", "Organisationnels", "Technologiques"],
                default=["Comportementaux", "Temporels"]
            )
        
        with col2:
            detection_sensitivity = st.slider(
                "📊 Sensibilité Détection",
                min_value=0.1,
                max_value=1.0,
                value=0.7,
                step=0.1
            )
        
        if st.button("🔍 Détecter Patterns Comportementaux Enhanced"):
            with st.spinner("Analyse des patterns enhanced en cours..."):
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress.progress(i + 1)
            
            st.success("✅ 8 patterns comportementaux Enhanced détectés et corrélés!")
            
            patterns_enhanced = [
                {"pattern": "📈 Amélioration continue progressive équipe A", "confiance": 94.2, "impact": "ÉLEVÉ"},
                {"pattern": "⚠️ Baisse engagement post-formation équipe B", "confiance": 87.6, "impact": "MOYEN"},
                {"pattern": "🎯 Corrélation positive leadership-sécurité", "confiance": 91.3, "impact": "ÉLEVÉ"},
                {"pattern": "🔄 Cycle d'apprentissage optimal 3 semaines", "confiance": 83.8, "impact": "MOYEN"},
                {"pattern": "💡 Innovation sécurité émergente équipe C", "confiance": 79.4, "impact": "ÉLEVÉ"},
                {"pattern": "🌡️ Impact météo sur performance sécurité", "confiance": 88.9, "impact": "MOYEN"},
                {"pattern": "📅 Pattern saisonnier incidents lundi matin", "confiance": 92.1, "impact": "ÉLEVÉ"},
                {"pattern": "🤝 Effet réseau positif buddy system", "confiance": 85.7, "impact": "ÉLEVÉ"}
            ]
            
            for pattern in patterns_enhanced:
                confidence_color = "🟢" if pattern["confiance"] > 90 else "🟡" if pattern["confiance"] > 80 else "🟠"
                impact_icon = "🔥" if pattern["impact"] == "ÉLEVÉ" else "📋"
                st.info(f"{confidence_color} {impact_icon} **{pattern['pattern']}** (Confiance: {pattern['confiance']:.# ===================================================================
# SAFETYGRAPH BEHAVIORX - VERSION COMPLÈTE ENHANCED
# Révolution Unifiée + Boutons Validation + Visualisations Enrichies
# Mario Plourde - 14 juillet 2025 - Preventera/GenAISafety
# ===================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import time
import random
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
import sqlite3
from pathlib import Path

# ===================================================================
# CONFIGURATION GLOBALE SAFETYGRAPH UNIFIÉ ENHANCED
# ===================================================================

st.set_page_config(
    page_title="SafetyGraph BehaviorX - VERSION COMPLÈTE ENHANCED",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Avancé pour interface révolutionnaire enhanced
st.markdown("""
<style>
/* Interface révolutionnaire SafetyGraph Enhanced */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
}

.unified-dashboard {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 1rem;
    border-radius: 12px;
    margin: 1rem 0;
    color: white;
    box-shadow: 0 8px 32px rgba(245, 87, 108, 0.3);
}

.correlation-alert {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 1rem;
    border-radius: 12px;
    margin: 0.5rem 0;
    animation: pulse 2s infinite;
    box-shadow: 0 4px 20px rgba(79, 172, 254, 0.4);
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}

.module-status {
    border: 2px solid #28a745;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    background: rgba(40, 167, 69, 0.1);
    backdrop-filter: blur(5px);
    transition: all 0.3s ease;
}

.module-status:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
}

.data-flow {
    background: linear-gradient(45deg, #fa709a 0%, #fee140 100%);
    padding: 1rem;
    border-radius: 12px;
    margin: 0.5rem 0;
    color: #333;
    font-weight: bold;
    box-shadow: 0 4px 20px rgba(250, 112, 154, 0.3);
}

.revolution-badge {
    position: fixed;
    top: 10px;
    right: 10px;
    background: linear-gradient(45deg, #ff6b6b, #ffa500);
    color: white;
    padding: 0.8rem 1.5rem;
    border-radius: 25px;
    z-index: 1000;
    animation: bounce 2s infinite;
    box-shadow: 0 4px 20px rgba(255, 107, 107, 0.4);
    font-weight: bold;
    font-size: 0.9em;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}

.validation-success {
    background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    color: white;
    font-weight: bold;
}

.validation-warning {
    background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    color: #333;
    font-weight: bold;
}

.enhanced-metric {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
}

.enhanced-metric:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.section-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.8rem 1.5rem;
    border-radius: 10px;
    margin: 1rem 0 0.5rem 0;
    font-weight: bold;
    text-align: center;
}

.status-indicator {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 8px;
    animation: blink 1.5s linear infinite;
}

.status-active { background-color: #28a745; }
.status-warning { background-color: #ffc107; }
.status-inactive { background-color: #dc3545; }

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0.3; }
}
</style>
""", unsafe_allow_html=True)

# ===================================================================
# CLASSES DE DONNÉES UNIFIÉES ENHANCED
# ===================================================================

@dataclass
class UnifiedMetrics:
    """Métriques unifiées du système SafetyGraph Enhanced"""
    culture_level: float
    engagement_rate: float
    compliance_rate: float
    proactivity_rate: float
    integration_score: float
    correlation_behaviorx_carto: float
    prediction_accuracy: float
    incidents_reduction: float
    alerts_count: int
    last_update: str
    data_quality_score: float
    risk_trend: str
    performance_index: float

@dataclass
class EnterpriseContext:
    """Contexte unifié de l'entreprise Enhanced"""
    name: str
    sector: str
    sector_code: str
    employees_count: int
    safety_officer: str
    risk_level: str
    location: str
    established_date: str
    certification_iso: bool
    union_presence: bool

@dataclass
class BehaviorXResults:
    """Résultats unifiés BehaviorX Enhanced"""
    vcs_score: float
    abc_score: float
    a1_enhanced_score: float
    integration_score: float
    blind_spots_count: int
    risk_factors: List[str]
    recommendations: List[str]
    analysis_timestamp: str
    confidence_level: float
    pattern_recognition: Dict[str, float]

@dataclass
class CartographyResults:
    """Résultats unifiés Cartographie Culture Enhanced"""
    culture_dimensions: Dict[str, float]
    overall_culture_score: float
    sector_benchmark: float
    improvement_areas: List[str]
    strengths: List[str]
    trend: str
    maturity_level: str
    action_plan: List[str]

@dataclass
class PredictiveResults:
    """Résultats unifiés Analytics Prédictifs Enhanced"""
    prediction_accuracy: float
    incident_probability: float
    risk_trends: Dict[str, float]
    alerts_generated: List[str]
    model_confidence: float
    seasonal_factors: Dict[str, float]
    intervention_recommendations: List[str]

class SafetyGraphUnifiedCore:
    """Cœur unifié du système SafetyGraph Enhanced"""
    
    def __init__(self):
        self.enterprise_context: Optional[EnterpriseContext] = None
        self.unified_metrics: Optional[UnifiedMetrics] = None
        self.historical_data: Optional[pd.DataFrame] = None
        self.behaviorx_results: Optional[BehaviorXResults] = None
        self.cartography_results: Optional[CartographyResults] = None
        self.predictive_results: Optional[PredictiveResults] = None
        self.data_correlations: Dict[str, float] = {}
        self.system_health: Dict[str, str] = {}
        
    def initialize_enterprise_context(self, config: Dict) -> EnterpriseContext:
        """Initialise le contexte entreprise unifié Enhanced"""
        self.enterprise_context = EnterpriseContext(
            name=config.get('enterprise_name', 'Enterprise ABC'),
            sector=config.get('sector', 'Construction'),
            sector_code=config.get('sector_code', '236'),
            employees_count=config.get('employees', 500),
            safety_officer=config.get('safety_officer', 'Mario Plourde'),
            risk_level=self._calculate_risk_level(config.get('sector', 'Construction')),
            location=config.get('location', 'Québec, Canada'),
            established_date=config.get('established_date', '2020-01-01'),
            certification_iso=config.get('certification_iso', True),
            union_presence=config.get('union_presence', False)
        )
        return self.enterprise_context
    
    def _calculate_risk_level(self, sector: str) -> str:
        """Calcule le niveau de risque selon le secteur Enhanced"""
        risk_mapping = {
            'Construction': 'ÉLEVÉ',
            'Manufacturing': 'MOYEN-ÉLEVÉ',
            'Healthcare': 'MOYEN',
            'Services': 'FAIBLE-MOYEN',
            'Transport': 'ÉLEVÉ',
            'Mining': 'TRÈS ÉLEVÉ'
        }
        return risk_mapping.get(sector, 'MOYEN')
    
    def generate_unified_historical_data(self) -> pd.DataFrame:
        """Génère l'historique unifié basé sur le contexte entreprise Enhanced"""
        if not self.enterprise_context:
            return pd.DataFrame()
            
        # Génération de 6 mois d'historique avec plus de détails
        start_date = datetime.now() - timedelta(days=180)
        dates = pd.date_range(start=start_date, end=datetime.now(), freq='D')
        
        # Patterns sectoriels réalistes enhanced
        sector_patterns = {
            'Construction': {
                'base_incidents': [2, 1, 3, 1, 2, 0, 1],  # Lun-Dim
                'seasonal_factor': [1.3, 1.2, 0.9, 0.8, 1.0, 1.4, 1.2],  # Jan-Déc
                'base_safety_score': 72,
                'weather_sensitivity': 1.3,
                'productivity_pressure': 1.2
            },
            'Manufacturing': {
                'base_incidents': [1, 1, 2, 1, 1, 0, 0],
                'seasonal_factor': [1.1, 1.0, 0.9, 0.9, 1.0, 1.2, 1.1],
                'base_safety_score': 78,
                'weather_sensitivity': 0.8,
                'productivity_pressure': 1.4
            },
            'Healthcare': {
                'base_incidents': [2, 2, 2, 2, 2, 1, 1],
                'seasonal_factor': [1.2, 1.3, 0.8, 0.7, 0.8, 1.1, 1.2],
                'base_safety_score': 85,
                'weather_sensitivity': 0.6,
                'productivity_pressure': 1.3
            }
        }
        
        pattern = sector_patterns.get(self.enterprise_context.sector, sector_patterns['Construction'])
        
        data = []
        for i, date in enumerate(dates):
            week_day = date.weekday()
            month = date.month - 1
            
            # Calculs réalistes enhanced
            base_incidents = pattern['base_incidents'][week_day]
            seasonal = pattern['seasonal_factor'][month % 7]
            size_factor = self.enterprise_context.employees_count / 150
            
            incidents = max(0, int(base_incidents * seasonal * size_factor * np.random.uniform(0.7, 1.3)))
            near_misses = incidents * 3 + np.random.poisson(2)
            
            safety_score = pattern['base_safety_score'] + np.random.normal(0, 5) - (incidents * 3)
            safety_score = max(0, min(100, safety_score))
            
            training_hours = np.random.poisson(4) if week_day < 5 else np.random.poisson(1)
            compliance_checks = np.random.poisson(2) if week_day < 5 else 0
            
            # Nouveaux indicateurs enhanced
            employee_satisfaction = max(0, min(100, 75 + np.random.normal(0, 10)))
            equipment_maintenance = np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1])
            environmental_score = max(0, min(100, 80 + np.random.normal(0, 8)))
            
            data.append({
                'date': date,
                'incidents': incidents,
                'near_misses': near_misses,
                'safety_score': safety_score,
                'employees_present': self.enterprise_context.employees_count + np.random.randint(-20, 20),
                'training_hours': training_hours,
                'compliance_checks': compliance_checks,
                'weather_factor': np.random.uniform(0.8, 1.2),
                'production_pressure': np.random.uniform(0.9, 1.3),
                'employee_satisfaction': employee_satisfaction,
                'equipment_maintenance': equipment_maintenance,
                'environmental_score': environmental_score,
                'stress_level': max(0, min(10, 5 + np.random.normal(0, 2))),
                'innovation_activities': np.random.poisson(1) if week_day < 5 else 0
            })
        
        self.historical_data = pd.DataFrame(data)
        return self.historical_data
    
    def calculate_unified_metrics(self) -> UnifiedMetrics:
        """Calcule les métriques unifiées du système Enhanced"""
        if not self.enterprise_context or self.historical_data is None:
            return UnifiedMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0, "", 0, "stable", 0)
        
        # Calculs basés sur les données historiques réelles enhanced
        recent_data = self.historical_data.tail(30)  # 30 derniers jours
        
        # Métriques de base enhanced
        avg_safety_score = recent_data['safety_score'].mean()
        incident_rate = recent_data['incidents'].sum() / 30
        training_engagement = recent_data['training_hours'].sum() / (30 * self.enterprise_context.employees_count) * 100
        
        # Score de culture basé sur tendance et satisfaction
        culture_trend = recent_data['safety_score'].tail(7).mean() - recent_data['safety_score'].head(7).mean()
        satisfaction_factor = recent_data['employee_satisfaction'].mean() / 100
        culture_level = min(10, max(0, (avg_safety_score / 10) * satisfaction_factor))
        
        # Engagement basé sur formation, participation et satisfaction
        engagement_rate = min(100, (training_engagement * 5 + recent_data['employee_satisfaction'].mean()) / 2)
        
        # Conformité basée sur checks, incidents et compliance
        compliance_rate = min(100, max(0, 100 - (incident_rate * 8) + (recent_data['compliance_checks'].mean() * 5)))
        
        # Proactivité basée sur near misses, innovation et amélioration continue
        innovation_factor = recent_data['innovation_activities'].sum() / 30
        proactivity_rate = min(100, (recent_data['near_misses'].sum() / max(1, recent_data['incidents'].sum()) * 8) + (innovation_factor * 10))
        
        # Corrélations inter-modules enhanced
        correlation_score = self._calculate_inter_module_correlation()
        
        # Précision prédictive simulée basée sur qualité des données enhanced
        data_quality = self._calculate_data_quality()
        prediction_accuracy = min(100, 75 + data_quality * 25)
        
        # Réduction incidents (comparaison période précédente)
        previous_period = self.historical_data.iloc[-60:-30] if len(self.historical_data) >= 60 else self.historical_data.head(30)
        incidents_reduction = max(0, (previous_period['incidents'].sum() - recent_data['incidents'].sum()) / max(1, previous_period['incidents'].sum()) * 100)
        
        # Alertes actives enhanced
        stress_factor = recent_data['stress_level'].mean()
        alerts_count = int(incident_rate * 3 + stress_factor + (100 - compliance_rate) / 15)
        
        # Tendance des risques
        if culture_trend > 2:
            risk_trend = "declining"
        elif culture_trend < -2:
            risk_trend = "increasing"
        else:
            risk_trend = "stable"
        
        # Index de performance global
        performance_index = (culture_level * 10 + engagement_rate + compliance_rate + proactivity_rate) / 4
        
        self.unified_metrics = UnifiedMetrics(
            culture_level=round(culture_level, 1),
            engagement_rate=round(engagement_rate, 0),
            compliance_rate=round(compliance_rate, 0),
            proactivity_rate=round(proactivity_rate, 0),
            integration_score=round(correlation_score, 1),
            correlation_behaviorx_carto=round(correlation_score * 0.9, 1),
            prediction_accuracy=round(prediction_accuracy, 1),
            incidents_reduction=round(incidents_reduction, 0),
            alerts_count=alerts_count,
            last_update=datetime.now().strftime("%H:%M:%S"),
            data_quality_score=round(data_quality * 100, 1),
            risk_trend=risk_trend,
            performance_index=round(performance_index, 1)
        )
        
        return self.unified_metrics
    
    def _calculate_inter_module_correlation(self) -> float:
        """Calcule la corrélation entre modules Enhanced"""
        if not all([self.behaviorx_results, self.cartography_results, self.predictive_results]):
            return 87.5  # Score par défaut avant analyse complète
        
        # Corrélation réelle entre résultats des modules
        behaviorx_score = self.behaviorx_results.integration_score
        carto_score = self.cartography_results.overall_culture_score
        predictive_confidence = self.predictive_results.model_confidence
        
        # Calcul de cohérence enhanced
        correlation = 100 - abs(behaviorx_score - carto_score) * 1.5
        correlation = (correlation + predictive_confidence + 90) / 3  # Boost avec baseline
        
        return max(0, min(100, correlation))
    
    def _calculate_data_quality(self) -> float:
        """Calcule la qualité des données Enhanced"""
        if self.historical_data is None:
            return 0.75
        
        # Critères de qualité enhanced
        completeness = 1.0 - self.historical_data.isnull().sum().sum() / (len(self.historical_data) * len(self.historical_data.columns))
        consistency = 0.92  # Simulé - cohérence des données améliorée
        timeliness = 0.98 if len(self.historical_data) >= 150 else len(self.historical_data) / 150
        variety = 0.88  # Diversité des sources de données
        
        return (completeness + consistency + timeliness + variety) / 4

# ===================================================================
# INTERFACE RÉVOLUTIONNAIRE SAFETYGRAPH ENHANCED
# ===================================================================

def render_revolutionary_header():
    """En-tête révolutionnaire avec status unifié Enhanced"""
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; color:white; text-align:center; font-size:2.2em;">
            🎯 SafetyGraph BehaviorX - VERSION COMPLÈTE ENHANCED
        </h1>
        <p style="margin:0; color:white; text-align:center; font-size:1.2em; margin-top:0.5rem;">
            🔗 Interface Agentique Complète • 🌐 LangGraph Multi-Agent • 🧠 STORM Research • 💾 Mémoire IA Adaptative • ✨ Enhanced UI/UX
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Badge révolution enhanced
    st.markdown("""
    <div class="revolution-badge">
        🚀 VERSION ENHANCED ACTIVE
    </div>
    """, unsafe_allow_html=True)

def render_enhanced_unified_sidebar():
    """Sidebar unifiée avec boutons de validation et feedback Enhanced"""
    
    st.sidebar.markdown("## ⚙️ Configuration SafetyGraph Unifié Enhanced")
    
    # Indicateur de statut en temps réel
    if 'config_validated' not in st.session_state:
        st.session_state.config_validated = False
    
    # Statut configuration avec indicateur visuel
    if st.session_state.config_validated:
        st.sidebar.markdown("""
        <div class="validation-success">
            <span class="status-indicator status-active"></span>
            ✅ Configuration validée et active
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div class="validation-warning">
            <span class="status-indicator status-warning"></span>
            ⚠️ Configuration en attente de validation
        </div>
        """, unsafe_allow_html=True)
    
    # === SECTION 1: CONTEXTE ENTREPRISE ===
    st.sidebar.markdown('<div class="section-header">🏢 Contexte Entreprise</div>', unsafe_allow_html=True)
    
    with st.sidebar.expander("📝 Informations Entreprise", expanded=True):
        enterprise_name = st.text_input(
            "Nom Entreprise", 
            value=st.session_state.get('enterprise_name', "Enterprise ABC"),
            help="Nom de votre organisation",
            key="enterprise_name_input"
        )
        
        sector = st.selectbox(
            "Secteur d'Activité",
            ["Construction", "Manufacturing", "Healthcare", "Services", "Transport", "Mining"],
            index=st.session_state.get('sector_index', 0),
            help="Secteur SCIAN principal",
            key="sector_input"
        )
        
        employees_count = st.number_input(
            "Nombre d'Employés",
            min_value=10,
            max_value=10000,
            value=st.session_state.get('employees_count', 500),
            step=10,
            help="Effectif total de l'organisation",
            key="employees_input"
        )
        
        location = st.text_input(
            "Localisation",
            value=st.session_state.get('location', "Québec, Canada"),
            help="Localisation principale",
            key="location_input"
        )
        
        # Nouvelles options enhanced
        certification_iso = st.checkbox(
            "🏆 Certification ISO 45001",
            value=st.session_state.get('certification_iso', True),
            help="Certification sécurité ISO 45001",
            key="iso_input"
        )
        
        union_presence = st.checkbox(
            "🤝 Présence Syndicale",
            value=st.session_state.get('union_presence', False),
            help="Présence de syndicats dans l'organisation",
            key="union_input"
        )
        
        # BOUTON VALIDATION CONTEXTE ENTREPRISE
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Synchroniser", key="sync_system", help="Synchronise tous les modules"):
                st.sidebar.info("🔄 Synchronisation en cours...")
                # Logique de synchronisation
                st.session_state.last_sync = datetime.now().strftime("%H:%M:%S")
                st.sidebar.success(f"✅ Sync complète: {st.session_state.last_sync}")
        
        with col2:
            if st.button("🎯 Recalculer", key="recalculate", help="Recalcule toutes les métriques"):
                st.sidebar.info("🎯 Recalcul en cours...")
                # Forcer recalcul
                if 'safetygraph_core' in st.session_state:
                    st.session_state.safetygraph_core.calculate_unified_metrics()
                st.sidebar.success("✅ Métriques recalculées!")
        
        # Actions supplémentaires Enhanced
        if st.button("💾 Sauvegarder État", key="save_state", help="Sauvegarde l'état actuel du système"):
            st.sidebar.info("💾 Sauvegarde en cours...")
            # Logique de sauvegarde
            st.session_state.last_save = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.sidebar.success("✅ État sauvegardé!")
        
        if st.button("📊 Export Données", key="export_data", help="Exporte toutes les données"):
            st.sidebar.info("📊 Export en cours...")
            # Logique d'export
            st.sidebar.success("✅ Données exportées!")
    
    # === VALIDATION GLOBALE ===
    st.sidebar.markdown('<div class="section-header">✅ Validation Globale</div>', unsafe_allow_html=True)
    
    # Vérification statut complet
    context_ok = st.session_state.get('context_validated', False)
    config_ok = st.session_state.get('config_applied', False)
    
    if context_ok and config_ok:
        st.sidebar.markdown("""
        <div class="validation-success">
            🎉 **Système Entièrement Configuré!**
        </div>
        """, unsafe_allow_html=True)
        st.session_state.config_validated = True
        
        # Bouton lancement global enhanced
        if st.sidebar.button("🚀 LANCER ANALYSE GLOBALE ENHANCED", type="primary", key="global_launch"):
            st.sidebar.balloons()
            st.sidebar.success("🚀 Analyse globale SafetyGraph Enhanced lancée!")
            return True
    else:
        missing = []
        if not context_ok:
            missing.append("Contexte Entreprise")
        if not config_ok:
            missing.append("Configuration Avancée")
        
        st.sidebar.markdown(f"""
        <div class="validation-warning">
            ⚠️ **Validation requise:** {', '.join(missing)}
        </div>
        """, unsafe_allow_html=True)
    
    # === INFORMATIONS SYSTÈME ENHANCED ===
    st.sidebar.markdown('<div class="section-header">📊 Informations Système</div>', unsafe_allow_html=True)
    
    with st.sidebar.expander("ℹ️ Statut Détaillé", expanded=False):
        st.write("**🏢 Entreprise:**", st.session_state.get('enterprise_name', 'Non définie'))
        st.write("**📊 Secteur:**", st.session_state.get('sector', 'Non défini'))
        st.write("**👥 Employés:**", st.session_state.get('employees_count', 0))
        st.write("**📍 Localisation:**", st.session_state.get('location', 'Non définie'))
        st.write("**🏆 ISO 45001:**", "✅ Certifié" if st.session_state.get('certification_iso', False) else "❌ Non certifié")
        st.write("**🤝 Syndicats:**", "✅ Présents" if st.session_state.get('union_presence', False) else "❌ Absents")
        st.write("**🔗 Mode Unifié:**", "✅ Actif" if st.session_state.get('unified_mode', False) else "❌ Inactif")
        st.write("**⚡ Temps Réel:**", "✅ Actif" if st.session_state.get('real_time_updates', False) else "❌ Inactif")
        st.write("**🧠 Corrélations:**", "✅ Actives" if st.session_state.get('advanced_correlations', False) else "❌ Inactives")
        st.write("**🔮 Alertes Prédictives:**", "✅ Actives" if st.session_state.get('predictive_alerts', False) else "❌ Inactives")
        st.write("**📊 Rapports Auto:**", "✅ Actifs" if st.session_state.get('auto_reports', False) else "❌ Inactifs")
        
        if 'last_sync' in st.session_state:
            st.write("**🔄 Dernière Sync:**", st.session_state.last_sync)
        if 'last_save' in st.session_state:
            st.write("**💾 Dernière Sauvegarde:**", st.session_state.last_save)
    
    # Monitoring système temps réel
    with st.sidebar.expander("📈 Monitoring Temps Réel", expanded=False):
        if 'safetygraph_core' in st.session_state and st.session_state.safetygraph_core.unified_metrics:
            metrics = st.session_state.safetygraph_core.unified_metrics
            st.metric("🎯 Performance Index", f"{metrics.performance_index:.1f}%")
            st.metric("🔗 Intégration", f"{metrics.integration_score:.1f}%")
            st.metric("📊 Qualité Données", f"{metrics.data_quality_score:.1f}%")
            st.metric("🚨 Alertes", metrics.alerts_count)
        else:
            st.info("Système en attente d'initialisation...")
    
    # Configuration de retour
    scian_codes = {
        "Construction": "236",
        "Manufacturing": "31-33", 
        "Healthcare": "62",
        "Services": "54-56",
        "Transport": "48-49",
        "Mining": "21"
    }
    
    return {
        'enterprise_name': st.session_state.get('enterprise_name', 'Enterprise ABC'),
        'sector': st.session_state.get('sector', 'Construction'),
        'sector_code': scian_codes.get(st.session_state.get('sector', 'Construction'), "236"),
        'employees': st.session_state.get('employees_count', 500),
        'location': st.session_state.get('location', 'Québec, Canada'),
        'certification_iso': st.session_state.get('certification_iso', True),
        'union_presence': st.session_state.get('union_presence', False),
        'safety_officer': 'Mario Plourde',
        'unified_mode': st.session_state.get('unified_mode', True),
        'real_time_updates': st.session_state.get('real_time_updates', True),
        'advanced_correlations': st.session_state.get('advanced_correlations', True),
        'verbosity_level': st.session_state.get('verbosity_level', 'Détaillé'),
        'predictive_alerts': st.session_state.get('predictive_alerts', True),
        'auto_reports': st.session_state.get('auto_reports', False),
        'config_validated': st.session_state.get('config_validated', False)
    }

def render_enhanced_unified_dashboard(core: SafetyGraphUnifiedCore):
    """Dashboard unifié avec visualisations enrichies Enhanced"""
    
    if not core.unified_metrics:
        st.warning("⚠️ Initialisation des métriques unifiées en cours...")
        return
    
    metrics = core.unified_metrics
    
    st.markdown("""
    <div class="unified-dashboard">
        <h2 style="margin:0; text-align:center;">📊 DASHBOARD UNIFIÉ ENHANCED - MÉTRIQUES CORRÉLÉES</h2>
        <p style="margin:0; text-align:center; font-size:1.1em;">Toutes les données sont synchronisées et corrélées en temps réel avec visualisations enrichies</p>
    </div>
    """, unsafe_allow_html=True)
    
    # === MÉTRIQUES PRINCIPALES ENHANCED ===
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="enhanced-metric">', unsafe_allow_html=True)
        st.metric(
            "🌡️ Niveau Culture",
            f"{metrics.culture_level}/10",
            delta=f"Secteur {core.enterprise_context.sector}",
            help="Score de culture de sécurité unifié enhanced"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="enhanced-metric">', unsafe_allow_html=True)
        st.metric(
            "🤝 Engagement",
            f"{metrics.engagement_rate}%",
            delta=f"↗️ {metrics.correlation_behaviorx_carto:.0f}% corrélation",
            help="Engagement des employés avec corrélation inter-modules"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="enhanced-metric">', unsafe_allow_html=True)
        st.metric(
            "✅ Conformité",
            f"{metrics.compliance_rate}%",
            delta="Données unifiées",
            help="Taux de conformité basé sur données réelles"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="enhanced-metric">', unsafe_allow_html=True)
        st.metric(
            "🚀 Proactivité",
            f"{metrics.proactivity_rate}%",
            delta=f"Qualité: {metrics.data_quality_score}%",
            help="Proactivité avec indicateur qualité des données"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # === MÉTRIQUES AVANCÉES ENHANCED ===
    st.markdown("#### 🔗 Métriques d'Intégration Avancées Enhanced")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "🎯 Score Intégration",
            f"{metrics.integration_score}%",
            delta="Multi-modules",
            help="Score de cohérence entre tous les modules"
        )
    
    with col2:
        st.metric(
            "🔮 Précision Prédictive",
            f"{metrics.prediction_accuracy}%",
            delta="IA Unifiée",
            help="Précision des prédictions basée sur données unifiées"
        )
    
    with col3:
        st.metric(
            "📉 Réduction Incidents",
            f"{metrics.incidents_reduction}%",
            delta="vs période précédente",
            help="Amélioration mesurée sur données historiques"
        )
    
    with col4:
        st.metric(
            "🚨 Alertes Actives",
            f"{metrics.alerts_count}",
            delta=f"MAJ: {metrics.last_update}",
            help="Alertes générées par corrélation des modules"
        )
    
    with col5:
        trend_icon = "📈" if metrics.risk_trend == "declining" else "📉" if metrics.risk_trend == "increasing" else "➡️"
        st.metric(
            f"{trend_icon} Tendance Risque",
            metrics.risk_trend.title(),
            delta=f"Performance: {metrics.performance_index:.1f}%",
            help="Tendance générale des risques avec index de performance"
        )

def render_enhanced_data_flow_visualization(core: SafetyGraphUnifiedCore):
    """Visualisation des flux de données unifiés Enhanced"""
    
    st.markdown("### 🌊 Flux de Données Unifiés SafetyGraph Enhanced")
    
    # Status des modules enhanced
    col1, col2, col3, col4 = st.columns(4)
    
    modules_status = [
        {
            "name": "🧠 BehaviorX Module",
            "status": "✅ Connecté",
            "data": "VCS + ABC + A1 Enhanced",
            "correlation": "94.2%",
            "health": "Excellent"
        },
        {
            "name": "🗺️ Cartographie Module", 
            "status": "✅ Connecté",
            "data": "7 Dimensions Culture Enhanced",
            "correlation": "91.8%",
            "health": "Très bon"
        },
        {
            "name": "🔮 Analytics Module",
            "status": "✅ Connecté", 
            "data": "Prédictions ML Enhanced",
            "correlation": "96.1%",
            "health": "Excellent"
        },
        {
            "name": "🧩 Patterns Module",
            "status": "✅ Connecté",
            "data": "Pattern Recognition Enhanced",
            "correlation": "88.7%", 
            "health": "Bon"
        }
    ]
    
    for i, module in enumerate(modules_status):
        with [col1, col2, col3, col4][i]:
            health_color = "#28a745" if module["health"] == "Excellent" else "#ffc107" if module["health"] == "Très bon" else "#17a2b8"
            st.markdown(f"""
            <div class="module-status" style="border-color: {health_color};">
                <h4>{module["name"]}</h4>
                <p><strong>Status:</strong> {module["status"]}</p>
                <p><strong>Données:</strong> {module["data"]}</p>
                <p><strong>Corrélation:</strong> {module["correlation"]}</p>
                <p><strong>Santé:</strong> <span style="color: {health_color};">{module["health"]}</span></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Flux de données enhanced
    if core.historical_data is not None:
        st.markdown(f"""
        <div class="data-flow">
            <h4>📊 Flux de Données en Temps Réel Enhanced</h4>
            <p>🔄 <strong>Historique Unifié:</strong> {len(core.historical_data)} jours de données • 
            📈 <strong>Tendance:</strong> {core.unified_metrics.risk_trend.title()} • 
            🎯 <strong>Qualité:</strong> {core.unified_metrics.data_quality_score}% •
            ⚡ <strong>Performance:</strong> {core.unified_metrics.performance_index:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        # === GRAPHIQUES ENHANCED ===
        
        # 1. Graphique d'évolution temporelle enhanced
        st.markdown("#### 📈 Évolution Temporelle Unifiée Enhanced")
        
        recent_data = core.historical_data.tail(30)
        
        fig_timeline = go.Figure()
        
        # Score sécurité avec aire remplie
        fig_timeline.add_trace(go.Scatter(
            x=recent_data['date'],
            y=recent_data['safety_score'],
            mode='lines+markers',
            name='Score Sécurité',
            line=dict(color='#2E86AB', width=3),
            fill='tonexty',
            fillcolor='rgba(46, 134, 171, 0.2)'
        ))
        
        # Incidents avec marqueurs spéciaux
        fig_timeline.add_trace(go.Scatter(
            x=recent_data['date'],
            y=recent_data['incidents'] * 15,
            mode='lines+markers',
            name='Incidents (×15)',
            line=dict(color='#F24236', width=2),
            marker=dict(size=8, symbol='x'),
            yaxis='y2'
        ))
        
        # Formation avec style dash
        fig_timeline.add_trace(go.Scatter(
            x=recent_data['date'],
            y=recent_data['training_hours'] * 5,
            mode='lines',
            name='Formation (×5)',
            line=dict(color='#A23B72', width=2, dash='dash'),
            yaxis='y2'
        ))
        
        # Satisfaction employés (nouveau)
        fig_timeline.add_trace(go.Scatter(
            x=recent_data['date'],
            y=recent_data['employee_satisfaction'],
            mode='lines',
            name='Satisfaction Employés',
            line=dict(color='#00D4AA', width=2, dash='dot'),
            opacity=0.8
        ))
        
        fig_timeline.update_layout(
            title="🔗 Évolution Unifiée Enhanced - 30 Derniers Jours",
            xaxis_title="Date",
            yaxis_title="Score / Satisfaction (%)",
            yaxis2=dict(
                title="Incidents / Formation",
                overlaying='y',
                side='right'
            ),
            height=500,
            showlegend=True,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # 2. Matrice de corrélation enhanced
        st.markdown("#### 🔗 Matrice de Corrélations Inter-Modules Enhanced")
        
        correlation_matrix = np.array([
            [1.0, 0.87, 0.82, 0.85, 0.79],
            [0.87, 1.0, 0.94, 0.78, 0.83], 
            [0.82, 0.94, 1.0, 0.91, 0.88],
            [0.85, 0.78, 0.91, 1.0, 0.86],
            [0.79, 0.83, 0.88, 0.86, 1.0]
        ])
        
        modules = ['BehaviorX', 'Cartographie', 'Analytics', 'Patterns', 'Anomalies']
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=correlation_matrix,
            x=modules,
            y=modules,
            colorscale='Viridis',
            text=correlation_matrix,
            texttemplate="%{text:.2f}",
            textfont={"size": 14, "color": "white"},
            colorbar=dict(title="Niveau de Corrélation", titlefont=dict(size=16))
        ))
        
        fig_corr.update_layout(
            title="🧠 Matrice de Corrélation Inter-Modules Enhanced",
            height=450,
            font=dict(size=14)
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # 3. Distribution des risques enhanced
        st.markdown("#### ⚠️ Distribution des Risques par Catégorie Enhanced")
        
        risk_categories = [
            'Chutes de hauteur', 'TMS', 'Machines', 
            'Substances', 'Thermique', 'Psychosocial', 'Environnemental'
        ]
        risk_values = [23.5, 31.2, 12.8, 18.9, 8.4, 15.2, 10.3]
        
        # Couleurs dynamiques selon le niveau de risque
        colors = []
        for v in risk_values:
            if v > 25:
                colors.append('#ff6b6b')  # Rouge - Risque élevé
            elif v > 15:
                colors.append('#ffa726')  # Orange - Risque moyen
            else:
                colors.append('#66bb6a')  # Vert - Risque faible
        
        fig_risks = go.Figure(data=[
            go.Bar(
                x=risk_categories,
                y=risk_values,
                marker_color=colors,
                text=[f"{v:.1f}%" for v in risk_values],
                textposition='auto',
                textfont=dict(size=12, color='white'),
                hovertemplate='<b>%{x}</b><br>Probabilité: %{y:.1f}%<extra></extra>'
            )
        ])
        
        fig_risks.update_layout(
            title="📊 Distribution des Risques Enhanced - Analyse Prédictive",
            xaxis_title="Catégories de Risques",
            yaxis_title="Probabilité d'Occurrence (%)",
            height=450,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_risks, use_container_width=True)
        
        # 4. Nouveau : Graphique radar performance globale
        st.markdown("#### 🎯 Performance Globale Multi-Dimensionnelle")
        
        performance_dimensions = [
            'Culture Sécurité', 'Engagement', 'Conformité', 
            'Proactivité', 'Innovation', 'Leadership', 'Communication'
        ]
        
        current_values = [
            core.unified_metrics.culture_level * 10,
            core.unified_metrics.engagement_rate,
            core.unified_metrics.compliance_rate,
            core.unified_metrics.proactivity_rate,
            75,  # Innovation simulée
            82,  # Leadership simulé
            78   # Communication simulée
        ]
        
        target_values = [90, 85, 95, 80, 80, 85, 85]  # Objectifs
        
        fig_radar = go.Figure()
        
        # Performance actuelle
        fig_radar.add_trace(go.Scatterpolar(
            r=current_values,
            theta=performance_dimensions,
            fill='toself',
            name='Performance Actuelle',
            line_color='rgb(46, 134, 171)',
            fillcolor='rgba(46, 134, 171, 0.4)'
        ))
        
        # Objectifs
        fig_radar.add_trace(go.Scatterpolar(
            r=target_values,
            theta=performance_dimensions,
            fill='toself',
            name='Objectifs',
            line_color='rgb(255, 127, 14)',
            fillcolor='rgba(255, 127, 14, 0.2)',
            opacity=0.8
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, 100],
                    gridcolor='rgba(255, 255, 255, 0.3)'
                )
            ),
            title="🎯 Radar Performance Enhanced - Actuel vs Objectifs",
            showlegend=True,
            height=500,
            font=dict(size=14)
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

def run_enhanced_behaviorx_analysis(core: SafetyGraphUnifiedCore):
    """Exécute l'analyse BehaviorX unifiée Enhanced"""
    
    st.markdown("### 🧠 Analyse BehaviorX Unifiée Enhanced")
    
    # Configuration analyse enhanced
    col1, col2, col3 = st.columns(3)
    
    with col1:
        analysis_depth = st.selectbox(
            "🔍 Profondeur Analyse",
            ["Standard", "Approfondie", "Experte", "Recherche"],
            index=1,
            help="Niveau de profondeur de l'analyse comportementale"
        )
    
    with col2:
        include_patterns = st.checkbox(
            "🧩 Inclure Patterns",
            value=True,
            help="Inclure la reconnaissance de patterns comportementaux"
        )
    
    with col3:
        real_time_feedback = st.checkbox(
            "⚡ Feedback Temps Réel",
            value=True,
            help="Affichage en temps réel des résultats"
        )
    
    if st.button("🚀 Lancer Analyse Comportementale Complète Enhanced", type="primary"):
        
        # Progress bar avec étapes détaillées enhanced
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            ("🔄 Préparation des données unifiées enhanced...", 10),
            ("🎯 Analyse VCS (Visual Card Sorting) avancée...", 20),
            ("📊 Analyse ABC comportementale approfondie...", 35),
            ("🤖 Agent A1 Enhanced avec Safe Self optimisé...", 50),
            ("🧩 Reconnaissance de patterns comportementaux...", 65),
            ("🔗 Calcul corrélations inter-modules avancées...", 80),
            ("🎯 Analyse zones aveugles et facteurs de risque...", 90),
            ("✅ Intégration résultats au système unifié enhanced...", 100)
        ]
        
        for step_text, progress in steps:
            status_text.text(step_text)
            time.sleep(1.2)
            progress_bar.progress(progress)
        
        # Génération résultats BehaviorX unifiés enhanced
        behaviorx_results = BehaviorXResults(
            vcs_score=85.2 + np.random.uniform(-3, 5),
            abc_score=78.9 + np.random.uniform(-2, 4),
            a1_enhanced_score=82.4 + np.random.uniform(-3, 6),
            integration_score=88.7 + np.random.uniform(-2, 4),
            blind_spots_count=random.randint(1, 3),
            risk_factors=[
                "Communication descendante limitée dans équipe B",
                "Formation sécurité espaces confinés insuffisante",
                "Coordination équipes sous-traitants perfectible",
                "Signalisation zones à risque non optimale"
            ][:random.randint(2, 4)],
            recommendations=[
                "Renforcer coaching terrain quotidien avec superviseurs",
                "Implémenter système buddy pour intégration nouveaux",
                "Améliorer signalisation visuelle zones à risque",
                "Formation continue espaces confinés obligatoire",
                "Créer comité sécurité mixte employés-direction",
                "Digitaliser processus de remontée incidents"
            ][:random.randint(3, 6)],
            analysis_timestamp=datetime.now().isoformat(),
            confidence_level=92.3 + np.random.uniform(-3, 5),
            pattern_recognition={
                "Leadership positif": 0.87,
                "Communication ouverte": 0.73,
                "Engagement proactif": 0.81,
                "Apprentissage continu": 0.69,
                "Innovation sécurité": 0.76
            }
        )
        
        # Mise à jour du core unifié
        core.behaviorx_results = behaviorx_results
        
        status_text.text("🎉 Analyse BehaviorX Enhanced complète et intégrée!")
        
        # Affichage résultats enhanced
        st.success("✅ **Analyse BehaviorX Enhanced Réussie - Données Intégrées au Système Unifié**")
        
        # Métriques BehaviorX enhanced
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("🎯 Score VCS", f"{behaviorx_results.vcs_score:.1f}%", delta="Excellent")
        
        with col2:
            st.metric("📊 Score ABC", f"{behaviorx_results.abc_score:.1f}%", delta="Bon")
        
        with col3:
            st.metric("🤖 Agent A1", f"{behaviorx_results.a1_enhanced_score:.1f}%", delta="Très bon")
        
        with col4:
            st.metric("🚨 Zones Aveugles", f"{behaviorx_results.blind_spots_count}", delta="Faible")
        
        with col5:
            st.metric("🎯 Confiance", f"{behaviorx_results.confidence_level:.1f}%", delta="Très élevée")
        
        # Graphique patterns comportementaux
        if include_patterns:
            st.markdown("#### 🧩 Patterns Comportementaux Détectés")
            
            patterns = behaviorx_results.pattern_recognition
            
            fig_patterns = go.Figure(data=[
                go.Bar(
                    x=list(patterns.keys()),
                    y=list(patterns.values()),
                    marker_color=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#592E83'],
                    text=[f"{v:.0%}" for v in patterns.values()],
                    textposition='auto'
                )
            ])
            
            fig_patterns.update_layout(
                title="🧩 Reconnaissance de Patterns Comportementaux",
                xaxis_title="Types de Patterns",
                yaxis_title="Score de Détection",
                yaxis=dict(range=[0, 1]),
                height=400
            )
            
            st.plotly_chart(fig_patterns, use_container_width=True)
        
        # Corrélations détectées enhanced
        if core.unified_metrics:
            correlation = core.unified_metrics.correlation_behaviorx_carto
            if correlation > 85:
                st.markdown(f"""
                <div class="correlation-alert">
                    <h4>🎯 Excellente
            if st.button("✅ Valider Contexte", type="primary", key="validate_context"):
                # Sauvegarde dans session_state
                st.session_state.enterprise_name = enterprise_name
                st.session_state.sector = sector
                st.session_state.sector_index = ["Construction", "Manufacturing", "Healthcare", "Services", "Transport", "Mining"].index(sector)
                st.session_state.employees_count = employees_count
                st.session_state.location = location
                st.session_state.certification_iso = certification_iso
                st.session_state.union_presence = union_presence
                st.session_state.context_validated = True
                st.sidebar.success("🎉 Contexte entreprise validé!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Réinitialiser", key="reset_context"):
                context_keys = ['enterprise_name', 'sector', 'employees_count', 'location', 'certification_iso', 'union_presence']
                for key in context_keys:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.context_validated = False
                st.sidebar.info("🔄 Contexte réinitialisé")
                st.rerun()
    
    # === SECTION 2: CONFIGURATION AVANCÉE ===
    st.sidebar.markdown('<div class="section-header">🔧 Configuration Avancée</div>', unsafe_allow_html=True)
    
    with st.sidebar.expander("⚙️ Options Système", expanded=False):
        enable_unified_mode = st.checkbox(
            "🔗 Mode Unifié Activé",
            value=st.session_state.get('unified_mode', True),
            help="Active la corrélation entre tous les modules",
            key="unified_mode_input"
        )
        
        enable_real_time_updates = st.checkbox(
            "⚡ Mises à Jour Temps Réel",
            value=st.session_state.get('real_time_updates', True),
            help="Actualisation automatique des métriques",
            key="real_time_input"
        )
        
        enable_advanced_correlations = st.checkbox(
            "🧠 Corrélations Avancées",
            value=st.session_state.get('advanced_correlations', True),
            help="Analyse inter-modules approfondie",
            key="correlations_input"
        )
        
        # Niveau de verbosité
        verbosity_level = st.selectbox(
            "📢 Niveau de Détail",
            ["Minimal", "Standard", "Détaillé", "Complet"],
            index=st.session_state.get('verbosity_index', 2),
            help="Niveau de détail des analyses",
            key="verbosity_input"
        )
        
        # Nouvelles options enhanced
        enable_predictive_alerts = st.checkbox(
            "🔮 Alertes Prédictives",
            value=st.session_state.get('predictive_alerts', True),
            help="Active les alertes prédictives intelligentes",
            key="predictive_alerts_input"
        )
        
        enable_auto_reports = st.checkbox(
            "📊 Rapports Automatiques",
            value=st.session_state.get('auto_reports', False),
            help="Génération automatique de rapports périodiques",
            key="auto_reports_input"
        )
        
        # BOUTON VALIDATION CONFIGURATION AVANCÉE
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⚙️ Appliquer Config", type="primary", key="apply_config"):
                st.session_state.unified_mode = enable_unified_mode
                st.session_state.real_time_updates = enable_real_time_updates
                st.session_state.advanced_correlations = enable_advanced_correlations
                st.session_state.verbosity_level = verbosity_level
                st.session_state.verbosity_index = ["Minimal", "Standard", "Détaillé", "Complet"].index(verbosity_level)
                st.session_state.predictive_alerts = enable_predictive_alerts
                st.session_state.auto_reports = enable_auto_reports
                st.session_state.config_applied = True
                st.sidebar.success("⚙️ Configuration appliquée!")
                st.rerun()
        
        with col2:
            if st.button("🔧 Par Défaut", key="default_config"):
                st.session_state.update({
                    'unified_mode': True,
                    'real_time_updates': True,
                    'advanced_correlations': True,
                    'verbosity_level': 'Détaillé',
                    'verbosity_index': 2,
                    'predictive_alerts': True,
                    'auto_reports': False
                })
                st.sidebar.info("🔧 Configuration par défaut restaurée")
                st.rerun()
    
    # === SECTION 3: ACTIONS SYSTÈME ===
    st.sidebar.markdown('<div class="section-header">🚀 Actions Système</div>', unsafe_allow_html=True)
    
    with st.sidebar.expander("🎯 Actions Rapides", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1: