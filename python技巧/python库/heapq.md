插入：`heappush(heap, x)`

删除：`heappop(heap)`

`heapfiy(heap)` 把一个列表调整成堆

`heapreplace(heap, x)` 弹出最小的元素，插入最大的元素

`nlargest(n, iter)`

`nsmallest(n, iter) `

```python
nums = []

lo, hi = 0, len(nums)
while lo < hi:
    mid = (lo + hi) // 2
    if x < nums[mid]:
        hi = mid
    else:
        lo = mid + 1
return hi
```







