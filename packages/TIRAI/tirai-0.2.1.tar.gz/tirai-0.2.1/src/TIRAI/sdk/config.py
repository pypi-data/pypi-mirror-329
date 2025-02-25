"""Configuration management for TIRAI SDK"""

import os
from typing import Dict, Any

from .providers import OpenAISDK, XAI_SDK, DeepSeekSDK, AzureOpenAISDK


class AISDKConfig:
    """Configuration manager for AI SDKs"""

    @staticmethod
    def get_config(model_type: str) -> Dict[str, str]:
        """Get configuration for a specific model type

        Args:
            model_type: Type of model ('gpt', 'grok', 'deepseek', 'azure')

        Returns:
            Dictionary containing configuration for the specified model

        Raises:
            ValueError: If API key is not found in environment variables
        """
        try:
            if model_type == 'gpt':
                return {
                    'api_key': os.environ['OPENAI_API_KEY'],
                    'base_url': os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')
                }
            elif model_type == 'grok':
                return {
                    'api_key': os.environ['XAI_API_KEY'],
                    'base_url': os.environ.get('XAI_BASE_URL', 'https://api.x.ai/v1')
                }
            elif model_type == 'deepseek':
                return {
                    'api_key': os.environ['DEEPSEEK_API_KEY'],
                    'base_url': os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
                }
            elif model_type == 'azure':
                return {
                    'api_key': os.environ['AZURE_OPENAI_API_KEY'],
                    'api_url': os.environ['AZURE_OPENAI_URL']
                }
            else:
                raise ValueError(f"Unknown model type: {model_type}")
        except KeyError as e:
            env_var = str(e).strip("'")
            raise ValueError(f"{env_var} not found in environment variables") from None

    @staticmethod
    def create_sdk(model_name: str) -> Any:
        """Create an SDK instance for the specified model

        Args:
            model_name: Name of the model to use (e.g., 'gpt-4o', 'grok-2-latest')

        Returns:
            SDK instance for the specified model

        Raises:
            ValueError: If model type is unknown or API key is missing
        """
        model_map = {
            'gpt-4o': ('gpt', OpenAISDK),
            'grok-2-latest': ('grok', XAI_SDK),
            'deepseek-reasoner': ('deepseek', DeepSeekSDK),
            'azure-o3-mini': ('azure', AzureOpenAISDK)
        }

        if model_name not in model_map:
            raise ValueError(f"Unknown model: {model_name}")

        model_type, sdk_class = model_map[model_name]
        config = AISDKConfig.get_config(model_type)

        if model_type == 'azure':
            return sdk_class(config['api_key'], model_name, config['api_url'])
        else:
            return sdk_class(config['api_key'], model_name, config['base_url'])
