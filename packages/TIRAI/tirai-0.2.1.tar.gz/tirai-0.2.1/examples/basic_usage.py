"""Basic usage example for TIRAI SDK"""

from TIRAI import AISDKConfig

def main():
    """
    Example usage of TIRAI SDK.
    
    Make sure to set the appropriate environment variables before running:
    - OPENAI_API_KEY for OpenAI
    - XAI_API_KEY for Grok
    - DEEPSEEK_API_KEY for DeepSeek
    - AZURE_OPENAI_API_KEY and AZURE_OPENAI_URL for Azure OpenAI
    """
    # Create SDK instance for your chosen model
    sdk = AISDKConfig.create_sdk('grok-2-latest')  # For Grok

    # Example prompt
    prompt = "What is artificial intelligence?"

    try:
        # Get response from the model
        response, time_taken = sdk.get_response(prompt)
        
        # Print results
        print(f"\nPrompt: {prompt}")
        print(f"Response: {response}")
        print(f"Time taken: {time_taken:.2f}s")
    
    except ValueError as e:
        print(f"Configuration error: {e}")  # Missing API keys, invalid models
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
