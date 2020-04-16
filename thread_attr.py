"""
线程属性
"""

from threading import Thread
from time import sleep


def fun():
    sleep(3)
    print("线程属性测试")


t = Thread(target=fun)

t.setDaemon(True)  # 该线程会随主线程退出

t.start()

t.setName("Tarena")
print(t.getName())

print(t.is_alive())
