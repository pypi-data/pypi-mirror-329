# -*- coding: utf-8 -*-
# @Time    : 2025/2/21 09:46
# @Author  : xuwei
# @FileName: response.py
# @Software: PyCharm


from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar('T')

CODE_SYSTEM_ERROR = -1
CODE_OK = 0
CODE_SHOW = 1


class BaseResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None
