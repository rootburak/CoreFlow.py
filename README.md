CoreFlow.py - Advanced Task Orchestration System

(Türkçe açıklama aşağıda)
Technical Description (EN)

A high-performance Python task scheduler with dynamic resource allocation, automatically distributing workloads between ThreadPool (I/O-bound) and ProcessPool (CPU-bound) based on:

    Real-time system load analysis

    Hardware capability detection (CPU cores/RAM)

    Adaptive timeout thresholds

Teknik Açıklama (TR)

Python tabanlı akıllı iş yükü dağıtıcısı. Sistem kaynaklarını gerçek zamanlı analiz ederek:

    I/O bağımlı işleri ThreadPool'da

    CPU yoğun işleri ProcessPool'da
    otomatik olarak yönetir.

Key Features / Temel Özellikler
Feature	EN	TR
Auto-Scaling	Dynamically adjusts worker pools	Çalışan havuzunu otomatik ölçeklendirir
Smart Task Classification	Detects I/O vs CPU-bound operations	İşlem türünü otomatik tanır
Queue Optimization	Priority-based task distribution	Öncelikli kuyruk yönetimi
System Requirements / Sistem Gereksinimleri
bash

# EN:  
- Python 3.8+ (with asyncio support)  
- 4+ CPU cores recommended  

# TR:  
- Python 3.8+ (asyncio desteğiyle)  
- Önerilen: 4+ işlemci çekirdeği  

Sample Usage / Örnek Kullanım
python

# EN: Add tasks to queue  
@task_enqueuer  
def data_processing():  
    ...

# TR: Kuyruğa görev ekleme  
@task_enqueuer  
def veri_isleme():  
    ...  

Technical Advantages / Teknik Avantajlar

    EN: Zero external dependencies (Pure Python)
    TR: Harici bağımlılık yok (Saf Python)

    EN: Built-in load balancing
    TR: Dahili yük dengeleme

    EN: Detailed performance logging
    TR: Detaylı performans kayıtları
