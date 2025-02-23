import asyncio
import random
from typing import List
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from SimplerLLM.workflow.builder import Workflow, Step, Loop, Condition
from SimplerLLM.language.llm import LLM as GenerationLLM, LLMProvider
from test_helpers import get_latest_youtube_comments, post_reply

def initialize_llm():
    return GenerationLLM.create(provider=LLMProvider.ANTHROPIC, model_name="claude-3-haiku-20240307")

def generate_reply(llm, item):
    return llm.generate_response(prompt=f"generate a 5 words reply to the following comment: {item['comment_text']}")



def get_latest_comments():
    return get_latest_youtube_comments("UC1234567890", 5)


# Create the workflow
youtube_workflow = Workflow("YouTube Comment Reply")

# Step 1: Get Latest Comments
youtube_workflow.add_step(Step(
    "get_latest_comments",
    get_latest_comments,
    {}
))

# Step 2: Initialize LLM
youtube_workflow.add_step(Step(
    "Initialize_LLM",
    initialize_llm,
    {}
))

# Step 3: Loop over comments and generate replies
youtube_workflow.add_step(Loop(
    lambda: youtube_workflow.results["get_latest_comments"],
    [
        Step(
            "Generate_Reply",
            generate_reply,
            {"llm": "results.Initialize_LLM"}
        ),
        Step(
            "Post_Reply",
            post_reply,
            {"comment_id": lambda item: item['comment_id'], "reply": "results.Generate_Reply"}
        )
    ]
))


youtube_workflow.execute()



#print("\nNow importing and executing the workflow from the JSON file:\n")


#exported_workflow = youtube_workflow.export_to_file("youtube_workflow.json")

# Later, import the workflow from the JSON file
#imported_workflow = Workflow.import_from_file("youtube_workflow.json")
#imported_workflow.execute()

# Execute the imported workflow
#imported_workflow.execute()