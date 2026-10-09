import hashlib
import itertools
import tqdm

SUBSTITUTIONS = {
    'a': ['a', 'A', '4', '@'], 'A': ['a', 'A', '4', '@'],
    'b': ['b', 'B'],           'B': ['b', 'B'],
    'c': ['c', 'C'],           'C': ['c', 'C'],
    'd': ['d', 'D'],           'D': ['d', 'D'],
    'e': ['e', 'E', '3'],      'E': ['e', 'E', '3'],
    'f': ['f', 'F'],           'F': ['f', 'F'],
    'g': ['g', 'G'],           'G': ['g', 'G'],
    'h': ['h', 'H'],           'H': ['h', 'H'],
    'i': ['i', 'I', '1'],      'I': ['i', 'I', '1', '!'],
    'j': ['j', 'J', '!'],           'J': ['j', 'J', '!'],
    'k': ['k', 'K'],           'K': ['k', 'K'],
    'l': ['l', 'L', '1', '!'],  'L': ['l', 'L', '1', '!'],
    'm': ['m', 'M'],           'M': ['m', 'M'],
    'n': ['n', 'N'],           'N': ['n', 'N'],
    'o': ['o', 'O', '0'],      'O': ['o', 'O', '0'],
    'p': ['p', 'P'],           'P': ['p', 'P'],
    'q': ['q', 'Q'],           'Q': ['q', 'Q'],
    'r': ['r', 'R'],           'R': ['r', 'R'],
    's': ['s', 'S', '5', '$'], 'S': ['s', 'S', '5', '$'],
    't': ['t', 'T', '7'],      'T': ['t', 'T', '7'],
    'u': ['u', 'U'],           'U': ['u', 'U'],
    'v': ['v', 'V'],           'V': ['v', 'V'],
    'w': ['w', 'W'],           'W': ['w', 'W'],
    'x': ['x', 'X'],           'X': ['x', 'X'],
    'y': ['y', 'Y'],           'Y': ['y', 'Y'],
    'z': ['z', 'Z'],           'Z': ['z', 'Z'],
}

def generate_variations(word: str) -> set:
    base_cases = {word, word.lower(), word.upper(), word.capitalize()}

    variations = set()
    for w in base_cases:
        char_options = [SUBSTITUTIONS.get(char, [char]) for char in w]
        for combo in itertools.product(*char_options):
            variations.add("".join(combo))

    return variations

def read_passwords(file_name: str) -> list:
    with open(file_name, "r") as fh:
        return [line.strip() for line in fh]

def crack_sha1(password: str, file_name: str = "Pwdb_top-10000000.txt") -> str:

    password = password.strip()
    target_hash = hashlib.sha1(password.encode()).hexdigest()
    words = read_passwords(file_name)
    attempts = 0

    for word in tqdm.tqdm(words):
        candidates = generate_variations(word)

        for candidate in candidates:
            attempts += 1
            candidate_hash = hashlib.sha1(candidate.encode()).hexdigest()

            if candidate_hash == target_hash:
                return f"Password cracked: '{candidate}' in {attempts} attempts"

    return f"Not found. Total attempts: {attempts}"