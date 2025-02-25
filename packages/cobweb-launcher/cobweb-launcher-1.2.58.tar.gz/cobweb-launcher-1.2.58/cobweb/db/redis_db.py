import redis
import time
from cobweb import setting
from redis.exceptions import ConnectionError, TimeoutError


class RedisClient:
    def __init__(self, **kwargs):
        redis_config = kwargs or setting.REDIS_CONFIG
        self.host = redis_config['host']
        self.password = redis_config['password']
        self.port = redis_config['port']
        self.db = redis_config['db']

        self.max_retries = 5
        self.retry_delay = 5
        self.client = None
        self.connect()

    def connect(self):
        """尝试连接 Redis"""
        retries = 0
        while retries < self.max_retries:
            try:
                self.client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    password=self.password,
                    db=self.db,
                    socket_timeout=5,  # 设置连接超时时间
                    socket_connect_timeout=5  # 设置连接超时时间
                )
                # 测试连接是否成功
                self.client.ping()
                return
            except (ConnectionError, TimeoutError) as e:
                retries += 1
                if retries < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    raise Exception("达到最大重试次数，无法连接 Redis")

    def is_connected(self):
        try:
            self.client.ping()
            return True
        except (ConnectionError, TimeoutError):
            return False

    def reconnect(self):
        self.connect()

    def execute_command(self, command, *args, **kwargs):
        retries = 0
        while retries < self.max_retries:
            try:
                if not self.is_connected():
                    self.reconnect()
                return getattr(self.client, command)(*args, **kwargs)
            except (ConnectionError, TimeoutError) as e:
                retries += 1
                if retries < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    raise Exception("达到最大重试次数，无法执行命令")

    def get(self, name):
        # with self.get_connection() as client:
        #     return client.get(name)
        return self.execute_command("get", name)

    def incrby(self, name, value):
        # with self.get_connection() as client:
        #     client.incrby(name, value)
        self.execute_command("incrby", name, value)

    def setnx(self, name, value=""):
        # with self.get_connection() as client:
        #     client.setnx(name, value)
        self.execute_command("setnx", name, value)

    def setex(self, name, t, value=""):
        # with self.get_connection() as client:
        #     client.setex(name, t, value)
        self.execute_command("setex", name, t, value)

    def expire(self, name, t, nx: bool = False, xx: bool = False, gt: bool = False, lt: bool = False):
        # with self.get_connection() as client:
        # client.expire(name, t, nx, xx, gt, lt)
        self.execute_command("expire", name, t, nx, xx, gt, lt)

    def ttl(self, name):
        # with self.get_connection() as client:
        #     return client.ttl(name)
        return self.execute_command("ttl", name)

    def delete(self, name):
        # with self.get_connection() as client:
        #     return client.delete(name)
        return self.execute_command("delete", name)

    def exists(self, *name) -> bool:
        # with self.get_connection() as client:
        #     return client.exists(*name)
        return self.execute_command("exists", *name)

    def sadd(self, name, value):
        # with self.get_connection() as client:
        #     return client.sadd(name, value)
        return self.execute_command("sadd", name, value)

    def zcard(self, name) -> bool:
        # with self.get_connection() as client:
        #     return client.zcard(name)
        return self.execute_command("zcard", name)

    def zadd(self, name, item: dict, **kwargs):
        # with self.get_connection() as client:
        #     return client.zadd(name, item, **kwargs)
        return self.execute_command("zadd", name, item, **kwargs)

    def zrem(self, name, *value):
        # with self.get_connection() as client:
        #     return client.zrem(name, *value)
        return self.execute_command("zrem", name, *value)

    def zcount(self, name, _min, _max):
        # with self.get_connection() as client:
        #     return client.zcount(name, _min, _max)
        return self.execute_command("zcount", name, _min, _max)

    # def zrangebyscore(self, name, _min, _max, start, num, withscores: bool = False, *args):
    #     with self.get_connection() as client:
    #        return client.zrangebyscore(name, _min, _max, start, num, withscores, *args)

    def lua(self, script: str, keys: list = None, args: list = None):
        keys = keys or []
        args = args or []
        keys_count = len(keys)
        return self.execute_command("eval", script, keys_count, *keys, *args)

    def lua_sha(self, sha1: str, keys: list = None, args: list = None):
        keys = keys or []
        args = args or []
        keys_count = len(keys)
        return self.execute_command("evalsha", sha1, keys_count, *keys, *args)

    def execute_lua(self, lua_script: str, keys: list, *args):
        execute = self.execute_command("register_script", lua_script)
        return execute(keys=keys, args=args)