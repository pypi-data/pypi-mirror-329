
from backend.config import REDIS_CONFIG
from redis import Redis
import json


class Memory(object):
    def __init__(self, config):
        self.instance = Redis(decode_responses=True, **config)

    def get(self, k):
        """获取值
        c.get('access_token_00b73bbe23f34a468b2a5f158701f17f_wx')
        """
        v = self.instance.get(k)
        return json.loads(v)

    def set(self, k, v, seconds=0):
        """修改值
        c.get('access_token_00b73bbe23f34a468b2a5f158701f17f_wx')
        """
        v = json.dumps(v, ensure_ascii=False)
        self.instance.set(k, v)
        if seconds != 0:
            self.expire(k, seconds)

    def hget(self, name, k):
        """获取值
        c.get('access_token_00b73bbe23f34a468b2a5f158701f17f_wx')
        """
        return self.instance.hget(name, k)
    
    def rpop(self, k):
        return self.instance.rpop(k)

    def remove(self, k):
        """修改值
        c.get('access_token_00b73bbe23f34a468b2a5f158701f17f_wx')
        """
        return self.instance.delete(k)

    def expire(self, k, seconds):
        """设置过期时间"""
        self.instance.expire(k, seconds)


def get_cache():
    return Memory(REDIS_CONFIG)




