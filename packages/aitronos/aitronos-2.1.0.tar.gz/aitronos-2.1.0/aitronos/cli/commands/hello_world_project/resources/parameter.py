import json
from pathlib import Path
from typing import Optional
from .helpers import User

class Parameters:
    def __init__(self, parameters_path: Optional[Path] = None):
        if parameters_path is None:
            parameters_path = Path(__file__).parent / 'parameters.json'
        
        with open(parameters_path, 'r') as f:
            self.parameters = json.load(f)
        
        self._parameters_dict = {param['id']: param for param in self.parameters}

    def get_parameter(self, parameter_id: str) -> dict:
        """Get a parameter by its ID"""
        if parameter_id not in self._parameters_dict:
            raise KeyError(f"Parameter '{parameter_id}' not found")
        return self._parameters_dict[parameter_id]

    def get_value(self, parameter_id: str) -> any:
        """Get the value of a parameter by its ID"""
        return self.get_parameter(parameter_id)['value']

    def get_all_parameters(self) -> list:
        """Get all parameters"""
        return self.parameters

    def is_required(self, parameter_id: str) -> bool:
        """Check if a parameter is required"""
        return self.get_parameter(parameter_id)['required']

    def get_description(self, parameter_id: str) -> str:
        """Get the description of a parameter"""
        return self.get_parameter(parameter_id)['description']

    def get_type(self, parameter_id: str) -> str:
        """Get the type of a parameter"""
        return self.get_parameter(parameter_id)['type']


