import json
import numpy as np
from bruteforce import solve
import min_cost_max_flow
from time import sleep
from multiprocessing import Pool


def generate_unitary_case(i, min_notes, max_notes):
    # to avoid same seed in multi-process threads
    # sleep(i/2)
    print(f"Generating test case no. {i}")
    notes_length = np.random.randint(min_notes, max_notes)
    n = np.zeros(notes_length)
    for j in range(notes_length):
        n[j] = np.random.randint(1, 10)

    sl = solve(n, verbose=0)
    print(sl)
    return {'in': n, 'out': sl}


def generate():

    min_notes = 4
    max_notes = 8
    no_tests = 10
    tests = {}

    sols = [generate_unitary_case(i, min_notes, max_notes)
            for i in range(1, no_tests+1)]

    for i in range(1, len(sols) + 1):
        # print(i, sols[i])
        sols[i]["in"] = list(sols[i]["in"])
        tests[i] = sols[i]

    with open('tests.json', 'w') as f:
        json.dump(tests, f)


generate()
