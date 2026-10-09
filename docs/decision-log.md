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

### ADR-006: Common Alerting Protocol (CAP v1.2) Separation & Operational Alert Tier Mapping
* **Date:** 2026-10-09
* **Status:** **Provisional Engineering Proposal**
* **Context:** The system requires an alert representation that complies with open emergency standards (OASIS CAP v1.2) while presenting clear, intuitive alert tiers (Warning, Watch, Advisory) to human operators.
* **Decision:**
  - Decouple CAP v1.2 formal schema elements (`severity`, `urgency`, `certainty`, `msgType`) from synthesized presentation tiers (`Warning`, `Watch`, `Advisory`).
  - Formal alert payloads will serialize raw CAP v1.2 attributes in a dedicated `cap_elements` dictionary, accompanied by an explicit `synthesized_tier` field.
  - Physical triggering thresholds do not originate from CAP, but are grounded in hazard-specific literature.
* **Consequences:** Guarantees interoperability with international civil defense alerting tools while maintaining user-friendly dashboard presentation.
* **Supervisor State:** `PENDING_SUPERVISOR_REVIEW` (Proposed synthesis mapping flagged as provisional).

---

### ADR-007: Task-Appropriate Uncertainty and Sensor-Specific Freshness Policy
* **Date:** 2026-10-09
* **Status:** **Provisional Engineering Proposal**
* **Context:** Non-continuous, multimodal spatial hazard tasks cannot be represented with universal Gaussian confidence intervals or uniform latency thresholds.
* **Decision:**
  - Enforce task-conditioned uncertainty representations: classification tasks report calibrated class posterior probabilities or uncalibrated decision scores; continuous index regressions report empirical residual bounds; detection tasks report sensor confidence flags.
  - Enforce sensor-specific freshness policies: polar-orbiting SAR allows up to 12 days; polar-orbiting optical allows up to 14 days; active thermal fire allows up to 24 hours; atmospheric reanalysis allows up to 48 hours.
  - Restrict optical cloud masking to optical products (Sentinel-2, Landsat); strictly suppress optical cloud masking on Sentinel-1 SAR backscatter.
* **Consequences:** Eliminates unscientific statistical overclaiming and prevents misleading false-negative warnings.
* **Supervisor State:** `PENDING_SUPERVISOR_REVIEW`.

---

### ADR-008: Selection of Retrospective Next-Day Wildfire Occurrence Classification as Initial Analytical Task
* **Date:** 2026-10-09
* **Status:** **Provisional Engineering Proposal**
* **Context:** Phase 3 requires selecting one specific hazard and analytical task for empirical verification. Wildfire offers public, high-quality, open-access datasets (NASA FIRMS VIIRS 375m, ERA5-Land via Open-Meteo, Copernicus DEM GLO-30). However, the analytical formulation must be strictly separated from static susceptibility, real-time hotspot detection, and operational weather forecasting.
* **Decision:**
  - Select *Retrospective Next-Day Fire-Occurrence Classification* as the initial hazard task.
  - Define the target variable $Y_{s,t} \in \{0, 1\}$ as satellite-detectable active vegetation fire occurrence in a $0.05^\circ \times 0.05^\circ$ cell $s$ on calendar date $t$, using categorical VIIRS confidence (`nominal`, `high`) and `type == 0` (presumed vegetation).
  - Explicitly document zero detections as *unconfirmed negatives* due to diurnal overpass gaps, cloud/smoke attenuation, and sub-canopy masking.
  - Establish a common analysis grid of $0.05^\circ \times 0.05^\circ$. Bilinear interpolation of $0.1^\circ$ ERA5-Land reanalysis is adopted strictly as a geometric sampling alignment convenience and does not increase native meteorological resolution.
  - Establish pilot engineering criteria ($\le 30\,\text{MB}$ tabular storage cap, $\le 5\%$ missing weather tolerance) for local computational feasibility, not universal scientific standards.
* **Phase 3.1, 3.2 & 3.3 Feasibility & Independent Audit Outcome (2026-10-09):**
  - **ERA5-Land via Open-Meteo:** PASS across all 6 evidence levels. 504 consecutive hourly observations verified across 4 quadrants; 0 missing timestamps, 0.00% missing values, zero future-leakage verified. (Reanalysis explicitly distinguished from operational forecasts).
  - **Copernicus DEM GLO-30:** PASS (Object & Header level). HTTP 200 confirmed on AWS S3 across 4 required tiles (`N21_E079`, `N21_E080`, `N22_E079`, `N22_E080`, $40\text{--}42\,\text{MB}$ each); TIFF magic 42 verified. Full raster decoding deferred to Phase 4.
  - **NASA FIRMS (VIIRS 375m SP):** PASS across all 6 evidence levels. Authenticated queries using `VIIRS_SNPP_SP` across 3 partitioned intervals (March 15–28, 2023) retrieved 349 active fire records with 15 confirmed schema columns, categorical confidence (`'l'`, `'n'`, `'h'`), and 225 qualifying vegetation fire observations (`type == 0` and nominal/high confidence). Zero credentials exposed or logged.
  - **Spatial Clustering & Corrected Buffer Audit (Phase 3.3.1):** 225 qualifying detections map to **173 unique positive cell-days** across **137 unique grid cells** (0.77% prevalence across $22,400$ total space-time cells).
    - Pre-exclusion distribution: Q1 (NW): 57, Q2 (NE): 26, Q3 (SW): 53, Q4 (SE): 37.
    - Design 1 (2-cell margin / ~20 km total buffer width across boundary): 21 positive cell-days inside buffer excised; 152 post-exclusion evaluation cases remaining (Q1: 46, Q2: 23, Q3: 48, Q4: 35). Reconciles strictly ($152 + 21 = 173$); zero cross-fold overlap.
    - Design 2 (4-cell margin / 20 km each side / ~40 km total buffer width): 49 positive cell-days inside buffer excised; 124 post-exclusion evaluation cases remaining (Q1: 44, Q2: 10, Q3: 39, Q4: 31). Reconciles strictly ($124 + 49 = 173$); zero cross-fold overlap.
    - Crucial finding: Under Design 2, only 10 positive cases remain in Q2, demonstrating that spatial holdout evaluation on a 14-day window is statistically underpowered. Spatial holdout remains strictly provisional.
  - **Sensor Lifecycle Notice:** NASA announced Suomi-NPP VIIRS data delivery will **cease on November 1, 2026**. Operational pipeline forward continuity requires migrating to NOAA-20/21.
  - **Transfer & Storage Audit:** $124,819\,\text{bytes}$ transferred total ($123,795\,\text{bytes}$ dataset payloads, $1,024\,\text{bytes}$ header probes); $0\,\text{bytes}$ retained on disk after cleanup (vastly within $25\,\text{MB}$ cap).
  - **Lifecycle Status:** Datasets updated to `Feasibility Verified (Access & Schema Validated; Data Ready Pending Supervisor Review for Phase 4 Authorization)`. None marked `Data Ready` without formal supervisor sign-off.
* **Consequences:** Provides a rigorous, testable foundation for Phase 4–6 without misleading claims regarding operational forecasting or label certainty.
* **Supervisor State:** `PENDING_SUPERVISOR_REVIEW` (Evaluation partitioning and bounding box).

---

## 2. Register of Pending Supervisor Decisions (`PENDING_SUPERVISOR_REVIEW`)

| Item ID | Topic | Description | Status |
| :--- | :--- | :--- | :--- |
| **SUP-01** | **Scope Exclusions** | Formal academic sign-off on excluding earthquakes, tsunamis, industrial hazards, and conflict events. | `PENDING_SUPERVISOR_REVIEW` |
| **SUP-02** | **Hazard Prioritization** | Formal sign-off on Tier-1 initial focus on Wildfire and Flood as the core capstone demonstration slice. | `PENDING_SUPERVISOR_REVIEW` |
| **SUP-03** | **Geographic Bounding** | Academic guidance on selecting pilot regions (Indian sub-basins vs. international benchmark datasets). | `PENDING_SUPERVISOR_REVIEW` |
| **SUP-04** | **Evaluation Benchmarks** | Academic agreement on target ML performance thresholds (e.g., target ROC-AUC, F1-score, or CSI). | `PENDING_SUPERVISOR_REVIEW` |
| **SUP-05** | **CAP Alert Tier Synthesis** | Academic review of proposed synthesis mapping from CAP v1.2 elements to operational tiers (Warning, Watch, Advisory). | `PENDING_SUPERVISOR_REVIEW` |
| **SUP-06** | **Physical Alert Thresholds** | Formal review and empirical calibration of provisional multi-hazard physical alert triggering thresholds. | `PENDING_SUPERVISOR_REVIEW` |
| **SUP-07** | **Wildfire Module Selection** | Academic sign-off on selecting retrospective next-day wildfire occurrence classification (NASA FIRMS + ERA5-Land + Copernicus DEM) as the first end-to-end hazard pipeline. | `PENDING_SUPERVISOR_REVIEW` |
| **SUP-08** | **Central India Bounding Box & Spatial Partitioning** | Academic review of the proposed Central India pilot bounding box ($21^\circ\text{--}23^\circ\text{N}, 79^\circ\text{--}81^\circ\text{E}$) and provisional 4-block spatial evaluation design with buffer zones (labeled provisional due to 14-day sample size limitations in Q2). | `PENDING_SUPERVISOR_REVIEW` |
