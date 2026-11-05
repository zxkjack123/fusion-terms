# T-5259 — M1 D3 (Task B1) decision report: **UNDECIDABLE / 只登记不改** + suggestion

Audience: repository developers / agents. Internal technical artifact; external-facing de-ai-fier (§0) not applicable.

- Date: `2026-11-05T12:01:31+08:00` (run `date`; see §5)
- Baseline commit under repair: `9668c2f` (`fix(registry): align lawson-criterion notes with GB/T two-threshold criterion … (M1 D2) (#T-5259)`)
- Plan authority: `.github/plans/5184-m3-m1-repair.md` §6.0 (GM-0/GM-1/GM-4/GM-5), §6.3 Task B1, §8.4; PM task for this work: **`#T-5259`** (never `#T-5184`)
- Decision taken: **③ 只登记不改 (`UNDECIDABLE`)** — no registry/derived data change; D3 remains FAIL.
- Branch: master; **no push, no tag, no `dist/`, no `CHANGELOG.md`** touched.

---

## 1. GM-1 evidence (read-only; commands实跑 + observed values)

### (a) registry rows for both cids

```console
$ grep -n '^poloidal-field-coils\?[[:space:]]' terms/registry/*.tsv
```

| file:line | verbatim |
|---|---|
| `terms/registry/concepts.tsv:118` | `poloidal-field-coil	concept	极向场线圈	poloidal field coil	PFC-coil	active	Coil producing poloidal magnetic field (disambig from PFC = plasma-facing component)	corpus` |
| `terms/registry/concepts.tsv:1747` | `poloidal-field-coils	concept	极向场线圈系统	Poloidal Field Coils		active		ITER-glossary` |
| `terms/registry/definitions.tsv:103` | `poloidal-field-coils	en	Components of a tokamak that assist in stabilizing the plasma. In ITER, the poloidal field coil system consists of six horizontal coils placed outside the toroidal magnet structure.	ITER-glossary` |
| `terms/registry/definitions.tsv:1404` | `poloidal-field-coils	zh	在托卡马克中用于产生极向场的线圈。	GB/T-4960.9` |
| `terms/registry/definitions.tsv:5076` | `poloidal-field-coil	en	A coil of the magnet system that produces the poloidal magnetic field …	corpus` |
| `terms/registry/definitions.tsv:5077` | `poloidal-field-coil	zh	磁体系统中产生装置极向场的线圈，所产生磁场沿极向方向；…	corpus` |
| `terms/registry/evidence.tsv:107` | `poloidal-field-coil	internal:magnets:PF-coil			2026-03-16` |
| `terms/registry/evidence.tsv:1601` | `poloidal-field-coils	https://www.iter.org/fusion-glossary	…	 t-5072-backfill	2026-10-31` |

Alias rows (col-2 = cid; `^`-anchor misses these because the alias string is column 1):

| file:line | verbatim |
|---|---|
| `terms/registry/aliases.tsv:536` | `极向场线圈	poloidal-field-coil	zh	preferred	preferred zh` |
| `terms/registry/aliases.tsv:537` | `poloidal field coil	poloidal-field-coil	en	preferred	preferred en (phrase)` |
| `terms/registry/aliases.tsv:538` | `poloidal-field-coil	poloidal-field-coil	en	alias	IME token-only form` |
| `terms/registry/aliases.tsv:539` | `PF coil	poloidal-field-coil	en	alias	common short form` |
| `terms/registry/aliases.tsv:3192` | `环形磁场线圈	poloidal-field-coil	zh	forbidden	误译：与纵场线圈混淆，正确为 极向场线圈` |
| `terms/registry/aliases.tsv:7832` | `Poloidal Field Coils	poloidal-field-coils	en	preferred	imported from ITER-glossary` |

**Key structural fact**: the Chinese face `极向场线圈` appears **exactly once** in `aliases.tsv` (line 536 → `poloidal-field-coil`). Concept `poloidal-field-coils` (1747) has **no zh alias row at all** — only its ITER English preferred (7832); its `preferred_zh` lives solely in `concepts.tsv:1747`.

### (b) GB/T authoritative mapping

```console
$ sed -n '413p' artifacts/terminology_sources/gbt4960_9_diff.tsv
poloidal field coils	exists	poloidal-field-coils	2.2.106	极向场线圈	PF	在托卡马克中用于产生极向场的线圈。
```

Header: `# term	status	matched_concept_id	term_id	zh	abbr	definition`.

⇒ **The authoritative face is unique**: `poloidal field coils` → `matched_concept_id = poloidal-field-coils` (1747), `zh = 极向场线圈`, `abbr = PF`, `id = 2.2.106`. A full-file scan (`grep -n -i poloidal …gbt4960_9_diff.tsv`) shows **no** GB/T row pointing at the singular `poloidal-field-coil` (row 240 `poloidal field …→ poloidal-field` is a different term, 2.1.239). So GB/T assigns the Chinese face `极向场线圈` to the **plural** concept, while the registry currently assigns it to the **singular** concept (aliases.tsv:536).

### (c) ITER attribution (re-verified)

```console
$ grep -n -i 'poloidal field coil' artifacts/terminology_sources/iter_glossary_raw.tsv artifacts/terminology_sources/iter_glossary_diff.tsv
artifacts/terminology_sources/iter_glossary_raw.tsv:103:Poloidal Field Coils	Components of a tokamak … the poloidal field coil system consists of six horizontal coils …	2026-04-14
artifacts/terminology_sources/iter_glossary_diff.tsv:103:Poloidal Field Coils	new		Components of a tokamak … the poloidal field coil system consists of six horizontal coils …	2026-04-14
```

⇒ ITER's face is the **plural / system-level** term, and `iter_glossary_diff.tsv:103` has an **empty** `matched_concept_id` (status=`new`). The plan's `[报告转述]` that "ITER points at 1747" is **confirmed by content** (the definition text equals `definitions.tsv:103`, whose cid is 1747), but the diff table leaves the id blank. Both external sources therefore point at / describe the plural system term, **not** the singular coil.

### (d) Downstream-reference / id-stability scan

```console
$ git grep -c 'poloidal-field-coil'      # substring: matches BOTH singular and plural
$ git grep -n 'poloidal-field-coil\b'    # word boundary: singular only
```

Word-boundary (singular `poloidal-field-coil` only) references, per file:

| file | singular refs | classification | migratable within authorised scope? |
|---|---|---|---|
| `terms/registry/concepts.tsv` | 1 (L118) | self concept row | ✅ yes (own data) |
| `terms/registry/definitions.tsv` | 2 (L5076/5077) | self definitions | ✅ yes (own data) |
| `terms/registry/evidence.tsv` | 1 (L107) | self evidence | ✅ yes (own data) |
| `terms/registry/aliases.tsv` | 5 (L536–539, L3192) | self aliases | ✅ yes (own data) |
| `artifacts/translation_dict.json` | 1 (L3496) | derived projection | ✅ yes (regenerated by `export_registry`) |
| **`terms/allowlist_en.txt`** | **1 (L721)** | **live IME allowlist / batch-verify contract source** | ❌ **NO — `terms/allowlist_*` is a HARD BOUNDARY (plan §6.3 B1 修改边界 + task HARD BOUNDARIES)** |
| **`scripts/batches/_batch_forbidden.py`** | **1 (L216)** | **code (forbidden-term batch generator)** | ❌ **NO — out of authorised scope** |
| **`.github/plans/t4973-batches/w1_b.ids`** | **1 (L15)** | **historical batch id-list** | ❌ **NO — out of scope / historical** |
| **`.github/plans/t4973-batches/w1_b_b01.ids`** | **1 (L15)** | **historical batch id-list** | ❌ **NO — out of scope / historical** |
| `docs/reviews/t5184/m1-group-G1.md` | 8 | historical M1 FAIL evidence | ❌ must not be rewritten (it is the record of this FAIL) |
| `docs/reviews/t5184/m1-summary.md` | 3 | historical M1 FAIL evidence | ❌ must not be rewritten |
| `docs/reviews/t5184/m1-sample-manifest.tsv` | 1 | historical M1 sample manifest | ❌ must not be rewritten |

Note on the allowlist: `terms/allowlist_en.txt:721` holds `poloidal-field-coil` **because** concept 118 has a phrase `preferred_en` (`poloidal field coil`) — see the binding contract in §2.2. The file also holds the **plural** `poloidal-field-coils` (L2143) and `terms/allowlist_zh.txt` holds both `极向场线圈` (L1099) and `极向场线圈系统` (L3122).

⇒ **There exist downstream references to the singular id that are NOT migratable within this task's authorised scope** (`terms/allowlist_*` is explicitly non-modifiable; `scripts/` and historical plan/review files are out of scope). This is precisely the plan's stop-condition: 「下游引用不可迁移 ⇒ ③ 只登记不改」.

---

## 2. Validator / contract rules quoted (STEP 1e)

### 2.1 `pipeline/validate_registry.py` — preferred-alias rule (lines 150–229)

```python
allowed_kinds = {"preferred", "alias", "deprecated", "forbidden"}          # L151
…
if kind in {"forbidden", "deprecated"}:                                      # L203
    forbidden_or_deprecated.add(alias)                                       # L204
if kind == "preferred":                                                      # L205
    concepts_with_preferred.add(concept_id)                                  # L206

# Alias must map to exactly one concept (avoid drift).
if alias in alias_to_concept and alias_to_concept[alias] != concept_id:      # L209
    _fail(… f"alias {alias!r} maps to multiple concept_ids: …")              # L210-214
alias_to_concept.setdefault(alias, concept_id)                               # L215

missing_preferred = sorted(concept_ids - concepts_with_preferred)            # L217
if missing_preferred:                                                        # L218
    _fail(… f"concepts without preferred alias: {preview}{more}")            # L225-229
```

**Rule in words**: (i) every `concept_id` must have **≥1 `preferred`-kind alias**, **regardless of the concept's own `status`** (`missing_preferred = concept_ids − concepts_with_preferred` uses *all* concept ids; the concepts `status` column is **not consulted** — the only `status`-like enum check is on the *alias* `kind`); (ii) any alias string must map to **exactly one** concept id. Hence a "demote the concept" scheme must **either keep ≥1 preferred alias for the retired cid or remove the concept row entirely and clean its sub-rows**.

### 2.2 `pipeline/validate_registry.py` — forbidden/deprecated ↛ allowlist bridge check (lines 309–326)

```python
allow_zh = load_simple_list(terms_dir / "allowlist_zh.txt")                  # L310
allow_en = load_simple_list(terms_dir / "allowlist_en.txt")                  # L311
forbidden_lower = {t.lower() for t in forbidden_or_deprecated}               # L312
…
leaked_lower = sorted(forbidden_lower & set(allow_lower_to_orig))            # L318
if leaked:
    raise SystemExit("… forbidden/deprecated aliases must not appear in IME allowlists …")
```

### 2.3 `scripts/registry_batch_verify.py` — registry→allowlist contract (lines 630–676)

```python
if zh not in zh_listed:                                                      # L659
    violations.append(… f"{cid}: preferred_zh {zh!r} not listed in …allowlist_zh.txt")   # L664
if " " in en and cid not in en_listed:                                       # L667
    violations.append(… f"{cid}: preferred_en {en!r} is a phrase; hyphenated token form "
                        f"{cid!r} not listed in …allowlist_en.txt")          # L672-673
```

**Contract**: every concept's `preferred_zh` must be in `allowlist_zh.txt`; every concept whose `preferred_en` is a **phrase** must have its hyphenated `concept_id` in `allowlist_en.txt`. (Concept 118: `preferred_en = "poloidal field coil"` (phrase) ⇒ `poloidal-field-coil ∈ allowlist_en` is **required by contract**.)

---

## 3. Decision + justification

**Decision: ③ / `UNDECIDABLE` — do NOT change data; D3 remains FAIL.**

Applying the plan's B1 rule verbatim (`.github/plans/5184-m3-m1-repair.md` §6.3 Task B1 裁决落地):

> 「**若外部权威面形唯一指向 `poloidal-field-coils`（`gbt4960_9_diff.tsv:413` 已指向该 cid）且 `git grep` 显示 `poloidal-field-coil` 无不可迁移的下游引用** ⇒ 按 **推荐项 ①** …；**证据不足或下游引用不可迁移 ⇒ ③ 只登记不改**（维持 FAIL）。**② 一律禁止**」

- **Condition 1 — authority-unique: SATISFIED.** `gbt4960_9_diff.tsv:413` uniquely maps the Chinese face `极向场线圈` to `poloidal-field-coils` (1747); ITER likewise describes only the plural/system term (§1b/c).
- **Condition 2 — no non-migratable downstream reference: NOT SATISFIED.** `poloidal-field-coil` is referenced by **`terms/allowlist_en.txt:721`** — a **live, contract-bound IME allowlist** that this task (§ HARD BOUNDARIES, plan §6.3 B1 修改边界「不得改 `terms/allowlist_*`」) is **forbidden to modify** — and by out-of-scope `scripts/batches/_batch_forbidden.py:216` and historical `.github/plans/t4973-batches/*.ids` + `docs/reviews/t5184/*` (§1d).

Because Condition 2 fails, the plan mandates **③ (只登记不改)**. Per GM-2 / §0.2 R1 the executor **must not self-escalate evidence** ("不得由「无反对证据」反推授权").

**Independent corroboration (GM-4).** GM-4 requires an *id-stability scheme*: "旧 id 是否保留为 `deprecated` 别名或 redirect". The natural scheme — retire the old id as a **`deprecated` alias** — is **mechanically impossible** here: `poloidal-field-coil` already sits in `allowlist_en.txt`, so adding a `deprecated`-kind alias with that string trips the §2.2 bridge check:

```console
# scratch copy /tmp/opencode/b1t2: rm aliases.tsv:538, append
#   poloidal-field-coil<TAB>poloidal-field-coils<TAB>en<TAB>deprecated<TAB>redirect (merged into system concept)
$ python3 -m pipeline.validate_registry --terms-dir /tmp/opencode/b1t2/terms
registry validation failed: forbidden/deprecated aliases must not appear in IME allowlists
offending terms:
- 'poloidal-field-coil'
# exit=1
```

The only other id-retention form (an `alias`-kind "redirect") would leave the retired concept's face pinned to the survivor without ever *retiring* the singular concept, i.e. it does not resolve the substantive D3 conflict (single coil vs six-coil system) and still leaves the allowlist reference stale. Therefore **no in-scope id-stability scheme exists** — a second, independent reason for ③.

**Option ② is FORBIDDEN** (改规范中文名 = M3's B-class action; plan §2.2 第 4 条, not authorised). Not considered.

---

## 4. Candidate ① implementation (recorded for a future authorised task; NOT executed)

Both flavours were tested in scratch copies (never in the repo):

**①a — full removal of the singular concept (validate_registry passes):**

```console
$ # /tmp/opencode/b1t3 (scratch copy of terms/):
$ #   rm concepts.tsv:118; rm definitions.tsv:5076/5077; rm evidence.tsv:107;
$ #   rm aliases.tsv:536/537/538/539/3192;
$ #   append  极向场线圈<TAB>poloidal-field-coils<TAB>zh<TAB>preferred<TAB>GB/T-4960.9 2.2.106 zh face
$ python3 -m pipeline.validate_registry --terms-dir /tmp/opencode/b1t3/terms
registry OK: 3075 concepts, 10246 aliases, 3202 evidence rows, 6150 definitions
# exit=0
```

- Effect: concept count 3076 → 3075; `alias_index['极向场线圈']` → `poloidal-field-coils` (unique).
- Residuals NOT fixable in scope: `terms/allowlist_en.txt:721` (`poloidal-field-coil`) becomes a stale, un-removable contract token; `scripts/batches/_batch_forbidden.py:216` and historical plan/review references stay.
- GM-4 statement would have to be "old id **fully retired, no redirect**" — which §1d shows is *not* clean.

**①b — retire as `deprecated` alias: BLOCKED** (§3, exit=1).

⇒ Even though ①a passes the mechanical gates, it is **not** the plan's authorised outcome, because Condition 2 (migratability) is false.

---

## 5. Gate evidence (this session; no data change)

```console
$ date
Thu Nov  5 12:01:31 PM CST 2026
$ git rev-parse HEAD
9668c2fa82d8ddb19e8cf7f6771b14978e644ac8
$ git status --porcelain          # (only pre-existing untracked files from other sessions + this report)
?? .github/plans/5184-m3-m1-repair.md
?? .github/plans/publication-program-lre-scientificdata.md
?? docs/publication/
?? evaluation/
?? scripts/paper_audit.py
?? scripts/sample_gold.py
?? tests/test_paper_audit.py
?? tests/test_sample_gold.py
```

| # | gate | command | exit | key output |
|---|---|---|---|---|
| G1 | validator | `python3 -m pipeline.validate_registry` | 0 | `registry OK: 3076 concepts, 10250 aliases, 3203 evidence rows, 6152 definitions` |
| G2 | row audit | `python3 scripts/registry_row_audit.py --audit` | 0 | `"is_clean": true` (all non-zero metrics empty) |
| G3 | batch self-test | `python3 scripts/registry_batch_verify.py --self-test` | 0 | `self-test: 27/27 assertions passed` |
| G4 | full suite | `python3 -m pytest -o addopts="" -q` | 0 | `207 passed` |

Baseline is green and unchanged; this report is the only file written.

### Before/after counts (no data change ⇒ identical)

| metric | before | after (this task) |
|---|---|---|
| concepts | 3076 | 3076 |
| aliases | 10250 | 10250 |
| evidence rows | 3203 | 3203 |
| definitions | 6152 | 6152 |
| `git grep -c 'poloidal-field-coil'` (files → hits) | see §1d | unchanged |

---

## 6. Recommendation for a future authorised task (suggestion only)

1. **Own the hard-boundary file explicitly.** To retire `poloidal-field-coil`, the follow-up task **must** be granted write authority over `terms/allowlist_en.txt` (and, if the zh face is re-homed, confirm `terms/allowlist_zh.txt` already suffices — it does: `极向场线圈` at L1099). Without that, GM-4's id-stability scheme is unsatisfiable (§3).
2. **Preferred implementation (①a)**: delete `concepts.tsv:118`, `definitions.tsv:5076/5077`, `evidence.tsv:107`, `aliases.tsv:536/537/538/539/3192`; add `极向场线圈 → poloidal-field-coils / zh / preferred`; **and** remove `poloidal-field-coil` from `terms/allowlist_en.txt:721`. Record the concept-count change 3076 → 3075 (GM-5). Optionally add `poloidal field coil → poloidal-field-coils / en / alias` (singular English face kept as alias) — but **not** as `deprecated` (bridge check).
3. **GM-4 id-stability statement**: "old id `poloidal-field-coil` retired; no `deprecated` alias possible (bridge check vs `allowlist_en`); redirect offered as `alias`-kind if the singular English face must remain resolvable; downstream code/historical references (`scripts/batches/_batch_forbidden.py`, `.github/plans/t4973-batches/*.ids`, `docs/reviews/t5184/*`) are historical and left as-is."
4. **Do not** rewrite the `m1-*` review evidence (it records this FAIL) or the read-only GB/T snapshot.
5. Re-run the full Batch B acceptance skeleton (§6.3) + the unique-`alias_index` assertion (`极向场线圈` → 1 cid) + orphan gate, and record before/after counts.

**Status effect**: D3 stays **FAIL** (M1 tally unchanged: 55 PASS / 9 FAIL / 0 UNDECIDABLE as recorded by the M1 summary; this report reclassifies D3's *decision* as UNDECIDABLE-with-suggestion, not a data fix).

---

## 7. Scope compliance

- Files changed: **this report only** (`docs/reviews/t5184/repair-m1-b1-suggestion.md`).
- Not touched: `terms/registry/*` (no data change), `artifacts/*` (no projection rebuild), `pipeline/*.py`, `terms/allowlist_*`, `artifacts/terminology_sources/*`, other D items (`pfirsch*`, `nuclear-fusion`, `plasma-termination`), `dist/`, `CHANGELOG.md`. No push, no tag.
