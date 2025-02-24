# -*- coding: utf-8 -*-
# @time: 2024/2/18 9:49
# @author: Dyz
# @file: base_conn.py
# @software: PyCharm
import functools
from typing import Optional

from loguru import logger
from tortoise import BaseDBAsyncClient, models, fields, Tortoise


async def init_db(tortoise_orm: dict, create: bool = False):
    """
    >>> {
        "connections": {
            "conn": {
                "engine": f"tortoise.backends.mysql",  # mysql/asyncpg/sqlite
                "credentials": {
                    'host': 'localhost',
                    'port': 3306,
                    'user': 'root',
                    'password': 'xxx',
                    'database': 'db_name',
                    'charset': 'utf8mb4'
                }
            }
        },
        "apps": {
            "jour": {"models": ["__main__"], "default_connection": "conn"},
        },
        'use_tz': False,
        'timezone': 'Asia/Shanghai',
    }
    """
    await Tortoise.init(
        config=tortoise_orm
    )
    if create:
        await Tortoise.generate_schemas()


async def close_db():
    """关闭数据库连接"""
    await Tortoise.close_connections()


def load_db(tortoise_orm, create: bool = False):
    """
    tortoise_orm: 数据库链接配置
    create: 创建表
    """

    def _load_db(func):
        """加载数据库"""

        @functools.wraps(func)
        async def wrap(*args, **kwargs):
            await init_db(tortoise_orm, create)

            result = await func(*args, **kwargs)

            await close_db()
            return result

        return wrap

    return _load_db


class DataModel(models.Model):
    """提供 数据截断表 与 复制的快捷操作"""
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True  # 标记为抽象类，不直接创建表

    @classmethod
    async def truncate_model(cls, using_db: Optional[BaseDBAsyncClient] = None):
        """截断表"""
        db = using_db or cls._choose_db(True)
        db_name = cls._meta.db_table
        if db.capabilities.dialect == 'postgres':  # mysql
            await db.execute_script(f'TRUNCATE TABLE {db_name} RESTART IDENTITY')
            logger.info(f'截断表[{db_name}]')
        else:
            await db.execute_script(f'TRUNCATE TABLE {db_name}')
            logger.info(f'截断表[{db_name}]')

    @classmethod
    async def copy_old(cls, using_db: Optional[BaseDBAsyncClient] = None, name='_old'):
        """复制表"""
        db = using_db or cls._choose_db(True)
        _table = cls._meta.db_table
        old_table = _table + name
        data = await cls.all().limit(1)
        if data:
            await db.execute_query(f'DROP TABLE IF EXISTS {old_table}')
            return await db.execute_query(f'CREATE TABLE {old_table} SELECT * FROM {_table}')


class BaseModel(DataModel):
    """基础模型类，包含创建时间和更新时间"""

    class Meta:
        abstract = True  # 标记为抽象类，不直接创建表

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

# class Journal(BaseModel):
#     class Meta:
#         table = 'journal' # 表名
#         unique_together = (("uid", "uid2", "word"),) # 联合唯一索引
#     table_description = '主题词查重数据表'  # 表描述
