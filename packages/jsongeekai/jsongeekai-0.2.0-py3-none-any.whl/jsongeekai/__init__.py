"""
JsonGeekAI - A high-performance JSON parser with AI-driven optimizations
"""

__version__ = "0.2.0"

from .parser import JsonGeekAI
from .exceptions import (
    JsonGeekAIError,
    SIMDNotSupportedError,
    WASMLoadError,
    JSONParseError,
    MemoryLimitError,
    DepthLimitError,
    FormatError,
    EncodingError,
    CompressionError
)

__all__ = [
    'JsonGeekAI',
    'JsonGeekAIError',
    'SIMDNotSupportedError',
    'WASMLoadError',
    'JSONParseError',
    'MemoryLimitError',
    'DepthLimitError',
    'FormatError',
    'EncodingError',
    'CompressionError'
]
