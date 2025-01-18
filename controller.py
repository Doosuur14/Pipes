#!/usr/bin/env python3


import os
import random
import signal
import sys
from subprocess import Popen, PIPE

processed_lines = 0

def sigusr1_handler(signum, frame):
    print(f"Processed {processed_lines} lines", file=sys.stderr)

signal.signal(signal.SIGUSR1, sigusr1_handler)

def main():
    global processed_lines

    pipe_a_read, pipe_a_write = os.pipe()
    pipe_b_read, pipe_b_write = os.pipe()
    pipe_c_read, pipe_c_write = os.pipe()

    # Fork process P1
    if os.fork() == 0:
        os.dup2(pipe_a_write, sys.stdout.fileno())
        os.close(pipe_a_read)
        os.close(pipe_b_read)
        os.close(pipe_b_write)
        os.close(pipe_c_read)
        os.close(pipe_c_write)
        try:
            os.execvp("python3", ["python3", "generator", str(random.randint(120, 180))]) 
        except FileNotFoundError:
            print("Error: generator.py not found")
            sys.exit(1)
        
    
    # Fork process P2
    if os.fork() == 0:
        os.dup2(pipe_b_read, sys.stdin.fileno())
        os.dup2(pipe_c_write, sys.stdout.fileno())
        os.close(pipe_a_read)
        os.close(pipe_a_write)
        os.close(pipe_b_write)
        os.close(pipe_c_read)
        os.execvp("/usr/bin/bc", ["bc"])
    
  
    os.close(pipe_a_write)
    os.close(pipe_b_read)
    os.close(pipe_c_write)

   
    with os.fdopen(pipe_a_read, "r") as pipe_a, \
         os.fdopen(pipe_b_write, "w") as pipe_b, \
         os.fdopen(pipe_c_read, "r") as pipe_c:

        for line in pipe_a:
            pipe_b.write(line)
            pipe_b.flush()
            result = pipe_c.readline().strip()
            print(f"{line.strip()} = {result}")
            processed_lines += 1

    os.wait()
    os.wait()

if __name__ == "__main__":
    main()
