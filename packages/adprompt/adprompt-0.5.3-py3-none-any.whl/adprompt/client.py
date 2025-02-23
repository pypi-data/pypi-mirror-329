from typing import List, Optional

from openai import OpenAI
from openai.types import Completion
from pydantic import BaseModel


class OpenAIConfig(BaseModel):
    base_url: str
    api_key: str
    model: str = None


class AIClient:

    def __init__(self, openai_config: OpenAIConfig = None):
        if openai_config:
            self.openai_client = OpenAI(
                api_key=openai_config.api_key,
                base_url=openai_config.base_url,
            )
            self.openai_model = openai_config.model
        else:
            self.openai_client = None
            self.openai_model = None

    def chat(self, messages: List[dict], temperature: float = 0, **kwargs) -> Optional[str]:
        if self.openai_client:
            if 'model' not in kwargs:
                kwargs['model'] = self.openai_model
            completion = self.openai_client.chat.completions.create(
                messages=messages,
                temperature=temperature,
                **kwargs,
            )
            return completion.choices[0].message.content

    def stream_chat(self, messages: List[dict], temperature: float = 0, **kwargs) -> Optional[Completion]:
        if self.openai_client:
            if 'stream' not in kwargs:
                kwargs['stream'] = True
            if 'model' not in kwargs:
                kwargs['model'] = self.openai_model
            completion = self.openai_client.chat.completions.create(
                messages=messages,
                temperature=temperature,
                **kwargs,
            )
            return completion
