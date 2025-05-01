import asyncio
from CoreFlow import async_task, async_task_await
import time 
start = time.time()

@async_task
async def my_test():
    print("my test is running")
    result = 1
    for i in range(1, 100000 + 1):
        result *= i
    return result

@async_task
async def my_test1():
    return [i * i for i in range(10**6)]

@async_task
async def my_test2():
    return sum(range(10**7))

@async_task
async def my_test3():
    product = 1
    for i in range(1, 10**4): 
        product *= i
    return product

async def main():
    await my_test()
    await my_test1()
    await my_test2()
    await my_test3()
    print(f"bitti {time.time()-start}")

if __name__ == "__main__":
    asyncio.run(main())