import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.OmniLabs.OmniClient import OmniClient, ChatMessage

@pytest.fixture
def client():
    """Fixture to create an API client instance."""
    return OmniClient(api_key="test-sk1o83e")

def test_get_all_models(client):
    """Test retrieving all available models."""
    all_models = client.get_available_models()
    assert isinstance(all_models, list)
    assert len(all_models) > 0
    print(f"\nAvailable models: {len(all_models)}")

def test_get_chat_models(client):
    """Test retrieving chat models."""
    chat_models = client.get_available_models(model_type='chat')
    assert isinstance(chat_models, list)
    assert len(chat_models) > 0
    print(f"\nAvailable chat models: {len(chat_models)}")
    # Print model names for reference
    for model in chat_models:
        print(f"- {model['id']}")

def test_get_image_models(client):
    """Test retrieving image models."""
    image_models = client.get_available_models(model_type='image')
    assert isinstance(image_models, list)
    assert len(image_models) > 0
    print(f"\nAvailable image models: {len(image_models)}")
    # Print model names for reference
    for model in image_models:
        print(f"- {model['id']}")

@pytest.mark.parametrize("message,expected_length", [
    ("What is 2+2? Answer with just the number.", 10),
    ("Say 'Hello' in French.", 10),
])
def test_chat_completion(client, message, expected_length):
    """Test chat completion with different messages."""
    messages = [ChatMessage(role="user", content=message)]
    
    response = client.chat(
        messages=messages,
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=expected_length
    )
    
    assert "content" in response
    assert "model" in response
    print(f"\nPrompt: {message}")
    print(f"Response: {response['content']}")

@pytest.mark.parametrize("prompt,size,model", [
    ("A simple red circle on white background", "1024x1024", "dall-e-3"),
    ("A blue square on black background", "1024x1024", "dall-e-3"),
])
def test_image_generation(client, prompt, size, model):
    """Test image generation with different prompts."""
    response = client.generate_image(
        prompt=prompt,
        size=size,
        model=model,
        quality="standard",
        n=1
    )
    
    assert "urls" in response
    assert len(response["urls"]) > 0
    print(f"\nPrompt: {prompt}")
    print(f"Generated image URL: {response['urls'][0]}")

@pytest.mark.parametrize("task", [
    {
        "message": "What is the derivative of x^2? Answer in one short sentence.",
        "accuracy": 0.8,
        "cost": 0.2,
        "type": "Math problem"
    },
    {
        "message": "Write a one-line poem about a sunset.",
        "accuracy": 0.3,
        "cost": 0.7,
        "type": "Creative task"
    },
    {
        "message": "Explain quantum computing in simple terms.",
        "accuracy": 0.6,
        "cost": 0.4,
        "type": "Educational task"
    }
])
def test_smart_select(client, task):
    """Test smart model selection with different types of tasks."""
    messages = [ChatMessage(role="user", content=task["message"])]
    
    response = client.smart_select(
        messages=messages,
        rel_accuracy=task["accuracy"],
        rel_cost=task["cost"],
        verbose=True
    )
    
    assert "model" in response
    assert "content" in response
    print(f"\n{task['type']}:")
    print(f"Prompt: {task['message']}")
    print(f"Selected model: {response['model']}")
    print(f"Response: {response['content']}")
    if "explanation" in response:
        print(f"Selection reasoning: {response['explanation']}")

def test_message_format_compatibility(client):
    """Test different message format compatibility."""
    # Test with ChatMessage objects
    messages1 = [ChatMessage(role="user", content="Say 'Hello'")]
    response1 = client.chat(
        messages=messages1,
        model="gpt-3.5-turbo",
        max_tokens=10
    )
    assert "content" in response1
    print(f"\nChatMessage format response: {response1['content']}")
    
    # Test with dict format
    messages2 = [{"role": "user", "content": "Say 'Hi'"}]
    response2 = client.chat(
        messages=messages2,
        model="gpt-3.5-turbo",
        max_tokens=10
    )
    assert "content" in response2
    print(f"Dict format response: {response2['content']}")
