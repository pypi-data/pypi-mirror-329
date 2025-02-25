from typing import List

from adprompt.client import AIClient
from adprompt.role import BaseRole

_ROLE_TMPL = """你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。"""


class ChatbotRole(BaseRole):
    """
    聊天机器人
    """

    def __init__(self, client: AIClient, role: str = None):
        super().__init__(client)

        self.role = role or _ROLE_TMPL

    def get_role_context(self) -> List[dict]:
        return [{
            "role": "system",
            "content": self.role,
        }]
