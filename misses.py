"""Where a run's wrong answers come from: how many wrong replies have no 'Answer:' line, and how many of those end
with the right number all the same.

    python misses.py results/<run> [results/<run> ...]"""
import json
import re
import sys

from grade import last_number

for folder in sys.argv[1:]:
    rows = [json.loads(line) for line in open(f"{folder}/replies.jsonl", encoding="utf-8")]
    wrong = [r for r in rows if not r["correct"]]
    untagged = [r for r in wrong if not re.search(r"answer\s*:", r["reply"], re.I)]
    right_last = [r for r in untagged if last_number(r["reply"]) == r["gold"]]
    print(f"{folder.rstrip('/').split('/')[-1]}: {len(wrong)} wrong of {len(rows)}; {len(untagged)} of them have no "
          f"'Answer:' line; {len(right_last)} of those end with the right number")
