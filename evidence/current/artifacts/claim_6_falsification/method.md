# Dedicated falsification route

The verifier seeks three contradictions in all released curves: failure to
improve before 40%, failure to remain within a 1.5-point plateau after 40%, or
a free-coefficient critical exponent outside `[0.5,1]`. It then requires both
shared-negative and independence assumptions before calling any contradiction
a valid falsification.

The negative control injects a large precritical reversal and marks both
assumptions established; it must exit nonzero with `VALID_FALSIFICATION`.
