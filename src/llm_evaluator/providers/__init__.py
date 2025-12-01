"""
LLM Provider abstraction layer.

Supports multiple backends: Ollama (local), OpenAI, Anthropic, HuggingFace.
"""

from .base import (
    AuthenticationError,
    GenerationConfig,
    GenerationResult,
    LLMProvider,
    ModelNotFoundError,
    ProviderError,
    ProviderType,
    RateLimitError,
    TimeoutError,
)
from .ollama_provider import OllamaProvider
from .cached_provider import CachedProvider

# Conditional imports for optional providers
_has_openai = False
OpenAIProvider = None  # type: ignore[assignment]
try:
    from .openai_provider import OpenAIProvider as _OpenAIProvider

    OpenAIProvider = _OpenAIProvider  # type: ignore[misc]
    _has_openai = True
except ImportError:
    pass

_has_anthropic = False
AnthropicProvider = None  # type: ignore[assignment]
try:
    from .anthropic_provider import AnthropicProvider as _AnthropicProvider

    AnthropicProvider = _AnthropicProvider  # type: ignore[misc]
    _has_anthropic = True
except ImportError:
    pass

_has_huggingface = False
HuggingFaceProvider = None  # type: ignore[assignment]
try:
    from .huggingface_provider import HuggingFaceProvider as _HuggingFaceProvider

    HuggingFaceProvider = _HuggingFaceProvider  # type: ignore[misc]
    _has_huggingface = True
except ImportError:
    pass

__all__ = [
    # Types
    "ProviderType",
    "GenerationConfig",
    "GenerationResult",
    # Base class
    "LLMProvider",
    # Errors
    "ProviderError",
    "RateLimitError",
    "AuthenticationError",
    "ModelNotFoundError",
    "TimeoutError",
    # Providers
    "OllamaProvider",
    "CachedProvider",
    "OpenAIProvider",
    "AnthropicProvider",
    "HuggingFaceProvider",
]
