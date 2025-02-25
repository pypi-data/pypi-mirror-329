from abc import ABC, abstractmethod
from typing import Any, Dict, List

class LLMClient(ABC):    
    @abstractmethod
    def send(self, messages: List[Dict], tools: List[Dict], model: str) -> Any:
        pass

    @abstractmethod
    def stream(self, messages: List[Dict], tools: List[Dict], model: str) -> Any:
        pass

    @abstractmethod
    def serialize_response(self, response: Any) -> Dict:
        pass