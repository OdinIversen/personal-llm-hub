from typing import Dict, Any, Optional, Protocol

class LLMProvider(Protocol):
    """Protocol defining the interface for all LLM providers."""
    
    def get_response(
        message: str,
        system_prompt: str,
        model: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Get a response from the LLM provider.
        
        Args:
            message: The user message to send
            system_prompt: The system instructions for the model
            model: The specific model to use
            parameters: Additional parameters like temperature, max_tokens

        Returns:
            The model's response text
        """
        ...