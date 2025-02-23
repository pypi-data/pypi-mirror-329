import requests
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from SimplerLLM.language.llm import LLM,LLMProvider

instance = LLM.create(provider=LLMProvider.OLLAMA, model_name="Phi-3-mini-4k-instruct-Q8_0")

answer = instance.generate_response(prompt="generate a word", system_prompt="answer in english",full_response=True)

print(answer)


