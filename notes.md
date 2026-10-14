# Notes

2026-10-05: Starting math-prompts; the question is in the README. Reference: Qwen2.5-0.5B-Instruct scores 49.6 on GSM8K (Qwen2.5 Technical Report, table 10).

2026-10-06: Decision: we test on a fixed subset of 250 test problems, not all 1319, so a run takes minutes on CPU. Qwen's 49.6 is on the full test set; it stays a reference, not a target.

2026-10-13: Our rule: step by step helps if it scores at least 5 points above the plain prompt.
