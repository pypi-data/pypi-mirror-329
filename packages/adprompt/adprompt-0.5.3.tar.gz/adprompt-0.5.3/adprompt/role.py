from abc import ABCMeta, abstractmethod
from typing import List

from adprompt.chat_model import ChatResponse
from adprompt.client import AIClient


class BaseRole(metaclass=ABCMeta):

    def __init__(self, client: AIClient):
        self.client = client

    @abstractmethod
    def get_role_context(self) -> List[dict]:
        """
        获取角色构建的上下文
        """

    def get_chat_messages(self, content: str) -> List[dict]:
        messages = self.get_role_context()
        messages.append({
            'role': 'user',
            'content': content,
        })
        return messages

    def post_process(self, content: str, input_content: str) -> ChatResponse:
        """
        对大模型输出结果进行后处理
        """
        return ChatResponse(
            content=content
        )

    def chat(self, content: str, **kwargs) -> ChatResponse:
        messages = self.get_chat_messages(content)
        result = self.post_process(self.client.chat(messages, **kwargs), content)
        return result
