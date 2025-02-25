from typing import List

from openai import BaseModel

from adprompt.chat_model import ChatResponse
from adprompt.client import AIClient
from adprompt.role import BaseRole
from adprompt.utils.json_utils import load_json_result


class ClassDef(BaseModel):
    key: str
    desc: str


_ROLE_TMPL = """你将负责根据预先定义好的类别以及这个类别包含哪些内容的描述，分析输入的文本和哪个类别所包含的内容相关。
下面我会依次给出各个类别的名称以及对类别中包含哪些内容的描述。
{}

接下来我会提供给你一个文本输入，你需要判断文本是否和某个类别描述中包含的内容相关，如果相关则认为文本属于该类别，你需要进一步评估文本和该类别的相关程度。
你需要用json列表形式输出不超过{}个和文本输入最相关的类别的分析结果，每个相关类别的分析结果用一个json格式数据表示，其中class字段的值为类别的标识，related字段的值为文本和对应类别的相关程度（取值包括“非常相关”、“一般相关”、“不相关”）{}。
如果经过分析后不是十分确定文本所属的类别，则输出一个空的json列表。
你需要严格按照json格式输出结果，不要输出其他无关内容。
"""


class ClassifierRole(BaseRole):
    """
    根据类别描述进行文本分类
    """

    def __init__(self, client: AIClient, classes: List[ClassDef], top_k: int = 3, reason_enabled=False):
        super().__init__(client)

        self.classes = classes
        self.top_k = top_k
        self.reason_enabled = reason_enabled

    def get_role_context(self) -> List[dict]:
        return [{
            "role": "system",
            "content": self._fill_tmpl(),
        }]

    def _fill_tmpl(self) -> str:
        lines = []
        for _i, c in enumerate(self.classes):
            lines.append(f'{_i + 1}. {c.key}：{c.desc}')
        return _ROLE_TMPL.format(
            '\n'.join(lines),
            self.top_k,
            ',reason字段的值为文本和对应类别相关的简短理由' if self.reason_enabled else '',
        )

    def post_process(self, content: str, input_content: str) -> ChatResponse:
        try:
            data = load_json_result(content)
        except Exception as e:
            return ChatResponse(
                content=content,
                error_message=f'Failed to load json result: {e}',
            )
        else:
            result = []
            if isinstance(data, list):
                for d in data:
                    class_key = d.get('class')
                    if class_key:
                        for i in self.classes:
                            if i.key == class_key:
                                result.append(d)
            return ChatResponse(
                result=result,
                content=content,
            )
