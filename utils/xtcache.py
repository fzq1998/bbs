# coding:utf-8
import memcache
cache = memcache.Client(['127.0.0.1:11211'], debug=True)


# 设置缓存的函数，默认过期时间1分钟
def set(key=None, value=None, timeout=60):
    if key and value:
        result = cache.set(key, value, timeout)
        return result
    return False


# 从缓存中获取数据
def get(key=None):
    if key:
        return cache.get(key)
    return None


# 删除缓存
def delete(key=None):
    if key:
        cache.delete(key)
        return True
    return False