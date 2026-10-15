"""One line per finished run, from its metrics.json."""
import json
from pathlib import Path

print(f"{'run':<22} {'prompt':<16} {'seed':>4} {'problems':>8} {'accuracy':>8}")
for m in sorted(Path("results").glob("r*_*/metrics.json")):
    d = json.loads(m.read_text(encoding="utf-8"))
    print(f"{m.parent.name:<22} {d['prompt']:<16} {d['seed']:>4} {d['problems']:>8} {d['accuracy']:>7.2f}%")
