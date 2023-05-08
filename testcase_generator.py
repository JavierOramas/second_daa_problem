import json
import numpy as np
from bruteforce import solve
import min_cost_max_flow
from time import sleep
from multiprocessing import Pool


def generate_unitary_case(i):
    # to avoid same seed in multi-process threads
    # sleep(i/2)
    print(f"Generating test case no. {i}")
    notes_length = np.random.randint(1, 10)
    n = np.zeros(notes_length)
    for j in range(notes_length):
        n[j] = np.random.randint(1, 10)
    print(f"N: {n}")
    print("fast:")
    print(min_cost_max_flow.solve(n))
    print("slow:")
    print(solve(n))
    return {'in': n, 'out': solve(n, verbose=3)}


def generate(num):

    tests = {}

    # # concurreny bug, leave 1 thread now
    # p = Pool(1)

    sols = [generate_unitary_case(i) for i in range(1, num+1)]

    for i in range(len(sols)):
        # print(i, sols[i])
        tests[i] = sols[i]

    with open('tests.json', 'w') as f:
        json.dump(tests, f)


generate(10)
