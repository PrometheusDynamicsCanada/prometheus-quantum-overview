# Prometheus Quantum: Verified Hardware Overview

**Prometheus helps quantum teams cut cloud hardware spend, run more circuits per job, and keep wider non-local circuits accurate across IBM, IQM, Rigetti, and QuEra processors.**

**[Website](https://prometheusdynamics.ca) · [Complexity Scaling Atlas](https://github.com/PrometheusDynamicsCanada/prometheus-circuit-complexity-atlas) · [Full Technical Report](DETAILED_TECHNICAL_REPORT.md) · [Start a Pilot](#start-a-pilot)**

## At a Glance

- **What Prometheus does:** Works alongside Qiskit SABRE O3 and Quantinuum TKET to route circuits, pack compatible jobs onto one chip, stop converged measurements early, and confirm results.
- **Lower billed spend:** **52% to 69% less QPU time/credits** per confirmed `<= 25 mHa` chemistry result, and **54.55% less IBM time** per accepted multi-family job.
- **Stronger gains as circuits grow:** Near parity on simple `3Q-6Q` chains, rising to **`2.35x-3.05x` overlap** on `13Q` Star-Hub circuits and **`1.57x-1.99x` vs. SABRE (`3.7x-30.3x` vs. TKET)** on `18Q-23Q` Dense All-to-All circuits.
- **Verified multi-cloud scale:** **`829` unique cloud QPU records** (`819` benchmark + `10` auxiliary, `0` duplicates), **`14,676` PUBs/schedules**, and **`22.40M` physical shots** across `7` cloud QPUs (`14` open quantum repositories).

![Non-Local Connectivity and Qubit-Width Scaling Across IBM Heron, IQM Crystal and AWS Rigetti](assets/fig1_nonlocal_scaling_star_and_dense_kn.png)
*Measured hardware scaling across `3Q-13Q` Central-Hub Star (`K_{1,N-1}`) and `7Q-23Q` Dense All-to-All (`K_N`) circuits on IBM, IQM, and AWS Rigetti.*

---

## 1. Key Questions & Where to Find the Proof

| Question | Headline Hardware Finding | Primary Repository |
| :--- | :--- | :--- |
| **Can I spend less per chemistry result?** | **`-52%` to `-69%`** charged IBM seconds & IQM credits (`172` jobs, `49/49` stops confirmed) | [`prometheus-quantum-chemistry`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-chemistry) |
| **How does it scale on wider / non-local graphs?** | **`27/32` (`84.4%`) `#1` wins**; **`2.35x-3.05x`** on `13Q` Star & **`1.57x`** on `18Q-19Q` Dense `K_N` | [`prometheus-circuit-complexity-atlas`](https://github.com/PrometheusDynamicsCanada/prometheus-circuit-complexity-atlas) |
| **Can I pack multiple circuits onto one chip?** | **`2.85x`/IBM s**, **`3.00x`/IQM credit**, and **`-54.55%` IBM s/accepted** across 4 families | [`prometheus-quality-gated-packing`](https://github.com/PrometheusDynamicsCanada/prometheus-quality-gated-packing) · [`prometheus-ibm-parallel-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-ibm-parallel-execution) |
| **Can difficult dense circuits pass checks?** | **`10/10` fresh + `5/5` (`+32h`)** passes on `15Q` IBM QFT & **`5/5`** on `12Q` IQM (`0` baseline) | [`prometheus-practical-execution-limits`](https://github.com/PrometheusDynamicsCanada/prometheus-practical-execution-limits) |
| **How does live queue & shot stopping behave?** | **`30/36` vs. `27/36`** accepted at `18 s` (IBM), **`+83.3%`** yield (IQM), **`0/31`** false stops | [`prometheus-quantum-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-execution) |
| **Does it work on Rigetti & neutral atoms?** | **`+6.61%`** post-recal on `108Q` Rigetti + **`+18.11%`** `12A` yield (`p = 0.0042`) on `256Q` QuEra | [`prometheus-braket-validation`](https://github.com/PrometheusDynamicsCanada/prometheus-braket-validation) |

## 2. Executive Compiler Summary (`N = 107` Matched 3-Way IBM Heron Jobs, `321` Circuits, `4,964,352` Shots)

*Hardware IDs:* `dbajlrhgv2cc73e6vuj0` .. `daf9p65nj4cs73ag3f20` across `ibm_fez`, `ibm_kingston`, and `ibm_marrakesh` (`4Q-23Q`, `*(mean)*` values shown; `*(median)*` values and `69`-job Dense `K_N` slice are in the expandable section below).

| Compiler (`N = 107` Jobs) | Overlap $F_B$ `(↑)` | Hellinger $F_H$ `(↑)` | `HOP` `(↑)` | `TVD` `(↓)` | `XEB` `(↑)` | Entropy `(↓)` | `2Q` `CZ` / Depth `(↓)` | Mean $F_B$ Delta |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Qiskit SABRE O3** | `0.3494` | `0.2624` | `52.13%` | `0.6565` | `233.5` | `11.79` | `338.8` / `321.2` | Best Baseline (`27/107` wins) |
| **Quantinuum TKET** | `0.2971` | `0.2277` | `50.23%` | `0.7184` | `109.4` | `11.92` | `532.5` / `464.1` | `-14.97%` vs. SABRE |
| **Prometheus** | **`0.3780`** | **`0.2742`** | **`53.70%`** | **`0.6286`** | **`290.3`** | **`11.67`** | **`290.9` / `256.6`** | **`+8.17%` vs. S (`+26.31%` on `K_N`)** |

*Metric Key:* $F_B = \sum_x \sqrt{P_{\text{ideal}}(x)P_{\text{meas}}(x)}$ (labeled `"State Fidelity"` in Studio UIs); $F_H = F_B^2$. `(↑)` higher is better, `(↓)` lower is better; **bold** marks winners. All baseline wins and unresolved regimes are published in full.

---

## Verify & Start a Pilot

- **Zero-credential 829-ID deduplication & SHA-256 audit:** `python scripts/verify_portfolio_accounting.py`
- **Start a supported pilot (`5-50` OpenQASM circuits):** [william@prometheusdynamics.ca](mailto:william@prometheusdynamics.ca) | [prometheusdynamics.ca](https://prometheusdynamics.ca)

---

## Deep-Dive Tables, All 14 Quantum Repositories & Technical Notes

<details>
<summary><strong>1. Complete Directory of All 14 Quantum Repositories (829 Unique Cloud Records · 22.40M Shots) - Click to expand</strong></summary>

Global portfolio totals are maintained in [`PORTFOLIO_ACCOUNTING_LEDGER.json`](PORTFOLIO_ACCOUNTING_LEDGER.json) (`829` unique provider records = `819` completed benchmark jobs/tasks + `10` auxiliary records across `475` IBM Quantum, `306` IQM Resonance, and `48` AWS Braket tasks; `14,676` PUBs/schedules; `22,398,648` physical shots; `0` cross-repository duplicates; simulations and GPU runs excluded):

| # | Repository | Incremental Scope (`Jobs`, `PUBs`, `Shots`) | Focus & Offline Verification Kind ([`PUBLIC_DISCLOSURE.md`](PUBLIC_DISCLOSURE.md)) |
| :---: | :--- | :---: | :--- |
| **1** | **[`prometheus-quantum-overview`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-overview)** | Hub (`0` incremental) | Portfolio hub, [`ARCHITECTURE.md`](ARCHITECTURE.md), & **829-ID deduplication verifier** |
| **2** | **[`prometheus-quantum-chemistry`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-chemistry)** | `172` jobs · `4,812` PUBs · `3,756,032` shots | `-52%` to `-69%` QPU cost per confirmed `<= 25 mHa` calc · **Ledger, billing & 42-run SPSA replay** |
| **3** | **[`prometheus-practical-execution-limits`](https://github.com/PrometheusDynamicsCanada/prometheus-practical-execution-limits)** | `24` jobs · `1,648` PUBs · `1,687,552` shots | `10/10` fresh + `5/5` (`+32h`) `15Q` QFT passes + boundaries · **Raw-histogram reconstruction** |
| **4** | **[`prometheus-quantum-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-execution)** | `157` rec (`149` bench) · `2,509` PUBs · `2,093,568` shots | Queue management & sequential shot stopping (`0/31` false stops) · **Billing & CRVE audit** |
| **5** | **[`prometheus-ibm-parallel-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-ibm-parallel-execution)** | `19` jobs · `586` PUBs · `655,360` shots | `2.85x` workloads/billed IBM second (8-way simultaneous) · **Raw-histogram reconstruction** |
| **6** | **[`prometheus-iqm-execution`](https://github.com/PrometheusDynamicsCanada/prometheus-iqm-execution)** | `59` jobs · `1,479` PUBs · `1,135,616` shots | `3.00x`/IQM credit 4-way parallel & `+3.73%` dense compilation · **Raw-histogram reconstruction** |
| **7** | **[`prometheus-ibm-compiler-benchmarks`](https://github.com/PrometheusDynamicsCanada/prometheus-ibm-compiler-benchmarks)** | `10` jobs · `441` circs · `755,712` shots | Same-window 3-way IBM tournaments (`65/99` vs. S, `89/99` vs. T) · **Raw payload + ledger audit** |
| **8** | **[`prometheus-ibm-scaling-benchmarks`](https://github.com/PrometheusDynamicsCanada/prometheus-ibm-scaling-benchmarks)** | `17` jobs · `1,023` circs · `1,047,552` shots | `4Q-17Q` 3-QPU repeat (`453`-seed SABRE control) + `8Q-101Q` mirrors · **Raw archive check** |
| **9** | **[`prometheus-braket-validation`](https://github.com/PrometheusDynamicsCanada/prometheus-braket-validation)** | `22` tasks · `462` runs · `463,800` shots | `108Q` Rigetti 3-window + `256`-atom QuEra Aquila MIS (`881` vs. `852` optima) · **Raw shot check** |
| **10** | **[`prometheus-processor-selection`](https://github.com/PrometheusDynamicsCanada/prometheus-processor-selection)** | Shared (`33` job ZIPs in #12 + `4` in #7) | `2.75x` observed spread across sibling `156Q` IBM Heron chips · **Raw IBM Job ZIP check** |
| **11** | **[`prometheus-noise-aware-routing`](https://github.com/PrometheusDynamicsCanada/prometheus-noise-aware-routing)** | `14` jobs · `774` PUBs · `4,125,440` shots | Exploratory `30/40` routing wins vs. `10/40` SWAP losses · **Raw `BitArray` reconstruction** |
| **12** | **[`prometheus-quantum-and-gpu-benchmarks`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-and-gpu-benchmarks)** | `119` QPU jobs · `357` circs · `5,084,160` shots | `107` IBM + `12` Braket QPU jobs + separate `150`-run H100 QUBO study · **Ledger & schedule check** |
| **13** | **[`prometheus-quality-gated-packing`](https://github.com/PrometheusDynamicsCanada/prometheus-quality-gated-packing)** | `29` rec (`28` bench) · `121` PUBs · `186,368` shots | `-54.55%` IBM s/acc (4 families) & `ABCCBA` `4-way` vs. `8-way` · **Raw-histogram check** |
| **14** | **[`prometheus-circuit-complexity-atlas`](https://github.com/PrometheusDynamicsCanada/prometheus-circuit-complexity-atlas)** | `187` rec (`186` bench) · `464` PUBs · `1,407,488` shots | `3Q-17Q` Star-Hub, Chemistry & Simultaneous 5-QPU Matrix (`27/32` `#1`) · **QASM + histogram check** |

*(Adjacent non-quantum repositories under the same GitHub account: [`argus-server-protection`](https://github.com/PrometheusDynamicsCanada/argus-server-protection) and [`Hyperion-fusion-telemetry`](https://github.com/PrometheusDynamicsCanada/Hyperion-fusion-telemetry).)*

</details>

<details>
<summary><strong>2. Full Mean & Median Breakdown on Dense All-to-All K_N (N = 69 Jobs) + Chemistry Cost Chart - Click to expand</strong></summary>

### Dense All-to-All `K_N` Subset (`N = 69` Matched 3-Way IBM Heron Jobs, `7Q-23Q`, `207` Circuits, `3,317,760` Shots)

| Compiler (`N = 69` `K_N` Jobs) | $F_B$ `*(mean / med)*` `(↑)` | $F_H$ `*(mean / med)*` `(↑)` | `HOP` `*(mean / med)*` `(↑)` | `TVD` `*(mean / med)*` `(↓)` | `XEB` `*(mean / med)*` `(↑)` | Entropy `*(mean / med)*` `(↓)` | `2Q` `CZ` / Depth `*(mean)*` `(↓)` | Pairwise Wins |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Qiskit SABRE O3** | `0.1731` / `0.0963` | `0.0745` / `0.0093` | `61.08%` / `59.19%` | `0.8035` / `0.8571` | `228.7` / `80.3` | `12.72` / `13.53` | `410.4` / `361.4` | `12 / 69` vs. Prom |
| **Quantinuum TKET** | `0.1091` / `0.0321` | `0.0466` / `0.0010` | `58.54%` / `58.72%` | `0.8761` / `0.9440` | `40.1` / `22.9` | `12.94` / `13.79` | `667.9` / `505.3` | `1 / 69` vs. Prom |
| **Prometheus** | **`0.2186` / `0.1444`** | **`0.0950` / `0.0208`** | **`63.55%` / `61.98%`** | **`0.7573` / `0.8089`** | **`316.1` / `185.7`** | **`12.54` / `13.37`** | **`352.0` / `279.8`** | **`+26.31%` mean (`+50.0%` med)** |

*(Full `N = 107` pooled medians: $F_B$ `0.2076` Prom vs. `0.1645` SABRE / `0.0732` TKET; $F_H$ `0.0431` vs. `0.0271` / `0.0054`; `HOP` `60.81%` vs. `57.32%` / `56.79%`; `TVD` `0.7501` vs. `0.8088` / `0.8851`; `XEB` `55.70` vs. `35.04` / `10.20`; Entropy `12.94` vs. `13.17` / `13.53`; `CZ` `317.0` vs. `351.0` / `559.0`; Depth `266.0` vs. `342.0` / `478.0`.)*

![Charged Hardware Resources per Accepted Molecular-Energy Result](assets/fig0_opening_chemistry_charged_cost.png)
*Charged IBM seconds and IQM credits per confirmed `<= 25.0 mHa` chemistry calculation across 24 held-out molecular configurations repeated three times ([`prometheus-quantum-chemistry`](https://github.com/PrometheusDynamicsCanada/prometheus-quantum-chemistry)).*

### How Prometheus Works Alongside Qiskit SABRE O3 & Quantinuum TKET
- **Evaluates candidates across compilers:** Falls back to baseline compilations whenever extra routing gates would hurt accuracy.
- **Uses live chip calibration & topology:** Avoids defective couplers and readout hotspots across Heavy-Hex and Square lattices.
- **Packs & stops safely:** Co-schedules compatible circuits simultaneously and stops converged shot ladders early (`0/31` false stops).
- **Commercial scope note:** Published savings measure provider-billed QPU resources on benchmark circuits (excluding software, classical compute, and integration costs). See [`DETAILED_TECHNICAL_REPORT.md`](DETAILED_TECHNICAL_REPORT.md), [`PUBLIC_DISCLOSURE.md`](PUBLIC_DISCLOSURE.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), and [`SCREENSHOT_GALLERY.md`](SCREENSHOT_GALLERY.md).

</details>
