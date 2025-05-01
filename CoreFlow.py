import asyncio
import time
import os
import inspect
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import wraps
from typing import Callable, Any

# Sistem kaynaklarına göre optimize edilmiş parametreler
CPU_COUNT = os.cpu_count() or 1
TASK_QUEUE = asyncio.Queue(maxsize=CPU_COUNT * 10)

class DynamicResourceManager:
    def __init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=self._calc_threads())
        self.process_pool = ProcessPoolExecutor(max_workers=self._calc_processes())

    def _calc_threads(self) -> int:
        return min(32, (CPU_COUNT * 2) + 4)

    def _calc_processes(self) -> int:
        return max(1, CPU_COUNT - 1)

def async_task(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> None:
        print(f"🏁 {func.__name__} kuyruğa eklendi")
        await TASK_QUEUE.put((func, args, kwargs))
    return wrapper

def async_task_await(func: Callable) -> Callable:
    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        print(f"⏳ {func.__name__} öncesi tasklar bekleniyor...")
        res_manager = DynamicResourceManager()
        results = await process_queue(res_manager)

        # Sonuçları güvenli bas:
        for kind, name, result in results:
            if isinstance(result, int) and result.bit_length() > 1024:
                # Çok büyük bir int ise uzunluğu göster
                print(f"🗂️ [{kind}] {name} → <big int: {result.bit_length()} bits>")
            else:
                print(f"🗂️ [{kind}] {name} → {result!r}")

        return await func(*args, **kwargs)
    return async_wrapper

async def process_task(
    func: Callable, args: tuple, kwargs: dict, res_manager: DynamicResourceManager
) -> Any:
    start = time.monotonic()
    try:
        future = res_manager.thread_pool.submit(func, *args, **kwargs)
        result = await asyncio.wait_for(asyncio.wrap_future(future), timeout=1.5)
        if inspect.iscoroutine(result):
            result = await result
        dur = time.monotonic() - start
        print(f"✅ [thread] {func.__name__} tamamlandı ({dur:.2f}s)")
        return ("thread", func.__name__, result)

    except asyncio.TimeoutError:
        print(f"⚡ [process] {func.__name__} CPU-bound işleniyor")
        future = res_manager.process_pool.submit(func, *args, **kwargs)
        result = await asyncio.wrap_future(future)
        if inspect.iscoroutine(result):
            result = await result
        dur = time.monotonic() - start
        print(f"✅ [process] {func.__name__} tamamlandı ({dur:.2f}s)")
        return ("process", func.__name__, result)

    except Exception as e:
        dur = time.monotonic() - start
        print(f"⛔ [error] {func.__name__}: {e} ({dur:.2f}s)")
        return ("error", func.__name__, str(e))

async def process_queue(res_manager: DynamicResourceManager):
    results = []
    print(f"🔄 process_queue başladı, sıra uzunluğu: {TASK_QUEUE.qsize()}")
    while not TASK_QUEUE.empty():
        func, args, kwargs = await TASK_QUEUE.get()
        results.append(await process_task(func, args, kwargs, res_manager))
        TASK_QUEUE.task_done()
        await asyncio.sleep(0.1)
    print("✅ process_queue tamamlandı.")
    return results
