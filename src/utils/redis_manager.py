# This file is used to manage the connection to the Redis database. It is a singleton class that creates a connection pool
import redis
from redis import ConnectionPool
from src.config.settings import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


class RedisConnectionManager:
    _pool = None

    @classmethod
    def get_pool(cls, db):
        # 修改为针对不同db创建不同的pool，或者共用一个pool但每次获取连接时指定db
        # 这里选择为每个db创建单独的pool实例，如果REDIS_DB经常变化，可能需要考虑另一种策略
        # 或者，如果通常只连接一个db，则原始逻辑问题不大，但更好的是支持多db
        # 为简化，暂时维持一个共享pool，但理想情况下应按db隔离或传入db到get_connection
        if cls._pool is None:  # 或者可以考虑一个字典来存储不同db的pool
            cls._pool = ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=db, password=REDIS_PASSWORD, decode_responses=True)
        elif cls._pool.connection_kwargs.get('db') != db:
            # 如果请求的db与现有pool的db不同，创建一个新的pool
            # 注意：这种方式下，_pool会被最后一次请求的db的pool覆盖
            # 更健壮的方式是使用字典 cls._pools = {}，cls._pools.setdefault(db, ConnectionPool(...))
            cls._pool = ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=db, password=REDIS_PASSWORD, decode_responses=True)
        return cls._pool

    @classmethod
    def get_connection(cls, db=REDIS_DB):
        return redis.Redis(connection_pool=cls.get_pool(db))
