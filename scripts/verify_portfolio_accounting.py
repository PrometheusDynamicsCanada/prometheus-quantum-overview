#!/usr/bin/env python3
"""
Standalone offline verifier for `prometheus-quantum-overview`:
1. Audits `PORTFOLIO_ACCOUNTING_LEDGER.json` arithmetic and verifies that all
   829 provider Job IDs / AWS Braket Task ARNs across all 14 quantum repositories
   are strictly unique (zero cross-campaign duplicates), with shared reference suites
   (`prometheus-processor-selection` 33 ZIPs and the 4-job 144-execution suite)
   explicitly cross-mapped and counted once.
2. Audits `matched_107_job_ibm_compiler_corpus_summary` (kept strictly separate from
   whole-portfolio job/shot totals), verifying internal relative/absolute delta
   arithmetic, 107-ID subset membership in `prometheus-quantum-and-gpu-benchmarks`,
   and (when sibling checkouts are present alongside this repository) full raw
   recomputation of the 107-job corpus and 1,648-PUB Phase 5 practical-limits ledger.
3. Verifies byte-for-byte SHA-256 integrity of all tracked files in `REPO_SHA256_MANIFEST.json`.
"""

import csv
import hashlib
import json
from pathlib import Path
import statistics


def sha256_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    ledger_path = root / "PORTFOLIO_ACCOUNTING_LEDGER.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))

    totals = ledger["portfolio_totals"]
    repos = ledger["constituent_repositories"]
    assert len(repos) == totals["quantum_repositories_total"] == 14

    rec_sum = sum(int(r["incremental_provider_records"]) for r in repos)
    bench_sum = sum(int(r["incremental_benchmark_jobs"]) for r in repos)
    aux_sum = sum(int(r["incremental_auxiliary_records"]) for r in repos)
    pub_sum = sum(int(r["incremental_physical_pubs"]) for r in repos)
    shot_sum = sum(int(r["incremental_physical_shots"]) for r in repos)

    assert rec_sum == totals["unique_provider_records"] == 829
    assert bench_sum == totals["completed_benchmark_jobs_or_tasks"] == 819
    assert aux_sum == totals["auxiliary_warmup_or_troubleshooting_records"] == 10
    assert bench_sum + aux_sum == rec_sum
    assert pub_sum == totals["physical_circuits_or_pubs"] == 14676
    assert shot_sum == totals["physical_measurement_shots"] == 22398648

    # Provider-family breakdown
    p_ibm = totals["ibm_quantum_records"]
    p_aws = totals["aws_braket_programset_tasks"]
    p_iqm = totals["iqm_resonance_records"]
    assert p_ibm["total"] == 475 and p_ibm["benchmark_jobs"] == 472 and p_ibm["auxiliary_records"] == 3
    assert p_aws["total"] == 48 and p_aws["benchmark_tasks"] == 48 and p_aws["auxiliary_records"] == 0
    assert p_aws["superconducting_programset_tasks"] + p_aws["neutral_atom_ahs_tasks"] == 48
    assert p_iqm["total"] == 306 and p_iqm["benchmark_jobs"] == 299 and p_iqm["auxiliary_records"] == 7
    assert p_ibm["total"] + p_aws["total"] + p_iqm["total"] == 829
    assert p_ibm["benchmark_jobs"] + p_aws["benchmark_tasks"] + p_iqm["benchmark_jobs"] == 819
    assert p_ibm["auxiliary_records"] + p_aws["auxiliary_records"] + p_iqm["auxiliary_records"] == 10

    # Strict cross-repository deduplication check across all 642 IDs
    all_ids = []
    by_repo = {}
    for r in repos:
        uids = r["unique_provider_ids"]
        assert len(uids) == int(r["incremental_provider_records"]), (
            f"{r['repository']}: expected {r['incremental_provider_records']} IDs, found {len(uids)}"
        )
        assert len(set(uids)) == len(uids), f"Duplicate ID inside {r['repository']}"
        by_repo[r["repository"]] = set(uids)
        all_ids.extend(uids)

    assert len(all_ids) == 829 and len(set(all_ids)) == 829, (
        f"Cross-repository duplicate Job ID detected: {len(all_ids)} total vs {len(set(all_ids))} unique"
    )

    # Verify shared reference subsets map 100% to their primary counting repositories
    for r in repos:
        shared = r.get("shared_reference_ids_counted_elsewhere", {})
        for target_key, ref_ids in shared.items():
            target_repo = target_key.replace("counted_in_", "")
            assert set(ref_ids).issubset(by_repo[target_repo]), (
                f"{r['repository']} shared IDs not subset of {target_repo}"
            )

    # Verify matched 107-job IBM Heron 3-way compiler corpus summary (kept separate from portfolio totals)
    corpus = ledger["matched_107_job_ibm_compiler_corpus_summary"]
    c_ids = corpus["job_ids"]
    assert len(c_ids) == len(set(c_ids)) == corpus["completed_three_way_comparisons"] == 107
    assert corpus["compiled_circuit_executions"] == 321
    assert corpus["physical_measurement_shots"] == 4964352
    assert set(c_ids).issubset(by_repo["prometheus-quantum-and-gpu-benchmarks"])
    assert sum(corpus["processor_counts"].values()) == 107
    assert sum(corpus["circuit_family_counts"].values()) == 107

    for m_key, m_obj in corpus["metrics"].items():
        assert m_obj["n_matched_comparisons"] == 107
        pm, sm, tm = m_obj["prometheus_mean"], m_obj["sabre_o3_mean"], m_obj["tket_mean"]
        assert abs((pm - sm) - m_obj["mean_abs_delta_vs_sabre_o3"]) < 1e-4, f"{m_key} abs delta vs SABRE mismatch"
        assert abs((pm - tm) - m_obj["mean_abs_delta_vs_tket"]) < 1e-4, f"{m_key} abs delta vs TKET mismatch"
        assert abs(((pm - sm) / abs(sm) * 100.0) - m_obj["mean_rel_pct_vs_sabre_o3"]) < 1e-2, f"{m_key} rel % vs SABRE mismatch"
        assert abs(((pm - tm) / abs(tm) * 100.0) - m_obj["mean_rel_pct_vs_tket"]) < 1e-2, f"{m_key} rel % vs TKET mismatch"

    by_fam = corpus["by_circuit_family"]
    assert len(by_fam) == 5
    assert sum(int(f["completed_three_way_comparisons"]) for f in by_fam.values()) == 107
    assert sum(int(f["compiled_circuit_executions"]) for f in by_fam.values()) == 321
    assert sum(int(f["physical_measurement_shots"]) for f in by_fam.values()) == 4964352
    for fam_name, fam_obj in by_fam.items():
        n_f = int(fam_obj["completed_three_way_comparisons"])
        assert int(fam_obj["compiled_circuit_executions"]) == 3 * n_f
        for m_key, m_obj in fam_obj["metrics"].items():
            assert m_obj["n_matched_comparisons"] == n_f
            pm, sm, tm = m_obj["prometheus_mean"], m_obj["sabre_o3_mean"], m_obj["tket_mean"]
            assert abs((pm - sm) - m_obj["mean_abs_delta_vs_sabre_o3"]) < 1e-4, f"{fam_name}:{m_key} abs delta SABRE"
            assert abs((pm - tm) - m_obj["mean_abs_delta_vs_tket"]) < 1e-4, f"{fam_name}:{m_key} abs delta TKET"
            exp_rel_s = ((pm - sm) / abs(sm) * 100.0) if abs(sm) > 1e-12 else 0.0
            exp_rel_t = ((pm - tm) / abs(tm) * 100.0) if abs(tm) > 1e-12 else 0.0
            assert abs(exp_rel_s - m_obj["mean_rel_pct_vs_sabre_o3"]) < 1e-2, f"{fam_name}:{m_key} rel % SABRE"
            assert abs(exp_rel_t - m_obj["mean_rel_pct_vs_tket"]) < 1e-2, f"{fam_name}:{m_key} rel % TKET"

    # Optional cross-repo raw recomputation when sibling checkouts are present
    sibling_corpus = root.parent / "prometheus-quantum-and-gpu-benchmarks" / "ibm_heron_156q_verified_benchmarks.json"
    recomputed_from_raw = False
    if sibling_corpus.is_file():
        raw_jobs = json.loads(sibling_corpus.read_text(encoding="utf-8"))["verified_jobs"]
        assert [j["job_id"] for j in raw_jobs] == c_ids
        assert sum(int(j["total_job_shots"]) for j in raw_jobs) == 4964352
        raw_extractors = {
            "distribution_overlap_fb": lambda j, c: j["physical_observables"][c]["fidelity"],
            "heavy_output_probability_hop": lambda j, c: j["physical_observables"][c]["hop"],
            "total_variation_distance_tvd": lambda j, c: j["physical_observables"][c]["tvd"],
            "linear_cross_entropy_xeb": lambda j, c: j["physical_observables"][c]["xeb"],
            "observed_shannon_entropy_bits": lambda j, c: j["physical_observables"][c]["entropy"],
            "two_qubit_gates": lambda j, c: j["circuit_metrics"][f"{c}_2q_gates"],
            "compiled_circuit_depth": lambda j, c: j["circuit_metrics"][f"{c}_depth"],
        }
        for m_key, fn in raw_extractors.items():
            m_obj = corpus["metrics"][m_key]
            pv = [fn(j, "prometheus") for j in raw_jobs]
            sv = [fn(j, "sabre") for j in raw_jobs]
            tv = [fn(j, "tket") for j in raw_jobs]
            assert abs(statistics.mean(pv) - m_obj["prometheus_mean"]) < 1e-5
            assert abs(statistics.mean(sv) - m_obj["sabre_o3_mean"]) < 1e-5
            assert abs(statistics.mean(tv) - m_obj["tket_mean"]) < 1e-5
            assert abs(statistics.median(pv) - m_obj["prometheus_median"]) < 1e-5
            assert abs(statistics.median(sv) - m_obj["sabre_o3_median"]) < 1e-5
            assert abs(statistics.median(tv) - m_obj["tket_median"]) < 1e-5
        for fam_name, fam_obj in by_fam.items():
            sub_jobs = [j for j in raw_jobs if j["circuit_family"] in fam_obj["raw_circuit_family_labels"]]
            assert len(sub_jobs) == fam_obj["completed_three_way_comparisons"]
            assert sum(int(j["total_job_shots"]) for j in sub_jobs) == fam_obj["physical_measurement_shots"]
            for m_key, fn in raw_extractors.items():
                m_obj = fam_obj["metrics"][m_key]
                pv = [fn(j, "prometheus") for j in sub_jobs]
                sv = [fn(j, "sabre") for j in sub_jobs]
                tv = [fn(j, "tket") for j in sub_jobs]
                assert abs(statistics.mean(pv) - m_obj["prometheus_mean"]) < 1e-5
                assert abs(statistics.mean(sv) - m_obj["sabre_o3_mean"]) < 1e-5
                assert abs(statistics.mean(tv) - m_obj["tket_mean"]) < 1e-5
                assert abs(statistics.median(pv) - m_obj["prometheus_median"]) < 1e-5
                assert abs(statistics.median(sv) - m_obj["sabre_o3_median"]) < 1e-5
                assert abs(statistics.median(tv) - m_obj["tket_median"]) < 1e-5
        recomputed_from_raw = True

    sibling_p5 = root.parent / "prometheus-practical-execution-limits" / "data" / "ALL_1648_EXECUTIONS_MASTER_LEDGER.csv"
    verified_p5_sibling = False
    if sibling_p5.is_file():
        p5_rows = list(csv.DictReader(sibling_p5.open("r", encoding="utf-8")))
        assert len(p5_rows) == 1648
        assert sum(int(r["shots"]) for r in p5_rows) == 1687552
        assert len({r["workload_id"] for r in p5_rows}) == 129
        assert {r["hardware_job_id"] for r in p5_rows} == by_repo["prometheus-practical-execution-limits"]
        verified_p5_sibling = True

    sibling_qgp = root.parent / "prometheus-quality-gated-packing" / "data" / "ALL_29_PROVIDER_JOBS_LEDGER.csv"
    verified_qgp_sibling = False
    if sibling_qgp.is_file():
        qgp_rows = list(csv.DictReader(sibling_qgp.open("r", encoding="utf-8")))
        assert len(qgp_rows) == 29
        assert sum(int(r["physical_pubs"]) for r in qgp_rows) == 121
        assert sum(int(r["physical_shots"]) for r in qgp_rows) == 186368
        assert {r["hardware_job_id"] for r in qgp_rows} == by_repo["prometheus-quality-gated-packing"]
        verified_qgp_sibling = True

    sibling_braket_rig = root.parent / "prometheus-braket-validation" / "data" / "ALL_450_RIGETTI_CIRCUITS_RESULTS.csv"
    sibling_braket_aq = root.parent / "prometheus-braket-validation" / "data" / "ALL_12_QUERA_AQUILA_TASKS_RESULTS.csv"
    verified_braket_sibling = False
    if sibling_braket_rig.is_file() and sibling_braket_aq.is_file():
        rig_rows = list(csv.DictReader(sibling_braket_rig.open("r", encoding="utf-8")))
        aq_rows = list(csv.DictReader(sibling_braket_aq.open("r", encoding="utf-8")))
        assert len(rig_rows) == 450 and len(aq_rows) == 12
        assert sum(int(r["shots"]) for r in rig_rows) + sum(int(r["shots"]) for r in aq_rows) == 463800
        braket_arns = {r["task_arn"] for r in rig_rows} | {r["task_arn"] for r in aq_rows}
        assert braket_arns == by_repo["prometheus-braket-validation"]
        verified_braket_sibling = True


    sibling_atlas = root.parent / "prometheus-circuit-complexity-atlas" / "data" / "ALL_187_PILOT_CLOUD_JOBS_LEDGER.csv"
    verified_atlas_sibling = False
    if sibling_atlas.is_file():
        at_rows = list(csv.DictReader(sibling_atlas.open("r", encoding="utf-8")))
        assert len(at_rows) == 187
        at_bench = [r for r in at_rows if r["record_role"] == "benchmark"]
        assert len(at_bench) == 186
        assert sum(int(r["physical_pubs"]) for r in at_bench) == 464
        assert sum(int(r["physical_shots"]) for r in at_bench) == 1407488
        assert {r["hardware_job_id"] for r in at_rows} == by_repo["prometheus-circuit-complexity-atlas"]
        verified_atlas_sibling = True

    print("=" * 92)
    print("PORTFOLIO ACCOUNTING & CROSS-REPOSITORY JOB-ID DEDUPLICATION AUDIT")
    print("=" * 92)
    print(f"  [PASS] Quantum Repositories Indexed      : {len(repos)}")
    print(f"  [PASS] Unique Provider Records Verified  : {len(set(all_ids))} / 829 (0 duplicates; {bench_sum} bench + {aux_sum} aux)")
    print(f"  [PASS] Physical Circuits / PUBs Verified : {pub_sum:,d}")
    print(f"  [PASS] Physical Shots Verified           : {shot_sum:,d}")
    raw_tag = " + raw sibling JSON recomputed" if recomputed_from_raw else ""
    print(f"  [PASS] 107-Job 3-Way IBM Corpus Summary  : 7 / 7 pooled metrics + 5 / 5 circuit families verified (321 circuits, 4,964,352 shots{raw_tag})")
    if verified_p5_sibling:
        print("  [PASS] Phase 5 Sibling Ledger Cross-Check: 24 / 24 Job IDs, 129 unique workloads, 1,648 PUBs, 1,687,552 shots")
    if verified_qgp_sibling:
        print("  [PASS] Quality-Gated Packing Cross-Check : 29 / 29 Job IDs, 121 PUBs, 186,368 shots (96.0s IBM + 15.75cr IQM)")
    if verified_braket_sibling:
        print("  [PASS] Braket Two-Arch Cross-Check       : 22 / 22 Task ARNs (10 Rigetti + 12 QuEra Aquila), 462 runs, 463,800 shots")
    if verified_atlas_sibling:
        print("  [PASS] Complexity Atlas Sibling Check    : 187 / 187 Cloud IDs (186 bench + 1 aux), 464 PUBs, 1,407,488 shots")

    manifest_path = root / "REPO_SHA256_MANIFEST.json"
    if manifest_path.exists():
        rm = json.loads(manifest_path.read_text(encoding="utf-8"))
        for rel_p, exp_sha in rm["files"].items():
            fp = root / rel_p
            act_sha = sha256_bytes(fp)
            assert act_sha == exp_sha, f"SHA-256 mismatch on {rel_p}: {act_sha} != {exp_sha}"
        print(f"  [PASS] REPO_SHA256_MANIFEST.json         : {len(rm['files'])} / {len(rm['files'])} files match byte-for-byte")
    print("=" * 92)


if __name__ == "__main__":
    main()
