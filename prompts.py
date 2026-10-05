"""The prompts: each problem as the chat messages the model is given."""


def messages(problem, prompts, style):
    return [{"role": "user", "content": prompts[style].format(question=problem["question"])}]
