#import SimplerLLM
from SimplerLLM.language.llm import (
    LLM,
    LLMProvider
)
from SimplerLLM.prompts.messages_template import MessagesTemplate
from SimplerLLM.tools.predefined_tools import load_content

from SimplerLLM.agents_deprecated.core_reflection_agent import ReflectionAgent

llm_instance = LLM.create(provider=LLMProvider.OPENAI,
               model_name="gpt-4o")


# Create an agent instance
simple_agent = ReflectionAgent(llm_instance,verbose=True)

user_simple_query = "I want a plan to host a streamlit app on ununtu server, step by step, dont miss any detail"

messages = MessagesTemplate()
messages.add_user_message(user_simple_query)

# Generate a response
response = simple_agent.generate_response(messages=messages,max_turns=5)

print(response)