# AGENTS.md — Project Governance & Engineering Rules

**Project:** Satellite-Based Multi-Hazard Disaster Risk Prediction and Early Warning System Using AI/ML  
**Repository Root:** `/Users/salman/Desktop/satellite-disaster`  
**Applicability:** Mandatory for all AI coding agents, subagents, and human contributors working in this repository.

---

## 1. Core Operating Principles

Every agent operating within this codebase must comply with the following twenty governing rules without exception:

1. **Pre-Task Instruction Review:** Read and understand relevant project instructions and phase guidelines before beginning any task.
2. **Pre-Implementation Workspace Inspection:** Inspect the actual filesystem and active codebase before proposing changes or assuming the existence/absence of files.
3. **Approval Gate Adherence:** Present a comprehensive plan and obtain explicit user approval before executing file modifications or advancing subphases.
4. **Focused Scope:** Make localized, surgical changes directly addressing the user request. Strictly avoid unrelated refactoring or stylistic reorganizations.
5. **Interface Preservation:** Preserve existing functionality, established public APIs, and documented interfaces unless an explicit deprecation is authorized.
6. **Test-Driven Progress:** Add or update automated unit/integration tests for any newly introduced functionality or behavioral modifications.
7. **Empirical Verification:** Run all applicable tests and report actual, unvarnished execution logs and verification outcomes.
8. **Scientific Honesty:** Never fabricate datasets, citations, benchmark metrics, model scores, predictions, or verification results.
9. **No Placeholder Deception:** Never present mock, hardcoded, or placeholder data as genuine satellite observations or real machine learning inferences.
10. **File Modification Restraint:** Never overwrite, delete, rename, or move existing project files without explicit user approval.
11. **System Safety:** Never execute destructive commands, system-wide package installations, OS upgrades, or background commands outside the designated workspace.
12. **Credential & Asset Security:** Never commit credentials, API tokens, passwords, local secrets, raw satellite imagery scenes, or large binary model weights.
13. **Isolated Python Runtime:** Use an isolated virtual environment (`.venv`) for all project dependencies; never install packages into the global system Python.
14. **Documentation Synchronization:** Keep all technical documentation, architecture records, and READMEs strictly synchronized with active code.
15. **Roadmap Discipline:** Follow the approved 13-phase master development sequence. Do not jump ahead across phase boundaries.
16. **No Gate Bypassing:** Never skip or declare a phase exit gate completed merely because generated code appears functional.
17. **Scope Consistency:** Maintain the eight in-scope hazards and four explicit exclusions consistent with the Phase 0 baselines.
18. **Academic Governance Checkpoints:** Mark all unapproved scope, architecture, or evaluation decisions as `PENDING_SUPERVISOR_REVIEW`.
19. **Scientific Task Disambiguation:** Strictly distinguish future forecasting, static susceptibility assessment, observational detection, storm tracking, index monitoring, and historical event mapping.
20. **Premature Architecture Prohibition:** Do not introduce databases, Docker, cloud deployment infrastructure, authentication systems, or microservices before the designated phase explicitly approves them.

---

## 2. In-Scope Hazards & Explicit Exclusions

### 2.1 In-Scope Hazards (8 Total)
All modules must reference hazards using their standardized internal identifiers:
1. `flood` — Flood
2. `wildfire` — Wildfire / Forest Fire
3. `landslide` — Landslide
4. `drought` — Drought
5. `cyclone` — Cyclone / Tropical Storm
6. `severe_storm` — Severe Storm / Extreme Convective Weather
7. `volcanic_activity` — Volcanic Activity
8. `avalanche` — Avalanche

### 2.2 Explicit Exclusions
The following categories are strictly excluded from the system:
- **Earthquakes**
- **Tsunamis**
- **Chemical / Industrial Disasters**
- **Terrorist Attacks & Conflict Events**

---

## 3. Standardized Lifecycle Status Taxonomy

Track the progress of every hazard, dataset, and system module using only the following standardized labels:
- `Planned`
- `Researching`
- `Data Ready`
- `Baseline Implemented`
- `Validated`
- `Integrated`
- `Deferred`

---

## 4. Phase Boundaries Reference

* **Phase 0:** Scope, Feasibility and Governance *(Status: PASS WITH LIMITATIONS)*
* **Phase 1:** Repository and Engineering Baseline *(Current Phase)*
* **Phase 2:** Requirements and UX Workflow
* **Phase 3:** Dataset Research and Governance
* **Phase 4:** Ingestion and Geospatial Processing
* **Phase 5:** Database and Persistence
* **Phase 6:** First ML Baseline and Evaluation
* **Phase 7:** API Contracts and Inference
* **Phase 8:** Frontend and Geospatial UI
* **Phase 9:** Hazard-by-Hazard Expansion
* **Phase 10:** Alert Lifecycle and History
* **Phase 11:** Security, Reliability and Deployment
* **Phase 12:** Independent Verification and Freeze
