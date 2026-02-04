# fusion-terms: extraction + review pipeline

## Inputs

- Markdown corpus root: `/home/gw/ComputeData/pdf2md/ZoteroIngest/staging` (recursive)

The extractor reads `*.md` and performs lightweight cleaning:

- strip fenced code blocks
- strip inline code
- remove/normalize Markdown links
- remove bare URLs
- ignore obvious reference noise where possible

## Candidate extraction strategy (optimized for high precision first)

The first iteration is intentionally **high precision** (low noise), then you increase recall:

### Chinese

- Extract spans of Han characters of length $[2,8]$.
- Store per-term frequency and up to N example contexts (line snippets).
- Review top candidates; add accepted terms to `terms/allowlist_zh.txt`.

Later upgrades (when you want more recall):

- stopword list tuned for your domain
- Chinese phrase scoring (凝固度/互信息) to prefer true phrases
- domain lexicon bootstrapping (seed terms → expand via co-occurrence)

### English / mixed strings

We focus on patterns typical for fusion engineering text:

- acronyms: `ITER`, `ICRH`, `NBI`, `ELM`, ...
- hyphenated regimes: `H-mode`, `DIII-D`
- material formulas: `Nb3Sn`, `CuCrZr`
- mixed tokens: `D-T`, `W/Be`

This avoids the low-value flood of generic English words.

#### Optional: English noun-phrase / method-name enhancement mode (non-acronym)

The baseline English extractor is intentionally conservative (acronyms, hyphenated tokens, formulas).
To bulk-extract **English method names and noun phrases** such as:

- *Thomson scattering*
- *neutral beam injection*
- *electron cyclotron resonance heating*

add an **English phrase enhancement mode**. This is an *add-on* step that produces an additional candidates file and does not change the review/build workflow.

##### Output (recommended)

In addition to `artifacts/candidates_en.tsv`, generate:

- `artifacts/candidates_en_phrases.tsv`

Use the same evidence schema (`term`, `count`, `examples`, `files`) so reviewers can use the same tooling and habits.

##### Algorithms (pick one; can also be combined)

1) **YAKE** (keyword/phrase extraction)

- Pros: good quality without heavy NLP models; works reasonably on technical prose.
- Cons: still needs post-filters to avoid generic phrases.

2) **RAKE** (Rapid Automatic Keyword Extraction)

- Pros: simple; fast; transparent.
- Cons: quality depends heavily on a good stopword list; may over-extract in noisy Markdown.

3) **spaCy noun chunks**

- Pros: best linguistic precision when the English is well-formed.
- Cons: requires installing a language model; slower; may miss domain-specific tokens (symbols, hyphenations) unless customized.

##### Strongly recommended filters (domain-friendly, keeps noise manageable)

No matter which algorithm you choose, apply lightweight filters before writing candidates:

- keep phrases with 2–6 words (tune later)
- drop phrases made only of stopwords/common verbs (maintain a stopword list)
- keep at least one “content” token (letters/digits), allow hyphens and Greek letter names
- blacklist boilerplate (e.g., “in this paper”, “as shown in”, “results show”)
- optionally **boost** phrases containing known domain seeds: `tokamak`, `plasma`, `confinement`, `scattering`, `diagnostic`, `heating`, `pellet`, `divertor`, etc.

##### Review workflow (unchanged)

Phrase candidates are still just **candidates**:

1) Review `artifacts/candidates_en_phrases.tsv`
2) Add accepted phrases into `terms/allowlist_en.txt`
3) Use `terms/synonyms.tsv` to normalize casing and hyphenation (e.g., `neutral-beam injection` → `neutral beam injection`)
4) Rebuild → `artifacts/domain_terms.txt` → (optional) Rime import

##### Upgrade path (how to introduce this without breaking the repo)

This enhancement mode is implemented as an optional extractor that can be enabled via:

- `--en-phrases=off|yake|rake|spacy`

Current implementation status:

- `--en-phrases off` (default): does not write any phrase candidates.
- `--en-phrases rake`: writes `artifacts/candidates_en_phrases.tsv` (discovery-only).

and should:

- write `candidates_en_phrases.tsv` only when enabled
- keep baseline outputs stable (`candidates_en.tsv` still produced)
- treat dependencies as optional (if YAKE/spaCy is not installed, emit a clear warning and continue baseline extraction)

If/when you implement it, also document dependency installation and model download steps in a separate note:

- see `docs/dev/04-english-phrase-extraction.md`

## Review loop

1) Run extraction to generate `artifacts/candidates_zh.tsv` and `artifacts/candidates_en.tsv`
2) Sort/filter by frequency and manually curate:

- **allowlist**: terms you want in the IME
- **denylist**: noise you never want to see
- **synonyms**: normalize casing/hyphenation/aliases

3) Run build to generate `artifacts/domain_terms.txt`

## Evidence format (TSV)

Each candidates TSV contains:

- `term`
- `count`
- `examples` (concatenated snippets)
- `files` (a small sample of file paths)

This makes manual review fast: you can judge whether a token is meaningful.
