from bruteforce import solve
import json

with open('tests.json') as f:
    tests = json.load(f)

for i in tests:
    n = tests[i]['in']
    out = tests[i]['out']

    sol = solve(n)
    if out == sol:
        print(f'Test {i}... OK')
    else:
        print(f'Test {i}... FAILED')
        print(f'Expected {out}, got {sol}')
