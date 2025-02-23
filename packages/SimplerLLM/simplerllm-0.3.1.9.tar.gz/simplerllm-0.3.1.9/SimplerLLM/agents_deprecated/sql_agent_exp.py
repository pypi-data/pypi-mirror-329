import sys
import io
import traceback
import mysql.connector
from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.json_helpers import extract_json_from_text
from SimplerLLM.tools.predefined_tools import PREDEFINED_TOOLS

class SQLAgent:
    def __init__(self, llm_instance: LLM, db_config: dict, verbose: bool = False):
        self.verbose = verbose
        self.llm_instance = llm_instance
        self.db_config = db_config
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
        self.available_actions = {
            "execute_sql_code": {
                "function": self.execute_sql_code,
                "description": """Execute SQL queries on the connected MySQL database.
                                  Parameters:
                                  query (str): A string containing the SQL query to be executed.
                                  """
            },
            "generate_final_answer": {
                "function": self.generate_final_answer,
                "description": """Returns the final response based on the input_conversation without any additions in JSON Format like this:
                                        {
                                            answser: the answer goes here.
                                        }

                                     Parameters:
                                     input_answer (str): A string containing the answer.
                                """
            }

        }
        self.system_prompt_template = """
                You are a professional data analyst, and you have access to a MySQL database. 

                Always get the database structure first to know what tables to query.

                ONLY Use Select, Never update the data!

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

                Full Answer:
            
                """.strip()

    def execute_sql_code(self, query):
        with mysql.connector.connect(**self.db_config) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    return result
                except mysql.connector.Error as e:
                    return f"SQL Error occurred: {e}"
                except Exception as e:
                    return f"Error occurred: {str(e)}\n" + traceback.format_exc()
                
    def generate_final_answer(
        self,
        input_answer: str,
    ):
        """Returns the final response based on the input_answer without any additions in JSON Format like this:

        {
            answser: the answer goes here.
        }

        """
        return ""

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
                        raise Exception(f"Unknown action: {function_name}")
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

    # def __del__(self):
    #     try:
    #         if self.cursor:
    #             self.cursor.close()
    #     except Exception as e:
    #         print(f"Failed to close cursor: {e}")
    #     try:
    #         if self.connection:
    #             self.connection.close()
    #     except Exception as e:
    #         print(f"Failed to close connection: {e}")