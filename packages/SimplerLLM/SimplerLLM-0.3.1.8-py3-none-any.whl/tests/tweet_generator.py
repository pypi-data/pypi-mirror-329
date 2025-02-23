from SimplerLLM.language.llm_router import LLMRouter
from SimplerLLM.language.llm import LLM, LLMProvider

def main():
    # Initialize LLM
    llm_instance = LLM.create(
        provider=LLMProvider.OPENAI,
        model_name="gpt-4o",
        verbose=True
    )

    # Initialize router
    router = LLMRouter(llm_instance=llm_instance)

    # Add template choices
    template_1 = """
    Most [***Topic People] spend their entire careers striving for [Goal*].**
    But here's something they don't teach you in school:
    Achieving [***Goal*] is way easier than you think.**
    Here's how to save yourself a decade and unlock [***Outcome*] this year:
    """

    template_2 = """
    They say it takes 10 years to master a craft.**
    But using this framework, I mastered [***Topic*] in 1/10th the time.**
    [***Step #1*]**
    [***Step #2*]**
    [***Step #3*]**
    [***Step #4*]**
    """

    template_3 = """
    Most people think learning [***Topic*] takes 10,000 hours.**
    But I can explain it to you in 30 seconds.
    A quick breakdown on:
    [***Main Point #1*]**
    [***Main Point #2*]**
    [***Main Point #3*]**
    """

    # Add choices in bulk
    choices = [
        (template_1, {"type": "tweet", "style": "achievement"}),
        (template_2, {"type": "tweet", "style": "educational"}),
        (template_3, {"type": "tweet", "style": "quick-tips"})
    ]
    indices = router.add_choices(choices)
    print("Added choices with indices:", indices)



    input = """
    Last Week, I shared that am working on PyDive, a free interactive Python course
    with a unique special curriculum.
    I want to share an update that I finished the first lecture, and I will be sharing a video
    on the udpates below.
    """
    
    
    print("\n Finding tweet templates")
    print("-" * 50)
    result = router.route_with_metadata(
        f"I want to create a tweet about: \n {input}",
        metadata_filter={"type": "tweet"}
    )
    if result:
        print(f"Found tweet template (index {result.selected_index + 1}):")
        print(f"Confidence: {result.confidence_score}")
        print(f"Reasoning: {result.reasoning}")
        

    template  = router.get_choice(result.selected_index)
    content, metadata = template


    generation_prompt = f"""

    Generate a Tweet based on thhe [INPUT] and provider [Template]

    [INPUT]: {input}

    [Template]: {content}

    """

    tweet = llm_instance.generate_response(prompt=generation_prompt)
    print(tweet)
    

if __name__ == "__main__":
    main()
