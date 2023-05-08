def condition(notes, indexes):
    if len(indexes) == 1:
        return True
    for i in range(len(indexes)-1):
        if not cond_compare(notes[indexes[i]], notes[indexes[i+1]]):
            return False
    return True


def cond_compare(x, y):
    if x % 7 == y % 7:
        # print(True)
        return True
    if abs(x - y) == 1:
        # print(True)
        return True

    return False
