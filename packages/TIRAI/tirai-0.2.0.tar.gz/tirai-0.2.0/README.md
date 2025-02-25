# TIRAI

The I Research AI - A unified SDK for various AI model providers.

[![PyPI version](https://badge.fury.io/py/TIRAI.svg)](https://badge.fury.io/py/TIRAI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation & Updates

```bash
# First time installation
pip install TIRAI
```
```bash
# Update to latest version
pip install --upgrade TIRAI
```

## Features

- Unified interface for multiple AI providers:
  - AWS Claude 3.7 Sonnet
  - xAI's grok-2-latest (waiting for grok 3 api)
  - DeepSeek's deepseek-reasoner
  - Azure o3-mini
  - OpenAI gpt-4o
- Simple API key management via environment variables
- Automatic model selection and configuration
- Response time tracking
- Comprehensive test coverage
- Type hints and documentation


## Super Quick Start
```python
from TIRAI import AISDKConfig

sdk = AISDKConfig.create_sdk('aws-claude-3.7-sonnet')
response, time_taken = sdk.get_response("What is artificial intelligence?")

print(response)
```

## Quick Start

1. Set up environment variables for your chosen provider:

```bash
# AWS Claude
export AWS_ACCESS_KEY_ID="your-access-key"                  # Required
export AWS_SECRET_ACCESS_KEY="your-secret-key"              # Required
export AWS_REGION="your-region"                             # Required

# xAI (Grok)
export XAI_API_KEY="your-key"                               # Required
export XAI_BASE_URL="https://api.x.ai/v1"                   # Optional

# DeepSeek
export DEEPSEEK_API_KEY="your-key"                          # Required
export DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"      # Optional

# Azure OpenAI
export AZURE_OPENAI_API_KEY="your-key"                      # Required
export AZURE_OPENAI_URL="your-deployment-url"               # Required

# OpenAI
export OPENAI_API_KEY="your-key"                             # Required
export OPENAI_BASE_URL="https://api.openai.com/v1"          # Optional
```

2. Create an SDK instance and get responses:

```python
from TIRAI import AISDKConfig

# Create an SDK instance for your chosen model
sdk = AISDKConfig.create_sdk('aws-claude-3.7-sonnet')  # For AWS Claude 3.7
# sdk = AISDKConfig.create_sdk('grok-2-latest')  # For xAI (Grok)
# sdk = AISDKConfig.create_sdk('deepseek-reasoner')  # For DeepSeek R1
# sdk = AISDKConfig.create_sdk('azure-o3-mini')  # For Azure o3-mini
# sdk = AISDKConfig.create_sdk('gpt-4o')         # For OpenAI GPT-4o

# Get a response
try:
    response, time_taken = sdk.get_response("What is artificial intelligence?")
    print(f"Response: {response}")
    print(f"Time taken: {time_taken:.2f}s")
except Exception as e:
    print(f"Error: {e}")
```

## Supported Models

- AWS Claude: `aws-claude-3.7-sonnet`
- xAI: `grok-2-latest`
- DeepSeek: `deepseek-reasoner`
- Azure OpenAI: `azure-o3-mini`
- OpenAI: `gpt-4o`

## Error Handling

The SDK provides clear error messages for common issues:

```python
try:
    response, time = sdk.get_response("Your prompt here")
except ValueError as e:
    print(f"Configuration error: {e}")  # Missing API keys, invalid models
except requests.exceptions.RequestException as e:
    print(f"API call failed: {e}")  # Network errors, API timeouts
```

## Advanced Usage Examples for Cloud Providers

### AWS Claude with Custom Parameters

```python
from TIRAI.sdk.providers import AWSClaudeSDK

sdk = AWSClaudeSDK(
    aws_access_key_id="your_access_key",
    aws_secret_access_key="your_secret_key",
    region_name="your_region",
    temperature=1,  # optional
    max_tokens=500,   # optional
    top_p=0.999,      # optional
    top_k=250,       # optional
    stop_sequences=["Stop here"]  # optional
)

response, time_taken = sdk.get_response("Your prompt here")
print(f"Response: {response}")
print(f"Time taken: {time_taken:.2f}s")
```

### Azure OpenAI

```python
from TIRAI.sdk.providers import AzureOpenAISDK

sdk = AzureOpenAISDK(
    api_key="your_azure_key",
    model="azure-o3-mini",
    deployment_url="your_deployment_url"  # required
)

response, time_taken = sdk.get_response("Your prompt here")
print(f"Response: {response}")
print(f"Time taken: {time_taken:.2f}s")
```


## Development

For development and contribution guidelines, please see [MAINTAINING.md](MAINTAINING.md).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
