# Project Decision Log & Architecture Decision Records (ADR)

**Project:** Satellite-Based Multi-Hazard Disaster Risk Prediction and Early Warning System Using AI/ML  
**Document Ownership:** Authoritative ledger of architectural, scoping, and governance decisions.  
**Cross-References:** Scope overview in [project-scope.md](file:///Users/salman/Desktop/satellite-disaster/docs/project-scope.md), Risk ledger in [risks-and-open-questions.md](file:///Users/salman/Desktop/satellite-disaster/docs/risks-and-open-questions.md).

---

## 1. Decision Records

---

### ADR-001: Scope Boundaries — 8 In-Scope Hazards and 4 Exclusions
* **Date:** 2026-10-09
* **Status:** **Approved Baseline**
* **Context:** A multi-hazard disaster warning system must establish rigorous physical and observational boundaries to avoid overextended, unscientific modeling.
* **Decision:**
  - Enforce 8 in-scope hazards: `flood`, `wildfire`, `landslide`, `drought`, `cyclone`, `severe_storm`, `volcanic_activity`, `avalanche`.
  - Strictly exclude 4 disaster types: Earthquakes, Tsunamis, Industrial/Chemical Disasters, and Terrorist/Conflict Events.
* **Consequences:** Earth observation satellites cannot forecast deep underground tectonic rupture (earthquakes) or open-ocean hydrodynamic waves (tsunamis). Excluding them preserves scientific integrity.
* **Supervisor State:** `PENDING_SUPERVISOR_REVIEW` (To be confirmed with academic guide).

---

### ADR-002: Phased Implementation Tiering (Core vs. Stretch Goals)
* **Date:** 2026-10-09
* **Status:** **Provisional Planning Hypothesis**
* **Context:** Delivering full production ML models across 8 distinct hazards simultaneously is infeasible within a single academic major project timeline.
* **Decision:**
  - **Tier 1 (Core Capstone Deliverable):** Wildfire (`wildfire`) and Flood (`flood`) — full end-to-end slice (Data $\rightarrow$ Features $\rightarrow$ ML $\rightarrow$ API $\rightarrow$ Frontend UI).
  - **Tier 2 (Secondary Modules):** Landslide (`landslide`) and Drought (`drought`) — susceptibility and multi-index models.
  - **Tier 3 (Stretch Research Goals):** Cyclone (`cyclone`), Severe Storm (`severe_storm`), Volcanic Activity (`volcanic_activity`), Avalanche (`avalanche`) — exploratory analysis and benchmark review.
* **Consequences:** Protects the delivery of a working, integrated software system while preserving long-term multi-hazard architecture.
* **Supervisor State:** `PENDING_SUPERVISOR_REVIEW`.

---

### ADR-003: 13-Phase Master Development Roadmap Adherence
* **Date:** 2026-10-09
* **Status:** **Approved Baseline**
* **Context:** Subphase drafts previously blurred Phase 1 (Repository Baseline) with Phase 4 (Geospatial Ingestion).
* **Decision:** Strictly adhere to the 13-phase development roadmap:
  - Phase 0: Scope, Feasibility & Governance *(Current)*
  - Phase 1: Repository & Engineering Baseline (scaffolding, testing, environment isolation, Git hygiene)
  - Phase 2: Requirements & UX Workflow
  - Phase 3: Dataset Research & Governance
  - Phase 4: Ingestion & Geospatial Processing
  - Phase 5: Database & Persistence
  - Phase 6: First ML Baseline & Evaluation
  - Phase 7: API Contracts & Inference
  - Phase 8: Frontend & Geospatial UI
  - Phase 9: Hazard-by-Hazard Expansion
  - Phase 10: Alert Lifecycle & History
  - Phase 11: Security, Reliability & Deployment
  - Phase 12: Independent Verification & Freeze
* **Consequences:** Engineering scaffolding in Phase 1 is isolated from ML data engineering, preventing premature dependencies.

---

### ADR-004: Standardized Lifecycle Status Taxonomy
* **Date:** 2026-10-09
* **Status:** **Approved Baseline**
* **Context:** Project tracking requires clear, non-interchangeable status labels across all hazards and datasets.
* **Decision:** Mandate the following 7 standardized labels across all documentation:
  - `Planned`
  - `Researching`
  - `Data Ready`
  - `Baseline Implemented`
  - `Validated`
  - `Integrated`
  - `Deferred`
* **Consequences:** Eliminates ambiguous claims regarding dataset availability or model completion.

---

### ADR-005: Deferral of Premature Implementation Commitments
* **Date:** 2026-10-09
* **Status:** **Approved Baseline**
* **Context:** Phase 0 should establish scientific evidence and feasibility rather than locking package versions, API keys, or specific frameworks prematurely.
* **Decision:**
  - Python virtual environment runtime (e.g. 3.11 vs 3.14) is deferred to Phase 1 where package wheel resolution can be tested cleanly.
  - Live API testing, credentials, and access quotas are deferred to Phase 3.
  - Storage consumption per pilot is deferred to Phase 3 once geographic bounding boxes are approved.
* **Consequences:** Prevents unverified assumptions from breaking downstream phases.

---

## 2. Register of Pending Supervisor Decisions (`PENDING_SUPERVISOR_REVIEW`)

| Item ID | Topic | Description | Status |
| :--- | :--- | :--- | :--- |
| **SUP-01** | **Scope Exclusions** | Formal academic sign-off on excluding earthquakes, tsunamis, industrial hazards, and conflict events. | `PENDING_SUPERVISOR_REVIEW` |
| **SUP-02** | **Hazard Prioritization** | Formal sign-off on Tier-1 initial focus on Wildfire and Flood as the core capstone demonstration slice. | `PENDING_SUPERVISOR_REVIEW` |
| **SUP-03** | **Geographic Bounding** | Academic guidance on selecting pilot regions (Indian sub-basins vs. international benchmark datasets). | `PENDING_SUPERVISOR_REVIEW` |
| **SUP-04** | **Evaluation Benchmarks** | Academic agreement on target ML performance thresholds (e.g., target ROC-AUC, F1-score, or CSI). | `PENDING_SUPERVISOR_REVIEW` |
