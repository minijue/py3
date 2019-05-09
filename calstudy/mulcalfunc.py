import random

if __name__ == '__main__':
    print("错误！不能执行库文件")
    exit(-1)


# 获得第一步计算的操作数和结果
def step1(c1):
    if c1 == 2:
        a1 = random.randint(1, 99)
        a2 = random.randint(0, 99 - a1)
        a = a1 + a2
    elif c1 == 3:
        a1 = random.randint(1, 99)
        a2 = random.randint(0, a1)
        a = a1 - a2
    elif c1 == 4:
        a1 = random.randint(1, 9)
        a2 = random.randint(1, 9)
        a = a1 * a2
    else:
        a2 = random.randint(1, 9)
        a1 = a2 * random.randint(1, 9)
        a = a1 // a2
    return a1, a2, a


def multical():
    c1 = random.randint(2, 5)
    c2 = random.randint(2, 5)
    eb = random.randint(0, 2)

    cs = ['', '', '+', '-', '×', '÷']

    a1, a2, a3 = 0, 0, 0

    if eb == 2 or (eb == 0 and ((c2 // 2) > (c1 // 2))):  # 先计算后面的算式
        a2, a3, a = step1(c2)

        if c1 == 2:  # 前面为加法
            a1 = random.randint(1, 100 - a)
        elif c1 == 3:  # 前面为减法
            a1 = random.randint(a, 100)
        elif c1 == 4:  # 前面为乘法
            while a > 9:  # 乘数不能大于9，重新生成后面的算式
                if c2 == 2:
                    a2 = random.randint(1, 9)
                    a3 = random.randint(0, 9 - a2)
                    a = a2 + a3
                elif c2 == 3:
                    a2 = random.randint(9, 100)
                    a3 = random.randint(a1 - 9, a2)
                    a = a2 - a3
                elif c2 == 4:
                    a2 = random.randint(1, 9)
                    a3 = random.randint(1, 9)
                    a = a2 * a3
                else:
                    pass
            a1 = random.randint(1, 9)
        else:  # 前面为除法
            while a > 9 or a == 0:  # 除数不能大于9或者等于0
                if c2 == 2:
                    a2 = random.randint(1, 9)
                    a3 = random.randint(0, 9 - a1)
                    a = a2 + a3
                elif c2 == 3:
                    a2 = random.randint(9, 100)
                    a3 = random.randint(a1 - 9, a1)
                    a = a2 - a3
                elif c2 == 4:
                    a2 = random.randint(1, 9)
                    a3 = random.randint(1, 9)
                    a = a2 * a3
                else:
                    pass
            a1 = a * random.randint(1, 9)
    else:  # 先计算前面的算式
        a1, a2, a = step1(c1)

        if c2 == 2:
            a3 = random.randint(1, 100 - a)
        elif c2 == 3:
            a3 = random.randint(0, a)
        elif c2 == 4:
            while a > 9:
                if c1 == 2:
                    a1 = random.randint(1, 9)
                    a2 = random.randint(0, 9 - a1)
                    a = a1 + a2
                elif c1 == 3:
                    a1 = random.randint(9, 100)
                    a2 = random.randint(a1 - 9, a1)
                    a = a1 - a2
                elif c1 == 4:
                    a1 = random.randint(1, 9)
                    a2 = random.randint(1, 9)
                    a = a1 * a2
                else:
                    pass
            a3 = random.randint(1, 9)
        else:
            a3 = random.randint(1, 9)
            while (a % a3) > 0 or (a // a3) > 9:
                b = a3 * random.randint(1, 9)
                if c1 == 2:
                    a1 = random.randint(0, b)
                    a2 = b - a1
                    a = a1 + a2
                elif c1 == 3:
                    a1 = random.randint(b, 100)
                    a2 = a1 - b
                    a = a1 - a2
                elif c1 == 4:
                    while (b % a1) > 0 or (b // a1) > 9:
                        a1 = random.randint(1, b)
                    a2 = b // a1
                    a = a1 * a2
                    a3 = random.randint(1, a if a < 9 else 9)
                else:
                    a3 = random.randint(1, a if a < 9 else 9)

    if eb == 1 and (c1 // 2) < (c2 // 2):
        return f'({a1} {cs[c1]} {a2}) {cs[c2]} {a3} ='
    elif eb == 2 and (c1 > c2 or (c2 == c1 and c1 % 2 == 1)):
        return f'{a1} {cs[c1]} ({a2} {cs[c2]} {a3}) ='
    else:
        return f'{a1} {cs[c1]} {a2} {cs[c2]} {a3} ='
