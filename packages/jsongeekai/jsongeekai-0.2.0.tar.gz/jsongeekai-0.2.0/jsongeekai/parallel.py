"""
Parallel processing module for JsonGeekAI.
"""
import os
import json
import queue
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Dict, List, Any, Optional, Union, Tuple
import numpy as np
from .exceptions import JSONParseError

class ChunkParser:
    """JSON chunk parser with thread safety."""
    
    def __init__(self, max_workers: Optional[int] = None):
        """Initialize chunk parser.
        
        Args:
            max_workers: Maximum number of worker threads/processes.
                        If None, uses CPU count.
        """
        self.max_workers = max_workers or os.cpu_count()
        self._result_queue = queue.Queue()
        self._error_queue = queue.Queue()
    
    def _find_chunk_boundaries(self, data: str) -> List[Tuple[int, int]]:
        """Find safe chunk boundaries for parallel processing.
        
        Args:
            data: JSON string to parse
            
        Returns:
            List of (start, end) positions for chunks
        """
        chunks = []
        depth = 0
        chunk_start = 0
        in_string = False
        escape_char = False
        
        # Estimate chunk size based on CPU count and data length
        target_chunk_size = max(len(data) // (self.max_workers * 2), 1024 * 1024)
        
        for i, char in enumerate(data):
            # Handle string literals
            if char == '"' and not escape_char:
                in_string = not in_string
            elif char == '\\' and not escape_char:
                escape_char = True
                continue
            
            if not in_string:
                if char in '{[':
                    depth += 1
                elif char in '}]':
                    depth -= 1
            
            escape_char = False
            
            # Create new chunk when we're at root level and chunk is large enough
            if depth == 0 and not in_string and i - chunk_start >= target_chunk_size:
                if char in ']},:':
                    chunks.append((chunk_start, i + 1))
                    chunk_start = i + 1
        
        # Add final chunk
        if chunk_start < len(data):
            chunks.append((chunk_start, len(data)))
        
        return chunks

    def _parse_chunk(self, data: str, start: int, end: int, chunk_id: int) -> None:
        """Parse a single JSON chunk.
        
        Args:
            data: Complete JSON string
            start: Start position of chunk
            end: End position of chunk
            chunk_id: Identifier for ordering results
        """
        try:
            # Find the context before and after the chunk
            context_size = 1024
            pre_context = data[max(0, start - context_size):start]
            post_context = data[end:min(len(data), end + context_size)]
            
            # Determine if we need to add brackets
            if data[start] != '[' and data[start] != '{':
                chunk_data = '[' + data[start:end] + ']'
                is_array = True
            else:
                chunk_data = data[start:end]
                is_array = False
            
            # Parse the chunk
            result = json.loads(chunk_data)
            
            # Extract inner data if we added brackets
            if is_array:
                result = result[0] if len(result) == 1 else result
            
            self._result_queue.put((chunk_id, result))
            
        except json.JSONDecodeError as e:
            # Enhance error message with context
            context = f"\nNear: ...{data[max(0, e.pos-50):min(len(data), e.pos+50)]}..."
            self._error_queue.put(JSONParseError(str(e), e.pos + start, context))

    def parse(self, data: str) -> Union[Dict, List]:
        """Parse JSON string in parallel.
        
        Args:
            data: JSON string to parse
            
        Returns:
            Parsed JSON data structure
            
        Raises:
            JSONParseError: If parsing fails
        """
        # Find chunk boundaries
        chunks = self._find_chunk_boundaries(data)
        
        # Create thread pool for parsing
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit parsing tasks
            futures = [
                executor.submit(self._parse_chunk, data, start, end, i)
                for i, (start, end) in enumerate(chunks)
            ]
            
            # Wait for all tasks to complete
            for future in futures:
                future.result()
        
        # Check for errors
        if not self._error_queue.empty():
            raise self._error_queue.get()
        
        # Combine results in correct order
        results = []
        while not self._result_queue.empty():
            chunk_id, result = self._result_queue.get()
            results.append((chunk_id, result))
        
        results.sort(key=lambda x: x[0])
        
        # Merge results
        if len(results) == 1:
            return results[0][1]
        
        final_result = []
        for _, chunk_result in results:
            if isinstance(chunk_result, list):
                final_result.extend(chunk_result)
            else:
                final_result.append(chunk_result)
        
        return final_result
