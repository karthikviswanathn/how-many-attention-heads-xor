# Ported Mathlib search CLIs (literature-survey technique)

These are the **key-free** semantic-search CLIs from `numina-lean-agent/skills/cli/`,
copied here verbatim so the literature-survey step can run them on the cluster. They
hit public search APIs over the network; none needs an API key.

| CLI | Source / API | Finds |
|---|---|---|
| `leansearch.py` | leansearch.net | Natural-language + Lean-term search of Mathlib |
| `leanfinder.py` | HF inference endpoint | Mathlib theorems by mathematical concept |
| `loogle.py` | loogle.lean-lang.org | Mathlib by type/pattern shape |
| `state_search.py` | premise-search.com | Lemmas matching a proof goal/state |
| `hammer_premise.py` | leanpremise.net | Premise retrieval for automation |

Each: `python3 search/<tool>.py "QUERY" -n 5`, prints JSON results to stdout.

`leanexplore` (numina's sixth tool) is **not** ported: it needs `LEAN_LEANDEX_API_KEY`,
which is not set in this key-free setup.

`literature_survey_claude.py` calls `leansearch` and `leanfinder` automatically; run
the others by hand when a target calls for a type-shape or proof-state lookup.
