# System Requirements, User Personas, and User Stories Specification

**Project:** Satellite-Based Multi-Hazard Disaster Risk Prediction and Early Warning System Using AI/ML
**Phase:** Phase 2 — Requirements and UX Workflow
**Document Ownership:** Authoritative specification for user personas, operational workflows, system requirements, and the Requirements Traceability Matrix.
**Cross-References:** Scope charter in [project-scope.md](file:///Users/salman/Desktop/satellite-disaster/docs/project-scope.md), Hazard task definitions in [hazard-task-definitions.md](file:///Users/salman/Desktop/satellite-disaster/docs/hazard-task-definitions.md), UX Dashboard Specification in [ux-workflow-and-dashboard-spec.md](file:///Users/salman/Desktop/satellite-disaster/docs/ux-workflow-and-dashboard-spec.md), Alert Taxonomy in [alert-and-severity-taxonomy.md](file:///Users/salman/Desktop/satellite-disaster/docs/alert-and-severity-taxonomy.md).

---

## 1. Target User Personas

| Persona ID | Persona Name | Role & Institutional Context | Primary Goal & System Interaction | Domain & Technical Literacy |
| :--- | :--- | :--- | :--- | :--- |
| **PER-01** | **Dr. Aris Thorne** | *Senior Research Scientist / Remote Sensing Evaluator (Academic/Research)* | Evaluates machine learning model calibration, spatial holdout performance, confusion matrices, and physical plausibility across historical disaster benchmark episodes. | High (Remote sensing, statistical machine learning, Python/GIS, atmospheric physics). |
| **PER-02** | **Kavita Raman** | *Regional Disaster Management Officer (State/Provincial Agency)* | Monitors multi-hazard spatial risk across administrative districts and river basins, filters active alerts by synthesized severity, and reviews physical triggering variables before drafting civil advisories. | Moderate (GIS dashboards, emergency standard operating procedures, civil defense). |
| **PER-03** | **Tariq Mansoor** | *Community Emergency Planner / Municipal First Responder* | Requires rapid, unambiguous situational awareness: which local zones are currently flagged under Warning vs. Watch, how fresh the underlying satellite observations are, and what the known observational blind spots are. | Basic-to-Moderate (Web maps, emergency dispatch, local civil defense protocols). |

---

## 2. In-Scope Hazards and Out-of-Scope Boundaries

### 2.1 Eight In-Scope Hazards
All user requirements and system components govern the following eight standardized hazard identifiers:
1. `flood` — Flood (Susceptibility & SAR Inundation Detection)
2. `wildfire` — Wildfire / Forest Fire (Fire Danger Susceptibility & Burn Severity)
3. `landslide` — Landslide (Slope Susceptibility & Dynamic Rainfall Trigger Monitoring)
4. `drought` — Drought (Multi-Index Vegetative and Meteorological Anomaly Monitoring)
5. `cyclone` — Cyclone / Tropical Storm (Storm Intensity & Trajectory Displacement Monitoring)
6. `severe_storm` — Severe Storm / Extreme Convective Weather (Convective Initiation Nowcasting)
7. `volcanic_activity` — Volcanic Activity (Thermal Anomaly & $\text{SO}_2$ Column Density Tracking)
8. `avalanche` — Avalanche (Alpine Terrain Exposure & Weather Advisory Assessment)

### 2.2 Four Strictly Excluded Disaster Categories
The system architecture strictly excludes:
- **Earthquakes:** Solid-earth lithospheric fault ruptures cannot be operationally predicted from satellite imaging.
- **Tsunamis:** Hydrodynamic wave propagation requires deep-ocean pressure sensors (DART buoys) and coastal seismic alarms.
- **Chemical / Industrial Disasters:** Point-source toxic releases are anthropogenic incidents requiring facility SCADA sensors.
- **Terrorist Attacks & Conflict Events:** Human security events fall outside physical Earth observation.

---

## 3. Core System Workflows

```text
[1. Dashboard Access]
       │
       ▼
[2. Geographic Domain Selection] ──► (Filter by Pre-defined Pilot Bounding Box)
       │
       ▼
[3. Hazard Layer Activation] ────► (Select 1 of 8 In-Scope Hazards)
       │
       ▼
[4. Data Freshness & Quality Check] ─► (Evaluate Observation Latency & Cloud Obscuration)
       │
       ▼
[5. Spatial Cell Inspection] ────► (Inspect Task Type, Target Variable, Physical Trigger, Limitations)
       │
       ▼
[6. Alert Ledger Review] ────────► (Inspect CAP Elements, Synthesized Tier, Lifecycle State)
```

---

## 4. User Stories & Measurable Acceptance Criteria

### US-01: Multi-Hazard Spatial Layer Selection (PER-02, PER-03)
* **User Story:** *As a regional disaster management officer, I want to toggle between the eight in-scope hazard layers on an interactive map so that I can inspect spatial risk without cross-hazard conflation or cluttered overlays.*
* **Acceptance Criteria:**
  1. The UI provides discrete layer toggle controls for all eight in-scope hazard identifiers.
  2. Selecting an active hazard completely deactivates previously loaded hazard rasters, replacing legend and scale controls accordingly.
  3. Hazards currently unintegrated (e.g. `cyclone`, `severe_storm`) explicitly display an empty state banner: `[Planned / Researching — Data Ingestion in Phase 4]`.
  4. In strict adherence to project rules, the UI never renders fabricated heatmaps, synthetic predictions, or mock risk contours.

### US-02: Grid-Cell Inspection & Scientific Task Disambiguation (PER-01, PER-02)
* **User Story:** *As a research evaluator, I want clicking any map grid unit to display the exact analytical task type, target variable, observation timestamp, and known physical limitations so that I never mistake real-time detection for future prediction.*
* **Acceptance Criteria:**
  1. Clicking a grid unit opens an inspector side panel displaying:
     * Hazard Identifier and Standard Name.
     * Analytical Task Category: *Observational Detection*, *Static Susceptibility*, *Index Monitoring*, *Nowcasting (0–2h)*, or *Forecasting (24–72h)*.
     * Primary Satellite Platform and Sensor (e.g., *Sentinel-1 C-SAR*, *VIIRS 375m*).
     * Exact Observation Timestamp (`observation_time_utc`).
     * Sensor Latency (hours elapsed since satellite acquisition).
  2. When inspecting susceptibility layers, the UI displays the mandatory scientific notice: *"Susceptibility quantifies conditional terrain probability, not deterministic event timing."*
  3. When inspecting active fire hotspots, the UI displays: *"Active hotspot detection identifies current combustion, not future ignition."*

### US-03: Evidence-Backed Alert Review & Lifecycle Filtering (PER-02, PER-03)
* **User Story:** *As an emergency planner, I want to filter alerts by synthesized operational tiers (Warning, Watch, Advisory) and review underlying physical metrics so that I understand why an alert was triggered.*
* **Acceptance Criteria:**
  1. The alert ledger provides filter toggles for `Warning`, `Watch`, and `Advisory`.
  2. Each alert card itemizes the physical variables and sensor readings triggering the threshold (e.g., `VIIRS FRP: 74 MW`, `Antecedent 3-day Rainfall: 112 mm`).
  3. Alert cards display full lifecycle states: `Active`, `Updated`, `Cleared`, `Expired`, or `Cancelled`.
  4. Each alert displays the mandatory academic disclaimer: *"Experimental research system — does not replace official emergency warnings from NDMA, IMD, NOAA, or ECMWF."*

### US-04: Transparency of Data Missingness, Latency, and Quality (PER-01, PER-02)
* **User Story:** *As a remote sensing analyst, I want to clearly see observation latency and sensor-specific quality degradations so that I am not misled by missing passes or optical cloud blindness.*
* **Acceptance Criteria:**
  1. Optical/multispectral layers (Sentinel-2, Landsat) render a visible hatched pattern over grid cells where cloud obscuration exceeds $20\%$, accompanied by the badge: `Data Quality: Degraded (Optical Cloud Obscuration)`.
  2. Synthetic Aperture Radar (Sentinel-1) layers do **not** apply optical cloud masks, instead displaying radar-specific caveats: `Radar Shadow / Double-Bounce Artifacts Possible in Urban Canyons`.
  3. If elapsed time since the latest satellite overpass exceeds the candidate product freshness threshold, the dashboard displays: `Data Stale (> 48h latency)`.

---

## 5. System Requirements Traceability Matrix

| Requirement ID | Formal Requirement Statement | Governing Specification | Future Acceptance Test Mapping (Phases 7 & 8) |
| :--- | :--- | :--- | :--- |
| **REQ-01** | Support exactly the 8 in-scope hazards and explicitly reject the 4 excluded categories. | Section 2; [project-scope.md](file:///Users/salman/Desktop/satellite-disaster/docs/project-scope.md) | Unit tests verifying API `/api/v1/hazards` returns exactly 8 items and schema validator rejects excluded categories. |
| **REQ-02** | Independent hazard layer toggling with complete state isolation. | Section 4 (US-01); [ux-workflow-and-dashboard-spec.md](file:///Users/salman/Desktop/satellite-disaster/docs/ux-workflow-and-dashboard-spec.md) | Frontend component test confirming activating `wildfire` clears `flood` canvas elements and updates active legend. |
| **REQ-03** | Decouple CAP v1.2 data elements (`severity`, `urgency`, `certainty`) from synthesized user-facing alert tiers (`Warning`, `Watch`, `Advisory`). | [alert-and-severity-taxonomy.md](file:///Users/salman/Desktop/satellite-disaster/docs/alert-and-severity-taxonomy.md) | Schema validation test verifying API alert response contains distinct `cap_elements` dictionary alongside `synthesized_tier`. |
| **REQ-04** | Flag all numerical alert trigger thresholds as provisional and requiring supervisor review. | [alert-and-severity-taxonomy.md](file:///Users/salman/Desktop/satellite-disaster/docs/alert-and-severity-taxonomy.md); [decision-log.md](file:///Users/salman/Desktop/satellite-disaster/docs/decision-log.md) | Governance audit verifying `PENDING_SUPERVISOR_REVIEW` tag accompanies every numerical threshold table. |
| **REQ-05** | Differentiate sensor-specific quality: apply optical cloud masks to optical data only; suppress cloud masking on SAR. | Section 4 (US-04); [ux-workflow-and-dashboard-spec.md](file:///Users/salman/Desktop/satellite-disaster/docs/ux-workflow-and-dashboard-spec.md) | UI render test asserting cloud-cover hatching is applied on Sentinel-2 optical bands and suppressed on Sentinel-1 SAR layers. |
| **REQ-06** | Task-appropriate uncertainty reporting across all risk endpoints without universal Gaussian assumptions. | [api-contracts-spec.md](file:///Users/salman/Desktop/satellite-disaster/docs/api-contracts-spec.md) | Contract test confirming continuous index endpoints return interval bounds, while classification endpoints return class probabilities. |
| **REQ-07** | Graceful UI handling of degraded states: `DATA_UNAVAILABLE`, `DATA_STALE`, and `REGION_UNSUPPORTED`. | [ux-workflow-and-dashboard-spec.md](file:///Users/salman/Desktop/satellite-disaster/docs/ux-workflow-and-dashboard-spec.md); [api-contracts-spec.md](file:///Users/salman/Desktop/satellite-disaster/docs/api-contracts-spec.md) | End-to-end integration test asserting HTTP 404/503 responses render dedicated non-crashing banner cards. |
| **REQ-08** | Absolute prohibition of fabricated predictions, mock heatmaps, or synthetic disaster data in the UI. | Section 4; [AGENTS.md](file:///Users/salman/Desktop/satellite-disaster/AGENTS.md) Rule #9 | Code audit and DOM test asserting zero hardcoded mock predictions or pseudo-random heatmaps exist in production assets. |
