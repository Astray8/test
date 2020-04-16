from threading import Thread
from time import sleep

ticket = ["T%d" % i for i in range(1, 501)]


def func(name):
    try:
        while ticket:
            sleep(0.1)
            print("%s窗口已售出%s票" % (name, ticket.pop(0)))
    except:
        print("余票不足")


jobs = []
for i in range(1, 11):
    t = Thread(target=func, args=("w%d" % i,))
    jobs.append(t)
    t.start()

for i in jobs:
    i.join()
