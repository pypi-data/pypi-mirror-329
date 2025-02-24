# Promuet

[![PyPI - Version](https://img.shields.io/pypi/v/promuet.svg)](https://pypi.org/project/promuet)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/promuet)](https://pypi.org/project/promuet)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/promuet.svg)](https://pypi.org/project/promuet)

*A simple yet powerful prompt templating engine*

Promuet is a simple Python library for designing complex chains of prompts using basic prompt templates:

```python
from promuet import PromptFlow, Prompt, UserMessage, AssistantMessage, AppFlow

HAIKU_GENERATION_FLOW = PromptFlow(
    Prompt(
        description="Brainstorm haiku themes",
        messages=[
            UserMessage(
                """
                I want to write a haiku. Let's brainstorm themes inspired by {{season}}.
                List a few poetic and evocative themes that capture the mood and essence of the season.
                """
            )
        ],
        response_format="{{haiku_themes}}"
    ),
    Prompt(
        description="Generate haiku",
        is_continuation=True,
        messages=[
            AssistantMessage("{{haiku_themes}}"),
            UserMessage(
                """
                Based on the following themes inspired by {{season}}:
                {{haiku_themes}}

                Please write a simple, elegant haiku for each theme.
                """
            )
        ],
        response_format="{{haikus}}"
    )
)

app_flow = AppFlow()
app_flow.run_prompt(HAIKU_GENERATION_FLOW, dict(season="autumn"))
print(app_flow['haikus'])
```

It supports a variety of parsing methods designed to make parsing LLMs natural and intuitive. See below for more details.

## Detailed Usage

### Parsing

At the core, Promuet is just a simple parsing engine:

```python
from promuet import TemplateMatchItem

template = TemplateMatchItem(
    """
       Name: {{name}}
       Age: {{age:int}}
    """
)
input_string = """
    Name: John Doe
    Age: 30
"""
data = template.parse(input_string)
assert data['name'] == 'John Doe'
assert data['age'] == 30
```

A variable like `{{foo}}` can currently be one of the following types (default is `str`):
- `str`: A multi-line wildcard (essentially `.*?`)
- `int`: A number
- `list`: A bulleted or numbered list of items

In addition to basic variables, Promuet also supports parsing lists of repeated items with a template like this:

```
[[:myitems:]]
Item name: {{name}}
Item attribute: {{attribute}}
[[:myitems:]]
```

Which will produce a parsed result like:
```json
{"myitems": [{"name": "Item 1", "attribute": "Attribute 1"}, ...]}
```

### Prompts

A prompt is just a convenient wrapper around a series of chat message templates:
````python
from promuet import Prompt, SystemMessage, UserMessage

GENERATE_USERS_PROMPT = Prompt(
    description="Generate sample users",
    messages=[
        SystemMessage(
            """
            You are a synthetic data generator generating sample people. Format your response like so:
            ```
            === Person 1 ===
            Name: John Doe
            Age: 23

            === Person 2 ===
            ...
            ```
            """
        ),
        UserMessage(
            """Generate me {{count}} sample people from the country of {{country}} around the age of {{age_range}}."""
        ),
    ],
    response_format="""
        [[:people:]]
        === Person {{index:int}} ===
        Name: {{name}}
        Age: {{age:int}}
        [[:people:]]
    """
)
````

You can execute a prompt as follows:
```python
from promuet import AppFlow, OpenAiChatClient

# Set OPENAI_API_KEY environment variable
app_flow = AppFlow()
app_flow.run_prompt(GENERATE_USERS_PROMPT, dict(country='Nigeria', count=5, age_range='50-60'))
for person in app_flow['people']:
    print(f"Generated person: {person['name']} (age {person['age']})")
```

### Prompt Flows

Finally, sometimes you may want to piece together multiple prompts to produce more complex reasoning chains:

```python
from promuet import PromptFlow, AppFlow, Prompt, UserMessage, AssistantMessage

STARTUP_IDEA_FLOW = PromptFlow(
    Prompt(
        description="Decide problem area",
        messages=[
            UserMessage(
                """
                Think about various problem areas in everyday life and then at the bottom propose a specific area that has high potential for innovation.
                For now, let's focus on problems related to {{problem_area}}.

                Place the final proposed problem area at the bottom like <problem_area>problem area</problem_area>.
                """
            ),
        ],
        response_format="""
            {{problem_area_thoughts}}
            <problem_area>{{problem_area}}</problem_area>
        """
    ),
    Prompt(
        description="Generate startup idea",
        messages=[
            UserMessage("What is a problem area that we can explore innovative solutions for? Provide a direct answer."),
            AssistantMessage("{{problem_area}}"),
            UserMessage(
                """
                Based on this problem area, generate a complete startup idea that addresses the problem.
                """
            ),
        ],
        response_format="{{startup_idea_description}}"
    ),
    Prompt(
        description="Generate startup plan",
        is_continuation=True,
        messages=[
            AssistantMessage("{{startup_idea_description}}"),
            UserMessage("Now develop a complete end to end business proposal and plan for this startup including how we go from MVP/POC to launch to scale."),
        ],
        response_format="{{startup_idea_proposal}}"
    )
)
app_flow = AppFlow()
app_flow.run_prompt(STARTUP_IDEA_FLOW, dict(problem_area="construction"))
print('Startup idea proposal:')
print(app_flow['startup_idea_proposal'])
```

## Installation

```console
pip install promuet
```

## License

`promuet` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
