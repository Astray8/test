"""
chat room
env: python 3.6
socket udp and process
"""

from socket import *
from multiprocessing import Process

# 服务器地址
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)

# 用户信息存储{name:address}
user = {}

# 警告列表
warning = {}


# 处理进入聊天室
def do_login(s, name, address):
    if name in user or "管理" in name:
        s.sendto("该用户名已经存在".encode(), address)
        return
    else:
        s.sendto("OK".encode(), address)
        # 告知其他人
        msg = "\n欢迎%s进入聊天室" % name
        for i in user:
            s.sendto(msg.encode(), user[i])
        user[name] = address  # 字典中增加一项
        warning[name] = 0


# 处理聊天
def do_chat(s, name, text):
    msg = "\n%s : %s" % (name, text)
    for i in user:
        # 除去本人
        if i != name:
            s.sendto(msg.encode(), user[i])


# 退出聊天室
def do_quit(s, name):
    del user[name]  # 删除用户
    msg = "\n%s 退出聊天室" % name
    for i in user:
        s.sendto(msg.encode(), user[i])


# 发言警告
def do_warning(s, name):
    msg = "\n请成员%s注意聊天用语,文明发言,若发现三次,将被踢出本群" % name
    for i in user:
        s.sendto(msg.encode(), user[i])
    warning[name] += 1
    if warning[name] > 3:
        s.sendto(b"Q",user[name])
        del user[name]  # 踢出群聊
        msg = "\n%s 被踢出聊天室" % name
        for i in user:
            s.sendto(msg.encode(), user[i])


# 发送管理员消息
def manager(s):
    while True:
        msg = input("管理员消息:")
        msg = "C 管理员 " + msg
        s.sendto(msg.encode(), ADDR)  # 从父进程将消息发送给子进程


# 接收各个客户端请求
def request(s):
    while True:
        data, addr = s.recvfrom(1024)  # 接收请求
        tmp = data.decode().split(" ", 2)  # 对请求解析
        if tmp[0] == "L":
            # 处理进入聊天室 tmp --> ["L","name"]
            do_login(s, tmp[1], addr)
        elif tmp[0] == "C":
            # 处理聊天 tmp --> [C,name,text]
            do_chat(s, tmp[1], tmp[2])
        elif tmp[0] == "Q":
            # 处理退出 tmp --> [Q,name]
            do_quit(s, tmp[1])
        elif tmp[0] == "S":
            do_warning(s, tmp[1])


# 搭建基本结构
def main():
    # 创建一个udp套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)

    # 创建新的进程
    p = Process(target=request, args=(s,))
    p.start()

    manager(s)  # 发送管理员消息

    p.join()


if __name__ == "__main__":
    main()
