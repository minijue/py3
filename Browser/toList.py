def tonumlist(str):  # 将字符串列表转换为数字列表
    lst = str.split()
    if len(lst) == 1:
        lst = str.split(',')

    numlst = list(map(int, lst))
    return numlst


if __name__ == '__main__':
    print("Please use me as a module.")
