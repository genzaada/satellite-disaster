# Data Provenance and Licensing Manifest

**Document Version:** 1.0
**Phase:** Phase 3 — Dataset Research and Governance
**Operational Status:** `Candidate Sources, not fully verified` (Feasibility experiment pending)
**Applicability:** Master repository registry for official source provenance, licensing terms, access endpoints, and rate limits.

---

## 1. Governance Principles & Integrity Rules

1. **Empirical Verification Requirement:** In compliance with `AGENTS.md` Rule 8 and Rule 9, no dataset in this manifest is marked `Data Ready`. The status remains `Candidate Source, not fully verified` until automated connection, parsing, schema validation, and storage bounds are confirmed by an approved feasibility experiment.
2. **Open Science & Licensing Compliance:** Only datasets with verified open research licenses (NASA Open Data Policy, Copernicus Open Access Licence, Creative Commons CC-BY 4.0) are accepted for pipeline ingestion.
3. **No Credential Exposure:** Authentication tokens, API keys, and access secrets must never be committed to source control (governed by `.gitignore` and `AGENTS.md` Rule 12).

---

## 2. In-Scope Dataset Provenance Catalog

### DS-01: NASA FIRMS Active Fire (VIIRS 375m)
* **Provider Organization:** National Aeronautics and Space Administration (NASA) Earth Science Data and Information System (ESDIS) / LANCE FIRMS.
* **Official Landing Page:** [https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms)
* **API Documentation:** [https://firms.modaps.eosdis.nasa.gov/api/](https://firms.modaps.eosdis.nasa.gov/api/)
* **Official Citation:** Schroeder, W., Oliva, P., Giglio, L., & Csiszar, I. A. (2014). The New VIIRS 375 m active fire detection data product: Algorithm description and initial assessment. *Remote Sensing of Environment*, 143, 85-96.
* **Product Identifiers:**
  - `VNP14IMGTDL_NRT` / `VNP14IMGTDL` (Suomi NPP 375 m VIIRS NRT / Archive)
  - `VJ114IMGTDL_NRT` / `VJ114IMGTDL` (NOAA-20 375 m VIIRS NRT / Archive)
* **License & Terms of Use:** NASA Earth Science Open Data Policy. Free, full, and open sharing of data for research, commercial, and educational applications without royalty. Attribution required.
* **Access Protocol & Endpoints:**
  - RESTful HTTPS API: `https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/{SOURCE}/{BOUNDS}/{DAYS}`
  - Earthdata Bulk Archive Download: `https://firms.modaps.eosdis.nasa.gov/download/`
* **Authentication & Rate Limits:**
  - Requires free registration for an individual `MAP_KEY`.
  - Transactional rate limit: 5,000 requests per 24-hour rolling window per key.
* **Data Format & Delivery:** Tabular CSV / GeoJSON / Shapefile.
* **Sensor Lifecycle & Long-Term Continuity Notice:** NASA has announced that forward operational data product delivery for Suomi-NPP VIIRS will **cease on November 1, 2026**. While Suomi-NPP is valid for retrospective training, operational forward implementations must evaluate cross-satellite compatibility with NOAA-20 (`VJ114IMGTDL`) and NOAA-21 (`VJ214IMGTDL`) before deployment.
* **Operational Verification State:** `Candidate Source, not fully verified (Feasibility Verified in Phase 3.2: 349 records retrieved, 225 qualifying vegetation fires, schema confirmed; Data Ready Pending Supervisor Review)`.

---

### DS-04: Copernicus Global Digital Elevation Model (GLO-30)
* **Provider Organization:** European Space Agency (ESA) / Airbus Defence and Space.
* **Official Landing Page:** [https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model](https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model)
* **Technical Documentation:** Copernicus DEM User Handbook, Issue 4.2 (2020), ESA Document.
* **Official Citation:** European Space Agency, Sinergise (2021). Copernicus Global Digital Elevation Model. Distributed by OpenTopography. DOI: 10.5069/G9028PQB.
* **Product Identifier:** `COP-DEM-GLO-30-DGED` (30 m / 1 arc-second global coverage).
* **License & Terms of Use:** Copernicus Access and Redistribution Licence. Free, full, and open distribution for all peaceful uses with attribution.
* **Access Protocol & Endpoints:**
  - Public AWS Cloud Storage: `s3://copernicus-dem-30m/` (Requester Pays disabled; open global public access via HTTPS `https://copernicus-dem-30m.s3.amazonaws.com/`).
  - OpenTopography REST API: `https://portal.opentopography.org/API/globaldem?demtype=COP30`
* **Tile Footprint & Structure:**
  - Distributed as $1^\circ \times 1^\circ$ geographic tiles referenced to WGS 84 / EGM2008.
  - The Central India pilot region ($21^\circ\text{--}23^\circ\text{N}, 79^\circ\text{--}81^\circ\text{E}$) requires exactly four tiles:
    1. `Copernicus_DSM_COG_10_N21_00_E079_00_DEM.tif`
    2. `Copernicus_DSM_COG_10_N21_00_E080_00_DEM.tif`
    3. `Copernicus_DSM_COG_10_N22_00_E079_00_DEM.tif`
    4. `Copernicus_DSM_COG_10_N22_00_E080_00_DEM.tif`
* **Authentication & Rate Limits:**
  - AWS Direct HTTPS: No authentication required; standard AWS S3 egress throttling.
  - OpenTopography API: Requires free registered API key; 1 query/sec recommended.
* **Operational Verification State:** `Candidate Source, not fully verified` (Pending Phase 3 Feasibility Experiment).

---

### DS-05: ECMWF ERA5-Land Reanalysis (via Open-Meteo & CDS)
* **Provider Organization:** European Centre for Medium-Range Weather Forecasts (ECMWF) / Copernicus Climate Change Service (C3S), served via Open-Meteo Historical Weather API.
* **Official Landing Pages:**
  - Primary Provider: [https://cds.climate.copernicus.eu/](https://cds.climate.copernicus.eu/)
  - Distribution API: [https://open-meteo.com/en/docs/historical-weather-api](https://open-meteo.com/en/docs/historical-weather-api)
* **Official Citation:**
  - Muñoz-Sabater, J., et al. (2021). ERA5-Land: A state-of-the-art global reanalysis dataset for land applications. *Earth System Science Data*, 13(9), 4349-4383.
  - Hersbach, H., et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*, 146(730), 1999-2049.
* **Product Identifier:** `era5_land` (0.1° / ~9 km land-surface hourly reanalysis).
* **License & Terms of Use:**
  - C3S Licence: Open, free access for commercial and non-commercial research with mandatory citation.
  - Open-Meteo Distribution: Creative Commons Attribution 4.0 International (CC-BY 4.0).
* **Access Protocol & Endpoints:**
  - RESTful HTTPS API: `https://archive-api.open-meteo.com/v1/archive`
  - Query Parameters: `latitude`, `longitude`, `start_date`, `end_date`, `hourly=temperature_2m,relative_humidity_2m,dew_point_2m,precipitation,surface_pressure,wind_speed_10m`
* **Authentication & Rate Limits:**
  - Non-commercial tier: No API key required.
  - Rate limits: Up to 10,000 daily API requests; max 600 calls/minute; max 5,000 hourly calls.
* **Format:** Structured JSON time series array / Flat CSV.
* **Scientific Resolution Notice:** Reanalysis is evaluated at $0.05^\circ$ cell centroids via bilinear interpolation. Interpolation is a spatial alignment mechanism and does not increase the physical resolution of the meteorological field beyond its native $0.1^\circ$ (~9 km) resolution.
* **Operational Verification State:** `Candidate Source, not fully verified` (Pending Phase 3 Feasibility Experiment).

---

## 3. Register of Secondary Candidate Datasets

The remaining multi-hazard datasets documented in `docs/dataset-register.md` maintain the following provenance summaries:

| Dataset ID | Hazard | Provider | Format | License | Operational State |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DS-02** | `flood` | ESA Copernicus (Sentinel-1 SAR) | SAFE / COG | Copernicus Open Access | Researching / Unverified |
| **DS-03** | `flood` / `wildfire` | ESA Copernicus (Sentinel-2 MSI) | SAFE / COG | Copernicus Open Access | Researching / Unverified |
| **DS-06** | `landslide` | NASA Earth Science (GLC) | CSV / GeoJSON | NASA Open Data | Researching / Unverified |
| **DS-07** | `drought` | USGS / LP DAAC (MOD13A2) | HDF-EOS / GeoTIFF | USGS Public Domain | Researching / Unverified |
| **DS-08** | `cyclone` | NOAA NCEI (IBTrACS) | NetCDF / CSV | NOAA Public Domain | Researching / Unverified |
| **DS-09** | `volcanic_activity` | Smithsonian GVP / USGS | CSV / JSON | Public Domain | Researching / Unverified |
| **DS-10** | `avalanche` | SLF / EAWS / IMD | XML / JSON / PDF | Open Research / Agency Specific | Researching / Unverified |

---

## 4. Verification Checkpoint Log

| Dataset ID | Documentation Verified | Endpoint Reachability | Schema Validation | Storage Budget Confirmed | Date Verified | Final Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DS-01** (NASA FIRMS VIIRS 375m) | YES | YES (HTTP 200: Live authenticated queries succeeded) | YES (15 columns confirmed, categorical 'l'/'n'/'h', 225 vegetation fires) | YES ($27.4\,\text{KB}$ transferred; 0 bytes retained) | 2026-10-09 | Candidate Source, not fully verified (Feasibility Verified in Phase 3.2; Data Ready Pending Supervisor Review) |
| **DS-04** (Copernicus DEM GLO-30) | YES | YES (HTTP 200 for 4 required tiles) | YES (TIFF magic 42 / Little-Endian verified; raster array decode deferred) | YES ($40\text{--}42\,\text{MB}$ COG tiles verified on AWS S3) | 2026-10-09 | Candidate Source, not fully verified (Header & availability verified; full raster array decode deferred to Phase 4) |
| **DS-05** (ERA5-Land via Open-Meteo) | YES | YES (HTTP 200 across 4 quadrant centroids) | YES (504 hours continuous, 0 missing timestamps, 0.00% missing values) | YES ($0.093\,\text{MB}$ actual transfer; 0 bytes retained) | 2026-10-09 | Candidate Source, not fully verified (Empirically verified across all 6 evidence levels in Phase 3.2; pipeline ingestion pending Phase 4) |
