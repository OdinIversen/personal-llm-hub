import os
import anthropic
from typing import Dict, Any, Optional

def get_response(
    message: str,
    system_prompt: str,
    model: str = "claude-3-5-sonnet",
    parameters: Optional[Dict[str, Any]] = None
) -> str:
    """
    Get a response from the Anthropic Claude API.
    
    Args:
        message: The user message to send
        system_prompt: The system instructions for the model
        model: The specific Claude model to use
        parameters: Additional parameters like temperature, max_tokens

    Returns:
        The model's response text
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Missing Anthropic API key. Set ANTHROPIC_API_KEY in .env file.")
    
    # Set up default parameters
    params = {
        "temperature": 0.7,
        "max_tokens": 1000,
    }
    
    # Update with custom parameters if provided
    if parameters:
        params.update(parameters)
    
    # Initialize client
    client = anthropic.Anthropic(api_key=api_key)
    
    try:
        # Create message
        response = client.messages.create(
            model=model,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=params.get("temperature"),
            max_tokens=params.get("max_tokens")
        )
        
        # Extract and return the text response
        return response.content[0].text
        
    except Exception as e:
        print(f"Error calling Anthropic API: {e}")
        raise