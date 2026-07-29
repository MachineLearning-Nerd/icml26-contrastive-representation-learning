# Method

With seed `260502116`, the checker samples 20,000 positive, negative, and
candidate distributions over supports from 2 to 16 using boundary-heavy
Dirichlet draws. It evaluates Theorem 3.4 directly as retrieval gap versus
`sqrt(2 KL)`. SymPy independently evaluates the asymptotic log-factor ratio.

This route is counterexample search and interpretation stress, not a universal
proof.
