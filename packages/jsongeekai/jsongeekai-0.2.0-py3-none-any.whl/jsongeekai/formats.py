"""
Extended format support for JsonGeekAI.
"""
from typing import Any, Dict, List, Union, BinaryIO, TextIO, Optional
import json
import json5
import msgpack
import ijson
from .exceptions import FormatError

class FormatHandler:
    """Handler for various JSON-like formats."""
    
    @staticmethod
    def detect_format(data: Union[str, bytes], filename: Optional[str] = None) -> str:
        """Detect the format of input data.
        
        Args:
            data: Input data as string or bytes
            filename: Optional filename to help with detection
            
        Returns:
            Format name: 'json', 'json5', 'jsonl', 'msgpack'
        """
        if isinstance(data, bytes):
            # Check for MessagePack magic bytes
            if data.startswith(b'\x95') or data.startswith(b'\x80'):
                return 'msgpack'
            try:
                data = data.decode('utf-8')
            except UnicodeDecodeError:
                return 'msgpack'
        
        # Check file extension if provided
        if filename:
            if filename.endswith('.json5'):
                return 'json5'
            elif filename.endswith('.jsonl'):
                return 'jsonl'
            elif filename.endswith('.msgpack'):
                return 'msgpack'
        
        # Content-based detection
        data = data.strip()
        if data.startswith('{') or data.startswith('['):
            # Could be JSON or JSON5, try strict JSON first
            try:
                json.loads(data[:1000])  # Test with first 1000 chars
                return 'json'
            except json.JSONDecodeError:
                return 'json5'
        elif '\n' in data and all(line.strip().startswith('{') or 
                                 line.strip().startswith('[') 
                                 for line in data.splitlines() if line.strip()):
            return 'jsonl'
        
        return 'json'  # Default to standard JSON

    @staticmethod
    def parse_json5(data: str) -> Any:
        """Parse JSON5 format.
        
        Args:
            data: JSON5 string
            
        Returns:
            Parsed data structure
            
        Raises:
            FormatError: If parsing fails
        """
        try:
            return json5.loads(data)
        except Exception as e:
            raise FormatError(f"JSON5 parse error: {str(e)}")

    @staticmethod
    def parse_jsonl(data: str) -> List[Any]:
        """Parse JSON Lines format.
        
        Args:
            data: JSONL string
            
        Returns:
            List of parsed objects
            
        Raises:
            FormatError: If parsing fails
        """
        result = []
        for i, line in enumerate(data.splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                result.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise FormatError(f"JSONL parse error at line {i}: {str(e)}")
        return result

    @staticmethod
    def parse_msgpack(data: bytes) -> Any:
        """Parse MessagePack format.
        
        Args:
            data: MessagePack bytes
            
        Returns:
            Parsed data structure
            
        Raises:
            FormatError: If parsing fails
        """
        try:
            return msgpack.unpackb(data)
        except Exception as e:
            raise FormatError(f"MessagePack parse error: {str(e)}")

    @staticmethod
    def dump_json5(data: Any) -> str:
        """Dump data as JSON5 string.
        
        Args:
            data: Python object to serialize
            
        Returns:
            JSON5 string
        """
        return json5.dumps(data)

    @staticmethod
    def dump_jsonl(data: List[Any]) -> str:
        """Dump data as JSONL string.
        
        Args:
            data: List of Python objects
            
        Returns:
            JSONL string
        """
        return '\n'.join(json.dumps(item) for item in data)

    @staticmethod
    def dump_msgpack(data: Any) -> bytes:
        """Dump data as MessagePack bytes.
        
        Args:
            data: Python object to serialize
            
        Returns:
            MessagePack bytes
        """
        return msgpack.packb(data)

    @staticmethod
    def stream_parse(file: Union[TextIO, BinaryIO], format: str = 'json') -> Any:
        """Stream parse large files.
        
        Args:
            file: File object
            format: Format to parse ('json', 'json5', 'jsonl', 'msgpack')
            
        Yields:
            Parsed objects
        """
        if format == 'json':
            parser = ijson.parse(file)
            current_prefix = None
            current_obj = None
            
            for prefix, event, value in parser:
                if prefix == '' and event in ('start_map', 'start_array'):
                    current_prefix = prefix
                    current_obj = {} if event == 'start_map' else []
                elif prefix == current_prefix and event in ('end_map', 'end_array'):
                    yield current_obj
                    current_obj = None
                elif current_obj is not None:
                    if isinstance(current_obj, dict):
                        current_obj[prefix.split('.')[-1]] = value
                    else:
                        current_obj.append(value)
        
        elif format == 'jsonl':
            for line in file:
                line = line.strip()
                if line:
                    yield json.loads(line)
        
        elif format == 'msgpack':
            unpacker = msgpack.Unpacker(file)
            for obj in unpacker:
                yield obj
        
        else:
            raise ValueError(f"Unsupported streaming format: {format}")

class JSON5Parser:
    """Enhanced JSON5 parser with additional features."""
    
    @staticmethod
    def parse(data: str) -> Any:
        """Parse JSON5 with enhanced features.
        
        - Supports comments (single and multi-line)
        - Supports trailing commas
        - Supports single quotes
        - Supports hex numbers
        - Supports infinity and NaN
        """
        return json5.loads(data)

class JSONLinesWriter:
    """JSONL writer with compression support."""
    
    def __init__(self, filename: str, compress: bool = False):
        """Initialize JSONL writer.
        
        Args:
            filename: Output filename
            compress: Whether to compress output
        """
        self.filename = filename
        self.compress = compress
        self._file = None
    
    def __enter__(self):
        import gzip
        self._file = gzip.open(self.filename, 'wt') if self.compress else open(self.filename, 'w')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()
    
    def write(self, obj: Any):
        """Write object as JSONL line."""
        self._file.write(json.dumps(obj) + '\n')
