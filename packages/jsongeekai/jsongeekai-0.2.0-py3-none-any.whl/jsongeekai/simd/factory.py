"""
Factory module for SIMD optimization selection.
"""
import platform
from typing import Optional, Type
from .base import SIMDBase
from .avx2 import AVX2Parser
from .neon import NEONParser
from ..exceptions import SIMDNotSupportedError

def get_simd_parser() -> SIMDBase:
    """Get the appropriate SIMD parser for the current platform.
    
    Returns:
        An instance of the appropriate SIMD parser class
        
    Raises:
        SIMDNotSupportedError: If SIMD is not supported on this platform
    """
    arch = platform.machine().lower()
    
    if arch in ('x86_64', 'amd64'):
        try:
            from cpuinfo import get_cpu_info
            info = get_cpu_info()
            if 'avx2' in info.get('flags', []):
                return AVX2Parser()
        except ImportError:
            pass
    elif arch in ('arm64', 'aarch64'):
        # ARM64 always has NEON
        return NEONParser()
    
    raise SIMDNotSupportedError(
        f"No SIMD support available for architecture: {arch}")
