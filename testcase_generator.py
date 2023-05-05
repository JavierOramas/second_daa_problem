import json
import numpy as np
from bruteforce import solve
from time import sleep
from multiprocessing import Pool


def generate_unitary_case(i):
    # to avoid same seed in multi-process threads
    sleep(10/i)
    print(f"Generating test case no. {i}")
    notes_length = np.random.randint(1, 25)
    n = np.zeros(notes_length)
    for j in range(notes_length):
        n[j] = np.random.randint(1, 100)
    return {'in': n, 'out': solve(n)}


def generate(num):

    tests = {}

    p = Pool(12)

    sols = p.map(generate_unitary_case, [i for i in range(num)])

    for i in range(len(sols)):
        tests[i] = sols[i]

    with open('tests.json', 'w') as f:
        json.dump(tests, f)


generate(100)
