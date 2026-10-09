# Risk Register and Open Inquiries

**Project:** Satellite-Based Multi-Hazard Disaster Risk Prediction and Early Warning System Using AI/ML  
**Document Ownership:** Risk assessment, failure mode analysis, and technical inquiry log.  
**Cross-References:** Architectural decisions in [decision-log.md](file:///Users/salman/Desktop/satellite-disaster/docs/decision-log.md), Task definitions in [hazard-task-definitions.md](file:///Users/salman/Desktop/satellite-disaster/docs/hazard-task-definitions.md).

---

## 1. Technical & Scientific Risk Register

| Risk ID | Category | Risk Description | Severity | Likelihood | Impact on Project | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-01** | **Scientific Integrity** | **Scientific Overclaiming:** Equating detection with forecasting (e.g., claiming active fire points predict future ignitions, or thermal anomalies guarantee volcanic eruptions). | Critical | High | Loss of academic credibility; invalid scientific claims. | Strict task boundary definitions in [hazard-task-definitions.md](file:///Users/salman/Desktop/satellite-disaster/docs/hazard-task-definitions.md). Explicit label taxonomy distinguishing detection, susceptibility, and forecasting. |
| **RSK-02** | **ML Methodology** | **Data Leakage in Temporal / Spatial Modeling:** Random k-fold splitting leaking spatial autocorrelation or future temporal weather states into training splits. | High | High | Artificially inflated validation metrics; model failure on unobserved events. | Mandatory temporal train/test splits (e.g. training on 2018–2021, testing on 2022–2023) and spatial block cross-validation (buffering training and validation regions). |
| **RSK-03** | **Data Quality** | **Ground-Truth Label Validity & Reporting Bias:** Historical landslide and flood records biased toward roads and urban centers, omitting backcountry occurrences. | High | High | Models learn human settlement proximity rather than physical hazard dynamics. | Combine human-reported catalogs with independent physical proxies (e.g., Copernicus EMS satellite activations, JRC surface water masks). |
| **RSK-04** | **Observational Data** | **Cloud Cover Obscuration in Optical Imagery:** Dense storm clouds mask Sentinel-2/Landsat optical bands during active flood, wildfire, and severe storm events. | High | Critical | Missing optical features at peak disaster moments. | Use radar/SAR (Sentinel-1 C-band) for flood inundation mapping; rely on reanalysis and thermal infrared sensors with cloud-clearing algorithms. |
| **RSK-05** | **Infrastructure & Storage** | **Storage Exhaustion from Large Satellite Scenes:** Global or unclipped Level-1/Level-2 satellite scenes quickly exceed the verified 64 GiB workspace storage ceiling. | High | Medium | Local disk saturation; pipeline crashes. | Enforce bounded geographic pilot regions; clip scenes to bounding boxes upon ingestion; cache only derived tabular features and lightweight Cloud-Optimized GeoTIFFs (COGs). |
| **RSK-06** | **External Services** | **API Rate Limits and Asynchronous Queue Latency:** Third-party providers (Copernicus CDS, CDSE, NASA FIRMS) enforce download quotas or asynchronous queues. | Medium | Medium | Automated ingestion pipelines block or fail during development. | Implement local raw-data caching (`data/raw/` with hash verification); avoid redundant API calls; use synchronous endpoints (e.g., Open-Meteo for ERA5 reanalysis prototyping). |
| **RSK-07** | **Project Schedule** | **Scope Explosion Across 8 Hazards:** Attempting to build production-depth ML pipelines for all 8 hazards in parallel within academic deadlines. | Critical | High | Incomplete, shallow implementations across all modules. | Formal scope tiering: execute full end-to-end slice for Tier-1 candidates (`wildfire` and `flood`), followed by secondary and stretch modules subject to supervisor approval. |
| **RSK-08** | **Environment & Tooling** | **Python Runtime & Native Geospatial Wheel Incompatibilities:** Running cutting-edge Python versions (e.g. 3.14) without pre-compiled ARM64 wheels for geospatial/ML packages (`rasterio`, `torch`). | Medium | Medium | Inability to install packages or build failures on Apple Silicon. | Environment isolation in Phase 1 with verified wheel resolution and installation sanity testing before development begins. |

---

## 2. Open Technical Inquiries

### INQ-01: Geographic Bounding for Pilot Hazards
* **Question:** Which specific geographic bounding boxes should define the Tier-1 pilot regions for Wildfire and Flood?
* **Options:**
  - *Option A:* Selected Indian regional zones (e.g., Central India deciduous forest belts for fire; Assam / Brahmaputra basin or Godavari basin for flood).
  - *Option B:* Standardized international benchmark test areas (e.g., Mediterranean basin, Western US fire zones, European Copernicus EMS flood basins).
* **Current Status:** Open investigation for Phase 2/3; flagged as `PENDING_SUPERVISOR_REVIEW`.

### INQ-02: Weather Reanalysis Data Ingestion Strategy
* **Question:** Should meteorological features be ingested via direct ECMWF Copernicus CDS API (`cdsapi` queued NetCDF downloads) or via Open-Meteo Historical Weather API (which provides immediate REST JSON access to ERA5)?
* **Considerations:** Open-Meteo significantly simplifies local client development and avoids multi-hour CDS queue delays, while direct CDS NetCDF files provide raw native gridded tensors.
* **Current Status:** To be tested and benchmarked during Phase 3.

### INQ-03: Radar Ingestion Pipeline Complexity
* **Question:** Should Sentinel-1 SAR GRD preprocessing (radiometric calibration, Lee speckle filtering, terrain correction) be executed locally via Python (`snappy` / `pyroSAR` / `rasterio`) or ingested as pre-processed surface water extents from Copernicus EMS / Global Flood Monitoring (GFM)?
* **Considerations:** Full raw SAR GRD processing requires significant CPU/memory and native GDAL/SNAP tooling; using open pre-processed flood extent products preserves focus on ML early warning integration.
* **Current Status:** Scheduled for Phase 3/4 evaluation.

---

## 3. Review Gates Requiring Supervisor Input

All inquiries directly impacting academic grading, project deliverables, and module selection require formal review and are logged in [decision-log.md](file:///Users/salman/Desktop/satellite-disaster/docs/decision-log.md).
