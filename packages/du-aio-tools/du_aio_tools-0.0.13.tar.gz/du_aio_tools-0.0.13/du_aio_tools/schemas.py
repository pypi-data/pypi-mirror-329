# -*- coding: utf-8 -*-
# @time: 2024/2/18 10:32
# @author: Dyz
# @file: schemas.py
# @software: PyCharm
import json
import re
from typing import List

from pydantic import BaseModel, validator


def reset_issn(issn: str):
    if issn:
        issn = issn.upper()
    if '*' in issn or 'N/A' in issn:
        return ''
    if len(issn) > 9:
        issn = re.findall('([0-9A-Z]{4}-[0-9A-Z]{4})', issn)
        if issn:
            issn = issn[0]
        else:
            issn = ''
    return issn.upper()


class journalSN(BaseModel):
    """期刊 ISSN 处理"""
    issn: str = ''
    eissn: str = ''

    @validator('issn')
    def check_issn(cls, val):
        """检查issn"""
        return reset_issn(val)

    @validator('eissn')
    def check_eissn(cls, val):
        """检查issn"""
        return reset_issn(val)

    def get_oissn(self) -> List:
        sn_set = set()
        if self.issn:
            sn_set.add(self.issn)
        if self.eissn:
            sn_set.add(self.eissn)
        return list(sn_set)


class BaseSchemas(BaseModel):
    """Base Schemas"""

    @staticmethod
    def dump(val):
        if isinstance(val, (list, dict)):
            return json.dumps(val, ensure_ascii=False)
        return val

    def value_dump(self) -> dict:
        """转换值，便于存储数据库"""
        return {k: self.dump(v) for k, v in self.dict().items()}
