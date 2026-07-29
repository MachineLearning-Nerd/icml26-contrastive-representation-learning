# Historical judged baseline

This baseline freezes the live evaluator state before stronger verification.
The verdict record is selected only by `space_id == "DineshAI/xixoixLXCr"`.

- Live score: 5/12
- Judged Space revision: `302f93efc3f480fc58029255717998691d765314`
- Judge time: `2026-07-29T11:07:19+00:00`
- Five claims: `toy`
- One claim: `inconclusive`

The historical Space tree has 13 protected files. Its manifest is
`judged_space_manifest.sha256`. This baseline does not upgrade any claim.

The first environment attempt (`7d9e3a6f-d65c-4b28-a31b-35c10b47b568`)
failed before the verifier started because the default HF CPU image lacked
`uv`. The repair uses the fixed
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim` image on the same node.
