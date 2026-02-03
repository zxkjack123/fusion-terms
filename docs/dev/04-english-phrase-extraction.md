# English phrase extraction enhancement mode (planned)

This note documents how to extend the repo to extract **English noun phrases / method names** (beyond acronyms), without breaking the current workflow.

## Why this exists

The baseline English extractor intentionally focuses on high-precision tokens:

- acronyms (`ICRH`, `NBI`, `ELM`)
- hyphenated technical tokens (`H-mode`, `DIII-D`)
- material-like formulas (`Nb3Sn`, `CuCrZr`)

But many valuable fusion terms are **multi-word phrases**:

- *Thomson scattering*
- *neutral beam injection*
- *electron cyclotron resonance heating*
- *charge exchange recombination spectroscopy*

These should be extracted into a separate candidates artifact for review.

## Non-breaking contract (must keep)

- Existing outputs remain stable:
  - `artifacts/candidates_en.tsv` and `artifacts/candidates_zh.tsv`
- Phrase mode adds a new output:
  - `artifacts/candidates_en_phrases.tsv`
- Review/build remains the same:
  - accept → `terms/allowlist_en.txt`
  - normalize → `terms/synonyms.tsv`
  - build → `artifacts/domain_terms.txt`

## Activation surface (recommended)

Introduce an optional flag (or config key):

- `--en-phrases=off|yake|rake|spacy`

Defaults to `off` so existing automation is unchanged.

## Option 1: YAKE

### Summary
YAKE is a keyword/phrase extractor that can work well on technical documents with relatively little setup.

### Practical constraints
- Works best when you feed it fairly clean English text.
- Still needs post-filters to avoid generic academic boilerplate.

### Recommended post-filters
- 2–6 words
- drop phrases starting/ending with stopwords
- drop phrases containing only very short tokens
- keep hyphenated tokens and alphanumeric tokens

## Option 2: RAKE

### Summary
RAKE is transparent and fast: it splits text on stopwords and scores candidate phrases.

### What you must maintain
A stopword list that fits your corpus. For scientific writing, add patterns like:

- “in this paper”, “as shown in”, “results show”, “we propose”, “we present”, …

### Recommended post-filters
Same as YAKE; RAKE is even more sensitive to stopwords, so treat the stopword list as a first-class asset.

## Option 3: spaCy noun chunks

### Summary
Use syntactic noun chunks to extract linguistically coherent phrases.

### Pros
- High precision for well-formed sentences.

### Cons
- Requires downloading a model (and that step varies by platform).
- Needs customization to keep domain tokens (hyphens, symbols) from being stripped.

### Recommended approach
- tokenize/normalize minimally (do not destroy hyphens)
- extract noun chunks
- merge with domain token patterns (e.g., keep `H-mode` inside a chunk)

## Quality checklist (how to tell it’s helping)

When phrase mode is enabled, track:

- precision on top 200 phrases (how many are truly useful terms)
- coverage increase: how many accepted phrases are **not** already captured by acronym/token extraction
- reviewer time per accepted term (if it goes up, your filters are too loose)

A simple target is: **≥70% of top-200 phrases are acceptable** after basic filters; then iterate.

## Integration into allowlist/synonyms

Suggested conventions:

- Prefer a canonical lower/upper casing per term family:
  - acronyms uppercase (`NBI`)
  - common method phrases lowercase (`neutral beam injection`)
  - named effects/titlecase only if commonly written that way
- Normalize hyphenation variants in `terms/synonyms.tsv`:
  - `neutral-beam injection` → `neutral beam injection`
  - `Thomson-Scattering` → `Thomson scattering`
