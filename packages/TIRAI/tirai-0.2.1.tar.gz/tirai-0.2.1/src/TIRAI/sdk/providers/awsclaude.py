"""AWS Claude API provider implementation"""

import time
import json
from typing import Tuple, Optional, List
import boto3

from ..base import BaseAISDK


class AWSClaudeSDK(BaseAISDK):
    """AWS Claude API client"""

    def __init__(
        self, 
        aws_access_key_id: str, 
        aws_secret_access_key: str, 
        region_name: str, 
        model: str = "anthropic.claude-3-7-sonnet-20250219-v1:0",
        max_tokens: int = 200,
        temperature: float = 1.0,
        top_p: float = 0.999,
        top_k: int = 250,
        stop_sequences: Optional[List[str]] = None
    ):
        super().__init__(model)
        self.client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.stop_sequences = stop_sequences or []

    def get_response(self, text: str) -> Tuple[str, float]:
        """Get response from AWS Claude model

        Args:
            text: Input text to send to the model

        Returns:
            Tuple of (response text, time taken in seconds)

        Raises:
            ClientError: If the API request fails
        """
        start_time = time.time()

        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "stop_sequences": self.stop_sequences,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            ]
        }

        response = self.client.invoke_model(
            modelId=self.model,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        
        end_time = time.time()
        return response_body['content'][0]['text'], end_time - start_time
