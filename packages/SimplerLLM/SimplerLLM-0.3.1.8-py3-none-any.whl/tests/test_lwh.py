import requests
import json
from SimplerLLM.language.llm import LLM,LLMProvider
from SimplerLLM.prompts.messages_template import MessagesTemplate

#instance = LLM.create(provider=LLMProvider.LWH, model_name="gpt-4o",user_id="2", api_key="sk-u-2-MRBr03YeQgHPW4Jbytozin8pFuXLmfNdGhOKcDCITAaEsSq6")
instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-4o")

#answer = instance.generate_response(prompt="generate a word", system_prompt="answer in arabic")

#answer = instance.generate_response(prompt="generate a word", system_prompt ="answer in arabic")

template = MessagesTemplate()
template.add_user_message("generate one word")
template.add_assistant_message("dog")
template.add_user_message("longer")
template.add_assistant_message("rain")
template.add_user_message("longer")
messages = template.get_messages()


answer = instance.generate_response(prompt="generate a sentence")



print(answer)


