from pandas import DataFrame
import sys
import io
import traceback
from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.json_helpers import extract_json_from_text
from SimplerLLM.tools.predefined_tools import PREDEFINED_TOOLS



class PandasAgent:
    def __init__(self, llm_instace : LLM, panda_df: DataFrame, verbose : bool = False):

        self.verbose = verbose
        self.llm_instance = llm_instace
        self.panda_df = panda_df
        self.available_actions = {
            "execute_pandas_python_code": {
                "function": self.execute_pandas_python_code,
                "description": """Execute Python code that operates on the provided DataFrame.
                                  Parameters:
                                  input_code (str): A string containing the Python code to be executed.
                                    """
            }
        }
        self.system_prompt_template = """
                You are a professional data analyst, and you are access to a Pandas Dataframe. 
                with access to following Actions:
                
                {actions_list}

                You run in a loop of Thought, Action, PAUSE, Action_Response.
                At the end of the loop you output an Answer.

                Use Thought to understand the question you have been asked.
                Use Action to run one of the actions available to you - then return PAUSE.
                Action_Response will be the result of running those actions.

                To use an action, please use the following format:

                Action:

                {{
                    "function_name": tool_name,
                    "function_parms": {{
                        "param": "value"
                    }}
                }}

                Action_Response: the result of the action.

            
                """.strip()
        


    def execute_pandas_python_code_base(self, input_code):
        """
        Executes a given Python code snippet within the context that includes the provided DataFrame.
        Captures its standard output and returns it along with any errors.

        Parameters:
        input_code (str): A string containing the Python code to be executed.

        Returns:
        tuple: A tuple containing two elements:
            - output (str): Captured standard output of the executed code if successful, None otherwise.
            - error_trace (str): Traceback of the exception if an error occurs, None otherwise.
        """
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        local_vars = {"df": self.panda_df}  # Access the instance's DataFrame

        try:
            wrapped_input_code = f"print({input_code})"
            exec(wrapped_input_code, globals(), local_vars)
            output = new_stdout.getvalue()
        except Exception as e:
            output = "Error occurred: " + str(e) + "\n" + traceback.format_exc()

        sys.stdout = old_stdout
        return output  # Return the output directly so you can see it when calling the method

    def execute_pandas_python_code_base_2(self, input_code):
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        # Setup a controlled local environment
        local_vars = {"df": self.panda_df.copy()}  # Use a copy of the DataFrame to prevent modifications to the original

        # Allow for assignment by including locals in exec
        try:
            wrapped_input_code = f"print({input_code})"
            exec(wrapped_input_code, globals(), local_vars)  # Execute with local_vars as the local context
            output = new_stdout.getvalue()
        except Exception as e:
            output = "Error occurred: " + str(e) + "\n" + traceback.format_exc()

        sys.stdout = old_stdout
        print(output)  # Ensure output is printed for the LLM to read
        return output  # Return the output directly so you can see it when calling the method

    def execute_pandas_python_code(self, input_code):
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        # Setup a controlled local environment
        local_vars = {"df": self.panda_df.copy()}  # Use a copy of the DataFrame to prevent modifications to the original

        try:
            # Dynamically determine whether to use eval (for expressions) or exec (for statements)
            if "=" in input_code or any(keyword in input_code for keyword in ("def ", "class ", "import ", "for ", "while ", "if ")):
                # It's likely a statement if there's an assignment or control structure
                exec(input_code, globals(), local_vars)
                # If exec is used, we typically expect it not to return anything, but let's fetch the last line's result for convenience
                try:
                    last_line = input_code.strip().split('\n')[-1]
                    # If the last line could be an expression, we print its result
                    if not any(keyword in last_line for keyword in ("=", "def ", "class ", "import ", "for ", "while ", "if ")):
                        print(eval(last_line, globals(), local_vars))
                except:
                    pass  # Ignore if the last line isn't a simple expression
            else:
                # Assume it's an expression and directly print its result
                print(eval(input_code, globals(), local_vars))
        except Exception as e:
            print("Error occurred:", str(e), "\n" + traceback.format_exc())

        output = new_stdout.getvalue()
        sys.stdout = old_stdout
        return output  # Return the captured output

    def construct_system_prompt(self):
        actions_description = "\n".join(
            [f"{name}:\n {details['description']}"
             for name, details in self.available_actions.items()]
        )
        return self.system_prompt_template.format(actions_list=actions_description)

    def generate_response(self, user_query, max_turns=5):
        final_response = ""
        react_system_prompt = self.construct_system_prompt()
        messages = [
            {"role": "system", "content": react_system_prompt},
            {"role": "user", "content": user_query}
        ]
        turn_count = 1

        while turn_count <= max_turns:
            if self.verbose:
                print(f"Loop: {turn_count}")
                print("----------------------")

            turn_count += 1

            agent_response = self.llm_instance.generate_response(messages=messages)
            messages.append({"role": "assistant", "content": agent_response})
            final_response = agent_response
            if self.verbose:
                print(agent_response)

            # Extract action JSON from text response.
            action_json = extract_json_from_text(agent_response)
            if action_json:
                if 'function_name' in action_json[0]:
                    function_name = action_json[0]['function_name']
                    function_parms = action_json[0]['function_parms']
                    if function_name not in self.available_actions:
                        raise Exception(f"Unknown action: {function_name}: {function_parms}")
                    if self.verbose:
                        print(f" -- running {function_name} with {function_parms}")
                    action_function = self.available_actions[function_name]["function"]
                    result = action_function(**function_parms)
                    if self.verbose:
                        print("Action_Response:", result)
                    function_result_message = f"Action_Response: {result}"
                    messages.append({"role": "user", "content": function_result_message})
                    if self.verbose:
                        print("----------------------")
                else:
                    break
            else:
                break


        return final_response


