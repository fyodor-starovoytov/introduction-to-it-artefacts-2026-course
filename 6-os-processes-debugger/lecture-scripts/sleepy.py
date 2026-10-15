import os
import time

print("sleepy.py PID:", os.getpid(), flush=True)

for check_number in range(1, 11):
    print("check", check_number, "of 10", flush=True)
    time.sleep(1)
