# SHORTHAND

- CONTEXT
- EVIDENCE
- TASK
- CONSTRAINTS
- FORMAT
- UNCERTAINTY EXIT

 Example:
```
 Context:
 I am using Bash on Linux. I want to remove only .tmp files from the
 current directory.

Evidence:
I ran:

    rm "*.tmp"

The shell responded:

    rm: cannot remove '*.tmp': No such file or directory

However:

    ls *.tmp

shows:

    a.tmp
    b.tmp

Task:
Explain why the rm command did not match the files.

Constraints:
Explain the cause before giving the corrected command.
Do not suggest sudo or recursive deletion.

Format:
1. Cause
2. Corrected command
3. A safe way to inspect what would be affected first

If the evidence is insufficient, say what else I should check.
```

# PROMPT PATTERNS

### Tutor
You are learning something and want help without giving away the learning task.
```
Do not solve the exercise for me.

Ask what I have tried first.
Then give me one hint at a time.

If I make a mistake, point me toward the concept I should reconsider
instead of giving the final answer immediately.
```

### Hypotheses, not answers
You are debugging.
```
Give me the three most likely causes of this behaviour.

For each cause:
1. explain why it is plausible;
2. tell me what evidence would support it;
3. tell me what evidence would refute it.

Do not choose the final cause until I provide the results.
```

### Tests first
You already understand the required behaviour of a function.
Write the tests before asking the LLM to implement the function.
```
Implement a function that satisfies these tests.

Explain any assumptions you make.

Do not change the tests.
```

### Critic
You already have an answer, program, explanation, or design and want a second pair of eyes.
```
Review this Python function for:

- correctness;
- edge cases;
- optimization
- readability;
- security problems.

For every issue:
1. identify the exact line or behaviour;
2. explain why it may be a problem;
3. describe how I can verify the issue.

Do not rewrite the whole program.
```
### Structured output
Another program is going to consume the answer.
```
Return only JSON with this structure:

{
  "event": "check_in | check_out",
  "time": "HH:MM | null"
}

Do not add Markdown or explanatory text.
If the time is not explicitly present in the input, use null
```


# SYSTEM PROMPT
A hidden set of instructions given to an AI model
before a conversation starts to define its role, tone, rules, and boundaries