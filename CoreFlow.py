import asyncio
import time
import os
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
        
    def _calc_threads(self):
        return min(32, (CPU_COUNT * 2) + 4)  # I/O bound optimizasyonu
        
    def _calc_processes(self):
        return max(1, CPU_COUNT - 1)  # 1 çekirdek sisteme ayır

def async_task(func):
    """Asenkron taskları yöneten dekoratör"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"🏁 {func.__name__} kuyruğa eklendi")
        await TASK_QUEUE.put((func, args, kwargs))
        return await func(*args, **kwargs)  # Bu satırı ekleyin
    return wrapper

def async_task_await(func: Callable) -> Callable:
    """Kuyruktaki tüm taskların bitmesini bekleyen dekoratör"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        print(f"⏳ {func.__name__} öncesi tasklar bekleniyor...")
        res_manager = DynamicResourceManager()
        await process_queue(res_manager)
        return await func(*args, **kwargs)
    return async_wrapper

async def process_task(func: Callable, args: tuple, kwargs: dict, res_manager: DynamicResourceManager) -> Any:
    """Tek bir taskı akıllı dağıtımla işler"""
    start = time.monotonic()
    try:
        # 1. ThreadPool'da dene (I/O optimizasyonu)
        future = res_manager.thread_pool.submit(func, *args, **kwargs)
        result = await asyncio.wait_for(
            asyncio.wrap_future(future), 
            timeout=1.5
        )
        duration = time.monotonic() - start
        print(f"✅ {func.__name__} tamamlandı ({duration:.2f}s)")
        return ("thread", func.__name__, result)
        
    except asyncio.TimeoutError:
        # 2. Zaman aşımında ProcessPool'a aktar
        print(f"⚡ {func.__name__} CPU bound olarak işleniyor")
        future = res_manager.process_pool.submit(func, *args, **kwargs)
        result = await asyncio.wrap_future(future)
        duration = time.monotonic() - start
        print(f"✅ {func.__name__} tamamlandı ({duration:.2f}s)")
        return ("process", func.__name__, result)
        
    except Exception as e:
        duration = time.monotonic() - start
        print(f"⛔ {func.__name__} hatası: {str(e)}")
        return ("error", func.__name__, str(e))

async def process_queue(res_manager: DynamicResourceManager):
    """Kuyruktaki tüm taskları işler ve sonuçları döndürür"""
    results = []
    while not TASK_QUEUE.empty():
        func, args, kwargs = await TASK_QUEUE.get()
        results.append(await process_task(func, args, kwargs, res_manager))
        TASK_QUEUE.task_done()
        await asyncio.sleep(0.1)  # Sistem yükünü dengelemek için
    return results

# Örnek kullanım
@async_task
async def cpu_yogun_islem():
    return sum(i*i for i in range(10**7))

@async_task
async def io_islemi():
    await asyncio.sleep(2)
    return "I/O operasyonu tamam"

@async_task_await
async def kritik_bolge():
    print("Tüm ön tasklar tamamlandı, kritik işlem yapılıyor...")
    return "Kritik işlem sonucu"

async def main():
    print(f"🖥️ Sistem kaynakları: {CPU_COUNT} çekirdek")
    start_time = time.monotonic()
    
    await cpu_yogun_islem()
    await io_islemi()
    
    sonuc = await kritik_bolge()
    print(sonuc)
    
    print(f"\n⏱️ Toplam süre: {time.monotonic() - start_time:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())