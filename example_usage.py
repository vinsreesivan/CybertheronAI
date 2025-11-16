"""
Example usage of the Multi-LLM Fusion API

This script demonstrates how to use the API programmatically.
Make sure the server is running before executing this script.
"""

import requests
import json
from typing import Dict, Any


class LLMFusionClient:
    """Simple client for the Multi-LLM Fusion API"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def health_check(self) -> Dict[str, Any]:
        """Check if the server is healthy"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

    def query(self, prompt: str, strategy: str = "refiner") -> Dict[str, Any]:
        """Query multiple LLMs and get fused response"""
        response = requests.post(
            f"{self.base_url}/query",
            json={"prompt": prompt, "strategy": strategy}
        )
        response.raise_for_status()
        return response.json()

    def get_config(self) -> Dict[str, Any]:
        """Get current server configuration"""
        response = requests.get(f"{self.base_url}/config")
        response.raise_for_status()
        return response.json()

    def list_models(self) -> Dict[str, Any]:
        """List available models"""
        response = requests.get(f"{self.base_url}/models")
        response.raise_for_status()
        return response.json()


def main():
    """Example usage"""

    # Initialize client
    client = LLMFusionClient()

    print("=" * 60)
    print("Multi-LLM Fusion - Example Usage")
    print("=" * 60)
    print()

    # 1. Health check
    print("1. Checking server health...")
    try:
        health = client.health_check()
        print(f"   ✅ Status: {health['status']}")
        print(f"   ✅ Models: {', '.join(health['models'])}")
        print(f"   ✅ Strategy: {health['fusion_strategy']}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error: Server not accessible. Is it running?")
        print(f"   Details: {e}")
        return

    print()

    # 2. List models
    print("2. Listing available models...")
    models = client.list_models()
    for model in models['models']:
        status = "✅ enabled" if model['enabled'] else "⏸️  disabled"
        print(f"   - {model['name']}: {status}")

    print()

    # 3. Example query - Factual question
    print("3. Example Query #1: Factual Question")
    print("-" * 60)
    prompt1 = "What are the main differences between Python and JavaScript?"
    print(f"Prompt: {prompt1}")
    print()

    result1 = client.query(prompt1, strategy="refiner")

    print("Refined Answer:")
    print(result1['fused_response'])
    print()
    print(f"Stats: {result1['total_time']}s | "
          f"{result1['successful_responses']}/{result1['models_queried']} models")
    print()

    # 4. Example query - Creative question
    print("4. Example Query #2: Creative Question (Consensus)")
    print("-" * 60)
    prompt2 = "Give me 3 creative project ideas combining AI and sustainability"
    print(f"Prompt: {prompt2}")
    print()

    result2 = client.query(prompt2, strategy="consensus")

    print("Consensus Answer:")
    print(result2['fused_response'])
    print()
    print(f"Stats: {result2['total_time']}s | "
          f"{result2['successful_responses']}/{result2['models_queried']} models")
    print()

    # 5. Show individual model responses
    print("5. Individual Model Responses (from Query #1):")
    print("-" * 60)
    for resp in result1['individual_responses']:
        print(f"\n{resp['model_name']} ({resp['time_taken']}s):")
        if resp['error']:
            print(f"   ❌ Error: {resp['error']}")
        else:
            # Print first 200 chars
            preview = resp['response'][:200] + "..." if len(resp['response']) > 200 else resp['response']
            print(f"   {preview}")

    print()
    print("=" * 60)
    print("Done! Check the API docs at http://localhost:8000/docs")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the server is running: python main.py")
