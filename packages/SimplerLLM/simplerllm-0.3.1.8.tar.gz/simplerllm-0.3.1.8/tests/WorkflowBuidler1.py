# Notes:
# Add Debug to see outputs on each step
# See if we can make 'comment_id' and 'comment_id' intelicence, on all outputs of functions
# Add logging and verbose with coloring
# Export and Import Workflows
# test with new functions
# add retry logic for each step, stop the workflow on error, report (email)
# add waits
# test parallel exection
# make it async
# monitor workflow execution (UI ?)
# call the workflow with API endpoint - webhook


import asyncio
from typing import List
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from SimplerLLM.language.llm import LLM as GenerationLLM, LLMProvider
from test_helpers import get_latest_youtube_comments, post_reply



from dataclasses import dataclass, field
from typing import Optional, Callable, Any
import asyncio
from typing import List, Any, Dict, TypeVar, Callable
from enum import Enum, auto


T = TypeVar('T')

class YouTubeMethods(Enum):
    GET_LATEST_COMMENTS = auto()
    POST_REPLY = auto()

class LLMMethods(Enum):
    INITIALIZE = auto()
    GENERATE_REPLY = auto()

class StepIO:
    def __init__(self, data: Any, metadata: Dict[str, Any] = None):
        self.data = data
        self.metadata = metadata or {}

class BaseStep:
    def __init__(self, name: str):
        self.name = name
        self.input_key = None
        self.output_key = None

    def execute(self, input: StepIO, workflow: 'Workflow') -> StepIO:
        raise NotImplementedError

class DataFlow:
    def __init__(self):
        self.data = {}

    def set(self, key: str, value: Any):
        self.data[key] = value

    def get(self, key: str) -> Any:
        return self.data.get(key)

class Workflow:
    def __init__(self, name: str):
        self.name = name
        self.steps = []
        self.data_flow = DataFlow()
        self.step_outputs = {}  # New dictionary to store step outputs

    def execute(self):
        for step in self.steps:
            try:
                input_data = self.data_flow.get(step.input_key)
                output = step.execute(StepIO(input_data), self)
                self.data_flow.set(step.output_key, output.data)
                self.step_outputs[step.name] = output  # Store the output
                print(f"Executed step: {step.name}")
            except Exception as e:
                print(f"Error executing step {step.name}: {str(e)}")
                # Implement error handling strategy (e.g., skip, retry, or abort)

    def get_step_output(self, step_name: str) -> StepIO:
        return self.step_outputs.get(step_name)



@dataclass
class YouTubeStep(BaseStep):
    name: str
    method: YouTubeMethods
    channel_id: Optional[str] = None
    num_comments: int = 5
    comment_id: Optional[str | Callable[[StepIO, Workflow], str]] = None
    reply: Optional[str | Callable[[StepIO, Workflow], str]] = None
    additional_params: dict = field(default_factory=dict)

    def __post_init__(self):
        super().__init__(self.name)

    def execute(self, input: StepIO, workflow: Workflow) -> StepIO:
        if self.method == YouTubeMethods.GET_LATEST_COMMENTS:
            channel_id = self.channel_id or self.additional_params.get('channel_id')
            num_comments = self.num_comments
            comments = get_latest_youtube_comments(channel_id, num_comments)
            return StepIO(comments)
        elif self.method == YouTubeMethods.POST_REPLY:
            comment_id = self._resolve_param(self.comment_id, input, workflow) or input.metadata.get('comment_id')
            reply = self._resolve_param(self.reply, input, workflow) or input.data
            result = post_reply(comment_id, reply)
            return StepIO(result)
        else:
            raise ValueError(f"Unknown method: {self.method}")

    def _resolve_param(self, param, input: StepIO, workflow: Workflow):
        if callable(param):
            return param(input, workflow)
        return param


        
@dataclass
class LLMStep(BaseStep):
    name: str
    method: LLMMethods
    provider: Optional[LLMProvider] = None
    model_name: Optional[str] = None
    llm_key: Optional[str] = None
    prompt: Optional[str | Callable[[StepIO, Workflow], str]] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    additional_params: dict = field(default_factory=dict)

    def execute(self, input: StepIO, workflow: Workflow) -> StepIO:
        if self.method == LLMMethods.INITIALIZE:
            llm = GenerationLLM.create(
                provider=self.provider,
                model_name=self.model_name,
                **self.additional_params
            )
            return StepIO(llm)
        elif self.method == LLMMethods.GENERATE_REPLY:
            llm = workflow.data_flow.get(self.llm_key)
            if llm is None:
                raise ValueError(f"LLM not found: {self.llm_key}")
            
            prompt = self.prompt
            if callable(prompt):
                prompt = prompt(input, workflow)
            
            response = llm.generate_response(
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                **self.additional_params
            )
            return StepIO(response)
        else:
            raise ValueError(f"Unknown method: {self.method}")

class LoopStep(BaseStep):
    def __init__(self, name: str, steps: List[BaseStep]):
        super().__init__(name)
        self.steps = steps

    def execute(self, input: StepIO, workflow: Workflow) -> StepIO:
        results = []
        for item in input.data:
            item_result = {}
            for step in self.steps:
                step_input = StepIO(item_result.get(step.input_key), metadata=item)
                step_output = step.execute(step_input, workflow)
                item_result[step.output_key] = step_output.data
            results.append(item_result)
        return StepIO(results)

class ConditionalStep(BaseStep):
    def __init__(self, name: str, condition: Callable[[StepIO], bool], true_step: BaseStep, false_step: BaseStep):
        super().__init__(name)
        self.condition = condition
        self.true_step = true_step
        self.false_step = false_step

    def execute(self, input: StepIO, workflow: Workflow) -> StepIO:
        if self.condition(input):
            return self.true_step.execute(input, workflow)
        else:
            return self.false_step.execute(input, workflow)

class ParallelSteps(BaseStep):
    def __init__(self, name: str, steps: List[BaseStep]):
        super().__init__(name)
        self.steps = steps

    async def execute_step(self, step: BaseStep, input: StepIO, workflow: Workflow) -> StepIO:
        return step.execute(input, workflow)

    def execute(self, input: StepIO, workflow: Workflow) -> StepIO:
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(self.execute_step(step, input, workflow)) for step in self.steps]
        results = loop.run_until_complete(asyncio.gather(*tasks))
        return StepIO(results)

class WorkflowBuilder:
    def __init__(self, name: str):
        self.workflow = Workflow(name)

    def add_step(self, step: BaseStep, input_key: str = None, output_key: str = None):
        step.input_key = input_key
        step.output_key = output_key or step.name
        self.workflow.steps.append(step)
        return self

    def add_conditional(self, conditional_step: ConditionalStep):
        return self.add_step(conditional_step)

    def add_parallel(self, parallel_step: ParallelSteps):
        return self.add_step(parallel_step)

    def add_loop(self, loop_step: LoopStep, input_key: str = None):
        return self.add_step(loop_step, input_key=input_key)

    def build(self) -> Workflow:
        return self.workflow

    def print_step_output(self, step_name: str):
        output = self.workflow.get_step_output(step_name)
        if output:
            print(f"\nOutput of step '{step_name}':")
            print(output.data)
        else:
            print(f"No output found for step '{step_name}'")


# Example usage
if __name__ == "__main__":
    # Create the WorkflowBuilder
    my_youtube_workflow = WorkflowBuilder("YouTube Comment Reply")

    # Define individual steps
    get_comments_step = YouTubeStep(
        name="get_comments",
        method=YouTubeMethods.GET_LATEST_COMMENTS,
        channel_id="UC1234567890",
        num_comments=5
    )    

    # Initialize LLM
    init_llm_step = LLMStep(
        name="init_llm",
        method=LLMMethods.INITIALIZE,
        provider=LLMProvider.ANTHROPIC,
        model_name="claude-3-haiku-20240307"
    )

    # Generate reply
    generate_reply_step = LLMStep(
        name="generate_reply",
        method=LLMMethods.GENERATE_REPLY,
        llm_key="init_llm",
        prompt=lambda input, workflow: f"Generate a 5 words reply to the following comment: {input.metadata.get('comment_text', '')}",
        temperature=0.8,
        max_tokens=300
    )



    post_reply_step = YouTubeStep(
        name="post_reply",
        method=YouTubeMethods.POST_REPLY,
        comment_id=lambda input, workflow: input.metadata.get('comment_id'),
        reply=lambda input, workflow: input.data
    )



    
    # Define a condition function
    def should_reply(input: StepIO) -> bool:
        return len(input.metadata.get('comment_text', '')) > 10

    # Create a step for when we don't want to reply
    skip_reply_step = BaseStep("skip_reply")
    skip_reply_step.execute = lambda input, workflow: StepIO("Skipped reply due to short comment")

    # Create the conditional step
    reply_condition_step = ConditionalStep("reply_condition", should_reply, generate_reply_step, skip_reply_step)

    # Create the loop step with the conditional
    process_comments_loop = LoopStep("process_comments", [reply_condition_step, post_reply_step])

    # Add steps to the workflow
    my_youtube_workflow.add_step(get_comments_step)
    my_youtube_workflow.add_step(init_llm_step)
    #my_youtube_workflow.add_loop(process_comments_loop, input_key="get_comments")

    # Build and execute the workflow
    youtube_workflow = my_youtube_workflow.build()
    youtube_workflow.execute()


    #youtube_workflow.get_step_output("init_llm")



    