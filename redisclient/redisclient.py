# -*- coding: utf-8 -*-
### author:chushiyan
### https://github.com/chushiyan/pytube-redis.git
### date:03.19.2019
### vesion:1.0.0

import redis


class RedisClient():
    def __init__(self, host, password, port, db):
        try:
            self.redisdb = redis.Redis(host=host, port=port, password=password, db=db)
        except Exception as e:
            print('Failed to connect redis.Check the information:%s' % e)

    def hash_get(self, name, k):
        res = self.redisdb.hget(name, k)
        if res:
            return res.decode()

    def hash_set(self, name, k, v):
        self.redisdb.hset(name, k, v)

    def hash_getall(self, name):
        res = self.redisdb.hgetall(name)
        data = {}
        if res:
            for k, v in res.items():
                k = k.decode()
                v = v.decode()
                data[k] = v
        return data

    def hash_del(self, name, k):
        res = self.redisdb.hdel(name, k)
        if res:
            print('Deleted successfully. ')
            return 1
        else:
            print('Delete failed.The key does not exist ')
            return 0

    @property
    def clean_redis(self):
        self.redisdb.flushdb()  # clear redis
        print('Success to clear.')
        return 0


# just for testing .
if __name__ == '__main__':
    client = RedisClient(host='localhost', port=6379, password='xxxxxx')
    urls = ["https://www.youtube.com/watch?v=2Uug_nVf56g",
            "https://www.youtube.com/watch?v=uj5-Ftd3VMg",
            "https://www.youtube.com/watch?v=SJTHseeWfoA",
            "https://www.youtube.com/watch?v=sbAUcyLqJiw",
            "https://www.youtube.com/watch?v=aKy9rhauAng"]

    # for url in urls:
    #     client.hash_set('jinyeyouxi', url,"False")

    data = client.hash_getall('jinyeyouxi')

    print(data)
