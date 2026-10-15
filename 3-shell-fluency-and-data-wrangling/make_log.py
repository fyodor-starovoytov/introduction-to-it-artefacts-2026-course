#!/usr/bin/env python3
"""make_log.py — generate app.log, a deterministic one-million-line server log for Lecture 4.

Usage:  python3 make_log.py                 (writes app.log in the current directory, ~52 MB, ~10 s)
        python3 make_log.py 200000          (smaller file for slow machines)
        python3 make_log.py 1000000 7       (a DIFFERENT day: second argument = seed; incidents move)

Same seed -> same file on every machine (Python >= 3.10). The script prints the line
count and an MD5 checksum so you can check that your file matches the course file.

Format (single spaces, one event per line, in time order):
    TIMESTAMP LEVEL SERVICE MESSAGE...
    2026-09-13T00:00:00 INFO api GET /orders 200 23ms
    2026-09-13T02:13:04 ERROR payments db connection timeout after 5000ms
"""
import hashlib, random, sys
from datetime import datetime, timedelta

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 20260913
rng = random.Random(SEED)
DAY = datetime(2026, 9, 13)

SERVICES = ["api", "auth", "payments", "search"]
WEIGHTS  = [45, 15, 20, 20]
PATHS = {
    "api":      (["GET /orders", "POST /orders", "GET /products", "GET /cart"], [5, 2, 6, 3]),
    "auth":     (["POST /login", "POST /logout", "GET /me"], [4, 1, 5]),
    "payments": (["POST /pay", "GET /invoices"], [3, 2]),
    "search":   (["GET /search"], [1]),
}
MEDIAN_MS = {"api": 25, "auth": 18, "payments": 60, "search": 80}
BACKGROUND_ERRORS = {
    "api":      ["upstream 502 from inventory", "unhandled exception in handler"],
    "auth":     ["token store unreachable"],
    "payments": ["db connection timeout after 5000ms", "card gateway returned 503"],
    "search":   ["index unavailable"],
}
# The two planted incidents (start_second, end_second, service, message, error_rate)
_shift = 0 if SEED == 20260913 else (SEED * 37) % 20 * 3600   # a different seed also moves the incidents
INCIDENTS = [
    ((2*3600 + 13*60 + _shift) % 86400, (2*3600 + 41*60 + 59 + _shift) % 86400, "payments", "db connection timeout after 5000ms", 0.60),
    ((17*3600 + _shift) % 86400,        (17*3600 + 4*60 + 59 + _shift) % 86400,  "search",   "index unavailable",                 0.30),
]

def incident_for(sec, service):
    for start, end, svc, msg, rate in INCIDENTS:
        if svc == service and start <= sec <= end:
            return msg, rate
    return None, 0.0

seconds = sorted(rng.randrange(86400) for _ in range(N))
md5 = hashlib.md5()
with open("app.log", "w", newline="\n") as f:
    buf = []
    for sec in seconds:
        ts = (DAY + timedelta(seconds=sec)).strftime("%Y-%m-%dT%H:%M:%S")
        service = rng.choices(SERVICES, WEIGHTS)[0]
        msg, rate = incident_for(sec, service)
        r = rng.random()
        if msg and r < rate:
            line = f"{ts} ERROR {service} {msg}"
        elif r < 0.001:
            line = f"{ts} ERROR {service} {rng.choice(BACKGROUND_ERRORS[service])}"
        else:
            path = rng.choices(*PATHS[service])[0]
            ms = int(MEDIAN_MS[service] * 2.718281828 ** rng.gauss(0, 0.6)) + 1
            if r < 0.02 or ms >= 1000:
                line = f"{ts} WARN {service} slow response {path} {ms}ms"
            else:
                status = 404 if rng.random() < 0.03 else 200
                line = f"{ts} INFO {service} {path} {status} {ms}ms"
        buf.append(line + "\n")
        if len(buf) >= 50_000:
            chunk = "".join(buf); f.write(chunk); md5.update(chunk.encode()); buf = []
    chunk = "".join(buf); f.write(chunk); md5.update(chunk.encode())

print(f"wrote app.log: {N} lines, md5 {md5.hexdigest()}")
