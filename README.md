# Think step by step: a small model on grade-school math

Does telling a small AI model to think step by step make it solve more grade-school math problems?

Two smaller questions on the way:

- Do worked examples help more than "think step by step"?
- How many problems do we need before the difference is real?

The model is Qwen2.5-0.5B-Instruct (Apache 2.0), run on CPU. The problems are GSM8K's test set (Cobbe et al. 2021, MIT license).

Reference: Qwen2.5-0.5B-Instruct scores 49.6 on GSM8K (Qwen Team, "Qwen2.5 Technical Report", arXiv:2412.15115, table 10, the instruction-tuned models, on the full test set of 1319 problems).

## In short

Step by step scored 16.7% and the plain prompt 13.1%: 3.6 points better, short of the study's 5-point pass mark.

The agent's summary said worked examples beat step by step by 22.9 points. rb reads 20.8 points from the runs and can't tell yet whether that holds. Graded the same way as plain, worked examples came out 3.6 points lower, on one run each.

Two reasons for caution: the plain prompt's 13.1% is far below the published 49.6%, and every pass mark was written after the results came in.

## Quick start: a sample study

Try Rabbit Brain on a sample study, so you don't need to set up any experiments or use your own research. Just open Claude Code or Codex in an empty folder and paste the prompt below.

```
Clone https://github.com/rabbit-brain/think-step-by-step and work inside it.
Install rabbit-brain from PyPI into a virtual environment in that folder.
It's open source: https://github.com/rabbit-brain/rb
Start rb login in the background and show me the sign-in link it prints. I'll sign in.
When I'm signed in, run rb sync and give me the link it prints.
Run rb context and tell me in three lines what the study found and what's still open.
Don't run any experiments.
```

Your agent gives you a sign-in link (an email code, no password). Then the study opens in your private account on rabbitbrain.ai. No account? Ask your agent to run rb page instead.

`rb open` shows the study in your browser, and `rb ui` shows it in your terminal. Both refuse to start when your agent runs them, so type them in your own terminal. A rule or decision your agent records stays unconfirmed until you press `c` on its row in `rb ui`.

Two results in the record point to `logs/`, a folder this repository leaves out. rb tells you their source is gone.

If something confuses you or breaks, open an issue at [github.com/rabbit-brain/rb/issues](https://github.com/rabbit-brain/rb/issues).

## Setup

```
pip install -r requirements.txt
```

Download the model from Hugging Face into `models/qwen2.5-0.5b-instruct`, at the revision named in `configs/model.yaml`. Put GSM8K's `test.jsonl` and `train.jsonl` in `data/gsm8k/`.

## Run

```
python solve.py --prompt plain --seed 0 --out results/<run>
python solve.py --prompt step_by_step --seed 0 --out results/<run>
```

The text of each prompt is in `configs/prompts.yaml`. `configs/sampling.yaml` holds the model's sampling settings, which decide how it picks the words of each reply. `configs/eval.yaml` sets which problems the model gets and how each reply is graded. Each run's folder under `results/` keeps the settings it used in `config.yaml`, every reply in `replies.jsonl`, its scores in `metrics.json`, and its log.

## Sweep

```
python sweep.py configs/sweep.yaml
python summarize.py
```

`sweep.py` reads the grid of settings in `configs/sweep.yaml` and makes one run for each combination in it, one after another.
