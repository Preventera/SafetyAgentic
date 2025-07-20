"""Factory pour créer les instances LLM (Claude ou OpenAI)"""

from enum import Enum
from typing import Optional
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain.schema.language_model import BaseLanguageModel
from ..core.config import config

class LLMType(Enum):
    """Types de LLM supportés"""
    CLAUDE = "claude"
    OPENAI = "openai"
    AUTO = "auto"

def get_llm(
    llm_type: LLMType = LLMType.AUTO,
    temperature: float = 0.1,
    max_tokens: Optional[int] = None
) -> BaseLanguageModel:
    """
    Factory pour créer une instance LLM
    
    Args:
        llm_type: Type de LLM souhaité
        temperature: Température pour la génération
        max_tokens: Nombre max de tokens
        
    Returns:
        Instance LLM configurée
        
    Raises:
        ValueError: Si aucune API n'est configurée
    """
    
    # Détermination automatique du LLM
    if llm_type == LLMType.AUTO:
        if config.has_claude_api:
            llm_type = LLMType.CLAUDE
        elif config.has_openai_api:
            llm_type = LLMType.OPENAI
        else:
            raise ValueError("Aucune API LLM configurée (Claude ou OpenAI)")
    
    # Création de l'instance Claude
    if llm_type == LLMType.CLAUDE:
        if not config.has_claude_api:
            raise ValueError("API Claude non configurée")
        
        return ChatAnthropic(
            model=config.claude_model,
            anthropic_api_key=config.anthropic_api_key,
            temperature=temperature,
            max_tokens=max_tokens or 4000
        )
    
    # Création de l'instance OpenAI
    elif llm_type == LLMType.OPENAI:
        if not config.has_openai_api:
            raise ValueError("API OpenAI non configurée")
        
        return ChatOpenAI(
            model=config.openai_model,
            api_key=config.openai_api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    else:
        raise ValueError(f"Type LLM non supporté: {llm_type}")

def get_preferred_llm(temperature: float = 0.1) -> BaseLanguageModel:
    """Obtient le LLM préféré selon la configuration"""
    return get_llm(LLMType.AUTO, temperature)