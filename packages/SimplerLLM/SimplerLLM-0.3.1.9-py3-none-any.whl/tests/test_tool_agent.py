#import SimplerLLM
from SimplerLLM.language.llm import (
    LLM,
    LLMProvider
)
from SimplerLLM.prompts.messages_template import MessagesTemplate
from SimplerLLM.tools.predefined_tools import load_content

from SimplerLLM.agents_deprecated.core_tool_calling_agent import ToolCallingAgent

llm_instance = LLM.create(provider=LLMProvider.OPENAI,
               model_name="gpt-4o")


# Create an agent instance
simple_agent = ToolCallingAgent(llm_instance,verbose=False)

simple_agent.add_tool(load_content)

user_simple_query = "generate a a sentence of 3 words, the reponse should only include the sentence without any addtional text."

user_query = """
Extract the content of the following page: https://learnwithhasan.com/generate-content-ideas-ai/?"""
 

messages = MessagesTemplate()
messages.add_user_message("Hi")
messages.add_assistant_message("Hi, how can I help")
messages.add_user_message(user_query)
#history = messages.get_messages()

# Generate a response
response = simple_agent.generate_response_new(messages=messages,execute_tool=False)
#response = simple_agent.generate_response_new(user_query = user_query, execute_tool=False)

print(response)