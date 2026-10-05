"""Replies from the model: batched sampling with its own settings (temperature, top-k, top-p, repetition penalty),
one seeded random stream per run. A reply ends at an end-of-turn token or at max_new_tokens."""
import random

from data import gold


def load(cfg):
    if cfg.get("kind") == "stub":
        return Stub(), None
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from transformers.utils import logging
    logging.disable_progress_bar()
    tok = AutoTokenizer.from_pretrained(cfg["path"])
    tok.padding_side = "left"
    model = AutoModelForCausalLM.from_pretrained(cfg["path"], dtype=getattr(torch, cfg["dtype"])).eval()
    return model, tok


def replies(model, tok, conversations, problems, cfg, seed, progress):
    if tok is None:
        return model.replies(conversations, problems, cfg, seed, progress)
    import torch
    gen = torch.Generator().manual_seed(seed)
    texts = [tok.apply_chat_template(c, tokenize=False, add_generation_prompt=True) for c in conversations]
    stops = torch.tensor(sorted({tok.convert_tokens_to_ids("<|im_end|>"), tok.convert_tokens_to_ids("<|endoftext|>")}))
    out = []
    size = cfg["batch_size"]
    for start in range(0, len(texts), size):
        out += _batch(model, tok, texts[start:start + size], cfg, gen, stops)
        progress(len(out), len(texts))
    return out


def _batch(model, tok, texts, cfg, gen, stops):
    import torch
    enc = tok(texts, return_tensors="pt", padding=True)
    mask = enc.attention_mask
    seen = enc.input_ids.masked_fill(mask == 0, -1)                 # the prompt's tokens, for the repetition penalty
    rows = torch.arange(len(texts))                                 # which reply each live row writes
    written = [[] for _ in texts]
    with torch.no_grad():
        logits, cache = _step(model, enc.input_ids, mask, None)
        for _ in range(cfg["max_new_tokens"]):
            nxt = _sample(logits, seen, cfg, gen)
            for r, t in zip(rows.tolist(), nxt.tolist()):
                written[r].append(t)
            done = torch.isin(nxt, stops)
            seen = torch.cat([seen, nxt[:, None]], 1)
            mask = torch.cat([mask, torch.ones(len(nxt), 1, dtype=mask.dtype)], 1)
            if done.all():
                break
            if done.any():                                          # drop finished rows from the batch and its cache
                keep = (~done).nonzero().squeeze(1)
                cache.reorder_cache(keep)
                rows, seen, mask, nxt = rows[keep], seen[keep], mask[keep], nxt[keep]
            logits, cache = _step(model, nxt[:, None], mask, cache)
    return [tok.decode([t for t in w if t not in stops.tolist()], skip_special_tokens=True) for w in written]


def _step(model, ids, mask, cache):
    import torch
    pos = (mask.cumsum(1) - 1).clamp(min=0)[:, -ids.shape[1]:]
    out = model(input_ids=ids, attention_mask=mask, position_ids=pos, past_key_values=cache, use_cache=True)
    return out.logits[:, -1, :].float(), out.past_key_values


def _sample(logits, seen, cfg, gen):
    import torch
    penalty = cfg["repetition_penalty"]
    if penalty != 1.0:
        present = torch.zeros_like(logits).scatter_add_(1, seen.clamp(min=0), (seen >= 0).float()) > 0
        logits = torch.where(present, torch.where(logits < 0, logits * penalty, logits / penalty), logits)
    logits = logits / cfg["temperature"]
    top, which = logits.topk(cfg["top_k"], dim=1)
    probs = top.softmax(1)
    cum = probs.cumsum(1)
    probs = probs.masked_fill(cum - probs > cfg["top_p"], 0)       # the smallest set whose mass reaches top_p
    pick = torch.multinomial(probs / probs.sum(1, keepdim=True), 1, generator=gen)
    return which.gather(1, pick).squeeze(1)


class Stub:
    """The test build's stand-in for the model: seeded replies, some ending 'Answer: N', some with the number only
    in a closing sentence, right more often when told to think step by step or shown worked examples."""

    def replies(self, conversations, problems, cfg, seed, progress):
        out = []
        for conv, problem in zip(conversations, problems):
            rng = random.Random(f"{seed}/{problem['index']}/{len(conv)}/{conv[-1]['content'][-40:]}")
            right = gold(problem["answer"])
            p = 0.3 + 0.1 * ("step by step" in conv[-1]["content"]) + 0.15 * (len(conv) > 1)
            got = right if rng.random() < p else right + rng.choice([-3, -1, 1, 2, 10])
            if rng.random() < 0.3:
                out.append(f"Working through it, the total comes to {got}.")
            else:
                out.append(f"Working through it step by step.\nAnswer: {got}")
            if len(out) % cfg["batch_size"] == 0 or len(out) == len(problems):
                progress(len(out), len(problems))
        return out
