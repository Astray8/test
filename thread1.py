"""
线程基础示例

流程与进程创建相同
"""
from threading import Thread
from time import sleep
import os

a = 1


# 线程执行函数
def music():
    for i in range(3):
        sleep(2)
        print(os.getpid(), "播放: 葫芦娃")
    global a
    a = 1000


# 创建线程对象
t = Thread(target=music)
t.start()  # 启动线程,执行music

for i in range(4):
    sleep(1)
    print(os.getpid(), "播放: 黑猫警长")

t.join()  # 回收线程
print("a:", a)
