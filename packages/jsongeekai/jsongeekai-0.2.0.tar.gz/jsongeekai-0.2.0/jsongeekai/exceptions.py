"""
JsonGeekAI custom exceptions module.
"""

class JsonGeekAIError(Exception):
    """Base exception for all JsonGeekAI errors."""
    def __init__(self, message: str, docs_url: str = None):
        self.message = message
        self.docs_url = docs_url or "https://jsongeekai.readthedocs.io/errors/"
        super().__init__(f"{message}\nFor more information, visit: {self.docs_url}")


class SIMDNotSupportedError(JsonGeekAIError):
    """Raised when SIMD operations are not supported on the current platform."""
    def __init__(self, message: str = None):
        super().__init__(
            message or "SIMD operations are not supported on this platform.",
            "https://jsongeekai.readthedocs.io/errors/simd-support"
        )


class WASMLoadError(JsonGeekAIError):
    """Raised when the WASM module fails to load."""
    def __init__(self, message: str = None, original_error: Exception = None):
        self.original_error = original_error
        super().__init__(
            message or f"Failed to load WASM module: {str(original_error)}",
            "https://jsongeekai.readthedocs.io/errors/wasm-setup"
        )


class JSONParseError(JsonGeekAIError):
    """Raised when JSON parsing fails."""
    def __init__(self, message: str, position: int, context: str = None):
        self.position = position
        self.context = context
        context_msg = f"\nContext: {context}" if context else ""
        super().__init__(
            f"JSON parse error at position {position}: {message}{context_msg}",
            "https://jsongeekai.readthedocs.io/errors/parse-errors"
        )


class MemoryLimitError(JsonGeekAIError):
    """Raised when processing exceeds memory limits."""
    def __init__(self, size: int, limit: int):
        self.size = size
        self.limit = limit
        super().__init__(
            f"Memory limit exceeded: Attempted to process {size} bytes (limit: {limit} bytes)",
            "https://jsongeekai.readthedocs.io/errors/memory-limits"
        )


class DepthLimitError(JsonGeekAIError):
    """Raised when JSON nesting depth exceeds limits."""
    def __init__(self, depth: int, max_depth: int):
        self.depth = depth
        self.max_depth = max_depth
        super().__init__(
            f"Maximum nesting depth exceeded: {depth} (limit: {max_depth})",
            "https://jsongeekai.readthedocs.io/errors/depth-limits"
        )


class FormatError(JsonGeekAIError):
    """Raised when there are format-specific errors."""
    def __init__(self, message: str, format: str = None):
        self.format = format
        format_msg = f" in {format} format" if format else ""
        super().__init__(
            f"Format error{format_msg}: {message}",
            "https://jsongeekai.readthedocs.io/errors/format-errors"
        )


class EncodingError(JsonGeekAIError):
    """Raised when there are encoding/decoding errors."""
    def __init__(self, message: str, encoding: str = None):
        self.encoding = encoding
        encoding_msg = f" with {encoding} encoding" if encoding else ""
        super().__init__(
            f"Encoding error{encoding_msg}: {message}",
            "https://jsongeekai.readthedocs.io/errors/encoding-errors"
        )


class CompressionError(JsonGeekAIError):
    """Raised when there are compression/decompression errors."""
    def __init__(self, message: str, algorithm: str = None):
        self.algorithm = algorithm
        algo_msg = f" using {algorithm}" if algorithm else ""
        super().__init__(
            f"Compression error{algo_msg}: {message}",
            "https://jsongeekai.readthedocs.io/errors/compression-errors"
        )
