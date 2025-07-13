from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseTrigger(ABC):
    """Base class for all triggers"""
    
    def __init__(self, keywords: List[str], priority: int, activation_criteria: str,
                 positive_examples: List[str], negative_examples: List[str]):
        self.keywords = keywords
        self.priority = priority
        self.activation_criteria = activation_criteria
        self.positive_examples = positive_examples
        self.negative_examples = negative_examples
    
    @abstractmethod
    def action(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Execute the trigger action
        
        Args:
            query: The user's spoken text
            **kwargs: Additional context
        
        Returns:
            Dict with 'text', 'speak', and optional 'voice_settings'
        """
        pass
    
    def matches(self, query: str) -> bool:
        """Check if this trigger should be activated for the given query"""
        query_lower = query.lower()
        return any(keyword.lower() in query_lower for keyword in self.keywords)
    
    def __str__(self):
        return f"{self.__class__.__name__}(priority={self.priority}, keywords={self.keywords})" 