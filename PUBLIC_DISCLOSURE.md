# Public Disclosure, Verification Tiers & Portfolio Scope

This portfolio hub ([`prometheus-quantum-overview`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-overview)) indexes the 14 public quantum execution repositories published by Prometheus Dynamics Canada (`867` unique provider QPU Job/Task records across IBM Quantum, AWS Braket, and IQM Resonance; see [`PORTFOLIO_ACCOUNTING_LEDGER.json`](PORTFOLIO_ACCOUNTING_LEDGER.json) and `python scripts/verify_portfolio_accounting.py`).

## 1. Five Verification Tiers Across the Public Portfolio

Different repositories archive different levels of primary artifacts depending on payload size and IP boundaries. Readers and auditors should distinguish five distinct verification levels:

1. **Raw Measurement Histogram / `BitArray` Payload Reconstruction:**
   - Repositories archiving returned shot histograms or Qiskit `SamplerV2` `BitArray` payloads allow independent offline reconstruction of output probability distributions, Classical Bhattacharyya Overlap (`F_B`), Squared Hellinger Fidelity (`F_H = F_B²`), Total Variation Distance (`TVD`), task-specific observables, and (where physical OpenQASM circuits are included) compiled gate counts and depths:
     - [`prometheus-circuit-complexity-atlas`](https://github.com/PrometheusDynamicsCanada/prometheus-circuit-complexity-atlas) (`225` unique provider records [`224` benchmark + `1` auxiliary], `708` PUBs, `1,782,272` shots across `38` three-compiler groups + `1` packed companion, raw bitstring histograms + unrouted OpenQASM 2.0 + standalone `numpy/qiskit` verifier)
     - [`prometheus-practical-execution-limits`](https://github.com/PrometheusDynamicsCanada/prometheus-practical-execution-limits) (`1,648` physical PUBs across `24` QPU jobs and `129` unique logical workloads, raw bitstring histograms + unrouted OpenQASM 2.0 + standalone `numpy` verifier)
     - [`prometheus-quality-gated-packing`](https://github.com/PrometheusDynamicsCanada/prometheus-quality-gated-packing) (`112` logical evaluations across `29` provider records [`28` benchmark + `1` auxiliary], `121` PUBs, `186,368` shots, raw bitstring histograms + unrouted OpenQASM 2.0 + standalone `numpy` verifier)
     - [`prometheus-braket-validation`](https://github.com/PrometheusDynamicsCanada/prometheus-braket-validation) (`450` Rigetti circuits with raw shot counts + compiled QASM, plus `12` `QuEra Aquila` neutral-atom tasks with `3,000` raw `pre_sequence` / `post_sequence` Rb-87 shots)
     - [`prometheus-ibm-scaling-benchmarks`](https://github.com/PrometheusDynamicsCanada/prometheus-ibm-scaling-benchmarks) (`1,023` circuits, raw measurement archives)
     - [`prometheus-iqm-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-iqm-execution) (`1,935` evaluations across `59` jobs, raw bitstring histograms)
     - [`prometheus-ibm-compiler-benchmarks`](https://github.com/PrometheusDynamicsCanada/prometheus-ibm-compiler-benchmarks) (`144`-execution validation suite raw payloads + `297`-circuit tournament ledger)
     - [`prometheus-processor-selection`](https://github.com/PrometheusDynamicsCanada/prometheus-processor-selection) (`33` archived IBM Quantum job ZIP bundles + `144`-execution suite)
     - [`prometheus-noise-aware-routing`](https://github.com/PrometheusDynamicsCanada/prometheus-noise-aware-routing) (`14` archived IBM `SamplerV2` result payloads)
2. **Outcome-Ledger Consistency, Billing Arithmetic & Statistical Recomputation:**
   - Repositories storing per-workload, per-subcircuit, and per-rung measured hardware outcomes (`fb_measured`, `fh_measured`, `tvd_measured`, `observable_measured`) without full `2^n` raw bitstring tables verify internal arithmetic (`F_H = F_B²`), dual-criteria acceptance rules, provider billing efficiency ratios (`billed seconds`, `active seconds`, `credits`), sequential stopping trajectories, paired Student-`t` / Wilcoxon / McNemar tests, cluster-robust variance estimators (`CRVE`), exact cluster sign-flip permutation tests, and Holm-Bonferroni multiplicity adjustments:
     - [`prometheus-quantum-chemistry`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-chemistry) (`172` live QPU jobs, `4,812` PUBs, `3,756,032` shots, `42` replayed closed-loop `SPSA` trajectories)
     - [`prometheus-quantum-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-execution) (`157` provider records, `4,963` evaluations)
     - [`prometheus-ibm-parallel-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-ibm-parallel-execution) (`19` jobs, `1,140` evaluations)
     - [`prometheus-quantum-and-gpu-benchmarks`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-and-gpu-benchmarks) (`119` 3-way QPU jobs/tasks + `150` separate classical H100 GPU runs)
3. **Byte-Exact File Checksums (`REPO_SHA256_MANIFEST.json` & `REPOSITORY_SHA256SUMS.txt`):**
   - Checksum manifests verify that downloaded repository files match exact published `LF`-normalized Git archive bytes (`0` modifications after release packaging).
4. **Recorded SHA-256 References to Withheld Pre-Sanitization Artifacts:**
   - Where physical coordinate lists or internal scheduler columns are redacted for IP protection, fields such as `original_private_ledger_sha256` or `subgraph_sha256` preserve deterministic cryptographic references to private originals for continuity across files or confidential due-diligence audits; on their own in a public repository, they do not independently authenticate withheld private files.
5. **Local Runner Serialization Timestamps vs. Independent Pre-Submission Timestamping:**
   - Local JSON timestamp fields record runner serialization time on the benchmark host rather than third-party cryptographic timestamping before job submission (for example, [`prometheus-braket-validation`](https://github.com/PrometheusDynamicsCanada/prometheus-braket-validation) explicitly discloses that Tasks 1-2 reflect later runner-resume commitment serialization, while Tasks 3-10 precede provider submission timestamps).

## 2. Withheld Proprietary Implementation & Clean-Repository Provenance

- **Withheld Internals:** Proprietary hardware-aware optimization: Prometheus uses circuit structure and device calibration data to guide compilation and execution. Proprietary optimization, compilation, placement, and execution-control software, internal parameters, and physical qubit coordinate mappings are withheld across all public repositories.
- **Single-Commit Clean Repository Releases:** All public repositories in this portfolio are published as freshly initialized single-commit sanitized releases with isolated Git object histories (`0` historical pre-sanitization commits in repository object storage). Note that external copies downloaded prior to repository recreation cannot be recalled.
