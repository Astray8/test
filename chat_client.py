"""
chat room
客户端
功能: 发送请求,获取结果
"""

from socket import *
from multiprocessing import Process
import sys

# 服务器地址
ADDR = ("127.0.0.1", 8888)

# 敏感词
sensitive_word = ["xx", "aa", "bb", "oo"]


# 发送消息
def send_msg(s, name):
    while True:
        try:
            text = input("发言:")
        except:
            text = "quit"
        if text == "quit":
            msg = "Q " + name
            s.sendto(msg.encode(), ADDR)  # 告知服务端
            sys.exit("退出聊天室")  # 进程结束
        else:
            for i in sensitive_word:
                if i in text:
                    msg = "S %s %s" % (name, text)
                    s.sendto(msg.encode(), ADDR)
                else:
                    msg = "C %s %s" % (name, text)
                    s.sendto(msg.encode(), ADDR)


# 接收消息
def recv_msg(s):
    while True:
        data, addr = s.recvfrom(4096)
        if data.decode() == "Q":
            sys.exit("你已被踢出聊天室")

        print(data.decode() + "\n发言:", end="")  # 打印接收内容


# 创建网络结构
def main():
    s = socket(AF_INET, SOCK_DGRAM)
    # 进入聊天室
    while True:
        name = input("输入姓名:")
        msg = "L " + name  # 根据协议,组织消息格式
        s.sendto(msg.encode(), ADDR)  # 将姓名发送给服务端
        data, addr = s.recvfrom(128)  # 接收反馈
        if data.decode() == "OK":
            print("你已进入聊天室")
            break
        else:
            print(data.decode())

    # 创建一个新的进程
    p = Process(target=recv_msg, args=(s,))
    p.daemon = True  # 子进程随父进程退出而退出
    p.start()

    # 发送消息
    send_msg(s, name)  # 发送消息由父进程执行


if __name__ == "__main__":
    main()
