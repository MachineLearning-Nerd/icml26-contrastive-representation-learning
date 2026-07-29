# Method

The verifier downloads the exact hashed arXiv source, opens the original
Matplotlib vector PDFs, calibrates their axes from vector tick marks, and emits
all 45 performance coordinates plus the critical-scaling points.

It tests two preregistered observations: every curve gains at least five points
between 10% and 40% negatives, and every curve varies by at most 1.5 points
from 40% through 100%. It also fits the critical points with and without a
free multiplicative coefficient.
