# Adversarial evaluation

Final route status is `NO_VALID_COUNTEREXAMPLE` only if:

- no positive-support exact case violates likelihood-ratio AUC optimality;
- every deliberately failing control is rejected for its stated assumption or
  quantifier violation;
- the historical baseline integrity checks still pass.

This status supports the constructive route but is not itself `VERIFIED`.

