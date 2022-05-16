https://docs.python.org/3/library/unittest.html

命令行运行

```
python -m unittest tests/test_something.py
```



异步测试

https://docs.aiohttp.org/en/stable/testing.html

```python
from unittest import IsolatedAsyncioTestCase
events = []
class Test(IsolatedAsyncioTestCase):
    def setUp(self):
        events.append("setUp")

    async def asyncSetUp(self):
        self._async_connection = await AsyncConnection()
        events.append("asyncSetUp")

    async def test_response(self):
        events.append("test_response")
        response = await self._async_connection.get("https://example.com")
        self.assertEqual(response.status_code, 200)
        self.addAsyncCleanup(self.on_cleanup)

    def tearDown(self):
        events.append("tearDown")

    async def asyncTearDown(self):
        await self._async_connection.close()
        events.append("asyncTearDown")

    async def on_cleanup(self):
        events.append("cleanup")
```

