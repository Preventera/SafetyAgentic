"""
Safety Agentique 4 - Module de nouvelle génération pour SafetyGraph
Capacités avancées : Multimodal, Temps réel, Claude Opus 4.1
"""

__version__ = "4.0.0"

V4_CONFIG = {
    "version": "4.0.0",  # Ajout de la clé version ici
    "enabled": True,
    "features": {
        "multimodal": True,
        "realtime": True,
        "ar_enabled": True,
        "voice_control": True,
        "claude_opus_4_1": True
    },
    "models": {
        "primary": "claude-opus-4-1-20250805",
        "fallback": "claude-sonnet-4"
    }
}

def initialize_v4_module(app=None, config=None):
    """Initialise le module V4 dans l'application SafetyGraph"""
    config = config or V4_CONFIG
    print(f"✅ Safety Agentique 4 module v{__version__} initialized")
    print(f"   Features enabled: {list(config['features'].keys())}")
    return True

# Export pour faciliter l'import
__all__ = ['V4_CONFIG', '__version__', 'initialize_v4_module']
