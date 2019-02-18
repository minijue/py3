def tonumlist(str):
    lst = str.split()
    if len(lst) == 1:
        lst = str.split(',')

    numlst = list(map(int, lst))
    return numlst
