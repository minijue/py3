import random


def ranplus():
    a = random.randint(0, 99)
    b = random.randint(0, 99)
    return f'{a:2d} + {b:2d} ='


def ransub():
    a = random.randint(1, 100)
    b = random.randint(0, a)
    return f'{a:2d} - {b:2d} ='


def ranmul():
    a = random.randint(0, 9)
    b = random.randint(0, 9)
    return f'{a:2d} × {b:<2d} ='


def randivintbl():
    a = random.randint(1, 9)
    b = random.randint(0, 9)
    return f'{a * b:2d} ÷ {a:<2d} ='
