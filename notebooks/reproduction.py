import marimo

__generated_with = "0.15.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Contrastive-learning consistency: an evidence-first tutorial

    **Observed outcome:** Claims 1–5 have proof-level executable certificates.
    Claim 6 remains **BLOCKED** after four routes; author-figure agreement is
    not independent CLIP training.

    | Claim | Outcome | Strongest evidence |
    | --- | --- | --- |
    | 1 | VERIFIED | symbolic likelihood-ratio proof + 162,000 rankings |
    | 2 | VERIFIED | exact KL/Pinsker chain + 4,672 stress cases |
    | 3–5 | VERIFIED | exact theorem quantifiers/rates/decomposition |
    | 6 | BLOCKED | 45 vector values + independent raster audit |
    """)
    return


@app.cell
def _():
    ratios = [1, 10, 40, 70, 100]
    curves = {
        "ImageNet 14M": [2.07, 21.70, 40.80, 41.20, 40.95],
        "COCO 14M": [0.74, 9.91, 20.62, 21.23, 21.69],
        "Flickr 14M": [1.47, 14.79, 33.34, 33.91, 34.63],
    }
    return curves, ratios


@app.cell
def _(curves, mo, ratios):
    rows = [
        {"task": task, "negative_ratio": ratio, "metric": value}
        for task, values in curves.items()
        for ratio, value in zip(ratios, values)
    ]
    mo.vstack(
        [
            mo.md(
                """
                ## What the Section 5 figures actually show

                The embedded values come from the paper's original vector PDFs,
                so no expensive rerun is required to inspect the released evidence.
                Performance rises sharply through 40% negatives and then plateaus.
                """
            ),
            mo.ui.table(rows, pagination=False),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Why the theorem checks are stronger than the old toy experiment

    A finite simulation can corroborate a universal theorem but cannot prove
    it. The current verifier instead checks the proof identities and quantified
    assumptions, then uses exhaustive finite cases only as an independent
    stress audit. Mutated certificates must fail with a nonzero exit.

    The exact command is:

    ```bash
    uv sync --frozen && uv run --frozen python run_reproduction.py
    ```

    Claim 6 is different: it is empirical. The paper-specific configs, exact
    data subsets, raw runs, checkpoints, seeds, and uncertainty are absent.
    Four documented routes therefore end in **BLOCKED**, not a proxy pass.
    """)
    return


if __name__ == "__main__":
    app.run()
