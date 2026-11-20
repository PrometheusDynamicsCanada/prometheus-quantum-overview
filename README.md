# Prometheus: Get More Useful Work from Quantum Hardware

**Prometheus helps teams get more useful results from quantum hardware by improving how calculations are compiled, scheduled, and executed.**

Cloud quantum processors charge by runtime or credit even when most of a chip sits idle, device calibration shifts, or fixed measurement budgets keep running after an answer has converged. Tested across superconducting and neutral-atom processors on IBM Quantum, IQM Resonance, and Amazon Braket alongside Qiskit SABRE, Quantinuum TKET, and documented vendor schedules, Prometheus delivered **52% to 69% lower charged hardware cost** per accepted molecular-energy result, **2.85x to 3.00x higher parallel throughput** per billed unit on small circuits, **repeated pass-versus-fail gains** on difficult dense circuits (`10/10` fresh passes and `5/5` repeat passes 32 hours later on IBM 15-qubit QFT, where both baselines passed `0`), and **two-window neutral-atom improvements** on `256`-atom `QuEra Aquila` (`881` vs. `852` exact optimal answers across `3,000` billed Rb-87 shots; `+18.11%` yield and `-15.35%` cost/optimum [`p = 0.0042`] on the hardest `12A` topology). Unresolved regimes and baseline wins are published alongside positive results.

**[Detailed results](DETAILED_TECHNICAL_REPORT.md) · [Verify the evidence](#verify-the-evidence) · [Discuss a pilot](#discuss-a-pilot)**

![Charged Hardware Resources per Accepted Molecular-Energy Result](assets/fig0_opening_chemistry_charged_cost.png)
*Opening example ([`prometheus-quantum-chemistry`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-chemistry)): Charged IBM seconds (left) and IQM credits (right) per independently confirmed molecular-energy result across 24 unseen configurations repeated three times.*

---

## 1. Customer Questions and Primary Evidence

Full denominators, provider job IDs, and statistical tests for each campaign are documented in [`DETAILED_TECHNICAL_REPORT.md`](DETAILED_TECHNICAL_REPORT.md) and the linked repositories:

| Customer Question | Primary Repository | Strongest Measured Outcome & Disclosed Boundary | Public Verification |
| :--- | :--- | :--- | :--- |
| **"Can I reduce what I spend per useful result?"** | **[`prometheus-quantum-chemistry`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-chemistry)** | **52% to 55% fewer IBM seconds** and **59% to 61% fewer IQM credits** per confirmed molecular-energy result (and **53% to 69% lower** during live iterative optimization); single-processor runs beat dual-cloud splits | Outcome-ledger, billing & optimization replay |
| **"Can I get more work through one processor?"** | **[`prometheus-ibm-parallel-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-ibm-parallel-execution)** · **[`prometheus-iqm-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-iqm-execution)** · **[`prometheus-quality-gated-packing`](https://github.com/PrometheusDynamicsCanada/prometheus-quality-gated-packing)** | **2.85x** qualifying workloads per billed IBM second, **3.00x** per IQM credit, **-54.55% billed IBM seconds/accepted** (`8/8` in `5.0 s`) across 4 circuit families, and **-10.0%** via quality-gated `4-way` vs. `8-way` near threshold | Raw-histogram reconstruction |
| **"Can difficult circuits pass quality checks?"** | **[`prometheus-practical-execution-limits`](https://github.com/PrometheusDynamicsCanada/prometheus-practical-execution-limits)** | **10/10 fresh + 5/5 (`+32h`)** confirmed passes on IBM 15Q dense QFT and **5/5** on IQM 12Q (`0` baseline passes); reports unresolved `16Q-17Q` and `ibm_fez` limits | Raw-histogram reconstruction |
| **"How are these coordinated on a live queue?"** | **[`prometheus-quantum-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-execution)** | **More accepted requests (`30` vs. `27`) at unchanged `18 s`** on IBM, **more accepted requests (`22` vs. `12`) at unchanged efficiency/credit** on IQM, and **0/31** false early stops | Outcome-ledger, billing & statistical audit |
| **"Does this extend beyond superconducting gates?"** | **[`prometheus-braket-validation`](https://github.com/PrometheusDynamicsCanada/prometheus-braket-validation)** | **`+3.91%` 3-window overlap** (`+6.61%` post-recalibration) on `108Q` Rigetti plus **`881` vs. `852` exact optima** (`+18.11%` yield / `-15.35%` cost/opt on hardest `12A`, `p = 0.0042`; `-40.34%` suboptimal MIS outcomes across `6/6` tasks) on `256`-atom `QuEra Aquila` | Raw-histogram & per-shot `pre`/`post_sequence` reconstruction |

### How Prometheus Works Alongside Existing Tools

Prometheus complements Qiskit SABRE, Quantinuum TKET, and cloud provider runtimes rather than replacing them:
- **Selects among execution options:** Evaluates candidate compilations across Qiskit SABRE, Quantinuum TKET, and Prometheus, falling back to baseline choices whenever extra routing gates would reduce quality.
- **Accounts for hardware characteristics:** Incorporates live device connectivity and calibration metrics across superconducting topologies.
- **Packs independent circuits:** Schedules compatible calculations simultaneously under a frozen execution policy.
- **Adjusts measurement effort:** Halts converged runs early using sequential confidence checks and skips unnecessary recompilation.
- **Checks results against acceptance criteria:** Pairs primary runs with independent confirmation measurements and native provider billing records.

*Benchmark Value vs. Commercial Opportunity:* These repositories establish measured improvements in **charged hardware resources**, throughput, and pass rates on benchmark workloads (excluding software, classical compute, and integration costs). Evaluating whether those gains transfer to a customer's specific proprietary circuits and production workflow is the goal of a bounded pilot.

---

## 2. Matched 107-Job 3-Way IBM Heron Compiler Corpus Summary (`321` Circuits, `4,964,352` Shots)

> [!NOTE]
> **Metric Conventions:** Classical Bhattacharyya Distribution Overlap is $F_B = \sum_x \sqrt{P_{\text{ideal}}(x) P_{\text{meas}}(x)}$ (labeled `"State Fidelity"` in Studio UIs); Squared Hellinger Fidelity is $F_H = F_B^2$; Total Variation Distance is $\text{TVD} = \frac{1}{2}\sum_x |P_{\text{ideal}}(x) - P_{\text{meas}}(x)|$. Direction indicators `(↑)` and `(↓)` show optimality; **bold** marks row winners. Kept strictly separate from whole-portfolio job totals; full per-family tables and Studio screenshots are in [`DETAILED_TECHNICAL_REPORT.md`](DETAILED_TECHNICAL_REPORT.md).

| Metric & Direction *(Source: [`ibm_heron_156q_verified_benchmarks.json`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-and-gpu-benchmarks/blob/main/ibm_heron_156q_verified_benchmarks.json))* | Pooled Corpus (`N = 107`, `4Q-23Q`) `*(mean / median)*`: Prom / SABRE / TKET | Pooled Mean Delta vs. SABRE / TKET | Dense All-to-All `K_N` (`N = 69`, `7Q-23Q`) `*(mean / median)*`: Prom / SABRE / TKET | Dense `K_N` Mean Delta & Pairwise Wins |
| :--- | :---: | :---: | :---: | :---: |
| **Distribution Overlap $F_B$ `(↑)`** | **0.3780 / 0.2076** · 0.3494 / 0.1645 · 0.2971 / 0.0732 | **+8.17%** / **+27.23%** | **0.2186 / 0.1444** · 0.1731 / 0.0963 · 0.1091 / 0.0321 | **+26.31%** *(+50.0% med)* / **+100.45%** (`57/69` vs. S · `68/69` vs. T) |
| **Heavy-Output Probability $\text{HOP}$ `(↑)`** | **53.70% / 60.81%** · 52.13% / 57.32% · 50.23% / 56.79% | **+1.58 pp** / **+3.47 pp** | **63.55% / 61.98%** · 61.08% / 59.19% · 58.54% / 58.72% | **+2.47 pp** / **+5.01 pp** (`50/69` vs. S · `52/69` vs. T) |
| **Total Variation Distance $\text{TVD}$ `(↓)`** | **0.6286 / 0.7501** · 0.6565 / 0.8088 · 0.7184 / 0.8851 | **-4.24%** / **-12.50%** | **0.7573 / 0.8089** · 0.8035 / 0.8571 · 0.8761 / 0.9440 | **-5.74%** / **-13.56%** (`58/69` vs. S · `68/69` vs. T) |
| **Linear Cross-Entropy $\text{XEB}$ `(↑)`** | **290.29 / 55.70** · 233.51 / 35.04 · 109.40 / 10.20 | **+24.31%** / **+165.34%** | **316.09 / 185.67** · 228.74 / 80.28 · 40.10 / 22.92 | **+38.19%** / **+688.35%** (`54/69` vs. S · `68/69` vs. T) |
| **Observed Shannon Entropy $H$ `(bits, ↓)`** | **11.67 / 12.94** · 11.79 / 13.17 · 11.92 / 13.53 | **-0.99%** / **-2.09%** | **12.54 / 13.37** · 12.72 / 13.53 · 12.94 / 13.79 | **-1.40%** / **-3.11%** (`56/69` vs. S · `68/69` vs. T) |
| **Native Two-Qubit `CZ` Gates `(↓)`** | **290.86 / 317.00** · 338.84 / 351.00 · 532.50 / 559.00 | **-14.16%** / **-45.38%** | **351.96 / 358.00** · 410.38 / 436.00 · 667.87 / 717.00 | **-14.24%** / **-47.30%** (`61/69` vs. S · `69/69` vs. T) |
| **Compiled Circuit Depth `(↓)`** | **256.64 / 266.00** · 321.19 / 342.00 · 464.09 / 478.00 | **-20.10%** / **-44.70%** | **279.78 / 295.00** · 361.36 / 370.00 · 505.26 / 501.00 | **-22.58%** / **-44.63%** (`69/69` wins vs. TKET) |

---

## Verify the Evidence

**Reconciled Portfolio Scope (`13` Quantum Repositories):** `642` unique provider records (`633` completed benchmark jobs/tasks + `9` auxiliary records) and `20,991,160` physical measurement shots.

Global portfolio totals are maintained exclusively in [`PORTFOLIO_ACCOUNTING_LEDGER.json`](PORTFOLIO_ACCOUNTING_LEDGER.json) (`0` cross-repository duplicate Job IDs; simulations, classical GPU runs, unrecovered queue dispatches, and two setup smoke tests excluded; multiplexed physical shots are never multiplied by packed component circuits):
- **13 Quantum Repositories:** **`642` Unique Provider Records** = **`633` Completed Benchmark Jobs/Tasks** + `9` Auxiliary Warm-Up/Troubleshooting/Superseded Records (`369` IBM Heron [`366` bench + `3` aux], `239` IQM Resonance [`233` bench + `6` aux], `34` AWS Braket tasks [`22` superconducting `ProgramSet` + `12` `QuEra Aquila` neutral-atom `AHS`]) | **`14,212` Physical Circuits/PUBs/Schedules** | **`20,991,160` Physical Measurement Shots**.

```bash
python scripts/verify_portfolio_accounting.py
```

| # | Repository | Incremental Scope (`Jobs`, `PUBs`, `Shots`) | Focus & Verification Kind ([`PUBLIC_DISCLOSURE.md`](PUBLIC_DISCLOSURE.md)) |
| :---: | :--- | :---: | :--- |
| **1** | **[`prometheus-quantum-overview`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-overview)** | Hub (`0` incremental) | Portfolio overview, architecture ([`ARCHITECTURE.md`](ARCHITECTURE.md)), & **642-ID deduplication verifier** (`scripts/verify_portfolio_accounting.py`) |
| **2** | **[`prometheus-quantum-chemistry`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-chemistry)** | `172` jobs · `4,812` PUBs · `3,756,032` shots | Lower charged QPU cost per confirmed `<= 25 mHa` chemistry result · **Outcome-ledger, billing & 42-trajectory SPSA replay audit** |
| **3** | **[`prometheus-practical-execution-limits`](https://github.com/PrometheusDynamicsCanada/prometheus-practical-execution-limits)** | `24` jobs · `1,648` PUBs · `1,687,552` shots | Repeated dense pass-vs-fail boundaries across processors & `+32h` (`129` unique workloads) · **Raw-histogram reconstruction (`numpy`)** |
| **4** | **[`prometheus-quantum-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-execution)** | `157` rec (`149` bench) · `2,509` PUBs · `2,093,568` shots | Queue management, separated IBM/IQM economics & live shot stopping (`0/31` false stops) · **Outcome-ledger, billing & CRVE audit** |
| **5** | **[`prometheus-ibm-parallel-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-ibm-parallel-execution)** | `19` jobs · `586` PUBs · `655,360` shots | Simultaneous 8-way parallel throughput on IBM Heron (`2.85x`/billed s) + selection study · **Raw-histogram reconstruction (`1,140` evals)** |
| **6** | **[`prometheus-iqm-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-iqm-execution)** | `59` jobs · `1,479` PUBs · `1,135,616` shots | Separate 4-way IQM parallel (`3.00x`/credit) & dense-compilation (`+3.73%`) studies · **Raw-histogram reconstruction (`1,935` evals)** |
| **7** | **[`prometheus-ibm-compiler-benchmarks`](https://github.com/PrometheusDynamicsCanada/prometheus-ibm-compiler-benchmarks)** | `10` jobs · `441` circs · `755,712` shots | Same-window 3-way IBM compiler comparisons (`65/99` vs. SABRE, `89/99` vs. TKET) · **Raw payload (`144`) + tournament ledger audit** |
| **8** | **[`prometheus-ibm-scaling-benchmarks`](https://github.com/PrometheusDynamicsCanada/prometheus-ibm-scaling-benchmarks)** | `17` jobs · `1,023` circs · `1,047,552` shots | Multi-processor application circuits (`+5.42%` $F_H$, 453-seed controls) + 8Q-101Q mirrors · **Raw-measurement archive reconstruction** |
| **9** | **[`prometheus-braket-validation`](https://github.com/PrometheusDynamicsCanada/prometheus-braket-validation)** | `22` tasks · `462` runs · `463,800` shots | 3-window tracking on `108Q` Rigetti (`+3.91%`) + 2-window neutral-atom validation on `256`-atom `QuEra Aquila` (`881` vs. `852` optima) · **Raw-histogram + per-shot neutral-atom reconstruction** |
| **10** | **[`prometheus-processor-selection`](https://github.com/PrometheusDynamicsCanada/prometheus-processor-selection)** | Shared (`33` job ZIPs in #12 + `4` in #7) | Observed `2.75x` cross-processor spread across sibling 156Q IBM chips (`16Q-23Q`) · **Raw IBM Job ZIP payload reconstruction** |
| **11** | **[`prometheus-noise-aware-routing`](https://github.com/PrometheusDynamicsCanada/prometheus-noise-aware-routing)** | `14` jobs · `774` PUBs · `4,125,440` shots | Exploratory routing studies: `30/40` wins, `10/40` SWAP-overhead losses, distribution shifts · **Raw Qiskit `BitArray` reconstruction** |
| **12** | **[`prometheus-quantum-and-gpu-benchmarks`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-and-gpu-benchmarks)** | `119` QPU jobs · `357` circs · `5,084,160` shots | `107` IBM + `12` Braket QPU jobs archived alongside `150` separate classical H100 QUBO runs · **Outcome-ledger & schedule feasibility audit** |
| **13** | **[`prometheus-quality-gated-packing`](https://github.com/PrometheusDynamicsCanada/prometheus-quality-gated-packing)** | `29` rec (`28` bench) · `121` PUBs · `186,368` shots | 3-campaign quality-gated `4-way` vs. `8-way` `ABCCBA` (`-10.0%` s/acc near floor) & 4-family packing (`-54.55%` s/acc) · **Raw-histogram reconstruction (`numpy`)** |

*(Standalone Non-Quantum Product: [`argus-server-protection`](https://github.com/PrometheusDynamicsCanada/argus-server-protection) documents Linux connection-flood protection and is independent of the quantum portfolio.)*

---

## Discuss a Pilot

**Bring a representative workload and an acceptance criterion. We can compare Prometheus with your existing execution approach and measure quality, acceptance rate and charged hardware resources.**

- **Contact:** [william@prometheusdynamics.ca](mailto:william@prometheusdynamics.ca) | [prometheusdynamics.ca](https://prometheusdynamics.ca)
- **Supporting documentation:** [`DETAILED_TECHNICAL_REPORT.md`](DETAILED_TECHNICAL_REPORT.md) · [`PUBLIC_DISCLOSURE.md`](PUBLIC_DISCLOSURE.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`SCREENSHOT_GALLERY.md`](SCREENSHOT_GALLERY.md)
