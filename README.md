CoreFlow

Bu kütüphane, Python ile geliştirilen uygulamalarınızda asenkron iş yüklerinin dinamik biçimde işlenmesini sağlar. Thread ve process havuzları arasında otomatik geçiş yaparak I/O ve CPU yoğun işlemleri en uygun kaynaktan çalıştırır.

Özellikler

Dinamik Kaynak Yönetimi: Sistemde kullanılabilir çekirdek sayısına göre thread ve process havuzu boyutlarını otomatik ayarlar.

Esnek Görev Kuyruğu: Görevler, dekoratörler sayesinde tek satırda kuyruğa eklenir ve sonrasında toplu işlenir.

Zaman Aşımı Destekli Dağıtım: I/O ağırlıklı görevler thread havuzunda, zaman aşımında kalanlar otomatik olarak process havuzuna aktarılır.

Basit Kullanım: @async_task ve @async_task_await dekoratörleri ile görev ekleme, bekleme ve sonuç alma kolay.


Kullanım

1. Görevleri Kuyruğa Ekleme

@async_task dekoratörü ile işaretlenen fonksiyonlar, çağrıldıklarında kuyruğa eklenir:

from CoreFlow import async_task, async_task_await

@async_task
async def io_islemi():
    await asyncio.sleep(2)
    return "I/O tamam"

@async_task
def cpu_islem():
    return sum(i*i for i in range(10**7))

2. Kuyruk İşlenip Ardından Kritik Bölge

@async_task_await ile sarılan fonksiyon, çağrıldığında önce kuyruktaki tüm görevleri işler, sonra kendi gövdesini yürütür:

@async_task_await
async def finalize():
    print("Tüm görevler işlendi, kritik adım başladı.")
    return "Sonuç"

async def main():
    await io_islemi()
    await cpu_islem()
    sonuc = await finalize()
    print(sonuc)

3. Manuel Kuyruk İşleme

Dekoratör kullanmadan da kuyruğu doğrudan boşaltabilirsiniz:

from CoreFlow import DynamicResourceManager, process_queue

async def main():
    # görevleri ekleyin...
    manager = DynamicResourceManager()
    results = await process_queue(manager)
    print(results)

Örnek Proje

git clone https://github.com/rootburak/CoreFlow.py
python coreFlowSpeedTest.py

Katkı

Katkıda bulunmak isterseniz, issue açabilir veya pull request gönderebilirsiniz.
