import os
import requests
from typing import List, Dict, Any, Optional, Union, Literal
from dataclasses import dataclass

__all__ = ['ChatMessage', 'OmniClient']

@dataclass
class ChatMessage:
    """Represents a single message in a chat conversation"""
    role: str
    content: str

    def to_dict(self) -> Dict[str, str]:
        """Convert the message to a dictionary format"""
        return {
            "role": self.role,
            "content": self.content
        }

class OmniClient:
    """
    Client for interacting with the OmniRouter API.
    
    This client provides a unified interface to access various LLM models through a single API.
    It supports chat completions, image generation, and smart model selection based on your needs.
    
    Args:
        api_key (str, optional): The API key for authentication. If not provided,
            will attempt to read from OMNI_API_KEY environment variable.
        base_url (str, optional): The base URL for the API. Defaults to https://omni-router.vercel.app/.
    
    Raises:
        ValueError: If no API key is provided or found in environment variables.
    """
    
    DEFAULT_BASE_URL = "https://omni-router.vercel.app/"
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: str = DEFAULT_BASE_URL
    ):
        self._api_key = api_key or os.getenv('OMNI_API_KEY')
        if not self._api_key:
            raise ValueError(
                "No API key provided. Pass it when initializing the client or "
                "set the OMNI_API_KEY environment variable."
            )
            
        self._base_url = base_url.rstrip('/')

    def _make_request(self, endpoint: str, method: str = 'GET', **kwargs) -> Dict[str, Any]:
        """
        Make a request to the API.
        
        Args:
            endpoint (str): The API endpoint to call
            method (str, optional): HTTP method to use. Defaults to 'GET'.
            **kwargs: Additional arguments to pass to requests.request()
            
        Returns:
            Dict[str, Any]: The JSON response from the API
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        headers = {
            'Authorization': f'Bearer {self._api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.request(
            method=method,
            url=f"{self._base_url}/{endpoint.lstrip('/')}",
            headers=headers,
            **kwargs
        )
        
        response.raise_for_status()
        return response.json()

    def get_available_models(self, model_type: Optional[Literal['chat', 'image']] = None) -> List[Dict[str, Any]]:
        """
        Get list of available models from the API.
        
        Args:
            model_type (str, optional): Type of models to get ('chat' or 'image'). 
                                      If None, returns all models.
        
        Returns:
            List[Dict[str, Any]]: List of available models and their information
        """
        endpoint = "v1/models"
        if model_type == 'chat':
            endpoint = "v1/models/chat"
        elif model_type == 'image':
            endpoint = "v1/models/image"
            
        return self._make_request(endpoint)["models"]

    def chat(
        self, 
        messages: Union[List[Dict[str, str]], List[ChatMessage]], 
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Send a chat completion request.
        
        Args:
            messages (Union[List[Dict[str, str]], List[ChatMessage]]): List of messages. Each message
                should have 'role' and 'content' keys, or be a ChatMessage object.
            model (str): The model ID to use
            temperature (float, optional): Sampling temperature. Defaults to 0.7.
            max_tokens (int, optional): Maximum tokens to generate. If None, uses model default.
            stream (bool, optional): Whether to stream the response. Defaults to False.
            
        Returns:
            Dict[str, Any]: The API response containing the chat completion
            
        Example:
            >>> client = APIClient()
            >>> messages = [
            ...     ChatMessage(role="user", content="What is 2+2?")
            ... ]
            >>> response = client.chat(messages, model="gpt-4")
            >>> print(response['content'])
        """
        # Convert ChatMessage objects to dicts if needed
        messages_dict = [
            msg.to_dict() if isinstance(msg, ChatMessage) else msg 
            for msg in messages
        ]
        
        request_data = {
            "model": model,
            "messages": messages_dict,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        return self._make_request(
            endpoint="v1/chat/completions",
            method="POST",
            json=request_data
        )

    def generate_image(
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: Literal["256x256", "512x512", "1024x1024"] = "1024x1024",
        quality: Literal["standard", "hd"] = "standard",
        n: int = 1
    ) -> Dict[str, Any]:
        """
        Generate images from a text prompt.
        
        Args:
            prompt (str): The image generation prompt
            model (str, optional): The model ID to use. Defaults to "dall-e-3".
            size (str, optional): Image size. One of "256x256", "512x512", "1024x1024".
                               Defaults to "1024x1024".
            quality (str, optional): Image quality. One of "standard", "hd".
                                  Defaults to "standard".
            n (int, optional): Number of images to generate. Defaults to 1.
            
        Returns:
            Dict[str, Any]: The API response containing image URLs
            
        Example:
            >>> client = APIClient()
            >>> response = client.generate_image(
            ...     prompt="A beautiful sunset over the ocean",
            ...     size="1024x1024"
            ... )
            >>> print(response['urls'][0])  # URL of the first generated image
        """
        request_data = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "n": n
        }
        
        return self._make_request(
            endpoint="v1/images/generate",
            method="POST",
            json=request_data
        )

    def smart_select(
        self,
        messages: Union[List[Dict[str, str]], List[ChatMessage]],
        k: int = 5,
        model_names: Optional[List[str]] = None,
        rel_cost: float = 0.5,
        rel_latency: float = 0.0,
        rel_accuracy: float = 0.5,
        verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Get model recommendation and completion based on messages and preferences.
        
        This method uses the smart router to select the best model for your task
        and automatically generates a response using that model.
        
        Args:
            messages (Union[List[Dict[str, str]], List[ChatMessage]]): The chat messages to analyze
                for model selection and to generate a response
            k (int, optional): Number of top models to consider. Defaults to 5.
            model_names (List[str], optional): Specific models to select from. Defaults to None.
            rel_cost (float, optional): Relative importance of cost (0-1). Defaults to 0.5.
            rel_latency (float, optional): Relative importance of latency (0-1). Defaults to 0.0.
            rel_accuracy (float, optional): Relative importance of accuracy (0-1). Defaults to 0.5.
            verbose (bool, optional): Whether to return detailed explanation. Defaults to False.
            
        Returns:
            Dict[str, Any]: Contains the selected model, completion response, and optionally
                           the detailed explanation of the selection process
                           
        Example:
            >>> client = APIClient()
            >>> messages = [
            ...     ChatMessage(role="user", content="Solve this calculus problem: ∫x²dx")
            ... ]
            >>> response = client.smart_select(
            ...     messages=messages,
            ...     rel_accuracy=0.8,  # Prioritize accuracy for math
            ...     rel_cost=0.2,
            ...     verbose=True
            ... )
            >>> print(f"Selected model: {response['model']}")
            >>> print(f"Response: {response['content']}")
            >>> if 'explanation' in response:
            ...     print(f"Selection reasoning: {response['explanation']}")
        """
        # Convert ChatMessage objects to dicts if needed
        messages_dict = [
            msg.to_dict() if isinstance(msg, ChatMessage) else msg 
            for msg in messages
        ]
        
        request_data = {
            "messages": messages_dict,
            "k": k,
            "model_names": model_names,
            "rel_cost": rel_cost,
            "rel_latency": rel_latency,
            "rel_accuracy": rel_accuracy,
            "verbose": verbose
        }
        
        return self._make_request(
            endpoint="v1/router/select-model",
            method="POST",
            json=request_data
        )

# Usage example:
# client = APIClient(api_key='your-api-key-here')
# Or using environment variable:
# client = APIClient()