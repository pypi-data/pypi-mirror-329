"""
AVX2-specific SIMD optimizations for x86_64 architecture.
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

class AVX2Parser(SIMDBase):
    """AVX2-optimized JSON parser operations."""
    
    def __init__(self):
        super().__init__()
        self._init_avx2()
    
    def _init_avx2(self):
        """Initialize AVX2-specific optimizations."""
        if HAVE_NUMBA:
            # Compile optimized functions
            self._compile_kernels()
    
    @staticmethod
    @jit(nopython=True, parallel=True)
    def _find_whitespace_avx2(data: np.ndarray, whitespace_mask: np.ndarray) -> np.ndarray:
        """AVX2-optimized whitespace detection."""
        result = np.zeros(len(data), dtype=np.bool_)
        for i in numba.prange(0, len(data), 32):
            chunk = data[i:i+32]
            result[i:i+len(chunk)] = whitespace_mask[chunk]
        return result
    
    @staticmethod
    @jit(nopython=True)
    def _find_structural_avx2(data: np.ndarray, char_class: np.ndarray) -> np.ndarray:
        """AVX2-optimized structural character detection."""
        result = np.zeros(len(data), dtype=np.bool_)
        for i in range(0, len(data), 32):
            chunk = data[i:i+32]
            classes = char_class[chunk]
            result[i:i+len(chunk)] = (classes >= 6) & (classes <= 11)
        return result
    
    @staticmethod
    @vectorize(['float64(float64, float64)'], target='parallel')
    def _simd_number_parse(mantissa: float, exponent: float) -> float:
        """AVX2-optimized number parsing."""
        return mantissa * (10.0 ** exponent)
    
    def parse_numbers_fast(self, data: Union[bytes, bytearray],
                          positions: List[slice]) -> List[float]:
        """Parse numbers using AVX2 optimization.
        
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
                numbers.append(self._simd_number_parse(mantissa, exponent))
            else:
                numbers.append(float(num_str))
        
        return numbers
    
    def find_strings_fast(self, data: Union[bytes, bytearray]) -> List[Tuple[int, int]]:
        """Find string literals using AVX2 optimization.
        
        Args:
            data: Input data
            
        Returns:
            List of (start, end) positions for strings
        """
        if not HAVE_NUMBA:
            return [(s.start, s.stop) for s in self.find_strings(data)]
        
        arr = np.frombuffer(data, dtype=np.uint8)
        result = []
        
        # Process 32 bytes at a time
        for i in range(0, len(arr), 32):
            chunk = arr[i:i+32]
            
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
        """Validate UTF-8 encoding using AVX2 optimization.
        
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
        def _validate_utf8_avx2(arr):
            for i in numba.prange(0, len(arr)):
                # Check for invalid UTF-8 sequences
                if arr[i] > 0x7F:  # Non-ASCII
                    if arr[i] & 0xE0 == 0xC0:  # 2-byte sequence
                        if i + 1 >= len(arr) or (arr[i+1] & 0xC0) != 0x80:
                            return False
                    elif arr[i] & 0xF0 == 0xE0:  # 3-byte sequence
                        if (i + 2 >= len(arr) or
                            (arr[i+1] & 0xC0) != 0x80 or
                            (arr[i+2] & 0xC0) != 0x80):
                            return False
                    elif arr[i] & 0xF8 == 0xF0:  # 4-byte sequence
                        if (i + 3 >= len(arr) or
                            (arr[i+1] & 0xC0) != 0x80 or
                            (arr[i+2] & 0xC0) != 0x80 or
                            (arr[i+3] & 0xC0) != 0x80):
                            return False
                    else:
                        return False
            return True
        
        return _validate_utf8_avx2(np.frombuffer(data, dtype=np.uint8))
    
    def _compile_kernels(self):
        """Pre-compile Numba kernels for better performance."""
        if not HAVE_NUMBA:
            return
        
        # Compile with dummy data
        dummy_data = np.zeros(64, dtype=np.uint8)
        dummy_mask = np.zeros(256, dtype=bool)
        dummy_class = np.zeros(256, dtype=np.uint8)
        
        # Warm up the JIT compiler
        self._find_whitespace_avx2(dummy_data, dummy_mask)
        self._find_structural_avx2(dummy_data, dummy_class)
        self._simd_number_parse(1.0, 1.0)
