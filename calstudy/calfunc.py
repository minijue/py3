import random

if __name__ == '__main__':
    print("错误！不能执行库文件")
    exit(-1)

n0 = 0


def ranplus(t):
    global n0
    a = random.randint(1, 99)
    b = random.randint(0, 100 - a)
    while n0 > t and (b < 2 or a == 1):
        a = random.randint(1, 99)
        b = random.randint(0, 100 - a)
    if b < 2 or a == 1:
        n0 += 1
    return f'{a} + {b} ='


def ransub(t):
    a = random.randint(1, 100)
    b = random.randint(0, a)
    global n0
    while (a == b or b < 2) and n0 > t:  # 次数超过限制
        a = random.randint(1, 100)
        b = random.randint(0, a)
    if a == b or b < 2:
        n0 += 1
    return f'{a} - {b} ='


def ranmul(t):
    a = random.randint(1, 9)
    b = random.randint(0, 9)
    global n0
    while n0 > t and (b < 2 or a == 1):
        a = random.randint(1, 9)
        b = random.randint(0, 9)
    if b < 2 or a == 1:
        n0 += 1
    return f'{a} × {b} ='


def randiv(t):
    global n0
    a = random.randint(1, 9)
    b = random.randint(0, 9)
    while (a == 1 or b < 2) and n0 > t:  # 次数超过限制
        a = random.randint(1, 9)
        b = random.randint(0, 9)
    if a == 1 or b < 2:
        n0 += 1
    mod = [0] * (a - 1) + list(range(0, a-1))   # 随机选择一个余数，提高 0 的概率
    c = a * b + (random.choice(mod) if len(mod) > 0 else 0)
    return f'{c} ÷ {a} ='
