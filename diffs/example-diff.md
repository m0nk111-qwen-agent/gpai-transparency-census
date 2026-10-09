# Example diff: 2026-09-01 -> 2026-10-08

Run: `python3 census.py diff snapshots/2026-09-01.jsonl snapshots/2026-10-08.jsonl`

The 2026-09-01 snapshot is a **synthetic reconstruction** from the drift documented in issue #1 (Mistral's summary was a section before the dedicated document appeared; OpenAI's flagship was GPT-6 Astra before the 2026-09-29 Sol addendum; DeepSeek's V3.2 summary is dated 2026-09-03). It demonstrates that the diff catches tier moves, document-date moves, URL/model moves and new providers. The 2026-10-08 snapshot is the real one (all 21 URLs fetched 2026-10-08).

```
DeepSeek:
  summary_location: dedicated per-model 'Public Summary of Training Content' for V3.1 (V3.2 summary published 2026-09-03, after this snapshot) -> dedicated per-model Public Summary of Training Content documents (Policies page)
  doc_date: 2026-06 -> 2026-09-03
  models_checked: ["V3.1"] -> ["V3.1", "V3.2", "V4"]
Mistral:
  tier: T2+ -> T3
  summary_location: training-content section inside technical docs (AI governance center, pre-dedicated-summary) -> dedicated Large 3 training-content summary + per-model legal docs (AI governance center)
  template_sections: ["sources"] -> ["info", "sources", "processing"]
OpenAI:
  url: null -> https://cdn.openai.com/pdf/38e3efcf-545e-44cd-99ec-2b7eb395f4cc/oai_GPT_6_1_Sol.pdf
  summary_location: GPT-6 Astra system card (flagship at the time); Sol addendum (2026-09-29) later reduced the description to a one-line redirect -> system card addendum (2026-09-29), section 2: one sentence - 'same types of data and training as GPT-6 Astra' (redirect)
  doc_date: 2026-08 -> 2026-09-29
  models_checked: ["GPT-6 Astra"] -> ["GPT-6.1 Sol"]
```

Added: Anthropic (row 21, added 2026-10-08 after the skeptic review flagged the sample). Unchanged: 17 providers.
