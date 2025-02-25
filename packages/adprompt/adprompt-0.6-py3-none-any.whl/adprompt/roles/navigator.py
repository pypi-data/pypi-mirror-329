from typing import List

from openai import BaseModel

from adprompt.chat_model import ChatResponse
from adprompt.client import AIClient
from adprompt.role import BaseRole
from adprompt.utils.json_utils import load_json_result


class ParamDef(BaseModel):
    key: str
    desc: str


class FuncDef(BaseModel):
    key: str
    desc: str
    params: List[ParamDef] = []


_ROLE_TMPL = """你将负责根据用户的输入推断应用场景并挑选出用于响应用户的函数。
下面我会依次给出各个函数的名称、适用的场景以及函数的相关参数。
{}

接下来我会提供给你一个用户的输入，你需要根据用户的输入和函数的适用场景准确地分析出使用哪个函数响应用户的请求。
如果能够分析出使用哪个函数响应用户的请求，你还需要根据函数参数的描述从用户的输入中提取函数参数，如果无法提取则认为参数为空。
你需要用json格式数据结果，其中function字段的值为选择的函数的名称，params字段的值为json格式的函数的参数和对应的参数值。
如果经过分析后不是十分确定响应用户请求的函数，function字段填充N/A。
你需要严格按照json格式输出结果，不要输出其他无关内容。
"""


class NavigatorRole(BaseRole):
    """
    选择调用函数并提取参数
    """

    def __init__(self, client: AIClient, funcs: List[FuncDef]):
        super().__init__(client)

        self.funcs = funcs

    def get_role_context(self) -> List[dict]:
        return [{
            "role": "system",
            "content": self._fill_tmpl(),
        }]

    def _fill_tmpl(self) -> str:
        lines = []
        for _i, func in enumerate(self.funcs):
            lines.append(f'{_i + 1}. *函数名称*：{func.key}')
            lines.append(f'*适用场景*：{func.desc}')
            if func.params:
                lines.append('*函数参数*：')
                for _j, param in enumerate(func.params):
                    lines.append(f'({_j + 1}) {param.key}：{param.desc}')
        return _ROLE_TMPL.format('\n'.join(lines))

    def post_process(self, content: str, input_content) -> ChatResponse:
        try:
            data = load_json_result(content)
        except Exception as e:
            return ChatResponse(
                content=content,
                error_message=f'Failed to load json result: {e}',
            )
        else:
            func_name = data.get('function')
            if func_name:
                for i in self.funcs:
                    if i.key == func_name:
                        return ChatResponse(
                            result=data,
                            content=content,
                        )
            return ChatResponse(
                content=content,
            )
