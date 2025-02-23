import asyncio
import random
from typing import List
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from typing import List, Any, Dict, Generic, TypeVar, Callable
from enum import Enum, auto
from SimplerLLM.language.llm import LLM as GenerationLLM, LLMProvider
from test_helpers import get_latest_youtube_comments, post_reply

T = TypeVar('T')

class StepResult(Generic[T]):
    def __init__(self, value: T):
        self.value = value

class YouTubeMethods(Enum):
    GET_LATEST_COMMENTS = auto()
    POST_REPLY = auto()

class LLMMethods(Enum):
    INITIALIZE = auto()
    GENERATE_REPLY = auto()

class BaseStep:
    def __init__(self, name: str):
        self.name = name

    def execute(self, workflow: 'Workflow', item: Any = None) -> Any:
        raise NotImplementedError

class YouTubeStep(BaseStep):
    def __init__(self, name: str, method: YouTubeMethods, **params):
        super().__init__(name)
        self.method = method
        self.params = params

    def execute(self, workflow: 'Workflow', item: Any = None) -> Any:
        if self.method == YouTubeMethods.GET_LATEST_COMMENTS:
            return get_latest_youtube_comments(
                self.params['channel_id'],
                self.params['num_comments']
            )
        elif self.method == YouTubeMethods.POST_REPLY:
            params = {}
            for key, value in self.params.items():
                if callable(value):
                    params[key] = value(item, workflow)
                else:
                    params[key] = value
            return post_reply(**params)

class LLMStep(BaseStep):
    def __init__(self, name: str, method: LLMMethods, **params):
        super().__init__(name)
        self.method = method
        self.params = params

    def execute(self, workflow: 'Workflow', item: Any = None) -> Any:
        if self.method == LLMMethods.INITIALIZE:
            return GenerationLLM.create(**self.params)
        elif self.method == LLMMethods.GENERATE_REPLY:
            llm = workflow.results[self.params['llm']].value
            return llm.generate_response(prompt=f"Generate a 5 words reply to the following comment: {item['comment_text']}")

class LoopStep(BaseStep):
    def __init__(self, name: str, iterable: str, steps: List[BaseStep]):
        super().__init__(name)
        self.iterable = iterable
        self.steps = steps

    def execute(self, workflow: 'Workflow', item: Any = None) -> None:
        for item in workflow.results[self.iterable].value:
            for step in self.steps:
                result = step.execute(workflow, item)
                workflow.results[f"{step.name}_{item['comment_id']}"] = StepResult(result)

class Workflow:
    def __init__(self, name: str):
        self.name = name
        self.steps: List[BaseStep] = []
        self.results: Dict[str, StepResult] = {}

    def add_step(self, step: BaseStep) -> None:
        self.steps.append(step)

    def execute(self) -> None:
        for step in self.steps:
            result = step.execute(self)
            if not isinstance(step, LoopStep):
                self.results[step.name] = StepResult(result)
            print(f"Executed step: {step.name}")

class WorkflowBuilder:
    def __init__(self, name: str):
        self.workflow = Workflow(name)

    def add_step(self, step: BaseStep) -> 'WorkflowBuilder':
        self.workflow.add_step(step)
        return self

    def build(self) -> Workflow:
        return self.workflow



# Create the WorkflowBuilder
my_youtube_workflow = WorkflowBuilder("YouTube Comment Reply")

# Define individual steps
get_comments_step = YouTubeStep("get_latest_comments", YouTubeMethods.GET_LATEST_COMMENTS, channel_id="UC1234567890", num_comments=5)

llm_init_step = LLMStep("initialize_llm", LLMMethods.INITIALIZE, provider=LLMProvider.ANTHROPIC, model_name="claude-3-haiku-20240307")

# Define the steps within the loop
generate_reply_step = LLMStep("generate_reply", LLMMethods.GENERATE_REPLY, llm="initialize_llm")

post_reply_step = YouTubeStep("post_reply", YouTubeMethods.POST_REPLY, 
                              comment_id=lambda item, _: item['comment_id'], 
                              reply=lambda item, workflow: workflow.results[f"generate_reply_{item['comment_id']}"].value)
# Create the loop step
process_comments_loop = LoopStep("process_comments", "get_latest_comments", [generate_reply_step, post_reply_step])

# Add steps to the workflow
my_youtube_workflow.add_step(get_comments_step)
my_youtube_workflow.add_step(llm_init_step)
my_youtube_workflow.add_step(process_comments_loop)

# Build and execute the workflow
youtube_workflow = my_youtube_workflow.build()
youtube_workflow.execute()

