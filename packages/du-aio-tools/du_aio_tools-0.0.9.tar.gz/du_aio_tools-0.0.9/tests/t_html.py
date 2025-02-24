# -*- coding: utf-8 -*-
# @time: 2024/2/19 17:18
# @author: Dyz
# @file: html.py
# @software: PyCharm
class Hit1(BaseModel):
    name: str


class Hit(BaseModel):
    name: str
    data: List[Hit1]


class Data1(MyBaseModel):
    id: int
    name: str
    data: List[Hit]


if __name__ == '__main__':
    hit = Hit(name='name', data=[Hit1(name='aaa')])
    data = Data1(id=1, name='aa', data=[hit])
    print(data)
    data = data.value_dump()
    for k, v in data.items():
        print(k)
        print(type(v), v)