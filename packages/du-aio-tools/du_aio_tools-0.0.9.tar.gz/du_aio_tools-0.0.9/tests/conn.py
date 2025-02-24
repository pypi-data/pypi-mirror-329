# -*- coding: utf-8 -*-
# @time: 2024/2/18 10:17
# @author: Dyz
# @file: conn.py
# @software: PyCharm
from du_aio_tools.base_conn import BaseModel, load_db
from tortoise import fields


db_conf = {
    "connections": {
        "conn": {
            "engine": f"tortoise.backends.asyncpg",
            "credentials": {
                'host': '10.168.2.142',
                'port': 5432,
                'user': 'postgres',
                'password': '02532dFb821',
                'database': 'scientific_research',
                # 'charset': 'utf8mb4'
            }
        }
    },
    "apps": {
        "jour": {"models": ["__main__"], "default_connection": "conn"},
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai',
}


class ZkyBase(BaseModel):
    class Meta:
        table = 'zky_all_test'

    year = fields.IntField(default=0, description='年份')



@load_db(db_conf, create=True)
async def t1():
    data = await ZkyBase.truncate_model()
    print(data)


if __name__ == '__main__':
    import asyncio

    asyncio.run(t1())
