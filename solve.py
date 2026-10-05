"""One run: a prompt style on the fixed subset of GSM8K test problems, at one sampling seed.

    python solve.py --prompt step_by_step --seed 0 --out results/<run> [--problems 250]

It writes config.yaml (what it resolved), replies.jsonl (each problem's reply, the number graded and whether it is
right), solve.log, and metrics.json: accuracy is the percentage of problems answered right."""
import argparse
import json

import data
import generate
import grade
from common import Run, load_configs, seed_everything, threads
from prompts import messages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True, choices=["plain", "step_by_step", "worked_examples"])
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--problems", type=int)
    args = ap.parse_args()
    cfg = load_configs()
    n = args.problems or cfg["eval"]["problems"]
    run = Run(args.out, {"prompt": args.prompt, "seed": args.seed, "problems": n, **cfg})
    seed_everything(args.seed)
    if cfg["model"].get("kind") != "stub":
        import torch
        torch.set_num_threads(threads())
    problems = data.subset(data.load(cfg["eval"]["split"]), n, cfg["eval"]["subset_seed"])
    conversations = [messages(p, cfg["prompts"], args.prompt) for p in problems]
    run.log(f"{cfg['model']['name']}, {args.prompt}, seed {args.seed}, {n} problems, checker {cfg['eval']['checker']}")
    model, tok = generate.load(cfg["model"])
    texts = generate.replies(model, tok, conversations, problems, cfg["sampling"], args.seed,
                             lambda done, total: run.log(f"{done}/{total} replies"))
    right = 0
    with open(run.out / "replies.jsonl", "w", encoding="utf-8") as f:
        for p, text in zip(problems, texts):
            want = data.gold(p["answer"])
            got, ok = grade.grade(text, want, cfg["eval"]["checker"])
            right += ok
            f.write(json.dumps({"index": p["index"], "gold": want, "graded": got, "correct": ok, "reply": text}) + "\n")
    run.finish({"prompt": args.prompt, "seed": args.seed, "problems": n, "correct": right,
                "accuracy": round(100 * right / n, 2)})


if __name__ == "__main__":
    main()
