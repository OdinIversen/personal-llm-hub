import os
from openai import OpenAI
from typing import Dict, Any, Optional

def get_response(
    message: str,
    system_prompt: str,
    model: str = "gpt-4o",
    parameters: Optional[Dict[str, Any]] = None
) -> str:
    """
    Get a response from the OpenAI API.
    
    Args:
        message: The user message to send
        system_prompt: The system instructions for the model
        model: The specific OpenAI model to use
        parameters: Additional parameters like temperature, max_tokens

    Returns:
        The model's response text
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in .env file.")
    
    # Set up default parameters
    params = {
        "temperature": 0.7,
        "max_tokens": 1000,
    }
    
    # Update with custom parameters if provided
    if parameters:
        params.update(parameters)
    
    # Initialize client
    client = OpenAI(api_key=api_key)
    
    try:
        # Create chat completion
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=params.get("temperature"),
            max_tokens=params.get("max_tokens")
        )
        
        # Extract and return the text response
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        raise