import redis

from src.infra.config.settings import Config


class JtechRedis:
    def __init__(self, host: str, port: int):
        self.host = host or Config.REDIS_HOST
        self.port = port or Config.REDIS_PORT
        self.db = Config.REDIS_DB
        self.password = Config.REDIS_PASSWORD
        self.redis = redis.StrictRedis(host=self.host, port=self.port, db=self.db, password=self.password)

    def set(self, key: str, value: str, expire: int = None):
        self.redis.set(key, value, ex=expire)

    def get(self, key: str):
        return self.redis.get(key)

    def delete(self, key: str):
        self.redis.delete(key)

    def keys(self, pattern: str):
        return self.redis.keys(pattern)

    def flush_db(self):
        self.redis.flushdb()
