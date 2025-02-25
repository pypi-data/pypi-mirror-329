"""DeepSeek API provider implementation"""

import time
from typing import Tuple
import requests

from ..base import BaseAISDK


class DeepSeekSDK(BaseAISDK):
    """DeepSeek API client"""

    def __init__(self, api_key: str, model: str, base_url: str = 'https://api.deepseek.com/v1'):
        super().__init__(model)
        self.api_key = api_key
        self.base_url = base_url

    def get_response(self, text: str) -> Tuple[str, float]:
        """Get response from DeepSeek model

        Args:
            text: Input text to send to the model

        Returns:
            Tuple of (response text, time taken in seconds)

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        start_time = time.time()

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': self.model,
            'messages': [{'role': 'user', 'content': text}],
            'temperature': 0.6
        }

        response = requests.post(
            f'{self.base_url}/chat/completions',
            headers=headers,
            json=data
        )
        response.raise_for_status()

        end_time = time.time()
        return response.json()['choices'][0]['message']['content'], end_time - start_time
