from SimplerLLM.tools.generic_loader import load_content
from SimplerLLM.tools.python_func import execute_python_code
from SimplerLLM.tools.pandas_func import execute_pandas_python_code


def agent_final_answer_tool(
    answer: str,
    source: str
):
    """Returns a natural language response to the user in `answer`, and a
    `source` which provides citations for where this information came from.
    """
    return ""

def generate_final_answer(
    input_conversation: str,
):
    """Returns the final response based on the input_conversation without any additions in JSON Format like this:

    {
        answser: the answer goes here.
    }

    """
    return ""


# List of predefined tools
PREDEFINED_TOOLS = {
    "load_content": load_content,
    "execute_python_code": execute_python_code,
    "agent_final_answer_tool": agent_final_answer_tool,
    "generate_final_answer": generate_final_answer,
    "execute_pandas_python_code": execute_pandas_python_code
}