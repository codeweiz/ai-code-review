from collections import OrderedDict


class LRUCache:
    """本地 LRU 缓存实现"""

    def __init__(self, max_size: int = 5000):
        self.cache: OrderedDict[str, str] = OrderedDict()
        self.max_size = max_size

    def get(self, key: str) -> str | None:
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def set(self, key: str, value: str):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.max_size:
            # 超过 max_size，淘汰最旧的
            self.cache.popitem(last=False)
