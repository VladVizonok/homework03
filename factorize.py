from multiprocessing import Process
from time import time


def factorize(*numbers):
    result = []
    for num in numbers:
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        result.append(factors)

    return result


def fast_factorize(*numbers):
    processes = []
    for num in numbers:
        processes.append(Process(target=factorize, args=(num,)))

    [process.start() for process in processes]
    [process.join() for process in processes]
    [process.close() for process in processes]
    return processes


if __name__ == '__main__':

    timer = time()
    a, b, c, d  = factorize(128, 255, 99999, 10651060)
    print(f'Done by 1 process: {round(time() - timer, 4)}') 

    timer = time()
    a, b, c, d  = fast_factorize(128, 255, 99999, 10651060)
    print(f'Done by many processes: {round(time() - timer, 4)}') 

