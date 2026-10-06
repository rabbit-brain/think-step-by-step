"""Runs every cell of configs/sweep.yaml's grid with solve.py, one after another, each in a run folder of its own.

    python sweep.py configs/sweep.yaml

A run folder is named r<next number>_<prompt>[_n<problems>]_s<seed>."""
import re
import subprocess
import sys
from itertools import product
from pathlib import Path

import yaml

SHORT = {"plain": "plain", "step_by_step": "step", "worked_examples": "worked"}


def next_number():
    taken = [int(m.group(1)) for p in Path("results").glob("r*_*") if (m := re.match(r"r(\d+)_", p.name))]
    return max(taken, default=0) + 1


def main():
    plan = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    default = yaml.safe_load(Path("configs/eval.yaml").read_text(encoding="utf-8"))["problems"]
    problems = plan.get("problems", default)
    keys = list(plan["grid"])
    failed = 0
    for values in product(*(plan["grid"][k] for k in keys)):
        cell = dict(zip(keys, values))
        size = "" if problems == default else f"_n{problems}"
        out = f"results/r{next_number():03d}_{SHORT[cell['prompt']]}{size}_s{cell['seed']}"
        cmd = [sys.executable, "solve.py", "--prompt", cell["prompt"], "--seed", str(cell["seed"]), "--out", out]
        if problems != default:
            cmd += ["--problems", str(problems)]
        print(f"sweep: {out}", flush=True)
        code = subprocess.run(cmd).returncode
        print(f"sweep: {out} exited {code}", flush=True)
        failed += code != 0
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
