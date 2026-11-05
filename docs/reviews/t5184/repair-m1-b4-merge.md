# T-5259 — M1 D8 (Task B4) decision report: **option ① MERGE** `plasma-termination` → `plasma-shutdown`

Audience: repository developers / agents. Internal technical artifact; external-facing de-ai-fier (§0) not applicable.

- Date: `2026-11-05T12:44:19+08:00` (run `date -Iseconds`)
- Baseline commit under repair: `8460437` (M1 D7 / B3 UNDECIDABLE commit); HEAD after this task = this commit.
- Plan authority: `.github/plans/5184-m3-m1-repair.md` §6.0 (GM-0/GM-1/GM-4/GM-5), §6.3 Task B4, §2.1/§2.2, §8.4; commit suffix **`#T-5259`** (never `#T-5184`). GM-0 satisfied (task id fixed by delegation).
- Decision: **DATA CHANGE — option ① merge `plasma-termination` → `plasma-shutdown`** (evidence sufficient; destination well-anchored; mechanically achievable within the §2.1 write whitelist). D8 is repaired.
- Branch: master; **no push, no tag, no `dist/`, no `CHANGELOG.md`** touched. B1/D3 (`644b9a7`), B2/D5 (`2e13370`), B3/D7 (`8460437`) were **not revisited**.

---

## 0. Summary of the decision

| Aspect | Result |
|---|---|
| GM-1 evidence (external authority) | **Sufficient** — GB/T-4960.9 §411 and ITER §98 both map the discharge-termination process to `plasma-shutdown`; `plasma-termination` has **no** external anchor |
| GM-1 ④ (independent superordinate?) | **No** — no new evidence for a distinct superordinate "discharge-termination" stage; `concepts.tsv` has no `parent` column (hierarchy only expressible in text) ⇒ merge, do **not** invent hierarchy |
| Destination quality | **Well-anchored** (`plasma-shutdown`: ITER-glossary cid, ITER + GB/T definitions, ITER evidence) ⇒ **no** semantic regression (contrast B3, whose destination was a self-declared glue word) |
| GM-4 mechanical feasibility | **Feasible**, with two proven constraints (§3): the sanctioned *deprecated-redirect* id-stability mechanism is **bridge-blocked**; a naive row **deletion** breaks the `--self-test` line anchors |
| Chosen outcome | **① merge** (data change); D8 repaired |
| Data change | concepts 3076→**3075**; aliases 10250→**10249**; evidence 3203→**3202**; definitions 6152→**6150** |

---

## 1. GM-1 evidence (read-only; commands 实跑 + observed values)

### (a) registry rows

```console
$ grep -n 'plasma-termination\|plasma-shutdown\|plasma-ramp-down' terms/registry/{concepts,definitions,aliases,evidence}.tsv
```

**concepts.tsv** (verbatim)

| file:line | verbatim |
|---|---|
| `concepts.tsv:781` | `plasma-ramp-down	concept	等离子体降流	plasma ramp-down		active	Plasma current termination ramp-down phase	corpus` (**must not be modified**) |
| `concepts.tsv:1536` | `plasma-termination	concept	等离子体终止	Plasma Termination		active	放电结束阶段	corpus` |
| `concepts.tsv:1744` | `plasma-shutdown	concept	等离子体熄灭	Plasma Shutdown		active		ITER-glossary` |

**definitions.tsv** (verbatim)

| file:line | verbatim |
|---|---|
| `definitions.tsv:98` | `plasma-shutdown	en	The orderly process of extinguishing the plasma at the end of a plasma burn pulse, involving reduction of the plasma thermal energy, and reduction of plasma current to zero.	ITER-glossary` |
| `definitions.tsv:1402` | `plasma-shutdown	zh	在等离子体燃烧末期，等离子体能量衰减为零的过程。	GB/T-4960.9` |
| `definitions.tsv:5068` | `plasma-termination	en	The phase at the end of a plasma discharge.	corpus` |
| `definitions.tsv:5069` | `plasma-termination	zh	等离子体终止是放电结束的阶段。	corpus` |

**aliases.tsv** (verbatim)

| file:line | verbatim |
|---|---|
| `aliases.tsv:6546` | `plasma termination	plasma-termination	en	preferred	preferred en` |
| `aliases.tsv:6547` | `等离子体终止	plasma-termination	zh	preferred	preferred zh` |
| `aliases.tsv:6548` | `plasma-termination	plasma-termination	en	alias	hyphenated form` |
| `aliases.tsv:7704` | `# -- plasma-termination (等离子体终止)` |
| `aliases.tsv:7705` | `等离子体终端	plasma-termination	zh	forbidden	AI误译termination(终止≠终端)：正确为 等离子体终止` |
| `aliases.tsv:7706` | `血浆终止	plasma-termination	zh	forbidden	AI误译plasma(等离子体≠血浆)：正确为 等离子体终止` |
| `aliases.tsv:7707` | `等离子体结束	plasma-termination	zh	forbidden	误译termination(终止≠结束)：正确为 等离子体终止` |
| `aliases.tsv:7829` | `Plasma Shutdown	plasma-shutdown	en	preferred	imported from ITER-glossary` |

`plasma-shutdown` has **exactly one** alias row (`:7829`); its `preferred_zh` `等离子体熄灭` has **no** alias row (pre-existing; not a defect for this task).

**evidence.tsv** (cid column)

| file:line | verbatim |
|---|---|
| `evidence.tsv:1406` | `plasma-termination	internal:registry-gap-review:batch6	Discharge termination phase	copilot	2026-04-04` |
| `evidence.tsv:1598` | `plasma-shutdown	https://www.iter.org/fusion-glossary	The orderly process of extinguishing the plasma at the end of a plasma burn pulse, involving reduction of the plasma thermal energy, and reduction of plasma current to zero.	t-5072-backfill	2026-10-31` |

⇒ `plasma-termination`'s only provenance is an **internal** gap-review; `plasma-shutdown` carries the **ITER** authoritative source.

### (b) external authority — both sources sit on the `plasma-shutdown` side

```console
$ sed -n '411p' artifacts/terminology_sources/gbt4960_9_diff.tsv
plasma shutdown	exists	plasma-shutdown	2.2.104	等离子体熄灭		在等离子体燃烧末期，等离子体能量衰减为零的过程。
$ sed -n '98p' artifacts/terminology_sources/iter_glossary_diff.tsv
Plasma Shutdown	new		The orderly process of extinguishing the plasma at the end of a plasma burn pulse, involving reduction of the plasma thermal energy, and reduction of plasma current to zero.	2026-04-14
```

- GB/T `:411` → `matched_concept_id = plasma-shutdown` (id `2.2.104`).
- ITER `:98` → `status=new`, `matched_concept_id` **empty** — the ITER term is not *bookkept* as matched in the diff table, **but it is already represented in the registry**: `concepts.tsv:1744` (`source=ITER-glossary`) + `definitions.tsv:98` (verbatim ITER text) + `evidence.tsv:1598` (ITER URL, `2026-10-31`). The empty `matched_concept_id` is an **import-bookkeeping gap**, not a missing concept (see §8 suggestion).
- **Neither** table maps `plasma termination` / `plasma-termination` ⇒ the retired cid's independent existence lacks any external anchor.

### (c) downstream references

```console
$ git grep -c 'plasma-termination' HEAD        # 16 files
$ git grep -n 'plasma-termination\b'            # full list
```

- **Code / tests / pipeline**: **none**. No entry under `pipeline/`, `scripts/`, or `tests/` references the concept id; no test asserts `zh2en['等离子体终止']`.
- **Docs / plans / historical id-lists only**: `.github/plans/expand-registry-batch6.md` (6), `.github/plans/t4973-batches/w1_b.ids` (1), `w1_b_b25.ids` (1), `.github/plans/terminology-coverage-and-definition-quality.md` (3), `.github/reviews/registry-gaps-batch6-2026-04-04.md` (2), `docs/reviews/t5184/*` (read-only audit artifacts), `artifacts/translation_dict.json` (derived).
- ⇒ **no non-migratable downstream reference**; a plain retirement needs no code redirect.

### (d) allowlist counts (`grep -Fnxc`, exact whole-line; `terms/allowlist_*` are READ-ONLY)

| string | `allowlist_zh.txt` | `allowlist_en.txt` |
|---|---|---|
| `等离子体终止` | **1** (L1743) | 0 |
| `等离子体熄灭` | **1** (L3119) | 0 |
| `plasma termination` | 0 | 0 |
| `plasma-termination` | 0 | **1** (L1120) |
| `plasma shutdown` | 0 | 0 |
| `plasma-shutdown` | 0 | **1** (L2140) |

- **`plasma-termination` and `等离子体终止` are exact IME allowlist entries.** ⇒ any **forbidden/deprecated** demotion of either string trips the validator bridge check (§3, proven).
- The 3 existing forbidden AI-misrendering strings (`等离子体终端`, `血浆终止`, `等离子体结束`) are **0** in both allowlists ⇒ they may stay `forbidden` (repointed) without tripping the bridge.

### (e) validator / bridge / self-test semantics (read + verified)

- **Preferred-alias rule** (`pipeline/validate_registry.py:205-228`): ≥1 `preferred` per concept; no cap per `(concept,lang)`; an alias maps to exactly one cid.
- **Bridge check** (`validate_registry.py:309-326`): fires when a **forbidden/deprecated** alias string appears (case-insensitively) in either allowlist. A string that stays `alias`/`preferred` never trips it.
- **Duplicate-definition rule** (`:300-306`): at most one definition per `(cid,lang)` ⇒ the retired cid's definitions **cannot be re-homed** to `plasma-shutdown` (that `(cid,lang)` already exists) and must be removed.
- **Orphan proxy** (plan §6.3 Batch B): `grep -c "^<cid>\t"` over `concepts/definitions/evidence/aliases`. For `aliases.tsv`, field 1 is the **alias**, so the proxy also forbids retaining an alias row whose surface form equals the retired cid.
- **`--self-test`**: `scripts/registry_batch_verify.py::_build_restored_defect_corpus` re-creates historical defects **in a copy of the LIVE registry** with row counts preserved so that hard-coded `file:line` anchors (`concepts.tsv:3171/3316`, `definitions.tsv:5837/5838`) still resolve (`:805-877`, `SELF_TEST_CASES:736-775`). Row-count preservation was the deliberate fix in commits `471ab41` / `5735da8` (see `.github/plans/t4973-batches/self-test-reanchor.md` §2: "改了断言…＝削弱自检覆盖").

---

## 2. Decision (mechanical, per plan §6.3 B4)

Option ① is **authorised** because **all three** of the task's blocking conditions are avoided and the evidence is sufficient:

1. **Evidence sufficient** — both external authorities (GB/T `:411`, ITER `:98`/registry representation) sit on the `plasma-shutdown` side; `plasma-termination` has only an internal gap-review anchor.
2. **GM-1 ④ = No** — no evidence supports `plasma-termination` as an independent superordinate discharge-termination stage; the plan forbids inventing hierarchy without new evidence (and `concepts.tsv` has no `parent` column).
3. **No `terms/allowlist_*` write** — none performed.
4. **No bridge-tripping demotion** — no forbidden/deprecated alias carries an allowlisted string.
5. **No `pipeline/*.py` change** — none performed.

⇒ apply **option ①** (merge → `plasma-shutdown`), with a GM-4 id-stability record (§6). This matches the plan's §6.3 B4 裁决落地 ("双外部源…均在 `plasma-shutdown` 侧…证据充分时按推荐项 ①").

---

## 3. Mechanical-feasibility proof (scratch mutations; repo tree was not written during probing)

Two genuine mechanical constraints were found and **proven by scratch mutation** (not assumed):

### (i) the *deprecated-redirect* id-stability mechanism is **BLOCKED** by the allowlist bridge

Attempt: full merge but keep the retired self-alias as `plasma-termination … en deprecated` (plan GM-5's "保留为 deprecated" alternative):

```console
$ python3 -m pipeline.validate_registry --terms-dir /tmp/opencode/sb-b4/dep_terms
registry validation failed: forbidden/deprecated aliases must not appear in IME allowlists
offending terms:
- 'plasma-termination'
exit=1
```

Cause: `plasma-termination` is listed in `terms/allowlist_en.txt:1120` (read-only) and `validate_registry.py:309-326` forbids a forbidden/deprecated alias string from appearing in either allowlist. ⇒ the retired cid **cannot** be kept as a deprecated alias/redirect.

### (ii) a naive row **deletion** breaks the `--self-test` line anchors

Attempt: a *clean* deletion (remove every row of the retired cid from all 4 tables) — proven by the first scratch run (Design Z):

```console
$ python3 -m pipeline.validate_registry --terms-dir /tmp/opencode/sb-b4/z_terms
registry OK: 3075 concepts, 10249 aliases, 3202 evidence rows, 6150 definitions       # exit 0
$ python3 scripts/registry_batch_verify.py --self-test --repo-root /tmp/opencode/sb-b4/z2root
...
self-test: 20/27 assertions passed
exit=1
```

The 7 failures are exactly the anchor-shift class: `concept_cols@…concepts.tsv:3316` fired at `:3315`; `names_zh_no_cjk@…:3171` fired at `:3170`; `def_boilerplate_regex/mark/lang_placeholder/source_unknown@…definitions.tsv:5837/5838` fired at `:5835/5836` (deleting 1 concepts row + 2 definitions rows above the anchors shifts them by −1 / −2).

### (iii) the resolution: **row-count-preserving retirement markers** (in scope)

`concepts.tsv` and `definitions.tsv` are the two self-test-anchored files. Replacing the retired rows **in place** with a one-line retirement marker (a `#` comment — skipped by every parser) preserves the file line counts, so the anchors stay verbatim. `evidence.tsv` and `aliases.tsv` are **not** anchored and are edited freely. Verified on a pristine `git archive HEAD` copy:

```console
$ python3 -m pipeline.validate_registry --terms-dir /tmp/opencode/sb-b4/cleanroot/terms
registry OK: 3075 concepts, 10249 aliases, 3202 evidence rows, 6150 definitions       # exit 0
$ python3 scripts/registry_batch_verify.py --self-test --repo-root /tmp/opencode/sb-b4/cleanroot
self-test: 27/27 assertions passed
self-test: OK
exit=0
```

⇒ **no mechanical block remains**: the merge is achievable **without** writing `terms/allowlist_*`, **without** any forbidden/deprecated demotion, **without** touching `pipeline/*.py`, and **without** editing `scripts/registry_batch_verify.py` (anchors stay verbatim, in the repo-idiomatic spirit of `471ab41`/`5735da8`). The retirement markers double as the GM-4 id-stability record (the sanctioned deprecated-alias mechanism being bridge-blocked).

---

## 4. The applied change (exact diff)

`git diff --stat` = `terms/registry/{concepts,definitions,evidence,aliases}.tsv`, 9 insertions / 11 deletions:

```
 concepts.tsv:1536   -plasma-termination	concept	等离子体终止	Plasma Termination		active	放电结束阶段	corpus
                     +# retired (merged): plasma-termination -> plasma-shutdown (T-5259)
 definitions.tsv:5068,5069  -plasma-termination	en	The phase at the end of a plasma discharge.	corpus
                            -plasma-termination	zh	等离子体终止是放电结束的阶段。	corpus
                            +# retired (merged): plasma-termination en -> plasma-shutdown (T-5259)
                            +# retired (merged): plasma-termination zh -> plasma-shutdown (T-5259)
 evidence.tsv:1406          -plasma-termination	internal:registry-gap-review:batch6	Discharge termination phase	copilot	2026-04-04   (deleted)
 aliases.tsv:
   -plasma termination	plasma-termination	en	preferred	preferred en
   -等离子体终止	plasma-termination	zh	preferred	preferred zh
   -plasma-termination	plasma-termination	en	alias	hyphenated form
   +plasma termination	plasma-shutdown	en	alias	merged from plasma-termination (retired preferred form)
   +等离子体终止	plasma-shutdown	zh	alias	merged from plasma-termination (retired preferred form)
   -# -- plasma-termination (等离子体终止)
   +# -- plasma-shutdown (等离子体熄灭) — merged from plasma-termination
   -等离子体终端/血浆终止/等离子体结束 … plasma-termination … forbidden   (3 rows)
   +等离子体终端/血浆终止/等离子体结束 … plasma-shutdown  … forbidden   (3 rows, comments kept)
```

Notes:
- The migrated **zh face** (`等离子体终止`) is re-homed to `plasma-shutdown` as `alias` (kind flipped from `preferred`, since `plasma-shutdown`'s canonical preferred are `Plasma Shutdown` / `等离子体熄灭`).
- The retired self-alias `plasma-termination` is **deleted** (required by the plan's literal orphan proxy; it cannot be kept as `deprecated` — §3(i)).
- The 3 forbidden AI-misrendering rows are **repointed** to the survivor (drift-scan coverage preserved; comments remain valid because `等离子体终止` is now the survivor's zh alias).
- All edited alias rows carry **non-empty 5th-field comments** ⇒ the derived `terminology_substitutions.tsv` rows stay 5-field clean (verified: 2149/2149 rows NF==5).
- `plasma-ramp-down` (`concepts.tsv:781`) is **byte-identical** (`md5 54e59305da11dc54fd1ce106908ef8f9` before/after).
- Retirement markers keep `concepts.tsv` (3408 lines) and `definitions.tsv` (6154 lines) line counts unchanged.

---

## 5. Gate results (all on the mutated repo tree)

| # | gate | command | exit | key output |
|---|---|---|---|---|
| G1 | validator | `python3 -m pipeline.validate_registry` | **0** | `registry OK: 3075 concepts, 10249 aliases, 3202 evidence rows, 6150 definitions` |
| G2 | row audit | `python3 scripts/registry_row_audit.py --audit` | **0** | `"is_clean": true`, `"w0_is_clean": true` |
| G3 | batch self-test | `python3 scripts/registry_batch_verify.py --self-test` | **0** | `self-test: 27/27 assertions passed` |
| G4 | full suite | `python3 -m pytest -o addopts="" -q` | **0** | `207 passed` |
| G5 | projection gate | `python3 -m pipeline.export_registry --config config.toml --query-expansions --translation-dict --substitutions --no-vale` | **0** | `exported registry artifacts to artifacts` (no `maps to multiple concepts`); artifacts diff = 2 files, 100% attributable to this merge; **restored to HEAD** (Batch B commits no M3-scoped artifacts, §2.1/AC-4) |
| G6 | orphan gate | `grep -c "^plasma-termination\t" terms/registry/{concepts,definitions,evidence,aliases}.tsv` | — | `0 / 0 / 0 / 0` ⇒ **PASS** |

**Projection assertions (rebuilt output, scratch copy):**

| assertion | result |
|---|---|
| `alias_index['等离子体终止']` | `'plasma-shutdown'` (**unique**) |
| `zh2en['等离子体终止']` | `'Plasma Shutdown'` (label; per F16 the value is the en preferred label, the cid direction is `alias_index`) |
| `en2zh['plasma termination']` / `en2zh['Plasma Shutdown']` | `'等离子体熄灭'` |
| retired label `Plasma Termination` still in `zh2en` values? | **False** |
| alias rows for `等离子体终端/血浆终止/等离子体结束` | all → `'plasma-shutdown'` |
| concept `plasma-termination` in `query_expansions.concepts`? | **False** |
| `plasma-shutdown` include bucket | size 3 (`Plasma Shutdown`, `plasma termination`, `等离子体终止`) |
| `plasma-ramp-down` byte-identical | **yes** (md5 unchanged) |

**Before / after counts:**

| metric | before | after |
|---|---|---|
| concepts | 3076 | **3075** |
| aliases | 10250 | **10249** |
| evidence rows | 3203 | **3202** |
| definitions | 6152 | **6150** |

**`git grep -c 'plasma-termination'`** before = **16** files → after = **15** files (`evidence.tsv` dropped; `aliases.tsv` 7 → 3; `concepts.tsv` 1 and `definitions.tsv` 2 now count only the retirement markers; `terms/allowlist_en.txt` 1 unchanged — read-only IME entry).

---

## 6. GM-4 — id-stability statement

- **Retired cid**: `plasma-termination`. **Downstream code/test/pipeline references**: **none** (§1c) ⇒ no redirect needed.
- The **sanctioned deprecated-alias/redirect** record is **mechanically blocked** (§3i): `plasma-termination` is an exact `terms/allowlist_en.txt` entry, and the validator forbids forbidden/deprecated alias strings in either allowlist.
- **Id-stability record adopted**: an in-place retirement marker line in `concepts.tsv` (+2 in `definitions.tsv`) documents the retirement; the hyphenated surface token `plasma-termination` remains in the read-only IME `allowlist_en.txt` (unaffected), and the process's semantics are preserved under the surviving cid `plasma-shutdown`.
- Residual, out-of-scope: the now-stale `plasma-termination` line in `terms/allowlist_en.txt` (read-only for this task) — see §8.

---

## 7. Scope compliance

- Files changed: `terms/registry/{concepts,definitions,evidence,aliases}.tsv` + **this report** (`docs/reviews/t5184/repair-m1-b4-merge.md`).
- Not touched: `terms/allowlist_*`, `pipeline/*.py`, `scripts/*` (incl. `registry_batch_verify.py` — anchors preserved, not edited), `artifacts/terminology_sources/*`, `artifacts/*` (rebuilt then restored), `plasma-ramp-down`, `thermonuclear-fusion`/`controlled-thermonuclear-fusion`, other D items, `dist/`, `CHANGELOG.md`, `docs/publication/`, `evaluation/`, `.github/plans/publication-program-lre-scientificdata.md`. No push, no tag.
- Date verified by live `date -Iseconds` = `2026-11-05T12:44:19+08:00`.

---

## 8. Suggestions (recorded only; not executed)

1. **ITER bookkeeping**: `iter_glossary_diff.tsv:98` (`Plasma Shutdown`) has an empty `matched_concept_id` although the concept is already in the registry (`plasma-shutdown`). A future import-bookkeeping pass should set `matched_concept_id = plasma-shutdown` (the snapshot files are read-only for this task).
2. **Allowlist hygiene**: `terms/allowlist_en.txt:1120` still lists `plasma-termination` (a valid surface form). No action required; if a future task wants IME-level retirement it must edit the allowlist source (out of scope here).
3. **Self-test anchoring**: `scripts/registry_batch_verify.py --self-test` is coupled to **live-registry line numbers**; any future M1 Batch-B merge must either preserve anchored-file line counts (as here) or re-anchor the `SELF_TEST_CASES` line numbers in a dedicated, authorised task. The plan does not currently state this coupling — a candidate plan note.
