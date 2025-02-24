import json
import textwrap

from promuet.match_items import TemplateMatchItem, extract_data_vars


def test_match_items():
    template = TemplateMatchItem(
        """
            Task {{task_number:int}}: {{task_title}}
            Description: {{task_description}}

            Verification: {{task_verification_items:list}}
        """
    )
    input_string = """
        Task 12: Clean the house
        Description:
        I need to clean the house to make it nice.

        The floors need to be cleaned, the rugs vacuumed, and the laundry folded.

        Verification:
        - Floors should have no dust
        - Rugs should be free of dirt
        - Laundry should be folded
    """
    data = template.parse(input_string)
    assert str(data['.str']).strip() == textwrap.dedent(input_string).strip()
    data = extract_data_vars(data)
    assert data == {
        'task_number': 12,
        'task_title': 'Clean the house',
        'task_description': 'I need to clean the house to make it nice.\n\nThe floors need to be cleaned, the rugs vacuumed, and the laundry folded.',
        'task_verification_items': [
            'Floors should have no dust',
            'Rugs should be free of dirt',
            'Laundry should be folded',
        ],
    }


def test_match_item_list():
    template = TemplateMatchItem(
        """
            Here are the tasks relating to '{{relates_to}}':
            [[:tasks:]]
            Task {{num:int}}: {{title}}
            [[:tasks:]]
            Note: {{note:str}}
        """
    )
    input_string = """
        Here are the tasks relating to 'hamburgers':

        Task 1: Do something

        Task 2: Something else

        Note: These are the tasks.
    """
    rdata = template.parse(input_string)
    data = extract_data_vars(rdata)
    assert data == {
        'relates_to': 'hamburgers',
        'tasks': [
            {'num': 1, 'title': 'Do something'},
            {'num': 2, 'title': 'Something else'},
        ],
        'note': 'These are the tasks.',
    }, json.dumps(rdata, indent=4)


def test_list():
    template = TemplateMatchItem(
        """
            Features:
            [[:app_mvp_features:]]
            {{number:int}}. {{title}}:
            [[:details:]]
            - {{content}}
            [[:details:]]
            [[:app_mvp_features:]]

            Note: ...
        """
    )
    input_string = """
Features:
1. Virtual Hacking World:
- Create a basic virtual environment with a single hacking scenario for players to explore.
- Include a graphical interface to depict the virtual system, with interactive elements to manipulate.
- Integrate some basic hacking challenges, such as bypassing firewalls or cracking passwords.

2. Coding Challenge:
- Develop a simple coding challenge within the hacking scenario for players to solve.
- Provide a basic code editor where players can write and execute code to progress through the challenge.
- Incorporate a scoring system to evaluate the player's coding skills and progression.

3. Realistic Hacking Tools:
- Include a limited set of realistic hacking tools that players can utilize during their hacking mission.
- Implement basic functionalities of these tools, such as port scanning or packet sniffing.
- Ensure that the tools have a visually appealing and intuitive user interface.

Note: ...
"""

    data = template.parse(input_string)
    features: list[dict] = data['app_mvp_features']  # type: ignore
    assert len(features) == 3
    assert [x['title'] for x in features] == [
        'Virtual Hacking World',
        'Coding Challenge',
        'Realistic Hacking Tools',
    ]
    assert [x['content'] for x in features[0]['details']] == [
        'Create a basic virtual environment with a single hacking scenario for players to explore.',
        'Include a graphical interface to depict the virtual system, with interactive elements to manipulate.',
        'Integrate some basic hacking challenges, such as bypassing firewalls or cracking passwords.',
    ]


if __name__ == '__main__':
    test_match_items()
    test_match_item_list()
    test_list()
