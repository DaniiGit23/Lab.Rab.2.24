# В программе будет два потока - производитель и потребитель. Производитель будет генерировать числа от 1 до N,
# а потребитель будет суммировать квадраты этих чисел.
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
from queue import Queue


class Producer(threading.Thread):
    def __init__(self, buffer, max_num):
        threading.Thread.__init__(self)
        self.buffer = buffer
        self.max_num = max_num

    def run(self):
        for num in range(1, self.max_num + 1):
            self.buffer.put(num)

        self.buffer.put(None)  # Сигнал конца генерации чисел


class Consumer(threading.Thread):
    def __init__(self, buffer):
        threading.Thread.__init__(self)
        self.buffer = buffer
        self.sum_of_squares = 0

    def run(self):
        while True:
            num = self.buffer.get()

            if num is None:
                break

            self.sum_of_squares += num ** 2

    def get_sum_of_squares(self):
        return self.sum_of_squares


if __name__ == '__main__':
    buffer = Queue()  # Создание буфера

    N = 10  # Максимальное число для расчета

    producer = Producer(buffer, N)
    consumer = Consumer(buffer)

    # Запуск производителя и потребителя
    producer.start()
    consumer.start()

    # Ожидание завершения работы потребителя
    consumer.join()

    # Получение результата
    result = consumer.get_sum_of_squares()
    print(f"Сумма квадратов чисел от 1 до {N}: {result}")
