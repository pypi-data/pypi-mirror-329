#import SimplerLLM
from SimplerLLM.language.llm import (
    LLM,
    LLMProvider
)
from SimplerLLM.prompts.messages_template import MessagesTemplate
from SimplerLLM.tools.predefined_tools import load_content

from SimplerLLM.agents_deprecated.core_react_agent import ReActAgent

llm_instance = LLM.create(provider=LLMProvider.OPENAI,
               model_name="gpt-4o")


# Create an agent instance
simple_agent = ReActAgent(llm_instance,verbose=True)

simple_agent.add_tool(load_content)

user_simple_query = "generate a a sentence of 3 words, the reponse should only include the sentence without any addtional text."

user_query = """
Summrize in bullet list the content of the following page: https://learnwithhasan.com/generate-content-ideas-ai/?"""
 
user_query_2 = """

extract the main topic from from the following blog post: https://learnwithhasan.com/generate-content-ideas-ai/

"""


messages = MessagesTemplate()
#messages.add_user_message("Hi")
#messages.add_assistant_message("Hi, how can I help")
messages.add_user_message(user_simple_query)
#history = messages.get_messages()

# Generate a response
response = simple_agent.generate_response(messages=messages,max_turns=5)

#response = simple_agent.generate_response(user_query = user_query)

print(response)