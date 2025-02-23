#import SimplerLLM
from SimplerLLM.language.llm import (
    LLM,
    LLMProvider
)
from SimplerLLM.tools.predefined_tools import load_content


llm_instance = LLM.create(provider=LLMProvider.OPENAI,
               model_name="gpt-4o")

prompt = """convert the following user prompt into the best 2-3
 keyword max search query to search google for and get the best
   relevant search results to the user prompt.
   
   user prompt: {user_input}
   
   """


query_1 = """
what is the best place to buy 9D VR Motion Machine
 to put in my home for my kids to play with"""

query_2 = """
what is the best place to buy 9D VR Motion Machine
 to put in my home for my kids to play with
   knowing that I live in the middle east"""



input_prompt = prompt.format(user_input = query_2)

response = llm_instance.generate_response(prompt=input_prompt)

print(response)


