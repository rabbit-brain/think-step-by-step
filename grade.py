"""How a reply is graded: which number in it counts as the model's answer."""
import re

NUMBER = r"-?\$?\d[\d,]*(?:\.\d+)?"


def _value(token):
    token = token.replace(",", "").replace("$", "").rstrip(".")
    try:
        v = float(token)
    except ValueError:
        return None
    return int(v) if v.is_integer() else v


def answer_tag(reply):
    """The number after the last 'Answer:' in the reply; None when it has no such line."""
    parts = re.split(r"answer\s*:", reply, flags=re.I)
    if len(parts) < 2:
        return None
    found = re.search(NUMBER, parts[-1])
    return _value(found.group()) if found else None


def last_number(reply):
    """The last number anywhere in the reply."""
    found = re.findall(NUMBER, reply)
    return _value(found[-1]) if found else None


CHECKERS = {"answer_tag": answer_tag, "last_number": last_number}


def grade(reply, gold, checker):
    got = CHECKERS[checker](reply)
    return got, got is not None and abs(float(got) - float(gold)) < 1e-6
