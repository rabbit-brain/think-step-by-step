"""The prompts: each problem as the chat messages the model is given."""
from data import shots


def messages(problem, prompts, style):
    if style == "worked_examples":
        cfg = prompts["worked_examples"]
        before = []
        for question, solution in shots(cfg["shots"], cfg["shots_seed"]):
            before += [{"role": "user", "content": prompts[cfg["template"]].format(question=question)},
                       {"role": "assistant", "content": solution}]
        return before + [{"role": "user", "content": prompts[cfg["template"]].format(question=problem["question"])}]
    return [{"role": "user", "content": prompts[style].format(question=problem["question"])}]
