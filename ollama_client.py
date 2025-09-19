import requests
import json
from typing import Dict, Any, Optional

class OllamaClient:
    """Client for communicating with local Ollama models."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "qwen2.5-coder:7b"  # Default model

    def set_model(self, model_name: str) -> None:
        """Set the model to use for completions."""
        self.model = model_name

    def generate(self, prompt: str, system_prompt: str = "", max_tokens: int = 1000, temperature: float = 0.0) -> str:
        """
        Generate a completion using the local Ollama model.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation (0.0 = deterministic)

        Returns:
            Generated text response
        """
        try:
            # Build the full prompt with system message if provided
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temperature,
                    "top_k": 40,
                    "top_p": 0.9,
                }
            }

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                return f"ERROR: Ollama request failed with status {response.status_code}: {response.text}"

        except requests.exceptions.RequestException as e:
            return f"ERROR: Failed to connect to Ollama: {e}"
        except json.JSONDecodeError as e:
            return f"ERROR: Failed to parse Ollama response: {e}"
        except Exception as e:
            return f"ERROR: Unexpected error: {e}"

    def chat(self, messages: list, max_tokens: int = 1000, temperature: float = 0.0) -> str:
        """
        Chat completion using Ollama's chat endpoint.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation

        Returns:
            Generated response
        """
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temperature,
                    "top_k": 40,
                    "top_p": 0.9,
                }
            }

            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "").strip()
            else:
                return f"ERROR: Ollama chat request failed with status {response.status_code}: {response.text}"

        except requests.exceptions.RequestException as e:
            return f"ERROR: Failed to connect to Ollama: {e}"
        except json.JSONDecodeError as e:
            return f"ERROR: Failed to parse Ollama response: {e}"
        except Exception as e:
            return f"ERROR: Unexpected error: {e}"

    def check_model(self) -> bool:
        """Check if the current model is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                available_models = [model.get("name", "") for model in models]
                return self.model in available_models
            return False
        except Exception:
            return False

    def list_models(self) -> list:
        """List all available models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model.get("name", "") for model in models]
            return []
        except Exception:
            return []

    def health_check(self) -> bool:
        """Check if Ollama server is running and responsive."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

def create_ollama_call(system_prompt: str = "") -> callable:
    """
    Create a function that mimics the anthropic_call interface but uses Ollama.

    Args:
        system_prompt: Optional system prompt to use for all calls

    Returns:
        Function that takes a prompt and returns a response
    """
    client = OllamaClient()

    def ollama_call(prompt: str) -> str:
        """Call Ollama with the given prompt."""
        return client.generate(prompt, system_prompt=system_prompt)

    return ollama_call

# Test function
def test_ollama_connection():
    """Test the Ollama connection and model availability."""
    client = OllamaClient()

    print("🔍 Testing Ollama connection...")

    # Health check
    if not client.health_check():
        print("❌ Ollama server is not running or not accessible")
        return False

    print("✅ Ollama server is running")

    # List models
    models = client.list_models()
    print(f"📋 Available models: {models}")

    # Check if our default model exists
    if not client.check_model():
        print(f"❌ Default model '{client.model}' not found")
        if models:
            print(f"💡 Available models: {', '.join(models)}")
            # Try to use the first available model
            client.set_model(models[0])
            print(f"🔄 Switched to model: {models[0]}")
        else:
            print("❌ No models available")
            return False
    else:
        print(f"✅ Model '{client.model}' is available")

    # Test generation
    print("🧪 Testing generation...")
    test_response = client.generate("Say 'Hello from Ollama!' and nothing else.")
    print(f"🤖 Response: {test_response}")

    if "ERROR" in test_response:
        print("❌ Generation test failed")
        return False

    print("✅ Ollama is working correctly!")
    return True

if __name__ == "__main__":
    test_ollama_connection()