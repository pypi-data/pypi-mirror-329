# -*- coding: utf-8 -*-
# @Time    : 2024/12/25 14:05
# @Author  : xuwei
# @FileName: redis_op.py
# @Software: PyCharm

from redis.asyncio import StrictRedis, ConnectionPool
from .dotenv_config import config

class RedisAsyncOp:
    def __init__(self, label='redis', db=0, strict=True, config_map=None, max_connections=5):
        self.__label = label
        self.__db = db
        self.__config_map = config_map
        self.__strict = strict
        self.__max_connections = max_connections
        self.__redis_pool = None
        self.con = StrictRedis

    def init(self):
        """
        使用方法

        redis_op = at.RedisAsyncOp('redis', 3, max_connections=1)
        redis_op.init()

        keys = await redis_op.con.set('stock_company', 'xwewrwrwe')
        print(keys)
        val = await redis_op.con.get('stock_company')
        print(val)

        await redis_op.close()
        """

        if self.__config_map:
            redis_host = self.__config_map['host']
            redis_port = int(self.__config_map['port'])
            redis_pass = self.__config_map.get('pass', "")
        else:
            redis_host = config(self.__label, 'host')
            redis_port = int(config(self.__label, 'port'))
            redis_pass = config(self.__label, 'pass', '')

        if not redis_pass: redis_pass = None

        redis_pool = ConnectionPool(
            host=redis_host, port=redis_port, password=redis_pass, db=self.__db, max_connections=self.__max_connections,
            decode_responses=self.__strict
        )

        self.__redis_pool = redis_pool
        self.con = StrictRedis(connection_pool=self.__redis_pool)

    async def close(self):
        await self.con.close(self.__redis_pool)
