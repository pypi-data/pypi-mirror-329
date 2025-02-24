from abc import ABC, abstractmethod
from hashlib import md5
import json
from pathlib import Path
from typing_extensions import Optional

from openai import OpenAI


class ChatClientBase(ABC):
    cache_key: str = ''

    @abstractmethod
    def predict(self, messages: list[dict]) -> str:
        pass


class OpenAiChatClient(ChatClientBase):
    def __init__(self, openai: Optional[OpenAI] = None, model: Optional[str] = None, completion_kwargs: Optional[dict] = None):
        self.client = openai or OpenAI()
        self.kwargs = completion_kwargs or {}
        self.kwargs.setdefault('model', model or 'gpt-4o-mini')
        self.cache_key = md5(
            json.dumps(self.kwargs, sort_keys=True).encode()
        ).hexdigest()

    def predict(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(messages=messages, **self.kwargs)  # type: ignore
        return response.choices[0].message.content


class CachedChatClient(ChatClientBase):
    def __init__(self, cache_path: Path, client: ChatClientBase):
        self.cache_path = cache_path
        self.cache = json.loads(cache_path.read_text()) if cache_path.is_file() else {}
        self.client = client

    def predict(self, messages: list[dict]) -> str:
        key = md5(
            (self.client.cache_key + json.dumps(messages, sort_keys=True)).encode()
        ).hexdigest()
        if key not in self.cache:
            self.cache[key] = self.client.predict(messages)
        return self.cache[key]
