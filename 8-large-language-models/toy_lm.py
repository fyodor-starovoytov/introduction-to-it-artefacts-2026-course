#!/usr/bin/env python3
# toy_lm.py — a language model small enough to read in five minutes.
# It learns ONE thing from a text: which word tends to follow which words. Then it writes by repeatedly
# choosing a likely next word. A real LLM does the same job ("predict the next token") with a neural network of
# billions of numbers instead of a table of counts, trained on a large part of the internet instead of one lecture.
#
#   python3 toy_lm.py --next "the receiver"              which words followed "the receiver", and how often?
#   python3 toy_lm.py --write "the packet" --seed 1      let it write 40 words
#   python3 toy_lm.py --write "the packet" --temperature 0.2     cautious: almost always the most likely word
#   python3 toy_lm.py --write "the packet" --temperature 1.5     adventurous: unlikely words get a bigger chance
import argparse, collections, random, re

p = argparse.ArgumentParser()
p.add_argument("--corpus", default="corpus.txt", help="the text it learns from (default: the Security Fundamentals lecture, the Bible and the Constitution of Finland (in English))")
p.add_argument("--context", type=int, default=2, help="how many previous words it looks at (1 or 2)")
p.add_argument("--next", metavar="WORDS", help="show the most likely next words after WORDS")
p.add_argument("--write", metavar="START", help="write text starting with START")
p.add_argument("--words", type=int, default=80)
p.add_argument("--temperature", type=float, default=1.0)
p.add_argument("--seed", type=int, default=None, help="same seed = same text (randomness made repeatable)")
a = p.parse_args()

TOKEN = re.compile(r"[a-z0-9]+(?:[-'.][a-z0-9]+)*|[.,;:?!]")   # our "tokens": words and punctuation
tokens = TOKEN.findall(open(a.corpus, encoding="utf-8").read().lower())
table = collections.defaultdict(collections.Counter)            # context (tuple of words) -> counts of next word
for i in range(len(tokens) - a.context):
    table[tuple(tokens[i:i + a.context])][tokens[i + a.context]] += 1
print("learned from %d tokens: %d different contexts" % (len(tokens), len(table)))


def probabilities(context, temperature):
    """Next-word probabilities after `context`. Temperature reshapes them: p ~ count ** (1 / T)."""
    counts = table.get(tuple(context[-a.context:]))
    if not counts:
        return {}
    weights = {w: c ** (1 / temperature) for w, c in counts.items()}
    total = sum(weights.values())
    return {w: x / total for w, x in sorted(weights.items(), key=lambda kv: -kv[1])}


if a.next:
    ctx = TOKEN.findall(a.next.lower())
    probs = probabilities(ctx, a.temperature)
    if not probs:
        print("never saw %r in the text: the model has no idea (a real LLM would still answer)" % " ".join(ctx[-a.context:]))
    for w, pr in list(probs.items())[:10]:
        print("  %-14s %5.1f%%  %s" % (w, 100 * pr, "#" * round(40 * pr)))

if a.write:
    rng = random.Random(a.seed)
    out = TOKEN.findall(a.write.lower())
    for _ in range(a.words):
        probs = probabilities(out, a.temperature)
        if not probs:
            break
        out.append(rng.choices(list(probs), weights=list(probs.values()))[0])
    text = " ".join(out)
    print(re.sub(r" ([.,;:?!])", r"\1", text))
