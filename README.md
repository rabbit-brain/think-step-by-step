# math-prompts

Does telling a small AI model to think step by step make it solve more grade-school math problems?

Two smaller questions on the way:

- Do worked examples help more than "think step by step"?
- How many problems do we need before the difference is real?

The model is Qwen2.5-0.5B-Instruct (Apache 2.0), run on CPU. The problems are GSM8K's test set (Cobbe et al. 2021, MIT license).

Reference: Qwen2.5-0.5B-Instruct scores 49.6 on GSM8K (Qwen Team, "Qwen2.5 Technical Report", arXiv:2412.15115, table 10, the instruction-tuned models, on the full test set of 1319 problems).

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
