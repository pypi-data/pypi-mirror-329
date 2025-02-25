"""Base classes and interfaces for TIR AI SDK"""

from abc import ABC, abstractmethod
from typing import Tuple, List


class BaseAISDK(ABC):
    """Base class for all AI SDK implementations"""

    def __init__(self, model: str):
        """Initialize the SDK with a model

        Args:
            model: Name of the model to use
        """
        self.model = model

    @abstractmethod
    def get_response(self, text: str) -> Tuple[str, float]:
        """Get response from AI model

        Args:
            text: Input text to send to the model

        Returns:
            Tuple of (response text, time taken in seconds)

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If configuration is invalid
        """
        pass

    @staticmethod
    def list_models() -> List[str]:
        """List all available models

        Returns:
            List of model names supported by the SDK
        """
        return [
            'grok-2-latest',
            'deepseek-reasoner',
            'azure-o3-mini',
            'gpt-4o'
        ]
