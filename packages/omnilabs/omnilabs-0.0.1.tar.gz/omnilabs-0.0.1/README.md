# OmniLabs Python Client

[![Website](https://img.shields.io/badge/website-omnilabs--ai-blue)](https://omnilabs-ai.github.io)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Python client for the OmniRouter API that provides unified access to various LLM models through a single interface. This client supports chat completions, image generation, and smart model selection capabilities.

## Installation

```bash
pip install omnilabs
```

## Quick Start

```python
from omnilabs import OmniClient, ChatMessage

# Initialize the client
client = OmniClient()  # API key can be set via OMNI_API_KEY environment variable
# Or provide the API key directly
client = OmniClient(api_key="your-api-key")

# Simple chat completion
messages = [
    ChatMessage(role="user", content="What is the capital of France?")
]
response = client.chat(messages, model="gpt-4")

# Generate an image
image_response = client.generate_image(
    prompt="A serene landscape with mountains at sunset",
    model="dall-e-3",
    size="1024x1024"
)

# Smart model selection
smart_response = client.smart_select(
    messages=messages,
    k=5,  # Get top 5 recommended models
    rel_cost=0.5,
    rel_accuracy=0.5
)
```

## Features

### 1. Chat Completions
- Support for various chat models (e.g., GPT-4, Claude, etc.)
- Customizable parameters like temperature and max tokens
- Streaming support for real-time responses

### 2. Image Generation
- Support for models like DALL-E 3
- Multiple size options: 256x256, 512x512, 1024x1024
- Quality settings: standard and HD

### 3. Smart Model Selection
- Intelligent model recommendations based on your requirements
- Balance between cost, latency, and accuracy
- Customizable weights for different factors

## API Reference

### ChatMessage Class
```python
ChatMessage(role: str, content: str)
```
Represents a single message in a chat conversation.

### OmniClient Class
```python
OmniClient(api_key: Optional[str] = None, base_url: str = "https://omni-router.vercel.app/")
```

#### Methods:

1. `chat(messages, model, temperature=0.7, max_tokens=None, stream=False)`
   - Send chat messages and get completions
   - Supports streaming for real-time responses

2. `generate_image(prompt, model="dall-e-3", size="1024x1024", quality="standard", n=1)`
   - Generate images from text prompts
   - Multiple size and quality options

3. `smart_select(messages, k=5, model_names=None, rel_cost=0.5, rel_latency=0.0, rel_accuracy=0.5)`
   - Get model recommendations based on your requirements
   - Customize importance of cost, latency, and accuracy

4. `get_available_models(model_type=None)`
   - List available models
   - Optional filtering by model type ('chat' or 'image')

## Environment Variables

- `OMNI_API_KEY`: Your OmniLabs API key

## Error Handling

The client includes proper error handling for common scenarios:
- Invalid API keys
- Network issues
- Rate limiting
- Invalid parameters

## Contributing

We welcome contributions! Please check our [GitHub repository](https://github.com/omnilabs-ai) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [https://omnilabs-ai.github.io](https://omnilabs-ai.github.io)
- Issues: [GitHub Issues](https://github.com/omnilabs-ai)