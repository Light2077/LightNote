https://blog.csdn.net/hhs_1996/article/details/119876521

```python
from collections import OrderedDict, defaultdict
 
class LRU:
    def __init__(self, capacity=128):
        self.capacity = capacity    # 缓存容量
        self.cache = OrderedDict()  # 有序字典缓存
 
    def put(self, key, value):
        """数据录入缓存"""
        if key in self.cache:
            # 若数据已存在，表示命中一次，需要把数据移到缓存队列末端
            self.cache.move_to_end(key)
            return
        if len(self.cache) >= self.capacity:
            # 若缓存已满，则需要淘汰最早没有使用的数据
            self.cache.popitem(last=False)
        # 录入缓存
        self.cache[key]=value
 
    def travel(self):
        """遍历key"""
        for key in self.cache.keys():
            print(key)
 
if __name__ == '__main__':
    l = LRU(3)       # 实例化缓存容量为3
    l.put('a','aa')  # 此时缓存未满，则录入数据a
    l.put('b','bb')  # 此时缓存未满，则录入数据b
    l.put('c','cc')  # 此时缓存未满，则录入数据c
    l.put('a','aa')  # 此时缓存已满，但是a已存在缓存中，则命中一次
    # l.travel()     # 输出 b c a
    l.put('d','dd')  # 此时缓存已满，淘汰掉最久不用的b
    l.travel()       # 输出 c a d
```

