"""
Extended format support for JsonGeekAI.
Includes BSON, YAML, and Protocol Buffers support.
"""
from typing import Any, Dict, List, Union, BinaryIO, TextIO, Optional, Type
import json
import bson
import yaml
from ruamel.yaml import YAML
from google.protobuf import json_format
from google.protobuf.message import Message
from .exceptions import FormatError, EncodingError

class BSONHandler:
    """BSON format handler."""
    
    @staticmethod
    def encode(data: Dict) -> bytes:
        """Encode data to BSON format.
        
        Args:
            data: Dictionary to encode
            
        Returns:
            BSON bytes
            
        Raises:
            FormatError: If encoding fails
        """
        try:
            return bson.encode(data)
        except Exception as e:
            raise FormatError(f"BSON encoding error: {str(e)}", "bson")
    
    @staticmethod
    def decode(data: bytes) -> Dict:
        """Decode BSON data.
        
        Args:
            data: BSON bytes
            
        Returns:
            Decoded dictionary
            
        Raises:
            FormatError: If decoding fails
        """
        try:
            return bson.decode(data)
        except Exception as e:
            raise FormatError(f"BSON decoding error: {str(e)}", "bson")
    
    @staticmethod
    def stream_decode(file: BinaryIO) -> Dict:
        """Stream decode BSON data.
        
        Args:
            file: Binary file object
            
        Yields:
            Decoded dictionaries
        """
        while True:
            try:
                yield bson.decode_file_iter(file)
            except StopIteration:
                break
            except Exception as e:
                raise FormatError(f"BSON stream decoding error: {str(e)}", "bson")


class YAMLHandler:
    """YAML format handler with advanced features."""
    
    def __init__(self, pure_yaml: bool = False):
        """Initialize YAML handler.
        
        Args:
            pure_yaml: If True, use PyYAML. If False, use ruamel.yaml
                      for advanced features.
        """
        self.pure_yaml = pure_yaml
        if not pure_yaml:
            self.yaml = YAML()
            self.yaml.preserve_quotes = True
            self.yaml.explicit_start = True
            self.yaml.explicit_end = True
    
    def dump(self, data: Any, stream: Optional[TextIO] = None) -> Optional[str]:
        """Dump data as YAML.
        
        Args:
            data: Data to dump
            stream: Optional text stream to write to
            
        Returns:
            YAML string if stream is None
        """
        try:
            if self.pure_yaml:
                return yaml.dump(data, stream, sort_keys=False)
            else:
                return self.yaml.dump(data, stream)
        except Exception as e:
            raise FormatError(f"YAML dump error: {str(e)}", "yaml")
    
    def load(self, stream: Union[str, TextIO]) -> Any:
        """Load YAML data.
        
        Args:
            stream: YAML string or text stream
            
        Returns:
            Loaded data structure
        """
        try:
            if self.pure_yaml:
                return yaml.safe_load(stream)
            else:
                return self.yaml.load(stream)
        except Exception as e:
            raise FormatError(f"YAML load error: {str(e)}", "yaml")


class ProtobufHandler:
    """Protocol Buffers format handler."""
    
    @staticmethod
    def message_to_dict(message: Message) -> Dict:
        """Convert Protobuf message to dictionary.
        
        Args:
            message: Protobuf message
            
        Returns:
            Dictionary representation
        """
        try:
            return json_format.MessageToDict(
                message,
                preserving_proto_field_name=True,
                including_default_value_fields=True
            )
        except Exception as e:
            raise FormatError(f"Protobuf to dict error: {str(e)}", "protobuf")
    
    @staticmethod
    def dict_to_message(data: Dict, message_type: Type[Message]) -> Message:
        """Convert dictionary to Protobuf message.
        
        Args:
            data: Dictionary data
            message_type: Protobuf message class
            
        Returns:
            Protobuf message
        """
        try:
            message = message_type()
            json_format.ParseDict(data, message)
            return message
        except Exception as e:
            raise FormatError(f"Dict to protobuf error: {str(e)}", "protobuf")
    
    @staticmethod
    def load_proto_file(proto_file: str) -> None:
        """Load .proto file and generate Python classes.
        
        Args:
            proto_file: Path to .proto file
        """
        from grpc_tools import protoc
        import os
        
        proto_dir = os.path.dirname(proto_file)
        proto_name = os.path.basename(proto_file)
        
        try:
            protoc.main([
                'grpc_tools.protoc',
                f'--proto_path={proto_dir}',
                f'--python_out={proto_dir}',
                f'--grpc_python_out={proto_dir}',
                os.path.join(proto_dir, proto_name)
            ])
        except Exception as e:
            raise FormatError(f"Proto file compilation error: {str(e)}", "protobuf")


class FormatConverter:
    """Format conversion utilities."""
    
    def __init__(self):
        self.bson_handler = BSONHandler()
        self.yaml_handler = YAMLHandler()
        self.protobuf_handler = ProtobufHandler()
    
    def convert(self, data: Any, from_format: str, to_format: str,
               protobuf_message_type: Type[Message] = None) -> Any:
        """Convert data between formats.
        
        Args:
            data: Data to convert
            from_format: Source format ('json', 'bson', 'yaml', 'protobuf')
            to_format: Target format
            protobuf_message_type: Required for protobuf conversion
            
        Returns:
            Converted data
        """
        # First convert to dictionary (if not already)
        if from_format == 'bson':
            if isinstance(data, bytes):
                data = self.bson_handler.decode(data)
        elif from_format == 'yaml':
            if isinstance(data, (str, TextIO)):
                data = self.yaml_handler.load(data)
        elif from_format == 'protobuf':
            if isinstance(data, Message):
                data = self.protobuf_handler.message_to_dict(data)
        
        # Then convert to target format
        if to_format == 'bson':
            return self.bson_handler.encode(data)
        elif to_format == 'yaml':
            return self.yaml_handler.dump(data)
        elif to_format == 'protobuf':
            if not protobuf_message_type:
                raise ValueError("protobuf_message_type is required for protobuf conversion")
            return self.protobuf_handler.dict_to_message(data, protobuf_message_type)
        elif to_format == 'json':
            return json.dumps(data)
        else:
            raise ValueError(f"Unsupported format: {to_format}")


# Initialize global converter instance
converter = FormatConverter()
