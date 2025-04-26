import time
start = time.time()

def my_test():
    # Uzun süren bir işlem (örneğin, büyük bir sayı ile faktöriyel hesaplama)
    result = 1
    for i in range(1, 100000 + 1):
        result *= i
    time.sleep(10)  # 10 saniye bekleme ekleyerek süreyi uzatıyoruz
    return result

def my_test1():
    # Uzun süren bir işlem (örneğin, büyük bir liste oluşturma)
    result = [i * i for i in range(10**6)]  # 1 milyon elemanlı bir liste
    return result


def my_test2():
    # Uzun süren bir işlem (örneğin, büyük bir sayı ile toplama)
    total = 0
    for i in range(10**7):  # 10 milyon döngü
        total += i
    return total

def my_test3():
    # Uzun süren bir işlem (örneğin, büyük bir sayı ile çarpma)
    product = 1
    for i in range(1, 10**4):  
        product *= i
    return product

my_test()
my_test1()
my_test2()
my_test3()



print(time.time()-start)

