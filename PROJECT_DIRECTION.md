# Roadmap & Cross-Paradigm Direction

Prometheus is designed to evaluate and optimize quantum execution economics across multiple hardware architectures and cloud providers:

1. **Superconducting & Neutral-Atom Cloud QPU Corpus (Operational Across 642 Cloud QPU Records):**
   - **IBM Quantum (156Q Heron r2):** `ibm_fez`, `ibm_marrakesh`, and `ibm_kingston`.
   - **IQM Resonance & Amazon Braket Superconducting QPUs:** `IQM Emerald` (54Q), `IQM Garnet` (20Q), and `Rigetti Cepheus-1-108Q` (108Q).
   - **Amazon Braket Neutral-Atom Analog QPU (`QuEra Aquila`, 256 Atoms):** Validated across two separated execution windows (`12` AHS tasks, `3,000` physical Rb-87 shots in [`prometheus-braket-validation`](https://github.com/PrometheusDynamicsCanada/prometheus-braket-validation)).
2. **Application Cost-to-Accuracy & Closed-Loop Variational Workflows (Operational):**
   - End-to-end molecular chemistry energy evaluation and cold-start iterative `SPSA` optimization (`prometheus-quantum-chemistry`), pairing buffered multi-slice chip packing with reference-free early stopping and standalone confirmation.
   - Next engineering milestone: cross-provider noise calibration matching so multi-cloud fleet splits match or exceed single-provider confirmed accuracy.
3. **Autonomous Queue Orchestration & Drift-Aware Refresh (Operational):**
   - Multi-window calibration tracking, selective placement remapping, and sequentially valid shot stopping (`prometheus-quantum-execution`).
4. **Trapped-Ion & Neutral-Atom Cross-Paradigm Compilation:**
   - Native continuous-angle synthesis for all-to-all trapped-ion processors (`AQT IBEX Q1`, `IonQ Forte 1`) and geometric register embedding for neutral-atom Analog Hamiltonian Simulation (`QuEra Aquila`).
5. **Hybrid Quantum-HPC Combinatorial Optimization:**
   - Constraint-preserving QUBO variable compression paired with GPU-accelerated combinatorial QUBO solvers (`VeloxQ NVIDIA H100`) and gate-model QAOA execution (`prometheus-quantum-and-gpu-benchmarks`).
