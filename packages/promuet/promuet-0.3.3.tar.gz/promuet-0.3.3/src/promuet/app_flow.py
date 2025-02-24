import json
from os import PathLike
from pathlib import Path
import sys
from typing import Optional, Type, Union
from typing_extensions import TypeVar

from .ai_client import ChatClientBase, OpenAiChatClient

from .prompt_flow import Prompt, PromptFlow, VarType


T = TypeVar('T', bound=Union[str, int, list, dict])


class AppFlow:
    def __init__(
        self,
        /,
        model: Optional[str] = None,
        client: Optional[ChatClientBase] = None,
        session_path: Optional[Union[str, Path]] = None,
        debug: bool = False,
    ):
        assert not (model and client), "Either model or client must be provided"
        self.client = client or OpenAiChatClient(model=model)
        self.session_path = Path(session_path) if session_path else None
        self.session: dict[str, VarType] = self.load_session()
        self.debug = debug

    def load_session(self) -> dict[str, VarType]:
        return (
            {}
            if not self.session_path or not self.session_path.is_file()
            else json.loads(self.session_path.read_text())
        )

    def save_session(self):
        if self.session_path:
            self.session_path.write_text(json.dumps(self.session, indent=4))

    def prompt_from_cli(self, field_name: str, prompt_message: str):
        """Gets a field from session or prompts the user for it."""
        if field_name not in self.session:
            self.session[field_name] = input(prompt_message).rstrip('.')

    def run_prompt(self, prompt: PromptFlow | Prompt, extra_args: Optional[dict] = None):
        self.session.update(extra_args or {})
        prompt_flow = PromptFlow(prompt) if isinstance(prompt, Prompt) else prompt
        new_vars = prompt_flow.run(self.session, self.client)
        self.session.update(new_vars)
        self.save_session()
        for key, value in new_vars.items():
            if key + '.str' in self.session:
                value = self.session[key + '.str']
            if key.endswith('.str'):
                continue

            assert isinstance(value, str), (key, value, key + '.str')
            self._debug('\n### {} ###'.format(key))
            self._debug(value)
            self._debug()

    def __getitem__(self, key: str) -> VarType:
        return self.session[key]

    def __setitem__(self, key: str, value: VarType):
        self.session[key] = value
        self.save_session()

    def get_var[T](self, key: str, cls: Type[T]) -> T:
        """Same as ['key'] but with type checking"""
        value = self.session[key]
        assert isinstance(value, cls), f'{key}: {value} is not an instance of {cls}'
        return value

    def __delitem__(self, key: str):
        del self.session[key]
        self.save_session()

    def __contains__(self, key: str) -> bool:
        return key in self.session

    def _debug(self, *args):
        if self.debug:
            sys.stdout.write(' '.join(str(arg) for arg in args) + '\n')
            sys.stdout.flush()
