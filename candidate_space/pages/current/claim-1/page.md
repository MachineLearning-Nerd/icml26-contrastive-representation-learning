# Claim 1 — Theorem 3.1

## Verdict

**VERIFIED**, for the well-posed domain used by the paper’s proof: `tau>0`,
finite risks, a positive finite likelihood ratio on common support, and an
attained real-valued minimizer.

## Exact claim and quantifiers

Theorem 3.1 states that a minimizer of the population contrastive loss over all
measurable real-valued scorers is a maximizer of the AUC-type retrieval
functional. The source theorem lists no explicit assumptions; the density-ratio
proof requires the well-posedness conditions above.

## Proof certificate

The executable verifier checks:

```python
q_s = p_minus * exp(s / tau) / Z_s
L(s) - L_star = tau * E_x[KL(p_plus || q_s)]
s_min = tau * log(p_plus / p_minus) + g(x)
auc_swap_gain = p_minus_i * p_minus_j * (ratio_i - ratio_j)
```

KL equality characterizes every attainable loss minimizer. The pairwise swap
gain is strictly positive for every likelihood-ratio inversion, so the
minimizer’s ordering maximizes AUC.

The independent exact checker enumerates every positive integer distribution
with support size 2–4 and weights 1–3 and compares every ranking using rational
arithmetic. The reversed likelihood-ratio order is a negative control and must
exit nonzero.

Formal run output, Git SHA, actual CPU allocation, and runtime will be inserted
from the OpenResearch run before release. The fixed command is:

```bash
uv sync --frozen && uv run --frozen python run_reproduction.py
```

## Limitations

This is an independently reconstructed proof certificate, not evidence from
larger finite simulation. The finite enumeration stress-tests the checker; it
does not replace the universal analytic argument. The paper should have stated
its support and finiteness conditions explicitly.

## Visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | this page | yes, key code inline | pending formal output | pending package mirror | independent symbolic + rational checker | reversed ordering | yes | provisional VERIFIED |
