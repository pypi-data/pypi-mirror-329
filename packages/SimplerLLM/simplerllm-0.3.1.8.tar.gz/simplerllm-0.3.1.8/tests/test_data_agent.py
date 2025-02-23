#import SimplerLLM
from SimplerLLM.language.llm import (
    LLM,
    LLMProvider
)
from SimplerLLM.tools.predefined_tools import generate_final_answer
from SimplerLLM.tools.predefined_tools import execute_pandas_python_code


from SimplerLLM.agents_deprecated.pandas_agent_exp import PandasAgent
import pandas as pd

df = pd.read_csv("test.csv").fillna(value = 0)

# Test function
  # Import your function if it's in another file

#Test Code 1: A simple operation that should succeed
# code1 = "print(df.shape[0])"
# output1, error1 = execute_pandas_python_code(code1, df)
# print("Output 1:", output1)
# print("Error 1:", error1)



llm_instance = LLM.create(provider=LLMProvider.OPENAI,
               model_name="gpt-4")

# # Create an agent instance
simple_agent = PandasAgent(llm_instance,panda_df=df,verbose=True)

#result = simple_agent.execute_pandas_python_code("df.shape[0]")
#print(result)


user_simple_query = "how many records are there in this dataset"
another_query = "How may patients were hospitalized during July 2020"
third_query = "generate 10 important questions to start with to analyze the data"
query = "Are there any missing values in the dataset? If so, how many in each column?"
query2 = "Are there any obvious correlations between any two variables/columns in the dataset?"




CSV_PROMPT_PREFIX = """
First set the pandas display options to show all the columns,
get the column names, then answer the question.
"""

CSV_PROMPT_SUFFIX = """
- **ALWAYS** before giving the Final Answer, try another method.
Then reflect on the answers of the two methods you did and ask yourself
if it answers correctly the original question.
If you are not sure, try another method.
- If the methods tried do not give the same result,reflect and
try again until you have two methods that have the same result.
- If you still cannot arrive to a consistent result, say that
you are not sure of the answer.
- If you are sure of the correct answer, create a beautiful
and thorough response using Markdown.
- **DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE,
ONLY USE THE RESULTS OF THE CALCULATIONS YOU HAVE DONE**.
- **ALWAYS**, as part of your "Final Answer", explain how you got
to the answer on a section that starts with: "\n\nExplanation:\n".
In the explanation, mention the column names that you used to get
to the final answer.
"""

QUESTION = "How may patients were hospitalized during July 2020" 
"in Texas, and nationwide as the total of all states?"
"Use the hospitalizedIncrease column" 



# # Generate a response
response = simple_agent.generate_response(query2)
print(response)