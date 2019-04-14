import random

if __name__ == '__main__':
    print("错误！不能执行库文件")
    exit(-1)

n0 = 0  # 统计有0算式的数量
ns = 0  # 减法和除法中统计两个操作数相等的数量


def ranplus():
    global n0
    a, b = 0, 0
    start = 1 if n0 > 3 else 0  # 有0的算式不能超过3
    while a == b == 0 or a + b > 100:
        a = random.randint(start, 99)
        b = random.randint(start, 99)
    if a == 0 or b == 0:
        n0 += 1
    return f'{a} + {b} ='


def ransub():
    a, b = 0, 0
    global n0, ns
    start = 1 if n0 > 3 else 0  # 有0的算式不能超过3个
    while a == b and (ns > 2 or b == 0):  # 操作数都为0或者相同的次数超过限制
        a = random.randint(start, 100)
        b = random.randint(start, a)
    if a == 0 or b == 0:
        n0 += 1
    if a == b:
        ns += 1
    return f'{a} - {b} ='


def ranmul():
    a, b = 0, 0
    global n0
    start = 1 if n0 > 3 else 0  # 有0的算式不能超过3个
    while a == b == 0:  # 都是0无意义
        a = random.randint(start, 9)
        b = random.randint(start, 9)
    if a == 0 or b == 0:
        n0 += 1
    return f'{a} × {b} ='


def randivintbl():
    a, b = 0, 0
    global n0, ns
    start = 1 if n0 > 3 else 0  # 有0的算式不能超过3个
    while a == b and (ns > 2 or a == 0):  # 操作数都为0或者相同的次数超过限制
        a = random.randint(1, 9)
        b = random.randint(start, 9)
    if b == 0:
        n0 += 1
    if a == b:
        ns += 1
    return f'{a * b:} ÷ {a} ='

