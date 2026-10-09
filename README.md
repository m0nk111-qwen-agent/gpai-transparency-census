# gpai-transparency-census

Machine-readable rows + first diff for the Pennyforge census of how general-purpose AI (GPAI) providers disclose their training content, against the EU AI Act **Art. 53(1)(d)** template ("Public Summary of Training Content").

Published companions:
- issue #1 (2026-10-08): <https://dev.to/pennyforgehq/only-2-of-21-ai-providers-publish-the-document-the-eu-ai-act-asks-for-414h>
- issue #3 (2026-10-09, correction): <https://dev.to/pennyforgehq/the-eu-ai-act-training-data-census-corrected-13-of-21-not-2-of-21-41n9> — re-verified snapshot, 13/21 at T3, DeepSeek URL resolution, hosting-fragility findings

## The document being measured

Official template: **C(2025) 8311 final** (5.12.2025), "Explanatory Notice and Template — Public Summary of Training Content for General Purpose AI Models", published on the European Commission's digital-strategy library (2025-07-24, last update 2026-03-26): <https://digital-strategy.ec.europa.eu/en/library/explanatory-notice-and-template-public-summary-training-content-general-purpose-ai-models>

Deadlines (Explanatory Notice §8): the obligation applies from **2025-08-02**; models placed on the EU market **before** that date must publish the summary **no later than 2 August 2027**; AI Office supervision/enforcement starts **2026-08-02**.

## Tiers

| Tier | Meaning |
|---|---|
| T3 | Dedicated public summary whose structure matches the template's three sections (general info / list of data sources / data processing aspects) |
| T2+ | Detailed model card or technical report with substantive training-data description, no dedicated template-form summary |
| T2 | Brief mention only (a few lines / one short paragraph) |
| T2-gated | Same as T2 but the document sits behind a login (e.g. gated Hugging Face repo) |
| T1-2 | Research pages / reports only; commercial models not clearly covered |
| UNVERIFIED | No dedicated document found in the sweep (possible CN-language blind spot) |

## Data

`data/providers.jsonl` — one JSON object per provider (current view). Fields: `provider`, `models_checked`, `url`, `url_checked`, `tier`, `summary_location`, `template_sections` (subset of `info|sources|processing` covered), `doc_date` (document date if published), `notes`.

`snapshots/YYYY-MM-DD.jsonl` — dated snapshots.

- **2026-10-08** = the issue #1 table (21 providers, all URLs fetched 2026-10-08).
- **2026-10-09** = corrected view after the 2026-10-09 in-lane re-verification pass: 10 providers promoted (OpenAI, Google, Anthropic, Meta, Microsoft, ByteDance, xAI, Tencent, Cohere, Aleph Alpha → **T3**). Headline is now **13 of 21 at T3**. Snapshot 2026-09-01 is a **synthetic** reconstruction (labeled in the file) used to demonstrate the diff mechanism.
- **2026-10-09-scope27** = the 2026-10-09 view **plus 6 extended-scope providers** added from the aial.ie 78-doc list diff (diffs/aial-ie-78-list-2026-10-09.md): Adobe, Black Forest Labs, Hugging Face, Midjourney, Minimax, Thinking Machines — every document verified live 2026-10-09 (4 first-party, 2 via aial.ie dated archives after bot-walls). **Conformance checked 2026-10-09: all 6 = T3** (full EC template, all 3 sections substantive; notes carry the nuances — Adobe first-party bot-wall, BFL EU model-doc request-only, Minimax doc covers H3 only, HF = interactive space app). The **core 21 remains the published denominator** (13/21 headline); extended rows carry a scope flag in `notes` and join the core at the next snapshot if aial.ie keeps them. Also updated: Alibaba row with the 2026-10-09 Qwen3.8 flagship-card check (no data-disclosure section on the card; program-level T2+ stands on earlier Qwen-era docs).

**First real diff (non-synthetic):** `python3 census.py diff snapshots/2026-10-08.jsonl snapshots/2026-10-09.jsonl` — 17 of 21 rows changed in 24 hours, including 10 tier promotions to T3. This is the drift the tracker exists to catch: provider-level EU summary programs (per-model "Public Summary of Training Content" PDFs, explicit Art. 53(1)(d) reporting programs) that sit alongside the thin model-card sections the issue #1 sweep graded.

## Cross-reference source

**AI Accountability Lab — "GPAI Training Transparency"** (<https://aial.ie/research/gpai-training-transparency/>, discovered 2026-10-09): per-model list of discovered Art. 53(1)(d) public summaries with live URLs, dated archives, and A+–F transparency/usefulness grades. Used as a discovery cross-check (not as ground truth) for the 2026-10-09 snapshot; its dated archive copies served as verification substitutes where live URLs were flaky or signed-URL-hosted (Cohere, Tencent, Anthropic, Meta documents). Each row's `url_source` records exactly which route was used.

## Tool

```
python3 census.py snapshot [--date YYYY-MM-DD]    # write snapshots/<date>.jsonl
python3 census.py diff <old> <new> [--json]       # added/removed/changed providers + field-level changes
python3 census.py stats <snapshot.jsonl>          # tier counts + headline
```

The diff is the point: conformance moves over time (Mistral's summary was a section in Dec 2025 and a dedicated document by Oct 2026), so the value is the *delta between snapshots*, not any single table.

`diffs/example-diff.md` shows the diff mechanism on a synthetic previous snapshot (2026-09-01) to prove it catches tier moves, URL moves and new providers.

## Caveats (inherited from issue #1)

- Non-random sample: the 21 largest providers by judgment, as of 2026-10-08.
- English sweep: CN-language documents were a known blind spot in the 10-08 snapshot (Tencent = UNVERIFIED); the 10-09 snapshot resolves it via a flagged cross-source (Tencent Hy3 summary, pending independent fetch).
- "Conformance" = a documentary check against the published template, not a Commission assessment. Not legal advice.

## License

Data: CC-BY-4.0 (Pennyforge). Code: MIT.
