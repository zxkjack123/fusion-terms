# T-5259 — M1 D7 (Task B3) decision report: **UNDECIDABLE / ③ 只登记不改** + suggestion

Audience: repository developers / agents. Internal technical artifact; external-facing de-ai-fier (§0) not applicable.

- Date: `2026-11-05T12:19:04+08:00` (run `date -Iseconds`; see §5)
- Baseline commit under repair: `2e1337038166a0242711acea9b9316f40527fb5b` (`2e13370`) — M1 D5 (B2) UNDECIDABLE commit; HEAD unchanged by this task.
- Plan authority: `.github/plans/5184-m3-m1-repair.md` §6.0 (GM-0/GM-1/GM-4/GM-5), §6.3 Task B3, §2.1/§2.2, §8.4; commit suffix **`#T-5259`** (never `#T-5184`). GM-0 satisfied (task id fixed by delegation).
- Decision taken: **③ 只登记不改 (`UNDECIDABLE`)** — no registry/derived data change; D7 remains FAIL.
- Branch: master; **no push, no tag, no `dist/`, no `CHANGELOG.md`** touched. B1/D3 (`644b9a7`) and B2/D5 (`2e13370`) were **not revisited**; B4/D8 (`plasma-termination`) untouched.

---

## 0. Summary of the decision

| Aspect | Result |
|---|---|
| GM-1 evidence (external authority) | **Sufficient** — GB/T-4960.9 §110 maps `fusion`/`核聚变`/`nuclear fusion` to **one** authority cid `fusion` (2.1.109) |
| GM-4 mechanical feasibility of ① | **Feasible** — scratch mutation passes `validate_registry`/`export_registry`/`row_audit`; **no mechanical block** |
| Plan-mandated semantic-regression risk | **Judged UNACCEPTABLE within this task's authorized bounds** (see §3) |
| Chosen outcome | **③ 只登记不改** (no data change; D7 stays FAIL) |
| Data change | **None** (counts identical, §5) |

---

## 1. GM-1 evidence (read-only; commands 实跑 + observed values)

### (a) registry rows for the four cids

```console
$ T=$'\t'; for f in concepts definitions aliases evidence; do
    grep -n "^\(nuclear-fusion\|fusion\|thermonuclear-fusion\|controlled-thermonuclear-fusion\)${T}" terms/registry/$f.tsv; done
```

**concepts.tsv**

| file:line | verbatim |
|---|---|
| `concepts.tsv:233` | `thermonuclear-fusion	concept	热核聚变	thermonuclear fusion		active	Fusion in thermal plasma (Maxwellian); contrasted with beam-target	corpus` |
| `concepts.tsv:1084` | `fusion	concept	聚变	fusion		active	Generic academic glue word for translation	corpus` |
| `concepts.tsv:1110` | `nuclear-fusion	concept	核聚变	nuclear fusion		active	Nuclear fusion (general)	corpus` |
| `concepts.tsv:2596` | `controlled-thermonuclear-fusion	nuclear-fusion	受控热核聚变	controlled thermonuclear fusion		active		GB/T-4960.9` |

**definitions.tsv**

| file:line | verbatim |
|---|---|
| `definitions.tsv:58` | `fusion	en	The merging of two light atomic nuclei into a heavier nucleus, with a resultant loss in the combined mass and a massive release of energy.	ITER-glossary` |
| `definitions.tsv:1108` | `fusion	zh	核聚变 nuclear fusion 轻元素的原子核聚合在一起形成较重元素的原子核并释放出能量的核反应。…	GB/T-4960.9` |
| `definitions.tsv:1277` | `thermonuclear-fusion	zh	利用高温实现聚变的反应。	GB/T-4960.9` |
| `definitions.tsv:2068` | `controlled-thermonuclear-fusion	en	Fusion reactions sustained under controlled laboratory conditions for energy production, distinct from uncontrolled detonation.	internal:dict-improvements` |
| `definitions.tsv:4904` | `nuclear-fusion	en	Nuclear fusion in the most general sense.	corpus` |
| `definitions.tsv:4905` | `nuclear-fusion	zh	核聚变指最一般意义上的核聚变。	corpus` |
| `definitions.tsv:5648` | `thermonuclear-fusion	en	A fusion reaction that is brought about by the use of a high temperature.	GB/T-4960.9` |

**aliases.tsv**

| file:line | verbatim |
|---|---|
| `aliases.tsv:1004` | `热核聚变	thermonuclear-fusion	zh	preferred	preferred zh` |
| `aliases.tsv:1005` | `thermonuclear fusion	thermonuclear-fusion	en	preferred	preferred en (phrase)` |
| `aliases.tsv:1006` | `thermonuclear-fusion	thermonuclear-fusion	en	alias	IME token-only form` |
| `aliases.tsv:3733` | `热核融合	thermonuclear-fusion	zh	forbidden	误用日语'融合'：正确为 热核聚变` |
| `aliases.tsv:3734` | `热核反应	thermonuclear-fusion	zh	deprecated	非标准：应为 热核聚变` |
| `aliases.tsv:5444` | `fusion	fusion	en	preferred	preferred en` |
| `aliases.tsv:5495` | `核聚变	nuclear-fusion	zh	preferred	preferred zh` |
| `aliases.tsv:5496` | `nuclear fusion	nuclear-fusion	en	preferred	preferred en` |
| `aliases.tsv:8711` | `controlled thermonuclear fusion	controlled-thermonuclear-fusion	en	preferred	imported from GB/T-4960.9` |
| `aliases.tsv:8712` | `受控热核聚变	controlled-thermonuclear-fusion	zh	preferred	imported from GB/T-4960.9` |
| `aliases.tsv:9037` | `thermal nuclear fusion	thermonuclear-fusion	en	preferred	imported from GB/T-4960.9` |

**evidence.tsv** (cid column)

| file:line | verbatim |
|---|---|
| `evidence.tsv:216` | `thermonuclear-fusion	https://en.wikipedia.org/wiki/Thermonuclear_fusion			2026-03-16` |
| `evidence.tsv:988` | `fusion	internal:translation:glue-vocabulary	High-frequency academic glue word for zh→en search translation		2026-03-29` |
| `evidence.tsv:1014` | `nuclear-fusion	internal:translation:compound-vocabulary	High-frequency compound term for zh→en search translation		2026-03-29` |
| `evidence.tsv:2443` | `controlled-thermonuclear-fusion	https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=FF51ABCCA1C1EED80A07C8B73E80C1F8		import_approved_terms	2026-04-14` |
| `evidence.tsv:2614` | `thermonuclear-fusion	https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=FF51ABCCA1C1EED80A07C8B73E80C1F8		import_approved_terms	2026-04-14` |

**Structural facts**

- `nuclear-fusion` (cid) carries **no external evidence** — only `internal:translation:compound-vocabulary` (`evidence.tsv:1014`). Its two definitions (`:4904`/`:4905`) are **circular** (zero mechanism, zero discriminating qualifier).
- `fusion` carries a substantive en definition from **ITER-glossary** (`:58`) and a substantive zh definition from **GB/T-4960.9** (`:1108`, the `核聚变 nuclear fusion …` text).
- `fusion` and its note: `concepts.tsv:1084` notes = **`Generic academic glue word for translation`** — 1 of **25** concepts sharing that exact note (`design, fusion, system, calculation, analysis, material, performance, radiation, activation, neutron, simulation, maintenance, evaluation, method, mode, device, transport, decay, cooling, damage, protection, sealing, reactor, steel, wall`; `awk -F'\t' '$7=="Generic academic glue word for translation"' terms/registry/concepts.tsv` → 25).

### (b) GB/T authoritative mapping

```console
$ sed -n '110p' artifacts/terminology_sources/gbt4960_9_diff.tsv
fusion	exists	fusion	2.1.109	聚变		核聚变 nuclear fusion 轻元素的原子核聚合在一起形成较重元素的原子核并释放出能量的核反应。最易实现的核聚变是在氢的两个同位素(氘和氚)之间的反应。氘-氚核聚变反应所释放的大部分能量是由高速中子所带走的。其余的能量则归于反应中产生的 α 粒子(氦核<sup>4</sup>He)。
```

Header: `# term	status	matched_concept_id	term_id	zh	abbr	definition`.

⇒ **Confirmed**: `matched_concept_id = fusion` (id `2.1.109`, zh column `聚变`); the definition's **first sentence** is literally `核聚变 nuclear fusion …`. The authority therefore treats `核聚变` / `nuclear fusion` / `聚变` / `fusion` as **one** concept whose cid is `fusion`. **No** GB/T row maps `nuclear-fusion`.

### (c) downstream references

```console
$ git grep -c 'nuclear-fusion' -- .        # 26 files
$ git grep -n 'nuclear-fusion\b' -- ':!*.tsv'
```

- **Code/tests**: **none** reference the concept id `nuclear-fusion`. Occurrences in `pipeline/validate_registry.py:24`, `scripts/registry_coverage_report.py:66`, `scripts/registry_row_audit.py:126` are the **`category` whitelist** string (a *category* value, unrelated to the concept id); `scripts/batches/_batch_forbidden4.py:462` is `thermonuclear-fusion`.
- **Doc/plan refs only**: `.github/plans/terminology-coverage-and-definition-quality.md` (14), `.github/plans/t4973-batches/*`, `docs/reviews/t5184/*`, `CHANGELOG`, `artifacts/translation_dict.json` (1 = `thermonuclear-fusion` substring).
- `terms/registry/concepts.tsv` shows **350** matches — **348** are the *category* value `nuclear-fusion` (a valid whitelisted category; `cut -f2 | sort | uniq -c` → 348) plus the concept row `:1110` and `controlled-thermonuclear-fusion` substrings.
- **No test under `tests/` references `nuclear-fusion` or asserts `zh2en['核聚变']=='nuclear fusion'`** (`grep -rln 'nuclear-fusion' tests/` → none; the only `核聚变` test hits are inside `国际热核聚变实验堆`).

### (d) allowlist counts (`grep -Fnxc`, exact whole-line)

| string | `terms/allowlist_zh.txt` | `terms/allowlist_en.txt` |
|---|---|---|
| `核聚变` | **1** (L1128) | 0 |
| `nuclear fusion` | 0 | 0 |
| `nuclear-fusion` | 0 | 0 |
| `聚变` | **1** (L1843) | 0 |
| `fusion` | 0 | **1** |
| `Fusion` | 0 | 0 |

- `terms/allowlist_en.txt` has **2** *substring* hits for `nuclear-fusion` — `thermonuclear-fusion` and `controlled-thermonuclear-fusion` — but **0** exact `nuclear-fusion` lines. ⇒ **No exact allowlist entry** corresponds to the cid `nuclear-fusion`.

### (e) validator / bridge / batch-verify semantics

- **Preferred-alias rule** (`pipeline/validate_registry.py:205-228`): a concept only needs **≥1** `preferred` alias row (`concepts_with_preferred`); the validator does **not** require `concepts.preferred_zh` to equal any alias text, and does **not** cap the number of preferred rows per `(concept, lang)`. An alias may map to **exactly one** cid (`alias_to_concept`, `:209-215`).
- **Bridge check** (`pipeline/validate_registry.py:309-326`): only fires when a **forbidden/deprecated** alias appears in `allowlist_zh`/`allowlist_en` (case-insensitive). An entry that stays `alias`/`preferred` never trips it.
- **Allowlist-orphan behaviour** (`scripts/registry_batch_verify.py`): the `allowlist` mode (`check_allowlist`, `:630`) is a **per-id** check driven by an explicit `ids` argument — it asserts each given cid has `preferred_zh` in `allowlist_zh` and its en form in `allowlist_en`. There is **no reverse/global gate** requiring every allowlist line to correspond to a registry concept/alias, and `--self-test` runs on internal fixtures. ⇒ **An allowlist entry with no corresponding registry concept does NOT trigger a failure**, and conversely **no allowlist edit is required to delete a concept**.

⇒ (e) conclusion: **a full-concept deletion is mechanically possible without editing `terms/allowlist_*`** (for `nuclear-fusion`, which has **no** exact allowlist entry).

---

## 2. Mechanical-feasibility proof (scratch mutation, 仓外)

Per GM-4 / the task's "prove any claimed mechanical block" requirement, the **①-merge** was actually applied on a scratch copy and run through the real gates (scratch dir `/tmp/opencode/t5259-b3/`; the repository tree was **not** modified):

```console
$ cp -a terms /tmp/opencode/t5259-b3/terms
$ python3 /tmp/opencode/t5259-b3/mutate.py        # delete cid nuclear-fusion + its defs/evidence/aliases; re-home 核聚变 & nuclear fusion as fusion aliases
concepts rows 3075 ; aliases rows 11570 ; definitions rows 6153 ; evidence rows 3252   (last line trimmed; trailing newline semantics preserved)
$ python3 -m pipeline.validate_registry --terms-dir /tmp/opencode/t5259-b3/terms
registry OK: 3075 concepts, 10250 aliases, 3202 evidence rows, 6150 definitions
exit 0
$ python3 -m pipeline.export_registry --terms-dir /tmp/opencode/t5259-b3/terms \
    --out-dir /tmp/opencode/t5259-b3/out --query-expansions --translation-dict --substitutions --no-vale
registry OK: 3075 concepts, 10250 aliases, 3202 evidence rows, 6150 definitions
exported registry artifacts to /tmp/opencode/t5259-b3/out
exit 0        # no "maps to multiple concepts"
$ python3 scripts/registry_row_audit.py --audit --concepts <scratch>/concepts.tsv --evidence … --definitions …
{"is_clean": true}   exit 0
```

Post-merge projections (scratch): `zh2en['核聚变']='fusion'`, `zh2en['聚变']='fusion'`, `alias_index['核聚变']='fusion'`, `en2zh['nuclear fusion']='聚变'`, `en2zh['fusion']='聚变'`, `fusion.all_terms=['fusion','nuclear fusion','核聚变','聚变']`.

⇒ **No mechanical block exists.** Option ① is mechanically achievable **without** writing `terms/allowlist_*`, **without** demoting any face to forbidden/deprecated (hence bridge check untripped), and **without** modifying `pipeline/*.py`. The decision below is therefore a **semantic-judgment** decision, not a mechanical one.

---

## 3. Semantic-regression risk assessment (plan §6.3 B3 mandate)

The plan (§6.3 B3, 裁决落地) requires an explicit evaluation of the risk of "把领域名（核聚变）挂到 notes 自述 `Generic academic glue word for translation` 的条". Findings:

1. **Improper home.** `fusion` (`concepts.tsv:1084`) is explicitly tagged in its own `notes` as a **translation glue word** (1 of 25 such batch-tagged concepts). It is a *utility* entry in the translation layer, not a curated domain concept. Re-homing the canonical domain name **核聚变** (and its standard English pair `nuclear fusion`) under `fusion` subordinates a core domain term to a self-declared glue word — a **semantic regression** in the registry's term-role model. The merge does **not** change `fusion`'s `notes`, so the mismatch is *entrenched*, not resolved.
2. **Translation-pairing crossing (measurable).** Pre-merge the registry pairs `核聚变 ↔ nuclear fusion` (`zh2en['核聚变']='nuclear fusion'`; `en2zh['nuclear fusion']='核聚变'`). Post-merge (scratch-verified) it returns `zh2en['核聚变']='fusion'` and `en2zh['nuclear fusion']='聚变'` — the *specific* standard pairing is replaced by the *generic* one. Because `zh2en[alias]` = the concept's `preferred_en` and `en2zh[alias]` = the concept's `preferred_zh` (`pipeline/export_registry.py`), this crossing is **unavoidable within authorized bounds**: preventing it would require editing `fusion`'s `preferred_en`/`preferred_zh` (`concepts.tsv:1084`) — a **B-class naming action** the plan does **not** authorize (`§2.2 #4` analog).
3. **Correct fix is out of bounds.** A clean consolidation presupposes first curating the `fusion` concept (drop the glue-word `notes`; possibly set `preferred_en='nuclear fusion'`) — an edit to `concepts.tsv:1084` that this task is not authorized to make.

**Judgment**: the risk is **UNACCEPTABLE within this task's authorized bounds**. Therefore **③ 只登记不改** is taken (the plan's explicit fallback: "风险不可接受 … ⇒ ② / ③ 只登记不改").

**Why not ②** (write a non-circular definition for `nuclear-fusion`): ② leaves the `nuclear-fusion ↔ fusion` duplication **unresolved** — both remain "general-sense" concepts — and it would **contradict** the GB/T authority (which assigns the concept to cid `fusion`), i.e. it would fabricate a distinction the authority denies. ② addresses only the *circularity* sub-defect and not the "重复登记 / 中文面归属冲突" sub-defect, so it is not the right outcome here.

---

## 4. Gate results (repository tree unchanged)

| # | gate | command | exit | key output |
|---|---|---|---|---|
| G1 | validator | `python3 -m pipeline.validate_registry` | 0 | `registry OK: 3076 concepts, 10250 aliases, 3203 evidence rows, 6152 definitions` |
| G2 | row audit | `python3 scripts/registry_row_audit.py --audit` | 0 | `is_clean: true` |
| G3 | batch self-test | `python3 scripts/registry_batch_verify.py --self-test` | 0 | `self-test: 27/27 assertions passed` |
| G4 | full suite | `python3 -m pytest -o addopts="" -q` | 0 | `207 passed in 8.28s` |

`git grep -c 'nuclear-fusion'` **before = after** (no data change): 26 files (concepts.tsv 350, aliases.tsv 10, definitions.tsv 6, evidence.tsv 4, plus docs/plans/category-whitelist).

### Before/after counts (no data change ⇒ identical)

| metric | before | after (this task) |
|---|---|---|
| concepts | 3076 | 3076 |
| aliases | 10250 | 10250 |
| evidence rows | 3203 | 3203 |
| definitions | 6152 | 6152 |

---

## 5. Scope compliance

- Files changed: **this report only** (`docs/reviews/t5184/repair-m1-b3-suggestion.md`).
- Not touched: `terms/registry/*` (no data change), `artifacts/*` (no projection rebuild — scratch only), `terms/allowlist_*`, `pipeline/*.py`, `artifacts/terminology_sources/*`, `thermonuclear-fusion`, `controlled-thermonuclear-fusion`, other D items (`pfirsch*`, `plasma-termination`), `dist/`, `CHANGELOG.md`, `docs/publication/`, `evaluation/`, `.github/plans/publication-program-lre-scientificdata.md`. No push, no tag.
- Date verified by live `date -Iseconds` = `2026-11-05T12:19:04+08:00`.

---

## 6. Recommendation for a future authorised task (suggestion only)

1. **Do not silently merge.** The merge is mechanically clean but the destination is a glue-word concept; a future task must be explicitly authorised to **first curate `fusion`** (`concepts.tsv:1084`): remove/replace the `Generic academic glue word for translation` `notes`, and decide whether `preferred_en` / `preferred_zh` stay `fusion` / `聚变` or become `nuclear fusion` / `核聚变` (so the standard bilingual pair is preserved).
2. **Then merge (①a)**: delete `concepts.tsv:1110`, `definitions.tsv:4904/4905`, `evidence.tsv:1014`, `aliases.tsv:5495/5496`; add `核聚变 → fusion / zh / alias` and `nuclear fusion → fusion / en / alias`; for GM-4 id-stability add `nuclear-fusion → fusion / en / deprecated` (bridge-safe: no exact `nuclear-fusion` line in either allowlist). Record concept count 3076 → 3075.
3. **Alternatively consider promoting** `nuclear-fusion` to be the curated survivor (preferred_zh `核聚变`, preferred_en `nuclear fusion`) **only if** a future task is authorised to rewrite the GB/T-facing mapping — but this contradicts `gbt4960_9_diff.tsv:110` (cid `fusion`), so ①a after curation is preferred.
4. **Do not** rewrite the read-only `m1-*` review evidence or the GB/T snapshot; D7 stays **FAIL**.
5. Re-run the Batch B acceptance skeleton (§6.3) + the `zh2en['核聚变'] == survivor.preferred_en` assertion + orphan gate, and record before/after `git grep -c 'nuclear-fusion'`.

**Status effect**: D7 stays **FAIL** (M1 tally unchanged: 55 PASS / 9 FAIL / 0 UNDECIDABLE per `m1-summary.md`; this report records D7's *decision* as UNDECIDABLE-with-suggestion, not a data fix).
