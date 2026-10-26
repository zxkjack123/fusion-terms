#!/usr/bin/env python3
"""Read-only fusion-terms registry gate evidence and handoff bundle."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_EVIDENCE_BYTES = 64 * 1024 * 1024
SUMMARY_BYTES = 4096
PROFILES = {"w0": "expect-clean", "all": "expect-clean-all"}
DATA_FILES = (
    "terms/registry/concepts.tsv",
    "terms/registry/aliases.tsv",
    "terms/registry/evidence.tsv",
    "terms/registry/definitions.tsv",
    "terms/allowlist_zh.txt",
    "terms/allowlist_en.txt",
)
CODE_FILES = (
    "pipeline/__init__.py",
    "pipeline/common.py",
    "pipeline/validate_registry.py",
    "scripts/registry_evidence_bundle.py",
    "scripts/registry_row_audit.py",
)
CHECKS = ("validate_registry", "registry_row_audit")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inventory(root: Path, names: tuple[str, ...]) -> dict[str, str]:
    return {name: sha256(root / name) for name in names}


def verify_regular_inventory(root: Path, names: tuple[str, ...]) -> dict[str, str]:
    for name in names:
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise SystemExit(f"refusing snapshot path: {name}")
    return inventory(root, names)


def execution_fingerprint(profile: str = "w0") -> tuple[str, dict]:
    status = subprocess.run(
        ["git", "status", "--porcelain=v1"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    status = "\n".join(
        line
        for line in status.splitlines()
        if not line.lstrip("?! ").startswith("artifacts/registry-evidence/")
    )
    payload = {
        "data": inventory(ROOT, DATA_FILES),
        "code": inventory(ROOT, CODE_FILES),
        "git_status": status,
        "python": sys.version,
        "executable": sys.executable,
        "profile": profile,
        "gate": PROFILES[profile],
        "max_evidence_bytes": MAX_EVIDENCE_BYTES,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest(), payload


def summary(text: str) -> str:
    return text.encode("utf-8", errors="replace")[:SUMMARY_BYTES].decode(
        "utf-8", errors="replace"
    )


def parse_result(
    check_id: str, rc: int, stdout: str, stderr: str, incomplete: bool, profile: str
) -> dict:
    result = {
        "check_id": check_id,
        "returncode": rc,
        "incomplete": incomplete,
        "stdout_summary": summary(stdout),
        "stderr_summary": summary(stderr),
    }
    if check_id == "validate_registry":
        result.update(
            status="pass" if rc == 0 and not incomplete else "fail",
            failure_detail=None if rc == 0 and not incomplete else (stderr or stdout),
            warnings=stderr.splitlines(),
            non_zero_metrics={},
        )
        return result
    try:
        audit = json.loads(stdout)
    except json.JSONDecodeError:
        return {
            **result,
            "status": "fail",
            "failure_detail": stderr or stdout,
            "warnings": stderr.splitlines(),
            "non_zero_metrics": {"invalid_json": 1},
        }
    non_zero = audit.get("non_zero_metrics", {})
    gate_pass = audit.get("w0_is_clean") if profile == "w0" else audit.get("is_clean")
    deferred = audit.get("deferred_w1_metrics", {}) if profile == "w0" else {}
    warnings = stderr.splitlines() + [
        f"deferred:{key}={value}" for key, value in deferred.items() if value
    ]
    passed = rc == 0 and bool(gate_pass) and not incomplete
    return {
        **result,
        "audit": audit,
        "gate_pass": bool(gate_pass),
        "status": "pass" if passed else "fail",
        "failure_detail": None if passed else non_zero,
        "warnings": warnings,
        "non_zero_metrics": non_zero,
    }


def copy_regular(source: Path, destination: Path) -> None:
    if source.is_symlink() or not source.is_file():
        raise SystemExit(f"refusing snapshot path: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def make_snapshot(target: Path) -> dict:
    before = inventory(ROOT, DATA_FILES + CODE_FILES)
    for name in DATA_FILES + CODE_FILES:
        copy_regular(ROOT / name, target / name)
    after = inventory(ROOT, DATA_FILES + CODE_FILES)
    if before != after:
        raise SystemExit("refusing evidence: source changed while snapshot was copied")
    snapshot = inventory(target, DATA_FILES + CODE_FILES)
    if snapshot != before:
        raise SystemExit("refusing evidence: snapshot hash mismatch")
    return snapshot


def run_cli(check_id: str, snapshot: Path, evidence_dir: Path, profile: str) -> dict:
    gate = PROFILES[profile]
    if check_id == "validate_registry":
        command = [
            sys.executable,
            "-m",
            "pipeline.validate_registry",
            "--terms-dir",
            "terms",
        ]
    else:
        command = [
            sys.executable,
            "scripts/registry_row_audit.py",
            "--audit",
            f"--{gate}",
            "--concepts",
            DATA_FILES[0],
            "--evidence",
            DATA_FILES[2],
            "--definitions",
            DATA_FILES[3],
        ]
    out_path, err_path = (
        evidence_dir / f"{check_id}.stdout",
        evidence_dir / f"{check_id}.stderr",
    )
    started = time.perf_counter_ns()
    with out_path.open("wb") as out, err_path.open("wb") as err:

        def limit_output() -> None:
            import resource

            resource.setrlimit(
                resource.RLIMIT_FSIZE, (MAX_EVIDENCE_BYTES, MAX_EVIDENCE_BYTES)
            )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(snapshot)
        proc = subprocess.Popen(
            command,
            cwd=snapshot,
            env=env,
            stdout=out,
            stderr=err,
            preexec_fn=limit_output,
        )
        rc = proc.wait()
    out_size, err_size = out_path.stat().st_size, err_path.stat().st_size
    incomplete = (
        out_size >= MAX_EVIDENCE_BYTES or err_size >= MAX_EVIDENCE_BYTES or rc < 0
    )
    stdout, stderr = (
        out_path.read_text(errors="replace"),
        err_path.read_text(errors="replace"),
    )
    result = parse_result(check_id, rc, stdout, stderr, incomplete, profile)
    result.update(
        wall_ms=(time.perf_counter_ns() - started) / 1_000_000,
        stdout_bytes=out_size,
        stderr_bytes=err_size,
        stdout_sha256=sha256(out_path),
        stderr_sha256=sha256(err_path),
    )
    return result


def result_key(result: dict) -> dict:
    return {
        key: result.get(key)
        for key in (
            "check_id",
            "returncode",
            "status",
            "incomplete",
            "warnings",
            "failure_detail",
            "non_zero_metrics",
        )
    }


def safe_bundle_path(bundle: Path, relative: str) -> Path:
    path = (bundle / relative).resolve()
    root = bundle.resolve()
    if path != root and root not in path.parents:
        raise SystemExit(f"refusing path outside bundle: {relative}")
    if path.is_symlink():
        raise SystemExit(f"refusing symlink evidence path: {relative}")
    if not path.is_file():
        raise SystemExit(f"refusing reuse: missing evidence path: {relative}")
    return path


def validate_manifest(bundle: Path, current_fingerprint: str | None = None) -> None:
    if bundle.is_symlink() or not bundle.is_dir():
        raise SystemExit("refusing reuse: invalid bundle path")
    manifest = json.loads(safe_bundle_path(bundle, "manifest.json").read_text())
    profile = manifest.get("profile")
    if manifest.get("schema") != 3 or profile not in PROFILES:
        raise SystemExit("refusing reuse: schema/profile mismatch")
    if (
        current_fingerprint is not None
        and manifest.get("execution_fingerprint") != current_fingerprint
    ):
        raise SystemExit("refusing reuse: execution fingerprint changed")
    expected = {(phase, check) for phase in ("baseline", "batch") for check in CHECKS}
    items = manifest.get("evidence", [])
    actual = {(item.get("phase"), item.get("check_id")) for item in items}
    if actual != expected:
        raise SystemExit("refusing reuse: incomplete phase/check evidence")
    snapshot = bundle / "snapshot"
    if snapshot.is_symlink() or not snapshot.is_dir():
        raise SystemExit("refusing reuse: missing or linked snapshot")
    if verify_regular_inventory(snapshot, DATA_FILES + CODE_FILES) != manifest.get(
        "snapshot_hashes"
    ):
        raise SystemExit("refusing reuse: snapshot hash mismatch")
    parsed = {}
    for item in items:
        phase, check = item["phase"], item["check_id"]
        out = safe_bundle_path(bundle, f"{phase}/{check}.stdout")
        err = safe_bundle_path(bundle, f"{phase}/{check}.stderr")
        if sha256(out) != item["stdout_sha256"] or sha256(err) != item["stderr_sha256"]:
            raise SystemExit(f"refusing reuse: tampered evidence {phase}/{check}")
        parsed[(phase, check)] = parse_result(
            check,
            item["returncode"],
            out.read_text(errors="replace"),
            err.read_text(errors="replace"),
            item["incomplete"],
            profile,
        )
    phase_results = {
        phase: [parsed[(phase, check)] for check in CHECKS]
        for phase in ("baseline", "batch")
    }
    if any(
        result_key(r) != manifest[phase][index]
        for phase in phase_results
        for index, r in enumerate(phase_results[phase])
    ):
        raise SystemExit("refusing reuse: phase result summary mismatch")
    same = all(
        result_key(a) == result_key(b)
        for a, b in zip(phase_results["baseline"], phase_results["batch"], strict=False)
    )
    if same != manifest.get("same_structured_result"):
        raise SystemExit("refusing reuse: comparison summary mismatch")
    if any(r["status"] != "pass" for r in phase_results["batch"]) or not same:
        raise SystemExit("refusing reuse: evidence incomplete or failed")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=tuple(PROFILES), default="w0")
    parser.add_argument("--compare", action="store_true")
    parser.add_argument("--reuse", type=Path)
    args = parser.parse_args(argv)
    output = ROOT / "artifacts" / "registry-evidence"
    output.mkdir(parents=True, exist_ok=True)
    with (output / ".registry-evidence.lock").open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise SystemExit("evidence bundle already running: lock held") from exc
        if args.reuse:
            fingerprint, _ = execution_fingerprint(args.profile)
            validate_manifest(args.reuse, fingerprint)
            print(
                json.dumps(
                    {
                        "check_id": "reuse",
                        "path": str(args.reuse),
                        "fingerprint": fingerprint,
                    }
                )
            )
            return 0
        bundle = (
            output / f"{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-{os.getpid()}"
        )
        with tempfile.TemporaryDirectory(prefix=".bundle-", dir=output) as temporary:
            staging = Path(temporary)
            snapshot_hashes = make_snapshot(staging / "snapshot")
            fingerprint, fingerprint_payload = execution_fingerprint(args.profile)
            if (
                snapshot_hashes
                != fingerprint_payload["data"] | fingerprint_payload["code"]
            ):
                raise SystemExit("refusing evidence: source changed after snapshot")
            baseline_dir, batch_dir = staging / "baseline", staging / "batch"
            baseline_dir.mkdir()
            batch_dir.mkdir()
            baseline = [
                run_cli(check, staging / "snapshot", baseline_dir, args.profile)
                for check in CHECKS
            ]
            batch = [
                run_cli(check, staging / "snapshot", batch_dir, args.profile)
                for check in CHECKS
            ]
            same = all(
                result_key(a) == result_key(b)
                for a, b in zip(baseline, batch, strict=False)
            )
            evidence = []
            for phase, results in (("baseline", baseline), ("batch", batch)):
                for result in results:
                    evidence.append(
                        {
                            "phase": phase,
                            "check_id": result["check_id"],
                            "returncode": result["returncode"],
                            "incomplete": result["incomplete"],
                            "stdout_sha256": result["stdout_sha256"],
                            "stderr_sha256": result["stderr_sha256"],
                        }
                    )
            incomplete = any(r["incomplete"] for r in baseline + batch)
            manifest = {
                "schema": 3,
                "profile": args.profile,
                "gate": PROFILES[args.profile],
                "execution_fingerprint": fingerprint,
                "fingerprint_payload": fingerprint_payload,
                "snapshot_hashes": snapshot_hashes,
                "checks": CHECKS,
                "baseline": [result_key(r) for r in baseline],
                "batch": [result_key(r) for r in batch],
                "same_structured_result": same,
                "incomplete": incomplete,
                "batch_status": "pass"
                if same and not incomplete and all(r["status"] == "pass" for r in batch)
                else "fail",
                "external_cli_entries": 1,
                "internal_cli_entries": 4,
                "baseline_wall_ms": sum(r["wall_ms"] for r in baseline),
                "batch_wall_ms": sum(r["wall_ms"] for r in batch),
                "evidence": evidence,
            }
            (staging / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True)
                + "\n"
            )
            os.replace(staging, bundle)
        print(
            json.dumps(
                {
                    "check_id": "registry-evidence-bundle",
                    "path": str(bundle),
                    "profile": args.profile,
                    "gate": PROFILES[args.profile],
                    "same_structured_result": manifest["same_structured_result"],
                    "status": manifest["batch_status"],
                    "external_cli_entries": 1,
                    "internal_cli_entries": 4,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0 if manifest["batch_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
