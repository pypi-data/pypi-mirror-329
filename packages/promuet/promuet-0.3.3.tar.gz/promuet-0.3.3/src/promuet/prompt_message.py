import textwrap
from typing import Literal

from pydantic import BaseModel

from promuet.match_items import VarType, serialize_template


class PromptMessage(BaseModel):
    role: Literal['system', 'user', 'assistant']
    content: str

    def to_chat_message(self, variables: dict[str, VarType] | None = None) -> dict:
        return {
            'role': self.role,
            'content': serialize_template(self.content, variables or {}),
        }


class SystemMessage(PromptMessage):
    def __init__(self, content: str):
        super().__init__(role='system', content=textwrap.dedent(content))


class UserMessage(PromptMessage):
    def __init__(self, content: str):
        super().__init__(role='user', content=textwrap.dedent(content))


class AssistantMessage(PromptMessage):
    def __init__(self, content: str):
        super().__init__(role='assistant', content=textwrap.dedent(content))
