# Claim 1 adversarial source audit

Theorem 3.1 quantifies over all measurable real scorers and calls no explicit
assumption. Lemma 3.2 and its proof divide by `p_minus`, take
`log(p_plus/p_minus)`, use KL equality, and require a finite log-partition.
This route therefore separates:

- valid well-posed cases with positive finite density ratio and attained risk;
- support mismatch, where the infimum is generally not attained;
- invalid controls with nonpositive temperature or a restricted scorer class.

Only the first category can falsify the exact minimizer implication.

