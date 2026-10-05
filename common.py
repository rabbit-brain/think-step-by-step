"""What every script shares: the configs, the run folder, and its log."""
import json
import os
import random
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

CONFIGS = ("model", "sampling", "eval", "prompts")


def load_configs():
    return {name: yaml.safe_load(Path(f"configs/{name}.yaml").read_text(encoding="utf-8")) for name in CONFIGS}


def commit():
    r = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True).stdout
    return (r.stdout.strip() or None), bool(dirty.strip())


def seed_everything(seed):
    random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
    except ImportError:
        pass


class Run:
    """A run folder: the config it resolved, a log, and metrics.json once it finishes."""

    def __init__(self, out, config):
        self.out = Path(out)
        if self.out.exists():
            sys.exit(f"{out} exists; give each run a folder of its own")
        self.out.mkdir(parents=True)
        sha, dirty = commit()
        self.config = {"command": "python " + " ".join(sys.argv), "commit": sha, "dirty": dirty,
                       "started": now(), **config}
        (self.out / "config.yaml").write_text(yaml.safe_dump(self.config, sort_keys=False), encoding="utf-8")
        self.log_file = open(self.out / "solve.log", "a", encoding="utf-8")
        self.t0 = time.time()

    def log(self, text):
        line = f"{now()}  {text}"
        print(line, flush=True)
        self.log_file.write(line + "\n")
        self.log_file.flush()

    def finish(self, metrics):
        metrics = {**metrics, "seconds": round(time.time() - self.t0, 1), "finished": now()}
        (self.out / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
        self.log(f"done: {json.dumps(metrics)}")
        self.log_file.close()
        return metrics


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def threads(default=None):
    return int(os.environ.get("OMP_NUM_THREADS") or default or os.cpu_count() or 1)
