"""
Base Tool Class - Foundation for all enterprise tools
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class ToolParameter(BaseModel):
    """Tool parameter definition"""
    name: str
    type: str  # string, number, boolean, array, object
    description: str
    required: bool = True
    default: Optional[Any] = None
    enum: Optional[List[Any]] = None


class ToolResult(BaseModel):
    """Standardized tool execution result"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: str = ""
    tool_name: str = ""
    
    def __init__(self, **data):
        if not data.get('timestamp'):
            data['timestamp'] = datetime.now().isoformat()
        super().__init__(**data)


class ToolCategory(str, Enum):
    """Tool categories for organization"""
    DATA_RETRIEVAL = "data_retrieval"
    CALCULATION = "calculation"
    COMMUNICATION = "communication"
    PLANNING = "planning"
    REPORTING = "reporting"
    ANALYSIS = "analysis"
    INTEGRATION = "integration"
    VALIDATION = "validation"


class BaseTool(ABC):
    """Base class for all enterprise tools"""
    
    def __init__(
        self,
        name: str,
        description: str,
        category: ToolCategory,
        version: str = "1.0.0"
    ):
        self.name = name
        self.description = description
        self.category = category
        self.version = version
        self.parameters: List[ToolParameter] = []
        self.enabled = True
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool with given parameters
        
        Returns:
            ToolResult: Standardized result object
        """
        pass
    
    def validate_parameters(self, **kwargs) -> tuple[bool, str]:
        """
        Validate input parameters
        
        Returns:
            tuple: (is_valid, error_message)
        """
        for param in self.parameters:
            if param.required and param.name not in kwargs:
                return False, f"Missing required parameter: {param.name}"
            
            if param.name in kwargs:
                value = kwargs[param.name]
                
                # Type validation
                type_map = {
                    'string': str,
                    'number': (int, float),
                    'boolean': bool,
                    'array': list,
                    'object': dict
                }
                
                expected_type = type_map.get(param.type)
                if expected_type and not isinstance(value, expected_type):
                    return False, f"Parameter '{param.name}' must be {param.type}"
                
                # Enum validation
                if param.enum and value not in param.enum:
                    return False, f"Parameter '{param.name}' must be one of {param.enum}"
        
        return True, ""
    
    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema for AI agents"""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "version": self.version,
            "enabled": self.enabled,
            "parameters": [
                {
                    "name": p.name,
                    "type": p.type,
                    "description": p.description,
                    "required": p.required,
                    "default": p.default,
                    "enum": p.enum
                }
                for p in self.parameters
            ]
        }



