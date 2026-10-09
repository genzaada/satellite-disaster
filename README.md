# Satellite-Based Multi-Hazard Disaster Risk Prediction and Early Warning System Using AI/ML

**Academic Context:** Final-Year B.Tech Computer Science and Engineering Major Project  
**Current Status:** Phase 1 in progress (Repository Foundation and Engineering Baseline)  
**Governance Baseline:** Phase 0 completed with status `PASS WITH LIMITATIONS`  

---

## 1. Project Purpose

This project develops an evidence-driven, multi-tier software system combining Earth observation (satellite) data, meteorological reanalysis, geospatial processing algorithms, machine learning models, a backend API service, and an interactive GIS web dashboard to assess risk and generate early warnings for distinct natural hazards.

The project emphasizes scientific defensibility: analytical tasks and spatial-temporal units are tailored to observational constraints rather than forced into uniform assumptions.

---

## 2. Scope Boundaries

### 2.1 In-Scope Hazards (8 Total)
The long-term system architecture encompasses eight natural hazards:
1. **Flood** (`flood`): Inundation detection and spatial susceptibility mapping.
2. **Wildfire / Forest Fire** (`wildfire`): Fire danger susceptibility forecasting and post-event burn severity (dNBR) mapping.
3. **Landslide** (`landslide`): Slope susceptibility modeling conditionally modulated by rainfall triggering thresholds.
4. **Drought** (`drought`): Multi-index vegetative and meteorological anomaly tracking (VHI / SPEI).
5. **Cyclone / Tropical Storm** (`cyclone`): Intensity estimation and storm center trajectory displacement monitoring.
6. **Severe Storm / Extreme Convective Weather** (`severe_storm`): Convective initiation nowcasting.
7. **Volcanic Activity** (`volcanic_activity`): Caldera thermal anomaly detection and $\text{SO}_2$ plume column density tracking.
8. **Avalanche** (`avalanche`): ATES terrain exposure mapping and high-altitude meteorological advisories.

### 2.2 Explicit Exclusions
The following disaster categories are strictly out of scope:
* **Earthquakes** (Solid-earth tectonic fault rupture cannot be reliably predicted in operational lead-times via satellite surface imaging).
* **Tsunamis** (Oceanic hydrodynamic propagation requires deep-sea DART pressure sensor arrays and seismic coastal alarms).
* **Chemical & Industrial Disasters** (Anthropogenic point-source technological failures requiring facility SCADA sensors).
* **Terrorist Attacks & Conflict Events** (Anthropogenic security crises outside geophysical Earth observation).

---

## 3. Master Development Roadmap

The project is governed by a sequential 13-phase development roadmap:

| Phase | Description | Status |
| :--- | :--- | :--- |
| **Phase 0** | Scope, Feasibility and Governance | `PASS WITH LIMITATIONS` |
| **Phase 1** | Repository and Engineering Baseline | **In Progress** |
| **Phase 2** | Requirements and UX Workflow | Planned |
| **Phase 3** | Dataset Research and Governance | Planned |
| **Phase 4** | Ingestion and Geospatial Processing | Planned |
| **Phase 5** | Database and Persistence | Planned |
| **Phase 6** | First ML Baseline and Evaluation | Planned |
| **Phase 7** | API Contracts and Inference | Planned |
| **Phase 8** | Frontend and Geospatial UI | Planned |
| **Phase 9** | Hazard-by-Hazard Expansion | Planned |
| **Phase 10** | Alert Lifecycle and History | Planned |
| **Phase 11** | Security, Reliability and Deployment | Planned |
| **Phase 12** | Independent Verification and Freeze | Planned |

---

## 4. Governance & Technical Documentation

Authoritative specifications are maintained in the [`docs/`](docs/) directory:

* [`docs/project-scope.md`](docs/project-scope.md) — Scope charter, governance definitions, and lifecycle taxonomy.
* [`docs/hazard-task-definitions.md`](docs/hazard-task-definitions.md) — Comprehensive 13-point scientific analysis for all eight hazards.
* [`docs/dataset-feasibility-matrix.md`](docs/dataset-feasibility-matrix.md) — Source feasibility audit across candidate datasets.
* [`docs/dataset-register.md`](docs/dataset-register.md) — Technical data asset catalog with access protocols and schemas.
* [`docs/risks-and-open-questions.md`](docs/risks-and-open-questions.md) — Risk register and technical inquiry ledger.
* [`docs/decision-log.md`](docs/decision-log.md) — Architecture Decision Records (ADRs) and supervisor review register.

---

## 5. Current Implementation State

* **Phase 0 Status:** Completed with `PASS WITH LIMITATIONS`. Core governance, hazard task specifications, and data feasibility matrices are established. Formal academic supervisor review and live dataset credential testing remain pending.
* **Engineering State:** Phase 1.2 completed. Minimal runnable frontend and backend skeletons are established:
  * **Backend:** FastAPI service with Pydantic schemas, isolated Python 3.11 virtual environment, and automated tests for `GET /health`.
  * **Frontend:** React + Vite + TypeScript application shell styled with Tailwind CSS, displaying project scope, diagnostic card querying `/health`, and dashboard placeholders (no fabricated maps or mock risk scores).
* **Data & ML State:** Machine learning models, live satellite ingestion connectors, database persistence, and spatial analytics are **not yet implemented** (scheduled for Phases 3–7).

---

## 6. Planned Architecture (Planned — Progressive Rollout)

The future target architecture comprises:
* **Frontend (Phase 8):** Interactive GIS web dashboard (React + Vite + TypeScript, Leaflet/MapLibre) displaying multi-hazard risk maps, active alerts, and time-series charts.
* **Backend (Phase 7):** Asynchronous REST API service (FastAPI) handling hazard inference requests, alert dispatching, and geospatial querying.
* **ML & Geospatial Engine (Phases 4 & 6):** Python-based feature extraction and machine learning inference pipelines consuming Earth observation imagery and reanalysis data.

---

## 7. Local Development Setup & Verification

### 7.1 Backend Setup (Python 3.11)
```bash
# 1. Create and activate isolated virtual environment
/opt/homebrew/bin/python3.11 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r backend/requirements-dev.txt

# 3. Run backend automated tests
pytest backend/tests/ -v

# 4. Start local development API server (port 8000)
uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

### 7.2 Frontend Setup (Node.js & Vite)
```bash
# 1. Install dependencies from lockfile
cd frontend
npm install

# 2. Run TypeScript type check
npx tsc --noEmit

# 3. Run production build check
npm run build

# 4. Start local development UI server (port 5173)
npm run dev
```

---

## 8. Safety & Operational Disclaimer

> [!WARNING]
> **Experimental Academic Project:** This software system is developed strictly for academic, research, and educational demonstration purposes as part of a B.Tech capstone major project. It is **not** an operational emergency early warning system and must **never** be used as a substitute for official disaster warnings issued by national meteorological and disaster management authorities (e.g., IMD, NDMA, NOAA, ECMWF, USGS).

