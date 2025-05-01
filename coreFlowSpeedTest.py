import asyncio
import time
from CoreFlow import async_task, async_task_await

@async_task
async def my_test():
    print("my_test çalışıyor")
    result = 1
    for i in range(1, 100_001):
        result *= i
    return result  # Bu çok büyük bir sayıdır

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

@async_task_await
async def finalize():
    print("🛠️ Tüm görevler işlendi, finalize içinde.")

async def main():
    start = time.time()

    # Kuyruğa ekle
    await my_test()
    await my_test1()
    await my_test2()
    await my_test3()

    # Kuyruk işlemesi ve sonuçların güvenli yazdırılması
    await finalize()

    print(f"🏁 Toplam süre: {time.time() - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
