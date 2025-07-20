"""
SafeGraph - Prototype Principal (Version Claude API)
Démonstration du système multi-agent d'analyse de culture sécurité
"""

import asyncio
from datetime import datetime
from src.core.graph import create_safety_graph
from src.core.state import create_initial_state
from src.core.config import config

def display_welcome():
    """Affiche le message de bienvenue avec info API"""
    print("=" * 60)
    print("🔒 SAFEGRAPH - Prototype Culture Sécurité")
    print("=" * 60)
    print("Système multi-agent d'analyse de culture sécurité")
    print("Basé sur LangGraph et spécialisé par secteur SCIAN")
    print("=" * 60)
    
    # Afficher le LLM configuré
    llm_status = f"🤖 LLM configuré : {config.preferred_llm.upper()}"
    if config.preferred_llm == "claude":
        llm_status += f" ({config.claude_model})"
    elif config.preferred_llm == "openai":
        llm_status += f" ({config.openai_model})"
    else:
        llm_status += " (Mode simulation - aucune API)"
    
    print(llm_status)
    print("=" * 60)
    print()

def display_results(final_state):
    """Affiche les résultats de l'analyse"""
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS DE L'ANALYSE")
    print("=" * 60)
    
    # Trace des agents
    print("\n🔄 Agents exécutés :")
    for agent in final_state.get("agent_trace", []):
        print(f"  ✅ {agent}")
    
    # LLM utilisé
    context = final_state.get("context", {})
    llm_used = context.get("llm_used", config.preferred_llm)
    print(f"\n🤖 LLM utilisé : {llm_used.upper()}")
    
    # Intent détecté
    intent = final_state.get("intent")
    print(f"\n🎯 Intention détectée : {intent.value if intent else 'Non déterminée'}")
    
    # Secteur SCIAN
    sector = final_state.get("scian_sector")
    sector_name = config.scian_sectors.get(sector, "Non spécifié") if sector else "Non spécifié"
    print(f"🏭 Secteur SCIAN : {sector} - {sector_name}")
    
    # Confiance de la classification
    confidence = context.get("confidence_score", 0)
    print(f"📈 Confiance classification : {confidence:.1%}")
    
    # Données collectées
    collection_results = final_state.get("collection_results", [])
    if collection_results:
        latest = collection_results[-1]
        print(f"\n📋 Données collectées :")
        print(f"  • Questionnaire : {latest.get('questionnaire_id', 'N/A')}")
        print(f"  • Taux de complétion : {latest.get('completion_rate', 0):.1%}")
        
        preliminary_scores = latest.get('preliminary_scores', {})
        if preliminary_scores and 'global' in preliminary_scores:
            global_score = preliminary_scores['global'].get('raw_score', 'N/A')
            print(f"  • Score global préliminaire : {global_score}")
    
    # Analyse des risques
    analysis = final_state.get("analysis", {})
    if analysis:
        risk_classification = analysis.get("risk_classification", "Non déterminé")
        print(f"\n⚠️  Classification de risque : {risk_classification}")
        
        # Qualité des données
        data_quality = analysis.get("data_quality", 0)
        print(f"📊 Qualité des données : {data_quality:.1%}")
        
        key_findings = analysis.get("key_findings", [])
        if key_findings:
            print("\n🔍 Conclusions clés :")
            for finding in key_findings:
                print(f"  • {finding}")
    
    # Recommandations
    recommendations = final_state.get("recommendations", [])
    if recommendations:
        print(f"\n💡 Recommandations générées : {len(recommendations)}")
        
        # Compter par priorité
        priority_counts = {}
        for rec in recommendations:
            priority = rec.get("priority", "Medium")
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        for priority, count in priority_counts.items():
            print(f"  • {priority} : {count}")
        
        # Afficher les 3 premières recommandations
        print("\n🎯 Top 3 recommandations :")
        for i, rec in enumerate(recommendations[:3]):
            priority = rec.get("priority", "Medium")
            title = rec.get("title", "Recommandation")
            source = rec.get("source", "unknown")
            print(f"  {i+1}. [{priority}] {title} ({source})")
    
    # Plan d'action
    action_plan = final_state.get("action_plan", {})
    if action_plan:
        summary = action_plan.get("summary", {})
        total_effort = summary.get("estimated_total_effort", "N/A")
        print(f"\n📋 Plan d'action : {total_effort} effort estimé")
        
        # Timeline
        timeline = action_plan.get("timeline", {})
        critical_actions = timeline.get("critical_actions", [])
        if critical_actions:
            print(f"🚨 Actions critiques : {len(critical_actions)}")
    
    # Actions prioritaires
    priority_actions = final_state.get("priority_actions", [])
    if priority_actions:
        print(f"\n🚨 Actions prioritaires immédiates :")
        for action in priority_actions:
            print(f"  • {action}")
    
    # Erreurs éventuelles
    errors = final_state.get("errors", [])
    if errors:
        print(f"\n❌ Erreurs détectées :")
        for error in errors:
            print(f"  • {error}")
    
    print("\n" + "=" * 60)

async def run_demo():
    """Exécute une démonstration du prototype"""
    
    display_welcome()
    
    # Exemples de requêtes pour la démo
    demo_queries = [
        {
            "query": "Je travaille en construction et j'aimerais évaluer ma culture sécurité sur le chantier",
            "description": "Évaluation Construction"
        },
        {
            "query": "Analyse des risques pour un conducteur de transport longue distance avec fatigue", 
            "description": "Analyse Transport"
        },
        {
            "query": "Recommandations pour améliorer la sécurité dans notre service de soins d'urgence",
            "description": "Recommandations Santé"
        },
        {
            "query": "Suivi des progrès sécurité après formation du personnel de maintenance",
            "description": "Monitoring Maintenance"
        }
    ]
    
    print("Requêtes de démonstration disponibles :")
    for i, demo in enumerate(demo_queries):
        print(f"  {i+1}. {demo['description']}")
    
    # Sélection interactive ou automatique
    try:
        choice = input("\nChoisissez une requête (1-4) ou Entrée pour toutes : ")
        if choice.isdigit() and 1 <= int(choice) <= 4:
            selected_demos = [demo_queries[int(choice)-1]]
        else:
            selected_demos = demo_queries
    except:
        selected_demos = demo_queries
    
    # Créer le graphe SafeGraph
    print("\n🔧 Initialisation du graphe SafeGraph...")
    try:
        graph = create_safety_graph()
        print("✅ Graphe créé avec succès")
    except Exception as e:
        print(f"❌ Erreur création graphe : {e}")
        return
    
    # Exécuter chaque démo
    for demo in selected_demos:
        print(f"\n{'='*60}")
        print(f"🧪 DÉMONSTRATION : {demo['description']}")
        print(f"Query : {demo['query']}")
        print(f"{'='*60}")
        
        try:
            # Créer état initial
            initial_state = create_initial_state(demo['query'])
            
            # Exécuter le graphe
            print("\n⚙️  Exécution du workflow SafeGraph...")
            final_state = await graph.ainvoke(initial_state)
            
            # Afficher les résultats
            display_results(final_state)
            
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution : {e}")
            print(f"Détails : {type(e).__name__}")
            import traceback
            if config.debug_mode:
                traceback.print_exc()
        
        # Pause entre les démos
        if len(selected_demos) > 1:
            input("\nAppuyez sur Entrée pour continuer...")

def run_sync_demo():
    """Version synchrone pour compatibilité"""
    
    display_welcome()
    
    print("🔧 Mode démo synchrone (simulation)...")
    
    # Test de configuration API
    if config.has_claude_api:
        print("✅ API Claude configurée")
    elif config.has_openai_api:
        print("✅ API OpenAI configurée")
    else:
        print("⚠️  Aucune API configurée - Mode simulation")
    
    # Simulation simple sans LangGraph complet
    test_queries = [
        "Je travaille en construction et j'aimerais évaluer ma culture sécurité",
        "Analyse des risques pour conducteur de transport",
        "Recommandations pour améliorer la sécurité des soins"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i} avec requête : {query}")
        
        # Créer état de test
        test_state = create_initial_state(query)
        
        print(f"  ✅ État initial créé")
        print(f"    • Session ID : {test_state['session_id']}")
        print(f"    • LLM préféré : {config.preferred_llm}")
    
    print(f"\n🏗️  Structure du projet SafeGraph initialisée avec succès !")
    print(f"  • {len(config.scian_sectors)} secteurs SCIAN supportés")
    print(f"  • Agents multi-spécialisés opérationnels")
    print(f"  • Architecture LangGraph prête")
    print(f"  • Support Claude + OpenAI")
    
    print(f"\n🚀 Prototype SafeGraph prêt pour développement complet !")

if __name__ == "__main__":
    print("Lancement du prototype SafeGraph...")
    
    # Vérifier configuration
    if config.preferred_llm == "none":
        print("⚠️  Aucune API LLM configurée - Mode simulation activé")
        run_sync_demo()
    else:
        print(f"🔑 API {config.preferred_llm.upper()} détectée - Mode complet")
        try:
            asyncio.run(run_demo())
        except Exception as e:
            print(f"Erreur mode async : {e}")
            print("Basculement en mode simulation...")
            run_sync_demo()