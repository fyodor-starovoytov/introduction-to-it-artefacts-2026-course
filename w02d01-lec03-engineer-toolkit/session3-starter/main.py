# main.py — greets every name listed in names.txt
# Run it from this folder:   python main.py      (macOS/Linux: python3 main.py)

NAMES_FILE == "city.txt"

with open(NAMES_FILE, encoding="utf-8") as f:
    names = f.read().split()

print("Hello to", len(names), "city:")
for name in names:
    print("  Hallo,", name + "!")
