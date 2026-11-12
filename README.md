# Does telling a small AI model to think step by step make it solve more grade-school math problems?

A sample study kept with [Rabbit Brain](https://github.com/rabbit-brain/rb).

## Quick start: a sample study

No setup and no research of your own needed. Open Claude Code or Codex in an empty folder and paste this:

```
Clone https://github.com/rabbit-brain/think-step-by-step and work inside it.
Install rabbit-brain from PyPI into a virtual environment in that folder. It's open source: https://github.com/rabbit-brain/rb
Start rb login in the background and show me the sign-in link it prints. I'll sign in.
When I'm signed in, run rb sync and give me the link it prints.
Run rb context and tell me in three lines what the study found and what's still open.
Don't run any experiments.
```

Your agent gives you a sign-in link (an email code, no password). Then the study opens in your private account on rabbitbrain.ai. No account? Ask your agent to run rb page instead.

## What's here

- The model is Qwen2.5-0.5B-Instruct. The problems are GSM8K's test set.
- `.rb/` holds the study's questions, experiments, runs and results.
- `solve.py` runs the model. Prompts and settings are in `configs/`.
