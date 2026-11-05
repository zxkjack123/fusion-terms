# T-5259 — M1 D5 (Task B2) decision report: **UNDECIDABLE / ③ 只登记不改** + suggestion

Audience: repository developers / agents. Internal technical artifact; external-facing de-ai-fier (§0) is **not applicable** (not a user-facing deliverable).

- Date: `2026-11-05T12:10:17+08:00` (run `date -Iseconds`; Always-On Rule 1)
- Baseline commit under repair: `644b9a7` (`docs(reviews): M1 D3 (B1) poloidal-field-coil face conflict — UNDECIDABLE, suggestion record only (#T-5259)`)
- Plan authority: `.github/plans/5184-m3-m1-repair.md` §6.0 (GM-0/GM-1/GM-2/GM-4/GM-5), §6.3 **Task B2**, §2.2, §8.4; PM task for this work: **`#T-5259`** (never `#T-5184`)
- Decision taken: **③ 只登记不改 (`UNDECIDABLE`)** — **no registry / derived data change**; D5 remains FAIL.
- Branch: `master`; **no push, no tag, no `dist/`, no `CHANGELOG.md`** touched.

---

## 1. GM-1 evidence (read-only; every command实跑, raw values recorded)

### (a) All `pfirsch` rows in registry + terminology-source snapshots

```console
$ grep -n 'pfirsch' terms/registry/*.tsv artifacts/terminology_sources/*.tsv
```

| file:line | verbatim |
|---|---|
| `terms/registry/aliases.tsv:2344` | `Pfirsch-Schlüter current	pfirsch-schlueter-current	en	preferred` |
| `terms/registry/aliases.tsv:2345` | `Pfirsch-Schlüter电流	pfirsch-schlueter-current	zh	preferred` |
| `terms/registry/aliases.tsv:2346` | `PS current	pfirsch-schlueter-current	en	alias` |
| `terms/registry/aliases.tsv:2930` | `Pfirsch-Schlüter regime	pfirsch-schlueter-regime	en	preferred` |
| `terms/registry/aliases.tsv:2931` | `Pfirsch-Schlüter区	pfirsch-schlueter-regime	zh	preferred` |
| `terms/registry/aliases.tsv:2932` | `PS regime	pfirsch-schlueter-regime	en	alias` |
| `terms/registry/aliases.tsv:4241` | `普费尔施-施吕特电流	pfirsch-schlueter-current	zh	forbidden	误音译人名：正确保留 Pfirsch-Schlüter电流` |
| `terms/registry/aliases.tsv:4242` | `普费尔施-施吕特区	pfirsch-schlueter-regime	zh	forbidden	误音译人名：正确保留 Pfirsch-Schlüter区` |
| `terms/registry/aliases.tsv:8953` | `Pfirsch-Schulueter regime	pfirsch-schulueter-regime	en	preferred	imported from GB/T-4960.9` |
| `terms/registry/aliases.tsv:8954` | `普费尔施-施吕特尔状态	pfirsch-schulueter-regime	zh	preferred	imported from GB/T-4960.9` |
| `terms/registry/concepts.tsv:649` | `pfirsch-schlueter-current	concept	Pfirsch-Schlüter电流	Pfirsch-Schlüter current		active	Neoclassical current arising from pressure gradient in toroidal geometry	corpus` |
| `terms/registry/concepts.tsv:909` | `pfirsch-schlueter-regime	concept	Pfirsch-Schlüter区	Pfirsch-Schlüter regime		active	High collisionality neoclassical transport regime	corpus` |
| `terms/registry/concepts.tsv:2711` | `pfirsch-schulueter-regime	nuclear-fusion	普费尔施-施吕特尔状态	Pfirsch-Schulueter regime		active		GB/T-4960.9` |
| `terms/registry/definitions.tsv:1206` | `pfirsch-schulueter-regime	zh	托卡马克(2.1.284)等离子体中的一种输运状态，其特征是平均自由程比连接长度短。在此状态中扩散系数为经典值的 q^2 倍(此处安全因子 q 大于或等于1)。	GB/T-4960.9` |
| `terms/registry/definitions.tsv:2264` | `pfirsch-schulueter-regime	en	High-collisionality regime of neoclassical transport where ν* > 1; current-driven enhancement of classical diffusion.	internal:dict-improvements` |
| `terms/registry/definitions.tsv:5009` | `pfirsch-schlueter-regime	en	The high collisionality neoclassical transport regime.	corpus` |
| `terms/registry/definitions.tsv:5010` | `pfirsch-schlueter-regime	zh	Pfirsch-Schlüter区是高碰撞率的新经典输运区。	corpus` |
| `terms/registry/evidence.tsv:831` | `pfirsch-schlueter-regime	internal:expansion:batch-42	High-collisionality regime	copilot	2026-03-19` |
| `terms/registry/evidence.tsv:2570` | `pfirsch-schulueter-regime	https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=FF51ABCCA1C1EED80A07C8B73E80C1F8		import_approved_terms	2026-04-14` |

**Note (fact correction vs plan text)**: the ν* regime-boundary criterion (`ν* > 1`) lives on the **GB/T-imported** side (`definitions.tsv:2264`, cid `pfirsch-schulueter-regime`), **not** on the FAIL item `pfirsch-schlueter-regime`. The FAIL item's only content not already present on the GB/T side is its `notes` string (`concepts.tsv:909`, `High collisionality neoclassical transport regime`; the GB/T concept `:2711` has an **empty** notes column) and its corpus en/zh definitions (`:5009`/`:5010`). Also note the atypical `category` of `:2711` = `nuclear-fusion` (not `concept`).

### (b) GB/T snapshot attribution — **empty** `matched_concept_id`

```console
$ grep -n 'Pfirsch' artifacts/terminology_sources/gbt4960_9_diff.tsv
211:Pfirsch-Schulueter regime	new		2.1.210	普费尔施-施吕特尔状态		托卡马克(2.1.284)等离子体中的一种输运状态，其特征是平均自由程比连接长度短。在此状态中扩散系数为经典值的 q^2 倍(此处安全因子 q 大于或等于1)。
$ sed -n '211p' artifacts/terminology_sources/gbt4960_9_terms.tsv
2.1.210	普费尔施-施吕特尔状态	Pfirsch-Schulueter regime		托卡马克(2.1.284)…	q^2 倍(…)	…	draft
```

Header of the diff: `# term	status	matched_concept_id	term_id	zh	abbr	definition`.

| field | observed value |
|---|---|
| `matched_concept_id` | **(empty)** |
| `status` | `new` |
| `term_id` / `id` | `2.1.210` |
| `zh` | `普费尔施-施吕特尔状态` |
| `definition` | `托卡马克(2.1.284)等离子体中的一种输运状态，其特征是平均自由程比连接长度短。在此状态中扩散系数为经典值的 q^2 倍(此处安全因子 q 大于或等于1)。` |

⇒ **The plan's guess ("报告称指向 2711，须复核") is NOT confirmed**: the GB/T snapshot row carries **no `matched_concept_id`** and status `new` — it was imported as a *new* term, not matched to any existing cid. The only link to `pfirsch-schulueter-regime` (`concepts.tsv:2711`) is the **zh-string correspondence** (`普费尔施-施吕特尔状态`) plus that concept's `source = GB/T-4960.9`. There is **no id-level authoritative attribution**.

### (c) `git grep -c` (id stability / downstream references — GM-4)

```console
$ git grep -c 'pfirsch-schlueter-regime'   # total occurrences across tracked files: 26
$ git grep -c 'pfirsch-schulueter-regime'  # total occurrences across tracked files: 15
```

| cid | registry rows | other tracked references |
|---|---|---|
| `pfirsch-schlueter-regime` | aliases ×4 (`2930,2931,2932,4242`), concepts ×1 (`909`), definitions ×2 (`5009,5010`), evidence ×1 (`831`) = **8** | `scripts/batches/_batch36_44.py` ×5, `scripts/batches/_batch_forbidden8.py` ×1, `.github/plans/t4973-batches/w1_b*.ids` ×2, `.github/plans/terminology-coverage-and-definition-quality.md` ×1, `docs/reviews/t5184/m1-group-G1.md` ×2, `m1-group-G4.md` ×5, `m1-sample-manifest.tsv` ×1, `m1-summary.md` ×1 |
| `pfirsch-schulueter-regime` | aliases ×2 (`8953,8954`), concepts ×1 (`2711`), definitions ×2 (`1206,2264`), evidence ×1 (`2570`) = **6** | `terms/allowlist_en.txt:1597` ×1, `.github/plans/t4973-batches/w2.ids/w2_b13.ids` ×2, `docs/reviews/t5184/m1-group-G1.md` ×2, `m1-group-G4.md` ×3, `m1-summary.md` ×1 |

### (d) Allowlist scan (`terms/allowlist_zh.txt` + `terms/allowlist_en.txt`) — **OUT OF SCOPE, read-only**

```console
$ for s in …; do printf '%s zh=%s en=%s\n' "$s" "$(grep -Fxc "$s" terms/allowlist_zh.txt)" "$(grep -Fxc "$s" terms/allowlist_en.txt)"; done
```

| string | `allowlist_zh.txt` count | `allowlist_en.txt` count | registry kind |
|---|---|---|---|
| `普费尔施-施吕特尔状态` | **1** (`:2562`) | 0 | preferred zh (2711) |
| `普费尔施-施吕特区` | 0 | 0 | **forbidden** zh (`aliases.tsv:4242`) |
| `Pfirsch-Schlüter区` | **1** (`:115`) | 0 | preferred zh (909) |
| `Pfirsch-Schlüter regime` | 0 | 0 | preferred en (909) |
| `Pfirsch-Schulueter regime` | 0 | 0 | preferred en (2711) |
| `PS regime` | 0 | 0 | alias en (909) |
| `pfirsch-schlueter-regime` | 0 | 0 | concept_id (909) |
| `pfirsch-schulueter-regime` | 0 | **1** (`:1597`) | concept_id (2711) |

⇒ Only **two** allowlist entries touch this family: `allowlist_zh.txt:115 = Pfirsch-Schlüter区` and `:2562 = 普费尔施-施吕特尔状态` (both attached to **preferred** aliases ⇒ no bridge-check leak today). The **forbidden** face `普费尔施-施吕特区` is in **neither** allowlist today (that is why baseline `validate_registry` = exit 0).

### (e) `validate_registry` preferred-alias rule (re-read, `pipeline/validate_registry.py:205-228`)

```python
if kind == "preferred":
    concepts_with_preferred.add(concept_id)
...
missing_preferred = sorted(concept_ids - concepts_with_preferred)
if missing_preferred:
    _fail(aliases_path, 1, f"concepts without preferred alias: {preview}{more}")
```

⇒ **Each concept requires ≥1 `preferred` alias** (lower bound only; **no upper bound** — a concept may hold several preferred aliases; validate_registry does not forbid that. The "preferred 双声明" consistency question is the separate open internal issue **O-6**, not enforced here).

Two further hard rules that govern any merge (`validate_registry.py`):
- `if concept_id not in concept_ids: _fail(…, f"unknown concept_id {concept_id!r}")` — an alias (or definition/evidence) row pointing at a removed cid **fails**.
- `if alias in alias_to_concept and alias_to_concept[alias] != concept_id: _fail("alias … maps to multiple concept_ids")` — an alias string may map to exactly one cid.
- **Bridge check** (`:309-327`): any alias whose `kind ∈ {forbidden, deprecated}` must **not** appear in either allowlist, else `SystemExit`.

---

## 2. Decision — **③ 只登记不改 (`UNDECIDABLE`)**

Option ① is authorised **only if** the evidence gate (`authoritative attribution` **AND** `orthography confirmable`) **and** the mechanical-achievability gate (no `terms/allowlist_*` write, no canonical-zh change, no edit of forbidden row `aliases.tsv:4242`) are **both** satisfied. **Three independent conditions fail.**

### Blocker 1 — Orthography NOT confirmable from in-repo authoritative sources (dispositive)

Three mutually inconsistent Latin spellings coexist in-repo, and **no in-repo authoritative source adjudicates between them**:

| form | where |
|---|---|
| `Pfirsch-Schlüter` (umlaut) | corpus side: `aliases.tsv:2930/2931`, `definitions.tsv:5009/5010`, `allowlist_zh.txt:115`, `translation_dict.json:6652+` |
| `Pfirsch-Schulueter` | GB/T import: `gbt4960_9_diff.tsv:211`, `gbt4960_9_terms.tsv:211`, `concepts.tsv:2711`, `definitions.tsv:1206/2264`, `translation_dict.json:566/8028` |
| `Schlueter` | only the `concept_id` (`pfirsch-schlueter-regime`) + a historical plan-note (`terminology-coverage-and-definition-quality.md:1801`, recording that the annotation `(Pfirsch-Schlueter)` was *removed* from a notes draft) |

The **GB/T snapshot itself uses `Pfirsch-Schulueter`** — a form matching *neither* `Schlüter` nor `Schlueter` nor `Schluter`. The plan (§6.3 B2, 拟验证 ③) itself classifies the orthography call as **「属领域/文献裁决」** (a domain/literature adjudication), i.e. *not* resolvable inside the repo. Per the task rule, non-confirmable orthography ⇒ **UNDECIDABLE**.

### Blocker 2 — Authoritative attribution is weak (id-level link absent)

`gbt4960_9_diff.tsv:211` has **empty `matched_concept_id`** and `status = new` (§1b). The GB/T snapshot does **not** name `pfirsch-schulueter-regime` as the target; attribution rests solely on the zh-string coincidence `普费尔施-施吕特尔状态` and the concept's `source` column. That is a *plausible* correspondence, not an authoritative id-level assignment ⇒ the "authoritative attribution" half of the evidence gate is not met either.

### Blocker 3 — Merge is NOT mechanically achievable without an unauthorised write (empirically proven)

Retiring the FAIL item (`pfirsch-schlueter-regime`, 909) so that it merges into 2711 collides with the forbidden row `aliases.tsv:4242` and/or the allowlist. Two minimal mutants were run against **scratch copies** (never the repo), using the real `validate_registry`:

- **MUT1** — delete concept row `concepts.tsv:909`, keep all aliases/definitions/evidence:
  ```console
  $ python3 -m pipeline.validate_registry --terms-dir /tmp/opencode/t5259b2/terms
  registry validation failed: /tmp/opencode/t5259b2/terms/registry/aliases.tsv:2930: unknown concept_id 'pfirsch-schlueter-regime'
  exit=1
  ```
  The forbidden row `4242` **also** points at `pfirsch-schlueter-regime`; since `4242` **must not be modified/deleted** (§0.2 R2, 补核-only), its cid can never be retired ⇒ permanent orphan ⇒ Option ① is blocked.

- **MUT2** — keep 909 but demote its zh preferred `Pfirsch-Schlüter区` to `deprecated` (the natural "migrate-the-face" step):
  ```console
  $ python3 -m pipeline.validate_registry --terms-dir /tmp/opencode/t5259b2b/terms
  registry validation failed: forbidden/deprecated aliases must not appear in IME allowlists
  offending terms:
  - 'Pfirsch-Schlüter区'
  exit=1
  ```
  `Pfirsch-Schlüter区` is at `allowlist_zh.txt:115` ⇒ demoting it (or any forbidden/deprecated treatment that keeps the string) **trips the bridge check**. Avoiding that requires writing to `terms/allowlist_zh.txt` — **out of scope / hard-boundary forbidden**.

For completeness, the *only* mechanically-valid variant — **MUT3** — merely flips 909's concept `status` to `deprecated` while keeping the whole row:
```console
$ python3 -m pipeline.validate_registry --terms-dir /tmp/opencode/t5259b2c/terms
registry OK: 3076 concepts, 10250 aliases, 3203 evidence rows, 6152 definitions
exit=0
```
This is **not the authorised Option ①** (it merges nothing — both concepts and both zh faces persist; no ν*/face migration), it leaves the orthography/attribution questions open, and it would be the repo's **first-ever** `deprecated` concept (current status distribution: `3076 active`, `0 deprecated`). It is recorded here as a **candidate for a future adjudicated task**, not executed.

### Conclusion

Option ① fails the evidence gate (Blockers 1 & 2) **and** the mechanical gate (Blocker 3), and Option ② is forbidden (would change a canonical Chinese face). ⇒ **③ 只登记不改 — `UNDECIDABLE`; D5 remains FAIL; no data change.**

---

## 3. Concrete suggestion (for a future, separately-adjudicated task)

Not authorised now; recorded per §6.3 B2 (「只登记建议」):

1. **Adjudicate the orthography first** (domain/literature call, external to repo): decide canonical Latin form among `Pfirsch-Schlüter` (corpus, umlaut-correct) vs `Pfirsch-Schulueter` (GB/T snapshot). Note the GB/T form appears to be a transliteration artifact; the physically-correct physicist name is **Pfirsch-Schlüter**.
2. **Resolve the `aliases.tsv:4242` coupling before any merge.** As long as forbidden row `4242` points at `pfirsch-schlueter-regime` and may not be rewritten (§0.2 R2), that cid cannot be retired. A future task must first obtain authority to either (a) repoint `4242` to the surviving cid, or (b) delete it, or (c) formally abandon cid retirement.
3. **If cid retirement is ever authorised**, then *and only then*: delete `concepts.tsv:909` + its dependent rows (`aliases 2930/2931/2932`, `definitions 5009/5010`, `evidence 831`), migrate 909's `notes` (`High collisionality neoclassical transport regime`) onto `concepts.tsv:2711`, and add the retired id `pfirsch-schlueter-regime` as a **`deprecated` alias** of 2711 for id-stability (GM-4). Verify the bridge check: `pfirsch-schlueter-regime` is **not** in either allowlist today (§1d), so that specific string would not trip the check.
4. **Do NOT** introduce `deprecated`/`forbidden` treatment for `Pfirsch-Schlüter区` while it remains at `allowlist_zh.txt:115` unless the allowlist is concurrently (and authoritatively) changed — otherwise `validate_registry` exits non-zero (MUT2).
5. **Also flag** (separate, out-of-B2-scope observation): `concepts.tsv:2711` has an atypical `category = nuclear-fusion` rather than `concept`; and the plan §6.3 B2 wording "迁移其 notes 中的 ν* 判据" is imprecise — the ν* criterion is on the **target** side (`definitions.tsv:2264`), not on 909.

---

## 4. Gates (baseline, re-run on the unchanged tree — no data touched)

| gate | command | result |
|---|---|---|
| registry validator | `python3 -m pipeline.validate_registry` | `registry OK: 3076 concepts, 10250 aliases, 3203 evidence rows, 6152 definitions` — **exit 0** |
| row audit | `python3 scripts/registry_row_audit.py --audit` | `is_clean: true` — **exit 0** |
| batch self-test | `python3 scripts/registry_batch_verify.py --self-test` | `27/27 assertions passed` — **exit 0** |
| unit tests | `python3 -m pytest -o addopts="" -q` | `207 passed in 8.46s` — **exit 0** |

Before/after counts: **identical** (no data change) — 3076 concepts / 10250 aliases / 3203 evidence / 6152 definitions.
Scratch mutants live only under `/tmp/opencode/t5259b2*` (never committed).

---

## 5. GM-4 id-stability statement

No id is retired in this task (UNDECIDABLE). **Had** Option ① been executed, the retired id `pfirsch-schlueter-regime` is referenced in **26** tracked locations, including two batch-authoring scripts (`scripts/batches/_batch36_44.py`, `_batch_forbidden8.py`) and the review/plan corpus (§1c) — hence the GM-4 requirement to keep it as a `deprecated` redirect alias. This coupling, plus the immutable forbidden row `4242`, is precisely why Blocker 3 is decisive.

## 6. Scope compliance

- Only file written: this report (`docs/reviews/t5184/repair-m1-b2-suggestion.md`).
- Untouched: `artifacts/terminology_sources/*`, `terms/allowlist_*`, `pipeline/*.py`, `terms/registry/*`, other D items' concepts, batch renames, `docs/publication/`, `evaluation/`, `.github/plans/publication-program-lre-scientificdata.md`.
- No `git add -A`, no `--no-verify`, no push/tag/dist/CHANGELOG.
