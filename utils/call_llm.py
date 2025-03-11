import os
import requests
from dotenv import load_dotenv
import streamlit as st

# Try to load from .env file for local development
load_dotenv()

def call_llm(prompt, system_prompt=None, model="deepseek/deepseek-r1-zero:free"):
    """
    Call the LLM using OpenRouter API.
    
    Args:
        prompt (str): The user prompt
        system_prompt (str, optional): System prompt to guide the model
        model (str, optional): Model to use, defaults to DeepSeek R1 Zero
        
    Returns:
        str: The model's response
    """
    # Try to get API key from Streamlit secrets first (for deployment)
    try:
        api_key = st.secrets["api_keys"]["openrouter"]
    except:
        # Fall back to environment variable (for local development)
        api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("OpenRouter API key not found. Please set OPENROUTER_API_KEY in .env file or add to Streamlit secrets.")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # Add user message
    messages.append({"role": "user", "content": prompt})
    
    data = {
        "model": model,
        "messages": messages
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )
    
    if response.status_code != 200:
        raise Exception(f"Error calling OpenRouter API: {response.text}")
    
    return response.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    # Test the function
    prompt = "What is the meaning of life?"
    system_prompt = "You are a helpful assistant."
    try:
        response = call_llm(prompt, system_prompt)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")