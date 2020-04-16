"""
线程创建示例

创建多个线程,线程传参
"""
from threading import Thread
from time import sleep


# 带有参数的线程
def func(sec, name):
    print("分支线程开始执行")
    sleep(sec)
    print("%s执行完毕" % name)


# 创建多个线程
jobs = []
for i in range(5):
    t = Thread(target=func, args=(2,), kwargs={"name": "T%d" % i})
    jobs.append(t)  # 存入线程对象
    t.start()

for i in jobs:
    i.join()
