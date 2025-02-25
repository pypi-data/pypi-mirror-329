"""Example usage of AWS Claude provider through TIRAI SDK"""

from TIRAI.sdk.providers.awsclaude import AWSClaudeSDK
import os

def main():
    # Initialize the Claude client with credentials from environment variables
    claude = AWSClaudeSDK(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name="us-west-2",
        model="anthropic.claude-3-7-sonnet-20250219-v1:0", 
        max_tokens=1000,  # Increase max tokens for longer responses
        temperature=0.7,  # Lower temperature for more focused responses
    )

    # Example prompts to test
    prompts = [
        "Explain quantum computing in one sentence.",
        "Write a haiku about programming.",
    ]

    # Process each prompt
    for prompt in prompts:
        print(f"\nPrompt: {prompt}")
        response = claude.generate(prompt)
        print(f"Response: {response}")

if __name__ == "__main__":
    main()
