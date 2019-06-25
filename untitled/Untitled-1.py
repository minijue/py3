import threading

def hello(name):
    global timer
    print("Hello")  # 定时器结束，运行指定语句

    timer = threading.Timer(0.5, hello) # 上一个定时器结束，需要创建新的定时器
    timer.start()


def click():
    global isstart, timer
    if not isstart:
        timer = threading.Timer(0.5, hello) # 创建定时器，定时0.5秒，结束后执行函数 hello
        timer.start()
    else:
        timer.cancel()

    isstart = not isstart

