


# 示例用法
# if __name__ == "__main__":
#     redis_client = RedisClient(
#         host="r-j6c1t3etiefpmz7cwdpd.redis.rds.aliyuncs.com", port=6379,
#         password="SpiderLinux666", db=0
#     )
#
#     # 执行 Redis 命令
#     try:
#         ss = redis_client.get("host_speed_control:bepls.com")
#         print(f"获取的值: {ss}")
#     except Exception as e:
#         print(f"操作失败: {e}")


import redis
from cobweb import setting


class RedisDB:

    def __init__(self, **kwargs):
        redis_config = kwargs or setting.REDIS_CONFIG
        pool = redis.ConnectionPool(**redis_config)
        self._client = redis.Redis(connection_pool=pool)

    def setnx(self, name, value=""):
        return self._client.setnx(name, value)

    def setex(self, name, t, value=""):
        return self._client.setex(name, t, value)

    def expire(self, name, t, nx: bool = False, xx: bool = False, gt: bool = False, lt: bool = False):
        return self._client.expire(name, t, nx, xx, gt, lt)

    def ttl(self, name):
        return self._client.ttl(name)

    def delete(self, name):
        return self._client.delete(name)

    def exists(self, *name) -> bool:
        return self._client.exists(*name)

    def sadd(self, name, value):
        return self._client.sadd(name, value)

    def zcard(self, name) -> bool:
        return self._client.zcard(name)

    def zadd(self, name, item: dict, **kwargs):
        return self._client.zadd(name, item, **kwargs)

    def zrem(self, name, *value):
        return self._client.zrem(name, *value)

    def zcount(self, name, _min, _max):
        return self._client.zcount(name, _min, _max)

    # def zrangebyscore(self, name, _min, _max, start, num, withscores: bool = False, *args):
    #     return self._client.zrangebyscore(name, _min, _max, start, num, withscores, *args)

    def lua(self, script: str, keys: list = None, args: list = None):
        keys = keys or []
        args = args or []
        keys_count = len(keys)
        return self._client.eval(script, keys_count, *keys, *args)

    def lua_sha(self, sha1: str, keys: list = None, args: list = None):
        keys = keys or []
        args = args or []
        keys_count = len(keys)
        return self._client.evalsha(sha1, keys_count, *keys, *args)

    def execute_lua(self, lua_script: str, keys: list, *args):
        execute = self._client.register_script(lua_script)
        return execute(keys=keys, args=args)

    def lock(self, key, t=15) -> bool:
        lua_script = """
        local status = redis.call('setnx', KEYS[1], 1)
        if ( status == 1 ) then
            redis.call('expire', KEYS[1], ARGV[1])
        end 
        return status 
        """
        status = self.execute_lua(lua_script, [key], t)
        return bool(status)

    def members(self, key, score, start=0, count=5000, _min="-inf", _max="+inf") -> list:
        lua_script = """
        local min = ARGV[1]
        local max = ARGV[2]
        local start = ARGV[3]
        local count = ARGV[4]
        local score = ARGV[5]
        local members = nil

        if ( type(count) == string ) then
            members = redis.call('zrangebyscore', KEYS[1], min, max, 'WITHSCORES')
        else
            members = redis.call('zrangebyscore', KEYS[1], min, max, 'WITHSCORES', 'limit', start, count)
        end

        local result = {}

        for i = 1, #members, 2 do
            local priority = nil
            local member = members[i]
            local originPriority = nil
            if ( members[i+1] + 0 < 0 ) then
                originPriority = math.ceil(members[i+1]) * 1000 - members[i+1] * 1000
            else
                originPriority = math.floor(members[i+1])
            end

            if ( score + 0 >= 1000 ) then
                priority = -score - originPriority / 1000
            elseif ( score + 0 == 0 ) then
                priority = originPriority
            else
                originPriority = score 
                priority = score
            end
            redis.call('zadd', KEYS[1], priority, member)
            table.insert(result, member)
            table.insert(result, originPriority)
        end

        return result
        """
        members = self.execute_lua(lua_script, [key], _min, _max, start, count, score)
        return [(members[i].decode(), int(members[i + 1])) for i in range(0, len(members), 2)]

    def done(self, keys: list, *args) -> list:
        lua_script = """
        for i, member in ipairs(ARGV) do
            redis.call("zrem", KEYS[1], member)
            redis.call("sadd", KEYS[2], member)
        end
        """
        self.execute_lua(lua_script, keys, *args)



