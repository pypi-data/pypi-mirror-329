

#add more modules and test different scenerios


import ast
import base64
import dill
import importlib
from typing import List, Dict, Any, Callable
import json
import inspect
import os






class Step:
    def __init__(self, name: str, function: callable, params: dict):
        self.name = name
        self.function = function
        self.params = params

class Condition:
    def __init__(self, condition: callable, if_true: list, if_false: list):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

class Loop:
    def __init__(self, iterable, steps: list):
        self.iterable = iterable
        self.steps = steps

class Workflow:
    def __init__(self, name, available_functions=None):
        self.name = name
        self.steps = []
        self.results = {}
        self.loop_results = {}
        self.available_functions = available_functions or {}

    def add_step(self, step):
        self.steps.append(step)

    def _execute_step(self, step, item=None):
        print(f"Executing step: {step.name}")
        print(f"Item: {item}")
        print(f"Step params: {step.params}")
        
        params = {}
        for k, v in step.params.items():
            if callable(v):
                sig = inspect.signature(v)
                if 'item' in sig.parameters and item is not None:
                    params[k] = v(item)
                else:
                    params[k] = v()
            elif isinstance(v, str) and v.startswith('results.'):
                parts = v.split('.')
                if len(parts) == 2 and parts[1] in self.results:
                    params[k] = self.results[parts[1]]
                elif len(parts) == 2 and parts[1] in self.loop_results:
                    params[k] = self.loop_results[parts[1]]
                else:
                    raise ValueError(f"Invalid results reference: {v}")
            else:
                params[k] = v
        
        sig = inspect.signature(step.function)
        if 'item' in sig.parameters and item is not None:
            params['item'] = item
        
        print(f"Params being passed to function: {params}")
        return step.function(**params)

    def execute(self):
        for step in self.steps:
            if isinstance(step, Step):
                result = self._execute_step(step)
                self.results[step.name] = result
                print(f"Executed step: {step.name}")
            elif isinstance(step, Condition):
                if step.condition():
                    for sub_step in step.if_true:
                        self._execute_step(sub_step)
                else:
                    for sub_step in step.if_false:
                        self._execute_step(sub_step)
            elif isinstance(step, Loop):
                print(f"Executing Loop step")
                self.loop_results.clear()
                if isinstance(step.iterable, str) and step.iterable.startswith('results.'):
                    iterable = self.results[step.iterable.split('.')[1]]
                else:
                    iterable = step.iterable() if callable(step.iterable) else step.iterable
                print(f"Loop iterable: {iterable}")
                for item in iterable:
                    print(f"Loop item: {item}")
                    for sub_step in step.steps:
                        result = self._execute_step(sub_step, item=item)
                        self.loop_results[sub_step.name] = result
                    self.results[f"{step.steps[-1].name}_results"] = self.loop_results.copy()

    def to_json(self):
        def step_to_dict(step):
            if isinstance(step, Step):
                return {
                    'type': 'Step',
                    'name': step.name,
                    'function': self._serialize_function(step.function),
                    'params': {k: self._serialize_param(v) for k, v in step.params.items()}
                }
            elif isinstance(step, Condition):
                return {
                    'type': 'Condition',
                    'condition': self._serialize_function(step.condition),
                    'if_true': [step_to_dict(s) for s in step.if_true],
                    'if_false': [step_to_dict(s) for s in step.if_false]
                }
            elif isinstance(step, Loop):
                return {
                    'type': 'Loop',
                    'iterable': self._serialize_function(step.iterable),
                    'steps': [step_to_dict(s) for s in step.steps]
                }

        workflow_dict = {
            'name': self.name,
            'steps': [step_to_dict(step) for step in self.steps]
        }
        return json.dumps(workflow_dict, indent=2)

    def _serialize_function(self, func):
        if callable(func):
            if func.__name__ == '<lambda>':
                return f"LAMBDA:{inspect.getsource(func).strip()}"
            return f"FUNCTION:{func.__module__}.{func.__name__}"
        return func

    def _serialize_param(self, param):
        if callable(param):
            return self._serialize_function(param)
        return param

    @classmethod
    def from_json(cls, json_str: str, available_functions=None):
        workflow_dict = json.loads(json_str)
        workflow = cls(workflow_dict['name'], available_functions)
        
        def resolve_function(func_str, workflow_instance):
            if isinstance(func_str, str):
                if func_str.startswith("LAMBDA:"):
                    lambda_code = func_str[7:]
                    # Create a function that will return the lambda
                    lambda_creator = f"def create_lambda(workflow, funcs):\n    return {lambda_code}"
                    # Execute the lambda creator function
                    exec(lambda_creator, globals())
                    # Call the creator function with the workflow instance and available functions
                    return globals()['create_lambda'](workflow_instance, workflow_instance.available_functions)
                elif func_str.startswith("FUNCTION:"):
                    module_name, func_name = func_str[9:].rsplit('.', 1)
                    module = importlib.import_module(module_name)
                    return getattr(module, func_name)
                elif func_str.startswith("results."):
                    parts = func_str.split('.')
                    if len(parts) == 2 and parts[1] in workflow_instance.results:
                        return workflow_instance.results[parts[1]]
                elif '.' in func_str:
                    module_name, func_name = func_str.rsplit('.', 1)
                    if module_name == '__main__':
                        if func_name in workflow_instance.available_functions:
                            return workflow_instance.available_functions[func_name]
                        else:
                            raise ValueError(f"Function '{func_name}' not found in available functions")
                    else:
                        module = importlib.import_module(module_name)
                        return getattr(module, func_name)
                elif func_str in workflow_instance.available_functions:
                    return workflow_instance.available_functions[func_str]
                else:
                    raise ValueError(f"Function '{func_str}' not found in available functions")
            return func_str

        def resolve_params(params, workflow_instance):
            resolved_params = {}
            for k, v in params.items():
                if isinstance(v, str) and v.startswith("LAMBDA:"):
                    try:
                        lambda_dict = json.loads(v[7:])
                        resolved_params[k] = {key: resolve_function(f"LAMBDA:{value}", workflow_instance) if isinstance(value, str) and value.startswith("lambda") else value for key, value in lambda_dict.items()}
                    except json.JSONDecodeError:
                        # If it's not a JSON string, treat it as a single lambda
                        resolved_params[k] = resolve_function(v, workflow_instance)
                else:
                    resolved_params[k] = resolve_function(v, workflow_instance)
            return resolved_params

        def dict_to_step(step_dict):
            if step_dict['type'] == 'Step':
                return Step(
                    step_dict['name'],
                    resolve_function(step_dict['function'], workflow),
                    resolve_params(step_dict['params'], workflow)
                )
            elif step_dict['type'] == 'Condition':
                return Condition(
                    resolve_function(step_dict['condition'], workflow),
                    [dict_to_step(s) for s in step_dict['if_true']],
                    [dict_to_step(s) for s in step_dict['if_false']]
                )
            elif step_dict['type'] == 'Loop':
                return Loop(
                    resolve_function(step_dict['iterable'], workflow),
                    [dict_to_step(s) for s in step_dict['steps']]
                )

        workflow.steps = [dict_to_step(step) for step in workflow_dict['steps']]
        return workflow
    

    def export_to_file(self, filename: str):
        """
        Export the workflow to a JSON file.
        
        :param filename: The name of the file to save the workflow to.
        """
        with open(filename, 'w') as f:
            json.dump(json.loads(self.to_json()), f, indent=2)
        print(f"Workflow exported to {filename}")

    @classmethod
    def import_from_file(cls, filename: str, available_functions=None):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file {filename} does not exist.")
        
        with open(filename, 'r') as f:
            json_str = f.read()
        
        return cls.from_json(json_str, available_functions)