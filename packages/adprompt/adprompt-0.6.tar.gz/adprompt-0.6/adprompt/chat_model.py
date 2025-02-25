from typing import Union

from pydantic import BaseModel


class ChatResponse(BaseModel):
    result: Union[dict, list] = None
    content: str = None
    error_message: str = None
