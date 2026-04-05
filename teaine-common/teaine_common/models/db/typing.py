"""定义通用的类型标注组件"""

from typing import Union

JSONValue = Union[float, int, str]
'''表模型中 JSON 的键类型'''

__all__ = [
    "JSONValue",
]
