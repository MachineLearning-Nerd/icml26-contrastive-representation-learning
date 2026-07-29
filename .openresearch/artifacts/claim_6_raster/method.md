# Method

The checker detects the standard Matplotlib blue, orange, and green pixels,
samples each curve at the five paper-specified negative ratios, and compares
45 pixel-derived values with the vector-derived table. The allowed maximum
pixel error is preregistered at 0.8 percentage points.

The negative control tightens that tolerance to 0.1 and must exit nonzero.
