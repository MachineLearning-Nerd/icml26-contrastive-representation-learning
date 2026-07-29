# Adversarial source interpretation

The exact Theorems 4.5 and 4.6 retain factors such as
`sqrt(log(1+c n))/sqrt(n)` and `sqrt(log(1+c m))/sqrt(m)`. The paper's own
summary uses tilde-O. A literal interpretation of the imported shorthand as
log-free big-O is therefore rejected because the ratio to `1/sqrt(n)` diverges.

The Section 4 decompositions use `<=`; the equality control `A=0,B=1,C=0`
has left side 0 and right side 2.
