import os
import asyncio
import queue
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import wraps
from typing import Callable

# Sistem kaynaklarına göre optimize edilmiş kuyruk boyutu
CPU_COUNT = os.cpu_count() or 1
TASK_QUEUE = queue.Queue(maxsize=CPU_COUNT * 10)  # Dinamik kuyruk boyutu

class DynamicResourceManager:
    def __init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=self._calc_threads())
        self.process_pool = ProcessPoolExecutor(max_workers=self._calc_processes())
        
    def _calc_threads(self):
        return min(32, (CPU_COUNT * 2) + 4)  # I/O bound optimizasyonu
        
    def _calc_processes(self):
        return max(1, CPU_COUNT - 1)  # 1 çekirdek sisteme ayır

def task_enqueuer(func: Callable) -> Callable:
    """Dekoratör: Fonksiyonu kuyruğa ekler ve loglar"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        print(f"🏁 Task {func.__name__} kuyruğa alındı")
        try:
            result = func(*args, **kwargs)
            duration = time.monotonic() - start
            print(f"✅ {func.__name__} başarıyla tamamlandı ({duration:.2f}s)")
            return result
        except Exception as e:
            print(f"⛔ {func.__name__} hatası: {str(e)}")
            raise
            
    TASK_QUEUE.put(wrapper)
    return wrapper

async def async_queue_consumer(res_manager: DynamicResourceManager):
    """Kuyruktaki task'ları akıllı dağıtımla işler"""
    results = []
    
    while not TASK_QUEUE.empty():
        task = TASK_QUEUE.get()
        try:
            # 1. ThreadPool'da dene (I/O optimizasyonu)
            future = res_manager.thread_pool.submit(task)
            result = await asyncio.wait_for(
                asyncio.wrap_future(future), 
                timeout=1.5
            )
            results.append(("thread", task.__name__, result))
            
        except asyncio.TimeoutError:
            # 2. Zaman aşımında ProcessPool'a aktar
            print(f"⚡ {task.__name__} CPU bound olarak işleniyor")
            future = res_manager.process_pool.submit(task)
            result = await asyncio.wrap_future(future)
            results.append(("process", task.__name__, result))
            
        except Exception as e:
            results.append(("error", task.__name__, str(e)))
            
        finally:
            TASK_QUEUE.task_done()
            
        # Sistem yükünü dengelemek için
        await asyncio.sleep(0.1)
        
    return results

# Örnek task tanımları
@task_enqueuer
def cpu_intensive():
    """CPU bound örnek task"""
    return sum(i*i for i in range(10**7))

@task_enqueuer
def io_operation():
    """I/O bound örnek task"""
    time.sleep(2)
    return "I/O işlemi tamam"

@task_enqueuer
def hybrid_task():
    """Karma yük örneği"""
    [time.sleep(0.1) for _ in range(10)]
    sum(range(10**6))  # CPU kısmı
    return "Hibrit işlem tamam"

async def main():
    print(f"🖥️ Sistem kaynakları: {CPU_COUNT} çekirdek")
    print("🚀 Task'lar işlenmeye başlıyor...\n")
    
    start_time = time.monotonic()
    res_manager = DynamicResourceManager()
    results = await async_queue_consumer(res_manager)
    
    # Sonuç analizi
    total_time = time.monotonic() - start_time
    print("\n📊 Performans Raporu:")
    print(f"Toplam süre: {total_time:.2f}s")
    print(f"İşlenen task sayısı: {len(results)}")
    print("\nDetaylar:")
    for res_type, name, _ in results:
        print(f"- {name:15} [{res_type.upper()}]")

if __name__ == "__main__":
    asyncio.run(main())