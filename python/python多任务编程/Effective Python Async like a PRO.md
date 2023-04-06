

# 像大佬一样高效使用python异步语法（Effective Python Async like a PRO🐍🔀）

[原文地址](https://guicommits.com/effective-python-async-like-a-pro/)

> 译者注💡：本文非机翻

我发现有些人在用异步语法的时候其实**并不知道他们在做什么**。

首先，他们错误地认为异步（async）就是并行（parallel），**[这篇文章](https://guicommits.com/how-python-async-works/)**解释了为什么异步≠并行。

他们写的代码并没有体现python异步语法的优势。换句话说，他们在用异步语法写同步的代码。

这篇文章的目的就是为了指出这些错误写法导致的性能问题，并帮助你从异步代码中获得更多好处。

## 🤔什么时候使用python异步

****

**只有在进行I/O操作时，异步才有意义。**

对于下面这种CPU密集型任务，异步就没啥用。

```python
import asyncio


async def sum_two_numbers_async(n1: int, n2: int) -> int:
    return n1 + n2


async def main():
    await sum_two_numbers_async(2, 2)
    await sum_two_numbers_async(4, 4)


asyncio.run(main())
```

由于*事件循环机制*，你的代码甚至可能会变慢。

这是因为**Python异步只优化空闲时间！**

> 💡译者注
>
> 这里的空闲时间（原文IDLE time）指的是CPU空闲时间，也就是说当CPU在工作时，CPU是没有空闲时间的，就不能用CPU去做别的工作。
>
> 而python异步的特点就是能够充分地利用CPU的空闲时间

如果你还不熟悉上述概念，可以先读读这篇文章：[Async python in real life🐍🔀](https://guicommits.com/async-python-in-real-life/)

IO-bound操作与读写操作相关，比如：

- 向HTTP请求某些数据
- 读写JSON或TXT文件
- 从数据库读取数据

👆所有这些操作都需要等待数据可用

当数据不可用时，事件循环（EVENT LOOP）会执行其他操作。

这就是并发（Concurrency）。

**而不是**并行（Parallelism）。

## 🖼️ Python Async Await 的案例

接下来从下面的场景开始

现在需要构建一个简单的宝可梦图鉴，可以同时查询3只宝可梦（这样才能提现异步的优势）。

查询完宝可梦后，构建一个宝可梦对象，步骤对应的操作类型如下：

| 步骤                                     | 操作类型  |
| ---------------------------------------- | --------- |
| 向[pokeapi](https://pokeapi.co/)发送请求 | IO-bound  |
| 构建一个宝可梦数据对象                   | CPU-bound |

## 🐌 使用 Python `async` 和 `await`

接下来的这段代码，是很多人都自豪地写过的“异步代码“

首先花点去构思一下这段代码：

- 模型类
- 函数：`parse_pokemon()`（CPU-bound）
- 函数：`get_pokemon()`（IO-bound）
- 函数：`get_all()`

```python
import asyncio
from datetime import timedelta
import time
import httpx
from pydantic import BaseModel

class Pokemon(BaseModel): # 👈 Defines model to parse pokemon
    name: str
    types: list[str]

def parse_pokemon(pokemon_data: dict) -> Pokemon: # 👈 CPU-bound operation
    print("🔄 Parsing pokemon")

    poke_types = []
    for poke_type in pokemon_data["types"]:
        poke_types.append(poke_type["type"]["name"])

    return Pokemon(name=pokemon_data['name'], types=poke_types)

async def get_pokemon(name: str) -> dict | None: # 👈 IO-bound operation
    async with httpx.AsyncClient() as client:
        print(f"🔍 Querying for '{name}'")
        resp = await client.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
        print(f"🙌 Got data for '{name}'")

        try:
            resp.raise_for_status()

        except httpx.HTTPStatusError as err:
            if err.response.status_code == 404:
                return None

            raise

        else:
            return resp.json()

async def get_all(*names: str): # 👈 Async
    started_at = time.time()

    for name in names: # 👈 Iterates over all names
        if data := await get_pokemon(name): # 👈 Invokes async function
            pokemon = parse_pokemon(data)
            print(f"💁 {pokemon.name} is of type(s) {','.join(pokemon.types)}")
        else:
            print(f"❌ No data found for '{name}'")

    finished_at = time.time()
    elapsed_time = finished_at - started_at
    print(f"⏲️ Done in {timedelta(seconds=elapsed_time)}")


POKE_NAMES = ["blaziken", "pikachu", "lugia", "bad_name"]
asyncio.run(get_all(*POKE_NAMES))
```

代码运行的输出：

```
🔍 Querying for 'blaziken'
🙌 Got data for 'blaziken'
🔄 Parsing pokemon
💁 blaziken is of type(s) fire,fighting

🔍 Querying for 'pikachu'
🙌 Got data for 'pikachu'
🔄 Parsing pokemon
💁 pikachu is of type(s) electric

🔍 Querying for 'lugia'
🙌 Got data for 'lugia'
🔄 Parsing pokemon
💁 lugia is of type(s) psychic,flying

🔍 Querying for 'bad_name'
🙌 Got data for 'bad_name'
❌ No data found for 'bad_name'

⏲️ Done in 0:00:02.152331
```

以上这段代码是反面教材

仔细看看输出就能发现，实际上代码是在一个一个请求数据，因此用不用异步语法都无法节约时间。

> 💡译者注：
>
> 注意到输出里每次都是顺序地`Querying for xx`然后`Parsing xx`，实际上并没有实现并发的效果。

让我们改进代码！🧑‍🏭

## 使用Python的 `asyncio.create_task`和`asyncio.gather`

如果想同时运行2个以上的函数，需要使用`asyncio.create_task`

创建一个任务（task）会触发异步操作，并且需要在某个时刻等待执行它。

例如：

```python
task = create_task(my_async_function('arg1'))
result = await task
```

当我们创建了许多任务时，需要使用`asyncio.gather`一次性等待所有任务被执行完。

更新后的代码如下（关注`get_all()`函数）

```python
import asyncio
from datetime import timedelta
import time
import httpx
from pydantic import BaseModel

class Pokemon(BaseModel):
    name: str
    types: list[str]

def parse_pokemon(pokemon_data: dict) -> Pokemon:
    print("🔄 Parsing pokemon")

    poke_types = []
    for poke_type in pokemon_data["types"]:
        poke_types.append(poke_type["type"]["name"])

    return Pokemon(name=pokemon_data['name'], types=poke_types)

async def get_pokemon(name: str) -> dict | None:
    async with httpx.AsyncClient() as client:
        print(f"🔍 Querying for '{name}'")
        resp = await client.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
        print(f"🙌 Got data for '{name}'")

        try:
            resp.raise_for_status()

        except httpx.HTTPStatusError as err:
            if err.response.status_code == 404:
                return None

            raise

        else:
            return resp.json()

async def get_all(*names: str):
    started_at = time.time()

    # 👇 Create tasks, so we start requesting all of them concurrently
    tasks = [asyncio.create_task(get_pokemon(name)) for name in names]

    # 👇 Await ALL
    results = await asyncio.gather(*tasks)

    for result in results:
        if result:
            pokemon = parse_pokemon(result)
            print(f"💁 {pokemon.name} is of type(s) {','.join(pokemon.types)}")
        else:
            print(f"❌ No data found for...")

    finished_at = time.time()
    elapsed_time = finished_at - started_at
    print(f"⏲️ Done in {timedelta(seconds=elapsed_time)}")


POKE_NAMES = ["blaziken", "pikachu", "lugia", "bad_name"]
asyncio.run(get_all(*POKE_NAMES))
```

输入如下

```python
🔍 Querying for 'blaziken'
🔍 Querying for 'pikachu'
🔍 Querying for 'lugia'
🔍 Querying for 'bad_name'

🙌 Got data for 'lugia'
🙌 Got data for 'blaziken'
🙌 Got data for 'pikachu'
🙌 Got data for 'bad_name'

🔄 Parsing pokemon
💁 blaziken is of type(s) fire,fighting
🔄 Parsing pokemon
💁 pikachu is of type(s) electric
🔄 Parsing pokemon
💁 lugia is of type(s) psychic,flying
❌ No data found for...

⏲️ Done in 0:00:00.495780
```

通过正确使用python异步语法，消耗的时间**从2s优化到了500ms**

注意：

- 代码同时查询了所有宝可梦数据（`blaziken`是第一个被查询的）
- 当数据可用时，以随机顺序检索数据（现在变成`lugia`是第一个了）
- 按顺序解析数据（反正这一步受限于CPU性能）

## 使用Python的`asyncio.as_completed`

有时候，并不需要等待每个任务都被处理完毕。

上面的场景就是这样，可以在得到第一个宝可梦的数据后立即开始进行解析。

用`asyncio.as_completed`可以实现这一点，该函数返回一个包含已完成的协程的生成器：

```python
import asyncio
from datetime import timedelta
import time
import httpx
from pydantic import BaseModel

class Pokemon(BaseModel):
    name: str
    types: list[str]

def parse_pokemon(pokemon_data: dict) -> Pokemon:
    print(f"🔄 Parsing pokemon '{pokemon_data['name']}'")

    poke_types = []
    for poke_type in pokemon_data["types"]:
        poke_types.append(poke_type["type"]["name"])

    return Pokemon(name=pokemon_data['name'], types=poke_types)

async def get_pokemon(name: str) -> dict | None:
    async with httpx.AsyncClient() as client:
        print(f"🔍 Querying for '{name}'")
        resp = await client.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
        print(f"🙌 Got data for '{name}'")

        try:
            resp.raise_for_status()

        except httpx.HTTPStatusError as err:
            if err.response.status_code == 404:
                return None

            raise

        else:
            return resp.json()

async def get_all(*names: str):
    started_at = time.time()

    tasks = [asyncio.create_task(get_pokemon(name)) for name in names]

    # 👇 Process the tasks individually as they become available
    for coro in asyncio.as_completed(tasks):
        result = await coro # 👈 You still need to await

        if result:
            pokemon = parse_pokemon(result)
            print(f"💁 {pokemon.name} is of type(s) {','.join(pokemon.types)}")
        else:
            print(f"❌ No data found for...")

    finished_at = time.time()
    elapsed_time = finished_at - started_at
    print(f"⏲️ Done in {timedelta(seconds=elapsed_time)}")


POKE_NAMES = ["blaziken", "pikachu", "lugia", "bad_name"]
asyncio.run(get_all(*POKE_NAMES))
```

输出，不过这次改进后的优势不是很明显

```python
🔍 Querying for 'blaziken'
🔍 Querying for 'pikachu'
🔍 Querying for 'lugia'
🔍 Querying for 'bad_name'

🙌 Got data for 'blaziken'
🔄 Parsing pokemon 'blaziken'
💁 blaziken is of type(s) fire,fighting
🙌 Got data for 'bad_name'
🙌 Got data for 'lugia'
🙌 Got data for 'pikachu'
❌ No data found for...
🔄 Parsing pokemon 'lugia'
💁 lugia is of type(s) psychic,flying
🔄 Parsing pokemon 'pikachu'
💁 pikachu is of type(s) electric

⏲️ Done in 0:00:00.316266
```

上面的代码还是一次性查询了所有的宝可梦

现在查询之后的数据解析顺序就完全混乱了。

这意味着Python在数据可用时立即处理数据，为其他请求留出足够的时间以后完成。

如果你能理解什么时候该用，为什么该用async、await、create_task、gather和as_completed

**那你会成为一名更优秀的开发人员。**

这篇文章是我正在写的书的一部分，如果你想从“代码能用就行”进阶到“优秀的代码”，可以去看看我写的这本书：[Python Like a PRO 🐍📚 Book](https://guilatrova.gumroad.com/l/python-like-a-pro)

## 🔀 真实场景下 Async IO 的使用

我目前在另一家旧金山的初创公司[Silk Security](https://silk.security/)工作，我们非常依赖第三方集成和他们的API。

我们需要尽可能快地请求大量数据。

例如通过请求[Snyk的API](https://snyk.docs.apiary.io/)以收集代码漏洞。

[Snyk](https://snyk.io/)的数据由包含许多项目的组织组成，每个项目又有很多问题。

这意味着我们需要列出所有的项目和组织，然后才能获取任何问题。

情况就像是：

![snyk-overview](images/snyk-overview.svg)

你看我们得做多少个请求！我们并发地进行这些请求。

并且需要小心API可能会抛出的速率限制问题。可以通过限制单次查询的数量的方式解决这个问题，并在查询更多数据之前开始运行一些处理。

这样能够节约时间，并避免了API的任何速率限制。

下面是一个真实项目中运行的代码片段（已经过编辑）：

```python
def _iter_grouped(self, issues: list[ResultType], group_count: int):
    group_count = min([len(issues), group_count])

    return zip(*[iter(issues)] * group_count)


async def get_issue_details(self):
    ...

    # NOTE: We need to be careful here, we can't create tasks for every issue or Snyk will raise 449
    # Instead, let's do it in chunks, and let's yield as it's done, so we can spend some time processing it
    # and we can query Snyk again.
    chunk_count = 4 # 👈 Limit to 4 queries at a time
    coro: Awaitable[tuple[ResultType | None]]
    for issues in self._iter_grouped(issues, chunk_count):
        tasks = [asyncio.create_task(self._get_data(project, issue)) for issue in issues]

        for coro in asyncio.as_completed(tasks):
            issue, details = await coro

            yield issue, details
```

可以表示成这样：

![snyk-rate-limit-1](images/snyk-rate-limit-1.svg)

如果你今天学到了新的东西，考虑在[Twitter](https://twitter.com/intent/user?screen_name=guilatrova)上关注我。我经常分享Python内容和酷炫的项目。欢迎通过私信给我反馈。

> 译者注💡：
>
> 译者也顺便求个点赞，如果你在学习python数据科学，这里有我的绝赞numpy学习项目，可以直接在线阅读和执行代码：
>
> 🎨[【画学numpy】3小时，让你看画快速入门numpy](https://aistudio.baidu.com/aistudio/projectdetail/5714994)【[GitHub](https://github.com/Light2077/drawing_and_studying_numpy)】