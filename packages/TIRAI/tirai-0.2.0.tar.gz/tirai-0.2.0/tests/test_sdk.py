"""Tests for TIRAI SDK"""

import os
import pytest
import responses
from TIRAI import AISDKConfig
from TIRAI.sdk.providers import OpenAISDK, XAI_SDK, DeepSeekSDK, AzureOpenAISDK

# Test data
TEST_API_KEY = "test-api-key"
TEST_PROMPT = "What is AI?"
TEST_RESPONSE = "AI is artificial intelligence"
TEST_BASE_URL = "https://api.test.com/v1"
TEST_AZURE_URL = "https://test.azure.openai.com/openai/deployments/test/chat/completions"

@pytest.fixture
def mock_env(monkeypatch):
    """Set up test environment variables"""
    # Required API keys
    monkeypatch.setenv("OPENAI_API_KEY", TEST_API_KEY)
    monkeypatch.setenv("XAI_API_KEY", TEST_API_KEY)
    monkeypatch.setenv("DEEPSEEK_API_KEY", TEST_API_KEY)
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", TEST_API_KEY)
    monkeypatch.setenv("AZURE_OPENAI_URL", TEST_AZURE_URL)
    
    # Optional base URLs
    monkeypatch.setenv("OPENAI_BASE_URL", TEST_BASE_URL)
    monkeypatch.setenv("XAI_BASE_URL", TEST_BASE_URL)
    monkeypatch.setenv("DEEPSEEK_BASE_URL", TEST_BASE_URL)

def test_config_creation(mock_env):
    """Test configuration creation for different providers"""
    # Test OpenAI config
    config = AISDKConfig.get_config('gpt')
    assert config['api_key'] == os.environ['OPENAI_API_KEY']
    assert config['base_url'] == os.environ['OPENAI_BASE_URL']
    
    # Test XAI config
    config = AISDKConfig.get_config('grok')
    assert config['api_key'] == os.environ['XAI_API_KEY']
    assert config['base_url'] == os.environ['XAI_BASE_URL']
    
    # Test DeepSeek config
    config = AISDKConfig.get_config('deepseek')
    assert config['api_key'] == os.environ['DEEPSEEK_API_KEY']
    assert config['base_url'] == os.environ['DEEPSEEK_BASE_URL']
    
    # Test Azure config
    config = AISDKConfig.get_config('azure')
    assert config['api_key'] == os.environ['AZURE_OPENAI_API_KEY']
    assert config['api_url'] == os.environ['AZURE_OPENAI_URL']

def test_sdk_creation(mock_env):
    """Test SDK instance creation for different models"""
    # Test OpenAI SDK
    sdk = AISDKConfig.create_sdk('gpt-4o')
    assert isinstance(sdk, OpenAISDK)
    assert sdk.model == 'gpt-4o'
    assert sdk.api_key == os.environ['OPENAI_API_KEY']
    
    # Test XAI SDK
    sdk = AISDKConfig.create_sdk('grok-2-latest')
    assert isinstance(sdk, XAI_SDK)
    assert sdk.model == 'grok-2-latest'
    assert sdk.api_key == os.environ['XAI_API_KEY']
    
    # Test DeepSeek SDK
    sdk = AISDKConfig.create_sdk('deepseek-reasoner')
    assert isinstance(sdk, DeepSeekSDK)
    assert sdk.model == 'deepseek-reasoner'
    assert sdk.api_key == os.environ['DEEPSEEK_API_KEY']
    
    # Test Azure SDK
    sdk = AISDKConfig.create_sdk('azure-o3-mini')
    assert isinstance(sdk, AzureOpenAISDK)
    assert sdk.model == 'azure-o3-mini'
    assert sdk.api_key == os.environ['AZURE_OPENAI_API_KEY']

@responses.activate
def test_openai_response(mock_env):
    """Test OpenAI API response handling"""
    responses.add(
        responses.POST,
        f"{os.environ['OPENAI_BASE_URL']}/chat/completions",
        json={"choices": [{"message": {"content": TEST_RESPONSE}}]},
        status=200
    )
    
    sdk = AISDKConfig.create_sdk('gpt-4o')
    response, time_taken = sdk.get_response(TEST_PROMPT)
    
    assert response == TEST_RESPONSE
    assert time_taken >= 0
    assert len(responses.calls) == 1
    assert responses.calls[0].request.headers['Authorization'] == f'Bearer {os.environ["OPENAI_API_KEY"]}'

@responses.activate
def test_xai_response(mock_env):
    """Test XAI API response handling"""
    responses.add(
        responses.POST,
        f"{os.environ['XAI_BASE_URL']}/chat/completions",
        json={"choices": [{"message": {"content": TEST_RESPONSE}}]},
        status=200
    )
    
    sdk = AISDKConfig.create_sdk('grok-2-latest')
    response, time_taken = sdk.get_response(TEST_PROMPT)
    
    assert response == TEST_RESPONSE
    assert time_taken >= 0

@responses.activate
def test_deepseek_response(mock_env):
    """Test DeepSeek API response handling"""
    responses.add(
        responses.POST,
        f"{os.environ['DEEPSEEK_BASE_URL']}/chat/completions",
        json={"choices": [{"message": {"content": TEST_RESPONSE}}]},
        status=200
    )
    
    sdk = AISDKConfig.create_sdk('deepseek-reasoner')
    response, time_taken = sdk.get_response(TEST_PROMPT)
    
    assert response == TEST_RESPONSE
    assert time_taken >= 0

@responses.activate
def test_azure_response(mock_env):
    """Test Azure OpenAI API response handling"""
    responses.add(
        responses.POST,
        os.environ['AZURE_OPENAI_URL'],
        json={"choices": [{"message": {"content": TEST_RESPONSE}}]},
        status=200
    )
    
    sdk = AISDKConfig.create_sdk('azure-o3-mini')
    response, time_taken = sdk.get_response(TEST_PROMPT)
    
    assert response == TEST_RESPONSE
    assert time_taken >= 0

def test_invalid_model():
    """Test error handling for invalid model"""
    with pytest.raises(ValueError):
        AISDKConfig.create_sdk('invalid-model')

def test_missing_api_key(monkeypatch):
    """Test error handling for missing API key"""
    # Clear all environment variables
    for key in ['OPENAI_API_KEY', 'XAI_API_KEY', 'DEEPSEEK_API_KEY', 'AZURE_OPENAI_API_KEY']:
        monkeypatch.delenv(key, raising=False)
    
    with pytest.raises(ValueError) as exc_info:
        AISDKConfig.create_sdk('gpt-4o')
    assert "API key not found" in str(exc_info.value)
