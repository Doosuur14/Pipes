#!/usr/bin/env python3


import sys
import random
import time

def main():
    if len(sys.argv) != 2:
        print("Usage: generator <N>")
        sys.exit(1)

    try:
        N = int(sys.argv[1])
    except ValueError:
        sys.exit(1)

    if not (120 <= N <= 180):
        sys.exit(1)

    operators = ['+', '-', '*', '/']
    for _ in range(N):
        x = random.randint(1, 9)
        y = random.randint(1, 9)
        operator = random.choice(operators)
        print(f"{x} {operator} {y}")
        time.sleep(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
