# Small hand-made, a bit dumb LLM.

## Launching the "Toy LLM"

 python3 toy_lm.py --next "~~the receiver~~"\
 ***(which words followed "~~the receiver~~", and how often?)***

 python3 toy_lm.py --write "~~the attacker~~" --seed 1\
 ***(let it write 40 words after "~~the attacker~~")***

 python3 toy_lm.py --write "~~the God~~" --temperature 0.2\
 ***(cautious: almost always the most likely word)***

 python3 toy_lm.py --write "~~the God~~" --temperature 1.5\
 ***(adventurous: unlikely words get a bigger chance)***
\
\
\
 The LLM has learned the following data:
 - the Security Fundamentals lecture
 - the Bible
 - the Constitution of Finland (in English)