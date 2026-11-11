# math-prompts

Does telling a small AI model to think step by step make it solve more grade-school math problems?

Two smaller questions on the way:

- Do worked examples help more than "think step by step"?
- How many problems do we need before the difference is real?

The model is Qwen2.5-0.5B-Instruct (Apache 2.0), run on CPU. The problems are GSM8K's test set (Cobbe et al. 2021, MIT license).

Reference: Qwen2.5-0.5B-Instruct scores 49.6 on GSM8K (Qwen Team, "Qwen2.5 Technical Report", arXiv:2412.15115, table 10, the instruction-tuned models, on the full test set of 1319 problems).

## Try it with Rabbit Brain

This study is kept with [Rabbit Brain](https://rabbitbrain.ai), an open-source CLI + MCP for Claude Code and Codex. Its questions, experiments, runs and results are recorded in `.rb/`. You don't need the model or the data to look around.

### Quick start: a sample study

Try Rabbit Brain on a sample study, so you don't need to set up any experiments or use your own research. Just open Claude Code or Codex in an empty folder and paste the prompt below.

```
Try Rabbit Brain on its sample study, then sync the study to my own private account on rabbitbrain.ai so I can explore the research catalogue in my browser.

Clone https://github.com/rabbit-brain/think-step-by-step. Then install Rabbit Brain from PyPI (rabbit-brain) using one of these methods. Use (a) unless I've removed it:

a. Just for this try: Create a virtual environment inside the cloned project folder, install rabbit-brain there, and use that environment's rb executable for all subsequent commands.

b. For ongoing use: Run uv tool install rabbit-brain (or pipx install rabbit-brain), which installs rb on my PATH in its own environment.

Rabbit Brain is open source (Apache-2.0): https://github.com/rabbit-brain/rb. The PyPI wheel contains its compiled binary, built from that repository.

Inside the cloned project, start rb login as a background process that stays running while I authenticate. Show me the login URL it prints. I'll open it, sign in with my email, and approve the login.

After authentication succeeds, run rb sync and give me the web URL it prints.

Run rb context and summarize in three lines what the study has established and what remains open.

Don't run the model or start any new experiments just yet. Explore and sync the existing sample study.

```

Your agent gives you one link to sign in (an email code, no password). Then you get the study's catalogue on rabbitbrain.ai, private to your account.

Rather not make an account? Ask your agent to run rb page instead and open the page it writes: the same catalogue, as one file on your machine.

`rb open` (in your browser) and `rb ui` (in your terminal) show the same study. They are your own screens, so your agent won't start them: run them in your own terminal. `rb ui` is also where you confirm what your agent proposes: press `c` on a waiting row.

`logs/` isn't in this repository, so Rabbit Brain says the source that two findings cite is gone.

Feedback is welcome at [github.com/rabbit-brain/rb/issues](https://github.com/rabbit-brain/rb/issues).

## Setup

```
pip install -r requirements.txt
```

The model goes in `models/qwen2.5-0.5b-instruct` (the Hugging Face snapshot at the revision in `configs/model.yaml`), and GSM8K's `test.jsonl` and `train.jsonl` in `data/gsm8k/`.

## Run

```
python solve.py --prompt plain --seed 0 --out results/<run>
python solve.py --prompt step_by_step --seed 0 --out results/<run>
```

The prompts are in `configs/prompts.yaml`, the model's sampling settings in `configs/sampling.yaml`, and which problems and how a reply is graded in `configs/eval.yaml`. Each run folder keeps the config it resolved (`config.yaml`), every reply (`replies.jsonl`), its log and `metrics.json`.

## Sweep

```
python sweep.py configs/sweep.yaml
python summarize.py
```

Each cell of the grid is one run, one after another.
