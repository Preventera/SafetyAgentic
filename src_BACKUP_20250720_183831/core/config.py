"""Configuration centrale SafeGraph"""

import os
from pathlib import Path
from typing import Dict, Any
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class SafeGraphConfig(BaseModel):
    """Configuration principale SafeGraph"""
    
    # Chemins
    project_root: Path = Path(__file__).parent.parent.parent
    data_path: Path = project_root / "data"
    prompts_path: Path = project_root / "prompts"
    logs_path: Path = project_root / "logs"
    
    # Claude API (remplace OpenAI)
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    claude_model: str = os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229")
    
    # Fallback OpenAI (optionnel)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # LangGraph
    langchain_tracing: bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    langchain_api_key: str = os.getenv("LANGCHAIN_API_KEY", "")
    
    # SafeGraph
    debug_mode: bool = os.getenv("SAFEGRAPH_DEBUG", "false").lower() == "true"
    log_level: str = os.getenv("SAFEGRAPH_LOG_LEVEL", "INFO")
    
    # Agents
    max_agents_concurrent: int = 5
    agent_timeout: int = 30
    
    # SCIAN
    scian_sectors: Dict[str, str] = {
        "236": "Construction",
        "484": "Transport routier", 
        "622": "Santé",
        "811": "Maintenance industrielle",
        "561": "Sécurité privée"
    }
    
    @property
    def has_claude_api(self) -> bool:
        """Vérifie si l'API Claude est configurée"""
        return bool(self.anthropic_api_key)
    
    @property
    def has_openai_api(self) -> bool:
        """Vérifie si l'API OpenAI est configurée"""
        return bool(self.openai_api_key)
    
    @property
    def preferred_llm(self) -> str:
        """Détermine le LLM préféré"""
        if self.has_claude_api:
            return "claude"
        elif self.has_openai_api:
            return "openai"
        else:
            return "none"

# Instance globale
config = SafeGraphConfig()