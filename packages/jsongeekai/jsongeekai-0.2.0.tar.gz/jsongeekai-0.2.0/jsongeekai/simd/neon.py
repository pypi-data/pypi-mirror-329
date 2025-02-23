"""
NEON-specific SIMD optimizations for ARM architecture.
"""
import numpy as np
from typing import Union, List, Tuple
from .base import SIMDBase

try:
    import numba
    from numba import jit, vectorize
    HAVE_NUMBA = True
except ImportError:
    HAVE_NUMBA = False

class NEONParser(SIMDBase):
    """NEON-optimized JSON parser operations."""
    
    def __init__(self):
        super().__init__()
        self._init_neon()
    
    def _init_neon(self):
        """Initialize NEON-specific optimizations."""
        if HAVE_NUMBA:
            # Compile optimized functions
            self._compile_kernels()
    
    @staticmethod
    @jit(nopython=True, parallel=True)
    def _find_whitespace_neon(data: np.ndarray, whitespace_mask: np.ndarray) -> np.ndarray:
        """NEON-optimized whitespace detection."""
        result = np.zeros(len(data), dtype=np.bool_)
        # Process 16 bytes at a time (NEON register size)
        for i in numba.prange(0, len(data), 16):
            chunk = data[i:i+16]
            result[i:i+len(chunk)] = whitespace_mask[chunk]
        return result
    
    @staticmethod
    @jit(nopython=True)
    def _find_structural_neon(data: np.ndarray, char_class: np.ndarray) -> np.ndarray:
        """NEON-optimized structural character detection."""
        result = np.zeros(len(data), dtype=np.bool_)
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            classes = char_class[chunk]
            result[i:i+len(chunk)] = (classes >= 6) & (classes <= 11)
        return result
    
    @staticmethod
    @vectorize(['float32(float32, float32)'], target='parallel')
    def _simd_number_parse(mantissa: float, exponent: float) -> float:
        """NEON-optimized number parsing."""
        return mantissa * (10.0 ** exponent)
    
    def parse_numbers_fast(self, data: Union[bytes, bytearray],
                          positions: List[slice]) -> List[float]:
        """Parse numbers using NEON optimization.
        
        Args:
            data: Input data
            positions: List of number positions
            
        Returns:
            List of parsed numbers
        """
        if not HAVE_NUMBA:
            return [float(data[pos]) for pos in positions]
        
        numbers = []
        for pos in positions:
            num_str = data[pos].decode('ascii')
            if 'e' in num_str.lower():
                # Handle scientific notation
                mantissa_str, exp_str = num_str.lower().split('e')
                mantissa = float(mantissa_str)
                exponent = float(exp_str)
                # Use 32-bit precision for ARM
                numbers.append(float(self._simd_number_parse(
                    np.float32(mantissa), np.float32(exponent))))
            else:
                numbers.append(float(num_str))
        
        return numbers
    
    def find_strings_fast(self, data: Union[bytes, bytearray]) -> List[Tuple[int, int]]:
        """Find string literals using NEON optimization.
        
        Args:
            data: Input data
            
        Returns:
            List of (start, end) positions for strings
        """
        if not HAVE_NUMBA:
            return [(s.start, s.stop) for s in self.find_strings(data)]
        
        arr = np.frombuffer(data, dtype=np.uint8)
        result = []
        
        # Process 16 bytes at a time
        for i in range(0, len(arr), 16):
            chunk = arr[i:i+16]
            
            # Find quotes
            quotes = np.where(self.quote_mask[chunk])[0]
            if len(quotes) % 2 != 0:
                # Handle quote spanning chunk boundary
                continue
            
            # Add string positions
            for start, end in zip(quotes[::2], quotes[1::2]):
                result.append((i + start, i + end + 1))
        
        return result
    
    def validate_utf8_fast(self, data: Union[bytes, bytearray]) -> bool:
        """Validate UTF-8 encoding using NEON optimization.
        
        Args:
            data: Input data
            
        Returns:
            True if valid UTF-8
        """
        if not HAVE_NUMBA:
            try:
                data.decode('utf-8')
                return True
            except UnicodeError:
                return False
        
        @jit(nopython=True, parallel=True)
        def _validate_utf8_neon(arr):
            # Similar to AVX2 version but optimized for NEON
            for i in numba.prange(0, len(arr), 16):
                chunk = arr[i:min(i+16, len(arr))]
                for j in range(len(chunk)):
                    if chunk[j] > 0x7F:  # Non-ASCII
                        idx = i + j
                        if chunk[j] & 0xE0 == 0xC0:  # 2-byte sequence
                            if (idx + 1 >= len(arr) or
                                (arr[idx+1] & 0xC0) != 0x80):
                                return False
                        elif chunk[j] & 0xF0 == 0xE0:  # 3-byte sequence
                            if (idx + 2 >= len(arr) or
                                (arr[idx+1] & 0xC0) != 0x80 or
                                (arr[idx+2] & 0xC0) != 0x80):
                                return False
                        elif chunk[j] & 0xF8 == 0xF0:  # 4-byte sequence
                            if (idx + 3 >= len(arr) or
                                (arr[idx+1] & 0xC0) != 0x80 or
                                (arr[idx+2] & 0xC0) != 0x80 or
                                (arr[idx+3] & 0xC0) != 0x80):
                                return False
                        else:
                            return False
            return True
        
        return _validate_utf8_neon(np.frombuffer(data, dtype=np.uint8))
    
    def _compile_kernels(self):
        """Pre-compile Numba kernels for better performance."""
        if not HAVE_NUMBA:
            return
        
        # Compile with dummy data
        dummy_data = np.zeros(32, dtype=np.uint8)
        dummy_mask = np.zeros(256, dtype=bool)
        dummy_class = np.zeros(256, dtype=np.uint8)
        
        # Warm up the JIT compiler
        self._find_whitespace_neon(dummy_data, dummy_mask)
        self._find_structural_neon(dummy_data, dummy_class)
        self._simd_number_parse(np.float32(1.0), np.float32(1.0))
