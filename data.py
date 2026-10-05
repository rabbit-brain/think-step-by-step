"""GSM8K (Cobbe et al. 2021) from data/gsm8k: the fixed subset of test problems, and worked examples from train."""
import json
import random
import re
from pathlib import Path

ROOT = Path("data/gsm8k")


def load(split):
    with open(ROOT / f"{split}.jsonl", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def gold(answer):
    """GSM8K's answer ends with '#### <number>'."""
    return number(answer.rsplit("####", 1)[1])


def number(text):
    text = text.strip().replace(",", "").replace("$", "").rstrip(".")
    try:
        value = float(text)
    except ValueError:
        return None
    return int(value) if value.is_integer() else value


def subset(problems, n, seed):
    """The first n of one seeded order of the test set: 50 is the start of 250, and 250 of 500."""
    order = list(range(len(problems)))
    random.Random(seed).shuffle(order)
    return [dict(problems[i], index=i) for i in order[:n]]


def worked(answer):
    """A training answer as a worked solution: its calculator marks dropped, its last line as 'Answer: N'."""
    steps, final = answer.rsplit("####", 1)
    steps = re.sub(r"<<[^>]*>>", "", steps).strip()
    return f"{steps}\nAnswer: {final.strip()}"


def shots(k, seed):
    train = load("train")
    picked = random.Random(seed).sample(range(len(train)), k)
    return [(train[i]["question"], worked(train[i]["answer"])) for i in picked]
