# Project Scope & Governance Charter

**Project Title:** Satellite-Based Multi-Hazard Disaster Risk Prediction and Early Warning System Using AI/ML  
**Academic Context:** Final-Year B.Tech Computer Science and Engineering Major Project  
**Current Phase:** Phase 0 — Scope, Feasibility, and Governance  
**Governance State:** Provisional Baseline (`PENDING_SUPERVISOR_REVIEW`)  

---

## 1. Executive Summary & Objective

The objective of this major project is to design, implement, evaluate, and benchmark a modular, multi-tier software system combining Earth observation (satellite) data, meteorological/environmental forcing factors, geospatial processing algorithms, machine learning models, a backend API service, and an interactive GIS web interface to assess risks and provide early warnings for distinct natural hazards.

The project strictly emphasizes **evidence-driven engineering**: hazard task types, spatial-temporal units, and analytical models are tailored to physical realities and open data constraints rather than forced into a uniform, artificial architecture.

---

## 2. In-Scope Hazards (8 Total)

The long-term project architecture encompasses eight specific natural hazards, tracked via standardized internal identifiers:

1. **Flood** (`flood`)
2. **Wildfire / Forest Fire** (`wildfire`)
3. **Landslide** (`landslide`)
4. **Drought** (`drought`)
5. **Cyclone / Tropical Storm** (`cyclone`)
6. **Severe Storm / Extreme Convective Weather** (`severe_storm`)
7. **Volcanic Activity** (`volcanic_activity`)
8. **Avalanche** (`avalanche`)

Detailed task formulations, candidate targets, geographic units, temporal horizons, and scientific failure modes for each hazard are authoritatively maintained in [hazard-task-definitions.md](file:///Users/salman/Desktop/satellite-disaster/docs/hazard-task-definitions.md).

---

## 3. Explicitly Excluded Disasters

The following categories of disasters are **strictly out of scope** and will not be addressed at any phase of this project:

* **Earthquakes:** Solid-earth lithospheric fault slip occurs underground and cannot be reliably predicted in operational lead times using orbital optical, multispectral, or radar surface imaging.
* **Tsunamis:** Deep-ocean hydrodynamic wave generation and propagation require dedicated marine ocean-bottom pressure sensors (e.g., DART buoys) and seismic coastal networks, falling outside terrestrial Earth observation.
* **Chemical and Industrial Disasters:** Technological failures, toxic gas leaks, and chemical plant explosions are facility-specific anthropogenic hazards requiring point-source industrial SCADA sensor telemetry.
* **Terrorist Attacks & Conflict Events:** Anthropogenic security crises and warfare fall within law enforcement, defense, and geopolitical domains, outside geophysical and meteorological Earth observation.

---

## 4. Master Development Roadmap

The project follows a sequential 13-phase engineering methodology:

* **Phase 0: Scope, Feasibility and Governance** *(Current Phase)*
* **Phase 1: Repository and Engineering Baseline**
* **Phase 2: Requirements and UX Workflow**
* **Phase 3: Dataset Research and Governance**
* **Phase 4: Ingestion and Geospatial Processing**
* **Phase 5: Database and Persistence**
* **Phase 6: First ML Baseline and Evaluation**
* **Phase 7: API Contracts and Inference**
* **Phase 8: Frontend and Geospatial UI**
* **Phase 9: Hazard-by-Hazard Expansion**
* **Phase 10: Alert Lifecycle and History**
* **Phase 11: Security, Reliability and Deployment**
* **Phase 12: Independent Verification and Freeze**

---

## 5. Scope Tiering: Core Deliverables vs. Stretch Goals

To ensure academic and engineering success within the final-year B.Tech timeframe, the hazard implementation is structured into a provisional planning hypothesis:

### 5.1 Core Capstone Deliverable (Tier 1 — Provisional Initial Focus)
* **Hazards:** Wildfire (`wildfire`) and Flood (`flood`).
* **Justification:** Extensive open Earth observation archives (NASA FIRMS, Copernicus EMS / Sentinel missions) provide accessible ground truth and multispectral/SAR data suitable for demonstration.
* **Scope:** Full vertical slice: automated data ingestion connectors, geospatial feature calculation, baseline ML models, REST API endpoints, and interactive map UI visualization.
* **Status:** `PENDING_SUPERVISOR_REVIEW`.

### 5.2 Secondary Expansion Modules (Tier 2)
* **Hazards:** Landslide (`landslide`) and Drought (`drought`).
* **Scope:** Geospatial susceptibility modeling (landslides) and multi-temporal anomaly index tracking (drought).
* **Status:** `PENDING_SUPERVISOR_REVIEW`.

### 5.3 Stretch Research Goals (Tier 3)
* **Hazards:** Cyclone (`cyclone`), Severe Storm (`severe_storm`), Volcanic Activity (`volcanic_activity`), Avalanche (`avalanche`).
* **Scope:** Exploratory data ingestion, observational anomaly tracking, or literature benchmarking.
* **Status:** `PENDING_SUPERVISOR_REVIEW`.

---

## 6. Lifecycle Status Taxonomy

Every hazard module, dataset, and system component must carry one of the following standardized status labels:

* **`Planned`:** Scoped in project architecture, but formal data acquisition and development have not commenced.
* **`Researching`:** Active literature review, API schema investigation, or feasibility testing underway.
* **`Data Ready`:** Open access verified, schema documented, sample data ingested, and ground-truth labels validated.
* **`Baseline Implemented`:** Minimum working ML model or analytical pipeline producing structured outputs.
* **`Validated`:** Formally evaluated against holdout ground-truth using hazard-appropriate metrics.
* **`Integrated`:** End-to-end data pipeline, ML inference, API endpoints, and frontend map UI verified.
* **`Deferred`:** Postponed due to data availability constraints, lack of open telemetry, or schedule limits.

---

## 7. Academic Governance & Supervision Gates

All key scope commitments, hazard tiering choices, geographic pilot bounding, and evaluation thresholds are provisional until formally reviewed and ratified by the academic project guide/supervisor.

Items flagged with `PENDING_SUPERVISOR_REVIEW` are maintained in [decision-log.md](file:///Users/salman/Desktop/satellite-disaster/docs/decision-log.md).
