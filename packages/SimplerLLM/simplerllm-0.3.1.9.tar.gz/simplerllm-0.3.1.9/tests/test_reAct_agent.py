#import SimplerLLM
from SimplerLLM.language.llm import (
    LLM,
    LLMProvider
)
from SimplerLLM.tools.predefined_tools import load_content
from SimplerLLM.agents_deprecated.reAct_agent import ReActAgent

llm_instance = LLM.create(provider=LLMProvider.OPENAI,
               model_name="gpt-4o")


# Create an agent instance
simple_agent = ReActAgent(llm_instance,verbose=True)

simple_agent.add_tool(load_content)

user_simple_query = "generate a a sentence of 3 words, the reponse should only include the sentence without any addtional text."

user_query = """
Generate a bullet point summary for the content of the following page: https://learnwithhasan.com/generate-content-ideas-ai/?"""
 
# Generate a response
response = simple_agent.generate_response(user_query)

print(response)