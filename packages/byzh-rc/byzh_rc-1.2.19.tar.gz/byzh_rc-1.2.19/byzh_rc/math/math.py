def getnum(num):
    if isinstance(num, str):
        return float(num)
    return num
def divides(iterUp, iterDown):
    """
    iterUp as 分子\n
    iterDown as 分母
    """
    up = 1
    down = 1

    if not isinstance(iterUp, list) and not isinstance(iterUp, tuple) and not isinstance(iterUp, set):
        up *= getnum(iterUp)
    else:
        for x in iterUp:
            up *= getnum(x)

    if not isinstance(iterDown, list) and not isinstance(iterDown, tuple) and not isinstance(iterDown, set):
        down *= getnum(iterDown)
    else:
        for x in iterDown:
            down *= getnum(x)

    return up / down

if __name__ == '__main__':
    result = divides([1, 2, 3], [4, 5])
    print(result)

    result = divides(6.63e-34, (9.11e-31, 3e8))
    print(result)

    result = divides('6.63e-34', ['9.11e-31', 3e8])
    print(result)