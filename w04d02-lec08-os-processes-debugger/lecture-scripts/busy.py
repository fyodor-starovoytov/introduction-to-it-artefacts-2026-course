import os

count = 0

print("busy.py PID:", os.getpid(), flush=True)

while count < 1_0000_0000_0000:
    count = count + 1

print("busy.py finished")
