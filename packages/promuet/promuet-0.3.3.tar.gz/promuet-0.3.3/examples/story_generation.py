import argparse
from promuet import PromptFlow, Prompt, UserMessage, AssistantMessage, AppFlow

def generate_story(story_setting):
    STORY_GENERATION_FLOW = PromptFlow(
        Prompt(
            description="Create characters",
            messages=[
                UserMessage(
                    """
                    I'm writing a story taking place in {{story_setting}}
                    I'd like you to propose 3 characters for me to use in my story.

                    Start by brainstorming various professions and which would be most interesting in a 5-10 paragraph passionate incoherent chain of thought manner, without making any decisions. Then, at the bottom, separated by a "---" divider, write out all the basic character descriptions.
                    """
                )
            ],
            response_format="""
                {{character_brainstorming}}
                ---
                {{character_descriptions}}
            """
        ),
        Prompt(
            description="Create character backstories",
            messages=[
                UserMessage(
                    """
                    Here are a set of dynamic and interesting characters that I will use in my story taking place in {{story_setting}}:
                    ```
                    {{character_descriptions}}
                    ```

                    For each character, let's flesh out their backstory, write a 2 paragraph storyline backstory for each character that covers their interesting and unique backstory, behaviors, and core motivations. This doesn't need to be written in story form yet and should be primarily a description / exploration.
                    """
                )
            ],
            response_format="{{character_backstories}}"
        ),
        Prompt(
            description="Brainstorm plotline",
            is_continuation=True,
            messages=[
                AssistantMessage("{{character_backstories}}"),
                UserMessage(
                    """
                    Now let's think about how these characters could somehow have an interesting set of interactions that bring each other together and lead to a compelling plotline.

                    I'd like you to perform a 5-10 paragraph brainstorming session where you passionately explore interesting interactions, and you constantly are changing your mind and generating new, even more interesting ideas and unique plotlines.
                    """
                )
            ],
            response_format="{{plotline_brainstorming}}"
        ),
        Prompt(
            description="Generate story",
            is_continuation=True,
            messages=[
                AssistantMessage("{{plotline_brainstorming}}"),
                UserMessage(
                    """
                    Finally, I'd like you to author the complete end to end story based on the plotline brainstorming session. Choose the most interesting ideas from your brainstorming session and use them to author an original, unique, and wildly interesting complete story taking place in {{story_setting}}. We should start by following the main character in a particularly eventful situation, then in the next chapter switch to another character's backstory, for the third chapter switch to the third character's backstory, and finally in the fourth chapter, we should follow the main character again the eventful situation, introducing the other characters as they encounter each other. Then, from there, take the story where it flows. In total, end to end, I would like you to author around 10 chapters worth of content.
                    """
                )
            ],
            response_format="{{full_story}}"
        )
    )

    app_flow = AppFlow()
    app_flow.run_prompt(STORY_GENERATION_FLOW, dict(story_setting=story_setting))
    print(app_flow['full_story'])


def main():
    parser = argparse.ArgumentParser(description="Generate a story with AI.")
    parser.add_argument("--story_setting", type=str, required=True, help="The setting of the story (e.g., '18th century London').")

    args = parser.parse_args()
    generate_story(args.story_setting)


if __name__ == "__main__":
    main()
