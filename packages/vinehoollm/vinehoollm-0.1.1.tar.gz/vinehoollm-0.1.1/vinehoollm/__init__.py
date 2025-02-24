"""
VinehooLLM - A Python package for interacting with OpenAI-compatible LLMs
"""

from .client import VinehooLLM
from .types import CompletionResponse, ChatMessage

__version__ = "0.1.0"
__all__ = ["VinehooLLM", "CompletionResponse", "ChatMessage"] 