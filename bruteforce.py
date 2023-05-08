
from utils import condition

def find_all_sub_strings(notes, idx, sub_arr, found):
    # print(id)
    if idx == len(notes):
        if len(sub_arr) != 0:
            return sub_arr
    else:
        n_sub_arr = find_all_sub_strings(
            notes, idx+1, sub_arr, [])
        if n_sub_arr and condition(notes, n_sub_arr):
            found.append(n_sub_arr)
        n_sub_arr = find_all_sub_strings(
            notes, idx+1, sub_arr+[idx], [])
        if n_sub_arr and condition(notes, n_sub_arr):
            found.append(n_sub_arr)


def find_longest(notes):
    max_len = 0
    bests = []
    for i, num_1 in enumerate(notes):
        for j, num_2 in enumerate(notes):
            for k, num_3 in enumerate(notes):
                for l, num_4 in enumerate(notes):
                    if len(set([i, j, k, l])) == 4:
                        if len(set(num_1+num_2+num_3+num_4)) == len(num_1+num_2+num_3+num_4):
                            if len(num_1+num_2+num_3+num_4) > max_len:
                                max_len = len(num_1+num_2+num_3+num_4)
                                bests = [num_1, num_2, num_3, num_4]
    return max_len, bests


def solve(notes, verbose=1):
    # found[id] = []
    f = find_all_sub_strings(notes, 0, [], [])

    print(f)
    if verbose >= 2:
        print("substrings found:", f)
    sol, dat = find_longest(f)
    if verbose >= 2:
        print("best melodies:", dat)
    if verbose >= 1:
        print("best score:", sol)
    return sol


solve([1, 2, 3, 4, 5], 3)
