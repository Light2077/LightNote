import asyncio
import random
import time


def get_battle_ids():
    if random.random() < 0.3:
        print("give idx")
        return [1, 2]
    else:
        return []


async def auto_battle(idx):
    print("start battle id:", idx)
    for i in range(3):
        print(idx, i + 1)
        await asyncio.sleep(5)


async def main():
    for i in range(5):
        battle_ids = get_battle_ids()
        tasks = [asyncio.create_task(auto_battle(idx)) for idx in battle_ids]
        await asyncio.wait(tasks)
        time.sleep(3)


if __name__ == '__main__':
    # asyncio.run(main())
    pass
