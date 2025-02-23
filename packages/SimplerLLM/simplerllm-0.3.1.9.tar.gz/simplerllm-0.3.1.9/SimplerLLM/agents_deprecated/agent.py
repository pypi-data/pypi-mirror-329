from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.json_helpers import extract_json_from_text
from SimplerLLM.tools.predefined_tools import PREDEFINED_TOOLS



class Agent:
    def __init__(self, llm_instace : LLM, verbose : bool = False):
        self.verbose = verbose
        self.llm_instance = llm_instace
        self.available_actions = {}
        self.system_prompt_template = """
                You run in a loop of Thought, Action, PAUSE, Action_Response.
                At the end of the loop you output an Answer.

                Use Thought to understand the question you have been asked.
                Use Action to run one of the actions available to you - then return PAUSE.
                Action_Response will be the result of running those actions.

                Your available actions are:

                {actions_list}

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
        

    # def output_final_answer()


    def add_tool(self, tool_function):
        if tool_function in PREDEFINED_TOOLS.values():
            tool_name = [name for name, func in PREDEFINED_TOOLS.items() if func == tool_function][0]
            description = tool_function.__doc__.strip()
        elif hasattr(tool_function, 'is_custom_tool') and tool_function.is_custom_tool:
            tool_name = tool_function.__name__
            description = tool_function.description
        else:
            raise ValueError("Tool function must be predefined or decorated as a custom tool.")

        self.available_actions[tool_name] = {
            "function": tool_function,
            "description": description
        }



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

        #extract final answer from json
        #answer_json = extract_json_from_text(final_response)
        #answer = final_response.strip().split(":", 1)[1].strip()

        return final_response


