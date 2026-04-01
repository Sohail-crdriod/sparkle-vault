#!/usr/bin/env python3
"""List available models on OpenRouter"""
import requests
import os

api_key = os.environ.get('OPENROUTER_API_KEY', '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')

print("Fetching available models from OpenRouter...")
print()

response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={"Authorization": f"Bearer {api_key}"}
)

if response.status_code == 200:
    models = response.json().get('data', [])
    
    # Filter for free models
    free_models = [m for m in models if ':free' in m.get('id', '')]
    
    print(f"Found {len(free_models)} FREE models:")
    print("-" * 50)
    for model in free_models[:20]:  # Show first 20
        model_id = model.get('id', 'unknown')
        name = model.get('name', model_id)
        print(f"  {model_id}")
        print(f"    └─ {name[:60]}...")
        print()
    
    if not free_models:
        print("No free models found. Your account may need credits.")
        print()
        print("Showing some popular paid models:")
        for model in models[:10]:
            print(f"  {model.get('id')}")
            
else:
    print(f"Error: {response.status_code}")
    print(response.text)
