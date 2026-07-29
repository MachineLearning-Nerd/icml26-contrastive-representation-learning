# Evaluator-blind red team — round 1

The reviewer used only the candidate README, `logbook.json`, `pages/index.md`,
the six current claim pages, the illustrated report, the formal run summary,
and the historical subset audit.

All six current verifiers, inline results, raw-output links, controls, exact
claim contracts, assumptions, command, revision, compute, and limitations were
locatable. One packaging conclusion could not be verified: the initial subset
audit counted 42 files because the local Hugging Face download cache was copied
alongside the 13 remote files. Those 29 cache metadata files were not part of
the judged Space revision.

Required fix: exclude `.cache`, rebuild from the protected 13-file manifest,
and repeat the evaluator-blind traversal. No scientific verdict changed.
