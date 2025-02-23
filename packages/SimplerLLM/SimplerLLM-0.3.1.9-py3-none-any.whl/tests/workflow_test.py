import asyncio
from typing import List
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))




from SimplerLLM.workflow.builder import Workflow, Module,ModuleType
from SimplerLLM.language.llm import LLM, LLMProvider
from test_helpers import get_latest_youtube_comments, post_reply



def create_youtube_reply_workflow():
    workflow = Workflow("YouTube Comment Reply Workflow", "Fetches recent YouTube comments and posts AI-generated replies")

    # Fetch Comments Module
    fetch_comments = Module("fetch_comments", ModuleType.FUNCTION, {
        "function": "get_latest_youtube_comments",
        "inputs": {"channel_id": "UC1234567890", "num_comments": 5},
        "output": "latest_comments"
    })
    workflow.add_module(fetch_comments)

    # Initialize LLM Module
    init_llm = Module("initialize_llm", ModuleType.LLM_INSTANCE, {
        "provider": "ANTHROPIC",
        "model": "claude-3-haiku-20240307",
        "output": "generation_llm"
    })
    workflow.add_module(init_llm)

    # Process Comments Loop Module
    process_comments = Module("process_comments", ModuleType.LOOP, {
        "iteration_variable": "comment",
        "iterable": "latest_comments"
    })
    workflow.add_module(process_comments)

    # Generate Reply Module (inside loop)
    generate_reply = Module("generate_reply", ModuleType.LLM_GENERATE, {
        "llm_instance": "generation_llm",
        "inputs": {"prompt": "generate a 5 words reply to the following comment: {comment['comment_text']}"},
        "output": "reply"
    })
    workflow.add_module(generate_reply)

    # Post Reply Module (inside loop)
    post_reply = Module("post_reply", ModuleType.FUNCTION, {
        "function": "post_reply",
        "inputs": {"comment_id": "{comment['comment_id']}", "reply_text": "{reply}"}
    })
    workflow.add_module(post_reply)

    # Connect modules
    workflow.connect_modules("fetch_comments", "initialize_llm")
    workflow.connect_modules("initialize_llm", "process_comments")
    workflow.connect_modules("process_comments", "generate_reply")
    workflow.connect_modules("generate_reply", "post_reply")

    return workflow


# Create the workflow
youtube_workflow = create_youtube_reply_workflow()

# Execute the workflow
#youtube_workflow.execute()

# Optionally, you can save the workflow to JSON for later use
workflow_json = youtube_workflow.to_json()


# Save the workflow to a JSON file
with open('youtube_reply_workflow.json', 'w') as f:
    json.dump(json.loads(workflow_json), f, indent=2)

print("Workflow saved to youtube_reply_workflow.json")

# To load and run the workflow later:
# loaded_workflow = Workflow.from_json(workflow_json)
# loaded_workflow.execute()





